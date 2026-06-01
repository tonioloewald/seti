#!/usr/bin/env python3
"""Step 6 input: NEOWISE multi-epoch W1/W2 light curves for the IR-excess set.

For the variability search (§1.1 / §5.3): does an IR excess *fluctuate*? We pull
NEOWISE-R single-exposure photometry (neowiser_p1bs_psd) for the battery's
W3/W4-excess candidates via a single bulk IRSA-TAP spatial cross-match (upload the
Gaia positions, server-side join), chunked. Each light curve is then cleaned for the
white-dwarf proper-motion / background-source trap:
  - good frames (qual_frame>0, clean cc_flags, W1 S/N>=3);
  - reject epochs whose W1 differs from the AllWISE W1 by >1.5 mag (background/PM).

Output (gitignored): data/raw/neowise/neowise_excess_epochs.parquet
"""
import os, time, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from astropy.table import Table
import pyvo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BAT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
OUTDIR = os.path.join(ROOT, "data", "raw", "neowise")
OUT = os.path.join(OUTDIR, "neowise_excess_epochs.parquet")
RADIUS_DEG = 5 / 3600.0
CHUNK = 250
TAP = "https://irsa.ipac.caltech.edu/TAP"
ADQL = ("SELECT u.source_id, w.mjd, w.w1mpro, w.w1sigmpro, w.w2mpro, w.w2sigmpro, "
        "w.w1snr, w.w2snr, w.qual_frame, w.cc_flags "
        "FROM neowiser_p1bs_psd w, TAP_UPLOAD.tgt u "
        "WHERE CONTAINS(POINT('ICRS',w.ra,w.dec), "
        f"CIRCLE('ICRS',u.ra,u.dec,{RADIUS_DEG:.6f}))=1")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    bat = pd.read_parquet(BAT)[["source_id"]]; bat["source_id"] = bat["source_id"].astype(str)
    aw = pd.read_parquet(AW)[["source_id", "w1mpro"]].rename(columns={"w1mpro": "aw_w1"})
    aw["source_id"] = aw["source_id"].astype(str)
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    tgt = bat.merge(man, on="source_id").merge(aw, on="source_id")
    print(f"targets: {len(tgt):,}", flush=True)
    svc = pyvo.dal.TAPService(TAP)

    parts, t0 = [], time.time()
    for i in range(0, len(tgt), CHUNK):
        sub = tgt.iloc[i:i + CHUNK]
        up = Table.from_pandas(sub.rename(columns={"ra_deg": "ra", "dec_deg": "dec"})
                               [["source_id", "ra", "dec"]])
        for attempt in range(4):
            try:
                r = svc.run_async(ADQL, uploads={"tgt": up}).to_table().to_pandas()
                parts.append(r)
                break
            except Exception:
                time.sleep(5 * (attempt + 1))
        print(f"  chunk {i//CHUNK+1}/{(len(tgt)+CHUNK-1)//CHUNK}  "
              f"({time.time()-t0:.0f}s, {sum(len(p) for p in parts):,} epochs)", flush=True)

    ep = pd.concat(parts, ignore_index=True)
    for c in ["w1mpro", "w1sigmpro", "w2mpro", "w2sigmpro", "w1snr", "w2snr", "qual_frame"]:
        ep[c] = pd.to_numeric(ep[c], errors="coerce")
    ep["source_id"] = ep["source_id"].astype(str)
    ep = ep.merge(aw, on="source_id", how="left")
    good = (ep["qual_frame"] > 0) & \
           (ep["cc_flags"].astype(str).isin(["00", "0000", "0", ""])) & \
           (ep["w1snr"] >= 3) & (np.abs(ep["w1mpro"] - ep["aw_w1"]) < 1.5)
    clean = ep[good].drop(columns=["aw_w1"]).reset_index(drop=True)
    clean.to_parquet(OUT, index=False)
    print(f"raw {len(ep):,} epochs -> clean {len(clean):,} for "
          f"{clean['source_id'].nunique():,} sources -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
