# Gemini re-review brief — Phase 2 bright-tier K-dwarf paper (post-convergence)

**Paper:** `paper/phase2_T0_draft.md` (shared alongside this brief).
**You reviewed an earlier draft** (the "v3" version) and returned a hostile methodological review. This
is a re-review of the **converged** draft, after a pass that implemented your review *and* a parallel
adversarial Claude review. Be a hostile referee again: confirm the fixes are real (not reworded), and
find anything still wrong. This brief is self-contained — it embeds the results you would otherwise
run yourself — so you can scrutinise the reasoning directly.

---

## What this is (recap)

Pre-registered (OSF osf.io/2akn3), mechanism-agnostic search for anomalous transit *shapes* around
K dwarfs (TESS). A fixed battery explains candidates away as natural (activity, eclipsing binary,
disintegrating body, planet, background blend, red noise); the unexplained remainder is bounded by a
Poisson limit f_max = 3/ΣC_i, reported **per morphology family**. Two tiers: T0 (G<11, 12,100 stars),
combined T0+T1 (G<12, 44,202). Detection bars are computed by a registered procedure and frozen; the
battery classifier was then refined twice post-data (logged in `AMENDMENTS.md`) and is **now frozen**.

## How your round-2 review was addressed (verify each is real, not cosmetic)

**1. "Fatal contradiction: manual adjudication of the final three residuals."** Accepted. §4.2 no
longer explains the three away object-by-object. They are reported as residuals the frozen battery
*cannot* auto-classify, each annotated with its **committed** diagnostic metrics (not prose
judgment), and their disposition is deferred to declared, uniformly-applied battery improvements. No
"pure null" is claimed. None is a flat-bottomed occulter, so the headline flat-occulter limit is
independent of how they resolve.

**2. "Red-noise over-correction → false negatives; raise the resolution floor until C_i(tail) > 0.80."**
**We did not raise the floor, and we ask you to reconsider this recommendation** — because the
premise was tested and did not hold. Your inference was: planet count jumped (45→92) and C_i(tail)
fell to ~0.58, therefore the depth-variability test is now blind to half the tails at faint G. We ran
exactly the test you proposed — inject real disintegrating tails into the faintest, noisiest G<12
stars and check the verdict. **Result: tail RESIDUAL-recovery is flat with host brightness** (≈0.52–
0.67 across the scatter range, no collapse at faint G), and a side-by-side re-implementation of the
old white-noise floor vs the new red-noise floor shows the new floor is, if anything, *more* permissive
at faint G (the white-noise floor over-suppressed at low cadence count). So the floor is not the
problem. The planet jump is real planets *correctly returning* from prior over-flagging, not anomalies
being buried. The true reason C_i(tail)≈0.58 is **structural, not a floor artifact**: a strongly
asymmetric tail is (correctly) classified a *natural* disintegrating body and earns no anomaly-credit
— the tail anomaly is near-degenerate with its own natural explanation. Raising the depth floor would
not fix this (it is an asymmetry degeneracy, not a depth effect). The paper now states the tail bound
is *intrinsically loose* for this reason (§4.2). **Do you accept the injection result, or do you have
a specific reason to distrust it?**

**3. "Incomplete completeness grid — extrapolating beyond 2%; expand to 15%."** Done. The injection
grid is now {0.5, 1, 2, 4, 8, 12, 15}% depth plus a fourth family (`triangle`, an asymmetric occulter).
This *measured* two boundaries (numbers below), rather than extrapolating.

**4. "Activity-metric limitation is load-bearing."** Bounded with numbers (below) and declared as a
limitation, not patched. The sinusoid activity gate (sin_r2) fires on **zero** residuals; a meaningful
fraction of residual hosts are high-variability.

**5. "f_max(box) is a real +3% shift, not 'unchanged'."** Accepted — stated as ~3%, comparable to the
≈1.7% per-cohort injection sampling error.

**6. Stopping rule.** Defined (§5, AMENDMENTS): the battery is **frozen at v3** for these data; known
weaknesses are declared, and any fix is made and re-validated on synthetic injection–recovery *before*
the fainter tiers are unblinded, never against the current candidate list. We also **retracted** the
earlier over-broad claim that the refinement procedure "can only weaken the limit" (true only for the
specific depth-variability change, not structurally).

