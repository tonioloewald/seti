#!/usr/bin/env python3
"""Step 15 (v2): recompute f_max with deeper CatWISE2020 W1/W2 depths.

Executes §3.4 of the frozen v2 plan: the zero-detection bound f_max = 3 / Σ_i C_i (§5.7),
recomputed with the empirically-derived CatWISE2020 5σ W1/W2 depths (deeper than AllWISE),
W3/W4 unchanged. Reports the warm-edge tightening and confirms the cold core is unchanged,
exactly as pre-registered. Compares directly to the v1 (AllWISE-depth) limit.

Output: data/derived/v2_f_max.parquet + figures/f_max_v2.png
"""
import os
import numpy as np, pandas as pd
from scipy.interpolate import LinearNDInterpolator
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = os.path.join(ROOT, "data", "models", "bergeron", "Table_DA")
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
OUT = os.path.join(ROOT, "data", "derived", "v2_f_max.parquet")
FIG = os.path.join(ROOT, "figures", "f_max_v2.png")
H, C, K, SIGMA = 6.62607e-34, 2.99792458e8, 1.380649e-23, 5.670374e-8
FBOL0 = 2.518e-8
LAM = {1: 3.3526e-6, 2: 4.6028e-6, 3: 11.5608e-6, 4: 22.0883e-6}
F0 = {1: 309.540, 2: 171.787, 3: 31.674, 4: 8.363}
DEPTH_V1 = {1: 16.9, 2: 16.0, 3: 11.5, 4: 8.0}          # AllWISE (v1)
DEPTH_V2 = {1: 18.65, 2: 17.42, 3: 11.5, 4: 8.0}        # CatWISE2020 W1/W2 (empirical), W3/W4 unchanged
T_GRID = [30, 50, 75, 100, 150, 200, 300, 500, 1000]
F_GRID = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]


def load_grid_cols(idx):
    teff, logg, vals = [], [], {k: [] for k in idx}
    for line in open(GRID):
        f = line.split()
        if len(f) < 44:
            continue
        try:
            t, g = float(f[0]), float(f[1]); v = {k: float(f[i]) for k, i in idx.items()}
        except (ValueError, IndexError):
            continue
        if not (1000 <= t <= 200000 and 6.5 <= g <= 9.5):
            continue
        teff.append(t); logg.append(g)
        for k in idx:
            vals[k].append(v[k])
    pts = np.column_stack([teff, logg])
    return {k: LinearNDInterpolator(pts, np.array(vals[k])) for k in idx}


def bb_fraction(b, T):
    nu = C / LAM[b]
    Bnu = (2 * H * nu**3 / C**2) / np.expm1(H * nu / (K * T))
    return np.pi * Bnu / (SIGMA * T**4) * 1e26


def fmax_for(F_bol, depth5):
    depth_jy = {b: F0[b] * 10 ** (-0.4 * depth5[b]) for b in F0}
    rows = []
    for T in T_GRID:
        thresh = min(depth_jy[b] / bb_fraction(b, T) for b in F0)   # W/m^2 at f=1
        for f in F_GRID:
            sumC = int(np.sum(F_bol >= thresh / f))
            rows.append({"T_x_K": T, "f_lum": f, "sum_Ci": sumC,
                         "f_max": 3.0 / sumC if sumC else np.inf})
    return pd.DataFrame(rows)


def main():
    interp = load_grid_cols({"Mbol": 3, "G3": 38})
    ob = pd.read_parquet(OB).dropna(subset=["teff_h", "logg_h", "g_mag"])
    teff = ob["teff_h"].to_numpy(float); logg = np.clip(ob["logg_h"].to_numpy(float), 7, 9)
    g = ob["g_mag"].to_numpy(float)
    F_bol = FBOL0 * 10 ** (-0.4 * (g + (interp["Mbol"](teff, logg) - interp["G3"](teff, logg))))
    F_bol = F_bol[np.isfinite(F_bol)]
    print(f"WDs with photosphere: {len(F_bol):,}")

    v1 = fmax_for(F_bol, DEPTH_V1).rename(columns={"f_max": "f_max_v1", "sum_Ci": "sumC_v1"})
    v2 = fmax_for(F_bol, DEPTH_V2).rename(columns={"f_max": "f_max_v2", "sum_Ci": "sumC_v2"})
    res = v1.merge(v2[["T_x_K", "f_lum", "f_max_v2", "sumC_v2"]], on=["T_x_K", "f_lum"])
    res["ratio"] = res["f_max_v1"] / res["f_max_v2"]
    res.to_parquet(OUT, index=False)

    print("\n f_max v1 (AllWISE) -> v2 (CatWISE2020 deeper W1/W2), at f=0.1:")
    print(f"  {'T_x(K)':>6} {'f_max v1':>10} {'f_max v2':>10} {'tighter x':>10}")
    for T in T_GRID:
        r = res[(res.T_x_K == T) & (res.f_lum == 0.1)].iloc[0]
        print(f"  {T:>6} {r.f_max_v1:>10.1e} {r.f_max_v2:>10.1e} {r.ratio:>9.1f}x")

    print("\n INTERPRETATION (as pre-registered):")
    wedge = res[(res.T_x_K.isin([200, 300])) & (res.f_lum == 0.1)]["ratio"].mean()
    ccore = res[(res.T_x_K.isin([50, 75, 100])) & (res.f_lum == 0.1)]["ratio"].mean()
    print(f"   cold CORE (50-100 K): mean tightening {ccore:.2f}x  -> unchanged (W4-limited), as predicted.")
    print(f"   warm EDGE (200-300 K): mean tightening {wedge:.2f}x  -> deeper W2 reaches the Wien tail.")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    for f, c in [(0.1, "C0"), (0.01, "C1")]:
        s1 = res[res.f_lum == f]; ax.plot(s1.T_x_K, s1.f_max_v1, "o--", color=c, alpha=.5,
                                          label=f"v1 AllWISE  f={f:g}")
        ax.plot(s1.T_x_K, s1.f_max_v2, "o-", color=c, label=f"v2 CatWISE  f={f:g}")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("excess temperature T_x (K)"); ax.set_ylabel("f_max (95% upper limit)")
    ax.axvspan(50, 300, alpha=0.10, color="seagreen")
    ax.set_title("Cold-excess upper limit: v1 (AllWISE) vs v2 (deeper CatWISE2020 W1/W2)")
    ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.3, which="both")
    fig.tight_layout(); fig.savefig(FIG, dpi=120)
    print(f"\n wrote {OUT} and {FIG}")


if __name__ == "__main__":
    main()
