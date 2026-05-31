# Pre-registration: An Anomaly-Residual Search for Signs of Persistence Around White Dwarfs

**Status:** Draft for pre-registration (Open Science Framework). This document is to be timestamped and frozen *before* any project-specific analysis of the target data is performed. Subsequent analysis code and data products will be developed in a public version-controlled repository whose commit history post-dates this registration.

**Date drafted:** 2026-05-31
**Authors:** Tonio Loewald (lead); contributors TBD
**Working repository:** (to be created — public GitHub)
**OSF registration DOI:** (to be assigned)

---

## 0. One-paragraph summary

We search catalogued white dwarfs for **persistent departures from the natural, well-modeled behavior of a cooling stellar remnant** — anomalies that resist explanation by known astrophysics — as an assumption-light test for the presence of something that has been *kept going* over deep time. We deliberately make **no assumptions about how such a thing would arise, what it would want, or what it would build**: we do not assume Dyson spheres, energy maximization, or thermodynamic-efficiency optimization. Our only assumptions concern physics and observability (§1.3). The method is **anomaly detection followed by adversarial natural explanation**: enumerate candidate anomalies, attempt to explain each away with a pre-specified battery of natural hypotheses, and report the residual that survives. **We expect a null result and treat it as a successful, publishable outcome** — it yields a quantitative upper bound on the prevalence of such anomalies around white dwarfs. We never claim an unexplained residual is evidence of intelligence; we claim only that it is unexplained, and we publish the residual catalogue.

---

## 1. What we are looking for, and what we refuse to assume

### 1.1 The target: persistence, not a mechanism

The thing we are searching for is the bare fact of **persistence** — evidence that something has been actively kept going for a very long time, on the order of billions of years. We take seriously that *we do not know how a long-lived civilization got there, what it is made of, what it wants, or what it builds.* Any search that presupposes those things is encoding a guess about alien psychology and technology that we have no basis to make.

What we *can* state without guessing is the physical signature of persistence in the abstract: a **maintained departure from equilibrium**. A dead system relaxes toward equilibrium and follows a predictable decay trajectory. Something doing sustained work to hold a configuration off that trajectory — whatever the means — shows up as a low-probability anomaly *against an otherwise well-understood background*. So the target signature is not a Dyson sphere, a waste-heat temperature, or any specific construct; it is **disequilibrium that should not still be present**, detected as a residual after natural explanations are exhausted.

