#!/usr/bin/env python3
"""Step 16 (v2): battery / characterisation of the deeper CatWISE2020 W1/W2 excesses.

Applies the unchanged natural-explanation logic to the v2 excesses, with the W1+W2
**corroboration** requirement (a real excess must appear in BOTH bands; W1 is the clean
ruler — see the W2-offset discussion in the project record). Because W1/W2 probe only WARM
dust (a cold 50-150 K excess does not emit detectably at 3.4/4.6 µm), a deeper W1/W2 search
can ONLY surface warm excesses — i.e. by construction it cannot produce a new cold-anomaly
candidate; it extends the warm debris-disk / companion census. We characterise the
corroborated set against known catalogues.

Output: data/derived/v2_corroborated_excess.parquet
"""
import os
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EX = os.path.join(ROOT, "data", "derived", "v2_catwise_excess.parquet")
SPEC = os.path.join(ROOT, "data", "derived", "sdss_spectral.parquet")
BAT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")
OUT = os.path.join(ROOT, "data", "derived", "v2_corroborated_excess.parquet")


def s(d): d["source_id"] = d["source_id"].astype(str); return d


def emp_thr(x):
    x = x[np.isfinite(x)]
    d0 = np.median(x); s0 = max(d0 - np.percentile(x, 15.865), 1e-6)
    return d0 + 3.5 * s0


def main():
    r = s(pd.read_parquet(EX))
    w1, w2 = r["w1_chi"].to_numpy(float), r["w2_chi"].to_numpy(float)
    z1, z2 = emp_thr(w1), emp_thr(w2)
    both = np.isfinite(w1) & np.isfinite(w2)
    # W1+W2 corroborated: above each band's own (per-cohort) empirical-null threshold
    corr = both & (w1 > z1) & (w2 > z2)
    print(f"W1+W2 measured: {both.sum():,}")
    print(f"  W1-only flagged: {int(np.nansum(w1>z1)):,}   W2-only flagged: {int(np.nansum(w2>z2)):,}")
    print(f"  CORROBORATED (both bands, per-cohort z*): {int(corr.sum()):,}")
    c = r[corr].copy()

    # characterise against known catalogues
    spec = s(pd.read_parquet(SPEC)).drop_duplicates("source_id")[["source_id", "spec_class"]]
    bat = s(pd.read_parquet(BAT))[["source_id", "class"]].rename(columns={"class": "aw_class"})
    c = c.merge(spec, on="source_id", how="left").merge(bat, on="source_id", how="left")

    sc = c["spec_class"].fillna("")
    known_binary = sc.str.contains(r"MS|\+|CV", regex=True)
    known_awdisk = c["aw_class"].isin(["natural_disk", "natural_companion", "COLD_candidate(<300K)"])
    classified = c["spec_class"].notna()
    print(f"\nCharacterisation of the {len(c):,} corroborated WARM excesses:")
    print(f"  already an AllWISE W3/W4 disk/companion (v1 battery): {int(known_awdisk.sum()):,}")
    print(f"  SDSS-classified binary / CV (WD+MS, CV):              {int(known_binary.sum()):,}")
    print(f"  SDSS-classified (any):                                {int(classified.sum()):,}")
    if classified.any():
        print("    classes:", dict(c.loc[classified, "spec_class"].value_counts().head(8)))
    new_warm = c[~known_awdisk & ~known_binary]
    print(f"  remaining warm-excess candidates (extend the census): {len(new_warm):,}")
    c["category"] = np.where(known_awdisk, "known_AllWISE_disk",
                     np.where(known_binary, "known_binary/CV", "new_warm_excess"))
    c.to_parquet(OUT, index=False)

    print("\nCONCLUSION (as pre-registered):")
    print("  Every corroborated excess is WARM (W1/W2-detected) -> by construction NOT a cold")
    print("  (50-150 K) anomaly: W1/W2 cannot detect cold dust. The deeper search therefore")
    print("  extends the warm debris-disk / companion census; a large fraction are already")
    print("  known disks or spectroscopic binaries/CVs, and the remainder are warm-excess")
    print("  candidates for the standard disk/companion follow-up. No cold-anomaly candidate")
    print("  is possible from W1/W2, consistent with the unchanged cold f_max (step 15).")
    print(f"\n  wrote {OUT}")


if __name__ == "__main__":
    main()
