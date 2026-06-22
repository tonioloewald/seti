# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **pre-registered, open technosignature search**: a mechanism-agnostic hunt for anomalous
departures from the natural behavior of cooling stellar remnants (Phase 1: white dwarfs) and
K dwarfs (Phase 2), across infrared-excess (Channel A), transit-morphology (Channel B), and
accretion-state (Channel C) channels. The deliverable is either a clean, *explained* null
with a quantitative prevalence upper limit (`f_max`) or a published catalogue of unexplained
residuals — never a claim of intelligence. Read `README.md`, then `preregistration.md`
(Phase 1) / `preregistration_kdwarf.md` (Phase 2). `docs/glossary.md` defines every domain
term used in the code and papers.

This is a single-author research repo: most "work" is analysis, writing, and adversarial
review, not feature development. The git history *is* the scientific record.

## Integrity invariant — read before changing analysis code

The whole project's value rests on one rule: **procedures and thresholds are specified
independently of the findings, and are never tuned to include or exclude particular objects.**
Concretely:

- Detection thresholds come from the registered empirical-null calibration + injection-recovery,
  **never** from inspecting a candidate/excess list. Do not adjust a cut to change which objects
  survive.
- The search is **blinded**. Phase-2 stage `k04_search.py` defaults to `--test` (injection-recovery
  validation, reveals no real candidate). `--unblind` runs the real search and **lifts the blind** —
  only run it against a frozen, tagged production calibration, and only when the human directs it.
- Frozen artifacts (manifests, calibration JSONs) are pinned to git tags (e.g. `phase2-calibration-T0T1`).
  Treat them as immutable; a change is a new tagged freeze, logged.
- Every elaboration of the registered method is logged in **`AMENDMENTS.md`** (top-level, scientific
  framing: pre-data = confirmatory / post-data = exploratory) and **`pipeline/IMPLEMENTATION_LOG.md`**
  (concrete decision + rationale + which registered § it implements). New data sources go in **`SOURCES.md`**
  with pinned release + checksum. Keeping these current is part of the task, not optional cleanup.
- `source_id` (19-digit Gaia ID) is carried as a **string** everywhere — float64 silently truncates it
  and merges distinct stars (see IMPLEMENTATION_LOG; glossary "IEEE-754"). For IRSA/TAP uploads only,
  use int64. Never let a Gaia id touch a float.

When in doubt about whether a change is methodologically legitimate, surface it to the human rather
than proceeding — the cost of an integrity slip here is the entire project.

## Environment & commands

Analysis runs in a pinned venv (`.venv/`, gitignored). One-time setup and the reproducibility
recipe are in `pipeline/env/README.md`. The `pipeline/fetch/` acquisition layer needs only stdlib +
`requests`; everything else (SED fitting, BLS, plotting) needs the venv.

```bash
# run any pipeline stage (always via the venv python, from repo root):
.venv/bin/python pipeline/analysis/01_ir_excess.py          # Phase 1, numbered stages
.venv/bin/python pipeline/fetch/k02_lightcurves.py --gmin 11 --gmax 12 --workers 6   # Phase 2 stages

# recreate the exact environment:
.venv/bin/pip install -r pipeline/env/requirements.lock

# render a markdown doc to review-ready PDF + HTML:
.venv/bin/python tools/build_pdf.py paper/phase2_T0_draft.md   # -> .pdf + .html beside it
```

There is no test suite, linter, or build system. "Validation" means the `pipeline/runners/`
scripts: `audit_T0_paper.py` (asserts every numeric claim in the paper against the data, 53/53 PASS),
`validate_wd.py` / `positive_control.py` / `pilot_*` (end-to-end sanity on known systems, e.g.
recovering WD 1856+534 b). Run the relevant runner after changing analysis code.

A `Stop` hook auto-exports the session transcript to its own per-session file
`docs/transcripts/claude-session-<id>.md` (via `tools/export_transcript.py`) — expect a
new/modified file for the current session. Per-session naming is deliberate: a single shared
output file used to let each new session's export silently overwrite the prior archive.

## Architecture

**Population-agnostic core + per-population plugins.** All statistics and SED/transit machinery
live in `pipeline/core/` (`sed`, `noise`, `stats`, `detect`, `transit`, `excess`, `fmax`, `grids`)
and are identical for every star class. A `pipeline/populations/` plugin (`white_dwarf.py`,
`k_dwarf.py`, subclassing `base.Population`) supplies only the three star-specific things: the bare-star
predicted photometry (natural baseline), the bolometric flux (for `f_max`), and which excess
temperatures count as natural (disk/companion) vs. a residual. To add a population, implement that
interface — e.g. swapping a Bergeron grid for a BT-Settl/PHOENIX grid via `core.grids.load_grid`.

**Phase 1 (white dwarfs) — complete, three clean nulls.** `pipeline/fetch/01–06` (data acquisition),
`pipeline/build/01_optical_baseline.py` (the intermediate "Step 2a": parses the pinned Gentile Fusillo
catalogue into `data/derived/optical_baseline.parquet`, the H0 SED anchor that the analysis stages consume),
and `pipeline/analysis/01–16` (numbered, run in order): excess → empirical null → battery → vetting →
upper limit → variability → transit/centroid → clean-zone, plus v2 (CatWISE) and robustness checks.
Results in `RESULTS.md` and the IMPLEMENTATION_LOG.

**Phase 2 (K dwarfs) — paper review-complete.** Staged scripts `pipeline/fetch/k01–k08`
(manifest → light curves + noise floor → calibrate → search+battery → identity → centroid →
multisector → triage), parameterized by the **`KRUN` env var** (`T0` = G<11 default, `T0T1` = combined).
Brightest-first tiers (T0/T1/T2) are an analysis *order* within one frozen manifest, not separate samples.
Live state and resume instructions: `docs/phase2_status.md`.

**Data is a recipe, not a payload.** Nothing bulk is committed. `data/manifests/` holds frozen
`source_id` lists, query text, provenance JSON, and `SHA256SUMS`; `data/raw|cache|derived|lightcurves/`
are gitignored and fetched on demand, verified against committed checksums (canonicalised sort →
hash). `SOURCES.md` is the determinism policy + fetched-artifact log.

**Papers & review.** `paper/` holds the working drafts (`.md` → rendered `.pdf`/`.html`) and the
adversarial-review briefs (Claude + Gemini rounds). Per memory, share the `.md` for review rounds;
only build a PDF when a render is explicitly wanted.
