#!/usr/bin/env python3
"""Phase 2, step 2 (prereg §6.2): pull light curves + the outlier-blind noise floor.

Resumable, tiered, brightest-first. For each star in the frozen manifest
(`kdwarf_sample.csv.gz`) this fetches a TESS (fallback Kepler) light curve, detrends it,
clips ONLY upward outliers (a downward clip would delete transits), computes the
outlier-blind MAD scatter (core.noise.robust_scatter -- the cohort metric, prereg §5a),
caches a compact detrended light curve, and appends one noise-floor row. It does **not**
run BLS or look at any candidate: this is the cheap noise-floor pass that feeds the
per-cohort calibration (step 3), staged so the expensive search comes later.

Tiers (brightest-first, nested; a pre-data implementation decision -- see AMENDMENTS.md):
  T0: G < 11   T1: 11 <= G < 12   T2: 12 <= G < 13.  Analysed in tier order; this is the
  analysis *order* within the one frozen manifest, not a separate sample.

Resumable: skips source_ids already in the noise-floor table; checkpoints periodically.
Usage:  k02_lightcurves.py [--max N] [--gmax G] [--mission TESS|Kepler|both]

Outputs:
  data/derived/kdwarf_noise_floor.parquet   one row/star (source_id, tier, mission, scatter...)
  data/lightcurves/<source_id>.npz          compact detrended LC (time, flux)  [gitignored]
"""
import os, sys, time, warnings, tempfile, shutil, signal
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

STAR_TIMEOUT = 90          # seconds per star before a hung MAST request is abandoned


class _Timeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise _Timeout()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.noise import robust_scatter                                    # noqa: E402

MAN = os.path.join(ROOT, "data", "manifests", "kdwarf_sample.csv.gz")
OUT = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
TIER_EDGES = [11.0, 12.0, 13.0]            # brightest-first tiers (pre-data decision)


def tier_of(g):
    for i, e in enumerate(TIER_EDGES):
        if g < e:
            return i
    return len(TIER_EDGES)


