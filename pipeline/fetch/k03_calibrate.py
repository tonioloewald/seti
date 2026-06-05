#!/usr/bin/env python3
"""Phase 2, step 3 (prereg §6.3): calibrate-and-FREEZE the detection thresholds.

Real-data version of runners/pilot_calibration.py. Operates on the cached light curves +
noise floor from step 2, and produces the frozen calibration that step 4 (unblind) will
apply. The order is the integrity crux:

  - Cohorts: bin the ok stars by their outlier-blind MAD scatter (prereg §5a).
  - Per-cohort empirical null: run BLS on each star's REAL light curve; the per-cohort null
    (delta0, sigma0, genomic-control lambda) is estimated from the BULK of the SDE
    distribution (Efron) -- robust to any real transit, which sits in the tail. The FWER bar
    is delta0 + z*sigma0 with z = Phi^-1(1-1/N_total), N_total = the WHOLE frozen manifest.
  - Per-family completeness C_i: inject the frozen forward-model anomaly library into the
    real light curves over a depth x period grid; recovery = SDE > the cohort bar.

CRITICAL: this script **does not reveal which real stars exceed the bar** -- it computes and
freezes the null, the threshold, and C_i, and stops. Unblinding (listing survivors) is step
4, a separate run against the frozen calibration. Calibrating here cannot peek at candidates.

Output (committed, small): data/derived/kdwarf_calibration.json
"""
import os, sys, json, time, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect, single_event_detect                      # noqa: E402
from core.stats import empirical_null, cohort_threshold, fwer_sigma, poisson_fmax  # noqa: E402
from core.noise import cohort_edges, assign_cohorts                          # noqa: E402
from core.transit import make_transit, multi_epoch_depths                    # noqa: E402

NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
OUT = os.path.join(ROOT, "data", "derived", "kdwarf_calibration.json")
MANIFEST_N = 175968                         # N_total: the whole frozen manifest (FWER bar)
N_COHORTS = 3
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])
# injection-recovery grid (per morphology family); modest for a first real calibration
DEPTHS = [0.005, 0.01, 0.02]
INJ_PERIODS = [3.1, 7.3]
FAMILIES = ["planet", "box", "tail"]


