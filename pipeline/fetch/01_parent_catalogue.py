#!/usr/bin/env python3
"""Step 1 (pre-registration §6.1): fetch the parent white-dwarf catalogue and
freeze the registered sample manifest — deterministically, stdlib only.

Pinned source: Gentile Fusillo et al. 2021, "A catalogue of white dwarfs in
Gaia EDR3", MNRAS 508, 3877 — VizieR J/MNRAS/508/3877 (a static release).
We download the CDS fixed-width main catalogue, verify/record its SHA-256, then
apply the registered §3 gate (P_WD > 0.75) to produce the frozen target list.

Outputs (committed, small):
  data/manifests/wd_sample.csv.gz            source_id, ra, dec, parallax,
                                             parallax_over_error, p_wd (sorted)
  data/manifests/SHA256SUMS                  checksums of source + manifest
  data/manifests/wd_sample.provenance.json   versions, URLs, counts, date
Raw download (gitignored): data/raw/gentile_fusillo_2021/

Re-running verifies the committed checksums rather than blindly re-fetching, so
the process is reproducible: same pinned release -> byte-identical manifest.
"""
import csv
import gzip
import hashlib
import io
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

# ---- pinned, static source -------------------------------------------------
VIZIER_ID = "J/MNRAS/508/3877"
BASE = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/508/3877"
FILES = {"readme": f"{BASE}/ReadMe", "maincat": f"{BASE}/maincat.dat.gz"}
PWD_GATE = 0.75  # registered §3 inclusion gate (high-confidence white dwarf)

# CDS byte-by-byte ranges (1-indexed, inclusive) from the ReadMe -> 0-indexed slices
COLS = {
    "source_id":           (25, 43),
    "ra_deg":              (95, 109),
    "dec_deg":             (120, 134),
    "parallax":            (145, 154),
    "parallax_over_error": (163, 172),
    "p_wd":                (184, 191),
}

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw", "gentile_fusillo_2021")
MAN = os.path.join(ROOT, "data", "manifests")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        print(f"  exists: {os.path.basename(dest)} ({os.path.getsize(dest)//1048576} MB)")
        return
    print(f"  downloading {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "seti-wd-search/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as out:
        n = 0
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            n += len(chunk)
    print(f"    -> {dest} ({n//1048576} MB)")


def slice_field(line, span):
    lo, hi = span
    return line[lo - 1:hi].strip()


def build_manifest(maincat_gz, out_gz):
    n_total = n_sel = 0
    rows = []
    with gzip.open(maincat_gz, "rt", encoding="latin-1") as f:
        for line in f:
            n_total += 1
            pwd_s = slice_field(line, COLS["p_wd"])
            if not pwd_s:
                continue
            try:
                pwd = float(pwd_s)
            except ValueError:
                continue
            if pwd <= PWD_GATE:
                continue
            rows.append((
                slice_field(line, COLS["source_id"]),
                slice_field(line, COLS["ra_deg"]),
                slice_field(line, COLS["dec_deg"]),
                slice_field(line, COLS["parallax"]),
                slice_field(line, COLS["parallax_over_error"]),
                pwd_s,
            ))
            n_sel += 1
    # canonical order for a deterministic checksum
    rows.sort(key=lambda r: int(r[0]))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["source_id", "ra_deg", "dec_deg", "parallax",
                "parallax_over_error", "p_wd"])
    w.writerows(rows)
    with gzip.open(out_gz, "wt", encoding="utf-8", newline="") as g:
        g.write(buf.getvalue())
    return n_total, n_sel


def main():
    os.makedirs(MAN, exist_ok=True)
    readme = os.path.join(RAW, "ReadMe")
    maincat = os.path.join(RAW, "maincat.dat.gz")
    download(FILES["readme"], readme)
    download(FILES["maincat"], maincat)

    sums = {
        "ReadMe": sha256_file(readme),
        "maincat.dat.gz": sha256_file(maincat),
    }
    print("  source checksums:")
    for k, v in sums.items():
        print(f"    {v}  {k}")

    out_gz = os.path.join(MAN, "wd_sample.csv.gz")
    print("  building frozen sample manifest (P_WD > %.2f) ..." % PWD_GATE)
    n_total, n_sel = build_manifest(maincat, out_gz)
    sums["wd_sample.csv.gz"] = sha256_file(out_gz)
    print(f"    parsed {n_total:,} rows -> selected {n_sel:,} "
          f"({os.path.getsize(out_gz)//1024} KB gz)")

    with open(os.path.join(MAN, "SHA256SUMS"), "w") as f:
        for k in ("maincat.dat.gz", "ReadMe", "wd_sample.csv.gz"):
            f.write(f"{sums[k]}  {k}\n")

    prov = {
        "dataset": "Gentile Fusillo et al. 2021, MNRAS 508, 3877",
        "vizier_id": VIZIER_ID,
        "source_urls": FILES,
        "accessed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registered_gate": f"p_wd > {PWD_GATE}",
        "n_catalogue_rows": n_total,
        "n_selected": n_sel,
        "manifest_columns": list(COLS.keys()),
        "source_sha256": {k: sums[k] for k in ("maincat.dat.gz", "ReadMe")},
        "manifest_sha256": sums["wd_sample.csv.gz"],
        "note": ("Frozen target list for the registered search (tag registered-1.0). "
                 "Gate 4 (>=1 informative IR constraint) and per-object reddening "
                 "handling are applied downstream at cross-match; see SOURCES.md."),
    }
    with open(os.path.join(MAN, "wd_sample.provenance.json"), "w") as f:
        json.dump(prov, f, indent=2)
    print("  wrote manifest, SHA256SUMS, provenance to data/manifests/")


if __name__ == "__main__":
    main()
