# A Pre-Registered, Mechanism-Agnostic Search for Anomalous Transit Signatures Around Main-Sequence K Dwarfs: First-Tier (G<11) Results

**Status: DRAFT for review.** Phase 2 of the program whose Phase 1 (white dwarfs) is published
and registered at OSF [10.17605/OSF.IO/6YH7R](https://doi.org/10.17605/OSF.IO/6YH7R). The Phase-2
plan was registered at OSF [osf.io/2akn3](https://osf.io/2akn3/) before any K-dwarf light curve was
analysed; this paper reports the first (brightest) tier of the executed search.

## Abstract

We report the first-tier result of a pre-registered, mechanism-agnostic search for anomalous
transit signatures around main-sequence K dwarfs. Rather than assume what an enduring intelligence
would build, the search looks only for a departure from the natural transit model — most powerfully
a transit *shape* no natural occulter can produce — and attempts to explain every candidate away
through a fixed, pre-registered battery of natural hypotheses. Detection thresholds are not chosen
but *computed* by a registered procedure (a per-noise-cohort empirical null with genomic-control
inflation, plus injection-recovery completeness) and frozen before the candidate tail is unblinded.

Applied to 12,100 bright (G < 11) K dwarfs with TESS photometry, the pipeline reduces 4,131 raw
box-least-squares candidates, through an identity cross-check, a difference-image centroid gate, a
multi-sector recurrence test, and a multi-sector morphology triage, to **no candidate that survives
the battery in the regime where transit morphology is resolvable** (transit depth ≳ 0.3%, the floor
set by the pre-registered injection pilot). Every resolvable candidate is accounted for as a
transiting planet, an eclipsing binary, a background blend, a single-sector red-noise artifact, or a
catalogued object. Completeness is classification-aware — an injected anomaly is counted only if it
both is detected and survives the battery as a residual, bounding the anomaly→natural leakage
directly in the limit. The result bounds the rate of **detectable anomalous transit *signatures*
within the searched range** (period < 13 d, depth ≳ 0.3%, shape matching a forward-modelled family):
**f_max ≈ 2.8×10⁻⁴ for flat-occulter ("megastructure-like") morphologies and ≈ 3.4×10⁻⁴ for
disintegrating-tail-like ones** at 1% depth. These are signature rates, not occurrence rates of the
structures; the two relate as f_signature = f_structure · P_transit with P_transit ~ R⋆/a (a factor
~30–300 across plausible orbits), so we show the conversion but decline to quote a structure-
occurrence rate the data do not license. As a by-product the search flags
6 eclipsing-binary and 10 transiting-planet candidates among K dwarfs not previously catalogued as
such; a further 273 candidates are carried explicitly as recurrence-untestable, sub-resolution, or
uncentroidable **follow-up targets**, none a detection and none in the resolvable regime. We frame the result not as a one-off null but as the initial
calibration of a reusable screening engine whose limit tightens automatically as photometric
precision and time baselines improve. No claim of artificiality is made.

## 1. Introduction

This is Phase 2 of a program that reframes technosignature detection away from mechanism-assuming
SETI (Dyson spheres, Kardashev scaling) and toward the only thing an enduring intelligence must
produce to be detectable at all: an **anomaly** — a departure from the well-modelled natural
behaviour of a system that resists every natural explanation. Phase 1 applied this anomaly-residual
method to white dwarfs and returned a clean, fully-explained null with a quantitative upper limit.

Phase 2 carries the same validated machinery to a *living* host. Among living stars, K dwarfs offer
the longest stable main-sequence lifetime (15–40 Gyr), the quietest photospheric baseline, and —
being small — the deepest, most morphologically-resolvable transits. The cost, stated in the
registration: a living star's cool photosphere is bright in the infrared, so the IR-excess channel
that anchored Phase 1 loses its contrast. Phase 2 is therefore **transit-anchored**: we search for
transit light curves whose shape (asymmetry, flat-bottomedness, box-versus-U, anomalous duration,
variable depth) cannot be reproduced by any natural occulter after those are explicitly fitted and
excluded. The one retained assumption is the precondition for there being anything to find: a star
must have existed long enough for life to have had the chance to originate. We cannot measure a
field K dwarf's age directly, so this enters as an activity-based youth-proxy floor, stated as such.

The differentiator is not the transit channel, which is well-trodden, but the discipline: thresholds
fixed by a registered procedure rather than by inspecting candidates, and a mandatory, uniform
explain-away battery. We register the *method*, not the numbers; a reviewer judges adherence to the
procedure, not the values it produced.

## 2. Sample and data

The parent sample is a frozen, checksummed manifest of 175,968 main-sequence K dwarfs from Gaia DR3
(Teff 3900–5300 K, log g > 4.3, RUWE < 1.4, parallax_over_error > 10, within a main-sequence box;
git tag `phase2-manifest-1.0`). The manifest is analysed in nested, brightest-first tiers, with the
expansion trigger being available compute rather than any result. This paper reports tier T0
(G < 11): 12,100 stars with a usable TESS SPOC, TESS-SPOC, or QLP light curve, detrended with an
upward-only outlier clip so transits are preserved. The remaining ~400 of the tier are
saturated-bright stars absent from standard photometric processing, recorded as unanalysable and
self-weighting to zero in the limit.

## 3. Methods

### 3.1 Integrity invariant

No real candidate data are analysed before the detection thresholds are computed and frozen. The
registered procedure computes the per-cohort empirical null and the family-wise bar on the noise
floor and on synthetic and known-object injections only (the empirical null is estimated from the
bulk of the statistic, so any real transit sits in the tail and cannot shift it); the candidate tail
is unblinded exactly once, against the frozen calibration. Sample, query, recipe, and per-stage
residual lists are committed in a public, branch-protected repository linked from the registration.

### 3.2 Calibration

Each star's out-of-transit noise is measured with an outlier-blind estimator — the median absolute
deviation of the continuum after iterative downward-only sigma-clipping — so a genuine deep dip
cannot inflate its own baseline and mask itself. Stars are binned into three equal-count noise
cohorts. Within each cohort, box-least-squares (BLS) is run on every star's light curve and the
null location δ0 and scale σ0 of the detection statistic (the signal-detection-efficiency SDE) are
estimated from the **lower bulk** of the per-star distribution (the median and the 15.9th
percentile), so that the real transiting planets and binaries — which are common, not rare, and
populate the *upper* tail — do not bias the null. The family-wise detection bar is δ0 + z·σ0 with
z = Φ⁻¹(1 − 1/N_total), N_total the full 175,968-star manifest. We label σ0² as a genomic-control
factor λ by analogy with large-scale inference, but the BLS SDE is not a z-statistic, so values of
λ away from unity (here 0.68–1.02 across cohorts) carry no inflation/deflation meaning; λ is simply
the per-cohort bulk scale that sets the threshold. The bar is a **white-noise candidate-generation**
threshold: it controls pure-noise false alarms, but is deliberately permissive toward the real
astrophysical signals and red-noise/systematic outliers that any sensitive transit survey produces
(§4.1 — 34% of stars yield a candidate), which are removed *downstream* by the centroid and
recurrence stages rather than by the bar. For T0 the three cohorts are 507 ppm (bar 7.6 SDE), 938 ppm
(7.7), and 1268 ppm (8.5), each with ≈ 4,100 stars; the calibration is frozen at git tag
`phase2-calibration-T0`. Per-star, per-cohort
completeness C_i is measured by injecting a frozen library of forward-modelled morphologies (a flat
occulter and a disintegrating dust-tail, against a limb-darkened-planet control) into the real light
curves. An injection counts as recovered only if it is **both detected above the bar and survives
the natural-explanation battery (§3.3) as a residual** — so a flat occulter that BLS finds but the
morphology mislabels a planet earns no completeness credit. The limit is therefore a bound on
anomalies that survive *classification*, not merely on detectable ones. Recovery self-weights with
both activity and morphology: the flat occulter recovers at C_i ≈ 0.96 (quiet cohort, 1% depth),
falling to ≈ 0.78 in the active cohort and ≈ 0.90 at 0.5% depth; the dust-tail recovers at ≈ 0.74,
lower precisely because it is often, and correctly, explained away as a natural disintegrating body.
The natural-control planet recovers at ≈ 0.1 — it classifies as a planet and so earns essentially no
anomaly-completeness, as it should.

### 3.3 Search and the natural-explanation battery

Detection runs BLS for periodic transits in parallel with an aperiodic, variable-depth matched
filter, so a fluctuating or one-off dip is not discarded as noise; detection never depends on
morphology. Each candidate above its cohort bar passes through a battery applied in a fixed order:

1. **Light-curve battery** — fold on the BLS period and classify by morphology and stellar
   variability (sinusoid variance for activity; secondary eclipse and odd–even depth for eclipsing
   binaries; depth coefficient-of-variation for disintegrating bodies; U-shape vs flat-bottom for
   planet vs occulter), retaining as a residual only what no natural class explains.
2. **Identity cross-check** — coincidence with a confirmed planet, a TESS Object of Interest, or a
   SIMBAD eclipsing-binary / binary / variable explains the candidate away; a stellar-property
   classification (e.g. high proper motion) does not, and such candidates survive. Prior knowledge
   is used only to *subtract* candidates, never to assume the residual set is empty.
3. **Difference-image centroid gate** — at TESS's ~21″ pixels a background eclipsing binary is the
   dominant false positive. The out-of-transit-minus-in-transit image localises where the flux
   actually dropped; a centroid more than one pixel off-target marks a background blend.
4. **Multi-sector recurrence** — a real transit repeats in every sector the star was observed; a
   single-sector red-noise false alarm does not. Because the BLS search is confined to periods
   P < 13 days, a transit recurs at least twice within every 27-day sector, so each observed sector
   genuinely samples it and the test is well-posed: a candidate detected in ≥ 2 sectors recurs; one
   seen in only the discovery sector among ≥ 2 (where transits were expected and are absent) is a
   red-noise artifact. Periods longer than 13 days are *out of scope* for this single-sector search —
   not silently rejected — and would require the longer baselines discussed in §5.
5. **Multi-sector triage** — the recurring candidates are re-run through the full battery on their
   stitched multi-sector light curves, at higher signal-to-noise and with a refined ephemeris.

### 3.4 Upper limit

For a class of anomalous occulter with classification-aware completeness C_i(depth, period) (§3.2),
the Poisson 95% zero-detection bound on its prevalence is f_max = 3 / Σ C_i, reported separately per
morphology family and as a function of depth, so the limit states where the search has teeth (a flat
occulter bounds tightly; a tail that mimics a natural disintegrating body bounds loosely; a subtle
asymmetric shape at shallow depth, not at all) rather than collapsing all morphologies onto one
number. A candidate that cannot be classified — because it is too shallow to measure a shape, or its
recurrence cannot be tested — contributes no detection to the numerator and is carried as a follow-up
target, not as a null.

f_max so defined bounds the rate of detectable anomalous transit *signatures* — the fraction of stars
whose light curve shows such a transit — and three qualifiers travel with the number: the period lies
below 13 days (the BLS grid), the depth is above the ~0.3% resolution floor, and the shape matches one
of the forward-modelled families. It is **not** an occurrence rate of the occulting structures. The
two relate as f_signature = f_structure · P_transit, with P_transit ~ R⋆/a the geometric transit
probability (~0.3–6% across plausible orbits), so a structure-occurrence rate would be f_max /
P_transit — larger by a factor ~30–300. We do not quote one: P_transit is unconstrained without an
orbital-distribution assumption the data do not provide, and the conversion compounds further
conditionality, since f_max / P_transit bounds only the occurrence of structures that *would* produce
an in-range, detectable signature *if* they transited (and assumes at most one per star), not the
structures full stop. Reporting the signature rate, with the conversion shown but not performed, is
the limit the data license. The search is in this sense agnostic about an anomaly's origin but
specific to its *shape*: detection and flagging are template-free — any sufficiently deep departure
the battery cannot explain is reported as a residual (§3.3) — but the completeness, and hence f_max,
is defined only for the forward-modelled families, so an anomaly of unmodelled morphology would be
*flagged* yet its prevalence left *unconstrained*.

### 3.5 Validation

Before unblinding, the morphology metrics' separation of the forward-modelled families was
established quantitatively on the synthetic injection grid (the statistical validation, spanning
family × depth × period). Two named, published systems then serve as real-data spot-checks — not a
classifier validation set: the pipeline fires on the disintegrating planet KIC 12557548 /
Kepler-1520 (asymmetry and depth-variability both elevated) and stays quiet on the clean transiting
planet Kepler-8 b, the same discipline by which Phase 1 validated on WD 1856+534 b. A broader
real-data control set is a natural extension.

## 4. Results

### 4.1 The residual cascade

The 12,100-star search produced 4,131 candidates above the per-cohort bar. The light-curve battery
classified 1,289 as planets, 1,215 as eclipsing binaries, 136 as activity, and 133 as disintegrating
bodies, leaving 1,358 residuals. The identity cross-check cleared 135 known objects (29 confirmed
planets, 17 TOIs, 8 eclipsing binaries, 54 binaries, 27 variables), leaving 1,223. The centroid gate
resolved these into 546 background blends (killed), 616 on-target, and 61 uncentroidable — 52 with
too few in-transit cadences to form a difference image and 9 transient fetch failures — carried as
follow-up. Multi-sector recurrence sorted the 616 on-target into 388 single-sector red-noise
artifacts (rejected), 86 recurring transits, and 142 recurrence-untestable candidates (78 with a
single SPOC sector, 64 with only QLP/FFI photometry). The deep multi-sector triage of the 86
recurring transits returned 6 eclipsing binaries, 10 transiting
planets, and 70 sub-resolution detections.

### 4.2 No resolved anomaly, and the upper limit

In the regime where transit morphology can be measured, no candidate survives unexplained. That
regime is set not by hand but by the pre-registered injection pilot: the flat-occulter completeness
is C_i ≈ 0.96 at 1% depth and still ≈ 0.90 at 0.5%, dropping below the morphology floor only as the
folded-profile signal-to-noise falls beneath the registered separation thresholds. Every one of the
70 surviving "residual" detections lies below 0.3% depth (45 below 0.1%) — beneath that floor, where
flat-bottom, asymmetry, and depth-variability are noise-dominated and no shape can be measured — and
none shows a deep, flat-bottomed, or otherwise structured occulter.

Because the completeness is classification-aware (§3.2), the limit already absorbs the battery's
anomaly→natural leakage, and that leakage is small for the morphology that matters most: a flat
occulter is recovered-and-classified-as-anomalous at C_i ≈ 0.96, essentially its raw detection rate,
so the leakage-corrected limit is barely weaker than a detection-only one would be. Over the searched
T0 population the zero-detection bounds at 1% depth are **f_max ≈ 2.8×10⁻⁴ for flat-occulter anomalies**
(Σ C_i ≈ 10,900) and **≈ 3.4×10⁻⁴ for disintegrating-tail-like anomalies** (Σ C_i ≈ 8,950); the latter
is weaker because such a shape is frequently, and correctly, explained as a natural disintegrating
body. Both limits weaken toward shallower depths as C_i falls and lapse below ~0.3% depth, where the
search places no anomaly constraint by construction.

### 4.3 By-product catalogue

The search flags, as a by-product of value independent of the technosignature framing, 6 eclipsing-
binary candidates (up to 26% deep, one detected across 14 sectors) and 10 transiting-planet
candidates among K dwarfs not previously catalogued as such.

### 4.4 Inconclusive sets — a follow-up roadmap

Three sets are carried explicitly, as incomplete observations rather than detections: 142
recurrence-untestable candidates (one TESS SPOC sector, or QLP-only photometry), 70 sub-resolution
recurring dips (real, repeating, but too shallow to measure a shape), and 61 uncentroidable
candidates (too few in-transit cadences for a difference image, or a transient fetch failure) —
273 in all. They contribute no detection to the limit — an unclassifiable signal is assigned no
anomaly-completeness and so self-weights out of f_max — and none lies in the resolvable regime, so
none bears on the result above. Rather than discard them, we publish them as a curated target list:
the recurrence-untestable dips are immediate targets for TESS extended-mission sectors (one further
sector separates red noise from a long-lived occulter), the sub-resolution dips are targets for
higher-precision photometry (CHEOPS, PLATO) able to resolve their morphology, and the uncentroidable
set is recovered by a re-run of the centroid gate. The same engine, re-run as those data arrive,
clears the queue and tightens the limit with no change of method.

## 5. Discussion

The result is the null the program was designed to expect, reached without a single threshold tuned
to a candidate. Its informativeness rests on the cascade: the dominant transit false positive at
TESS resolution is the background eclipsing binary, removed by the centroid gate, and the dominant
artifact of a single-sector long-period search is red noise, removed by recurrence — together these
account for the bulk of the raw residuals. The principal limitation is the single-sector depth and
baseline: a 27-day sector yields only 2–4 transits at long period, which both seeds red-noise false
alarms (controlled here by recurrence where ≥ 2 sectors exist) and leaves the recurrence-untestable
set genuinely open. The sub-resolution residuals reflect a hard floor: below ~0.3% depth no transit
morphology can be measured, so the search detects but cannot classify, and makes no anomaly claim
there. The by-product eclipsing-binary and planet candidates are the expected natural yield of any
sensitive transit survey and are reported as such.

More than a single observational result, T0 is the initial calibration of a living screening engine.
Its statistical machinery adapts to better data without modification: as photometric precision
improves or baselines lengthen, the classification-aware completeness rises, the resolution floor
drops below 0.3% depth, and the f_max ceiling falls automatically — the limit scales with the
hardware (a future TESS data reduction, or a mission such as PLATO, tightens it with no change of
method). Because the analysis is built as a population-agnostic core with a thin per-population plugin
(`pipeline/core` vs `populations/k_dwarf.py`), the same engine retargets to M dwarfs, subgiants, or
any population one wishes to stress-test. And independent of the technosignature framing, it is an
efficient sieve that strips planets, eclipsing binaries, and instrumental artifacts from large
photometric datasets, leaving whatever genuinely resists modelling — of value to stellar astrophysics
regardless of the motivating question. The intended mode of operation is to re-run the engine as data
accumulate, lowering the limit as the census fills, until either the population is exhausted or a
signal survives the full battery.

## 6. Conclusions

The brightest tier of a pre-registered, mechanism-agnostic transit-anomaly search of 12,100 K dwarfs
yields no anomaly that survives the battery in the morphology-resolvable regime, classification-aware
population upper limits of f_max ≈ 2.8×10⁻⁴ (flat occulter) and ≈ 3.4×10⁻⁴ (disintegrating-tail) at
1% depth, a small by-product catalogue of natural transiting systems, and a curated 273-target
follow-up list. We present this as the initial calibration of a living pipeline rather than a closed
result: the null shows the natural-explanation battery is tight, and the same engine
(`pipeline/fetch/k02`–`k08`, on the validated population-agnostic core) extends to the fainter tiers
(G 11–13) for the full solar-neighbourhood census — where the larger Σ C_i tightens the limit and a
QLP-inclusive recurrence pass plus accumulating sectors close the inconclusive sets — and, beyond
that, to other populations and to better data as they arrive.

## 7. Data and code availability

Public, branch-protected repository linked from the OSF registration: the frozen manifest and
checksums, the pinned data recipe, the per-stage residual lists (`data/manifests/kdwarf_T0_*`), and
the full pipeline. Bulk light curves are fetched on demand from MAST. Calibration frozen at
`phase2-calibration-T0`.

## 8. Provenance

Authored and directed by the sole investigator, who bears full responsibility for the contents and
errors. Special thanks are owed to a cross-disciplinary collaborator whose insight brought the
population-level statistical standards of epidemiology and genome-wide association studies to bear on
the problem. Two AI systems (Google Gemini, Anthropic Claude) functioned as active co-designers and
adversarial reviewers in methodology, implementation, and review; the complete working transcripts
are archived in the public repository.

## References

- Efron, B. 2004, *JASA*, 99, 96 — empirical null.
- Devlin, B., & Roeder, K. 1999, *Biometrics*, 55, 997 — genomic control.
- Kovács, G., Zucker, S., & Mazeh, T. 2002, *A&A*, 391, 369 — Box Least Squares.
- Hippke, M., & Heller, R. 2019, *A&A*, 623, A39 — Transit Least Squares.
- Jenkins, J. M., et al. 2002, *ApJ*, 564, 495 — Kepler detection threshold.
- Arnold, L. F. A. 2005, *ApJ*, 627, 534 — artificial transit signatures.
- Rappaport, S., et al. 2012, *ApJ*, 752, 1 — KIC 12557548 (disintegrating planet).
- Vanderburg, A., et al. 2015, *Nature*, 526, 546 — WD 1145+017.
- Ricker, G. R., et al. 2015, *JATIS*, 1, 014003 — TESS.
