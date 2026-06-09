# A Pre-Registered, Mechanism-Agnostic Search for Anomalous Transit Signatures Around Main-Sequence K Dwarfs: Bright-Tier (G < 12) Results

**Status: DRAFT for review.** Phase 2 of the program whose Phase 1 (white dwarfs) is published
and registered at OSF [10.17605/OSF.IO/6YH7R](https://doi.org/10.17605/OSF.IO/6YH7R). The Phase-2
plan was registered at OSF [osf.io/2akn3](https://osf.io/2akn3/) before any K-dwarf light curve was
analysed; this paper reports the executed search over the two brightest tiers — T0 (G < 11), the
registered headline tier, and a combined bright sample T0+T1 (G < 12) that tightens the limit
threefold and is the first to surface morphologically-resolvable follow-up candidates.

## Abstract

We report the first-tier result of a pre-registered, mechanism-agnostic search for anomalous
transit signatures around main-sequence K dwarfs. Rather than assume what an enduring intelligence
would build, the search looks only for a departure from the natural transit model — most powerfully
a transit *shape* no natural occulter can produce — and attempts to explain every candidate away
through a fixed, pre-registered battery of natural hypotheses. Detection thresholds are not chosen
but *computed* by a registered procedure (a per-noise-cohort empirical null calibrated on the lower
bulk of the statistic, plus injection-recovery completeness) and frozen before the candidate tail is
unblinded.

Applied first to 12,100 bright (G < 11) K dwarfs and then to a combined 44,202-star bright sample
(G < 12) with TESS photometry, the pipeline reduces the box-least-squares candidates through an
identity cross-check, a difference-image centroid gate, a multi-sector recurrence test, and a
multi-sector morphology triage. In the brightest (T0) tier **no candidate survives the battery in
the regime where transit morphology is resolvable** (transit depth ≳ 0.3%, the floor set by the
pre-registered injection pilot); in the deeper combined sample **seven candidates survive there —
all U-shaped, none a flat-bottomed occulter, all of sub-stellar implied radius (< 1.31 R_J)** — and
are carried as morphologically-anomalous **follow-up targets, not detections**. Completeness is
classification-aware: an injected anomaly is counted only if it both is detected and survives the
battery as a residual, bounding the anomaly→natural leakage directly in the limit. The result bounds
the rate of **detectable anomalous transit *signatures* within the searched range** (period < 13 d,
depth ≳ 0.3%, shape matching a forward-modelled family): for flat-occulter ("megastructure-like")
morphologies at 1% depth **f_max tightens from ≈ 2.8×10⁻⁴ (T0) to ≈ 8.1×10⁻⁵ (combined)**, and from
≈ 3.4×10⁻⁴ to ≈ 9.5×10⁻⁵ for disintegrating-tail-like ones; because none of the seven resolvable
residuals is a flat occulter, the megastructure-morphology limit rests on a zero-flat-residual basis.
These are signature rates, not occurrence rates of the structures; the two relate as
f_signature = f_structure · P_transit, and within the searched range (a ≲ 0.1 AU) the geometric
transit probability P_transit ~ R⋆/a runs ~3–30%, so a structure-occurrence rate would be larger by
at most ~30× — while orbits beyond ~0.1 AU are unsampled and unconstrained entirely. We show the
conversion but decline to quote an occurrence rate the data do not license. As a by-product the
search flags eclipsing-binary and transiting-planet candidates among K dwarfs not previously
catalogued as such (6 + 13 in T0; 25 + 45 in the combined sample); further candidates are carried
explicitly as recurrence-untestable, sub-resolution, or uncentroidable **follow-up targets**, none a
detection. We frame the result not as a one-off null but as the initial calibration of a reusable
screening engine whose limit tightens — and whose follow-up yield grows — automatically as
photometric precision, sky coverage, and time baselines improve. No claim of artificiality is made.

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
excluded.

The registration retained one further assumption — an activity-based youth-proxy floor, on the
premise that a host must be old enough for life to have originated. **We drop it, and declare the drop
as a registered deviation** rather than excise it silently. The premise does not survive scrutiny: it
is undefined (the only abiogenesis timescale is Earth's, N = 1, and the relevant clock for an enduring
*builder* is longer and less constrained still); for K dwarfs it is nearly vacuous (their 15–40 Gyr
main-sequence lifetimes exceed the age of the universe, so any K dwarf not conspicuously young clears
any Earth-calibrated bar by construction); and a biological-plausibility prior is precisely the kind
of mechanism assumption this program defines itself against. Dropping it costs nothing operationally —
the floor was never implemented as a sample cut (§2), so no candidate changes — and the activity it
would have keyed on is already handled where it belongs, on photometric-noise grounds: the battery
removes stellar activity as a false-positive class, and active (noisier) stars receive lower
completeness and so weight down in the limit. K dwarfs remain the target for the stability of their
long-lived, quiet platform and their deep, resolvable transits — properties of the host as an
*observing platform*, not a prior on its inhabitants.

The differentiator is not the transit channel, which is well-trodden, but the discipline: thresholds
fixed by a registered procedure rather than by inspecting candidates, and a mandatory, uniform
explain-away battery. We register the *method*, not the numbers; a reviewer judges adherence to the
procedure, not the values it produced.

## 2. Sample and data

The parent sample is a frozen, checksummed manifest of 175,968 main-sequence K dwarfs from Gaia DR3
(Teff 3900–5300 K, log g > 4.3, RUWE < 1.4, parallax_over_error > 10, within a main-sequence box;
git tag `phase2-manifest-1.0`). The manifest is analysed in nested, brightest-first tiers, with the
expansion trigger being available compute rather than any result. This paper reports two tiers. Tier
**T0 (G < 11)** is 12,100 stars with a usable TESS SPOC, TESS-SPOC, or QLP light curve, detrended
with an upward-only outlier clip so transits are preserved (the remaining ~400 of the tier are
saturated-bright stars absent from standard photometric processing, recorded as unanalysable and
self-weighting to zero in the limit). The **combined bright sample T0+T1 (G < 12)** adds the next
tier and is searched jointly as **44,202 stars** with usable photometry, re-calibrated from scratch
on the larger noise floor (so the combined limit is not a stitch of two per-tier limits but a single
calibrated search; git tag `phase2-calibration-T0T1`). T0 is retained intact as the registered
headline tier and is reported alongside the combined result rather than superseded; the combined
calibration and residual lists are separate, immutable artifacts (`kdwarf_T0T1_*`).

The activity-based youth floor named in the registration is **dropped** (§1) — a registered deviation,
not deferred work — so the only sample cuts are the Teff / log g / RUWE / parallax / colour-magnitude
criteria above, and the full main-sequence K-dwarf manifest is searched. The floor was never
implemented as a cut, so dropping it removes no candidate and changes no number. Stellar activity
enters only on photometric-noise grounds (the battery removes it as a false-positive class, and active
cohorts carry lower completeness); the result below is a constraint on the full main-sequence
population.

## 3. Methods

### 3.1 Integrity invariant

No real candidate data are analysed before the detection thresholds are computed and frozen. The
registered procedure computes the per-cohort empirical null and the family-wise bar on the noise
floor and on synthetic and known-object injections only (the empirical null is estimated from the
*lower* bulk of the statistic, so the common real transits, which populate the upper tail, cannot
shift it); the candidate tail
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
the per-cohort bulk scale that sets the threshold (we retain the genomic-control reference for this
per-cohort scaling construction, not for an inflation correction, which the SDE does not admit). The bar is a **white-noise candidate-generation**
threshold: it controls pure-noise false alarms, but is deliberately permissive toward the real
astrophysical signals and red-noise/systematic outliers that any sensitive transit survey produces
(§4.1 — 34% of stars yield a candidate), which are removed *downstream* by the centroid and
recurrence stages rather than by the bar. For T0 the three cohorts are 507 ppm (bar 7.6 SDE), 938 ppm
(7.7), and 1268 ppm (8.5), each with ≈ 4,100 stars; the calibration is frozen at git tag
`phase2-calibration-T0`. The combined T0+T1 sample is re-calibrated identically on its own 44,202-star
noise floor — cohorts 595, 1262, and 2051 ppm with bars 7.3, 8.1, and 8.7 SDE (git tag
`phase2-calibration-T0T1`); the fainter tier raises the per-cohort scatter and so the combined search
trades a slightly higher noise floor for ~3.6× more stars, net-tightening the limit. Per-star, per-cohort
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
   binaries; depth variability for disintegrating bodies; U-shape vs flat-bottom for planet vs
   occulter), retaining as a residual only what no natural class explains. Two of these tests are
   sharpened by physics that needs no free parameter (logged as a registered methods refinement,
   §6 / `AMENDMENTS.md`). First, a transit depth implies an occulter radius — depth = (R_occ/R⋆)²,
   so on a 0.7 R⊙ K dwarf a depth above ~0.13 implies R_occ > ~2.5 R_Jupiter, larger than any planet
   or brown dwarf and therefore a stellar companion; such a transit is classed an eclipsing binary
   directly, catching the faint-companion eclipsing binaries whose secondary and odd–even signatures
   are too shallow to trigger the classical tests. Second, the depth-variability test is evaluated
   against the noise expectation: the per-epoch depth scatter is compared to scatter/√n_in-transit,
   and only an *excess* beyond that floor counts as genuine variability — so photon noise on a
   shallow but real planet no longer inflates its apparent depth-variability and diverts it out of
   the planet class. Both refinements were validated pre-application on the injection grid (a flat
   occulter still classes as a residual, a variable-depth tail still classes as a residual) so the
   completeness, the bars, and the limit are unchanged; only the labelling of real by-product
   candidates is improved.
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
probability. Critically, the conversion is valid only over the orbits the search actually samples:
across the searched range (P < 13 d, hence a ≲ 0.1 AU for a 0.7 M⊙ K dwarf) P_transit runs from ~30%
at the shortest periods to ~3% at P = 13 d, so a structure-occurrence rate would be f_max / P_transit
— larger by **at most ~30×**. We do *not* extend this to wider orbits: at a ≈ 1 AU the factor would be
~300×, but P = 13 d is the period ceiling of the BLS grid, so structures on orbits beyond ~0.1 AU are
not sampled and are entirely unconstrained, not loosely constrained by a large conversion. Even within
range we decline to quote an occurrence number: P_transit needs an orbital-distribution assumption the
data do not provide, and the conversion compounds further conditionality, since f_max / P_transit
bounds only the occurrence of structures that *would* produce an in-range, detectable signature *if*
they transited (and assumes at most one per star), not the structures full stop. Reporting the signature rate, with the conversion shown but not performed, is
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
planet Kepler-8 b, the same discipline by which Phase 1 validated on WD 1856+534 b. These Kepler
spot-checks exercise only the morphology classifier; the TESS-specific stages — the 21″ difference-
image centroid gate and multi-sector recurrence — are instead exercised on the survey candidates
themselves (§4.1), where they remove background blends and single-sector red noise at scale. A broader
real-data control set spanning all stages is a natural extension.

## 4. Results

### 4.1 The residual cascade

**T0 (G < 11).** The 12,100-star search produced 4,131 candidates above the per-cohort bar. The
light-curve battery classified 1,560 as planets, 1,336 as eclipsing binaries, 136 as activity, and
76 as disintegrating bodies, leaving 1,023 residuals. The identity cross-check cleared 111 known
objects (30 confirmed planets, 15 TOIs, 1 eclipsing binary, 41 binaries, 24 variables), leaving 912.
The centroid gate resolved these into 430 background blends (killed), 463 on-target, and 19
uncentroidable (11 with too few in-transit cadences to form a difference image, 8 transient fetch
failures) carried as follow-up. Multi-sector recurrence sorted the 463 on-target into 289
single-sector red-noise artifacts (rejected), 61 recurring transits, and 113 recurrence-untestable
candidates (68 with a single SPOC sector, 45 with only QLP/FFI photometry). The deep multi-sector
triage of the 61 recurring transits returned 6 eclipsing binaries, 13 transiting planets, 9
disintegrating bodies, and 33 sub-resolution residuals.

**Combined T0+T1 (G < 12).** The joint 44,202-star search produced 15,451 candidates above the bar;
the battery left 4,223 residuals (5,504 planets, 4,674 eclipsing binaries, 759 activity, 282
disintegrating). Identity cleared 267 known objects, leaving 3,956; the centroid gate kept 1,607
on-target (2,211 blends killed, 138 uncentroidable); recurrence confirmed 198 recurring transits
(868 single-sector artifacts rejected, 541 recurrence-untestable). The deep triage of the 198
recurring returned 25 eclipsing binaries, 45 transiting planets, 30 disintegrating bodies, and 98
residuals — of which **seven lie in the morphology-resolvable regime** (depth > 0.3%; §4.2), the
first such survivors the search has produced, the remaining 91 being sub-resolution.

### 4.2 No resolved anomaly, and the upper limit

The resolvable regime is set not by hand but by the pre-registered injection pilot: the flat-occulter
completeness is C_i ≈ 0.96 at 1% depth and still ≈ 0.90 at 0.5%, dropping below the morphology floor
only as the folded-profile signal-to-noise falls beneath the registered separation thresholds.

**T0: a clean resolvable null.** In the brightest tier no candidate survives the battery where
morphology can be measured. Every one of the 33 surviving residuals lies below 0.3% depth (the
deepest is 0.186%) — beneath the floor, where flat-bottom, asymmetry, and depth-variability are
noise-dominated and no shape can be measured — and none shows a deep, flat-bottomed, or otherwise
structured occulter.

**Combined T0+T1: seven resolvable follow-up residuals, none a flat occulter.** The deeper sample is
the first to leave survivors in the resolvable regime: seven of its 98 residuals exceed 0.3% depth
(0.30–3.54%). They are **not detections** — each has passed only the on-target and recurrence gates
and now awaits human difference-imaging and depth-consistency review — and their morphology is
informative. None is a flat-bottomed occulter (the cleanest megastructure-like signature; the
flattest has a flat-bottom score of 0.67, all U-shaped), and all imply a sub-stellar occulter radius
(0.55–1.31 R_Jupiter), so none is a hidden eclipsing binary. Two are notably asymmetric. The other
five are U-shaped and symmetric but show per-transit depth variability exceeding the noise floor
(§3.3); whether that variability is astrophysical (starspot crossings, gravity darkening, a
multi-body system) or instrumental (sector-dependent dilution at TESS's coarse pixels) is exactly
what the follow-up will settle. The pipeline’s role is to surface them rather than to explain them
away, and it does: they are carried as a curated anomaly-candidate list, with no claim attached.
Critically, because **none is a flat occulter**, the megastructure-morphology limit below stands on a
zero-flat-residual basis in both tiers.

**The limit.** Because the completeness is classification-aware (§3.2), the limit already absorbs the
battery's anomaly→natural leakage, and that leakage is small for the morphology that matters most: a
flat occulter is recovered-and-classified-as-anomalous at C_i ≈ 0.96, essentially its raw detection
rate, so the leakage-corrected limit is barely weaker than a detection-only one would be. The
zero-detection bounds at 1% depth are, for flat-occulter anomalies, **f_max ≈ 2.8×10⁻⁴ in T0**
(Σ C_i ≈ 10,900) tightening to **≈ 8.1×10⁻⁵ in the combined sample** (Σ C_i ≈ 37,000), and for
disintegrating-tail-like anomalies **≈ 3.4×10⁻⁴ → ≈ 9.5×10⁻⁵** (Σ C_i ≈ 8,950 → ≈ 31,600); the tail
limit is weaker at fixed sample because such a shape is frequently, and correctly, explained as a
natural disintegrating body. Both limits weaken toward shallower depths as C_i falls and lapse below
~0.3% depth, where the search places no anomaly constraint by construction.

### 4.3 By-product catalogue

The search flags, as a by-product of value independent of the technosignature framing, eclipsing-
binary and transiting-planet candidates among K dwarfs not previously catalogued as such: 6 + 13 in
T0, and 25 + 45 in the combined sample (the depth→radius criterion of §3.3 moves several deep
faint-companion systems into the eclipsing-binary column that the classical secondary/odd-even tests
had left unclassified). Each recurs across sectors and is on-target by difference imaging.

### 4.4 Inconclusive sets — a follow-up roadmap

Beyond the explained candidates, four sets are carried explicitly as incomplete observations rather
than detections (counts given as T0 / combined). The highest priority is new to the deeper sample:
the **seven morphology-resolvable residuals** (0 / 7; §4.2) — real, recurring, on-target transits of
unusual shape (asymmetric, or depth-variable beyond the noise floor) that no natural class explains,
each a direct target for difference-image confirmation and per-sector depth analysis. Below them sit
the sets that are open for want of data, not want of explanation: **recurrence-untestable** dips
(113 / 541; one TESS SPOC sector, or QLP-only photometry), **sub-resolution recurring** dips (33 / 91;
real, repeating, but too shallow to measure a shape), and **uncentroidable** candidates (19 / 138;
too few in-transit cadences for a difference image, or a transient fetch failure). The three
data-limited sets contribute no detection to the limit — an unclassifiable or sub-resolution signal
is assigned no anomaly-completeness and so self-weights out of f_max. Rather than discard any of
them, we publish them as a curated target list: the resolvable seven for immediate difference-imaging
follow-up; the recurrence-untestable dips for TESS extended-mission sectors (one further sector
separates red noise from a long-lived occulter); the sub-resolution dips for higher-precision
photometry (CHEOPS, PLATO) able to resolve their morphology; and the uncentroidable set for a re-run
of the centroid gate. The same engine, re-run as those data arrive, clears the queue and tightens the
limit with no change of method.

## 5. Discussion

The result is the outcome the program was designed to expect, reached without a single threshold
tuned to a candidate: no anomaly is claimed, the megastructure-morphology limit holds on a
zero-flat-residual basis in both tiers, and the deeper search behaves exactly as a screening engine
should — tightening the limit threefold while surfacing, for the first time, a short list of
genuinely odd transiting signals (the seven resolvable residuals of §4.2) for human follow-up rather
than explaining them away. That T0 is clean in the resolvable regime and the combined sample is not
is expected, not contradictory: 3.6× more stars and a fainter tier admit more astrophysically
unusual systems (spotted, gravity-darkened, or multi-body transiters) whose depth-variability or
asymmetry the battery is built to flag, not to absorb. Its informativeness rests on the cascade: the
dominant transit false positive at TESS resolution is the background eclipsing binary, removed by the
centroid gate, and the dominant artifact of a single-sector long-period search is red noise, removed
by recurrence — together these account for the bulk of the raw residuals. The principal limitation is the single-sector depth and
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
signal survives the full battery. Such re-runs are sequential looks at the same hypotheses rather than
independent trials, but they do not inflate the false-alarm rate the way naive repeated testing would:
the decisive battery stages strengthen with more data — additional sectors make spurious recurrence
*harder*, not easier, to pass, and deeper photometry resolves morphology that was previously
unmeasurable — so accumulating data subjects a candidate to progressively more stringent tests, and
the look-elsewhere cost of the re-run family is largely self-correcting.

## 6. Conclusions

The two brightest tiers of a pre-registered, mechanism-agnostic transit-anomaly search — 12,100
K dwarfs (G < 11) and a combined 44,202-star bright sample (G < 12) — yield no anomaly claimed as a
detection; classification-aware population upper limits on flat-occulter ("megastructure-like")
signatures that tighten from f_max ≈ 2.8×10⁻⁴ to ≈ 8.1×10⁻⁵ at 1% depth (and ≈ 3.4×10⁻⁴ → ≈ 9.5×10⁻⁵
for disintegrating-tail-like ones), on a zero-flat-residual basis in both tiers; a by-product
catalogue of natural transiting systems; and a curated follow-up list whose top entries are seven
morphology-resolvable residuals in the combined sample — none a flat occulter, all sub-stellar in
implied radius — carried as anomaly-candidates for difference-imaging follow-up, not as detections.
We present this as the calibration of a living pipeline rather than a closed result: the limit holds
where it has teeth, the battery surfaces what it cannot explain rather than absorbing it, and the
same engine (`pipeline/fetch/k02`–`k08`, on the validated population-agnostic core) extends to the
fainter tiers (G 12–13) for the full solar-neighbourhood census — where the larger Σ C_i tightens the
limit further and a QLP-inclusive recurrence pass plus accumulating sectors close the inconclusive
sets — and, beyond that, to other populations and to better data as they arrive.

## 7. Data and code availability

Public, branch-protected repository linked from the OSF registration: the frozen manifest and
checksums, the pinned data recipe, the per-stage residual lists for both tiers
(`data/manifests/kdwarf_T0_*` and `kdwarf_T0T1_*`, including the seven resolvable residuals in the
combined triage), and the full pipeline. Bulk light curves are fetched on demand from MAST.
Calibrations frozen at `phase2-calibration-T0` and `phase2-calibration-T0T1`; the two battery
refinements of §3.3 are logged in `AMENDMENTS.md`. Every number in this paper is reconstructed from
the committed artifacts by `pipeline/runners/audit_T0_paper.py`.

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
