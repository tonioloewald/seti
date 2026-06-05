#!/usr/bin/env python3
"""Synthetic end-to-end calibration pilot (pre-registration steps 3a -> 3b -> 3c).

Runs the registered procedure on a *synthetic* K-dwarf population -- no target data -- to show
it produces sane numbers before it is ever pointed at the real manifest: outlier-blind cohorts
form, the per-cohort empirical null + genomic-control lambda + FWER bar come out in the expected
regime and control false alarms, U-transit completeness C_i behaves (quiet cohorts deeper than
active), and the anomaly families are recovered by the detectors and flagged by morphology.

This is the dress rehearsal: at the real run we execute the identical core functions on real
light curves. Numbers here are illustrative of the *method*, not the survey result.

Output: figures/pilot_calibration.png + console report.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPE)
from core.noise import robust_scatter, cohort_edges, assign_cohorts          # noqa: E402
from core.detect import bls_detect, single_event_detect                      # noqa: E402
from core.stats import empirical_null, cohort_threshold, fwer_sigma, poisson_fmax  # noqa: E402
from core.transit import inject_periodic, multi_epoch_depths, make_transit, metrics  # noqa: E402

N_LC = 150
CAD = 30.0 / 1440.0                 # 30-min cadence (days)
SPAN = 27.0                         # one TESS sector
N_TOTAL = 100_000                   # representative real K-dwarf manifest size (for the bar)
PERIODS = np.arange(0.5, 8.0, 0.01)
DURS = np.array([0.04, 0.08, 0.16])
DEPTHS = [0.003, 0.005, 0.01, 0.02]
INJ_PERIODS = [2.3, 5.1]


def synth_lc(sigma, rng, var_amp=0.0, var_period=5.0):
    """A bare synthetic light curve: white noise sigma + optional slow stellar variability."""
    t = np.arange(0, SPAN, CAD)
    f = 1.0 + rng.normal(0, sigma, t.size)
    if var_amp:
        f += var_amp * np.sin(2 * np.pi * t / var_period + rng.uniform(0, 6.28))
    return t, f


def main():
    rng = np.random.default_rng(7)

    # ---- build a synthetic population spanning quiet -> active --------------------------
    sigmas = 10 ** rng.uniform(np.log10(3e-4), np.log10(3e-3), N_LC)       # 300-3000 ppm
    var = np.where(sigmas > 1.2e-3, rng.uniform(0, 2e-3, N_LC), 0.0)        # active stars vary
    lcs = [synth_lc(s, rng, v) for s, v in zip(sigmas, var)]

    # ---- 3a: outlier-blind scatter -> cohorts -----------------------------------------
    scat = np.array([robust_scatter(f) for _, f in lcs])
    edges = cohort_edges(scat, n_cohorts=3)
    coh = assign_cohorts(scat, edges)
    print("3a  COHORTS (outlier-blind MAD):")
    for c in range(3):
        m = coh == c
        print(f"    cohort {c}: n={m.sum():3d}  median scatter={np.median(scat[m])*1e6:5.0f} ppm")

    # ---- 3b: per-cohort null, lambda, FWER bar; then U-transit completeness ------------
    sde0 = np.array([bls_detect(t, f, PERIODS, DURS)["sde"] for t, f in lcs])   # noise-only
    print("\n3b  PER-COHORT NULL + FWER BAR (N_total = %d):" % N_TOTAL)
    thr = {}
    for c in range(3):
        d0, s0, lam = empirical_null(sde0[coh == c])
        thr[c] = cohort_threshold(d0, s0, N_TOTAL)
        print(f"    cohort {c}: lambda={lam:5.2f}  null(d0={d0:.1f},s0={s0:.2f})  "
              f"bar={thr[c]:.1f} SDE  (= {fwer_sigma(N_TOTAL):.1f} sigma-equiv)")
    fa = sum((sde0[coh == c] > thr[c]).sum() for c in range(3))
    print(f"    false alarms among {N_LC} noise LCs at the bar: {fa}  "
          f"(~FWER controlled; null fit on {N_LC//3}/cohort -- the real survey fits on thousands)")

    print("\n3b  U-TRANSIT COMPLETENESS C_i(depth) by cohort (recovered = SDE>bar & P matched):")
    Cgrid = np.zeros((3, len(DEPTHS)))
    for di, dep in enumerate(DEPTHS):
        rec = np.zeros(N_LC, bool)
        for i, (t, f) in enumerate(lcs):
            p = INJ_PERIODS[i % 2]
            fi = f * inject_periodic(t, "planet", dep, p, 1.0, 0.12)
            r = bls_detect(t, fi, PERIODS, DURS)
            rec[i] = (r["sde"] > thr[coh[i]]) and abs(r["period"] - p) < 0.05
        for c in range(3):
            Cgrid[c, di] = rec[coh == c].mean()
        print(f"    depth {dep*100:4.1f}%:  " +
              "  ".join(f"coh{c}={Cgrid[c,di]:.2f}" for c in range(3)))

    # ---- 3c: anomaly families recovered by detectors + flagged by morphology -----------
    print("\n3c  ANOMALY FAMILIES (depth 1%, P=2.3 d): detection GATE + morphology NET")
    print("    (detection must catch all; morphology only needs to flag the clear non-planets)")
    for fam in ["planet", "box", "triangle", "tail"]:
        det_bls = det_se = 0
        for i, (t, f) in enumerate(lcs):
            ed = multi_epoch_depths(40, 0.01, rng=rng) if fam == "tail" else None
            fi = f * inject_periodic(t, fam, 0.01, 2.3, 1.0, 0.12, epoch_depths=ed)
            det_bls += (bls_detect(t, fi, PERIODS, DURS)["sde"] > thr[coh[i]])
            det_se += (single_event_detect(t, fi, scat[i])["best_snr"] > 7)
        m = metrics(*make_transit(fam, depth=0.01))                # template morphology
        flag = "FLAG non-planet" if (m["flat_bottom"] > 0.85 or m["asymmetry"] > 0.03) else "planet-like"
        print(f"    {fam:9s}: detect[BLS={det_bls/N_LC:.2f} single-event={det_se/N_LC:.2f}]  "
              f"morph[flat={m['flat_bottom']:.2f} asym={m['asymmetry']:.3f} -> {flag}]")

    # illustrative f_max from the U-transit completeness (sum C_i over the synthetic sample)
    sumCi = sum(Cgrid[c, 2] * (coh == c).sum() for c in range(3))   # at 1% depth
    print(f"\n    illustrative f_max (1% U-transit, this synthetic sample): "
          f"3/sum(C_i)={poisson_fmax(sumCi):.3f}  (sum C_i={sumCi:.0f})")

    # ---- figure ------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for c in range(3):
        ax[0].hist(sde0[coh == c], bins=15, alpha=0.5, label=f"cohort {c}")
        ax[0].axvline(thr[c], ls="--", color=f"C{c}")
    ax[0].set(xlabel="BLS SDE (noise-only)", ylabel="N light curves",
              title="3b: per-cohort null + FWER bar (dashed)")
    ax[0].legend(fontsize=9)
    for c in range(3):
        ax[1].plot([d*100 for d in DEPTHS], Cgrid[c], "o-", label=f"cohort {c}")
    ax[1].set(xlabel="injected depth (%)", ylabel="completeness C_i",
              title="3b: U-transit completeness (quiet cohorts deeper)")
    ax[1].legend(fontsize=9)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(PIPE), "figures", "pilot_calibration.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=120)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
