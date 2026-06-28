#!/usr/bin/env python
"""EXPLORATORY post-data re-vet of the T0T1T2 recurring-candidate triage for narrow / shallow
secondary eclipses missed by the frozen battery.

Why: the frozen battery's secondary-eclipse test takes a MEDIAN over a +/-0.05-phase window and
fires only if secondary_depth > 0.3 x primary_depth. For narrow eclipses that window (~3x the
eclipse width) dilutes a real secondary to ~zero (TIC 156074324: true secondary 0.7% in FFI /
1.7% in SPOC 2-min, measured 0.0 by the frozen test), and the 0.3x-primary relative threshold
misses shallow-secondary low-mass / grazing EBs (1.7%/8.6% = 0.20 < 0.30) even when measured.

This re-vet is EXPLORATORY (post-unblind): it does NOT alter the frozen battery, calibration, the
detection bars, or f_max. It re-measures the secondary eclipse at each candidate's TRUE BLS period
with a window MATCHED to the BLS transit duration, and a SIGNIFICANCE criterion (secondary depth vs
out-of-eclipse scatter), to identify residuals that are in fact eclipsing binaries.

Validation built in: applied to the 108 frozen-battery natural_planet objects, the new secondary
flag must stay rare (planets have no secondary) -- printed as a false-positive check.
"""
import os, sys
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect  # noqa: E402

PERIODS = np.arange(0.5, 13.0, 0.02); DURS = np.array([0.05, 0.1, 0.2])
LCDIR = os.path.join(ROOT, "data", "lightcurves")
TRIAGE = os.path.join(ROOT, "data", "manifests", "kdwarf_T0T1T2_recurring_triage.csv")
SIG = 5.0   # secondary significance threshold (sigma vs out-of-eclipse scatter)


def revet(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"), allow_pickle=True)
    t, f = np.asarray(d["time"], float), np.asarray(d["flux"], float)
    g = np.isfinite(t) & np.isfinite(f); t, f = t[g], f[g]
    if len(t) < 200:
        return None
    bls = bls_detect(t, f, PERIODS, DURS)
    P, t0, dur = bls["period"], bls["t0"], bls["duration"]
    ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
    hw = max(0.5 * dur / P, 0.005)                       # window matched to BLS eclipse duration
    oot = np.abs(ph) > 0.30                              # out-of-eclipse (also off secondary at 0.5? no)
    base = np.median(f[oot]) if oot.sum() > 10 else np.median(f)
    # out-of-eclipse scatter, excluding both eclipse phases, for the significance floor
    clean = (np.abs(ph) > 3 * hw) & (np.abs(np.abs(ph) - 0.5) > 3 * hw)
    sig_pt = np.std(f[clean]) if clean.sum() > 10 else np.std(f)
    msec = np.abs(np.abs(ph) - 0.5) < hw
    mpri = np.abs(ph) < hw
    if msec.sum() < 5 or mpri.sum() < 5:
        return None
    sec_depth = base - np.median(f[msec])
    pri_depth = base - np.median(f[mpri])
    sec_sigma = sec_depth / (sig_pt / np.sqrt(msec.sum())) if sig_pt > 0 else np.nan
    return {"source_id": sid, "trueP": P, "dur_h": dur * 24, "hw": hw,
            "pri_depth": pri_depth, "sec_depth": sec_depth, "sec_sigma": sec_sigma,
            "sec_over_pri": sec_depth / pri_depth if pri_depth > 0 else np.nan,
            "is_EB_new": bool(sec_depth > 0 and sec_sigma > SIG)}


def main():
    tri = pd.read_csv(TRIAGE, dtype={"source_id": str})
    rows = []
    for _, r in tri.iterrows():
        out = revet(r["source_id"])
        if out:
            out["old_verdict"] = r["verdict"]; out["triage_depth"] = r["depth"]
            rows.append(out)
    rv = pd.DataFrame(rows)

    # false-positive check on frozen-battery planets
    pl = rv[rv["old_verdict"] == "natural_planet"]
    print(f"=== VALIDATION: secondary flag rate among {len(pl)} frozen natural_planet ===")
    print(f"   flagged as EB by new secondary test: {int(pl['is_EB_new'].sum())} "
          f"({100*pl['is_EB_new'].mean():.1f}%)  [should be low: planets have no secondary]")

    res = rv[rv["old_verdict"] == "RESIDUAL"]
    flipped = res[res["is_EB_new"]]
    print(f"\n=== RESIDUALS re-vetted: {len(res)} | newly identified as EB (secondary >{SIG}sigma): {len(flipped)} ===")
    cols = ["source_id", "trueP", "dur_h", "pri_depth", "sec_depth", "sec_sigma", "sec_over_pri", "triage_depth"]
    if len(flipped):
        print(flipped.sort_values("sec_sigma", ascending=False)[cols].to_string(index=False))

    # focus: the 6 resolvable residuals (triage depth > 0.3%)
    resolv = res[res["triage_depth"] > 0.003]
    print(f"\n=== the {len(resolv)} RESOLVABLE residuals (depth>0.3%), new secondary test ===")
    print(resolv.sort_values("triage_depth", ascending=False)[
        cols + ["is_EB_new"]].to_string(index=False))

    out = os.path.join(ROOT, "data", "manifests", "kdwarf_T0T1T2_secondary_revet.csv")
    rv.to_csv(out, index=False)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
