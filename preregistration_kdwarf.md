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
  Applied in two pre-specified stages: a coarse Gaia-only proxy in the manifest (kinematics; Gaia
  photometric-variability amplitude), refined before the transit search by rotation-period
  gyrochronology and activity indicators (GALEX, ROSAT/eROSITA, Ca II) where catalogued. Thresholds
  are fixed from the parent-sample distributions, never tuned to candidates.
- **No hard "quiet" cut — noisy stars self-weight.** Rather than excluding active stars, we include
  every star above the youth floor and let the per-star injection-recovery completeness C_i (§5) do
  the work: a transit is harder to recover in an active light curve, so a noisy star earns a low
  C_i and contributes little to `f_max` automatically (the Phase-1 self-weighting principle —
  under-probed objects weight toward zero). The limit stays honest over whatever has been analysed.
- **Resource-triggered, nested, staged analysis order (so iteration stays confirmatory).** Because
  the goal is everything and the binding constraint is compute, we pre-register a *nested* sequence
  of tiers (cleanest/brightest first: T₁ ⊂ T₂ ⊂ … ⊂ the full sample), analysed in that fixed order,
  with the expansion trigger being *available resources*, declared in advance — never the result of
  a prior tier. The survey-wide trial-factor / family-wise threshold (§5) is recomputed for each
  expanded sample (alpha-spending across stages). Growing the sample is therefore a pre-registered
  confirmatory extension (cf. the Phase-1 variability expansion), not a post-hoc tweak; what is
  forbidden is loosening any boundary *in reaction to a result* or to rescue a candidate.
- No assumption that an anomaly orbits in a habitable zone; all periods the data permit are
  searched.
- **Stated selection biases:** brightness-limited (toward nearby), the TESS/Kepler footprint, and
  the youth floor. `f_max` is interpreted as a prevalence among the *effectively probed,
  solar-neighbourhood* K-dwarf population, self-weighted by per-star completeness.

## 4. Channels

- **Channel B — transit morphology (PRIMARY, CALIBRATED).** BLS/TLS detection; morphology metrics
  (asymmetry, flat-bottom fraction, box-vs-U, duty cycle); and a **mandatory automated
  difference-image centroid gate** (§5). The Phase-1 machinery transfers directly: K dwarfs are
  point sources with clean Gaia astrometry, and a real occulter gives a *deep* transit, so the
  "deep ⇒ on-target real; shallow-and-offset ⇒ background blend, confirmed by centroiding" logic
  applies (the same code validated for white dwarfs, `pipeline/analysis/07–09`). Crucially, the
  sample size — tens of thousands versus Phase 1's 157 — **graduates this from a secondary,
  candidate-generating channel into a primary, calibrated one**: it now supports a rigorous
  population-level upper limit on structural transit anomalies (RQ3, §5), the transit analogue of
  Phase 1's IR-excess `f_max`.
- **Channel P — photometric departure (SECONDARY).** Departures from the natural
  rotation/granulation/activity model; correlated/structured variability; same empirical-null
  calibration as Phase 1.
- **Channel A — infrared excess (CORROBORATING; extreme-outlier only, no standalone limit).** A
  K dwarf's cool IR photosphere suppresses excess contrast, and debris disks are a common,
  *expected* natural explanation — so this channel is toothless for *marginal* signals and carries
  **no calibrated `f_max`**. Following the Phase-1 Channel-C precedent (an ordinal corroborating
  flag with no standalone threshold), it is registered as a **high-bar extreme-outlier flag**: the
  empirical null, calibrated against the disk-rich bulk, flags only the *far tail* — an excess
  outside any natural disk/companion regime, an anomalous SED shape, or (highest value) a
  *fluctuating* excess that a static disk cannot fake. Every flag is cross-checked against SIMBAD /
  the literature / known debris-disk catalogues and the already-explained ones killed (prior
  knowledge used as a *filter*, never as an assumption that the tail is empty). A surviving extreme
  excess **elevates an object only when it coincides with a Channel-B transit anomaly on the same
  star** — that coincidence (an otherwise-inexplicable IR excess *and* an anomalous transit on one
  K dwarf) is the high-value residual, far stronger than either channel alone.

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
  data via those procedures, never from inspecting candidates): **(a)** an **empirical null on the
  per-star BLS detection statistic, computed *within noise/activity cohorts*** (binned by each
  light curve's photometric scatter / CDPP / activity level) rather than globally — so a quiet star
  is judged against other quiet stars and the active stars' heavy-tailed noise (spots, flares,
  rotation) does **not** inflate the threshold for the clean ones. This per-cohort grading (the
  lesson from the v2 W2-offset handling, generalised) is what lets us keep every star above the
  youth floor without a hard activity cut: within each cohort, genomic-control inflation λ rescales
  for the non-Gaussian reality of TESS/Kepler systematics — as the WISE-excess null did (λ≈10.6 in
  Phase 1). And **(b)** a
  **survey-wide family-wise / look-elsewhere correction** (Gross & Vitells 2010; FDR, Benjamini–
  Hochberg / Storey) such that the expected number of pure-noise false alarms across the *entire
  frozen sample* is < 1. The resulting threshold is expected to land in the **≈6–7σ regime** (cf.
  the Kepler 7.1σ bar, Jenkins et al. 2002, for ~150k stars) — but it is **derived from our own
  injection-recovery on the frozen sample, not borrowed from Kepler**, since it depends on our
  sample size, cadence, and period range. It is frozen before the real candidate tail is unblinded.
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
3. **Calibrate and freeze the thresholds before unblinding** — run the empirical-null calibration
   on the bulk BLS-statistic distribution (the noise floor, not the candidate tail) and the
   injection-recovery on the frozen sample to fix the family-wise-controlled detection threshold
   and the per-star completeness C_i. *This step touches only the noise floor and synthetic
   injections — never the real candidate tail.*
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
