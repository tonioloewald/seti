#!/usr/bin/env python3
"""Phase 2, step 4 battery item 0: the difference-image centroid gate (prereg §5).

The dominant false positive at TESS's ~21" pixels is a background eclipsing binary whose
dimming bleeds into the K dwarf's aperture. Difference imaging localises where the flux
actually dropped: build the mean out-of-transit image minus the mean in-transit image, take
its flux-weighted centroid, and compare to the target's pixel position. If the transit
source sits more than ~1 pixel off-target, it is a background blend and is killed.

Runs on the identity-cross-check survivors (k05). For each, the transit ephemeris
(period / epoch / duration) is re-derived from the cached light curve by the same BLS as the
search (deterministic), then a TESS target-pixel file (or TESScut FFI cutout) is fetched and
the difference-image centroid computed. Parallel, resumable.

Output: data/manifests/kdwarf_T0_residuals_centroid.csv  (survivors + centroid offset)
A candidate that survives BOTH identity and this gate is a genuine residual for human
difference-imaging review and conventional follow-up -- never, by this pipeline, a detection.
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

IDENT = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_identity.csv")
OUT = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_centroid.csv")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])
TESS_PIX_ARCSEC = 21.0
OFFSET_THRESH_PIX = 1.0          # > 1 pixel off-target => background blend (pre-data decision)


def _ephemeris(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"))
    r = bls_detect(d["time"], d["flux"], PERIODS, DURS)
    return r["period"], r["t0"], r["duration"]


def centroid_offset(ra, dec, period, t0, duration, dldir):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from lightkurve import search_targetpixelfile, search_tesscut
    coord = SkyCoord(ra * u.deg, dec * u.deg)
    sr = search_targetpixelfile(coord, mission="TESS")
    tpf = None
    if len(sr):
        tpf = sr[0].download(download_dir=dldir)
    else:
        sc = search_tesscut(coord)
        if len(sc):
            tpf = sc[0].download(cutout_size=11, download_dir=dldir)
    if tpf is None:
        return None, "no_tpf"
    t = tpf.time.value
    flux = np.asarray(tpf.flux.value, float)                       # (T, ny, nx)
    ph = ((t - t0) / period + 0.5) % 1.0 - 0.5
    hw = min(0.5 * duration / period, 0.25)                        # in-transit half-width (phase)
    intr = np.abs(ph) < hw
    oot = (np.abs(ph) > 1.5 * hw) & (np.abs(ph) < 0.48)            # away from transit + secondary
    if intr.sum() < 3 or oot.sum() < 5:
        return None, "too_few_cadences"
    diff = np.nanmedian(flux[oot], axis=0) - np.nanmedian(flux[intr], axis=0)  # +ve = flux lost
    diff = diff - np.nanmedian(diff)
    diff = np.clip(diff, 0, None)
    if not np.isfinite(diff).any() or diff.sum() <= 0:
        return None, "no_diff_signal"
    ny, nx = diff.shape
    Y, X = np.mgrid[0:ny, 0:nx]
    w = diff.sum()
    cx, cy = float((diff * X).sum() / w), float((diff * Y).sum() / w)
    try:
        px, py = tpf.wcs.world_to_pixel(coord)                     # target pixel in the TPF frame
        px, py = float(px), float(py)
    except Exception:
        return None, "wcs_fail"
    off_pix = float(np.hypot(cx - px, cy - py))
    return off_pix, "ok"


def _vet(task):
    sid, ra, dec = task
    signal.signal(signal.SIGALRM, _on_alarm); signal.alarm(VET_TIMEOUT)
    dldir = tempfile.mkdtemp(prefix="tpf_")
    try:
        period, t0, duration = _ephemeris(sid)
        off, status = centroid_offset(ra, dec, period, t0, duration, dldir)
    except Exception as e:
        off, status = None, f"err:{type(e).__name__}"
    finally:
        signal.alarm(0)
        shutil.rmtree(dldir, ignore_errors=True)
    verdict = ("on_target" if (status == "ok" and off is not None and off <= OFFSET_THRESH_PIX)
               else "background_blend" if status == "ok" else status)
    return {"source_id": sid, "offset_pix": off,
            "offset_arcsec": (off * TESS_PIX_ARCSEC if off is not None else np.nan),
            "centroid_status": status, "centroid_verdict": verdict}


def main():
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 6
    res = pd.read_csv(IDENT, dtype={"source_id": str})
    surv = res[res["identity"] == "unknown"].copy()
    print(f"identity survivors to centroid-vet: {len(surv)} on {workers} workers", flush=True)
    done = {}
    if os.path.exists(OUT):
        prev = pd.read_csv(OUT, dtype={"source_id": str})
        done = {r.source_id: r._asdict() for r in prev.itertuples(index=False)}
    todo = surv[~surv["source_id"].isin(done)]
    tasks = [(r["source_id"], r["ra_deg"], r["dec_deg"]) for _, r in todo.iterrows()]

    rows = list(done.values()); t0 = time.time(); n = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_vet, t) for t in tasks]
        for fut in as_completed(futs):
            rows.append(fut.result()); n += 1
            if n % 50 == 0:
                pd.DataFrame(rows).to_csv(OUT, index=False)
                ot = sum(1 for r in rows if r.get("centroid_verdict") == "on_target")
                print(f"  {n}/{len(tasks)} ({time.time()-t0:.0f}s, {ot} on-target so far)", flush=True)
    out = pd.DataFrame(rows)
    full = surv.merge(out, on="source_id", how="left")
    full.to_csv(OUT, index=False)
    vc = out["centroid_verdict"].value_counts()
    print("\n=== CENTROID GATE ===")
    for k, v in vc.items():
        print(f"  {k:20s} {v}")
    on = full[full["centroid_verdict"] == "on_target"]
    print(f"\n  {len(on)} candidates are ON-TARGET after identity + centroid "
          f"(genuine residuals for human review). wrote {OUT}")


if __name__ == "__main__":
    main()
