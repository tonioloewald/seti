#!/usr/bin/env python3
"""Phase 2, step 1 (prereg §6.1): freeze the registered K-dwarf sample manifest.

Pinned source: Gaia DR3 `gaiadr3.gaia_source` (a static release) via the ESA Gaia TAP
service. The registered §3 selection is applied in two parts:

  CORE (in the ADQL query, the registered cuts):
    Teff_gspphot 3900-5300 K, logg_gspphot > 4.3 (dwarf), RUWE < 1.4,
    parallax_over_error > 10, and the hard limit G < 13.

  MAIN-SEQUENCE BOX (post-query, the "absolute-G vs BP-RP main-sequence box" of §3,
    whose exact parameters are a pre-data implementation decision -- logged in
    AMENDMENTS.md): M_G within +/-1.5 mag of an empirical K-dwarf main-sequence ridge,
    over BP-RP in [0.78, 1.84]. Generous by design (accommodates the metallicity spread)
    -- a sanity cut on top of the logg dwarf selection, not a tight isochrone.

Gaia DR3 is static, so the fixed query reproduces byte-identically; the manifest SHA-256
is the freeze anchor (git tag phase2-manifest-1.0). source_id is carried as a STRING
(19-digit Gaia IDs exceed float64's exact-integer range).

Outputs (committed, small):
  data/manifests/kdwarf_sample.csv.gz          source_id + selection/CMD columns (sorted)
  data/manifests/kdwarf_sample.provenance.json query text, DR3, counts, date, SHA-256
  data/manifests/SHA256SUMS_kdwarf             checksum of the manifest
Re-running with the same DR3 + query yields an identical manifest.
"""
import gzip, hashlib, json, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAN = os.path.join(ROOT, "data", "manifests")
GMAX = 13.0                                    # hard magnitude limit (pre-data decision)

ADQL = f"""
SELECT source_id, ra, dec, parallax, parallax_over_error, ruwe,
       phot_g_mean_mag, bp_rp, teff_gspphot, logg_gspphot
FROM gaiadr3.gaia_source
WHERE teff_gspphot BETWEEN 3900 AND 5300
  AND logg_gspphot > 4.3
  AND ruwe < 1.4
  AND parallax_over_error > 10
  AND phot_g_mean_mag < {GMAX}
"""

# main-sequence box (pre-data implementation decision; see AMENDMENTS.md)
BPRP_LO, BPRP_HI = 0.78, 1.84
RIDGE_M0, RIDGE_BP0, RIDGE_SLOPE = 5.5, 0.85, 2.83   # M_G ridge = M0 + slope*(BP_RP - BP0)
BOX_HALFWIDTH = 1.5


def ms_box(df):
    ridge = RIDGE_M0 + RIDGE_SLOPE * (df["bp_rp"] - RIDGE_BP0)
    return ((df["bp_rp"] >= BPRP_LO) & (df["bp_rp"] <= BPRP_HI)
            & ((df["m_g"] - ridge).abs() < BOX_HALFWIDTH))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    from astroquery.gaia import Gaia
    os.makedirs(MAN, exist_ok=True)
    print("querying Gaia DR3 (core registered cuts, G < %.1f) ..." % GMAX, flush=True)
    job = Gaia.launch_job_async(ADQL)
    t = job.get_results()
    df = t.to_pandas()
    n_core = len(df)
    print(f"  core sample: {n_core:,}", flush=True)

    df["source_id"] = df["source_id"].astype("int64").astype(str)   # exact, as string
    df = df.rename(columns={"ra": "ra_deg", "dec": "dec_deg",
                            "phot_g_mean_mag": "g_mag"})
    df["m_g"] = df["g_mag"] + 5.0 * np.log10(df["parallax"] / 1000.0) + 5.0  # parallax in mas

    keep = ms_box(df)
    n_box = int(keep.sum())
    print(f"  after main-sequence box: {n_box:,}  (removed {n_core - n_box:,})", flush=True)
    df = df[keep].copy()

    cols = ["source_id", "ra_deg", "dec_deg", "parallax", "parallax_over_error",
            "ruwe", "g_mag", "bp_rp", "teff_gspphot", "logg_gspphot", "m_g"]
    df = df[cols].sort_values("source_id", key=lambda s: s.astype(np.int64)).reset_index(drop=True)

    out_gz = os.path.join(MAN, "kdwarf_sample.csv.gz")
    with gzip.open(out_gz, "wt", encoding="utf-8", newline="") as g:
        df.to_csv(g, index=False)
    man_sha = sha256_file(out_gz)
    print(f"  wrote {out_gz} ({os.path.getsize(out_gz)//1024} KB, {len(df):,} rows)", flush=True)

    with open(os.path.join(MAN, "SHA256SUMS_kdwarf"), "w") as f:
        f.write(f"{man_sha}  kdwarf_sample.csv.gz\n")
    prov = {
        "dataset": "Gaia DR3 gaiadr3.gaia_source (static release)",
        "service": "ESA Gaia TAP (astroquery.gaia)",
        "adql": ADQL.strip(),
        "accessed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registered_core_cuts": ("Teff 3900-5300 K; logg>4.3; RUWE<1.4; "
                                 "parallax_over_error>10; G<%.1f" % GMAX),
        "ms_box": {"bp_rp": [BPRP_LO, BPRP_HI],
                   "ridge_M_G": f"{RIDGE_M0}+{RIDGE_SLOPE}*(bp_rp-{RIDGE_BP0})",
                   "halfwidth_mag": BOX_HALFWIDTH,
                   "note": "pre-data implementation decision; see AMENDMENTS.md Phase 2"},
        "n_core": n_core,
        "n_selected": n_box,
        "manifest_columns": cols,
        "manifest_sha256": man_sha,
        "note": ("Frozen K-dwarf target list for the registered Phase-2 search "
                 "(OSF osf.io/2akn3). No light curve is pulled before this is committed."),
    }
    with open(os.path.join(MAN, "kdwarf_sample.provenance.json"), "w") as f:
        json.dump(prov, f, indent=2)
    print("  wrote SHA256SUMS_kdwarf + provenance", flush=True)
    # sanity summary
    print(f"  Teff range {df.teff_gspphot.min():.0f}-{df.teff_gspphot.max():.0f} K; "
          f"G {df.g_mag.min():.1f}-{df.g_mag.max():.1f}; M_G {df.m_g.min():.1f}-{df.m_g.max():.1f}")


if __name__ == "__main__":
    main()
