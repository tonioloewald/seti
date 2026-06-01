#!/usr/bin/env python3
"""Step 2a: build the optical photosphere baseline (the H0 anchor for SED fits).

Re-parses the already-downloaded, pinned Gentile Fusillo catalogue
(data/raw/gentile_fusillo_2021/maincat.dat.gz; SHA-256 recorded in
data/manifests/SHA256SUMS) and extracts, for the registered sample (P_WD > 0.75),
the Gaia EDR3 photometry (G/BP/RP + errors) and the authors' pure-H atmosphere fit
(Teff, logg). Output is a derived product, regenerable from the pinned source, so
it is gitignored:

  data/derived/optical_baseline.parquet     (source_id-keyed)

Provenance (committed): data/manifests/optical_baseline.provenance.json
"""
import gzip, hashlib, json, os
from datetime import datetime, timezone
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAINCAT = os.path.join(ROOT, "data", "raw", "gentile_fusillo_2021", "maincat.dat.gz")
OUT = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
MAN = os.path.join(ROOT, "data", "manifests")
PWD_GATE = 0.75

# CDS byte ranges (1-indexed inclusive) from the maincat ReadMe
COLS = {
    "source_id":  (25, 43),
    "p_wd":       (184, 191),
    "g_mag":      (698, 704), "g_mag_err":  (706, 711),
    "bp_mag":     (783, 789), "bp_mag_err": (791, 798),
    "rp_mag":     (838, 844), "rp_mag_err": (846, 853),
    "teff_h":     (1028, 1036), "teff_h_err": (1038, 1045),
    "logg_h":     (1047, 1054), "logg_h_err": (1056, 1063),
}
FLOAT_COLS = [c for c in COLS if c not in ("source_id",)]


def sl(line, span):
    return line[span[0] - 1:span[1]].strip()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    recs = []
    n_total = 0
    with gzip.open(MAINCAT, "rt", encoding="latin-1") as f:
        for line in f:
            n_total += 1
            pwd = sl(line, COLS["p_wd"])
            try:
                if not pwd or float(pwd) <= PWD_GATE:
                    continue
            except ValueError:
                continue
            # source_id as a canonical digit STRING: 19-digit Gaia IDs overflow
            # float64's exact-integer range, so any numeric coercion downstream would
            # silently corrupt them. str(int(...)) normalises whitespace/leading zeros.
            rec = {"source_id": str(int(sl(line, COLS["source_id"])))}
            for c in FLOAT_COLS:
                v = sl(line, COLS[c])
                try:
                    rec[c] = float(v) if v else None
                except ValueError:
                    rec[c] = None
            recs.append(rec)
    df = pd.DataFrame.from_records(recs).sort_values(
        "source_id", key=lambda s: s.astype("int64")).reset_index(drop=True)
    df.to_parquet(OUT, index=False)

    h = hashlib.sha256()
    with open(OUT, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    n_teff = int(df["teff_h"].notna().sum())
    prov = {
        "step": "2a optical baseline (photosphere anchor)",
        "derived_from": "Gentile Fusillo 2021 maincat.dat.gz (pinned; see SHA256SUMS)",
        "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_catalogue_rows": n_total,
        "n_selected": len(df),
        "n_with_teff_h": n_teff,
        "columns": list(COLS.keys()),
        "product": "data/derived/optical_baseline.parquet (gitignored; regenerable)",
        "parquet_sha256": h.hexdigest(),
    }
    json.dump(prov, open(os.path.join(MAN, "optical_baseline.provenance.json"), "w"), indent=2)
    print(f"selected {len(df):,} of {n_total:,}; {n_teff:,} with pure-H Teff")
    print(f"  -> {OUT}  ({os.path.getsize(OUT)//1024} KB, gitignored)")
    print("  G/BP/RP non-null:",
          *[f"{c}={int(df[c].notna().sum()):,}" for c in ("g_mag", "bp_mag", "rp_mag")])


if __name__ == "__main__":
    main()