def load_lc(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"))
    return d["time"], d["flux"]


def main():
    nf = pd.read_parquet(NOISE)
    nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf["status"] == "ok") & np.isfinite(nf["scatter_ppm"])].reset_index(drop=True)
    print(f"ok stars: {len(ok)}", flush=True)
    if len(ok) < 3 * N_COHORTS:
        print("too few stars for calibration; pull more first."); return

    # ---- cohorts -----------------------------------------------------------------------
    scat = (ok["scatter_ppm"].to_numpy() / 1e6)
    edges = cohort_edges(scat, n_cohorts=N_COHORTS)
    ok["cohort"] = assign_cohorts(scat, edges)

    # ---- per-cohort null from real BLS SDE (bulk-robust) -------------------------------
    t0 = time.time(); sde = np.full(len(ok), np.nan)
    for i, sid in enumerate(ok["source_id"]):
        try:
            t, f = load_lc(sid)
            sde[i] = bls_detect(t, f, PERIODS, DURS)["sde"]
        except Exception:
            pass
        if (i + 1) % 25 == 0:
            print(f"  null BLS {i+1}/{len(ok)} ({time.time()-t0:.0f}s)", flush=True)
    ok["sde"] = sde
    z = fwer_sigma(MANIFEST_N)
    cohorts = {}
    for c in range(N_COHORTS):
        s = ok.loc[ok["cohort"] == c, "sde"].to_numpy()
        s = s[np.isfinite(s)]
        d0, s0, lam = empirical_null(s)
        thr = cohort_threshold(d0, s0, MANIFEST_N)
        cohorts[c] = {"n": int(len(s)), "median_scatter_ppm": float(
            np.median(ok.loc[ok["cohort"] == c, "scatter_ppm"])),
            "delta0": d0, "sigma0": s0, "lambda": lam, "threshold_sde": thr}
        print(f"  cohort {c}: n={len(s)}  scatter~{cohorts[c]['median_scatter_ppm']:.0f}ppm  "
              f"lambda={lam:.2f}  bar={thr:.1f} SDE", flush=True)

    # ---- per-family completeness C_i (injection-recovery into real LCs) ----------------
    # precompute one forward-model template per (family, depth) -- it does not depend on the
    # star; inject by remapping it onto each star's phase (the inject_periodic transform).
    print(f"injection-recovery ({len(FAMILIES)} families x {len(DEPTHS)} depths x "
          f"{len(INJ_PERIODS)} periods)...", flush=True)
    templ = {(fam, dep): make_transit(fam, depth=dep, npix=150)
             for fam in FAMILIES for dep in DEPTHS}

    def inject(t, fam, dep, period, t0, dur, ed):
        tph, tfl = templ[(fam, dep)]
        frac = ((t - t0) / period + 0.5) % 1.0 - 0.5
        inj = np.interp(frac * period / (2.0 * dur), tph, tfl, left=1.0, right=1.0)
        if ed is not None:
            ep = np.clip(np.floor((t - t0) / period + 0.5).astype(int) - 0, 0, None)
            ep = np.minimum(ep - ep.min(), len(ed) - 1)
            inj = 1.0 - (1.0 - inj) * (ed[ep] / dep)
        return inj

    rng = np.random.default_rng(0)
    Cgrid = {}
    for fam in FAMILIES:
        Cgrid[fam] = {}
        for dep in DEPTHS:
            rec_by_cohort = {c: [] for c in range(N_COHORTS)}
            for _, r in ok.iterrows():
                try:
                    t, f = load_lc(r["source_id"])
                except Exception:
                    continue
                p = INJ_PERIODS[int(r["source_id"]) % len(INJ_PERIODS)]   # deterministic
                ed = multi_epoch_depths(60, dep, rng=rng) if fam == "tail" else None
                fi = f * inject(t, fam, dep, p, t[0] + 0.3 * p, 0.12, ed)
                det = bls_detect(t, fi, PERIODS, DURS)["sde"] > cohorts[r["cohort"]]["threshold_sde"]
                if fam == "tail":          # tail also gets the parallel variable-depth net
                    det = det or single_event_detect(t, fi, r["scatter_ppm"] / 1e6)["best_snr"] > z
                rec_by_cohort[int(r["cohort"])].append(bool(det))
            Cgrid[fam][f"{dep:.3f}"] = {c: float(np.mean(v)) if v else np.nan
                                        for c, v in rec_by_cohort.items()}
            cstr = "  ".join(f"c{c}={Cgrid[fam][f'{dep:.3f}'][c]:.2f}" for c in range(N_COHORTS))
            print(f"  {fam:7s} depth {dep*100:.1f}%:  {cstr}", flush=True)

    # ---- illustrative per-family f_max (sum C_i over the analysed stars) ----------------
    fmax = {}
    for fam in FAMILIES:
        d = "0.010" if "0.010" in Cgrid[fam] else list(Cgrid[fam])[0]
        sumCi = sum((Cgrid[fam][d][c] or 0) * (ok["cohort"] == c).sum() for c in range(N_COHORTS))
        fmax[fam] = poisson_fmax(sumCi) if sumCi > 0 else None

    cal = {"n_ok": int(len(ok)), "n_total_manifest": MANIFEST_N, "n_cohorts": N_COHORTS,
           "fwer_sigma": float(z), "cohort_edges_scatter": [float(e) for e in edges],
           "cohorts": cohorts, "completeness": Cgrid,
           "illustrative_fmax_at_1pct": fmax,
           "note": ("Frozen Phase-2 detection calibration. Computed on the noise floor + "
                    "synthetic injections only; no real candidate revealed. Step 4 applies "
                    "the per-cohort threshold_sde to unblind."),
           "grids": {"periods": [float(PERIODS[0]), float(PERIODS[-1]), float(PERIODS[1]-PERIODS[0])],
                     "durations": [float(x) for x in DURS], "inj_depths": DEPTHS,
                     "inj_periods": INJ_PERIODS}}
    with open(OUT, "w") as fp:
        json.dump(cal, fp, indent=2)
    print(f"\nwrote {OUT}")
    print("illustrative per-family f_max (1% depth, this calibration sample):",
          {k: (round(v, 3) if v else None) for k, v in fmax.items()})


if __name__ == "__main__":
    main()
