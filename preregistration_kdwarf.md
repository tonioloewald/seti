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
  excluding subgiants/giants), with clean astrometry (RUWE < 1.4, parallax_over_error > 10).
  *Scale (this repository, sized pre-data):* ~12,600 at G < 11; ~22,000 within 100 pc; ~178,000
  at G < 13. Target finding is not the binding constraint.
- **Data-quality / channel requirement.** A usable TESS and/or Kepler light curve (the transit
  instrument). The Kepler-field subset (4-year continuous photometry) is the morphology gold
  standard and is treated as a distinct, deepest tier.
- **Old / quiet weighting (the life-prior + the cleanliness criterion).** A pre-specified
  selection toward old, magnetically-quiet stars, via rotation-period gyrochronology where
  available, low flare rate, low photometric activity amplitude, and thick-disk-leaning
  kinematics. Exact thresholds are fixed from the *activity/rotation distributions of the parent
  sample*, before any transit search — never tuned to candidates.
- No assumption that an anomaly orbits in a habitable zone; all periods the data permit are
  searched.
- **Stated selection biases:** brightness-limited (toward nearby), the TESS/Kepler footprint, and
  the old/quiet cut. `f_max` is interpreted as a prevalence among the *effectively probed,
  old-quiet-weighted, solar-neighbourhood* K-dwarf population.

## 4. Channels

- **Channel B — transit morphology (PRIMARY).** BLS/TLS detection; morphology metrics (asymmetry,
  flat-bottom fraction, box-vs-U, duty cycle); and **mandatory difference-image centroid /
  background-eclipsing-binary vetting**. The Phase-1 machinery transfers directly: K dwarfs are
  point sources with clean Gaia astrometry, and a real occulter gives a *deep* transit, so the
  "deep ⇒ on-target real; shallow-and-offset ⇒ background blend, confirmed by centroiding" logic
  applies (the same code validated for white dwarfs, `pipeline/analysis/07–09`).
- **Channel P — photometric departure (SECONDARY).** Departures from the natural
  rotation/granulation/activity model; correlated/structured variability; same empirical-null
  calibration as Phase 1.
- **Channel A — infrared excess (TERTIARY, weak).** Retained for completeness (WISE/CatWISE), but
  with the explicit caveat that a K dwarf's cool IR photosphere suppresses excess contrast; this
  is *not* the primary instrument here.

## 5. Natural-explanation battery, statistics, and stopping rule

A flagged candidate becomes a residual only if it survives every applicable test:

1. **Eclipsing binary** (the dominant transit false positive) — fit EB models; check for a
   secondary eclipse, odd–even depth differences, ellipsoidal/reflection modulation; radial
   velocities where available.
2. **Background eclipsing binary / aperture blend** — mandatory difference-image centroiding: the
   flux dip must localise to the K dwarf, not an offset source in the aperture.
3. **Stellar activity** — starspot rotational modulation, flares, faculae; cross-check against the
   star's rotation period and activity indicators.
4. **Bona-fide planet** — a real planet transit is *natural*; we flag only morphologies
   inconsistent with a spherical or ringed planet (noting the ringed-planet ambiguity of Arnold
   2005).
5. **Disintegrating planetesimal / dust tail** — tested by recurrence, depth evolution, and an
   explicit asymmetric dust-tail template (cf. WD 1145+017, KIC 12557548).
6. **Instrumental / systematic** — TESS/Kepler systematics, momentum dumps, scattered light,
   aperture contamination.

- **Thresholds** come from the empirical null (Efron 2004) with genomic-control inflation
  (Devlin & Roeder 1999), FDR control (Benjamini–Hochberg / Storey), and a staged look-elsewhere
  correction (Gross & Vitells 2010) carried to a Kepler-style high-significance bar (Jenkins et
  al. 2002) — all set by **injection-recovery, not candidate inspection**.
- **Upper limit:** the Poisson zero-detection bound `f_max = 3 / Σ_i C_i`, with per-star
  completeness C_i from injection-recovery of anomalous occulters across depth and period.
- **Stopping rule (unchanged from Phase 1):** "unexplained" means "survives the registered
  battery at procedure-frozen thresholds," nothing more. We report the *full ranked residual
  list*, and the standing interpretation is that a residual is a target for conventional
  astrophysical follow-up — never, in this document or its outputs, a claim of detected
  intelligence.

## 6. Analysis plan

Freeze sample + manifest → pull TESS/Kepler light curves (deterministic recipe) → detrend →
BLS/TLS search → morphology metrics → natural-explanation battery → empirical-null calibration →
`f_max`. Same recipe-in-repo, checksum, gitignored-bulk discipline as Phase 1.

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