## Embedded results (so you can audit the reasoning without the repo)

**Cascade (frozen v3 battery):**

| stage | T0 | T0+T1 |
|---|---|---|
| candidates > bar | 4,131 | 15,451 |
| → RESIDUAL (battery) | 765 | 3,036 |
| → survive identity | 666 | 2,821 |
| → on-target (centroid) | 337 | 1,121 |
| → recurring | 53 | 140 |
| → triage: EB / planet / disint / RESIDUAL | 5 / 35 / 1 / 12 | 17 / 92 / 4 / 27 |
| → resolvable residuals (depth > 0.3%) | 2 | 2 (3 distinct across tiers) |

**Per-family limits at 1% depth:** f_max(box) 2.75×10⁻⁴ (T0) / 8.3×10⁻⁵ (combined); f_max(tail)
4.2×10⁻⁴ / 1.2×10⁻⁴; f_max(asymmetric/triangle) 5.6×10⁻³ / 9.4×10⁻⁴.

**Flat-occulter completeness vs depth (combined, three cohorts), showing the upper boundary:**
0.5%: [0.66, 0.65, 0.26] · 1%: [0.91, 0.89, 0.64] · 2%: [0.97, 0.93, 0.73] · 4%: [0.98, 0.94, 0.80]
· 8%: [0.98, 0.95, 0.85] · 12%: [0.98, 0.95, 0.86] · **15%: [0, 0, 0]**. The collapse at 15% is the
depth→radius EB cut (depth > 13% ⟹ R_occ > 2.5 R_J ⟹ classified a stellar companion): the
flat-occulter search is structurally blind to occulters larger than a brown dwarf. This is now stated
in the abstract and conclusions, not buried.

**The three resolvable residuals (reported, not adjudicated):**
- `1397924585409290240` (G 10.7, 2.69%, P 11.7 d): detected 12/12 sectors, per-sector depth CV 0.25,
  depth–scatter corr 0.39 (a real transit), R_occ ≈ 1.1 R_J. Host at the 94th scatter percentile of
  planet hosts; sin_r2 = 0.001 — the activity gate sees nothing while irregular variability drives its
  shape flags.
- `5615925139763813248` (G 9.6): stitched-data SDE 2.3 (below the 8.7 bar), centroid 0.89 px
  off-target, high-proper-motion star — a weak-statistic near-blend.
- `93357127133226496` (G 11.7, 0.30%, P 3.2 d): at the floor, detected 5/7 sectors (absent in two),
  strongly asymmetric.

**Activity cross-match:** residual hosts above the planet-host 90th-percentile scatter: 5/12 (T0),
4/27 (combined); the sinusoid gate (sin_r2 > 0.6) fires on none of them.

**Audit:** `pipeline/runners/audit_T0_paper.py` reconstructs every number from committed artifacts —
53/53 PASS, including a per-source_id check on each resolvable residual's depth.

## Open questions for your final pass

1. **Is Option A (report-don't-adjudicate) the right resolution of your "fatal contradiction," or do
   you still prefer the algorithmic fix (upgrade the activity gate in code and re-run)?** The
   counter-argument to the algorithmic fix is the stopping rule: another in-loop battery change on the
   unblinded candidates is exactly what the discipline says to stop doing. Is "freeze + declare +
   report the residuals" sufficient, or a dodge?
2. **The narrow effective sensitivity.** Only the flat occulter is tightly bounded, over 0.3–13% depth
   and P < 13 d; tails are degenerate, asymmetric occulters recover at C_i ≈ 0.06, deep occulters are
   unconstrained. Is this honestly scoped now, or does it undercut the "mechanism-agnostic anomaly
   search" framing to the point the title/abstract overpromise?
3. **Does the injection result (point 2 above) actually retire your under-flagging concern?** If not,
   what specific test would change your mind?
4. **Any remaining must-fix before this is submittable**, or factual/logical errors in the prose.

Return a verdict: ready for write-up/submission, or remaining blockers (ranked).
