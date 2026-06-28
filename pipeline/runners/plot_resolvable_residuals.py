#!/usr/bin/env python
"""Phase-fold the T0T1T2 resolvable-regime residuals (depth>0.3%) for visual adjudication.

Production/diagnostic only: reads the committed triage CSV + cached light curves, re-derives
(period, t0, duration) with the pipeline's own BLS (core.detect.bls_detect on the same PERIODS/DURS
grid as k04), folds, and plots. Computes no thresholds and changes no analysis. Output: figures/.
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect  # noqa: E402

PERIODS = np.arange(0.5, 13.0, 0.02)   # identical to k04_search.PERIODS
DURS = np.array([0.05, 0.1, 0.2])      # identical to k04_search.DURS
LCDIR = os.path.join(ROOT, "data", "lightcurves")
FIGDIR = os.path.join(ROOT, "figures")
os.makedirs(FIGDIR, exist_ok=True)

TRIAGE = os.path.join(ROOT, "data", "manifests", "kdwarf_T0T1T2_recurring_triage.csv")


def load_lc(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"), allow_pickle=True)
    t, f = np.asarray(d["time"], float), np.asarray(d["flux"], float)
    g = np.isfinite(t) & np.isfinite(f)
    return t[g], f[g]


def fold(t, f, period, t0):
    ph = ((t - t0) / period + 0.5) % 1.0 - 0.5
    o = np.argsort(ph)
    return ph[o], f[o]


def binned(ph, f, nbin=80):
    edges = np.linspace(-0.5, 0.5, nbin + 1)
    idx = np.clip(np.digitize(ph, edges) - 1, 0, nbin - 1)
    xb, yb = [], []
    for b in range(nbin):
        m = idx == b
        if m.sum() >= 3:
            xb.append(0.5 * (edges[b] + edges[b + 1]))
            yb.append(np.median(f[m]))
    return np.array(xb), np.array(yb)


def panel(ax, sid, period, t0, title):
    t, f = load_lc(sid)
    ph, ff = fold(t, f, period, t0)
    ax.plot(ph, ff, ".", ms=1.2, alpha=0.18, color="0.5", rasterized=True)
    xb, yb = binned(ph, ff)
    ax.plot(xb, yb, "-", color="C3", lw=1.6)
    ax.axhline(1.0, color="C0", lw=0.6, ls=":")
    ax.set_title(title, fontsize=9)
    ax.set_xlim(-0.5, 0.5)
    ax.set_xlabel("phase")
    ax.set_ylabel("rel. flux")


def main():
    tri = pd.read_csv(TRIAGE, dtype={"source_id": str})
    res = tri[tri["verdict"] == "RESIDUAL"]
    resolv = res[res["depth"] > 0.003].sort_values("depth", ascending=False)
    print(f"resolvable residuals to fold: {len(resolv)}")

    rows = []
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, (_, r) in zip(axes.ravel(), resolv.iterrows()):
        sid = r["source_id"]
        t, f = load_lc(sid)
        bls = bls_detect(t, f, PERIODS, DURS)
        rows.append({"source_id": sid, "triage_P": r["period"], "triage_depth": r["depth"],
                     "bls_P": bls["period"], "bls_depth": bls["depth"], "bls_t0": bls["t0"],
                     "bls_dur": bls["duration"], "bls_sde": bls["sde"],
                     "flat_bottom": r["flat_bottom"], "asymmetry": r["asymmetry"]})
        title = (f"{sid}\ntriage P={r['period']:.2f}d d={r['depth']*100:.2f}% "
                 f"flat={r['flat_bottom']:.2f} asym={r['asymmetry']:.2f}\n"
                 f"BLS P={bls['period']:.2f}d d={bls['depth']*100:.2f}% SDE={bls['sde']:.1f}")
        panel(ax, sid, bls["period"], bls["t0"], title)
    fig.suptitle("T0T1T2 resolvable-regime residuals (depth>0.3%) — folded at BLS period", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = os.path.join(FIGDIR, "kdwarf_T0T1T2_resolvable_residuals.png")
    fig.savefig(out, dpi=130)
    print("wrote", out)

    # Standout detail: 1397924585409290240 folded at BLS, triage P, and k04 search P (harmonics)
    sid = "1397924585409290240"
    t, f = load_lc(sid)
    bls = bls_detect(t, f, PERIODS, DURS)
    fig2, ax2 = plt.subplots(1, 3, figsize=(15, 4.3))
    for ax, (P, t0, lab) in zip(ax2, [
            (bls["period"], bls["t0"], f"BLS P={bls['period']:.2f}d"),
            (11.74, bls["t0"], "triage P=11.74d"),
            (2.94, bls["t0"], "k04-search P=2.94d")]):
        panel(ax, sid, P, t0, f"{sid}\n{lab}")
    fig2.suptitle("Standout 1397924585409290240 — harmonic check (same t0)", fontsize=11)
    fig2.tight_layout(rect=[0, 0, 1, 0.94])
    out2 = os.path.join(FIGDIR, "kdwarf_T0T1T2_standout_1397924585409290240.png")
    fig2.savefig(out2, dpi=130)
    print("wrote", out2)

    summ = pd.DataFrame(rows)
    print("\n=== BLS re-derivation vs triage ===")
    print(summ.to_string(index=False))


if __name__ == "__main__":
    main()
