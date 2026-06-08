#!/usr/bin/env python3
"""Phase 2, step 4 battery: multi-sector recurrence (prereg §5 instrumental/systematics).

The dominant residual after identity + centroid is the single-sector long-period BLS false
alarm: with only 2-4 transits in one 27-day TESS sector, correlated/red noise can mimic a
periodic dip. The clean discriminant is recurrence -- a real transit repeats at the SAME
ephemeris in every sector the star was observed; a red-noise false alarm does not.

For each on-target candidate (k06): re-derive its ephemeris from the cached single-sector
light curve, fetch ALL available TESS sectors, and at the fixed (period, t0) measure the
transit depth + SNR in each sector independently. Verdict:
  recurs                detected (SNR>3, depth>0) in >=2 independent sectors  -> SURVIVES
  single_sector_artifact  >=2 sectors observed but the dip appears in <2       -> rejected
  single_sector_only      only 1 sector exists -> recurrence untestable here   -> inconclusive
  no_data / err

Parallel, resumable. Output: data/manifests/kdwarf_T0_residuals_multisector.csv
"""
import os, sys, time, tempfile, shutil, warnings, signal
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

VET_TIMEOUT = 120
class _Timeout(Exception): pass
def _on_alarm(signum, frame): raise _Timeout()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.environ.get("KRUN", "T0")            # T0 (default) | T0T1 (combined)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect                                  # noqa: E402
from core.noise import robust_scatter                              # noqa: E402

CEN = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_centroid.csv")
OUT = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_multisector.csv")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])


def _ephemeris(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"))
    r = bls_detect(d["time"], d["flux"], PERIODS, DURS)
    return r["period"], r["t0"], r["duration"]


def fetch_sectors(ra, dec, dldir):
    """Return list of (sector, time, flux) for every usable SPOC TESS light curve."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from lightkurve import search_lightcurve
    sr = search_lightcurve(SkyCoord(ra*u.deg, dec*u.deg), mission="TESS", radius=5*u.arcsec)
    if len(sr) == 0:
        return []
    sub = sr[[a in ("SPOC", "TESS-SPOC") for a in sr.table["author"]]]
    if len(sub) == 0:
        return []
    out = []
    for i in range(len(sub)):
        try:
            lc = sub[i].download(download_dir=dldir).remove_nans().normalize()
            lc = lc.flatten(window_length=401).remove_outliers(sigma_upper=5, sigma_lower=1e9)
            t = np.asarray(lc.time.value, float); f = np.asarray(lc.flux, float)
            g = np.isfinite(t) & np.isfinite(f)
            if g.sum() < 100:
                continue
            sec = int(lc.meta.get("SECTOR", -i - 1))
            out.append((sec, t[g], f[g]))
        except Exception:
            continue
    return out


def _vet(task):
    sid, ra, dec = task
    signal.signal(signal.SIGALRM, _on_alarm); signal.alarm(VET_TIMEOUT)
    dldir = tempfile.mkdtemp(prefix="ms_")
    try:
        period, t0, duration = _ephemeris(sid)
        secs = fetch_sectors(ra, dec, dldir)
        # de-duplicate by sector number
        bysec = {}
        for sec, t, f in secs:
            bysec.setdefault(sec, (t, f))
        n_sectors = len(bysec)
        if n_sectors == 0:
            return {"source_id": sid, "n_sectors": 0, "n_detected": 0, "ms_verdict": "no_data"}
        hw = min(0.5 * duration / period, 0.2)
        n_det = 0; depths = []
        for sec, (t, f) in bysec.items():
            ph = ((t - t0) / period + 0.5) % 1.0 - 0.5
            intr = np.abs(ph) < hw
            oot = (np.abs(ph) > 1.5 * hw) & (np.abs(ph) < 0.48)
            if intr.sum() < 3 or oot.sum() < 10:
                continue
            base = np.median(f[oot]); dep = base - np.median(f[intr])
            sc = robust_scatter(f)
            snr = dep * np.sqrt(intr.sum()) / sc if sc > 0 else 0
            if dep > 0 and snr > 3:
                n_det += 1; depths.append(dep)
        if n_sectors == 1:
            verdict = "single_sector_only"
        elif n_det >= 2:
            verdict = "recurs"
        else:
            verdict = "single_sector_artifact"
        return {"source_id": sid, "n_sectors": n_sectors, "n_detected": n_det,
                "ms_verdict": verdict}
    except Exception as e:
        return {"source_id": sid, "n_sectors": -1, "n_detected": 0, "ms_verdict": f"err:{type(e).__name__}"}
    finally:
        signal.alarm(0)
        shutil.rmtree(dldir, ignore_errors=True)


def main():
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 6
    cen = pd.read_csv(CEN, dtype={"source_id": str})
    on = cen[cen["centroid_verdict"] == "on_target"].copy()
    print(f"on-target candidates for recurrence test: {len(on)} on {workers} workers", flush=True)
    rcols = ["source_id", "n_sectors", "n_detected", "ms_verdict"]   # worker result columns
    done = {}
    if os.path.exists(OUT):
        prev = pd.read_csv(OUT, dtype={"source_id": str})
        done = {r["source_id"]: {c: r[c] for c in rcols} for _, r in prev.iterrows()}
    if "--retry" in sys.argv:                  # re-attempt transient no_data/err failures
        done = {k: v for k, v in done.items()
                if not str(v.get("ms_verdict", "")).startswith(("no_data", "err"))}
    todo = on[~on["source_id"].isin(done)]
    tasks = [(r["source_id"], r["ra_deg"], r["dec_deg"]) for _, r in todo.iterrows()]
    rows = list(done.values()); t0 = time.time(); n = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_vet, t) for t in tasks]
        for fut in as_completed(futs):
            rows.append(fut.result()); n += 1
            if n % 50 == 0:
                pd.DataFrame(rows).to_csv(OUT, index=False)
                rec = sum(1 for r in rows if r.get("ms_verdict") == "recurs")
                print(f"  {n}/{len(tasks)} ({time.time()-t0:.0f}s, {rec} recurring)", flush=True)
    out = pd.DataFrame(rows)[rcols]            # only result cols, so re-merge can't collide
    full = on.merge(out, on="source_id", how="left")
    full.to_csv(OUT, index=False)
    vc = out["ms_verdict"].value_counts()
    print("\n=== MULTI-SECTOR RECURRENCE ===")
    for k, v in vc.items():
        print(f"  {k:24s} {v}")
    rec = full[full["ms_verdict"] == "recurs"]
    sso = full[full["ms_verdict"] == "single_sector_only"]
    print(f"\n  recurring (real, repeat across sectors): {len(rec)}")
    print(f"  single-sector-only (recurrence untestable, inconclusive): {len(sso)}")
    print(f"  rejected as single-sector artifacts: {(out['ms_verdict']=='single_sector_artifact').sum()}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
