#!/usr/bin/env python
"""Clean phase-fold figure for the research note on residual Gaia DR3 1397924585409290240.
Reads the committed cached light curve, folds at the true BLS period (the detector's own recovered
period; the triage period was a 4x harmonic alias). Production only — no thresholds."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect  # noqa: E402

PERIODS = np.arange(0.5, 13.0, 0.02); DURS = np.array([0.05, 0.1, 0.2])
SID = "1397924585409290240"

d = np.load(os.path.join(ROOT, "data/lightcurves", f"{SID}.npz"), allow_pickle=True)
t, f = np.asarray(d["time"], float), np.asarray(d["flux"], float)
g = np.isfinite(t) & np.isfinite(f); t, f = t[g], f[g]
bls = bls_detect(t, f, PERIODS, DURS)
P, t0 = bls["period"], bls["t0"]
ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
o = np.argsort(ph); ph, ff = ph[o], f[o]


def binned(x, y, lo, hi, nbin):
    e = np.linspace(lo, hi, nbin + 1); idx = np.clip(np.digitize(x, e) - 1, 0, nbin - 1)
    xb, yb = [], []
    for b in range(nbin):
        m = idx == b
        if m.sum() >= 3:
            xb.append(0.5 * (e[b] + e[b + 1])); yb.append(np.median(y[m]))
    return np.array(xb), np.array(yb)


fig, (axf, axz) = plt.subplots(1, 2, figsize=(12, 4.4))
# full fold
axf.plot(ph, ff, ".", ms=1.0, alpha=0.15, color="0.55", rasterized=True)
xb, yb = binned(ph, ff, -0.5, 0.5, 100); axf.plot(xb, yb, "-", color="C3", lw=1.4)
axf.axhline(1.0, color="C0", lw=0.6, ls=":")
axf.axvspan(0.5 - 0.05, 0.5, color="C1", alpha=0.12)
axf.axvspan(-0.5, -0.5 + 0.05, color="C1", alpha=0.12)
axf.text(0.42, 0.945, "secondary\nphase (none)", fontsize=7, color="C1", ha="center")
axf.set_xlim(-0.5, 0.5); axf.set_xlabel("orbital phase"); axf.set_ylabel("relative flux")
axf.set_title(f"Gaia DR3 {SID} — full fold at P={P:.3f} d")
# zoom on transit
mz = np.abs(ph) < 0.06
axz.plot(ph[mz], ff[mz], ".", ms=2.0, alpha=0.30, color="0.45", rasterized=True)
xb, yb = binned(ph[mz], ff[mz], -0.06, 0.06, 40); axz.plot(xb, yb, "-", color="C3", lw=1.8)
axz.axhline(1.0, color="C0", lw=0.6, ls=":")
axz.set_xlim(-0.06, 0.06); axz.set_xlabel("orbital phase"); axz.set_ylabel("relative flux")
axz.set_title("transit zoom — symmetric, flat-ish bottom, ~6–7% deep")
fig.tight_layout()
out = os.path.join(ROOT, "figures", "note_1397924585409290240_fold.png")
fig.savefig(out, dpi=140)
print("wrote", out, "| P=%.4f t0=%.3f depth=%.3f%% SDE=%.2f" % (P, t0, bls["depth"] * 100, bls["sde"]))