This reframing dissolves a debate that earlier drafts of this project spent effort on — whether a mature civilization would optimize for thermodynamic *efficiency* (running cold, per Landauer's principle) or for *resilience* (running warm to power redundancy, sensing, and defense). **Both were mechanism hypotheses, and we adopt neither as a prior.** We retain the underlying physics only where it tells us what anomalies are physically *possible and detectable* — not as a prediction of what a civilization would do.

### 1.2 Assumptions we explicitly refuse to make

We list these to bind ourselves: none may re-enter the analysis as a hidden premise.

- **That a long-lived civilization builds megastructures / Dyson spheres** [as in Dyson 1960; Zuckerman 2022; Suazo et al. 2024]. We do not assume starlight is reprocessed into any particular signature.
- **That it maximizes energy throughput** (the Kardashev 1964 ordering). High gross power is one possibility, not an expectation.
- **That it optimizes for thermodynamic efficiency** and trends cold toward the CMB (the Landauer 1961 / aestivation [Sandberg, Armstrong & Ćirković 2017] logic). A specific operating temperature is not assumed.
- **That it optimizes for resilience** and therefore runs warm. Also a mechanism guess.
- **That it follows any particular developmental or technological path.** We assume nothing about how persistence is achieved.

These appear in §8's reference list and in §1.4 because they define the prior literature we are *departing from*, not premises we share.

### 1.3 Assumptions we do make (scope, not truth-claims about aliens)

A search with literally zero assumptions is unsearchable and unfalsifiable. The discipline is not "assume nothing" but "confine assumptions to *physics and observability*, never to alien psychology or technology." We make exactly the following, and we label them as the **domain of applicability** of this search rather than as claims about what is out there:

1. **Persistence requires a stable, long-lived platform.** Whatever persists for ~Gyr needs an energy/material environment stable on that timescale. White dwarfs are among the very few such platforms: they have no stellar dynamo, no flares, and cool along a slow, exceptionally well-modeled trajectory over tens of Gyr. *We do not assume a civilization would prefer or migrate to one* — only that, if persistence exists at all, a white dwarf is one of the few places it could be sustained and is observable.
2. **A well-modeled background makes anomalies legible.** Precisely because white-dwarf cooling, atmospheres, and debris processes are well understood [e.g. Farihi 2016], a genuine departure stands out cleanly. We are looking where the physics is best understood — "where the light is good."
3. **Maintained disequilibrium leaves an electromagnetic imprint in channels we already survey** — the spectral energy distribution, the transit/eclipse light curve, and the photospheric-accretion state. **This is a real limitation, stated up front: if persistence manifests through channels we do not survey, this search is blind to it.** We do not claim completeness; we claim a defined, falsifiable slice.

Everything downstream (the specific channels in §4) is a consequence of assumption 3 — i.e., *the list of places an anomaly could currently show up* — not an additional assumption about alien behavior.

**Why this assumes far less than mainstream SETI.** Classic radio SETI encodes a much *larger* technology assumption than ours: that a civilization radiates in a particular band, with particular structure, recognizable as artificial — i.e. that it builds and leaks the kind of beacon we happen to imagine. That premise fails precisely when the technology is not the one we pictured. A concrete illustration: our own present-day radio traffic — spread-spectrum, digitally encoded, frequently encrypted — would be largely indistinguishable from thermal noise to a 1970s receiver. "Assume-the-signal" searches are brittle in exactly this way. Our premise is weaker and degrades more gracefully: we assume only that *something* persists off the natural-decay trajectory and leaves *some* imprint in channels we already survey — not that it produces any specific, pre-imagined signature. We are not asking "does it look like our idea of a technology?" but "does it fail to look like known nature?"

### 1.4 Why we expect a null result

Independent of any of the above, we expect to find nothing:

- The catalogued white-dwarf sample is ~10⁵–10⁶ objects, not astronomically large.
- The intuition that intelligence is common rests on multiplying *point estimates* of highly uncertain Drake-equation factors. Propagating realistic *uncertainty distributions* instead places substantial probability mass on "we are effectively alone," dissolving the apparent paradox [Sandberg, Drexler & Ord 2018].
- The relevant quantity is not "did something ever persist here" but "is it present *at the epoch we observe this system*." Contemporaneity is a stringent filter against ~13.8 Gyr of cosmic time, making the per-system prior very small.

The scientifically valuable product is therefore the **upper bound** a clean null places on the prevalence of persistent anomalies around white dwarfs, plus a reusable, published anomaly catalogue with dispositions.

### 1.5 Relation to prior searches (what is and is not new)

Prior technosignature searches around white dwarfs and elsewhere share the mechanism assumption we drop:

- **Zuckerman (2022)** searched ~100 white dwarfs (Spitzer/WISE) for Dyson-sphere infrared excess and set an upper limit of <3% of habitable planets building detectably bright megastructures — assuming **warm** constructs at **300–1000 K**, which is *the natural debris-disk temperature regime*. The warm, most-confounded band is thus already partly constrained, under an explicit Dyson-sphere assumption.
- **Project Hephaistos** [Suazo et al. 2024] and related *Gaia*/2MASS/WISE surveys target main-sequence stars in the warm-excess regime, assuming partial Dyson spheres.
- **The Ĝ / G-HAT survey** [Wright et al. 2014a,b; Griffith et al. 2015; Wright et al. 2016] targets galaxy-scale (Kardashev III) mid-infrared waste heat.

**This project's distinct contributions:** (a) the target is **persistence/maintained-disequilibrium, mechanism-agnostic**, not an assumed construct; (b) an explicit **anomaly-residual methodology** with a pre-registered natural-explanation battery, rather than assume-a-signature-and-set-a-limit; (c) coverage of anomaly channels and temperature bands *outside* the already-constrained warm-Dyson regime; and (d) **pre-registration plus an open, version-controlled pipeline.**

---

## 2. Research questions and hypotheses

Registered in anomaly-residual form. None is phrased as "we will detect intelligence," and none assumes a mechanism.

- **RQ1 (SED channel).** Do any catalogued white dwarfs show a spectral-energy-distribution anomaly — most legibly an infrared excess from a re-radiating component, scanned across a broad temperature band — not accounted for by the natural-explanation battery (§5)?
- **RQ2 (light-curve channel).** Do any show transit/eclipse morphologies inconsistent with spherical, natural occulters (asymmetric, irregular, flat-bottomed/square-wave, or anomalously deep) after natural alternatives are excluded?
- **RQ3 (accretion-state channel).** Do any photospherically polluted (actively accreting) white dwarfs show an anomalously *clean* inner zone — a maintained departure from the expected debris behavior — after natural clearing mechanisms are excluded?
- **RQ4 (primary deliverable, holds regardless of RQ1–3).** What quantitative upper limit does the (expected) null result place on the prevalence of such anomalies around white dwarfs, as a function of the assumed signal properties (e.g. excess temperature and covering fraction) — i.e. the detectability envelope of the search?

**Primary registered prediction:** the residual surviving the full natural-explanation battery is statistically consistent with zero. Any surviving residual is reported as *unexplained*, flagged for independent astrophysical follow-up, and explicitly **not** asserted to be artificial or intelligent.

---

## 3. Sample / sampling plan (frozen target list)

- **Parent catalogue.** White-dwarf candidates from *Gaia* EDR3 [Gentile Fusillo et al. 2021]: 1,280,266 sources with a white-dwarf probability *P*_WD; ~359,000 high-confidence candidates at *P*_WD > 0.75. (Early project notes' "~200,000" corresponds to the older *Gaia* DR2 catalogue; we adopt EDR3 and state the cut explicitly.)
- **Registered selection cut.** *P*_WD > 0.75 as the primary high-confidence sample, full *P*_WD distribution retained for sensitivity tests. Additional registered quality cuts (parallax S/N, photometric quality flags, Galactic-latitude / reddening limits to control cold-dust confusion) to be fixed in the final registration version **before** any cross-match to infrared data.
- **Frozen manifest.** The exact source list (*Gaia* source IDs) and all thresholds will be committed as an immutable, checksummed manifest at registration time. No post-hoc additions/removals except via a documented, dated amendment.
- **Cross-match targets.** WISE/NEOWISE (and, where available, Spitzer, 2MASS, far-IR archives) at frozen coordinates; TESS light curves for the filtered subset; JWST/MIRI archival or proposed follow-up for high-residual candidates only.

---

## 4. Anomaly channels and their detectability

These are **the channels in which a maintained departure could currently show up**, given existing surveys — *not* predictions that persistence produces any particular signature. Each is a characterization tool applied *after* anomaly flagging, paired with its natural-explanation tests in §5.

### Channel A — Spectral-energy-distribution anomaly (infrared excess)
A re-radiating component would distort the otherwise simple cooling-blackbody SED of a bare white dwarf. **Anomaly:** a suppressed expected SED with an added IR component at some blackbody temperature, scanned as a free parameter. Natural debris disks occupy ~300–1000 K [Farihi 2016]; a cold component (e.g. tens of K) would sit *below* that regime and be less confounded — but, **stated as a limitation,** a ~30 K blackbody peaks near ~100 µm (far-IR), so WISE's longest band (W4, 22 µm) samples only its Wien tail. We therefore treat the excess temperature as a **scanned free parameter**, report sensitivity vs. temperature explicitly, note the warm end is already partly constrained [Zuckerman 2022], and reserve the cold, clean band for far-IR / JWST-MIRI sensitivity assessment rather than over-claiming WISE coverage.

### Channel B — Transit / eclipse light-curve morphology
The white-dwarf circumstellar zone is tight (~0.005–0.02 AU [Agol 2011]), giving hours-to-days periods, and white dwarfs are ~Earth-sized, so an occulter can block a large light fraction — cf. the first transiting white-dwarf planet WD 1856+534 b [Vanderburg et al. 2020]. **Anomaly:** asymmetric, irregular, flat-bottomed/square-wave, or anomalously deep transits inconsistent with a spherical body [Arnold 2005; Wright et al. 2016], in the methodological spirit of (but not assuming the conclusion of) the KIC 8462852 anomaly [Boyajian et al. 2016].

### Channel C — Accretion-state / inner-zone anomaly
Many white dwarfs show photospheric metal pollution from ongoing debris accretion [Farihi 2016]. **Anomaly:** a polluted (actively accreting) system that nonetheless shows an anomalously *clean* inner zone — a maintained departure from expected debris behavior. We register that this channel is the hardest to quantify and the most prone to natural explanation; it is treated as corroborating, not stand-alone, evidence.

---

## 5. Natural-explanation battery (the core of the method)

An anomaly-residual search is only as strong as the alternatives we attempt *first*. We register the following non-exhaustive battery; each candidate anomaly must survive rejection by **every** applicable test to enter the residual, and each threshold is fixed at registration.

For **Channel A (IR excess):**
1. Natural circumstellar **debris disk** (300–1000 K dust) — tested by SED temperature and shape.
2. **Unresolved cool companion** (late-M / brown-dwarf / second WD) — tested by SED, color, and where possible astrometry/RV.
3. **Background/foreground cold-dust (cirrus) contamination** — tested by local far-IR background, beam-confusion checks, angular-resolution cross-checks.
4. **Photometric/calibration artifacts and blends** — tested by survey quality flags, epoch consistency (NEOWISE), PSF/contamination flags.
5. **CMB / instrumental confusion at the cold limit** — assessed as a sensitivity boundary, not a detection.

For **Channel B (light curves):**
6. **Spherical/ringed planet or eclipsing-binary** geometries — tested by fitting natural models, including the ringed-planet ambiguity noted by Arnold (2005).
7. **Stellar/instrumental variability, pulsation, systematics** — tested against TESS systematics and known WD variability classes.
8. **Transiting debris / disintegrating planetesimals** (a known WD phenomenon) — tested by recurrence, evolution, accompanying pollution.

For **Channel C (clean inner zone):**
9. **Natural dynamical clearing** (sublimation radius, Poynting–Robertson drag, resonances, recent disruption) — tested against disk-evolution models.
10. **Selection/sensitivity effects** mimicking cleanliness — tested by injection-recovery.

**Stopping rule and residual definition.** "Unexplained" means "survives the registered battery at the registered thresholds," nothing more. We pre-commit to: (a) a fixed battery (amendments require a dated, public amendment); (b) an explicit **anomaly/residual score** per object quantifying how much signal survives each test; (c) reporting the *full ranked residual catalogue*, not only top candidates; and (d) the standing interpretation that the residual is a list of objects warranting conventional astrophysical follow-up — never, in this document or its outputs, a claim of detected intelligence. This guards against the god-of-the-gaps failure mode in which "unexplained" silently becomes "the current limit of our models."

---

## 6. Analysis plan

1. Freeze sample and manifest (§3); commit checksums.
2. Cross-match to WISE/NEOWISE (+ Spitzer/2MASS/far-IR where available); build SEDs.
3. Fit each SED to (a) bare-WD cooling models and (b) the natural alternatives of §5; compute IR-excess significance and best-fit excess temperature across the scanned band.
4. **Injection-recovery / sensitivity characterization:** inject synthetic excesses across the scanned temperature band and recover them, producing the detectability-vs-temperature curve underwriting the RQ4 upper limit. Run on synthetic signals only, so thresholds are never tuned on real anomalies.
5. For the IR-flagged subset, retrieve and vet TESS light curves against the Channel-B battery.
6. For polluted systems, evaluate the Channel-C clean-zone test.
7. Compute per-object anomaly/residual scores; assemble the ranked residual catalogue.
8. Derive the prevalence upper limit (RQ4) as a function of signal properties, given sample size and recovered sensitivity.
9. JWST/MIRI follow-up reserved for surviving high-residual candidates; **not** part of the registered statistical sample.

**Discipline against post-hoc reasoning:** thresholds, the battery, and the scoring rule are fixed in this document before step 2. Sensitivity (step 4) uses injected synthetic signals so detection thresholds are not tuned to real outliers. Any deviation is recorded as a dated amendment with rationale; the public git history provides an independent timeline.

---

## 7. What counts as a result

- **Null (expected):** no object survives the natural-explanation battery. **Outcome:** publish the prevalence upper limit (RQ4) and the full residual catalogue with dispositions. A complete, successful result.
- **Surviving residual — most likely a new *natural* phenomenon:** one or more objects survive the battery. The highest-probability interpretation of any survivor is **not** life but **previously unmodeled natural astrophysics** — e.g. an unknown mechanism by which a remnant or companion stays warm, an unmodeled disk or accretion process, or a new variability/occultation class. This is treated as a primary, valued outcome in its own right: the residual catalogue has scientific worth as a list of *objects current models do not explain*, independent of how any one of them ultimately resolves. **Outcome:** publish survivors as *unexplained anomalies warranting independent astrophysical follow-up*, with all natural tests shown. No claim of artificiality or intelligence is made on the basis of this pipeline.

In none of these branches does success depend on detecting anything intelligent. The deliverables are a reusable anomaly catalogue and a quantitative constraint — useful to stellar-remnant and debris-disk astrophysics whether or not the technosignature framing ever pays off.

---

## 8. Open-science commitments

- This pre-registration is timestamped on OSF before project-specific data analysis.
- All code, queries, the frozen sample manifest, the natural-explanation battery implementation, and the residual catalogue are released in a public GitHub repository whose history post-dates registration.
- Amendments are public, dated, and rationale-bearing; superseded versions are retained.

---

## References

*(Verified against primary sources during drafting unless marked “[verify]”. References to mechanism-assuming prior work are cited as the literature we depart from, per §1.2/§1.5, not as shared premises.)*

- Agol, E. 2011, "Transit Surveys for Earths in the Habitable Zones of White Dwarfs," *ApJL* 731, L31. arXiv:1103.2791
- Arnold, L. F. A. 2005, "Transit Lightcurve Signatures of Artificial Objects," *ApJ* 627, 534. arXiv:astro-ph/0503580
- Boyajian, T. S., et al. 2016, "Planet Hunters IX. KIC 8462852 — Where's the Flux?," *MNRAS* 457, 3988. arXiv:1509.03622
- Dyson, F. J. 1960, "Search for Artificial Stellar Sources of Infrared Radiation," *Science* 131, 1667. doi:10.1126/science.131.3414.1667
- Farihi, J. 2016, "Circumstellar debris and pollution at white dwarf stars," *New Astronomy Reviews* 71, 9. arXiv:1604.03092
- Gentile Fusillo, N. P., et al. 2021, "A catalogue of white dwarfs in *Gaia* EDR3," *MNRAS* 508, 3877. arXiv:2106.07669
- Griffith, R. L., et al. 2015, "The Ĝ Infrared Search for Extraterrestrial Civilizations with Large Energy Supplies. III.," *ApJS* 217, 25.
- Kardashev, N. S. 1964, "Transmission of Information by Extraterrestrial Civilizations," *Soviet Astronomy* 8, 217. [verify exact page]
- Landauer, R. 1961, "Irreversibility and Heat Generation in the Computing Process," *IBM J. Res. Dev.* 5, 183. doi:10.1147/rd.53.0183
- Sandberg, A., Armstrong, S., & Ćirković, M. M. 2017, "That is not dead which can eternal lie: the aestivation hypothesis for resolving Fermi's paradox," *JBIS* / arXiv:1705.03394
- Sandberg, A., Drexler, E., & Ord, T. 2018, "Dissolving the Fermi Paradox," arXiv:1806.02404
- Suazo, M., et al. 2024, "Project Hephaistos – II. Dyson sphere candidates from *Gaia* DR3, 2MASS, and WISE," *MNRAS* 531, 695. arXiv:2405.02927
- Vanderburg, A., et al. 2020, "A giant planet candidate transiting a white dwarf," *Nature* 585, 363. (WD 1856+534 b)
- Wright, J. T., Mullan, B., Sigurdsson, S., & Povich, M. S. 2014a, "The Ĝ Infrared Search … I. Background and Justification," *ApJ* 792, 26. arXiv:1408.1133
- Wright, J. T., et al. 2014b, "… II. Framework, Strategy, and First Result," *ApJ* 792, 27. arXiv:1408.1134
- Wright, J. T., et al. 2016, "… IV. The Signatures and Information Content of Transiting Megastructures," *ApJ* 816, 17. arXiv:1510.04606
- Zuckerman, B. 2022, "Infrared and optical detectability of Dyson spheres at white dwarf stars," *MNRAS* 514, 227. arXiv:2204.09627

**Standard mission/instrument references to add:** *Gaia* mission (Gaia Collaboration 2016; EDR3 2021); WISE (Wright, E. L., et al. 2010, *AJ* 140, 1868); NEOWISE (Mainzer et al. 2011); TESS (Ricker et al. 2015, *JATIS* 1, 014003); JWST/MIRI (Rieke et al. 2015). *[mission refs to be confirmed before final registration]*
