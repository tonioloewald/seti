#!/usr/bin/env python3
"""Step 5: the cold-excess upper limit f_max(T_x, f) — the registered headline (§5.7).

Injection-recovery via survey depth: a white dwarf *constrains* a cold excess of
temperature T_x carrying a fraction f of its bolometric luminosity if that excess
would have produced a >=5sigma WISE detection (i.e. its flux density exceeds the
AllWISE depth in some band). The per-object completeness C_i(T_x,f) is that boolean;
the registered zero-detection bound is

    f_max(T_x, f) = 3.0 / sum_i C_i(T_x, f)        (95% one-sided; §5.7)

This is computed for ALL sample WDs with a usable photosphere — the non-detected
majority included — so it is the population limit, not just the AllWISE-detected set.

NOTE (per §4.A): WISE's reddest band is 22 um, so for genuinely cold T_x (<~100 K)
the sensitivity collapses (sum C_i -> 0) and f_max is unconstrained. The curve is
meant to show exactly that honestly. Forced-photometry (CatWISE/unWISE) would deepen
W1/W2; that refinement is noted for a later amendment.

Output: data/derived/f_max.parquet (committed-small) + figures/f_max.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRID = os.path.join(ROOT, "data", "models", "bergeron", "Table_DA")
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
OUT = os.path.join(ROOT, "data", "derived", "f_max.parquet")
FIG = os.path.join(ROOT, "figures", "f_max.png")

# physical constants (SI)
H, C, K, SIGMA = 6.62607e-34, 2.99792458e8, 1.380649e-23, 5.670374e-8
FBOL0 = 2.518e-8                       # W/m^2 for apparent m_bol = 0 (IAU 2015)
LAM = {1: 3.3526e-6, 2: 4.6028e-6, 3: 11.5608e-6, 4: 22.0883e-6}   # m
F0 = {1: 309.540, 2: 171.787, 3: 31.674, 4: 8.363}                 # Jy
DEPTH5 = {1: 16.9, 2: 16.0, 3: 11.5, 4: 8.0}                       # AllWISE 5sig (Vega mag)
DEPTH_JY = {b: F0[b] * 10 ** (-0.4 * DEPTH5[b]) for b in F0}       # Jy

T_GRID = [30, 50, 75, 100, 150, 200, 300, 500, 1000]
F_GRID = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]


def load_grid_cols(cols_idx):
    """Return interpolators over (Teff, logg) for the given {name: data-col-index}."""
    from scipy.interpolate import LinearNDInterpolator
    teff, logg, vals = [], [], {k: [] for k in cols_idx}
    for line in open(GRID):
        f = line.split()
        if len(f) < 44:
            continue
        try:
            t, g = float(f[0]), float(f[1])
            v = {k: float(f[i]) for k, i in cols_idx.items()}
        except (ValueError, IndexError):
            continue
        if not (1000 <= t <= 200000 and 6.5 <= g <= 9.5):
            continue
        teff.append(t); logg.append(g)
        for k in cols_idx:
            vals[k].append(v[k])
    pts = np.column_stack([teff, logg])
    return {k: LinearNDInterpolator(pts, np.array(vals[k])) for k in cols_idx}


def bb_fraction(b, T):
    """pi*B_nu(nu_b,T)/(sigma T^4) in Jy per unit apparent bolometric W/m^2."""
    nu = C / LAM[b]
    Bnu = (2 * H * nu**3 / C**2) / np.expm1(H * nu / (K * T))   # W/m^2/Hz/sr
    return np.pi * Bnu / (SIGMA * T**4) * 1e26                  # -> Jy per (W/m^2)


def main():
    interp = load_grid_cols({"Mbol": 3, "G3": 38})   # data-col indices
    ob = pd.read_parquet(OB).dropna(subset=["teff_h", "logg_h", "g_mag"])
    teff = ob["teff_h"].to_numpy(float)
    logg = np.clip(ob["logg_h"].to_numpy(float), 7.0, 9.0)
    g_obs = ob["g_mag"].to_numpy(float)
    # apparent bolometric flux (distance-independent BC anchored on observed G)
    m_bol = g_obs + (interp["Mbol"](teff, logg) - interp["G3"](teff, logg))
    F_bol = FBOL0 * 10 ** (-0.4 * m_bol)             # W/m^2
    F_bol = F_bol[np.isfinite(F_bol)]
    n_used = len(F_bol)
    print(f"WDs with usable photosphere/bolometric flux: {n_used:,}")

    rows = []
    for T in T_GRID:
        # per-band sensitivity: an excess f*F_bol gives F_exc_i = f*F_bol*frac_i(T) [Jy]
        # detectable if F_exc_i >= depth_i for some band -> f*F_bol >= min_i(depth_i/frac_i)
        thresh_Fbol_unit_f = min(DEPTH_JY[b] / bb_fraction(b, T) for b in F0)  # W/m^2 at f=1
        for f in F_GRID:
            need_Fbol = thresh_Fbol_unit_f / f
            sumC = int(np.sum(F_bol >= need_Fbol))
            fmax = 3.0 / sumC if sumC > 0 else np.inf
            rows.append({"T_x_K": T, "f_lum": f, "sum_Ci": sumC, "f_max": fmax})
    res = pd.DataFrame(rows)
    res.to_parquet(OUT, index=False)

    # plot: f_max vs T_x for several f
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for f in F_GRID:
        sub = res[res["f_lum"] == f]
        ax.plot(sub["T_x_K"], sub["f_max"], "o-", label=f"f={f:g}")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("excess temperature $T_x$ (K)")
    ax.set_ylabel(r"$f_{\max}$  (95% upper limit on host fraction)")
    ax.set_title(f"Cold-excess upper limit  ($N={n_used:,}$ WDs, AllWISE depth)")
    ax.axvspan(20, 50, alpha=0.10, color="slategray")       # WISE-blind
    ax.axvspan(50, 300, alpha=0.12, color="seagreen")       # cold-anomaly window
    ax.axvspan(300, 1000, alpha=0.08, color="goldenrod")    # natural-disk regime
    y0 = ax.get_ylim()[0]
    ax.text(31, y0 * 3, "WISE-\nblind", fontsize=7, color="dimgray", ha="center")
    ax.text(123, y0 * 3, "cold-anomaly window\n(the constraint)", fontsize=7,
            color="darkgreen", ha="center")
    ax.text(550, y0 * 3, "natural-disk regime\n(excess = disk;\nnot an anomaly limit)",
            fontsize=7, color="saddlebrown", ha="center")
    ax.legend(title=r"$L_{exc}/L_{WD}$", fontsize=8, ncol=2, loc="upper right")
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout(); fig.savefig(FIG, dpi=120)

    print("\n f_max (95% upper limit on the fraction of WDs hosting the excess):")
    print("  T_x(K) |", "  ".join(f"f={f:g}" for f in F_GRID))
    for T in T_GRID:
        sub = res[res["T_x_K"] == T].set_index("f_lum")
        cells = []
        for f in F_GRID:
            fm = sub.loc[f, "f_max"]
            cells.append("  inf " if not np.isfinite(fm) else f"{fm:6.1e}")
        print(f"  {T:>5}  |", " ".join(cells))
    print("\n INTERPRETATION as an ANOMALY (technosignature) limit:")
    print("   T_x < ~50 K : WISE-blind (reddest band 22um) -> unconstrained.")
    print("   ~50-300 K   : cold-anomaly window -- a cold excess is both WISE-detectable")
    print("                 AND distinguishable from a natural (warm) disk. Zero")
    print("                 unexplained excesses found -> these f_max ARE the registered")
    print("                 constraint (RQ4): few e-3 to e-4 of WDs, per (T_x, f).")
    print("   > 300 K     : any excess is classified as a NATURAL debris disk (~536 found,")
    print("                 all natural) -> the tight numbers there are a generic IR-excess")
    print("                 detection limit, NOT an anomaly limit.")
    print(f"\n wrote {OUT} and {FIG}")


if __name__ == "__main__":
    main()
