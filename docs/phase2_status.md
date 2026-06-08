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

## T1 (11 ≤ G < 12) — PULLED, awaiting calibration

- **Pull + transient retry DONE:** 32,891 processed, **32,102 ok (97.6%)** in the noise floor
  (`data/derived/kdwarf_noise_floor.parquet`, gitignored; LCs cached in `data/lightcurves/`).
  Remaining fails: 692 genuine no-data + ~75 persistent malformed products (not worth re-trying).
  - Re-pull if ever needed (idempotent; skips done): `.venv/bin/python pipeline/fetch/k02_lightcurves.py --gmin 11 --gmax 12 --workers 6`

## Combined T0+T1 run — IN PROGRESS (decision: combined; T0 kept immutable)

Stages parameterized by env `KRUN` (default `T0` = published run; `T0T1` = combined). Done so far:
combined calibration frozen (`kdwarf_calibration_T0T1.json`, tag `phase2-calibration-T0T1`; cohorts
595/1262/2051 ppm, bars 7.3/8.1/8.7 SDE, 44,380 stars); unblind 5,796 residuals, projected
**f_max(box) ≈ 8.1e-5 / tail ≈ 9.5e-5** (~3.4× tighter than T0); identity → 5,435 survive.

**Resume the cascade** (each resumable; in order, env `KRUN=T0T1 --workers 6`):
`k06_centroid.py` (running) → `k07_multisector.py` → `k08_triage.py`. Combined lists:
`data/manifests/kdwarf_T0T1_residuals*.csv`. T0 artifacts (`kdwarf_calibration_T0.json`,
`kdwarf_T0_residuals*.csv`, the paper) are untouched.

**After the cascade:** extend the cumulative `f_max`, update the paper with the combined tier,
re-run `pipeline/runners/audit_T0_paper.py` (and add a T0T1 audit).

## What is and isn't durable

- **Durable:** everything committed to `origin/main` (code, results, paper, residual lists, frozen
  calibrations, transcripts), the OSF registration, and the `~/.claude` memory files. The T1 pull is
  resumable from its checkpoint via the command above.
- **Not durable:** the live conversation context and the harness's handle on the background task. If a
  session is lost, a fresh one recovers state from this file + `MEMORY.md` + the git history, and
  resumes the pull with the command above.
