#!/usr/bin/env python3
"""Pilot: validate that Channel B's morphology metrics actually fire on the injected
anomaly library, and quantify the noise level at which the separation fails.

This is methods-development, fully synthetic -- it touches no target light curves and so
runs freely before the OSF freeze. It answers the pre-registration's open question: do the
morphology discriminants (flat_bottom, asymmetry, depth-CV) separate the anomaly families
from the natural-planet locus, and down to what per-point SNR?

Outputs:
  figures/kdwarf_injection_pilot.png  -- folded families + metric-space separation
  console summary                     -- metric means per family and the SNR at which
                                         each anomaly axis stops separating from 'planet'
"""
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPE)
from core.transit import make_transit, multi_epoch_depths, metrics   # noqa: E402

ROOT = os.path.dirname(PIPE)
FIG = os.path.join(ROOT, "figures", "kdwarf_injection_pilot.png")
DEPTH = 0.01                       # 1% -- a plausible K-dwarf occulter transit
FAMILIES = ["planet", "box", "louver", "triangle", "tail"]
COLOR = {"planet": "#888888", "box": "#1f77b4", "louver": "#d62728",
         "triangle": "#2ca02c", "tail": "#9467bd"}


def noisy_metrics(kind, sigma, nreal, rng):
    """Inject `kind` at fiducial depth into a folded profile whose per-bin scatter is
    sigma, nreal times; return arrays of the anomaly metrics. The noise is per *phase
    bin* of the stacked/folded transit -- the regime morphology actually operates in,
    reachable by folding enough epochs -- not per raw cadence point."""
    ph, f0 = make_transit(kind, depth=DEPTH)
    out = {"flat_bottom": [], "asymmetry": []}
    for _ in range(nreal):
        m = metrics(ph, f0 + rng.normal(0, sigma, f0.size))
        out["flat_bottom"].append(m["flat_bottom"])
        out["asymmetry"].append(m["asymmetry"])
    return {k: np.array(v) for k, v in out.items()}


def main():
    rng = np.random.default_rng(42)

    # ---- (1) noise-free metric separation -------------------------------------------
    print("Noise-free morphology metrics (depth = %.0f%%):" % (DEPTH * 100))
    print(f"  {'family':>9} {'flat_bottom':>12} {'asymmetry':>10} {'dur_frac':>9}")
    base = {}
    for k in FAMILIES:
        ph, f = make_transit(k, depth=DEPTH)
        m = metrics(ph, f)
        base[k] = m
        print(f"  {k:>9} {m['flat_bottom']:>12.3f} {m['asymmetry']:>10.3f} "
              f"{m['duration_frac']:>9.3f}")

    # ---- (2) depth-CV for the disintegrating family ---------------------------------
    d = multi_epoch_depths(40, DEPTH, cv=0.6, dropout=0.15, rng=rng)
    print(f"\nDisintegrating 'tail' per-epoch depth: mean={d.mean():.4f} "
          f"CV={d.std()/d.mean():.2f} (vs ~0 for a stable planet) -- the depth-CV axis.")

    # ---- (3) at what folded-profile SNR does each anomaly axis stop separating? ------
    # folded per-bin SNR = depth / sigma_bin. Separation = anomaly mean is >2 sigma off
    # the planet distribution on that axis. (A folded profile reaches high per-bin SNR by
    # stacking many epochs, so these floors are achievable, not the single-cadence SNR.)
    print("\nFolded-profile per-bin SNR at which each anomaly separates from 'planet':")
    snr_grid = np.array([60, 40, 30, 20, 12, 8, 5])
    pp = {}
    for snr in snr_grid:
        sigma = DEPTH / snr
        pp[snr] = {k: noisy_metrics(k, sigma, 120, rng) for k in FAMILIES}
    # report each anomaly on whichever axis separates it most easily (lowest SNR floor)
    for fam in ["box", "louver", "triangle", "tail"]:
        best = None
        for axis in ["flat_bottom", "asymmetry"]:
            thr = None
            for snr in snr_grid:
                pl = pp[snr]["planet"][axis]
                an = pp[snr][fam][axis]
                if abs(np.nanmean(an) - np.nanmean(pl)) > 2 * np.nanstd(pl):
                    thr = snr
            if thr and (best is None or thr < best[1]):
                best = (axis, thr)
        msg = (f"folded SNR >= {best[1]:>2} on {best[0]}" if best
               else "not separated in tested range (needs depth-CV / deeper transit)")
        print(f"  {fam:>9}: {msg}")

    # ---- (4) figure: folded families + metric space ---------------------------------
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for k in FAMILIES:
        ph, f = make_transit(k, depth=DEPTH)
        ax[0].plot(ph, f, label=k, color=COLOR[k], lw=1.6)
    ax[0].set(xlabel="phase", ylabel="normalised flux",
              title=f"Forward-modelled families (depth {DEPTH*100:.0f}%)", xlim=(-0.25, 0.25))
    ax[0].legend(fontsize=9)
    snr = 50
    sigma = DEPTH / snr
    for k in FAMILIES:
        m = noisy_metrics(k, sigma, 120, rng)
        ax[1].scatter(m["flat_bottom"], m["asymmetry"], s=10, alpha=0.5,
                      color=COLOR[k], label=k)
    ax[1].set(xlabel="flat_bottom  (box-vs-U)", ylabel="asymmetry  (centroid offset)",
              title=f"Metric space at folded-profile per-bin SNR={snr}")
    ax[1].legend(fontsize=9)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=120)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()
