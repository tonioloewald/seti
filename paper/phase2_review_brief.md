# Adversarial review brief — Phase 2 bright-tier paper (battery v3, round 2)

**For:** a separate Claude instance (and then Gemini) as independent adversarial reviewers.
**Paper under review:** `paper/phase2_T0_draft.md` (share this brief alongside it).
**Your job:** try to break the result. Hostile referee, not friendly. Every criticism comes with how
you'd prove it or how to fix it. You have full repo access — run diagnostics, don't just speculate.

---

## What this is

A pre-registered (OSF [osf.io/2akn3](https://osf.io/2akn3/)), mechanism-agnostic search for
anomalous transit *shapes* around K dwarfs (TESS). Departures from the natural transit model that
survive a fixed battery of natural explanations (activity, EB, disintegrating body, planet,
background blend, red noise); Poisson upper limit `f_max = 3/ΣC_i` per morphology family. Two tiers:
T0 (G<11, 12,100 stars) and combined T0+T1 (G<12, 44,202 stars).

## What changed since your last review (this is round 2 — attack the new moves)

The **previous round's** automated review (you, effectively) found that the depth-variability test
over-flagged faint noisy stars (per-sector depth tracked per-sector scatter, corr up to 0.99). That
critique was implemented as **battery v3**:

1. **Red-noise-aware depth-variability floor** (§3.3): in-transit per-epoch depth scatter is now
   compared to the same scatter at *off-transit* phases (empirical control inheriting correlated
   noise), not to a white-noise `scatter/√n`. Only excess over that control counts as variability.
2. **Single 0.15 asymmetry boundary** (removed the 0.1–0.15 dead zone).
3. **C_i refreshed**, bars kept frozen (`k03b_refreeze_completeness.py`). Effect: `f_max(box)` held
   (2.75e-4 / 8.3e-5); **`f_max(tail)` loosened ~25%** (4.2e-4 / 1.2e-4) — reported as a correction.
4. **Per-sector coherence diagnostic** added to the triage (`sec_detected`, `sec_frac_detected`,
   `sec_depth_cv`, `sec_depth_scatter_corr`) — every resolvable residual now carries it.

**Result shift:** the v2 "seven resolvable residuals" (the depth-variable ones) correctly returned to
the planet class. v3 leaves **2 resolvable residuals per tier, 3 distinct objects**, each examined
per-object and found ordinary:
- `1397924585409290240` (G10.7): real deep 3.9% transit, **coherent 12/12 sectors**, but the host is
  **photometrically active** — variability corrupts the shape metrics (flat_bottom=1.0, asym=0.32).
  Called a by-product transiter + an **activity-metric limitation** (§3.5), not an anomaly.
- `5615925139763813248` (G9.6): marginal, only 2 sectors (depths 0.4% vs 1.0%).
- `93357127133226496` (G11.7): intermittent (5/7 sectors), shallow (0.34%, at floor), asym 0.67.

## The sharpest questions for THIS round (go hardest here)

1. **Did the pendulum swing from over-flagging to UNDER-flagging?** v2 over-flagged noise as anomalies;
   v3 may now hide real anomalies. The planet by-product count jumped (T0 13→35, combined 45→92) and
   the tail C_i fell to ~0.58. **Is the red-noise floor now so conservative it produces false
   negatives** — classifying a genuine variable-depth or shallow anomaly as a planet or as noise?
   Test it: inject a real disintegrating-tail signal (or a genuinely depth-varying occulter) into
   faint TESS light curves and check whether v3 still recovers it as RESIDUAL, or now buries it in
   `natural_planet`. The injection machinery is `pipeline/fetch/k03_calibrate.py` (`_recover`,
   families planet/box/tail) and the battery is `pipeline/fetch/k04_search.py` (`battery()`). If the
   tail recovery has collapsed at faint magnitude, the limit is being held up by a test that no longer
   fires — say so.

2. **Two rounds of post-data battery refinement — is this still disciplined or now a fishing
   expedition?** The defense (AMENDMENTS.md): each change is candidate-independent, the registered
   bars are never touched, and each can only *weaken* the limit. Is "monotone-weakening + bars frozen"
   a sufficient guardrail against an unbounded sequence of post-hoc refinements, or should the whole
   battery have been frozen pre-data? At what round does this stop being legitimate?

3. **Is the activity-metric limitation load-bearing — and is stating-not-fixing acceptable?** The
   `1397...` case shows shape metrics fail on active stars and the `sin_r2` activity gate misses
   irregular variability. **How many OTHER residuals (resolvable or sub-resolution) are active stars
   with corrupted metrics?** Could activity be masking a real anomaly elsewhere, or inflating the
   sub-resolution residual count? Is it defensible to ship with this stated as future work, or does it
   undercut the headline null? Cheap test: cross-match the residual lists against a variability/CDPP
   metric and report how many residuals are high-variability hosts.

4. **Is the per-object examination cherry-picking?** Each of the 3 gets a one-line "ordinary"
   explanation. Pressure-test each: is `5615...` ("marginal, 2 sectors") genuinely marginal or a real
   asymmetric transit being waved off? Is `93357...`'s intermittency real or a period/ephemeris error?
   Re-fetch and check.

5. **`f_max(box)` "unchanged" — true?** The box C_i cohort values moved ~2% (e.g. 0.93→0.907) and
   `f_max(box)` went 8.10→8.34e-5. Is "essentially unchanged within injection sampling" honest, or
   should the ~3% shift be owned as a real (if small) change from the population/subsample difference?

6. **Anything else** — the completeness grid stops at 2% while a residual is at 2.7% (no injection
   tests the 2%→13% depth corner); validation is still 2 Kepler spot-checks with zero faint-TESS
   active-star control; the signature-vs-occurrence conversion (§3.4); look-elsewhere for re-runs (§5).

## Where to verify

- Numbers: `pipeline/runners/audit_T0_paper.py` (47/47 PASS, both tiers, reconstructs every figure).
- Battery: `pipeline/fetch/k04_search.py` `battery()` (red-noise floor ~lines 90–120).
- Amendments + provenance of v2/v3: `AMENDMENTS.md`.
- Residuals + coherence columns: `data/manifests/kdwarf_{T0,T0T1}_recurring_triage.csv`.
- Cached light curves: `data/lightcurves/<source_id>.npz` (keys time, flux). Venv: `.venv/bin/python3`.

Return: (a) ranked flaws/overclaims with fixes; (b) the result of the false-negative injection test
(Q1) — does v3 still recover a real tail/variable anomaly at faint G, or did the fix over-correct?;
(c) verdict on whether two rounds of post-data refinement remain legitimate; (d) any
factual/internal-consistency errors vs the artifacts.
