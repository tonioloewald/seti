#!/usr/bin/env python3
"""Step (fetch) 6: CatWISE2020 deeper W1/W2 cross-match (v2 amendment).

Pre-registered in `preregistration_v2_unwise.md` (frozen at commit f510757, before this
fetch). Positional cross-match of the frozen WD sample against the CatWISE2020 catalogue
(Marocco et al. 2021), which reaches ~0.8 mag deeper in W1 and ~1.5 mag deeper in W2 than the
AllWISE depths used in v1. We retrieve every CatWISE2020 source within 3" of each WD (so the
analysis can apply the pre-specified nearest-within-2" match + reject-if-second-within-3"
blend guard). source_id is uploaded to IRSA as int64 (IRSA TAP rejects unicode upload
columns) and converted back to string on return.

Resumable: checkpoints by chunk index. Output (gitignored): data/raw/catwise/catwise_xmatch.parquet
"""
import os, time, json, hashlib
import numpy as np, pandas as pd, pyvo
from astropy.table import Table

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
OUTDIR = os.path.join(ROOT, "data", "raw", "catwise")
OUT = os.path.join(OUTDIR, "catwise_xmatch.parquet")
CKPT = os.path.join(OUTDIR, "_catwise_ckpt.json")
PROV = os.path.join(ROOT, "data", "manifests", "catwise_xmatch.provenance.json")
TAP = "https://irsa.ipac.caltech.edu/TAP"
RADIUS_DEG = 3.0 / 3600.0
CHUNK = 1500
ADQL = ("SELECT u.source_id, c.ra AS cw_ra, c.dec AS cw_dec, "
        "c.w1mpro, c.w1sigmpro, c.w2mpro, c.w2sigmpro, c.w1snr, c.w2snr, "
        "c.cc_flags, c.ab_flags "
        "FROM catwise_2020 c, TAP_UPLOAD.tgt u "
        f"WHERE CONTAINS(POINT('ICRS',c.ra,c.dec),CIRCLE('ICRS',u.ra,u.dec,{RADIUS_DEG:.6f}))=1")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    svc = pyvo.dal.TAPService(TAP)
    nchunks = (len(man) + CHUNK - 1) // CHUNK

    start, parts = 0, []
    if os.path.exists(CKPT) and os.path.exists(OUT):
        start = json.load(open(CKPT)).get("next_chunk", 0)
        parts = [pd.read_parquet(OUT)]
        print(f"resuming at chunk {start}/{nchunks}", flush=True)

    t0 = time.time()
    for ci in range(start, nchunks):
        sub = man.iloc[ci * CHUNK:(ci + 1) * CHUNK]
        up = Table.from_pandas(sub.rename(columns={"ra_deg": "ra", "dec_deg": "dec"})
                               [["source_id", "ra", "dec"]])
        up["source_id"] = up["source_id"].astype("int64")
        for attempt in range(4):
            try:
                r = svc.run_async(ADQL, uploads={"tgt": up}).to_table().to_pandas()
                if len(r):
                    r["source_id"] = r["source_id"].astype("int64").astype(str)
                    parts.append(r)
                break
            except Exception:
                time.sleep(5 * (attempt + 1))
        if ci % 5 == 0 or ci == nchunks - 1:
            pd.concat(parts, ignore_index=True).to_parquet(OUT, index=False)
            json.dump({"next_chunk": ci + 1}, open(CKPT, "w"))
            nm = sum(len(p) for p in parts)
            print(f"  chunk {ci+1}/{nchunks}  ({time.time()-t0:.0f}s, {nm:,} matches)", flush=True)

    res = pd.concat(parts, ignore_index=True)
    # nearest match + separation; blend guard applied in analysis
    m = res.merge(man.rename(columns={"ra_deg": "wd_ra", "dec_deg": "wd_dec"}), on="source_id")
    res["sep_arcsec"] = np.hypot((m.cw_ra - m.wd_ra) * np.cos(np.radians(m.wd_dec)),
                                 m.cw_dec - m.wd_dec) * 3600.0
    res.to_parquet(OUT, index=False)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    json.dump({"table": "catwise_2020", "service": TAP, "radius_arcsec": 3.0,
               "n_targets": int(len(man)), "n_rows": int(len(res)),
               "n_wd_matched": int(res.source_id.nunique()), "sha256_out": sha},
              open(PROV, "w"), indent=2)
    print(f"done: {len(res):,} CatWISE rows for {res.source_id.nunique():,} WDs "
          f"({100*res.source_id.nunique()/len(man):.1f}%) -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
