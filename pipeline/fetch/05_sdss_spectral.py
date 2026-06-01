#!/usr/bin/env python3
"""Step (fetch) 5: SDSS spectral classifications for Channel C (accretion state).

Downloads the *second* table of the already-pinned Gentile Fusillo et al. 2021 VizieR
catalogue (J/MNRAS/508/3877) — `sdssspec.dat.gz`, the Gaia-SDSS spectroscopic sample
(41,820 rows) with a visual **spectral classification** per object. This is the
deterministic, citable source of *which* white dwarfs are metal-polluted (actively
accreting): any class containing 'Z' (Ca H&K lines). Channel C needs no new survey.

Pre-data amendment (post-registration): uses the same pinned release as the parent
catalogue; only a different table from it. Recorded in SOURCES.md.

Output: data/derived/sdss_spectral.parquet (source_id[str], specClass, Pwd, G, Teff).
"""
import os, gzip, hashlib, urllib.request, json
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw", "gentile_fusillo_2021")
OUT = os.path.join(ROOT, "data", "derived", "sdss_spectral.parquet")
PROV = os.path.join(ROOT, "data", "manifests", "sdss_spectral.provenance.json")
BASE = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/508/3877"
URL = f"{BASE}/sdssspec.dat.gz"
LOCAL = os.path.join(RAW, "sdssspec.dat.gz")

# fixed-width byte ranges (1-indexed, inclusive) from the catalogue ReadMe
COLS = {"source_id": (25, 43), "p_wd": (117, 124), "g_mag": (128, 134),
        "teff_h": (173, 181), "spec_class": (496, 501)}


def sl(line, rng):
    return line[rng[0] - 1:rng[1]].strip()


def fnum(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    os.makedirs(RAW, exist_ok=True)
    if not os.path.exists(LOCAL):
        print(f"downloading {URL} ...", flush=True)
        urllib.request.urlretrieve(URL, LOCAL)
    sha = sha256_file(LOCAL)
    print(f"sdssspec.dat.gz sha256={sha[:12]}…", flush=True)

    recs = []
    with gzip.open(LOCAL, "rt", encoding="latin-1") as f:
        for line in f:
            sid = sl(line, COLS["source_id"])
            if not sid or sid in ("-", "0"):
                continue
            pwd = sl(line, COLS["p_wd"])
            rec = {"source_id": str(int(sid)),  # canonical digit string
                   "spec_class": sl(line, COLS["spec_class"]),
                   "p_wd": fnum(pwd),
                   "g_mag": fnum(sl(line, COLS["g_mag"])),
                   "teff_h": fnum(sl(line, COLS["teff_h"]))}
            recs.append(rec)
    df = pd.DataFrame.from_records(recs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df.to_parquet(OUT, index=False)
    json.dump({"source_url": URL, "sha256_sdssspec_gz": sha, "n_rows": len(df),
               "n_classes": int(df["spec_class"].nunique())},
              open(PROV, "w"), indent=2)
    print(f"parsed {len(df):,} spectroscopic rows -> {OUT}")
    pol = df["spec_class"].fillna("").str.contains("Z")
    print(f"  metal-polluted (class contains 'Z'): {int(pol.sum()):,}")
    print("  top classes:", dict(df["spec_class"].value_counts().head(10)))


if __name__ == "__main__":
    main()
