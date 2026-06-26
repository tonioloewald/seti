# Phase 2 — live status & resume anchor

A single place to recover the state of work if a session is lost. The authoritative record is
the git history + the OSF registration + the AI transcripts; this is the human-readable "where
we are and how to continue." Last updated 2026-06-22.

## Registered

- Plan: `preregistration_kdwarf.md`, OSF [osf.io/2akn3](https://osf.io/2akn3/), tag `phase2-registered-1.0`.
- Frozen manifest: 175,968 K dwarfs, `data/manifests/kdwarf_sample.csv.gz`, tag `phase2-manifest-1.0`.
- Pipeline (population-agnostic core + K-dwarf plugin): `pipeline/core/`, `pipeline/populations/k_dwarf.py`,
  stages `pipeline/fetch/k01`–`k08`. Deviations logged in `AMENDMENTS.md` (notably: youth floor **dropped**).

## Battery v2 (2026-06-09) — applied to both tiers

Two candidate-independent battery refinements (`AMENDMENTS.md`, commit history): a depth→radius
**eclipsing-binary criterion** (depth > 0.13 ⟹ R_occ > ~2.5 R_J ⟹ stellar companion) and a
**noise-aware depth-variability** test (per-epoch depth-CV judged against scatter/√n_in, so photon
noise no longer diverts real planets out of `natural_planet`). Injection-recovery confirms
box→RESIDUAL and tail→RESIDUAL preserved, so **C_i, the detection bars, and f_max are unchanged**;
only by-product labelling is refined. Both tiers re-run from k04 with this battery.

## T0 (G < 11) — DONE (battery v2)

- 12,100 stars; cascade 4,131 cand → 1,023 residual → 912 identity-survive → 463 on-target →
  61 recurring → triage (6 EB, 13 planet, 9 disint, 33 RESIDUAL). **0 resolvable-regime residuals**
  (all 33 RESIDUAL < 0.3% depth, max 0.186%) — clean null preserved. `f_max` ≈ 2.8×10⁻⁴ (box) /
  3.4×10⁻⁴ (tail), unchanged. Calibration frozen: `kdwarf_calibration_T0.json`, tag
  `phase2-calibration-T0`. Lists: `data/manifests/kdwarf_T0_residuals*.csv`, `kdwarf_T0_recurring_triage.csv`.

## T1 (11 ≤ G < 12) — PULLED (noise floor in combined run)

- 32,102 ok (97.6%) in `data/derived/kdwarf_noise_floor.parquet` (gitignored; LCs in `data/lightcurves/`).
  Re-pull if needed (idempotent): `.venv/bin/python pipeline/fetch/k02_lightcurves.py --gmin 11 --gmax 12 --workers 6`

## Combined T0+T1 — DONE (battery v2)

Stages parameterized by env `KRUN` (`T0` default | `T0T1` combined). Calibration frozen
(`kdwarf_calibration_T0T1.json`, tag `phase2-calibration-T0T1`; cohorts 595/1262/2051 ppm, bars
7.3/8.1/8.7 SDE, 44,202 stars). Cascade: 15,451 cand → 4,223 residual → 3,956 identity-survive →
1,607 on-target → 198 recurring → triage (25 EB, 45 planet, 30 disint, 98 RESIDUAL).
**7 resolvable-regime residuals** (depth > 0.3%): all U-shaped (**none a flat-bottomed occulter** →
f_max(box) holds on zero-flat-residual basis), all sub-stellar radius (< 1.31 R_J); 5 are
depth-variable beyond the noise floor, 2 asymmetric — genuine morphologically-anomalous **follow-up
candidates**, not detections. `f_max(box) ≈ 8.1×10⁻⁵ / tail ≈ 9.5×10⁻⁵` (~3.4× tighter than T0).
Lists: `data/manifests/kdwarf_T0T1_*`.

## Paper — REVIEW-COMPLETE (2026-06-12)

`paper/phase2_T0_draft.md` converged through battery v2 → v3 (red-noise-aware depth variability,
frozen) and three adversarial review rounds (automated Claude reviewer ×3 + Gemini ×2). Final state:
the resolvable residuals are **reported, not adjudicated** (Option A); the battery is **frozen** with
a declared stopping rule; the completeness grid spans 0.5–15% (measuring the 13% flat-occulter EB-cut
ceiling and the weak asymmetric-occulter / degenerate-tail bounds); f_max(box) 2.75e-4 (T0) / 8.3e-5
(combined), f_max(tail) 4.2e-4 / 1.2e-4. Audit `pipeline/runners/audit_T0_paper.py` = 53/53 PASS
(now checks each resolvable residual's depth per source_id). **Gemini verdict: "Ready for write-up and
submission — no remaining blockers."** Review briefs archived: `paper/phase2_review_brief.md` (Claude),
`paper/phase2_gemini_brief.md` (Gemini). **Next:** author write-up / submission; fixes to the declared
weaknesses (activity-robust morphology) deferred to the G 12–13 tiers, re-validated before unblinding.

## Publication production — DONE (2026-06-22, commit f085a17)

The publication-*production* gap is closed for the K-dwarf paper (`paper/phase2_T0_draft.md`). What
was done:

1. **Figures — DONE.** Five figures generated from frozen artifacts by
   `pipeline/runners/make_paper_figures.py` (production-only: reads committed calibrations/CSVs/noise
   floor, no new thresholds; cascade counts self-verify against the paper): `figures/kdwarf_`
   `{noise_cohorts, completeness, cascade, fmax_depth, residual_metrics}.png`, embedded with captions
   and in-order callouts (Figs 1–5).
2. **References — DONE.** 36-entry verified bibliography (DOIs traced to ADS/publisher), inline
   author-year citations, author block, Facilities/Software acknowledgment. Self-cites use the real
   OSF prereg titles/dates (6YH7R 2026-06-01; 2AKN3 2026-06-05).
3. **Scope — DECIDED: two separate papers.** K-dwarf is standalone and **cites** the Phase 1 WD null
   (Loewald 2026a); no combined methods paper. (WD paper `paper/draft.md` still its own production task.)
4. **Review — DONE.** Independent adversarial pass on the additions; one blocker (Fig 2 dust-tail
   grouping) + polish items fixed. `audit_T0_paper.py` still 53/53 PASS.

**Still open before actual submission:** (a) author **affiliation + ORCID** (placeholder in the md);
(b) **venue + format** — still house Markdown→PDF, not AASTeX/LaTeX; RNAAS vs AJ/MNRAS vs arXiv
undecided; (c) optional **phase-folded light curves** of the 3 resolvable residuals + the 2 validation
systems (needs a MAST fetch); (d) **nothing submitted** yet (no arXiv/journal/cover letter); (e) the
**push to public `origin/main`** — 3 commits now unpushed (this + 2 from 06-14), awaiting the go-ahead.

## G12-13 (T0T1T2) — pre-unblind work DONE (2026-06-22, commit a228639)

The deferred activity-robust-morphology fix is implemented, validated, and the production
calibration is frozen — everything up to (but not including) the blind-lift:

- **Battery v4 = local per-transit detrending** (`core.transit.local_detrend`): morphology measured
  on a detrended fold so irregular activity no longer distorts the folded shape on active hosts; the
  activity gate / EB tests / red-noise depth-variability stay on raw flux. Threaded through `k04/k03/k08`.
- **Validated candidate-blind:** `k04 --test` regression preserved; objective active-host injection test
  (`validate_activity_robust.py`) → active-host planet recovery **+0.19**, quiet no-op, box **−0.07** on
  active hosts. Fixed-sample v3→v4 isolation on tiers [0,1] → box completeness **neutral** (f_max(box)
  ratio 1.01×), so the flat-occulter limit is preserved. Human-directed decision: **freeze with the
  detrend alone** (safeguard B held).
- **Frozen** `data/manifests/kdwarf_calibration_T0T1T2.json`, tag **`phase2-calibration-T0T1T2`**:
  61,178 stars, cohorts 629/1241/2248 ppm, bars 7.1/8.3/9.0; f_max(box) **6.6×10⁻⁵**, tail **9.0×10⁻⁵**
  (tighter than T0+T1 from the larger sample). Logged in AMENDMENTS.md (pre-data/confirmatory) + IMPL_LOG.
- Published T0 / T0+T1 results retain battery v3 (separate immutable artifacts); v4 is for the new tier.

## G12-13 (T0T1T2) — UNBLIND AUTHORIZED & IN PROGRESS (human said "Unblind!" 2026-06-26)

The human directed the unblind. The blind is lifted; a fresh session may run the steps below freely.
A machine reboot interrupted the run mid-search — **no harm**: `k04 --unblind` writes its output only at
the very end, so an interrupted run leaves no partial file and is simply re-run from scratch
(deterministic against the frozen, tagged calibration). **Resume from step 1.**

Run from repo root, in order (each stage is `KRUN`-parameterized and writes `data/manifests/kdwarf_T0T1T2_*`):

```bash
# 1. the search (lifts the blind) — ~12 min, NOT resumable (re-run whole; deterministic). Writes
#    kdwarf_T0T1T2_residuals.csv + prints battery verdicts and the real per-family f_max.
KRUN=T0T1T2 .venv/bin/python pipeline/fetch/k04_search.py --unblind --workers 14
# 2-5. the cascade — network-heavy (MAST/SIMBAD/TESScut fetches), each resumable:
KRUN=T0T1T2 .venv/bin/python pipeline/fetch/k05_identity.py
KRUN=T0T1T2 .venv/bin/python pipeline/fetch/k06_centroid.py --workers 8
KRUN=T0T1T2 .venv/bin/python pipeline/fetch/k07_multisector.py --workers 8
KRUN=T0T1T2 .venv/bin/python pipeline/fetch/k08_triage.py --workers 8
```

Expectations / scale: ~4,000+ residuals → identity survivors → centroid (slow, a TESScut fetch per
candidate) → recurrence → triage. The cascade (k06-k08) may take a few hours. The T0T1T2 result then
feeds a paper update. Note: this run re-searches the brighter tiers with v4 too, so it re-evaluates
their residuals (incl. the active-host `1397924585409290240`) under the new activity-robust morphology —
that is expected and part of the unblind. Frozen calibration: tag `phase2-calibration-T0T1T2`;
f_max(box) 6.6×10⁻⁵ if the residuals clear. Status task #8 tracks this.

## What is and isn't durable

- **Durable:** everything committed to `origin/main` (code, results, paper, residual lists, frozen
  calibrations, transcripts), the OSF registration, and the `~/.claude` memory files. The T1 pull is
  resumable from its checkpoint via the command above.
- **Not durable:** the live conversation context and the harness's handle on the background task. If a
  session is lost, a fresh one recovers state from this file + `MEMORY.md` + the git history, and
  resumes the pull with the command above.
