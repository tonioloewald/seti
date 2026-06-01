#!/usr/bin/env python3
"""Step 6 input: NEOWISE multi-epoch W1/W2 light curves for the IR-excess set.

For the variability search (§1.1 / §5.3), the highest-value question is whether an
IR excess *fluctuates*. We pull NEOWISE-R single-exposure photometry
(neowiser_p1bs_psd at IRSA) for the battery's W3/W4-excess candidates, cleaning each
light curve for the white-dwarf proper-motion / background-source trap:

  - query a 5" cone at the Gaia position;
  - keep good frames (qual_frame>0, clean cc_flags, W1 S/N>=3);
  - reject epochs whose W1 differs from the AllWISE W1 by >1.5 mag (background/PM).

Resumable (per-source rows accumulated to a checkpoint). Output (gitignored):
  data/raw/neowise/neowise_excess_epochs.parquet
"""
import os, time, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.ipac.irsa import Irsa

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BAT = os.path.join(ROOT, "data", "derived", "battery_w34.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
OUTDIR = os.path.join(ROOT, "data", "raw", "neowise")
OUT = os.path.join(OUTDIR, "neowise_excess_epochs.parquet")
CKPT = os.path.join(OUTDIR, "_checkpoint.parquet")
RADIUS = 5 * u.arcsec
KEEP = ["mjd", "w1mpro", "w1sigmpro", "w2mpro", "w2sigmpro", "w1snr", "w2snr"]


def query_lc(ra, dec, aw_w1):
    for attempt in range(3):
        try:
            t = Irsa.query_region(SkyCoord(ra, dec, unit="deg"),
                                  catalog="neowiser_p1bs_psd", spatial="Cone", radius=RADIUS)
            break
        except Exception:
            time.sleep(3 * (attempt + 1))
    else:
        return None
    if t is None or len(t) == 0:
        return None
    d = t.to_pandas()
    for c in KEEP + ["qual_frame", "cc_flags"]:
        if c not in d.columns:
            d[c] = np.nan
    good = (pd.to_numeric(d["qual_frame"], errors="coerce") > 0) & \
           (d["cc_flags"].astype(str).isin(["00", "0000", "0", ""])) & \
           (pd.to_numeric(d["w1snr"], errors="coerce") >= 3) & \
           (np.abs(pd.to_numeric(d["w1mpro"], errors="coerce") - aw_w1) < 1.5)
    d = d[good]
    return d[KEEP] if len(d) else None


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    bat = pd.read_parquet(BAT)[["source_id"]]
    aw = pd.read_parquet(AW)[["source_id", "w1mpro"]]
    man = pd.read_csv(MAN)[["source_id", "ra_deg", "dec_deg"]]
    tgt = bat.merge(aw, on="source_id").merge(man, on="source_id").dropna(subset=["w1mpro"])
    done = set()
    parts = []
    if os.path.exists(CKPT):
        prev = pd.read_parquet(CKPT)
        parts.append(prev); done = set(prev["source_id"].unique())
    print(f"targets: {len(tgt):,}  already done: {len(done)}", flush=True)

    t0 = time.time()
    for i, (_, r) in enumerate(tgt.iterrows()):
        sid = int(r["source_id"])
        if sid in done:
            continue
        lc = query_lc(r["ra_deg"], r["dec_deg"], r["w1mpro"])
        if lc is not None and len(lc):
            lc = lc.copy(); lc.insert(0, "source_id", sid)
            parts.append(lc)
        if i % 25 == 0:
            pd.concat(parts, ignore_index=True).to_parquet(CKPT, index=False) if parts else None
            print(f"  {i+1}/{len(tgt)}  ({time.time()-t0:.0f}s, {sum(len(p) for p in parts):,} epochs)", flush=True)
    full = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    full.to_parquet(OUT, index=False)
    n_src = full["source_id"].nunique() if len(full) else 0
    print(f"done: {len(full):,} epochs for {n_src:,} sources -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