def fetch_one(ra, dec, mission_pref, download_dir=None):
    """Return (time, flux, mission, label, cadence_d) for the best available light curve,
    detrended and upward-only-clipped, or raise. `download_dir` isolates concurrent downloads."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    from lightkurve import search_lightcurve
    coord = SkyCoord(ra, dec, unit="deg")
    missions = (["TESS", "Kepler"] if mission_pref == "both" else [mission_pref])
    for mis in missions:
        sr = search_lightcurve(coord, mission=mis, radius=5 * u.arcsec)
        if len(sr) == 0:
            continue
        sub = None
        if mis == "TESS":
            for auth in ["SPOC", "TESS-SPOC", "QLP"]:
                s = sr[[a == auth for a in sr.table["author"]]]
                if len(s):
                    sub = s; break
        else:
            s = sr[[a == "Kepler" for a in sr.table["author"]]]
            sub = s if len(s) else None
        if sub is None:
            continue
        lc = sub[0].download(download_dir=download_dir).remove_nans().normalize()
        lc = lc.flatten(window_length=401).remove_outliers(sigma_upper=5, sigma_lower=1e9)
        t = np.asarray(lc.time.value, float); f = np.asarray(lc.flux, float)
        good = np.isfinite(t) & np.isfinite(f)
        t, f = t[good], f[good]
        if t.size < 100:
            continue
        cad = float(np.median(np.diff(np.sort(t))))
        label = f"{mis}:{sub.table['author'][0]}:s{int(lc.meta.get('SECTOR', lc.meta.get('QUARTER', -1)))}"
        return t, f, mis, label, cad
    raise RuntimeError("no_usable_lightcurve")


def process_star(s, mission):
    """Fetch + characterise one star (thread-safe: isolated download dir, own npz)."""
    sid = s["source_id"]
    rec = {"source_id": sid, "tier": tier_of(s["g_mag"]), "g_mag": float(s["g_mag"])}
    tmp = tempfile.mkdtemp(prefix="lk_")               # isolate astroquery/lightkurve cache
    signal.signal(signal.SIGALRM, _on_alarm)           # per-star wall-clock timeout so a hung
    signal.alarm(STAR_TIMEOUT)                          # MAST request cannot stall a worker
    try:
        tt, ff, mis, label, cad = fetch_one(float(s["ra_deg"]), float(s["dec_deg"]), mission, tmp)
        sc = robust_scatter(ff)
        np.savez_compressed(os.path.join(LCDIR, f"{sid}.npz"), time=tt, flux=ff)
        rec.update({"mission": mis, "label": label, "n_points": int(tt.size),
                    "cadence_d": cad, "scatter_ppm": sc * 1e6, "status": "ok"})
    except _Timeout:
        rec.update({"mission": "", "label": "", "n_points": 0, "cadence_d": np.nan,
                    "scatter_ppm": np.nan, "status": "err:timeout"})
    except Exception as e:
        rec.update({"mission": "", "label": "", "n_points": 0, "cadence_d": np.nan,
                    "scatter_ppm": np.nan, "status": f"err:{type(e).__name__}"})
    finally:
        signal.alarm(0)
        shutil.rmtree(tmp, ignore_errors=True)
    return rec


def main():
    args = sys.argv[1:]
    def opt(name, default, cast=str):
        return cast(args[args.index(name) + 1]) if name in args else default
    maxn = opt("--max", 10**9, int)
    gmin = opt("--gmin", 0.0, float)
    gmax = opt("--gmax", 99.0, float)
    sample = opt("--sample", 0, int)          # >0: random-sample across the range (for the
    seed = opt("--seed", 0, int)              #     full-manifest noise floor; not tier-ordered)
    mission = opt("--mission", "TESS")
    workers = opt("--workers", 6, int)        # concurrent MAST downloads (I/O-bound)
    os.makedirs(LCDIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    man = pd.read_csv(MAN, dtype={"source_id": str})
    man = man[(man["g_mag"] >= gmin) & (man["g_mag"] < gmax)].sort_values("g_mag").reset_index(drop=True)
    done = set()
    rows = []
    if os.path.exists(OUT):
        prev = pd.read_parquet(OUT); prev["source_id"] = prev["source_id"].astype(str)
        done = set(prev["source_id"]); rows = prev.to_dict("records")
    if "--retry" in args:                  # re-attempt TRANSIENT failures only -- not
        def transient(st):                 # err:RuntimeError (genuinely no usable light curve)
            st = str(st)
            return st.startswith("err:") and not st.startswith("err:RuntimeError")
        retry_ids = {r["source_id"] for r in rows if transient(r.get("status"))}
        rows = [r for r in rows if r["source_id"] not in retry_ids]
        done -= retry_ids
        print(f"  retry: re-attempting {len(retry_ids)} transient failures (not no-data)", flush=True)
    todo = man[~man["source_id"].isin(done)]
    if sample > 0:
        todo = todo.sample(min(sample, len(todo)), random_state=seed)  # representative spread
        maxn = min(maxn, sample)
    todo = todo.head(maxn)
    total = len(todo)
    print(f"manifest in [G{gmin},{gmax}): {len(man):,} | done: {len(done):,} | "
          f"this run: {total:,} on {workers} workers", flush=True)

    t0 = time.time(); n = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(process_star, s.to_dict(), mission) for _, s in todo.iterrows()]
        for fut in as_completed(futs):
            rows.append(fut.result()); n += 1
            if n % 25 == 0:
                pd.DataFrame(rows).to_parquet(OUT, index=False)
                ok = sum(1 for r in rows if r.get("status") == "ok")
                rate = n / max(time.time() - t0, 1e-9)
                eta = (total - n) / max(rate, 1e-9)
                print(f"  {n}/{total}  ({time.time()-t0:.0f}s, {rate:.1f}/s, ETA {eta/60:.0f}m, "
                      f"{ok} ok total)", flush=True)
    df = pd.DataFrame(rows); df.to_parquet(OUT, index=False)
    try:
        ok = df[df["status"] == "ok"]
        print(f"done this run: +{n} processed; total {len(df):,} ({len(ok):,} ok).", flush=True)
        if len(ok):
            print(f"  scatter (ppm): median={ok['scatter_ppm'].median():.0f}  "
                  f"p10={ok['scatter_ppm'].quantile(.1):.0f}  p90={ok['scatter_ppm'].quantile(.9):.0f}")
            print(f"  by tier: " + "  ".join(f"T{t}={(ok['tier']==t).sum()}"
                                             for t in sorted(ok['tier'].unique())))
    except (ValueError, OSError):
        pass            # stdout may be closed under a background redirect; the parquet is saved


if __name__ == "__main__":
    main()
