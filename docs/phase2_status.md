# Phase 2 — live status & resume anchor

A single place to recover the state of work if a session is lost. The authoritative record is
the git history + the OSF registration + the AI transcripts; this is the human-readable "where
we are and how to continue." Last updated 2026-06-07.

## Registered

- Plan: `preregistration_kdwarf.md`, OSF [osf.io/2akn3](https://osf.io/2akn3/), tag `phase2-registered-1.0`.
- Frozen manifest: 175,968 K dwarfs, `data/manifests/kdwarf_sample.csv.gz`, tag `phase2-manifest-1.0`.
- Pipeline (population-agnostic core + K-dwarf plugin): `pipeline/core/`, `pipeline/populations/k_dwarf.py`,
  stages `pipeline/fetch/k01`–`k08`. Deviations logged in `AMENDMENTS.md` (notably: youth floor **dropped**).

## T0 (G < 11) — DONE

- 12,100 stars searched; cascade → no resolved anomaly; `f_max` ≈ 2.8×10⁻⁴ (flat occulter) / 3.4×10⁻⁴ (tail);
  by-product 6 EB + 10 planet; 273 follow-up. Calibration frozen: tag `phase2-calibration-T0`,
  `data/manifests/kdwarf_calibration_T0.json`. Residual lists: `data/manifests/kdwarf_T0_residuals*.csv`.
- **Paper:** `paper/phase2_T0_draft.md` — converged after ~5 adversarial review rounds. Every number
  verified against the committed artifacts by `pipeline/runners/audit_T0_paper.py` (all PASS).

## T1 (11 ≤ G < 12) — IN PROGRESS

- **Pull running** (background): 32,891 stars. ~0.5/s, ~97% success, 90s/star timeout.
  - **Resume the pull** (idempotent; skips done): `.venv/bin/python pipeline/fetch/k02_lightcurves.py --gmin 11 --gmax 12 --workers 6`
  - Writes to `data/derived/kdwarf_noise_floor.parquet` (gitignored, checkpointed every 25) and
    `data/lightcurves/<source_id>.npz` (gitignored cache).

## Next steps (in order), once the T1 pull completes

1. **Retry transients:** `k02_lightcurves.py --gmin 11 --gmax 12 --retry` (recovers timeout/Connection/etc.;
   leaves `err:RuntimeError` = genuine no-data). Optionally run over T0 too for consistency.
2. **Calibrate.** Open decision: recalibrate on the *combined* T0+T1 noise floor (one consistent
   calibration, refines the bars with more data — data-driven, candidate-independent) **vs** per-tier
   calibration (T0 frozen as-is, T1 its own). Run `k03_calibrate.py` accordingly; freeze + tag.
3. **Search + battery:** `k04_search.py --unblind` (against the frozen T1/combined calibration) → then
   `k05_identity` → `k06_centroid` → `k07_multisector` → `k08_triage`, same as T0.
4. **Report:** extend the cumulative `f_max` (Σ C_i grows), update the paper, re-run the audit.

## What is and isn't durable

- **Durable:** everything committed to `origin/main` (code, results, paper, residual lists, frozen
  calibrations, transcripts), the OSF registration, and the `~/.claude` memory files. The T1 pull is
  resumable from its checkpoint via the command above.
- **Not durable:** the live conversation context and the harness's handle on the background task. If a
  session is lost, a fresh one recovers state from this file + `MEMORY.md` + the git history, and
  resumes the pull with the command above.
