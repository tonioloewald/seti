#!/usr/bin/env python3
"""Audit: verify every number in the T0 paper against the committed repository artifacts.

The one risk a referee can't check from the prose alone is whether the frozen manifest, the
per-stage residual lists, and the calibration actually carry the numbers the paper claims.
This reconstructs each claim from the committed files and reports PASS/FAIL, so the prose and
the data are checkably consistent.
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


def main():
    print("MANIFEST")
    man = pd.read_csv(os.path.join(M, "kdwarf_sample.csv.gz"), dtype={"source_id": str})
    chk("frozen manifest size", len(man), 175968)

    print("CALIBRATION (kdwarf_calibration_T0.json)")
    cal = json.load(open(os.path.join(M, "kdwarf_calibration_T0.json")))
    chk("n cohorts", cal["n_cohorts"], 3)
    bars = sorted(round(cal["cohorts"][c]["threshold_sde"], 1) for c in cal["cohorts"])
    chk("cohort bars (SDE)", bars, [7.6, 7.7, 8.5])
    scat = sorted(round(cal["cohorts"][c]["median_scatter_ppm"]) for c in cal["cohorts"])
    chk("cohort median scatter (ppm)", scat, [507, 938, 1268])

    print("CASCADE")
    res = pd.read_csv(os.path.join(M, "kdwarf_T0_residuals.csv"), dtype={"source_id": str})
    chk("k04 residuals", len(res), 1358)
    idn = pd.read_csv(os.path.join(M, "kdwarf_T0_residuals_identity.csv"), dtype={"source_id": str})
    chk("identity total", len(idn), 1358)
    chk("identity survivors (unknown)", int((idn.identity == "unknown").sum()), 1223)
    chk("identity known cleared", int((idn.identity != "unknown").sum()), 135)
    cen = pd.read_csv(os.path.join(M, "kdwarf_T0_residuals_centroid.csv"), dtype={"source_id": str})
    v = cen.centroid_verdict
    chk("centroid on_target", int((v == "on_target").sum()), 616)
    chk("centroid background_blend", int((v == "background_blend").sum()), 546)
    chk("centroid uncentroidable", int((~v.isin(["on_target", "background_blend"])).sum()), 61)
    chk("centroid total", len(cen), 1223)
    ms = pd.read_csv(os.path.join(M, "kdwarf_T0_residuals_multisector.csv"), dtype={"source_id": str})
    mv = ms.ms_verdict
    chk("recurrence recurs", int((mv == "recurs").sum()), 86)
    chk("recurrence single-sector artifacts", int((mv == "single_sector_artifact").sum()), 388)
    chk("recurrence untestable", int(mv.isin(["single_sector_only", "no_data"]).sum()), 142)
    chk("recurrence total", len(ms), 616)
    tri = pd.read_csv(os.path.join(M, "kdwarf_T0_recurring_triage.csv"), dtype={"source_id": str})
    tv = tri.verdict
    chk("triage eclipsing_binary", int((tv == "eclipsing_binary").sum()), 6)
    chk("triage natural_planet", int((tv == "natural_planet").sum()), 10)
    chk("triage sub-resolution (RESIDUAL+disintegrating)",
        int(tv.isin(["RESIDUAL", "disintegrating_body"]).sum()), 70)
    chk("triage total (recurring)", len(tri), 86)

    print("FOLLOW-UP and LIMIT")
    chk("follow-up total (142+70+61)", 142 + 70 + 61, 273)
    # recompute f_max from frozen completeness x the searched-T0 cohort counts (noise floor)
    nf = pd.read_parquet(os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet"))
    nf["source_id"] = nf["source_id"].astype(str)
    t0 = nf[(nf.status == "ok") & np.isfinite(nf.scatter_ppm) & (nf.tier == 0)].copy()
    edges = np.array(cal["cohort_edges_scatter"])
    t0["cohort"] = assign_cohorts(t0.scatter_ppm.to_numpy() / 1e6, edges)
    chk("searched T0 stars", len(t0), 12100, tol=5)
    for fam, want in [("box", 2.8e-4), ("tail", 3.4e-4)]:
        sumCi = sum((cal["completeness"][fam]["0.010"][str(c)] or 0) * int((t0.cohort == c).sum())
                    for c in range(3))
        fmax = poisson_fmax(sumCi)
        chk(f"f_max({fam}) at 1%", round(fmax, 5), want, tol=0.2e-4)

    print("\n" + ("ALL CHECKS PASS — paper and artifacts agree." if ok_all
                  else "** DISCREPANCY — paper and artifacts disagree; investigate **"))
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
