# An Anomaly-Residual Search for Unexplained Thermal and Photometric Signatures Around White Dwarfs

*Pre-registration. A mechanism-agnostic technosignature search — motivated by, but not presupposing, long-lived intelligence.*

**Status:** Draft for pre-registration (Open Science Framework). This document is to be timestamped and frozen *before* any project-specific analysis of the target data is performed. Subsequent analysis code and data products will be developed in a public version-controlled repository whose commit history post-dates this registration.

**Date drafted:** 2026-05-31
**Investigator:** Tonio Loewald (sole investigator)
**Drafting assistance:** Google Gemini and Anthropic Claude (tools, not authors; see Acknowledgments)
**Working repository:** https://github.com/tonioloewald/seti (private until registration, then public)
**License:** code Apache-2.0; documents and data products CC-BY-4.0
**OSF registration DOI:** (to be assigned)

---

## 0. One-paragraph summary

We search catalogued white dwarfs for **anomalous departures — static or time-varying — from the natural, well-modeled behavior of a cooling stellar remnant**: signatures that resist explanation by known astrophysics. The *motivating* question is whether anything has been actively *kept going* over deep time, but we treat that as motivation only — the target we actually measure is the anomaly, not a presupposed persister. We deliberately make **no assumptions about how such a thing would arise, what it would want, or what it would build**: we do not assume Dyson spheres, energy maximization, or thermodynamic-efficiency optimization. Our only assumptions concern physics and observability (§1.3). Among anomalies, we flag **fluctuating or structured-variable ones as the highest-value class** — a static surprise tends to resolve into new equilibrium physics, whereas a dynamic one implies ongoing activity and is far harder to explain away. The method is **anomaly detection followed by adversarial natural explanation**: enumerate candidate anomalies, attempt to explain each away with a pre-specified battery of natural hypotheses, and report the residual that survives. **We expect a null result and treat it as a successful, publishable outcome** — it yields a quantitative upper bound on the prevalence of such anomalies around white dwarfs. We never claim an unexplained residual is evidence of intelligence; we claim only that it is unexplained, and we publish the residual catalogue.

---

## 1. What we are looking for, and what we refuse to assume

### 1.1 The target: an anomalous departure from nature — not a presupposed persister

Our *motivation* is the possibility of **persistence** — that something has been actively kept going for a very long time, on the order of billions of years. But persistence is a *hypothesis about a cause*, and it presupposes a persister; it is therefore **not** our target. We take seriously that *we do not know how a long-lived civilization got there, what it is made of, what it wants, or what it builds* — any search that presupposes those things encodes a guess about alien psychology and technology we have no basis to make. So the thing we actually search for and measure is the **observable anomaly**, and we stay agnostic about whether anything is persisting behind it.

What we *can* state without guessing is the physical signature in the abstract: a **departure from equilibrium that nature does not explain** — whether *static* (a configuration held off the decay trajectory) or, more tellingly, *dynamic* (a fluctuating or structured-variable departure). A dead system relaxes toward equilibrium along a predictable decay trajectory; a low-probability anomaly stands out against that well-understood background. The target signature is not a Dyson sphere, a waste-heat temperature, or any specific construct; it is **disequilibrium that should not be present**, detected as a residual after natural explanations are exhausted. We weight the **dynamic** case most heavily: a static anomaly is degenerate with an unmodeled steady-state — science tends to absorb it as new equilibrium physics — whereas a *fluctuating, structured* anomaly implies ongoing **work** (a system *doing* something, not merely *being* in an odd state), which is both harder to write off naturally and closer to the operational signature of active maintenance. (The grip of KIC 8462852 was precisely its *irregular, aperiodic* dimming; a steady dip would have been filed under "disk" at once.)

