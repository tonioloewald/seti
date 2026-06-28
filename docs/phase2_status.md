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

## G12-13 (T0T1T2) — UNBLIND DONE for search; cascade in progress (2026-06-26)

The human directed the unblind. The blind is lifted.

**Step 1 (k04 --unblind) — DONE 2026-06-26 (re-run clean after the reboot).** 61,178 stars searched
against frozen bars 7.1/8.3/9.0 SDE → 22,606 candidates. Battery verdicts: 9,394 natural_planet,
7,421 eclipsing_binary, **4,501 RESIDUAL**, 1,077 activity/variability, 198 disintegrating_body,
15 unfoldable. Per-family f_max matched the frozen prediction **exactly**: box **6.60e-05** (sum C_i
45,476), tail **8.99e-05** (33,376), planet 9.19e-04, triangle 9.01e-04. Residuals →
`data/manifests/kdwarf_T0T1T2_residuals.csv` (NOT detections — each needs the centroid gate +
identity/known-planet cross-check). Top residuals by SDE incl. 437785333585272192 (SDE 21.6, P=0.50d,
d=0.15%) and 2628360590325729920 (SDE 19.1, d=2.49%, the deepest).

**Steps 2-5 (cascade k05→k08) — DONE 2026-06-28.** Cascade: 4,501 raw residuals → k05 identity
4,195 survive (134 known_binary, 62 known_planet, 58 known_variable, 46 TOI, 6 EB removed) → k06
centroid **1,598 on-target** (2,370 background_blend rejected; transient fetch errors retried down to
1 unfetchable TPF) → k07 multisector **194 recurring** (757 single-sector artifacts rejected, 230
single-sector-only inconclusive, 417 no_data; recurs count stable under `--retry`) → k08 triage:
**108 natural_planet, 64 RESIDUAL, 17 eclipsing_binary, 5 disintegrating_body** (timeouts retried to
zero). Lists: `data/manifests/kdwarf_T0T1T2_residuals{,_identity,_centroid,_multisector}.csv` +
`kdwarf_T0T1T2_recurring_triage.csv`.

**RESOLVABLE-REGIME RESIDUALS (depth > 0.3%) — NOT a clean zero-flat-bottom outcome.** 6 of the 64
RESIDUAL are in the resolvable regime; **2 are flat-bottomed (flat_bottom ≥ 0.5)** — unlike the
published combined T0T1 (v3), which had none. Per human direction (2026-06-28): these are surfaced
and flagged as interesting candidates, **not explained away**; f_max(box) does NOT hold on a
zero-flat-bottom basis for T0T1T2 — there are flat-bottomed resolvable residuals to report.

| source_id | sectors | P(d) | depth | flat | asym | sec | odd_even | depth_cv | host ppm |
|---|---|---|---|---|---|---|---|---|---|
| **1397924585409290240** | 12 | 11.74 | **2.69%** | **1.00** | 0.14 | ~0 | 0.0015 | 1.56 | 1739 |
| 5427691493560560000 | 6 | 12.88 | 1.93% | 0.43 | **2.50** | ~0 | 0.004 | 1.22 | 2517 |
| 431616180013613568 | 2 | 12.32 | 0.38% | **0.75** | 1.07 | ~0 | 0.22 | 5.10 | 752 |
| 2561459808901475584 | 3 | 2.12 | 0.31% | 0.38 | 0.15 | ~0 | 0.013 | 1.29 | 1229 |
| 93357127133226496 | 7 | 3.20 | 0.30% | 0.29 | 0.65 | ~0 | 0.10 | NaN | 1850 |
| 4589589824738659200 | 5 | 12.40 | 0.30% | 0.44 | 0.15 | ~0 | 0.018 | NaN | 1646 |

**Standout: `1397924585409290240`** — flat-bottomed (flat=1.0), symmetric (asym=0.14), deep (2.69%),
recurs across **12 sectors**, no secondary eclipse, no odd-even depth difference. R_p/R_* ≈ √0.0269 ≈
0.16 (sub-stellar). It is a *persistent* flat-bottomed resolvable residual: it appeared identically
(flat=1.0, d=2.69%, P=11.74d) in the T0 (v2) triage CSV, and now survives the v4 activity-robust
detrending — persistence is the opposite of what an activity artifact should do under detrending.
It is a known active host (scatter 1739 ppm), so activity is *a* hypothesis, but it is not
established. **Not a detection; a follow-up candidate.** Needs human adjudication + phase-folded LC.

