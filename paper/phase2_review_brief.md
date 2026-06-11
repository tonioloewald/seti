# Adversarial review brief — Phase 2 bright-tier paper (round 3, convergence check)

**For:** a separate Claude instance, then Gemini, as independent adversarial reviewers.
**Paper:** `paper/phase2_T0_draft.md`. **You have full repo access — run diagnostics, don't speculate.**
**Your job:** hostile referee. Two tasks: (1) verify the round-2 fixes actually landed and didn't
introduce new problems; (2) find anything still broken. Every criticism comes with a test or a fix.

---

## What this is

Pre-registered (OSF [osf.io/2akn3](https://osf.io/2akn3/)), mechanism-agnostic search for anomalous
transit *shapes* around K dwarfs (TESS). Fixed battery of natural explanations; Poisson limit
f_max = 3/ΣC_i per morphology family. Two tiers: T0 (G<11, 12,100 stars), combined T0+T1 (G<12,
44,202). Audit: `.venv/bin/python3 pipeline/runners/audit_T0_paper.py` (51/51 PASS).

## What changed since round 2 (verify each actually fixes what it claims)

Round 2 (you + Gemini) converged on five demands. The responses:

1. **Stop adjudicating the 3 resolvable residuals in prose ("fatal contradiction").** Response
   ("Option A"): §4.2 now *reports* them as residuals the frozen battery cannot auto-classify, with
   committed diagnostic metrics, and explicitly declines to explain them away object-by-object; no
   "pure null" is claimed. **Check: is this genuinely non-adjudicating, or just reworded
   adjudication?** The metrics cited (sin_r2=0.001 for the active host; SDE 2.3 / 0.89-px centroid for
   the near-blend; 5/7-sector intermittency) are in the committed CSVs — verify them, and judge
   whether "report with diagnostics + defer disposition" escapes the candidate-by-candidate objection
   or merely launders it.
2. **Define a stopping rule; freeze the battery.** Response: §5 + AMENDMENTS declare the battery frozen
   at v3 for these data, weaknesses declared-not-patched, fixes re-validated on injections *before*
   unblinding fainter tiers. The paper also **retracts** the earlier "refinement can only weaken the
   limit" claim as not a structural guarantee. **Check: is the stopping rule actually a constraint, or
   an escape hatch? Is the retraction complete?**
3. **f_max(box) "unchanged" is really +3%.** Response: now stated as "~3% move, within the ~1.7%
   per-cohort injection SE." **Check the SE claim** (300 injections/cohort, C_i≈0.9).
4. **Completeness grid stops at 2% while a residual is deeper.** Response: grid extended to
   {0.5,1,2,4,8,12,15}% and a `triangle` (asymmetric occulter) family added. This *measured* two
   boundaries now in the paper: box C_i holds to ~12% then →0 at 15% (the 13% depth→EB cut is an
   **upper bound** on the flat-occulter search); triangle C_i≈0.06 → f_max(asymmetric occulter)
   ~6e-3/9e-4. **Check: are these completeness numbers real (re-run k03b or spot-check), and is the
   13% ceiling a genuine blind spot the paper now honestly owns?**
5. **Factual errors.** 1397's depth was mis-stated 3.9%; now 2.69% (matches its 1.1 R_J and the triage
   CSV). 5615 was oversold as a "marginal detection"; now reported as a weak-statistic near-blend
   (SDE 2.3, centroid 0.89px, high-PM star). **Verify both against the artifacts.** An audit assertion
   on resolvable-residual depths was added to catch future mis-quotes.

## Fresh attack surface (find what round 2 missed)

- **The 13% upper-bound blind spot.** The depth→radius EB cut means a flat occulter larger than
  ~2.5 R_J is auto-classified a stellar companion and never flagged. A large megastructure is exactly
  such an object. Is "we are blind to flat occulters deeper than 13%" adequately surfaced, or buried?
  Is the whole megastructure framing undercut by a 13%-depth ceiling the abstract should state plainly?
- **Triangle C_i≈0.06 is devastating if taken seriously.** The search recovers only ~6% of asymmetric
  occulters (it calls them planets). If "asymmetry no natural occulter can produce" is a core
  selling-point morphology, a 6% completeness means the search is nearly blind to it. Does the paper
  honestly reckon with the fact that two of its three anomaly morphologies (tail, triangle) are weakly
  constrained, leaving essentially only the flat occulter — over a 0.3–13% depth window?
- **Is reporting-not-adjudicating actually weaker science, not stronger?** A skeptic could say: you
  now have 3 unexplained residuals and a pipeline that admits it can't classify them. Have you traded
  an overclaimed null for an underclaimed non-result? Is the limit still meaningful if the classifier
  leaves objects it cannot judge?
- **Anything in the prose vs artifacts** — re-run the audit, spot-check the cascade counts and the new
  triangle/deep-depth completeness in `data/manifests/kdwarf_*_calibration_*.json`.

## Verify against

- `pipeline/runners/audit_T0_paper.py` (51/51); `AMENDMENTS.md` (v2/v3 + the freeze/stopping-rule
  entry); `pipeline/fetch/k04_search.py` `battery()`; `data/manifests/kdwarf_{T0,T0T1}_recurring_triage.csv`
  (residuals + coherence columns); `data/manifests/kdwarf_calibration_{T0,T0T1}.json` (completeness grid).

Return: (A) for each of the 5 round-2 fixes, did it land — yes/no/partial, with evidence; (B) ranked
NEW or still-open flaws with fixes; (C) verdict: is the paper now defensible for external (Gemini)
review, or is there a remaining must-fix?