This reframing dissolves a debate that earlier drafts of this project spent effort on — whether a mature civilization would optimize for thermodynamic *efficiency* (running cold, per Landauer's principle) or for *resilience* (running warm to power redundancy, sensing, and defense). **Both were mechanism hypotheses, and we adopt neither as a prior.** We retain the underlying physics only where it tells us what anomalies are physically *possible and detectable* — not as a prediction of what a civilization would do.

### 1.2 Assumptions we explicitly refuse to make

We list these to bind ourselves: none may re-enter the analysis as a hidden premise.

- **That a long-lived civilization builds megastructures / Dyson spheres** [as in Dyson 1960; Zuckerman 2022; Suazo et al. 2024]. We do not assume starlight is reprocessed into any particular signature.
- **That it maximizes energy throughput** (the Kardashev 1964 ordering). High gross power is one possibility, not an expectation.
- **That it optimizes for thermodynamic efficiency** and trends cold toward the CMB (the Landauer 1961 / aestivation [Sandberg, Armstrong & Ćirković 2017] logic). A specific operating temperature is not assumed.
- **That it optimizes for resilience** and therefore runs warm. Also a mechanism guess.
- **That it follows any particular developmental or technological path.** We assume nothing about how persistence is achieved.

These appear in the References and in §1.5 because they define the prior literature we are *departing from*, not premises we share.

### 1.3 Assumptions we do make (scope, not truth-claims about aliens)

A search with literally zero assumptions is unsearchable and unfalsifiable. The discipline is not "assume nothing" but "confine assumptions to *physics and observability*, never to alien psychology or technology." We make exactly the following, and we label them as the **domain of applicability** of this search rather than as claims about what is out there:

1. **Persistence requires a stable, long-lived platform.** Whatever persists for ~Gyr needs an energy/material environment stable on that timescale. White dwarfs are among the very few such platforms: they have no stellar dynamo, no flares, and cool along a slow, exceptionally well-modeled trajectory over tens of Gyr. *We do not assume a civilization would prefer or migrate to one* — only that, if persistence exists at all, a white dwarf is one of the few places it could be sustained and is observable.
2. **A well-modeled background makes anomalies legible.** Precisely because white-dwarf cooling, atmospheres, and debris processes are well understood [e.g. Farihi 2016], a genuine departure stands out cleanly. We are looking where the physics is best understood — "where the light is good."
3. **An anomalous disequilibrium (static or time-varying) leaves an electromagnetic imprint in channels we already survey** — the spectral energy distribution and its variation across epochs, the transit/eclipse light curve, and the photospheric-accretion state. **This is a real limitation, stated up front: if persistence manifests through channels we do not survey, this search is blind to it.** We do not claim completeness; we claim a defined, falsifiable slice.

Everything downstream (the specific channels in §4) is a consequence of assumption 3 — i.e., *the list of places an anomaly could currently show up* — not an additional assumption about alien behavior.

**Why this assumes far less than mainstream SETI.** Classic radio SETI encodes a much *larger* technology assumption than ours: that a civilization radiates in a particular band, with particular structure, recognizable as artificial — i.e. that it builds and leaks the kind of beacon we happen to imagine. That premise fails precisely when the technology is not the one we pictured. A concrete illustration: our own present-day radio traffic — spread-spectrum, digitally encoded, frequently encrypted — would be largely indistinguishable from thermal noise to a 1970s receiver. "Assume-the-signal" searches are brittle in exactly this way. Our premise is weaker and degrades more gracefully: we assume only that *something* persists off the natural-decay trajectory and leaves *some* imprint in channels we already survey — not that it produces any specific, pre-imagined signature. We are not asking "does it look like our idea of a technology?" but "does it fail to look like known nature?"

### 1.4 Why we expect a null result

Independent of any of the above, we expect to find nothing:

- The catalogued white-dwarf sample is ~10⁵–10⁶ objects, not astronomically large.
- The intuition that intelligence is common rests on multiplying *point estimates* of highly uncertain Drake-equation factors. Propagating realistic *uncertainty distributions* instead places substantial probability mass on "we are effectively alone," dissolving the apparent paradox [Sandberg, Drexler & Ord 2018].
- The relevant quantity is not "did something ever persist here" but "is it present *at the epoch we observe this system*." Contemporaneity is a stringent filter against ~13.8 Gyr of cosmic time, making the per-system prior very small.

The scientifically valuable product is therefore the **upper bound** a clean null places on the prevalence of unexplained anomalies around white dwarfs, plus a reusable, published anomaly catalogue with dispositions.

### 1.5 Relation to prior searches (what is and is not new)

Prior technosignature searches around white dwarfs and elsewhere share the mechanism assumption we drop:

- **Zuckerman (2022)** searched ~100 white dwarfs (Spitzer/WISE) for Dyson-sphere infrared excess and set an upper limit of <3% of habitable planets building detectably bright megastructures — assuming **warm** constructs at **300–1000 K**, which is *the natural debris-disk temperature regime*. The warm, most-confounded band is thus already partly constrained, under an explicit Dyson-sphere assumption.
- **Project Hephaistos** [Suazo et al. 2024] and related *Gaia*/2MASS/WISE surveys target main-sequence stars in the warm-excess regime, assuming partial Dyson spheres.
- **The Ĝ / G-HAT survey** [Wright et al. 2014a,b; Griffith et al. 2015; Wright et al. 2016] targets galaxy-scale (Kardashev III) mid-infrared waste heat.

**This project's distinct contributions:** (a) the target is an **anomalous departure from the natural model (static or time-varying), mechanism-agnostic**, not an assumed construct; (b) an explicit **anomaly-residual methodology** with a pre-registered natural-explanation battery, rather than assume-a-signature-and-set-a-limit; (c) coverage of anomaly channels and temperature bands *outside* the already-constrained warm-Dyson regime; and (d) **pre-registration plus an open, version-controlled pipeline.**

---

## 2. Research questions and hypotheses

Registered in anomaly-residual form. None is phrased as "we will detect intelligence," and none assumes a mechanism.

- **RQ1 (SED channel, static and time-varying).** Do any catalogued white dwarfs show a spectral-energy-distribution anomaly — most legibly an infrared excess from a re-radiating component, scanned across a broad temperature band — *and/or anomalous time-variability of that excess across multi-epoch (NEOWISE) photometry* — not accounted for by the natural-explanation battery (§5)?
- **RQ2 (light-curve channel).** Do any show transit/eclipse morphologies inconsistent with spherical, natural occulters (asymmetric, irregular, flat-bottomed/square-wave, or anomalously deep) after natural alternatives are excluded?
- **RQ3 (accretion-state channel).** Do any photospherically polluted (actively accreting) white dwarfs show an anomalously *clean* inner zone — a maintained departure from the expected debris behavior — after natural clearing mechanisms are excluded?
- **RQ4 (primary deliverable, holds regardless of RQ1–3).** What quantitative upper limit does the (expected) null result place on the prevalence of such anomalies around white dwarfs, as a function of the assumed signal properties (e.g. excess temperature and covering fraction) — i.e. the detectability envelope of the search?

**Primary registered prediction:** the residual surviving the full natural-explanation battery is statistically consistent with zero. Any surviving residual is reported as *unexplained*, flagged for independent astrophysical follow-up, and explicitly **not** asserted to be artificial or intelligent.

---

## 3. Sample / sampling plan (frozen target list)

**Parent catalogue.** White-dwarf candidates from *Gaia* EDR3 [Gentile Fusillo et al. 2021]: 1,280,266 sources with a white-dwarf probability *P*_WD; ~359,000 high-confidence candidates at *P*_WD > 0.75. (Early project notes' "~200,000" corresponds to the older *Gaia* DR2 catalogue; we adopt EDR3.)

**Inclusion is by data sufficiency, not distance.** The search targets the white-dwarf data we actually have. That data set is *naturally* volume-limited by detectability — faint, distant white dwarfs tend to lack adequate photometry — but we impose **no hard distance or brightness horizon**: a distant white dwarf is included if, and only if, its data are good enough to run the test. The frozen inclusion gate is:

1. **`P_WD > 0.75`** — high-confidence white dwarf (this already encodes *Gaia* astrometric confidence).
2. **Astrometric / photometric quality recorded, never an exclusion gate.** Poor solutions are *not* cut: high RUWE or a failed single-star astrometric fit is routed to the natural-explanation battery (unresolved companion / blend, item 2), and poor photometry simply enlarges the SED errors and lowers that object's sensitivity (`C_i`). This avoids the anomaly-hunter's trap — an asymmetric occulter or a shifted photocenter can itself spoil a standard single-star *Gaia* solution, so gating on "sane flags" would preferentially discard the extreme objects we are hunting.
3. **Photospheric baseline constrained** — Teff determinable to a registered tolerance from the optical/near-IR SED (the photosphere against which any IR excess is measured). This is a *data-sufficiency* rule, **not** a distance cut: it admits any white dwarf with adequate optical/NIR photometry regardless of distance, and replaces the cruder parallax-S/N cut considered earlier.
4. **At least one informative IR constraint** — a detection *or* a catalogued flux upper limit in ≥1 mid-IR band (WISE W1–W4 / Spitzer), so the object can contribute either a measurement or a bound.

No white dwarf meeting these is excluded for being far away. Objects whose data cannot constrain the test contribute ~zero effective sensitivity (see below) and drop out *harmlessly*, without a hard cut.

**Inherited selection (stated limitation).** The parent catalogue is itself constructed from *Gaia* astrometry and photometry, so an object whose signal entirely breaks *Gaia*'s solution may be missing from our sample *upstream*, before any rule of ours applies. Recovering such cases would require working from raw *Gaia* epoch data and is outside this registration's scope; we flag it as a known blind spot rather than claim completeness.

**Completeness is per-object (the consequence).** Because sensitivity varies object-to-object, the search assumes **no single uniform completeness**. Each object's detectability `C_i(T_x, Ω)` is measured by injection-recovery against *its own* photometry and local noise (§5.3), and the population upper limit sums these per-object sensitivities (§5.7). Every white dwarf then contributes exactly as much as its data afford — the standard heterogeneous-sensitivity occurrence-rate approach, and a direct implementation of "use everything, exclude nothing arbitrarily."

**Selection bias toward the solar neighborhood (stated limitation).** No hard distance cut is applied, but the data-sufficiency rules (a well-constrained optical/NIR SED; ≥1 informative IR band) preferentially admit nearby, bright, and/or hot white dwarfs — a strong Malmquist-type bias toward the local volume. The per-object `C_i` framework handles this *statistically* (under-probed objects self-weight toward zero), so the upper limit stays formally valid; but its *interpretation* is scoped accordingly — `f_max` constrains prevalence among the **effectively probed, neighborhood-weighted population**, not the full Galactic white-dwarf census. We state this directly to preempt sample-completeness objections.

**Contamination.** A moderate reddening ceiling removes only the worst cirrus fields; residual cold-dust confusion is handled per object via the local far-IR background (battery item 3) — per-object vetting in preference to aggressive pre-cuts.

**Frozen manifest.** The exact source list (*Gaia* source IDs) and all inclusion-rule parameters are committed as an immutable, checksummed manifest at registration. No post-hoc additions/removals except via a dated, public amendment.

**Cross-match targets.** WISE/NEOWISE (+ Spitzer/2MASS/far-IR where available) at frozen coordinates; TESS light curves for the filtered subset; JWST/MIRI archival or proposed follow-up for high-residual candidates only.

---

## 4. Anomaly channels and their detectability

These are **the channels in which an anomalous departure could currently show up**, given existing surveys — *not* predictions that persistence produces any particular signature. Each is a characterization tool applied *after* anomaly flagging, paired with its natural-explanation tests in §5.

Cutting across all three is the **time domain**, which we treat as a first-class dimension: per §1.1 a *fluctuating or structured-variable* anomaly is the highest-value signature, so each channel tests not only for a static departure but, where multi-epoch data exist, for anomalous *variability* of it. The channels probe **complementary temporal regimes** and we do not mix them: Channel A samples long-baseline, low-cadence variability (≈months–years, via NEOWISE's ~6-month visit clusters), while Channel B samples short-baseline, high-cadence morphology (≈minutes–days, within a TESS sector). We do not attempt to extract high-cadence signal from sparse NEOWISE epochs, nor year-scale trends from a single 27-day TESS sector. The honest catch — spelled out per channel below — is that our time-domain coverage is thinnest exactly where the signal would be most exciting (the cold IR band).

### Channel A — Spectral-energy-distribution anomaly (infrared excess)
A re-radiating component would distort the otherwise simple cooling-blackbody SED of a bare white dwarf. **Anomaly:** a suppressed expected SED with an added IR component at some blackbody temperature, scanned as a free parameter. Natural debris disks are typically warm — roughly a few ×100 K up to ~1000 K [Farihi 2016] (the operational boundary is derived empirically, not hard-coded; §5.2 item 1); a cold component (e.g. tens of K) would sit *below* that regime and be less confounded — but, **stated as a limitation,** a ~30 K blackbody peaks near ~100 µm (far-IR), so WISE's longest band (W4, 22 µm) samples only its Wien tail. We therefore treat the excess temperature as a **scanned free parameter**, report sensitivity vs. temperature explicitly, note the warm end is already partly constrained [Zuckerman 2022], and reserve the cold, clean band for far-IR / JWST-MIRI sensitivity assessment rather than over-claiming WISE coverage. **Time-variability:** beyond the static excess, we test whether the excess itself *varies* across NEOWISE's decade of multi-epoch sampling — a *structured* variation being far harder to attribute to nature (§5.3). Crucially, that multi-epoch sampling exists only in **W1/W2** (3.4/4.6 µm, probing *warm* excess); the cold-relevant W3/W4 bands have only the single cryogenic 2010 epoch, so a *fluctuating cold* excess — the most diagnostic signal of all — is essentially **unobservable with existing all-sky IR data**, and stands as a primary motivation for the follow-up/extensibility clause (§5.4).

### Channel B — Transit / eclipse light-curve morphology
The white-dwarf circumstellar zone is tight (~0.005–0.02 AU [Agol 2011]), giving hours-to-days periods, and white dwarfs are ~Earth-sized, so an occulter can block a large light fraction — cf. the first transiting white-dwarf planet WD 1856+534 b [Vanderburg et al. 2020]. **Anomaly:** asymmetric, irregular, flat-bottomed/square-wave, or anomalously deep transits inconsistent with a spherical body [Arnold 2005; Wright et al. 2016], in the methodological spirit of (but not assuming the conclusion of) the KIC 8462852 anomaly [Boyajian et al. 2016].

### Channel C — Accretion-state / inner-zone anomaly
Many white dwarfs show photospheric metal pollution from ongoing debris accretion [Farihi 2016]. **Anomaly:** a polluted (actively accreting) system that nonetheless shows an anomalously *clean* inner zone — a maintained departure from expected debris behavior. We register that this channel is the hardest to quantify and the most prone to natural explanation; it is treated as corroborating, not stand-alone, evidence.

---

## 5. The natural-explanation battery and the anomaly score

An anomaly-residual search is only as strong as the alternatives we attempt *first*. The battery below is the set of natural hypotheses we fit to each object; the **anomaly score is the badness-of-fit of the best natural model** — how poorly the data are explained once nature has been given its best shot. "Anomalous" means "even the best natural explanation fits badly," never "looks unusual to us."

### 5.1 Frozen-procedures principle: register the rule, not the number

We commit to a principle that governs every threshold in this section:

> **The *procedure* that computes each cutoff is frozen here; the *numeric value* it yields is computed at analysis time from external or whole-sample data, reported, and may not be altered after inspecting individual candidates.**

This reconciles two things that look opposed: pre-registration (so we cannot tune toward a result) and not prematurely hard-coding numbers before we have seen any data. We freeze meta-parameters and recipes (e.g. the false-discovery setting, the margin used to define a natural regime, the calibration method); the data then determine the actual flux/score/temperature cutoffs. The only move pre-registration forbids — and the one this principle blocks — is choosing or sliding a cutoff so that a *particular object* falls inside or outside it. Every cutoff must be a deterministic function of (a frozen rule) applied to (external or bulk-sample data, not the individual candidates).

### 5.2 The registered battery of natural alternatives

Each candidate anomaly must survive rejection by **every** applicable test to enter the residual.

For **Channel A (IR excess):**
1. Natural circumstellar **debris disk** — tested by SED temperature and shape. The natural-disk temperature region is **not** a hard-coded "300–1000 K"; per §5.1 it is derived from the observed temperature distribution of *known* white-dwarf debris disks (external data) plus a registered margin. **Natural disks also vary in time** (collisional events, disk-state transitions), so this hypothesis is the natural explanation tested against any observed IR *variability* (§5.3), not only against a static excess.
2. **Unresolved cool companion** (late-M / brown-dwarf / second WD) — tested against an empirical M/L/T-dwarf SED library, plus color and (where possible) astrometry/RV. **Brown-dwarf companions are intrinsically variable in the mid-IR** (rotational "weather" — patchy silicate clouds rotating in and out of view, on hours-to-years baselines), so this hypothesis is also the natural explanation tested against observed IR *variability* (§5.3), not only against a static color.
3. **Background/foreground cold-dust (cirrus) contamination** — tested by local far-IR background, beam-confusion checks, angular-resolution cross-checks.
4. **Photometric/calibration artifacts and blends** — tested by survey quality flags, epoch consistency (NEOWISE), PSF/contamination flags.
5. **CMB / instrumental confusion at the cold limit** — assessed as a sensitivity boundary, not a detection.

For **Channel B (light curves):**
6. **Spherical/ringed planet or eclipsing-binary** geometries — tested by fitting natural occulter models (Mandel–Agol transit; EB), including the ringed-planet ambiguity noted by Arnold (2005).
7. **Stellar/instrumental variability, pulsation, systematics** — tested against TESS systematics and known WD variability classes.
8. **Transiting debris / disintegrating planetesimals** (a known WD phenomenon that produces *genuinely asymmetric, variable* transits) — tested by recurrence, evolution, accompanying pollution, and an explicit dust-tail template.
9. **Background eclipsing binary (BEB) / aperture blend** — TESS pixels are ~21″ and white dwarfs are intrinsically faint, so a deep dip recorded in a white-dwarf aperture is *a priori* far more likely a background eclipsing binary blended into the pixel than an event on the white dwarf itself. **This is the dominant Channel-B false positive.** Tested by mandatory **difference-image / photocentroid analysis**: the flux drop must be localized to the white dwarf's coordinates, not an offset background source within the aperture.

For **Channel C (clean inner zone):**
10. **Natural dynamical clearing** (sublimation radius, Poynting–Robertson drag, resonances, recent disruption) — tested against disk-evolution models.
11. **Selection/sensitivity effects** mimicking cleanliness — tested by injection-recovery.

### 5.3 Channel A — the calibrated IR-excess score (primary channel)

For each white dwarf we fit a nested set of models to the assembled SED:
- **H₀** — bare WD photosphere. Teff/log g from [Gentile Fusillo et al. 2021]; synthetic photometry from a DA/DB atmosphere grid (Koester / Bergeron). In the WISE bands the photosphere lies on the Rayleigh–Jeans tail, so its predicted flux is stiff and low-uncertainty.
- **H_disk**, **H_comp** — the natural add-ons of §5.2 items 1–2 (flat opaque dust disk, after Jura 2003; empirical companion SED).
- **H_anom** — photosphere + a *free-temperature* blackbody excess (temperature *T*_x and solid angle Ω both free, *T*_x allowed from a few K through and beyond the disk regime). This agnostic component can fit any excess shape, including a cold one outside every natural regime.

**Two-stage statistic.**
1. *Excess present?* `Δχ²(H₀ → H_anom)` must exceed the flagging threshold (no excess ⇒ no anomaly).
2. *Can nature explain it?* The score is `A = χ²(best of {H_disk, H_comp}) − χ²(H_anom)` — i.e. how much better the agnostic excess fits than the best **natural** model. If a natural disk or companion fits as well as the free blackbody, `A ≈ 0` (natural, not anomalous). If the data demand an excess whose temperature/shape sits *outside* the natural regimes, the natural models fit far worse → large `A`. Reported alongside `A`: the best-fit *T*_x and its credible interval, and whether that interval falls outside the union of natural regimes (a large `A` whose *T*_x lands *inside* the disk regime is just a good disk detection, not an anomaly).

**Time-variability statistic — an independent gate.** Variability is tested **in parallel with** the static excess, *not* conditioned on it: an object enters the natural-explanation battery if it shows a static excess (above) **or** anomalous multi-epoch variability. This matters because a *transient or episodic* anomaly (e.g. an intermittent IR flare) can average back to the photospheric baseline over a decade and leave **no** static excess, so a variability check gated behind static detection would be blind to it. We compute a per-object **variability statistic** on the multi-epoch NEOWISE W1/W2 photometry — excess scatter and structure beyond the photometric-noise model *and* beyond both natural sources of intrinsic IR variability: the disk variability of §5.2 item 1 (collisions, disk-state transitions) *and the rotational atmospheric ("weather") variability of cool/brown-dwarf companions in §5.2 item 2*. A *structured* (non-stochastic) variation is the highest-value flag (§1.1). The variability statistic is calibrated by the **same empirical-null + Benjamini–Hochberg FDR machinery** as the static score (below). It is constrained in **W1/W2 only**; the cold W3/W4 band is single-epoch, so cold-excess variability is not testable with existing data and is deferred to follow-up (§4.A, §5.4). The variability gate feeds the residual in parallel and is reported separately from the static-excess upper limit (§5.7).

**Censored likelihood (the subtlety that matters most).** The cold regime appears only in W3/W4, where most white dwarfs are undetected. All fits treat WISE non-detections as proper **upper limits** via a censored likelihood, never as zeros or missing data. Crucially, those same W3/W4 bands are contaminated by Galactic **cirrus** (cold interstellar dust), and an upper limit is only valid if that background is modeled: the censored likelihood therefore carries a **local far-IR background-variance term** (estimated from the surrounding field and external cirrus maps). Where the local cirrus is too bright or too variable to set a clean limit, the object's sensitivity **degrades gracefully to `C_i → 0`** — it contributes *no* constraint rather than a spuriously tight one, the same self-weighting that handles distance (§3). Mishandling any of this is the easiest way to manufacture or erase a cold excess, and it is why the cold band is detectability-limited (§4.A): there, the honest product is largely an upper limit, not a detection.

**Calibration — the empirical null (primary).** Rather than trusting textbook χ² p-values (which assume the error bars and noise model are exactly right — they are not), we let the population define "normal": since ~all ~10⁵ objects are natural, the distribution of `A` across the whole sample is approximately its null distribution, automatically absorbing real-world error-bar imperfections. We flag objects in the extreme tail beyond that empirical null. *(Rationale: this search deliberately probes under-examined regimes from a new angle; inheriting a predefined notion of "normal" would smuggle others' assumptions back in. A handful of genuine signals cannot bias the curve when ~10⁵ ordinary objects define it.)* Theoretical χ² significance is retained only as a cross-check. Independently, **injection–recovery** of synthetic excesses (natural and anomalous, across *T*_x, Ω) into real photometry sets the completeness function `C(T_x, Ω)` and confirms the empirical-null thresholds; it runs on synthetic signals only, so thresholds are never tuned on real outliers.

**Multiple testing.** With ~10⁵ trials we control false flags via **Benjamini–Hochberg FDR** on the per-object natural-inexplicability p-values at a frozen setting *q* (the frozen *number* per §5.1; the resulting score cutoff is computed from the data). Consistent with our completeness-favoring choice, *q* is set permissively to yield a finite candidate list we vet by hand, and a separate strict high-significance subset is also reported.

### 5.4 Channel B — light-curve morphology (secondary, extensible)

In principle Channel B mirrors Channel A: detect events (BLS/TLS on TESS), fit the natural occulter set (§5.2 items 6–9, including the dust-tail template **and a mandatory background-eclipsing-binary / centroid-offset check**), and score the residual against a flexible phenomenological model, with registered morphology flags (ingress/egress asymmetry, secondary structure, depth vs. implied radius). Every Channel-B candidate must pass difference-image centroiding to confirm the signal originates at the white dwarf's coordinates rather than a blended background source (item 9). **But** white dwarfs are faint (G ≈ 15–20) and TESS is photon-starved on them, so light-curve coverage is non-uniform and often poor. We therefore register Channel B as a **secondary, candidate-generating channel with manual/physical vetting — not** a calibrated channel from which a population upper limit is claimed; promising such a limit would assert a precision the current data do not support. This demotion is a statement about **data, not importance**: the time domain is where a *fluctuating* anomaly — our highest-value signature (§1.1) — would appear most clearly, which is precisely why expanding time-domain coverage (next clause) is the project's highest-leverage future step.

**Extensibility clause.** This framework anticipates better time-domain data becoming available later — e.g. ZTF, ground-based white-dwarf transit surveys, or targeted follow-up that Channel-A candidates may themselves motivate. Upgrading Channel B to a calibrated channel, or adding *any* new data source, is done via a **dated, public amendment that pre-registers the new analysis before that data is examined**, per §5.1 and §8. The project may thus grow opportunistically (including chance discoveries) without ever analyzing new data outside a locked plan.

### 5.5 Channel C — clean inner zone (corroborating only)

"Accreting but no detectable inner dust" is common and has known natural explanations (optically-thin or gas-only disks, recently-fully-accreted events — an open natural puzzle in its own right). Channel C is therefore registered as an **ordinal corroborating flag with no standalone detection threshold**; it elevates an object only when it coincides with a Channel-A or -B survivor on the same target.

### 5.6 Combining channels, residual definition, and stopping rule

The channels are heterogeneous and many objects lack data in some of them, so we **do not** define a single mandatory weighted scalar (the place where arbitrary, tunable weights would creep in). We register instead:
- **Primary residual and upper limit:** Channel A alone (calibrated, FDR-controlled) — an object enters via a static-excess survival *or* an independent variability survival (§5.3).
- **Secondary candidate list:** Channel B survivors (for follow-up).
- **Corroboration:** Channel C flags, only when coincident with A/B.
- A combined rank may be reported as a clearly-defined *secondary* product (e.g. multi-channel coincidences first); the registered primary analysis keeps channels separate.

**Stopping rule and residual definition.** "Unexplained" means "survives the registered battery at the procedure-frozen thresholds (§5.1)," nothing more. We pre-commit to: (a) a fixed battery and fixed threshold-setting procedures (changes require a dated, public amendment); (b) the explicit per-object anomaly score above; (c) reporting the *full ranked residual catalogue*, not only top candidates; and (d) the standing interpretation that the residual is a list of objects warranting conventional astrophysical follow-up — never, in this document or its outputs, a claim of detected intelligence. This guards against the god-of-the-gaps failure mode in which "unexplained" silently becomes "the current limit of our models."

### 5.7 From anomaly score to the §2/RQ4 upper limit

A clean null in Channel A yields, as a function of the injected anomaly properties, the standard zero-detection Poisson bound

`f_max(T_x, Ω) ≈ 3.0 / Σ_i C_i(T_x, Ω)`  (95% one-sided; 0 events → 3.0),

summed over every included object *i*, where `C_i` is that object's own injection-recovery completeness (§3, §5.3). Each white dwarf contributes exactly its own sensitivity — distant or poorly-measured objects contribute little, nearby well-measured ones contribute ≈1 — so no object is excluded by fiat and none is over-counted. (The uniform-sample form `f_max ≈ 3.0/(N_eff·C̄)` is just the special case where all `C_i` are equal.) This is the headline result for the expected null: *"fewer than f_max of white dwarfs host a standing cold IR-excess of temperature T_x and covering fraction Ω."*

---

## 6. Analysis plan

1. Freeze sample and manifest (§3); commit checksums.
2. Cross-match to WISE/NEOWISE (+ Spitzer/2MASS/far-IR where available); build SEDs.
3. Fit each SED to (a) bare-WD cooling models and (b) the natural alternatives of §5; compute IR-excess significance and best-fit excess temperature across the scanned band.
4. **Injection-recovery / sensitivity characterization:** inject synthetic excesses across the scanned temperature band and recover them, producing the detectability-vs-temperature curve underwriting the RQ4 upper limit. Run on synthetic signals only, so thresholds are never tuned on real anomalies.
5. For the IR-flagged subset, retrieve and vet TESS light curves against the Channel-B battery.
6. For polluted systems, evaluate the Channel-C clean-zone test.
7. Compute per-object anomaly/residual scores; assemble the ranked residual catalogue.
8. Derive the prevalence upper limit (RQ4) as a function of signal properties, summing the per-object recovered sensitivities (§5.7).
9. JWST/MIRI follow-up reserved for surviving high-residual candidates; **not** part of the registered statistical sample.

**Discipline against post-hoc reasoning:** the battery, the scoring rule, and the threshold-*setting procedures* (§5.1) are fixed in this document before step 2; the numeric thresholds they yield are computed at analysis time from external or whole-sample data and may not be altered after inspecting individual candidates. Sensitivity (step 4) uses injected synthetic signals so detection thresholds are not tuned to real outliers. Any deviation, and any added data source (§5.4), is recorded as a dated public amendment with rationale; the public git history provides an independent timeline.

---

## 7. What counts as a result

- **Null (expected):** no object survives the natural-explanation battery. **Outcome:** publish the prevalence upper limit (RQ4) and the full residual catalogue with dispositions. A complete, successful result.
- **Surviving residual — most likely a new *natural* phenomenon:** one or more objects survive the battery. The highest-probability interpretation of any survivor is **not** life but **previously unmodeled natural astrophysics** — e.g. an unknown mechanism by which a remnant or companion stays warm, an unmodeled disk or accretion process, or a new variability/occultation class. This is treated as a primary, valued outcome in its own right: the residual catalogue has scientific worth as a list of *objects current models do not explain*, independent of how any one of them ultimately resolves. Among survivors, a **fluctuating or structured-variable** anomaly would be the single highest-value outcome — hardest of all to attribute to a static unmodeled equilibrium, and the closest to a signature of activity (§1.1). **Outcome:** publish survivors as *unexplained anomalies warranting independent astrophysical follow-up*, with all natural tests shown. No claim of artificiality or intelligence is made on the basis of this pipeline.

In none of these branches does success depend on detecting anything intelligent. The deliverables are a reusable anomaly catalogue and a quantitative constraint — useful to stellar-remnant and debris-disk astrophysics whether or not the technosignature framing ever pays off.

---

## 8. Open-science commitments

- This pre-registration is timestamped on OSF before project-specific data analysis.
- All code, queries, the frozen sample manifest, the natural-explanation battery implementation, and the residual catalogue are released in a public GitHub repository whose history post-dates registration.
- **Amendments are public, dated, and rationale-bearing; superseded versions are retained** (logged in `AMENDMENTS.md`). We distinguish two kinds and label every result accordingly: *pre-data amendments* — refinements to the frozen plan made **before** any real target data is analyzed (e.g. from ongoing expert review), which remain fully **confirmatory**; and *post-data changes* — anything decided **after** real data has been seen, which are flagged **exploratory / post-hoc** and never presented as confirmatory. Both the immutable OSF registration timestamp and the public git history fix which is which; **pre-data amendments are registered as formal Updates to the OSF Registration** — OSF's native, immutable update mechanism — alongside the human-readable `AMENDMENTS.md` log. Because git history is mutable (force-push), the OSF Updates are the *authoritative* immutable record; the git log and a force-push-protected `main` branch are the companion record, not the sole authority. This pre-registration is deliberately frozen *before* feedback-gathering is complete, so that expert review arriving later enters as transparent pre-data amendments rather than silent edits.

---

## Acknowledgments

This pre-registration was authored by the investigator (T. Loewald) with substantial drafting and analysis-design assistance from two AI systems used as tools — Google Gemini and Anthropic Claude (via Claude Code). They are acknowledged here, not credited as authors: all scientific judgments, the choice of methods, and responsibility for the contents rest with the investigator. The design was developed iteratively and will be reviewed by domain experts before registration.

---

## References

*(All references verified against primary sources. References to mechanism-assuming prior work are cited as the literature we depart from, per §1.2/§1.5, not as shared premises.)*

- Agol, E. 2011, "Transit Surveys for Earths in the Habitable Zones of White Dwarfs," *ApJL* 731, L31. arXiv:1103.2791
- Arnold, L. F. A. 2005, "Transit Lightcurve Signatures of Artificial Objects," *ApJ* 627, 534. arXiv:astro-ph/0503580
- Boyajian, T. S., et al. 2016, "Planet Hunters IX. KIC 8462852 — Where's the Flux?," *MNRAS* 457, 3988. arXiv:1509.03622
- Dyson, F. J. 1960, "Search for Artificial Stellar Sources of Infrared Radiation," *Science* 131, 1667. doi:10.1126/science.131.3414.1667
- Farihi, J. 2016, "Circumstellar debris and pollution at white dwarf stars," *New Astronomy Reviews* 71, 9. arXiv:1604.03092
- Gentile Fusillo, N. P., et al. 2021, "A catalogue of white dwarfs in *Gaia* EDR3," *MNRAS* 508, 3877. arXiv:2106.07669
- Griffith, R. L., et al. 2015, "The Ĝ Infrared Search for Extraterrestrial Civilizations with Large Energy Supplies. III.," *ApJS* 217, 25.
- Kardashev, N. S. 1964, "Transmission of Information by Extraterrestrial Civilizations," *Soviet Astronomy* 8, 217–221. (ADS 1964SvA.....8..217K)
- Landauer, R. 1961, "Irreversibility and Heat Generation in the Computing Process," *IBM J. Res. Dev.* 5, 183. doi:10.1147/rd.53.0183
- Sandberg, A., Armstrong, S., & Ćirković, M. M. 2017, "That is not dead which can eternal lie: the aestivation hypothesis for resolving Fermi's paradox," *JBIS* / arXiv:1705.03394
- Sandberg, A., Drexler, E., & Ord, T. 2018, "Dissolving the Fermi Paradox," arXiv:1806.02404
- Suazo, M., et al. 2024, "Project Hephaistos – II. Dyson sphere candidates from *Gaia* DR3, 2MASS, and WISE," *MNRAS* 531, 695. arXiv:2405.02927
- Vanderburg, A., et al. 2020, "A giant planet candidate transiting a white dwarf," *Nature* 585, 363. (WD 1856+534 b)
- Wright, J. T., Mullan, B., Sigurdsson, S., & Povich, M. S. 2014a, "The Ĝ Infrared Search … I. Background and Justification," *ApJ* 792, 26. arXiv:1408.1133
- Wright, J. T., et al. 2014b, "… II. Framework, Strategy, and First Result," *ApJ* 792, 27. arXiv:1408.1134
- Wright, J. T., et al. 2016, "… IV. The Signatures and Information Content of Transiting Megastructures," *ApJ* 816, 17. arXiv:1510.04606
- Zuckerman, B. 2022, "Infrared and optical detectability of Dyson spheres at white dwarf stars," *MNRAS* 514, 227. arXiv:2204.09627

**Mission and instrument papers** (verified):

- Gaia Collaboration (Prusti, T., et al.) 2016, "The Gaia mission," *A&A* 595, A1. doi:10.1051/0004-6361/201629272
- Gaia Collaboration (Brown, A. G. A., et al.) 2021, "Gaia Early Data Release 3: Summary of the contents and survey properties," *A&A* 649, A1. doi:10.1051/0004-6361/202039657
- Mainzer, A., et al. 2011, "Preliminary Results from NEOWISE: An Enhancement to the Wide-field Infrared Survey Explorer for Solar System Science," *ApJ* 731, 53.
- Rieke, G. H., et al. 2015, "The Mid-Infrared Instrument for the James Webb Space Telescope, I: Introduction," *PASP* 127, 584. doi:10.1086/682252
- Ricker, G. R., et al. 2015, "Transiting Exoplanet Survey Satellite (TESS)," *JATIS* 1, 014003.
- Wright, E. L., et al. 2010, "The Wide-field Infrared Survey Explorer (WISE): Mission Description and Initial On-orbit Performance," *AJ* 140, 1868.
