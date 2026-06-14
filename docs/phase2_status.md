# Phase 2 — live status & resume anchor

A single place to recover the state of work if a session is lost. The authoritative record is
the git history + the OSF registration + the AI transcripts; this is the human-readable "where
we are and how to continue." Last updated 2026-06-09.

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

## Publication gap & plan (assessed 2026-06-14)

"Review-complete draft" ≠ submittable manuscript. The *argument* is written and externally
stress-tested; the *manuscript a referee could read* is not. Concrete gaps, both papers
(`paper/phase2_T0_draft.md` K-dwarf, `paper/draft.md` white-dwarf) being internal Markdown→PDF only:

1. **Figures: none.** The K-dwarf paper references zero figures (no `![`, no `.png`, no "Figure 1");
   `figures/` holds almost only Phase-1 plots. Every result (cascade, f_max-vs-depth, completeness/
   recovery grid incl. the 13% EB-cut ceiling, resolvable-residual light curves, injection-recovery
   calibration) is prose-only. **Biggest gap — the planned first task.**
2. **References are a 9-item placeholder sketch.** Missing the Gentile Fusillo catalogue, our own OSF
   prereg DOI, software (astropy/lightkurve/BLS), and methods refs (Gross–Vitells, Stetson, …).
3. **No target venue / journal format.** House Markdown, not AASTeX/LaTeX (ApJ/AJ/MNRAS) or an
   arXiv-ready package; no formatted author/affiliation block. Venue undecided (RNAAS vs AJ/MNRAS vs arXiv).
4. **One-paper-vs-two unresolved.** Combined WD+K-dwarf methods paper, or separate? Shapes everything.
5. **Nothing submitted anywhere** — no arXiv, no journal, no co-author sign-off, no cover letter.

**Plan (next session, 2026-06-15):** close the gap starting with **figures** (generated from data
already in hand), then references → venue/format decision → submit. After that, **process the next
dataset** (the G 12–13 tiers, with the deferred activity-robust-morphology fix done up front and
re-validated on injections *before* unblinding, per the stopping rule).

## What is and isn't durable

- **Durable:** everything committed to `origin/main` (code, results, paper, residual lists, frozen
  calibrations, transcripts), the OSF registration, and the `~/.claude` memory files. The T1 pull is
  resumable from its checkpoint via the command above.
- **Not durable:** the live conversation context and the harness's handle on the background task. If a
  session is lost, a fresh one recovers state from this file + `MEMORY.md` + the git history, and
  resumes the pull with the command above.
