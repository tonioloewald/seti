# Pre-registration (DRAFT) — An Anomaly-Residual Search for Unexplained Transit and Photometric Signatures Around Old, Quiet K Dwarfs

**Status: DRAFT / in preparation — NOT yet registered.** Phase 2 of the program whose
Phase 1 (white dwarfs) is registered at OSF [10.17605/OSF.IO/6YH7R](https://doi.org/10.17605/OSF.IO/6YH7R).
This plan is to be frozen and registered on OSF **before any K-dwarf light curve is analysed**;
until then it is edited freely in this repository. It reuses the *validated* population-agnostic
pipeline core (see `pipeline/core/`, regression-tested in `pipeline/runners/validate_wd.py`);
the K-dwarf-specific parts are a new population plugin, not a fork.

---

## 0. Summary

A pre-registered, mechanism-agnostic search for anomalous transit and photometric signatures
around **old, quiet main-sequence K dwarfs** — the longest-lived, most thermally-stable, and
photometrically-quietest *living* stellar hosts. Phase 1 applied this anomaly-residual
methodology to white-dwarf remnants and returned a clean, fully-explained null with a
quantitative upper limit. Phase 2 carries the **same validated machinery** to a living host,
with **transit morphology as the primary channel**. We search for departures from the natural
model — most powerfully, transit light curves whose *shape* no natural occulter (planet,
eclipsing binary, disintegrating body, starspot) can produce — and try to explain each away
through a fixed natural-explanation battery, with detection thresholds set by an empirical null
and injection-recovery, never by inspecting candidates.

## 1. The search target and its assumptions

- **The target is the observable anomaly** — an unexplained transit/photometric departure — not
  a presupposed structure, mechanism, or agent (as in Phase 1).
- **The agnostic stance, extended.** We are agnostic about: (a) *mechanism* — no assumed
  engineering; (b) *engineering vs. mere existence* — we detect departures in the star's light
  and do not presuppose they are built; (c) *timescale* — we assume no schedule of activity.
  A consequence we state plainly: over our ~decade observational baselines, any process on
  >decade timescales is effectively **static**, so the realistic primary signal is a *steady*
  anomaly (a persistent anomalous transit shape), with genuine *variability* (a changing transit
  depth or morphology) the highest-value-but-lowest-prior bonus, not the expectation.
- **The one prior we retain: time for life to have *originated*.** This is not a mechanism or
  timescale assumption — it is the precondition for there being anything to find at all. K dwarfs
  uniquely maximise it: 15–40 Gyr main-sequence lifetimes mean every K dwarf has had ample time
  and none has evolved off the main sequence. The sample is further weighted toward *old* K
  dwarfs (§3).
- **What we refuse to assume.** We do not assume life requires planets, photosynthesis, visible
  light, or any particular biochemistry. None of these enters the detection — which measures only
  departures in the star's integrated light — so the search takes no position on them.
- **Why K dwarfs, and the honest limitation.** Among *living* hosts, K dwarfs offer the longest
  stable lifetime, the quietest baseline (calmer than flaring M dwarfs), and — being small — the
  deepest, most morphologically-resolvable transits. The cost, stated up front: a living star's
  cool photosphere is bright in the infrared, so the IR-excess channel that anchored Phase 1
  loses its contrast. **Phase 2 is therefore transit-anchored, not excess-anchored.** We further
  acknowledge the transit channel is comparatively well-trodden; our differentiator is not the
  channel but the *discipline* — calibrated empirical-null thresholds and a mandatory,
  pre-registered explain-away battery applied uniformly.

## 2. Research questions

- **RQ1 (morphology).** Do any K dwarfs show a periodic transit whose *shape* — asymmetry,
  flat-bottomedness, box-versus-U, anomalous duration or secondary structure — cannot be
  reproduced by any natural occulter (sphere, ring, eclipsing binary, disintegrating body) after
  those are explicitly fitted and excluded?
- **RQ2 (photometric departure).** Do any show a persistent or time-varying photometric signature
  departing from the natural rotation/granulation/activity model that survives the battery?
- **RQ3 (upper limit).** With no unexplained anomaly, what upper limit `f_max` can we place on
  the prevalence of anomalous occulters/departures around old, quiet K dwarfs, as a function of
  depth and period?

## 3. Sample and inclusion

- **Parent sample.** Main-sequence K dwarfs from Gaia DR3: Teff 3900–5300 K, log g > 4.3 (dwarf,
  excluding subgiants/giants), with clean astrometry (RUWE < 1.4, parallax_over_error > 10), plus
  the equivalent absolute-G versus (G_BP − G_RP) main-sequence box. *Scale (this repository, sized
  pre-data):* ~12,600 at G < 11; ~22,000 within 100 pc; ~178,000 at G < 13. Target finding is not
  the binding constraint. The exact constraints (the colour–magnitude box, the RUWE and parallax
  cuts, and the hard magnitude/volume limit) are committed as an **immutable, checksummed
  manifest** of source_ids before any light curve is pulled — the frozen sample against which all
  later results are reproducible, identical in spirit to the Phase-1 `wd_sample` manifest.
- **Data-quality / channel requirement.** A usable TESS and/or Kepler light curve (the transit
  instrument). The Kepler-field subset (4-year continuous photometry) is the morphology gold
  standard and is treated as a distinct, deepest tier.
- **The goal is the whole population; staging is a resource constraint, not a scientific one.** We
  impose no scientific exclusion beyond the minimal *youth floor* below and the data-quality
  requirement above. Which stars have been *analysed* at any moment is set by available compute;
  the asymptotic target is the entire K-dwarf census.
- **Youth floor (the one real cut — soft and pre-specified).** We exclude only genuinely young,
  active stars, for two reasons that point the same way: the *life prior* (a star must have
  *existed* long enough for life to have originated, regardless of how long it will ultimately
  live) and *data quality* (young K dwarfs are magnetically active — the worst photometric noise).
  The floor is a **fixed rule, not a placeholder** (so the data decides *which* stars without any
  human break-picking): a star is excluded iff **(i)** its gyrochronological age from a measured
  rotation period, via the Angus et al. (2019) relation, is **< 1.0 Gyr**, **or (ii)** its
  fractional X-ray luminosity (eROSITA/ROSAT) is **log(L_X/L_bol) > −4.0** (saturated/active), **or
  (iii)** it lacks a rotation period *and* sits in the youngest decile of the Gaia
  photometric-variability-amplitude distribution. Stars with no measurable rotation period and
  normal activity are **retained** (absence of a period is not youth). These relations and the
  three numeric cuts (1.0 Gyr, −4.0 dex, 10th percentile) are frozen here; rotation/activity are
  measured pre-unblinding as noise characterisation, never from the transit candidates.
- **No hard "quiet" cut — noisy stars self-weight.** Rather than excluding active stars, we include
  every star above the youth floor and let the per-star injection-recovery completeness C_i (§5) do
  the work: a transit is harder to recover in an active light curve, so a noisy star earns a low
  C_i and contributes little to `f_max` automatically (the Phase-1 self-weighting principle —
  under-probed objects weight toward zero). The limit stays honest over whatever has been analysed.
- **Resource-triggered, nested, staged analysis order (so iteration stays confirmatory).** Because
  the goal is everything and the binding constraint is compute, we pre-register a *nested* sequence
  of tiers (cleanest/brightest first: T₁ ⊂ T₂ ⊂ … ⊂ the full sample), analysed in that fixed order,
  with the expansion trigger being *available resources*, declared in advance — never the result of
  a prior tier. **The detection threshold is *not* spent per stage** (our compute-determined tiers
  have no pre-fixed information fractions, so a group-sequential alpha-spending function would not
  apply): instead the survey-wide family-wise threshold (§5) is set **once, for control over the
  entire intended census** — the full frozen sample size N_total declared in the manifest — and
  applied **unchanged** to every tier. Expanding the analysed set can therefore only add confirmed
  detections under the *same fixed bar*; it can never relax the threshold, so there is no dial to
  tune by stopping at a convenient tier. This is deliberately conservative (we control as if the
  whole census were analysed from the start). Growing the sample is a pre-registered confirmatory
  extension (cf. the Phase-1 variability expansion); what is forbidden is loosening any boundary
  *in reaction to a result* or to rescue a candidate.
- No assumption that an anomaly orbits in a habitable zone; all periods the data permit are
  searched.
- **Stated selection biases:** brightness-limited (toward nearby), the TESS/Kepler footprint, and
  the youth floor. `f_max` is interpreted as a prevalence among the *effectively probed,
  solar-neighbourhood* K-dwarf population, self-weighted by per-star completeness.

## 4. Channels

- **Channel B — transit morphology (PRIMARY, CALIBRATED).** Detection by BLS/TLS for periodic
  box/U transits, **plus a parallel variable-depth / aperiodic-dip detector**, then morphology
  metrics (asymmetry, flat-bottom fraction, box-vs-U, duty cycle) and a **mandatory automated
  difference-image centroid gate** (§5). The Phase-1 machinery transfers directly: K dwarfs are
  point sources with clean Gaia astrometry, and a real occulter gives a *deep* transit, so the
  "deep ⇒ on-target real; shallow-and-offset ⇒ background blend, confirmed by centroiding" logic
  applies (the same code validated for white dwarfs, `pipeline/analysis/07–09`). Crucially, the
  sample size — tens of thousands versus Phase 1's 157 — **graduates this from a secondary,
  candidate-generating channel into a primary, calibrated one**: it now supports a rigorous
  population-level upper limit on structural transit anomalies (RQ3, §5), the transit analogue of
  Phase 1's IR-excess `f_max`.
  - **Variable-depth detection is not optional.** BLS/TLS are optimised for *constant-depth* periodic
    boxes, but the highest-value signals (§1) — and a natural battery item, the disintegrating dust
    tail (KIC 12557548) — have transit depths that *fluctuate epoch-to-epoch*. A BLS-only trigger
    would down-weight or miss exactly the dynamic morphologies we most want to evaluate, blinding the
    search to its own stated priority. Detection therefore runs the variable-depth/aperiodic pass
    (single-event and depth-varying matched filters; cf. KIC 8462852) *alongside* BLS/TLS, with its
    own empirical-null calibration (§5).
  - **Morphology resolution is cadence-bounded (stated caveat).** Resolving Arnold-type ingress/egress
    asymmetry requires fine sampling: at TESS 2-minute cadence a ~2-hour transit's ingress is only a
    handful of points, so the subtlest non-spherical signatures are resolvable only for the brightest
    targets with 20-second cadence, long-duration transits, or deep events. The morphology channel's
    sensitivity is reported *as a function of cadence and transit duration*, not assumed uniform.
- **Channel P — photometric departure (SECONDARY).** Departures from the natural
  rotation/granulation/activity model; correlated/structured variability; same empirical-null
  calibration as Phase 1.
- **Channel A — infrared excess (CALIBRATED but weak; self-weighting + corroborating).** A K dwarf's
  cool IR photosphere suppresses excess contrast and debris disks are a common, *expected* natural
  explanation, so this channel is *weak* — but weak is not zero, and **we keep a calibrated `f_max`**
  (correcting an earlier draft that dropped it). The Phase-1 self-weighting math already handles the
  weakness exactly: inject a synthetic anomalous excess and measure per-star completeness C_i; where
  the photosphere swamps the signal (a cold, low-`f` anomaly) injection-recovery returns C_i ≈ 0 and
  that star contributes nothing to `f_max = 3/ΣC_i`, while a warm, luminous structure (e.g. 500 K at
  `f`=0.1) gives C_i ≈ 1 and a real constraint. The limit therefore *self-evaporates where the data
  are blind and stands where they are not* — dropping it pre-emptively would throw away a valid (if
  weak) upper limit on bright technological structures. We state plainly that this limit is inherently
  weaker than Phase 1's WD limit, and let ΣC_i show by how much. Natural debris disks are removed by
  the battery (SED regime + SIMBAD/literature cross-check), exactly as for white dwarfs.
  - **Corroborating extreme-outlier flag — with a *locked* threshold (coincidence multiplicity).**
    Separately from the `f_max`, Channel A contributes a high-bar flag for the *far tail* (an excess
    outside any natural regime, an anomalous SED shape, or a *fluctuating* excess a static disk cannot
    fake). Because we elevate a star when its IR flag **coincides** with a Channel-B transit anomaly,
    the intersection has its own multiplicity: with M Channel-B survivors and K Channel-A flags over N
    stars, the expected chance coincidences under the null are ≈ M·K/N. K must therefore be *locked
    before unblinding*, not chosen to manufacture a coincidence: the Channel-A flag fires at a fixed
    **> 4σ on the per-cohort IR empirical null**, which fixes K, so the expected false-coincidence
    rate M·K/N is pre-computed and registered here (with M held to ≈1 by the §5 FWER bar, a 4σ tail
    giving the joint chance rate ≪ 1). A surviving extreme IR excess *and* an anomalous transit on one
    K dwarf is then the high-value residual — far stronger than either channel alone, and now with a
    pre-registered false-alarm budget rather than an arbitrary one.

## 5. Natural-explanation battery, statistics, and stopping rule

A flagged candidate becomes a residual only if it survives every applicable test. The order is
deliberate: the cheapest, highest-yield contaminant filter runs *first and automatically*,
because at this sample size nothing can be vetted by hand.

0. **Background eclipsing binary / aperture blend — automated centroid gate (FIRST, mandatory).**
   TESS's ~21″ pixels guarantee that *hundreds* of off-target eclipsing binaries blend into
   K-dwarf apertures — the dominant transit false positive at scale. Difference-image
   centroiding (the flux-weighted centroid of the out-of-transit minus in-transit image) is run
   **automatically as the first gate**: a candidate whose dip centroid sits more than a pre-set
   tolerance (≈1 TESS pixel) from the target is killed with no human inspection. In Phase 1 this
   was a manual check on 3 candidates; here it is a mandatory, automated guillotine at the front
   of the battery.
1. **Eclipsing binary (on-target)** — fit EB models; check for a secondary eclipse, odd–even
   depth differences, ellipsoidal/reflection modulation; radial velocities where available.
2. **Stellar activity** — starspot rotational modulation, flares, faculae; cross-check against the
   star's rotation period and activity indicators.
3. **Bona-fide planet** — a real planet transit is *natural*; we flag only morphologies
   inconsistent with a spherical or ringed planet (noting the ringed-planet ambiguity of Arnold
   2005).
4. **Disintegrating planetesimal / dust tail** — tested by recurrence, depth evolution, and an
   explicit asymmetric dust-tail template (cf. WD 1145+017, KIC 12557548).
5. **Instrumental / systematic** — TESS/Kepler systematics, momentum dumps, scattered light,
   aperture contamination.

- **Detection threshold and the trial factor.** With tens of thousands of stars × ~10⁶ BLS
  period/phase trials each, a 3–4σ bar would bury the residual list in noise. We therefore
  compose two corrections, both pre-specified as *procedures* (the resulting numbers come from the
  data via those procedures, never from inspecting candidates):
  - **(a) Per-cohort empirical null — with an outlier-*blind* noise metric.** An empirical null on
    the per-star BLS detection statistic, computed *within noise/activity cohorts* (binned by each
    light curve's scatter / activity level) rather than globally — so a quiet star is judged against
    other quiet stars and the active stars' heavy-tailed noise (spots, flares, rotation) does **not**
    inflate the threshold for the clean ones. **The cohort-assignment noise metric is an
    outlier-blind robust estimator — the median absolute deviation (MAD) of the out-of-transit
    continuum after iterative σ-clipping of *downward* excursions (points > 3σ below the median are
    masked) — never the raw standard deviation or CDPP.** This is load-bearing: a genuine deep
    anomalous dip inflates a naïve variance, which would mis-bin that very star into a "noisy"
    cohort, raise its local threshold, and let the anomaly **mask itself**. Clipping the dips before
    measuring the baseline closes that data-leak. Within each cohort, genomic-control inflation λ
    rescales for the non-Gaussian reality of TESS/Kepler systematics (as the WISE-excess null did,
    λ≈10.6 in Phase 1); this per-cohort grading (the v2 W2-offset lesson, generalised) is what lets
    us keep every star above the youth floor without a hard activity cut.
  - **(b) One survey-wide family-wise (FWER) bar — a single framework, not a mix.** The threshold
    controls the expected number of pure-noise false alarms across the *entire frozen manifest* to
    **< 1** (cf. the Kepler 7.1σ bar, Jenkins et al. 2002, for ~150k stars), derived from **our own
    injection-recovery**, not borrowed — it depends on our sample size, cadence, and period range,
    and is expected to land in the **≈6–7σ regime**. Crucially we **do not compose mismatched
    error-control frameworks**: we control FWER, full stop; we do *not* also spend FDR against the
    same decision (FDR / Benjamini–Hochberg is used only to *rank-report* the surviving residual
    list, never to set the detection bar), and we do *not* spend alpha per tier — `N_total` is the
    fixed size of the immutable manifest (§3), not an open-ended census, so the bar is well-defined
    and set **once** for the whole population.
  - **(c) Calibrated up front from the whole manifest, then frozen.** Both the per-cohort nulls and
    the FWER bar are calibrated **once, from the noise floor of the *entire* manifest** — a cheap
    pass computing each star's robust scatter and BLS-null statistic, with **no transit search** —
    *before* any tier is searched. This is what makes the staged analysis (§3) statistically clean:
    because the cohorts and the bar are fixed from the whole population at the outset, analysing
    tiers in compute order cannot retrospectively shift the null or threshold a later tier sees (the
    "cohort clash" is closed). Only the transit search and injection-recovery are staged; the
    statistical calibration covers everything from the start. The bar is frozen before any real
    candidate tail is unblinded.
- **Upper limit (Channel B, now calibrated).** The Poisson zero-detection bound
  `f_max(depth, period) = 3 / Σ_i C_i`, with per-star completeness C_i(depth, period) measured by
  **injection-recovery of synthetic anomalous transits into the real light curves** — the same
  logic as Phase 1's IR-excess limit, now yielding a population constraint on structural transit
  anomalies as a function of depth and period.
- **Stopping rule (unchanged from Phase 1):** "unexplained" means "survives the registered
  battery at procedure-frozen thresholds," nothing more. We report the *full ranked residual
  list*, and the standing interpretation is that a residual is a target for conventional
  astrophysical follow-up — never, in this document or its outputs, a claim of detected
  intelligence.

## 6. Analysis plan

1. Freeze the sample → the immutable checksummed manifest (§3).
2. Pull TESS/Kepler light curves (deterministic recipe); detrend.
3. **Calibrate and freeze the thresholds before unblinding** — over the **whole manifest's** noise
   floor (every star's outlier-blind MAD scatter and BLS-null statistic; no transit search), fix the
   per-cohort empirical nulls and the single FWER-controlled detection bar; run injection-recovery
   to fix the per-star completeness C_i. Calibrating from the entire population up front (not from
   whatever tier is in hand) is what keeps the staged search clean. *This step touches only the
   noise floor and synthetic injections — never the real candidate tail.*
4. **Unblind:** run the BLS/TLS search, apply the frozen threshold, compute morphology metrics,
   and pass survivors through the natural-explanation battery (automated centroid gate first).
5. Report the full ranked residual list and the calibrated `f_max(depth, period)`.

Same recipe-in-repo, checksum, gitignored-bulk discipline as Phase 1. The split between steps 3
(noise-floor/synthetic calibration, thresholds frozen) and 4 (real candidates unblinded against
the frozen thresholds) is the integrity crux at this sample size: it is what prevents a strange
real signal from tempting a threshold tweak.

## 7. Outcomes and interpretation

- **Expected:** a clean, explained null plus a prevalence upper limit, with a byproduct catalogue
  of K-dwarf transit candidates and activity characterisation of value independent of the
  technosignature framing.
- **A surviving residual** is, in order of probability, a *previously-unmodelled natural*
  occulter or variability class — published as such, with all natural tests shown. A *fluctuating
  or structured* anomalous morphology would be the single highest-value outcome. No claim of
  artificiality is made on the basis of this pipeline.

## 8. Open science and reproducibility

Public repository; pinned data recipe, query text, frozen manifests, and checksums; bulk data
fetched on demand (gitignored). The analysis runs on the **validated population-agnostic core**
plus a new **K-dwarf plugin** — Phase 1 reused, not forked, with the WD regression test as a
standing guarantee that the shared core is unchanged. AI-collaboration transcripts archived.
Registered on OSF before any K-dwarf light curve is analysed; post-registration changes are
dated, public amendments.

## Statement of Provenance and Acknowledgments

**Human accountability.** Authored and directed by the sole investigator (T. Loewald), who bears
full responsibility for its contents, methodological selections, and errors. Special thanks are
owed to a cross-disciplinary collaborator whose insight — bringing the population-level
statistical standards of epidemiology and genome-wide association studies to bear on an
astrophysical problem — motivated the empirical-null and genomic-control framework this search
inherits from Phase 1.

**AI intellectual provenance.** Two AI systems (Google Gemini, Anthropic Claude) functioned as
active computational logic engines and co-designers in methodology, implementation, and
adversarial review; they are credited as such while the investigator retains all accountability.
The complete, lightly-redacted working transcripts are archived in the public repository.

## References

(Shared methodology references as Phase 1, plus transit-specific.)
- Arnold, L. F. A. 2005, *ApJ*, 627, 534 — artificial/ringed transit signatures.
- Kovács, G., Zucker, S., & Mazeh, T. 2002, *A&A*, 391, 369 — Box Least Squares.
- Hippke, M., & Heller, R. 2019, *A&A*, 623, A39 — Transit Least Squares.
- Boyajian, T. S., et al. 2016, *MNRAS*, 457, 3988 — KIC 8462852 (anomalous, structured transits).
- Vanderburg, A., et al. 2015, *Nature*, 526, 546 — disintegrating planetesimals at WD 1145+017.
- Borucki, W. J., et al. 2010, *Science*, 327, 977 — Kepler.
- Ricker, G. R., et al. 2015, *JATIS*, 1, 014003 — TESS.
- Jenkins, J. M., Caldwell, D. A., & Borucki, W. J. 2002, *ApJ*, 564, 495 — transit detection threshold.
- Efron, B. 2004, *JASA*, 99, 96 — empirical null. · Devlin & Roeder 1999, *Biometrics*, 55, 997 — genomic control.
- Gentile Fusillo, N. P., et al. 2021, *MNRAS*, 508, 3877 / Gaia Collaboration — sample provenance.
