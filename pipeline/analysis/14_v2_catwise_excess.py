#!/usr/bin/env python3
"""Step 14 (v2): deeper W1/W2 excess search on CatWISE2020.

Executes the frozen v2 plan (`preregistration_v2_unwise.md`): apply the pre-specified
cross-match cuts to the CatWISE2020 matches, compute the *identical* calibrated excess
statistic as v1 (§5.3 / `01_ir_excess.py`), and re-derive the empirical-null genomic-control
inflation λ on the deeper W1/W2 distribution. Anything flagged proceeds to the unchanged
natural-explanation battery (separate step). source_id is a string throughout.

Pre-specified cuts (frozen, not tuned to data): nearest CatWISE source within 2.0"; reject if
a second source lies within 3.0" (blend guard); per-band detection = SNR>=5 with clean cc_flags.
Output: data/derived/v2_catwise_excess.parquet
"""
import os
import numpy as np, pandas as pd
from scipy.interpolate import LinearNDInterpolator

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = os.path.join(ROOT, "data", "models", "bergeron", "Table_DA")
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
CW = os.path.join(ROOT, "data", "raw", "catwise", "catwise_xmatch.parquet")
OUT = os.path.join(ROOT, "data", "derived", "v2_catwise_excess.parquet")
IDX = {"G3": 38, "W1": 17, "W2": 18}
LN10_04 = 0.4 * np.log(10.0)


def load_grid():
    teff, logg, mags = [], [], {b: [] for b in IDX}
    for line in open(GRID):
        f = line.split()
        if len(f) < 41:
            continue
        try:
            t, g = float(f[0]), float(f[1]); v = {b: float(f[i]) for b, i in IDX.items()}
        except (ValueError, IndexError):
            continue
        if not (1000 <= t <= 200000 and 6.5 <= g <= 9.5):
            continue
        teff.append(t); logg.append(g)
        for b in IDX:
            mags[b].append(v[b])
    pts = np.column_stack([teff, logg])
    return {b: LinearNDInterpolator(pts, np.array(mags[b])) for b in IDX}


def emp_null(x):
    """Empirical null: location delta0 (median) and inflated scale sigma0; lambda = sigma0^2."""
    x = x[np.isfinite(x)]
    d0 = np.median(x)
    s0 = max(d0 - np.percentile(x, 15.865), 1e-6)   # robust lower-half sigma
    return d0, s0, s0 * s0


def clean(cc):
    cc = str(cc).strip()
    return cc in ("", "0", "00", "000", "0000") or set(cc) <= {"0"}


def main():
    interp = load_grid()
    cw = pd.read_parquet(CW); cw["source_id"] = cw["source_id"].astype(str)
    for c in ["w1mpro", "w1sigmpro", "w2mpro", "w2sigmpro", "w1snr", "w2snr", "sep_arcsec"]:
        cw[c] = pd.to_numeric(cw[c], errors="coerce")

    # --- pre-specified cross-match cuts ---
    nsrc = cw.groupby("source_id").size()
    blended = set(nsrc[nsrc > 1].index)                       # 2nd source within 3"
    cw = cw[~cw["source_id"].isin(blended)].copy()            # blend guard
    cw = cw[cw["sep_arcsec"] <= 2.0]                          # nearest within 2"
    print(f"CatWISE matches after blend guard + 2\" cut: {len(cw):,} WDs "
          f"({len(blended):,} blended dropped)")

    ob = pd.read_parquet(OB); ob["source_id"] = ob["source_id"].astype(str)
    df = cw.merge(ob[["source_id", "g_mag", "teff_h", "logg_h"]], on="source_id", how="inner")
    df = df.dropna(subset=["g_mag", "teff_h", "logg_h"])
    teff = df["teff_h"].to_numpy(float)
    logg = np.clip(df["logg_h"].to_numpy(float), 7.0, 9.0)
    g_obs = df["g_mag"].to_numpy(float)
    g_model = interp["G3"](teff, logg)

    rows = {"source_id": df["source_id"].to_numpy(), "teff_h": teff}
    for b, col in [(1, "w1"), (2, "w2")]:
        B = f"W{b}"
        wpred = g_obs + (interp[B](teff, logg) - g_model)       # photosphere anchored on G
        wobs = df[f"{col}mpro"].to_numpy(float)
        werr = df[f"{col}sigmpro"].to_numpy(float)
        snr = df[f"{col}snr"].to_numpy(float)
        det = (snr >= 5) & np.array([clean(x) for x in df["cc_flags"]]) & np.isfinite(wobs)
        dm = wpred - wobs                                       # >0 means observed brighter = excess
        chi = (1.0 - np.power(10.0, -0.4 * dm)) / (LN10_04 * werr)
        chi[~det] = np.nan
        rows[f"{col}_chi"] = chi
        rows[f"{col}_pred_mag"] = wpred
        rows[f"{col}mpro"] = wobs
    res = pd.DataFrame(rows)
    res.to_parquet(OUT, index=False)

    print("\nEmpirical-null recalibration on the DEEPER W1/W2 (genomic-control λ):")
    for col in ["w1", "w2"]:
        x = res[f"{col}_chi"].to_numpy(float)
        n = int(np.isfinite(x).sum())
        d0, s0, lam = emp_null(x)
        zthr = d0 + 3.5 * s0                                   # inflation-aware flag threshold
        nflag = int(np.nansum(x > zthr))
        print(f"  {col.upper()}: n={n:,}  δ0={d0:+.2f}  σ0={s0:.2f}  λ={lam:.1f}  "
              f"z*={zthr:.1f}  → flagged(excess)={nflag}")
    print(f"\n  wrote {OUT}")
    print("  (v1 AllWISE λ was ~10.6 in W1 — the deeper sample re-derives its own null,")
    print("   per the frozen plan; flagged excesses go to the unchanged battery next.)")


if __name__ == "__main__":
    main()
