#!/usr/bin/env python3
"""Audit: verify every number in the K-dwarf bright-tier paper against committed artifacts.

The one risk a referee can't check from the prose alone is whether the frozen manifest, the
per-stage residual lists, and the calibrations actually carry the numbers the paper claims.
This reconstructs each claim for BOTH reported tiers -- T0 (G<11) and the combined T0+T1
(G<12) -- from the committed files and reports PASS/FAIL, so the prose and the data are
checkably consistent. (Battery v2, 2026-06-09: the depth->radius EB criterion and noise-aware
depth-variability test changed only classification, not the bars or completeness; the f_max
checks below confirm the limit is unchanged.)
"""
import os, sys, json
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.stats import poisson_fmax                                   # noqa: E402
from core.noise import assign_cohorts                                 # noqa: E402
M = os.path.join(ROOT, "data", "manifests")
ok_all = True


def chk(label, got, want, tol=0):
    global ok_all
    p = (abs(got - want) <= tol) if isinstance(want, (int, float)) else (got == want)
    ok_all &= p
    print(f"  [{'PASS' if p else 'FAIL'}] {label}: artifact={got}  paper={want}")


def audit_tier(run, E):
    print(f"\n==== TIER {run} ====")
    cal = json.load(open(os.path.join(M, f"kdwarf_calibration_{run}.json")))
    chk(f"{run} n cohorts", cal["n_cohorts"], 3)
    chk(f"{run} cohort bars (SDE)",
        sorted(round(cal["cohorts"][c]["threshold_sde"], 1) for c in cal["cohorts"]), E["bars"])
    chk(f"{run} cohort median scatter (ppm)",
        sorted(round(cal["cohorts"][c]["median_scatter_ppm"]) for c in cal["cohorts"]), E["scatter"])

    res = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals.csv"), dtype={"source_id": str})
    chk(f"{run} k04 residuals", len(res), E["residuals"])
    idn = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_identity.csv"), dtype={"source_id": str})
    chk(f"{run} identity survivors (unknown)", int((idn.identity == "unknown").sum()), E["survive"])
    chk(f"{run} identity known cleared", int((idn.identity != "unknown").sum()), E["cleared"])
    cen = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_centroid.csv"), dtype={"source_id": str})
    v = cen.centroid_verdict
    chk(f"{run} centroid on_target", int((v == "on_target").sum()), E["on_target"])
    chk(f"{run} centroid background_blend", int((v == "background_blend").sum()), E["blend"])
    chk(f"{run} centroid uncentroidable", int((~v.isin(["on_target", "background_blend"])).sum()), E["uncentroidable"])
    chk(f"{run} centroid total = identity survivors", len(cen), E["survive"])
    ms = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_multisector.csv"), dtype={"source_id": str})
    mv = ms.ms_verdict
    chk(f"{run} recurrence recurs", int((mv == "recurs").sum()), E["recurs"])
    chk(f"{run} recurrence single-sector artifacts", int((mv == "single_sector_artifact").sum()), E["artifact"])
    chk(f"{run} recurrence untestable", int((~mv.isin(["recurs", "single_sector_artifact"])).sum()), E["untestable"])
    chk(f"{run} recurrence total = on_target", len(ms), E["on_target"])
    tri = pd.read_csv(os.path.join(M, f"kdwarf_{run}_recurring_triage.csv"), dtype={"source_id": str})
    tv = tri.verdict
    chk(f"{run} triage eclipsing_binary", int((tv == "eclipsing_binary").sum()), E["EB"])
    chk(f"{run} triage natural_planet", int((tv == "natural_planet").sum()), E["planet"])
    chk(f"{run} triage disintegrating_body", int((tv == "disintegrating_body").sum()), E["disint"])
    chk(f"{run} triage RESIDUAL", int((tv == "RESIDUAL").sum()), E["RESIDUAL"])
    chk(f"{run} triage total = recurring", len(tri), E["recurs"])
    r = tri[tv == "RESIDUAL"]
    chk(f"{run} resolvable-regime residuals (depth>0.3%)", int((r.depth > 0.003).sum()), E["resolvable"])

    # f_max recomputed from frozen completeness x searched cohort counts (zero-detection basis)
    nf = pd.read_parquet(os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet"))
    nf["source_id"] = nf["source_id"].astype(str)
    sel = nf[(nf.status == "ok") & np.isfinite(nf.scatter_ppm) & (nf.tier.isin(E["tiers"]))].copy()
    edges = np.array(cal["cohort_edges_scatter"])
    sel["cohort"] = assign_cohorts(sel.scatter_ppm.to_numpy() / 1e6, edges)
    chk(f"{run} searched stars", len(sel), E["searched"], tol=5)
    for fam, want, tol in E["fmax"]:
        sumCi = sum((cal["completeness"][fam]["0.010"][str(c)] or 0) * int((sel.cohort == c).sum())
                    for c in range(3))
        chk(f"{run} f_max({fam}) at 1%", poisson_fmax(sumCi), want, tol=tol)


def main():
    print("MANIFEST")
    man = pd.read_csv(os.path.join(M, "kdwarf_sample.csv.gz"), dtype={"source_id": str})
    chk("frozen manifest size", len(man), 175968)

    audit_tier("T0", dict(
        bars=[7.6, 7.7, 8.5], scatter=[507, 938, 1268], tiers=[0], searched=12100,
        residuals=765, survive=666, cleared=99,
        on_target=337, blend=310, uncentroidable=19,
        recurs=53, artifact=194, untestable=90,
        EB=5, planet=35, disint=1, RESIDUAL=12, resolvable=2,
        fmax=[("box", 2.75e-4, 0.25e-4), ("tail", 4.17e-4, 0.35e-4)]))

    audit_tier("T0T1", dict(
        bars=[7.3, 8.1, 8.7], scatter=[595, 1262, 2051], tiers=[0, 1], searched=44202,
        residuals=3036, survive=2821, cleared=215,
        on_target=1121, blend=1580, uncentroidable=120,
        recurs=140, artifact=578, untestable=403,
        EB=17, planet=92, disint=4, RESIDUAL=27, resolvable=2,
        fmax=[("box", 8.34e-5, 0.35e-5), ("tail", 1.19e-4, 0.12e-4)]))

    print("\n" + ("ALL CHECKS PASS -- paper and artifacts agree." if ok_all
                  else "** DISCREPANCY -- paper and artifacts disagree; investigate **"))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
