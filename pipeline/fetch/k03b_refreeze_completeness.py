#!/usr/bin/env python3
"""Battery v3: refresh ONLY the classification-aware completeness C_i in a frozen calibration,
using the current (red-noise-aware) battery, while leaving the registered detection bars, cohort
edges, and nulls EXACTLY as frozen. The bars are battery-independent (deterministic BLS null) and
registered; the reviewer challenged only the completeness, which depends on battery(). C_i(box) is
flat-bottom-driven and unchanged within injection sampling; C_i(tail) weakens because the red-noise
floor is more conservative about calling a shallow tail 'variable'. Run per tier via KRUN.

    KRUN=T0   .venv/bin/python pipeline/fetch/k03b_refreeze_completeness.py --workers 8
    KRUN=T0T1 .venv/bin/python pipeline/fetch/k03b_refreeze_completeness.py --workers 8
"""
import os, sys, json, time
import numpy as np, pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, os.path.join(ROOT, "pipeline", "fetch"))
from core.noise import assign_cohorts                                   # noqa: E402
from core.stats import poisson_fmax                                     # noqa: E402
import k03_calibrate as k03                                             # _recover/_templ use new battery via import

RUN = os.environ.get("KRUN", "T0")
TIERS = {"T0": [0], "T0T1": [0, 1]}.get(RUN, [0])
NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
CALPATH = os.path.join(ROOT, "data", "manifests", f"kdwarf_calibration_{RUN}.json")


def main():
    args = sys.argv[1:]
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 8
    cal = json.load(open(CALPATH))
    edges = np.array(cal["cohort_edges_scatter"])
    z = cal["fwer_sigma"]
    inj_per = cal.get("inj_per_cohort", 300)
    thr = {int(c): cal["cohorts"][c]["threshold_sde"] for c in cal["cohorts"]}

    nf = pd.read_parquet(NOISE); nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf.status == "ok") & np.isfinite(nf.scatter_ppm) & (nf.tier.isin(TIERS))].reset_index(drop=True)
    ok["cohort"] = assign_cohorts(ok.scatter_ppm.to_numpy() / 1e6, edges)
    print(f"{RUN}: {len(ok)} ok stars (tiers {TIERS}); bars {thr} FROZEN; recomputing C_i with battery v3",
          flush=True)

    sub = pd.concat([ok[ok.cohort == c].sample(min(inj_per, int((ok.cohort == c).sum())), random_state=c)
                     for c in range(k03.N_COHORTS)])
    tasks = [(r["source_id"], int(r["cohort"]), fam, dep, thr[int(r["cohort"])], r["scatter_ppm"] / 1e6, z)
             for fam in k03.FAMILIES for dep in k03.DEPTHS for _, r in sub.iterrows()]
    agg = {(fam, f"{d:.3f}", c): [] for fam in k03.FAMILIES for d in k03.DEPTHS for c in range(k03.N_COHORTS)}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(k03._recover, t): (t[2], f"{t[3]:.3f}") for t in tasks}
        for j, fut in enumerate(as_completed(futs)):
            res = fut.result()
            if res is not None:
                fam, ds = futs[fut]; agg[(fam, ds, res[0])].append(res[1])
            if (j + 1) % 3000 == 0:
                print(f"  inject {j+1}/{len(tasks)} ({time.time()-t0:.0f}s)", flush=True)

    Cgrid = {fam: {f"{d:.3f}": {} for d in k03.DEPTHS} for fam in k03.FAMILIES}
    for fam in k03.FAMILIES:
        for dep in k03.DEPTHS:
            ds = f"{dep:.3f}"
            for c in range(k03.N_COHORTS):
                v = agg[(fam, ds, c)]; Cgrid[fam][ds][c] = float(np.mean(v)) if v else None
    fmax = {}
    for fam in k03.FAMILIES:
        sCi = sum((Cgrid[fam]["0.010"][c] or 0) * int((ok.cohort == c).sum()) for c in range(k03.N_COHORTS))
        fmax[fam] = poisson_fmax(sCi) if sCi > 0 else None

    old = cal["completeness"]
    print("\n  C_i @1%   family   frozen -> v3   (f_max@1%)")
    for fam in k03.FAMILIES:
        n = [Cgrid[fam]["0.010"][c] or 0 for c in range(3)]
        if fam in old and "0.010" in old[fam]:
            o = [old[fam]["0.010"][str(c)] or 0 for c in range(3)]
            sCo = sum(o[c] * int((ok.cohort == c).sum()) for c in range(3))
            print(f"    {fam:7s} {[round(x,3) for x in o]} -> {[round(x,3) for x in n]}   "
                  f"{poisson_fmax(sCo):.2e} -> {fmax[fam]:.2e}")
        else:
            print(f"    {fam:7s} (new) -> {[round(x,3) for x in n]}   f_max {fmax[fam]:.2e}")

    cal["completeness"] = Cgrid
    cal["illustrative_fmax_at_1pct"] = fmax
    cal["battery_version"] = "v3 (red-noise-aware depth variability; single 0.15 asymmetry boundary)"
    cal["note"] = (cal.get("note", "") +
                   f" | Battery-v3 C_i refresh ({RUN}, tiers {TIERS}): bars/edges/nulls unchanged; "
                   "completeness recomputed with the red-noise-aware depth-variability test. "
                   "C_i(box) unchanged within sampling; C_i(tail) reduced (more conservative floor).")
    json.dump(cal, open(CALPATH, "w"), indent=2)
    print(f"\n  wrote {CALPATH}")


if __name__ == "__main__":
    main()
