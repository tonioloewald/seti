#!/usr/bin/env python3
"""Step 2b: cross-match the frozen WD sample to AllWISE via the Gaia archive's
precomputed, source_id-keyed cross-match (deterministic — no fuzzy positional
matching).

Reads data/manifests/wd_sample.csv.gz; for each chunk of source_ids, joins
gaiaedr3.allwise_best_neighbour -> gaiadr1.allwise_original_valid and pulls
W1-W4 (mpro + errors), quality flags (cc_flags, ph_qual, ext_flag, var_flag),
and per-band mean MJDs. Writes per-chunk parquet (resumable) then a merged,
source_id-sorted table to data/raw/allwise/ (gitignored), with provenance +
SHA-256 in data/manifests/.

AllWISE is a *detection* catalogue, so this yields photometry only for the
WISE-detected subset (~8%, the IR-excess-measurable objects). W3/W4 rows flagged
ph_qual='U' are upper limits (preregistration.md §5.3). Forced-photometry upper
limits for the non-detected majority are a separate step (see SOURCES.md).
"""
import csv, glob, gzip, hashlib, json, os, time, warnings
from datetime import datetime, timezone
warnings.filterwarnings("ignore")
from astroquery.gaia import Gaia
import pandas as pd

Gaia.ROW_LIMIT = -1
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw", "allwise")
CH = os.path.join(RAW, "chunks")
MAN = os.path.join(ROOT, "data", "manifests")
CHUNK = 5000
RETRIES = 4

QUERY = """
SELECT bn.source_id, bn.angular_distance, w.designation, w.ra, w.dec,
       w.w1mpro, w.w1mpro_error, w.w2mpro, w.w2mpro_error,
       w.w3mpro, w.w3mpro_error, w.w4mpro, w.w4mpro_error,
       w.cc_flags, w.ph_qual, w.ext_flag, w.var_flag,
       w.w1mjd_mean, w.w2mjd_mean, w.w3mjd_mean, w.w4mjd_mean
FROM gaiaedr3.allwise_best_neighbour AS bn
JOIN gaiadr1.allwise_original_valid AS w ON bn.allwise_oid = w.allwise_oid
WHERE bn.source_id IN ({ids})
"""


def load_ids():
    ids = []
    with gzip.open(os.path.join(MAN, "wd_sample.csv.gz"), "rt") as f:
        for row in csv.DictReader(f):
            ids.append(row["source_id"])
    return ids


def run_chunk(ids):
    adql = QUERY.format(ids=",".join(ids))
    last = None
    for attempt in range(RETRIES):
        try:
            return Gaia.launch_job_async(adql).get_results()
        except Exception as e:
            last = e
            time.sleep(5 * (attempt + 1))
    raise last


def main():
    os.makedirs(CH, exist_ok=True)
    ids = load_ids()
    n = len(ids)
    nchunks = (n + CHUNK - 1) // CHUNK
    print(f"{n:,} source_ids -> {nchunks} chunks of {CHUNK}", flush=True)
    t0 = time.time()
    n_matched = 0
    for i in range(nchunks):
        out = os.path.join(CH, f"chunk_{i:04d}.parquet")
        if os.path.exists(out) or os.path.exists(out + ".empty"):
            continue
        res = run_chunk(ids[i * CHUNK:(i + 1) * CHUNK])
        if len(res):
            res.to_pandas().to_parquet(out, index=False)
        else:
            open(out + ".empty", "w").close()
        if i % 10 == 0 or i == nchunks - 1:
            print(f"  chunk {i + 1}/{nchunks}  ({time.time() - t0:.0f}s)", flush=True)

    parts = sorted(glob.glob(os.path.join(CH, "chunk_*.parquet")))
    if not parts:
        print("no matches"); return
    merged = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)
    merged = merged.sort_values("source_id").reset_index(drop=True)
    mp = os.path.join(RAW, "allwise_xmatch.parquet")
    merged.to_parquet(mp, index=False)
    n_matched = len(merged)
    h = hashlib.sha256()
    with open(mp, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    sha = h.hexdigest()
    print(f"merged {n_matched:,} AllWISE matches -> {mp}\n  sha256 {sha}", flush=True)
    prov = {
        "step": "2b AllWISE cross-match",
        "join": "gaiaedr3.allwise_best_neighbour -> gaiadr1.allwise_original_valid (allwise_oid)",
        "accessed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_source_ids": n,
        "n_matched": n_matched,
        "match_rate": round(n_matched / n, 4),
        "chunk_size": CHUNK,
        "product": "data/raw/allwise/allwise_xmatch.parquet (gitignored)",
        "sha256": sha,
        "query": QUERY.strip(),
    }
    json.dump(prov, open(os.path.join(MAN, "allwise_xmatch.provenance.json"), "w"), indent=2)
    print("wrote provenance to data/manifests/allwise_xmatch.provenance.json")


if __name__ == "__main__":
    main()
