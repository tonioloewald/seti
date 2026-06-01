#!/usr/bin/env python3
"""Step 6: time-variability of the IR excess (§1.1 highest-value signature, §5.3).

For each IR-excess WD with a NEOWISE light curve, compute two variability metrics on
the cleaned W1/W2 epochs:
  - reduced chi^2 of W1 vs a constant (variability amplitude vs per-epoch errors);
  - the Stetson J index on simultaneous (W1,W2) pairs -- *correlated* two-band
    variability, which a real astrophysical signal produces and noise does not. This
    is the proxy for the "structured" variation §1.1 prizes.

Both are empirical-null calibrated (the bulk = quiet WDs define the null; the tail =
variables). Flagged variables are then vetted against the natural sources of IR
variability already in the battery: debris-disk variability and brown-dwarf "weather"
(companions, §5.2 item 2), plus W1 saturation for very bright sources.

DISCIPLINE: thresholds come from the empirical null, not from inspecting the list.
Output (gitignored): data/derived/variability.parquet
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LC = os.path.join(ROOT, "data", "raw", "neowise", "neowise_excess_epochs.parquet")
BAT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
OUT = os.path.join(ROOT, "data", "derived", "variability.parquet")
MIN_EP = 10


def stetson_J(m1, s1, m2, s2):
    n = len(m1)
    if n < 2:
        return np.nan
    k = np.sqrt(n / (n - 1.0))
    d1 = k * (m1 - np.average(m1, weights=1 / s1**2)) / s1
    d2 = k * (m2 - np.average(m2, weights=1 / s2**2)) / s2
    P = d1 * d2
    return np.sum(np.sign(P) * np.sqrt(np.abs(P))) / n


def emp_null(x):
    x = x[np.isfinite(x)]
    d0 = np.median(x)
    s0 = max(d0 - np.percentile(x, 15.865), 1e-6)
    return d0, s0


def main():
    lc = pd.read_parquet(LC)
    for c in ["w1mpro", "w1sigmpro", "w2mpro", "w2sigmpro"]:
        lc[c] = pd.to_numeric(lc[c], errors="coerce")
    rows = []
    for sid, g in lc.groupby("source_id"):
        w1 = g["w1mpro"].to_numpy(); s1 = g["w1sigmpro"].to_numpy()
        ok = np.isfinite(w1) & np.isfinite(s1) & (s1 > 0)
        w1, s1 = w1[ok], s1[ok]
        if len(w1) < MIN_EP:
            continue
        wbar = np.average(w1, weights=1 / s1**2)
        chi2red = np.sum(((w1 - wbar) / s1) ** 2) / (len(w1) - 1)
        # Stetson J on simultaneous W1/W2
        w2 = g["w2mpro"].to_numpy()[ok]; s2 = g["w2sigmpro"].to_numpy()[ok]
        ok2 = np.isfinite(w2) & np.isfinite(s2) & (s2 > 0)
        J = stetson_J(w1[ok2], s1[ok2], w2[ok2], s2[ok2]) if ok2.sum() >= MIN_EP else np.nan
        rows.append((sid, len(w1), wbar, chi2red, J))
    v = pd.DataFrame(rows, columns=["source_id", "n_ep", "w1_mean", "chi2red", "stetson_J"])

    d0c, s0c = emp_null(v["chi2red"].to_numpy())
    d0j, s0j = emp_null(v["stetson_J"].to_numpy())
    v["z_chi2"] = (v["chi2red"] - d0c) / s0c
    v["z_J"] = (v["stetson_J"] - d0j) / s0j
    from scipy.stats import norm
    zthr = float(norm.ppf(1 - 0.05 / max(len(v), 1)))   # conservative Bonferroni
    v["variable_flag"] = (v["z_chi2"] > zthr) & (v["z_J"] > zthr)  # amplitude AND correlated

    # vet flagged against natural variability
    bat = pd.read_parquet(BAT)[["source_id", "class"]]
    aw = pd.read_parquet(AW)[["source_id"]]
    v = v.merge(bat, on="source_id", how="left")
    v["saturated"] = v["w1_mean"] < 8.0
    v.to_parquet(OUT, index=False)

    print(f"sources with NEOWISE LC (>= {MIN_EP} epochs): {len(v):,}")
    print(f"  chi2red empirical null: delta0={d0c:.2f} sigma0={s0c:.2f}")
    print(f"  Stetson J empirical null: delta0={d0j:.3f} sigma0={s0j:.3f}")
    print(f"  conservative z* = {zthr:.2f}")
    flagged = v[v["variable_flag"]]
    print(f"  flagged variable (amplitude AND correlated): {len(flagged)}")
    if len(flagged):
        print("  flagged, with natural-explanation vet:")
        for _, r in flagged.sort_values("z_J", ascending=False).iterrows():
            nat = []
            if r["class"] in ("natural_disk",): nat.append("disk-var")
            if r["class"] in ("natural_companion",): nat.append("BD-weather")
            if r["saturated"]: nat.append("W1-saturated")
            tag = ",".join(nat) if nat else "** UNEXPLAINED **"
            print(f"    {int(r['source_id'])}  n={int(r['n_ep'])}  chi2red={r['chi2red']:.1f}"
                  f"  J={r['stetson_J']:.2f}  class={r['class']}  -> {tag}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
