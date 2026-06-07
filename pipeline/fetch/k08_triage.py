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


def _triage(task):
    sid, ra, dec = task
    dldir = tempfile.mkdtemp(prefix="tri_")
    try:
        secs = fetch_sectors(ra, dec, dldir)
        if not secs:
            return {"source_id": sid, "n_sectors": 0, "verdict": "no_data"}
        t = np.concatenate([s[1] for s in secs]); f = np.concatenate([s[2] for s in secs])
        o = np.argsort(t); t, f = t[o], f[o]
        r = bls_detect(t, f, PERIODS, DURS)
        b = battery(t, f, r["period"], r["t0"], robust_scatter(f))
        return {"source_id": sid, "n_sectors": len(secs), "period": r["period"],
                "depth": b.get("depth", np.nan), "verdict": b["verdict"],
                "flat_bottom": b.get("flat_bottom", np.nan), "asymmetry": b.get("asymmetry", np.nan),
                "secondary_depth": b.get("secondary_depth", np.nan), "odd_even": b.get("odd_even", np.nan),
                "depth_cv": b.get("depth_cv", np.nan), "sin_r2": b.get("sin_r2", np.nan)}
    except Exception as e:
        return {"source_id": sid, "n_sectors": -1, "verdict": f"err:{type(e).__name__}"}
    finally:
        shutil.rmtree(dldir, ignore_errors=True)


def main():
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 6
    ms = pd.read_csv(MS, dtype={"source_id": str})
    rec = ms[ms["ms_verdict"] == "recurs"].copy()
    print(f"recurring candidates to triage: {len(rec)} on {workers} workers", flush=True)
    tasks = [(r["source_id"], r["ra_deg"], r["dec_deg"]) for _, r in rec.iterrows()]
    rows = []; t0 = time.time(); n = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_triage, t) for t in tasks]
        for fut in as_completed(futs):
            rows.append(fut.result()); n += 1
            if n % 25 == 0:
                print(f"  {n}/{len(tasks)} ({time.time()-t0:.0f}s)", flush=True)
    out = pd.DataFrame(rows)
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