**Caveats to weigh (neutral, not adjudication):** (a) battery v4's local detrending materially shifts
morphology metrics — e.g. 5427691493560560000 was natural_planet in T0T1/v3 with asym=0.0098, now
RESIDUAL with asym=2.50; the detrending can reveal *or* distort shape, so v3↔v4 morphology should be
compared. (b) Discrepancy RESOLVED: the on-disk `kdwarf_T0_recurring_triage.csv` (12 RESIDUAL, max 2.69%) is a
**battery-v3 artifact** — overwritten when the cascade was re-run with v3 (commit 2131ee6 "v3 cascade
artifacts", touched again by 49814ae). The T0 status note below ("33 RESIDUAL, max 0.186%") describes
the **superseded battery-v2** T0 run whose CSV no longer exists on disk. Cite the v3 file as the
current T0, the v2 numbers only as historical. (Note the v3 on-disk T0 already contains
1397924585409290240 at flat=1.0/2.69% — the paper §4.2 addresses it as the active-host deep transiter,
consistent with the true-period correction above.)

**CORRECTION (2026-06-28, after phase-folding — refines the "2 flat-bottomed" headline above).**
The triage CSV computes morphology at k08's multi-sector period, which for several objects is a
**harmonic alias** of the true BLS period (1397924585409290240: 11.74 ≈ 4×2.94 d). At an alias period
the folded signal smears, so `flat_bottom` is unreliable *and* the v4 local detrend is defeated
(windows land at the wrong phase). Recomputed at each object's true BLS period (with v4 detrend
applied there) — `pipeline/runners/plot_resolvable_residuals.py` + table
`data/manifests/kdwarf_T0T1T2_resolvable_truePeriod_morphology.txt`:

| source_id | triage flat (alias) | flat @ trueP | asym @ trueP | depth | trueP | SDE |
|---|---|---|---|---|---|---|
| 1397924585409290240 | 1.00 | **0.67** | 0.03 | 7.2% | 2.94 | 11.0 |
| 5427691493560560000 | 0.43 | 0.40 | 0.67 | 0.33% | 11.42 | 4.1 |
| 431616180013613568 | 0.75 | 0.60 | 0.18 | 0.39% | 12.34 | 5.2 |
| 2561459808901475584 | 0.38 | 0.75 | 1.47 | 0.79% | 1.82 | 10.2 |
| 93357127133226496 | 0.29 | 0.75 | 1.34 | 0.58% | 3.20 | 9.9 |
| 4589589824738659200 | 0.44 | 0.11 | 0.29 | 0.47% | 12.42 | 3.7 |

At true periods **no object is cleanly flat (≈1) AND symmetric AND significant**: the ones that go
flat (2561…, 93357…) are highly asymmetric (asym>1.3); the symmetric one (1397…) is only moderately
flat (0.67). So the "2 flat-bottomed resolvable occulters" headline was an **alias artifact** — this
restores consistency with the v3 paper §4.2 ("no genuine flat-bottomed occulter; flat≈1 is an
activity/profile artifact"). **NOT a vindication-by-tuning:** the correction came from folding at the
detector's own recovered period, not from adjusting any cut. f_max(box) zero-flat-bottom basis is
**not** broken by an alias artifact — but the human should make the final call.

**The standout survives the correction and is NOT explained away:** `1397924585409290240` at its true
2.94 d period is a clean, deep (7.2%), strikingly symmetric (asym=0.03), recurring (12 sectors),
sub-stellar-radius (~1.9 R_J) dip the battery cannot classify, in no catalogue, and it survived the v4
activity fix built specifically for it (sin_r2=0.001). A real, uncatalogued deep transiter of
undetermined nature (inflated HJ / brown dwarf / grazing low-mass companion / other) — a genuine
follow-up target, carried as unexplained (paper Option A).

**Methodological item to log/fix:** k08's multi-sector period re-derivation can alias relative to k04's
single-pass BLS, corrupting the triage morphology metrics and defeating the v4 detrend. The resolvable
residuals' morphology should be verified at the BLS-consistent period (as done here) before any are
cited; consider reconciling k08's period to k04's or flagging alias multiples.

Figures: `figures/kdwarf_T0T1T2_resolvable_residuals.png` (all 6, folded at true P),
`figures/kdwarf_T0T1T2_standout_1397924585409290240.png` (harmonic check).

**Standout written up (2026-06-28): `paper/note_residual_TIC156074324.md`.** Full battery recomputed at
the true 2.94d period: no secondary (≈0), no odd-even (0.008), symmetric (asym 0.028), flat 0.67, low
sin_r2 (0.083), per-transit depth stable (CV 0.11, no dropouts), on-target centroid. Host = K1V,
Teff 4866K, R★≈0.72R☉, RUWE 1.06 (clean single-star astrometry) → R_p≈1.7–1.9 R_J (sub-stellar, large
for a planet). **Catalogue cross-checks: SIMBAD** = plain star, no variable/EB/planet type; **ExoFOP
(TIC 156074324)** = no TOI, no SPOC TCE, no disposition, no notes (caveat: ExoFOP TCEs are 2-min SPOC;
our detection is FFI, so absence may mean it wasn't a 2-min target); **literature** = nothing. So:
genuinely uncatalogued; survives all discriminants at true period; most-likely mundane (inflated HJ or
grazing/low-mass EB) but undetermined from photometry. **NOT a detection.** No solid *local* deeper-dive
path remains (planet-vs-EB needs RV / 2-min data / spectroscopy = external follow-up).

**Next:** continue the program (the period-alias k08↔k04 fix; paper §4.2 extension to G<13 remain open
items). The note + cascade are committed and pushed to origin/main.

Original resume note (retained): a reboot interrupting `k04 --unblind` is **no harm** — it writes
output only at the very end, so it leaves no partial file and is re-run from scratch (deterministic
against the frozen, tagged calibration).

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
