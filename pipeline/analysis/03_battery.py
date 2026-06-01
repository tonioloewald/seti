#!/usr/bin/env python3
"""Step 4: natural-explanation battery for IR excesses (Channel A, Stage 2 / §5.2-5.3).

Focus set: WDs detected in W3 and/or W4 — the cooler bands where the photosphere is
negligible, so any detection IS a real excess (the clean, unambiguous excess sample;
no photosphere-scatter contamination). For each, we fit a blackbody to the excess SED
(observed - predicted photosphere, in the detected bands with positive excess) and read
off the best-fit excess temperature T_x and solid angle.

Per §5.3, the natural explanations are a debris disk (~300-1500 K) and a cool/brown-dwarf
companion (~1500-4000 K). The agnostic free-T fit gives T_x; an excess whose T_x lands
in those natural regimes is *natural* (a disk or companion), not an anomaly. The
interesting residual is anything that does NOT (e.g. T_x < ~300 K cold dust, or no
acceptable blackbody) — but note WISE cannot detect truly cold (<~150 K) excess, so the
cold anomaly search lives in the upper-limit layer, not here (§4.A).

Output: data/derived/battery_w34.parquet (gitignored) + a printed summary.
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IRX = os.path.join(ROOT, "data", "derived", "ir_excess.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
OUT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")

F0 = {1: 309.540, 2: 171.787, 3: 31.674, 4: 8.363}        # WISE Vega zero-points (Jy)
LAM = {1: 3.3526, 2: 4.6028, 3: 11.5608, 4: 22.0883}      # band eff. wavelength (um)
LN10_04 = 0.4 * np.log(10.0)
HCK = 14387.77                                            # h c / k in um*K

# natural-regime boundaries (pre-data choice; logged in IMPLEMENTATION_LOG)
DISK = (300.0, 1500.0)
COMP = (1500.0, 4000.0)


def fit_excess_bb(lam, fexc, sig):
    """Best blackbody (T, Omega>=0) for excess fluxes; returns (chi2, T_x, Omega, dof)."""
    Tg = np.logspace(np.log10(40.0), np.log10(5000.0), 200)
    best = (np.inf, np.nan, np.nan)
    for T in Tg:
        B = (1.0 / lam**3) / np.expm1(HCK / (lam * T))
        denom = np.sum(B * B / sig**2)
        Om = np.sum(fexc * B / sig**2) / denom if denom > 0 else 0.0
        Om = max(Om, 0.0)
        chi2 = np.sum(((fexc - Om * B) / sig) ** 2)
        if chi2 < best[0]:
            best = (chi2, T, Om)
    return best[0], best[1], best[2], len(lam) - 1


def main():
    irx = pd.read_parquet(IRX); irx["source_id"] = irx["source_id"].astype(str)
    aw = pd.read_parquet(AW)[["source_id", "ph_qual"] +
                            [f"w{b}mpro" for b in range(1, 5)] +
                            [f"w{b}mpro_error" for b in range(1, 5)]]
    aw["source_id"] = aw["source_id"].astype(str)
    df = irx.merge(aw, on="source_id", how="inner")
    ph = df["ph_qual"].astype(str).to_numpy()
    cand = np.array([len(s) == 4 and (s[2] in "ABC" or s[3] in "ABC") for s in ph])
    df = df[cand].reset_index(drop=True)
    print(f"W3/W4-excess candidate set: {len(df):,}")

    rows = []
    for _, r in df.iterrows():
        s = str(r["ph_qual"])
        lam, fexc, sig = [], [], []
        for b in range(1, 5):
            if s[b - 1] not in "ABC":
                continue
            mobs = r[f"w{b}mpro"]; merr = r[f"w{b}mpro_error"]
            mpred = r[f"w{b}_pred_mag"]
            if not np.isfinite(mobs) or not np.isfinite(mpred) or not np.isfinite(merr):
                continue
            fo = F0[b] * 10 ** (-0.4 * mobs)
            fp = F0[b] * 10 ** (-0.4 * mpred)
            fx = fo - fp
            if fx <= 0:
                continue
            lam.append(LAM[b]); fexc.append(fx); sig.append(fo * LN10_04 * merr)
        if len(lam) < 2:
            rows.append((r["source_id"], len(lam), np.nan, np.nan, "unresolved_<2band"))
            continue
        chi2, Tx, Om, dof = fit_excess_bb(np.array(lam), np.array(fexc), np.array(sig))
        if not np.isfinite(Tx):
            cls = "fit_failed"
        elif Tx < DISK[0]:
            cls = "COLD_candidate(<300K)"
        elif Tx <= DISK[1]:
            cls = "natural_disk"
        elif Tx <= COMP[1]:
            cls = "natural_companion"
        else:
            cls = "hot(>4000K)"
        rows.append((r["source_id"], len(lam), Tx, chi2, cls))

    res = pd.DataFrame(rows, columns=["source_id", "n_excess_bands", "T_x", "chi2", "class"])
    res.to_parquet(OUT, index=False)
    print(f"  wrote {OUT}")
    fitted = res[res["T_x"].notna()]
    print(f"  fitted (>=2 excess bands): {len(fitted):,}")
    if len(fitted):
        print(f"  T_x median {fitted['T_x'].median():.0f} K, "
              f"range [{fitted['T_x'].min():.0f}, {fitted['T_x'].max():.0f}]")
    print("  classification:")
    for c, n in res["class"].value_counts().items():
        print(f"    {c:<24} {n:>5}")


if __name__ == "__main__":
    main()
