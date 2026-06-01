#!/usr/bin/env python3
"""Step 4b: vet the cold-fit IR-excess candidates (Channel A residual).

Takes the battery's cold (T_x < 300 K) fits and applies the remaining
natural-explanation filters before anything is called a residual:
  - contamination: clean AllWISE cc_flags and ext_flag = 0;
  - reliability:   a reliable (ph_qual A/B) W3 or W4 detection with S/N >= 5;
  - cirrus (item 3): SFD E(B-V) at the position below a ceiling (high cirrus -> the
                     cold W3/W4 "excess" is likely Galactic dust, not circumstellar).

Survivors are the un-explained cold candidates to scrutinise further (NOT yet claimed
as anomalies — the A-based empirical null and independent follow-up still apply).
"""
import os, time
import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.ipac.irsa.irsa_dust import IrsaDust

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BAT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
OUT = os.path.join(ROOT, "data", "derived", "cold_candidates_vetted.parquet")
EBV_CEILING = 0.15   # pre-data cirrus ceiling (logged in IMPLEMENTATION_LOG)


def ebv_sfd(ra, dec):
    for attempt in range(3):
        try:
            t = IrsaDust.get_query_table(SkyCoord(ra, dec, unit="deg"), section="ebv")
            for col in ("ext SFD mean", "ext SFD ref", "ext SandF mean"):
                if col in t.colnames:
                    return float(t[col][0])
            return float("nan")
        except Exception:
            time.sleep(3 * (attempt + 1))
    return float("nan")


def main():
    b = pd.read_parquet(BAT)
    aw = pd.read_parquet(AW)
    man = pd.read_csv(MAN)[["source_id", "ra_deg", "dec_deg"]]
    cold = b[b["class"] == "COLD_candidate(<300K)"].merge(aw, on="source_id", how="left")

    cc = cold["cc_flags"].astype(str)
    clean = (cc.str.replace("0", "").str.replace("-", "") == "") & (cold["ext_flag"].fillna(0) == 0)
    ph = cold["ph_qual"].astype(str)
    snr = lambda e: np.where(np.isfinite(e) & (e > 0), 1.0 / (0.9210340 * e), 0.0)
    relW3 = ph.str[2].isin(["A", "B"]) & (snr(cold["w3mpro_error"].to_numpy(float)) >= 5)
    relW4 = ph.str[3].isin(["A", "B"]) & (snr(cold["w4mpro_error"].to_numpy(float)) >= 5)
    surv = cold[clean & (relW3 | relW4)].merge(man, on="source_id", how="left").copy()
    print(f"cold-fit: {len(cold)}  ->  clean+reliable: {len(surv)}  -> querying cirrus...")

    ebv = []
    for _, r in surv.iterrows():
        e = ebv_sfd(r["ra_deg"], r["dec_deg"])
        ebv.append(e)
        print(f"    {int(r['source_id'])}  T_x={r['T_x']:.0f}K  E(B-V)={e:.3f}"
              f"  {'CIRRUS' if (np.isfinite(e) and e > EBV_CEILING) else 'low-cirrus'}")
    surv["ebv_sfd"] = ebv
    surv["cirrus_flag"] = surv["ebv_sfd"] > EBV_CEILING
    final = surv[~surv["cirrus_flag"]]
    surv.to_parquet(OUT, index=False)
    print(f"\n  after cirrus ceiling E(B-V) <= {EBV_CEILING}: "
          f"{len(final)} survive (of {len(surv)})")
    print(f"  wrote {OUT}")
    if len(final):
        print("  surviving cold candidates (source_id, T_x K, E(B-V)):")
        for _, r in final.iterrows():
            print(f"    {int(r['source_id'])}  {r['T_x']:.0f}  {r['ebv_sfd']:.3f}")


if __name__ == "__main__":
    main()
