# Adversarial review brief — Phase 2 bright-tier paper (battery v2 + combined tier)

**For:** Gemini and a separate Claude instance, as independent adversarial reviewers.
**Paper under review:** `paper/phase2_T0_draft.md` (share this brief alongside it).
**Your job:** try to break the result. Be a hostile referee, not a friendly one. Where the prose
overclaims, say so; where a number could be an artifact, say how you'd prove it.

---

## What this is

A pre-registered (OSF [osf.io/2akn3](https://osf.io/2akn3/)), mechanism-agnostic search for
**anomalous transit *shapes*** around K dwarfs — departures from the natural transit model that
survive a fixed battery of natural explanations (activity, eclipsing binary, disintegrating body,
planet, background blend, red noise). Thresholds are computed by a registered procedure and frozen
before unblinding; the limit is a Poisson zero-detection bound `f_max = 3 / ΣC_i` per morphology
family. Phase 1 (white dwarfs) is published; this is Phase 2.

## What changed since your last review (the things to attack)

The previous round reviewed a **T0-only (G < 11) clean null**. Two things are new:

1. **Battery v2 — two refinements made *after* unblinding** (logged in `AMENDMENTS.md`, Sec 3.3):
   - **Depth→radius EB criterion:** depth = (R_occ/R⋆)², so on a 0.7 R⊙ K dwarf a depth > 0.13
     implies R_occ > ~2.5 R_Jupiter → a stellar companion → `eclipsing_binary`. Catches
     faint-companion EBs whose secondary/odd-even signatures are too shallow to trigger the
     classical tests.
   - **Noise-aware depth-variability:** per-epoch depth scatter is compared to scatter/√n_in-transit;
     only *excess* beyond that counts as a disintegrating body, so photon noise no longer diverts
     real planets to RESIDUAL.
   - **Claimed to be limit-neutral:** injection-recovery confirms box→RESIDUAL and tail→RESIDUAL are
     preserved, so C_i, the bars, and f_max are byte-for-byte unchanged (audit confirms). Only the
     *labelling* of real by-product candidates changes.

2. **A combined bright sample T0+T1 (G < 12; 44,202 stars)**, re-calibrated from scratch. f_max
   tightens ~3.4× (box 2.8e-4 → 8.1e-5; tail 3.4e-4 → 9.5e-5).

## The headline shift you must scrutinise

- **T0 (G < 11): clean** — 0 morphology-resolvable residuals (deepest RESIDUAL 0.186%).
- **Combined T0+T1 (G < 12): 7 resolvable residuals** (depth > 0.3%) — the first the search has
  produced. They are framed as **follow-up candidates, not detections**. None is a flat-bottomed
  occulter; all imply sub-stellar radius (< 1.31 R_J); 5 are depth-variable beyond the noise floor,
  2 are asymmetric.

**Diagnostic already run — all 7 are in the fainter T1 tier (G > 11):**

| source_id | G | Teff | period (d) | depth | R_occ (R_J) | flat_bottom | asym | n_sec | why RESIDUAL |
|---|---|---|---|---|---|---|---|---|---|
| 1129490881755217152 | 11.26 | 5062 | 11.40 | 1.57% | 0.87 | 0.67 | 0.076 | 20 | depth-variable |
| 93357127133226496 | 11.71 | 5059 | 3.20 | 0.30% | 0.38 | 0.25 | 0.665 | 7 | asymmetric |
| 3788580279456572928 | 11.81 | 5064 | 1.46 | 1.94% | 0.97 | 0.38 | 0.040 | 8 | depth-variable |
| 1834102703593748864 | 11.50 | 5193 | 6.94 | 0.46% | 0.47 | 0.50 | 0.137 | 2 | asymmetric (gap) |
| 1864765162307057024 | 11.11 | 4898 | 2.00 | 3.54% | 1.31 | 0.28 | 0.044 | 4 | depth-variable |
| 5427691493560560000 | 11.96 | 5218 | 12.88 | 2.77% | 1.16 | 0.36 | 0.010 | 6 | depth-variable |
| 5316921989201452288 | 11.94 | 4667 | 3.52 | 0.62% | 0.55 | 0.23 | 0.019 | 5 | depth-variable |

## The sharpest questions (please go hardest at these)

1. **Are the 7 real anomalies or noise/systematics?** All sit at faint G > 11. The depth-variability
   test is *supposed* to be noise-aware (scales by scatter/√n). So why do all 5 depth-variable
   residuals appear only at faint magnitude? Two hypotheses: (a) genuine — fainter K dwarfs are more
   active/variable; (b) artifact — the per-point robust-scatter noise model underestimates faint-star
   *correlated* systematics (sector-to-sector dilution at TESS's 21″ pixels, CDPP red noise), so the
   test over-triggers. **How would you decisively distinguish (a) from (b) from the existing data**
   (e.g. depth-vs-sector correlation with crowding metric, odd-even on a per-sector basis, CDPP
   comparison to the cohort)? Is the paper's "astrophysical *or* instrumental, to be resolved by
   follow-up" hedge adequate, or a dodge?

2. **Post-data amendment legitimacy.** Battery v2 was prompted by seeing 15 residuals in the combined
   unblind. The defence is that it tunes *no parameter to any candidate* — the 0.13 depth follows from
   the radius relation, the 2.5σ excess from Gaussian noise — and was validated on the pre-data
   injection grid before application, with the limit provably unchanged. **Is that defence sufficient,
   or is this still a garden-of-forking-paths move?** What would make it airtight (e.g. should the
   criteria have been in the registration, and does deriving them from first principles excuse that)?

3. **The depth→radius EB cut uses a fixed R⋆ = 0.7 R⊙.** K dwarfs span ~0.6–0.8 R⊙. At 0.6 R⊙, depth
   0.13 → R_occ ≈ 2.15 R_J (still super-planetary, OK); a 2 R_J inflated hot Jupiter on a 0.7 R⊙ star
   gives depth ≈ 8.3% < 13% (safely below the cut). Does the fixed-R⋆ approximation ever
   mis-bin a real object, and should it use the per-star Teff→R⋆ instead?

4. **Is 7 in 44,202 surprising at all?** Or is it exactly the rate of spotted/active/grazing K dwarfs
   you'd expect, i.e. the result is "0 anomalies, 7 ordinary stellar oddities flagged for follow-up"?
   What's the right null expectation, and does the paper overstate the interest of the 7 by calling
   them "anomaly-candidates"?

5. **Asymmetry threshold gap.** One residual (asym 0.137) is RESIDUAL only because it falls in the gap
   between the planet cutoff (asym < 0.1) and the disintegrating cutoff (asym > 0.15). Is that gap
   principled, or an artifact of two independently-chosen thresholds?

6. **f_max-unchanged claim.** The paper asserts C_i is identical under battery v2 because box and tail
   injections still classify as RESIDUAL. Probe the logic: is there any depth/period corner where the
   new natural_planet or EB rule could capture an injected box/tail and silently lower C_i?

7. **Anything else** — overclaims, the signature-vs-occurrence-rate conversion (Sec 3.4), the
   look-elsewhere argument for re-runs (Sec 5), the validation set being only 2 Kepler spot-checks.

## Where to verify

- Numbers: `pipeline/runners/audit_T0_paper.py` reconstructs every figure from committed artifacts
  (47/47 PASS, both tiers).
- Amendments: `AMENDMENTS.md`. Battery code: `pipeline/fetch/k04_search.py` `battery()`.
- The 7 residuals and all per-stage lists: `data/manifests/kdwarf_T0T1_*`.

Please return: (a) anything you'd call a flaw or overclaim, ranked; (b) the single most likely
mundane explanation for the 7, and the cheapest test that would confirm or kill it; (c) a verdict on
whether the paper's framing of the 7 is appropriately cautious.
