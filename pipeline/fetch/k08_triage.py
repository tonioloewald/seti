#!/usr/bin/env python3
"""Phase 2, step 4 closure: final triage of the recurring T0 candidates (prereg §5).

The 86 candidates that recur across sectors (k07) are real, repeating transits. This stage
re-runs the full natural-explanation battery on their STITCHED multi-sector light curves --
higher SNR than the single sector the search used, a precise refined ephemeris, and (for
short-period systems) many more eclipses for the secondary / odd-even tests. The result
sorts them into eclipsing binaries, planet candidates (the byproduct catalogue), and any
genuine RESIDUAL anomaly that survives even this deeper look.

Output: data/manifests/kdwarf_T0_recurring_triage.csv
"""
import os, sys, time, tempfile, shutil, warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.environ.get("KRUN", "T0")            # T0 (default) | T0T1 (combined)
FETCH = os.path.join(ROOT, "pipeline", "fetch")
sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, FETCH)
from core.detect import bls_detect                                  # noqa: E402
from core.noise import robust_scatter                              # noqa: E402
from k04_search import battery                                     # noqa: E402
from k07_multisector import fetch_sectors                          # noqa: E402

MS = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_multisector.csv")
OUT = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_recurring_triage.csv")
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])


def _periods_for(p_k04):
    """Period grid for the triage re-fit. Pinned to a narrow ±1% band around the k04 SEARCH period
    (which defines the candidate and to which the calibration/completeness is keyed), so the longer
    multi-sector baseline refines t0/duration/period *within* the search-grid uncertainty but cannot
    lock onto a harmonic alias. An unconstrained re-search here aliased `1397924585409290240` to
    11.74 d (= 4 × 2.94 d), corrupting its morphology/EB metrics (see IMPLEMENTATION_LOG, P2-k08-period).
    Falls back to the full grid if no search period is carried."""
    if p_k04 and np.isfinite(p_k04) and p_k04 > 0:
        step = max(p_k04 * 0.0005, 0.001)
        return np.arange(p_k04 * 0.99, p_k04 * 1.01 + step, step)
    return PERIODS


def _sector_coherence(secs, period, t0, dur):
    """Per-sector depth-coherence diagnostic (for the follow-up list). A clean recurring transit has
    a stable per-sector depth uncorrelated with per-sector scatter; a noise/systematics-driven flag
    shows depth tracking scatter (corr -> 1) or an intermittent depth (detected in a fraction of
    sectors). Returns (n_with_dip, frac_detected, depth_cv_sector, depth_scatter_corr)."""
    hw = min(0.5 * dur / period, 0.2)
    deps, scs = [], []
    n_obs = 0
    for _, tt, ff in secs:
        ph = ((tt - t0) / period + 0.5) % 1.0 - 0.5
        intr = np.abs(ph) < hw
        oot = (np.abs(ph) > 1.5 * hw) & (np.abs(ph) < 0.45)
        if intr.sum() < 3 or oot.sum() < 10:
            continue
        n_obs += 1
        sc = robust_scatter(ff); dep = np.median(ff[oot]) - np.median(ff[intr])
        snr = dep * np.sqrt(intr.sum()) / sc if sc > 0 else 0
        if dep > 0 and snr > 3:
            deps.append(dep); scs.append(sc)
    deps, scs = np.array(deps), np.array(scs)
    n_det = len(deps)
    frac = float(n_det / n_obs) if n_obs else np.nan
    cv = float(np.std(deps) / np.mean(deps)) if n_det >= 2 and np.mean(deps) > 0 else np.nan
    corr = float(np.corrcoef(deps, scs)[0, 1]) if n_det >= 3 else np.nan
    return n_det, frac, cv, corr


def _triage(task):
    sid, ra, dec, p_k04 = task
    dldir = tempfile.mkdtemp(prefix="tri_")
    try:
        secs = fetch_sectors(ra, dec, dldir)
        if not secs:
            return {"source_id": sid, "n_sectors": 0, "verdict": "no_data"}
        t = np.concatenate([s[1] for s in secs]); f = np.concatenate([s[2] for s in secs])
        o = np.argsort(t); t, f = t[o], f[o]
        r = bls_detect(t, f, _periods_for(p_k04), DURS)
        b = battery(t, f, r["period"], r["t0"], robust_scatter(f), r["duration"])
        n_det, frac, scv, corr = _sector_coherence(secs, r["period"], r["t0"], r["duration"])
        return {"source_id": sid, "n_sectors": len(secs), "period": r["period"],
                "depth": b.get("depth", np.nan), "verdict": b["verdict"],
                "flat_bottom": b.get("flat_bottom", np.nan), "asymmetry": b.get("asymmetry", np.nan),
                "secondary_depth": b.get("secondary_depth", np.nan), "odd_even": b.get("odd_even", np.nan),
                "depth_cv": b.get("depth_cv", np.nan), "sin_r2": b.get("sin_r2", np.nan),
                # per-sector coherence diagnostic (follow-up vetting; not a hard gate)
                "sec_detected": n_det, "sec_frac_detected": frac,
                "sec_depth_cv": scv, "sec_depth_scatter_corr": corr}
    except Exception as e:
        return {"source_id": sid, "n_sectors": -1, "verdict": f"err:{type(e).__name__}"}
    finally:
        shutil.rmtree(dldir, ignore_errors=True)


def main():
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 6
    ms = pd.read_csv(MS, dtype={"source_id": str})
    rec = ms[ms["ms_verdict"] == "recurs"].copy()
    print(f"recurring candidates to triage: {len(rec)} on {workers} workers", flush=True)
    has_p = "period" in rec.columns
    tasks = [(r["source_id"], r["ra_deg"], r["dec_deg"], float(r["period"]) if has_p else np.nan)
             for _, r in rec.iterrows()]
    rows = []; t0 = time.time(); n = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_triage, t) for t in tasks]
        for fut in as_completed(futs):
            rows.append(fut.result()); n += 1
            if n % 25 == 0:
                print(f"  {n}/{len(tasks)} ({time.time()-t0:.0f}s)", flush=True)
    out = pd.DataFrame(rows)
    # attach the host's single-sector scatter (variability proxy), so the residuals' activity
    # comparison (vs planet hosts) is reconstructable from this committed file alone.
    nfp = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
    if os.path.exists(nfp):
        nf = pd.read_parquet(nfp); nf["source_id"] = nf["source_id"].astype(str)
        out = out.merge(nf[["source_id", "scatter_ppm"]].rename(columns={"scatter_ppm": "host_scatter_ppm"}),
                        on="source_id", how="left")
    out.to_csv(OUT, index=False)
    print("\n=== RECURRING-CANDIDATE TRIAGE (multi-sector battery) ===")
    for k, v in out["verdict"].value_counts().items():
        print(f"  {k:22s} {v}")
    resid = out[out["verdict"] == "RESIDUAL"]
    print(f"\n  RESIDUAL anomalies surviving the deep multi-sector battery: {len(resid)}")
    if len(resid):
        cols = ["source_id", "n_sectors", "period", "depth", "flat_bottom", "asymmetry",
                "secondary_depth", "odd_even", "depth_cv"]
        print(out[out["verdict"] == "RESIDUAL"][cols].to_string(index=False))
    print(f"\n  wrote {OUT}")


if __name__ == "__main__":
    main()
