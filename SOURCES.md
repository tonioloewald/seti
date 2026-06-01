# Data sources and reproducibility

This project **does not** store survey data in the repository. Instead it stores a
*deterministic recipe* for obtaining exactly the data used: pinned dataset releases,
the exact queries, a frozen list of target identifiers, and checksums. Bulk data is
fetched on demand into gitignored directories (`data/raw/`, `data/cache/`,
`data/derived/`) and verified against the committed checksums.

See [`preregistration.md`](preregistration.md) §3 (data sources & inclusion) and §6
(analysis plan, step 1: "freeze sample and manifest"). All data work post-dates the
OSF registration (tag `registered-1.0`); see [`REGISTRATION.md`](REGISTRATION.md).

## Determinism policy

- **Pin releases**, not "latest." Each dataset below names a fixed, static release.
- **Commit the recipe, not the data**: the exact query text, the frozen target
  identifier list, and a `SHA256SUMS` of every fetched artifact live in git
  (`data/manifests/`). The bulk products do not.
- **Canonicalise before hashing**: query results are sorted by a stable key (e.g.
  `source_id`) before checksumming, so server-side row-order nondeterminism does not
  break verification.
- **Record provenance at fetch time**: each fetcher writes the access date, the
  service endpoint, and the returned row count next to the data, and appends to the
  checksum manifest.
- **Pin the software environment** (`pipeline/env/`): astroquery/astropy query
  behaviour is version-dependent, so it is locked.

## Datasets

| # | Dataset | Pinned release | Access | Role |
|---|---------|----------------|--------|------|
| 1 | **Gaia EDR3 white-dwarf catalogue** (Gentile Fusillo et al. 2021, *MNRAS* 508, 3877) | VizieR `J/MNRAS/508/3877` (static) | CDS / VizieR file download | Parent object list → frozen sample manifest |
| 2 | **Gaia EDR3** astrometry + photometry | Gaia EDR3 (static) | Gaia archive TAP (`gea.esac.esa.int`), `gaiaedr3.gaia_source`, ADQL by `source_id` | Teff / parallax / optical SED anchor |
| 3 | **AllWISE Source Catalog** | AllWISE (static) | IRSA TAP (`irsa.ipac.caltech.edu/TAP`), `allwise_p3as_psd` | Static mid-IR SED (W1–W4) |
| 4 | **NEOWISE-R single-exposure** (W1/W2) | NEOWISE-R *Data Release year — to pin* | IRSA TAP, `neowiser_p1bs_psd`, positional | Multi-epoch IR variability (§5.3) |
| 5 | **2MASS** (PSC) | static | IRSA, `fp_psc` | Near-IR SED |
| 6 | **Spitzer** (SEIP / archival) | static | IRSA, where available | SED / cross-check |
| 7 | **TESS** light curves | SPOC/QLP — to pin per sector | MAST (astroquery / lightkurve), *IR-flagged subset only* | Channel B (secondary) |
| 8 | **JWST / MIRI** | — | MAST | Candidate follow-up only |

*Exact table names and query text are verified and frozen at first fetch, and recorded
here with the access date and returned row counts. Items marked "to pin" are fixed when
that fetcher is first run (a pre-data amendment if it post-dates registration).*

## What is committed vs fetched

- **Committed (git):** `data/manifests/` — frozen `source_id` list (compressed) + coords,
  query files, `SHA256SUMS`; `pipeline/` code; `pipeline/env/` lock; this file.
- **Fetched on demand (gitignored):** everything in `data/raw/`, `data/cache/`,
  `data/derived/` — catalogues, cross-matched photometry, light curves, SEDs, scores.

## Fetched-artifact log

| Date (UTC) | Source | Pinned ref | SHA-256 (source) | Product |
|---|---|---|---|---|
| 2026-06-01 | Parent catalogue `maincat.dat.gz` (568 MB) | VizieR `J/MNRAS/508/3877` | `f7c134e8…de12757b` | `data/manifests/wd_sample.csv.gz` — **359,073** rows at `P_WD > 0.75` (of 1,280,266). Fetcher: `pipeline/fetch/01_parent_catalogue.py`. Full provenance + checksums: `data/manifests/wd_sample.provenance.json`, `data/manifests/SHA256SUMS`. |
| 2026-06-01 | **AllWISE** via Gaia cross-match | `gaiaedr3.allwise_best_neighbour` → `gaiadr1.allwise_original_valid` (EDR3, static) | `732a8c97…cc3888934` | `data/raw/allwise/allwise_xmatch.parquet` (gitignored) — **16,924** matches (4.7%); detections W1 16,897 / W2 9,081 / W3 650 / W4 339. Fetcher: `pipeline/fetch/02_allwise_xmatch.py`; provenance: `data/manifests/allwise_xmatch.provenance.json`. |
| 2026-06-01 | **Optical baseline** (derived, no new fetch) | from pinned `maincat.dat.gz` | see provenance | `data/derived/optical_baseline.parquet` (gitignored) — **359,073** rows: Gaia G/BP/RP (+err) and pure-H Teff/logg (295,406 with Teff). Builder: `pipeline/build/01_optical_baseline.py`; provenance: `data/manifests/optical_baseline.provenance.json`. |
| 2026-06-01 | **WD atmosphere grids** (§5.3 H0) | Bédard et al. 2020, Bergeron/Montreal (`Table_DA`/`Table_DB`, static) | `ff3cfe68…`, `9353da84…` | `data/models/bergeron/` (**committed**, ~200 KB — small static reference). Fetcher: `pipeline/fetch/03_bergeron_grids.py`. Drives the IR-excess prediction in `pipeline/analysis/01_ir_excess.py`. |
| 2026-06-01 | **NEOWISE-R** multi-epoch W1/W2 | IRSA TAP `neowiser_p1bs_psd` (bulk spatial cross-match) | — | `data/raw/neowise/neowise_excess_epochs.parquet` (gitignored) — 80,379 clean epochs for 807 IR-excess WDs. Fetcher: `pipeline/fetch/04_neowise.py`; variability: `pipeline/analysis/06_variability.py`. |

