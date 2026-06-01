#!/usr/bin/env python3
"""Step 3: IR-excess significance for the WISE-detected sample (Channel A, Stage 1).

Predicts the photospheric W1-W4 flux from a DA atmosphere grid (Bergeron/Bedard
2020; §5.3 H0) at each WD's catalogue (Teff_H, logg_H), anchored on the observed
Gaia G via the distance-independent model colour (Wn - G3). The per-band excess
significance is then

    chi_n = (f_obs - f_pred) / sigma_f_obs       (positive = excess)

computed only where AllWISE reports a real detection (ph_qual in A/B/C).

DISCIPLINE: this computes and *reports* the excess distribution. It does NOT set a
detection threshold here — the registered threshold comes from the empirical null
+ injection-recovery (preregistration.md §5.3), not from eyeballing this output.

Output (gitignored, derived): data/derived/ir_excess.parquet
"""
import os
import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = os.path.join(ROOT, "data", "models", "bergeron", "Table_DA")
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
OUT = os.path.join(ROOT, "data", "derived", "ir_excess.parquet")
BANDS = ["w1", "w2", "w3", "w4"]
LN10_04 = 0.4 * np.log(10.0)


def load_grid():
    """Parse Table_DA -> interpolators over (Teff, logg) for G3 and W1-W4 (abs mag).

    The header writes "log g" as two tokens, so column positions are taken from the
    fixed data layout (Teff=0, logg=1, W1..W4=17..20, G3=38) rather than the header.
    """
    IDX = {"G3": 38, "W1": 17, "W2": 18, "W3": 19, "W4": 20}
    teff, logg, mags = [], [], {b: [] for b in IDX}
    for line in open(GRID):
        f = line.split()
        if len(f) < 41:                         # data rows have 44 cols; metadata is short
            continue
        try:
            t, g = float(f[0]), float(f[1])
            vals = {b: float(f[i]) for b, i in IDX.items()}
        except (ValueError, IndexError):
            continue
        if not (1000.0 <= t <= 200000.0 and 6.5 <= g <= 9.5):
            continue
        teff.append(t); logg.append(g)
        for b in IDX:
            mags[b].append(vals[b])
    pts = np.column_stack([teff, logg])
    interp = {b: LinearNDInterpolator(pts, np.array(mags[b])) for b in IDX}
    print(f"  grid: {len(teff)} nodes, logg {sorted(set(logg))}, "
          f"Teff [{min(teff):.0f},{max(teff):.0f}]")
    return interp


def main():
    interp = load_grid()
    ob = pd.read_parquet(OB)
    aw = pd.read_parquet(AW)
    df = aw.merge(ob[["source_id", "g_mag", "teff_h", "logg_h"]], on="source_id", how="left")

    teff = df["teff_h"].to_numpy(float)
    logg = np.clip(df["logg_h"].to_numpy(float), 7.0, 9.0)   # grid range
    g_obs = df["g_mag"].to_numpy(float)
    g_model = interp["G3"](teff, logg)
    ph = df["ph_qual"].astype(str).to_numpy()

    out = {"source_id": df["source_id"].to_numpy(), "teff_h": teff, "g_mag": g_obs}
    n_det = {}
    for i, b in enumerate(BANDS):
        B = b.upper()
        wobs = df[f"{b}mpro"].to_numpy(float)
        werr = df[f"{b}mpro_error"].to_numpy(float)
        wmodel = interp[B](teff, logg)
        # predicted photospheric apparent mag = G_obs + (Wn - G3) model colour
        wpred = g_obs + (wmodel - g_model)
        # excess significance = (f_obs - f_pred) / sigma(f_obs), bounded by the
        # detection S/N when the photosphere is negligible (cold bands):
        #   = (1 - f_pred/f_obs) / (ln10*0.4*werr),  f_pred/f_obs = 10^(-0.4(wpred-wobs))
        dm = wpred - wobs                                  # >0 => observed brighter (excess)
        chi = (1.0 - np.power(10.0, -0.4 * dm)) / (LN10_04 * werr)
        detected = np.array([len(s) == 4 and s[i] in "ABC" for s in ph])
        chi = np.where(detected & np.isfinite(chi) & np.isfinite(wmodel), chi, np.nan)
        out[f"{b}_pred_mag"] = wpred
        out[f"{b}_chi"] = chi
        n_det[B] = int(np.isfinite(chi).sum())

    res = pd.DataFrame(out)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    res.to_parquet(OUT, index=False)
    print(f"  wrote {OUT} ({len(res):,} rows)")
    print("  excess significance computed where detected & model-covered:")
    for b in BANDS:
        c = res[f"{b}_chi"].dropna()
        if len(c):
            print(f"    {b.upper()}: n={len(c):>6,}  median chi={c.median():+.2f}  "
                  f"95th={c.quantile(0.95):+.2f}  max={c.max():+.1f}")
    # descriptive only (NOT a registered threshold):
    for b in ["w3", "w4"]:
        c = res[f"{b}_chi"]
        print(f"  [descriptive] {b.upper()} with chi>5: {int((c > 5).sum())}  "
              f"chi>10: {int((c > 10).sum())}")


if __name__ == "__main__":
    main()
