#!/usr/bin/env python3
"""Step 3b (DIAGNOSTIC): empirical-null behaviour of the RAW IR-excess significance.

Ordering note (important): the registered anomaly flagging (§5.3) applies the
empirical null to the *post-battery* natural-model residual A, NOT to the raw excess.
This script is therefore a **diagnostic**, valuable for two things it reveals:
  (a) the photosphere-prediction scatter, via the genomic-control inflation lambda —
      the key W1/W2 finding (lambda ~ 10: the textbook errors are ~10x too small, so
      naive thresholds would massively over-flag);
  (b) confirmation that for W3/W4 the *detected* population is excess-dominated (no
      bare WD is detectable there), so its "bulk" is debris disks, not the photospheric
      null (sigma0 collapses to ~0.3). This is precisely why the empirical null must be
      applied AFTER the natural-explanation battery, on A.
The flagged counts below are NOT anomaly detections.

Per band we estimate the empirical null (Efron 2004):
  - centre  delta0 = median(chi)
  - width   sigma0 estimated from the LEFT side only (chi <= median), which is
            uncontaminated by astrophysical excess (excess only adds positive chi):
            sigma0 = delta0 - percentile(chi, 15.865)
and report the genomic-control-style inflation lambda = sigma0**2 (vs the textbook
N(0,1) null). The calibrated statistic is z = (chi - delta0)/sigma0.

Flagging uses the registered Stage-1 *conservative* trial factor (§5.3): Bonferroni
over the number of tests in the band, one-sided, alpha=0.05. This is deliberately
the strictest bar; the survivors are Channel-A candidates for the natural-explanation
battery.

Outputs:
  data/derived/ir_excess_calibrated.parquet   (gitignored) z per band
  data/manifests/empirical_null.summary.json  (committed)  per-band calibration
  figures/qq_excess.png                        (committed)  QQ diagnostic
"""
import json, os
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN = os.path.join(ROOT, "data", "derived", "ir_excess.parquet")
OUT = os.path.join(ROOT, "data", "derived", "ir_excess_calibrated.parquet")
MAN = os.path.join(ROOT, "data", "manifests")
FIG = os.path.join(ROOT, "figures", "qq_excess.png")
BANDS = ["w1", "w2", "w3", "w4"]


def empirical_null(chi):
    chi = chi[np.isfinite(chi)]
    delta0 = float(np.median(chi))
    q = float(np.percentile(chi, 15.865))     # ~ -1 sigma point of the null
    sigma0 = max(delta0 - q, 1e-6)
    return delta0, sigma0, len(chi)


def main():
    df = pd.read_parquet(IN)
    summary = {}
    fig, axes = plt.subplots(2, 2, figsize=(10, 9))
    for ax, b in zip(axes.ravel(), BANDS):
        chi = df[f"{b}_chi"].to_numpy(float)
        delta0, sigma0, n = empirical_null(chi)
        lam = sigma0 ** 2
        z = (chi - delta0) / sigma0
        df[f"{b}_z"] = z
        # registered Stage-1 conservative Bonferroni threshold (one-sided)
        zthr = float(norm.ppf(1 - 0.05 / max(n, 1)))
        nflag = int(np.nansum(z > zthr))
        summary[b.upper()] = {"n": n, "delta0": round(delta0, 3),
                              "sigma0": round(sigma0, 3), "lambda": round(lam, 3),
                              "z_threshold_bonferroni": round(zthr, 3),
                              "n_flagged": nflag}
        # QQ plot of calibrated z vs theoretical normal
        zf = np.sort(z[np.isfinite(z)])
        if len(zf):
            theo = norm.ppf((np.arange(len(zf)) + 0.5) / len(zf))
            ax.plot(theo, zf, ".", ms=2, alpha=0.5)
            lim = [min(theo.min(), -4), max(zf.max(), 4)]
            ax.plot([-4, 4], [-4, 4], "k--", lw=0.8)
            ax.axhline(zthr, color="crimson", lw=0.8, ls=":")
            ax.set_xlim(-4, 4); ax.set_ylim(lim)
        ax.set_title(f"{b.upper()}: n={n}, "
                     r"$\delta_0$=%.2f, $\sigma_0$=%.2f, $\lambda$=%.2f, flagged=%d"
                     % (delta0, sigma0, lam, nflag), fontsize=9)
        ax.set_xlabel("theoretical N(0,1) quantile"); ax.set_ylabel("calibrated z")
    fig.suptitle("Empirical-null QQ diagnostic — IR-excess (Channel A)", fontsize=11)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=120)

    df.to_parquet(OUT, index=False)
    json.dump(summary, open(os.path.join(MAN, "empirical_null.summary.json"), "w"), indent=2)

    print("per-band empirical null + conservative (Bonferroni) flagging:")
    for b in BANDS:
        s = summary[b.upper()]
        print(f"  {b.upper()}: n={s['n']:>6,}  delta0={s['delta0']:+.2f}  "
              f"sigma0={s['sigma0']:.2f}  lambda={s['lambda']:.2f}  "
              f"z*={s['z_threshold_bonferroni']:.2f}  -> flagged={s['n_flagged']}")
    print(f"wrote {OUT}, summary json, and {FIG}")


if __name__ == "__main__":
    main()
