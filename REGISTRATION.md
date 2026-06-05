# Registration plan and decisions

This note records the deliberate choices around registering this pre-registration, so the reasoning is archived alongside the work (consistent with the open-science commitments in [`preregistration.md`](preregistration.md) §8).

## Narrative summary (OSF registration field)

This project grows out of a frustration with how much credence the Fermi Paradox and its descendants — the Dark Forest, the Kardashev scale, the Dyson sphere — still command. These frameworks measure intelligence with a human-shaped ruler, and specifically the growth-and-conquest assumptions of 19th-century industrial expansionism, projecting a parochial set of values onto minds that, if they exist and have *endured*, may share none of them. Strip those assumptions away and a sharper question remains: how and where could we credibly detect a civilization that has actually persisted for billions of years?

That reframing motivates the search registered here. Rather than assume what an enduring intelligence would *build* (a Dyson sphere, maximal energy use, thermodynamic efficiency), we make no assumptions about its mechanism or psychology and instead look for the only thing it must produce to be detectable at all: an **anomaly** — a departure from the well-modelled natural behaviour of a system — that resists every natural explanation we can throw at it. The target is white dwarfs (among the few platforms stable on billion-year timescales, and exceptionally well-modelled, so anomalies stand out cleanly), cross-matching open survey data (Gaia, WISE/NEOWISE, TESS, with JWST/MIRI for follow-up). The pipeline is an "anomaly-residual" search: flag candidate infrared-excess, time-variability, and transit anomalies, attempt to explain each away with a pre-registered battery of natural hypotheses, and report the residual. The statistics are borrowed from large-scale simultaneous inference in genomics and epidemiology (empirical-null calibration, false-discovery control) and from astronomy's own detection conventions (the look-elsewhere effect; the Kepler 7.1σ threshold). We expect — and would be content with — a null result: it yields a quantitative upper limit, and the residual catalogue of unexplained objects is valuable as new natural astrophysics regardless of any technosignature interpretation.

**How this differs from prior work.** Existing technosignature searches assume a mechanism: Zuckerman (2022) searched white dwarfs for Dyson-sphere infrared excess, but only in the *warm* (~300–1000 K) regime that overlaps natural debris disks; Project Hephaistos and the Ĝ/G-HAT survey similarly presuppose partial Dyson spheres. This registration instead (a) is mechanism-agnostic, defining its target as an unexplained departure from the natural model rather than an assumed construct; (b) extends into the colder and *time-varying* regimes those searches leave unprobed; and (c) freezes its statistical procedures before any data is analysed. To my knowledge no one has approached white-dwarf data this way.

The idea took shape through extended discussion with Google Gemini, and was developed with heavy use of both Gemini and Anthropic Claude to compensate for gaps and rustiness in my own knowledge. In keeping with that, the complete development transcripts are published with the project, and the AI systems' substantive role is documented in the registration's Statement of Provenance.

## Route: OSF Open-Ended Registration (unmoderated)

We register via the Open Science Framework's **Open-Ended Registration**, not a structured template (e.g. the social-science "Preregistration" form). Reasons:

- The structured templates are built around hypothesis-testing studies in psychology and clinical research, and fit a custom observational-astronomy methodology poorly.
- Open-Ended Registration creates an immutable, timestamped snapshot with a **DOI** — exactly what is needed to anchor "the plan was fixed before any data was analyzed."
- It is **unmoderated**: the registration is created directly, with no moderator gate. (Moderation applies only when submitting to specific moderated registries.)

The registration is created **public**, with no embargo.

## Timing: register before reviews are complete

We register **before** the investigator's final read-through and the domain-expert reviews are finished. This is deliberate and does not compromise integrity, because the invariant that matters is:

> No analysis of real target data occurs before the plan is frozen and registered.

Registration timestamps the plan. Any change that arrives afterward — from the investigator's own review, from domain experts (an ANU emeritus and an active astrophysicist), or from the one method still marked for refinement (the Stage-2 trial-factor estimator, §5.3) — enters as a **pre-data amendment**: dated, public, and *confirmatory*, because no real data has been touched. Post-data changes, by contrast, are flagged exploratory. That distinction (§8, and [`AMENDMENTS.md`](AMENDMENTS.md)) is what keeps "register early, improve in the open" honest.

## The provenance stand

The Statement of Provenance (`preregistration.md`) describes the two AI systems used — Google Gemini and Anthropic Claude — as **co-designers** and active logic engines, not merely tools: an accurate account of their functional role, with the complete (lightly-redacted) transcripts published in [`docs/transcripts/`](docs/transcripts/).

We are aware this exceeds current academic boilerplate, which designates AI strictly as a non-author tool. We retain the accountability designation in full — the investigator bears 100% of responsibility — but decline to let that necessary designation stand as a *description* of what happened. If a moderated venue ever rejects the work on the grounds of this honesty, the rejection (and any OSF tombstone) becomes part of the record: OSF registrations are never erased, only withdrawn-with-tombstone. We accept that trade.

## What is immutable

Two independent, public, timestamped records secure this work:

1. The **OSF registration** (DOI below) — a frozen snapshot; never deletable, only withdrawable-with-tombstone.
2. This **public Git repository** — branch-protected `main` (no force-push, no deletion), whose commit history independently timestamps the entire development.

## Status

- Pre-registration: **registered on OSF, 2026-06-01.**
- OSF: <https://osf.io/6yh7r> · DOI **10.17605/OSF.IO/6YH7R** — registration **accepted and live**; the public Git repository is linked from the OSF project, and post-registration amendments are tracked there (`AMENDMENTS.md`) with the authoritative timeline in the git history.
- Registered-version git tag: **`registered-1.0` → commit `005ef88`** — the exact `preregistration.md` and `REGISTRATION.md` submitted to OSF. Everything after it is a dated pre-data amendment.

---

# Phase 2 — Main-Sequence K Dwarfs

Phase 2 ([`preregistration_kdwarf.md`](preregistration_kdwarf.md)) is a **new, separate** OSF Open-Ended Registration (its own DOI), linked to this same public repository and cross-referencing the Phase-1 DOI. It is *not* an amendment to Phase 1: the sample (living K dwarfs), the primary channel (transit morphology), and the upper limit (per morphology family) are new. It reuses the Phase-1 **validated population-agnostic pipeline core** (regression-tested in [`pipeline/runners/validate_wd.py`](pipeline/runners/validate_wd.py)) via a new K-dwarf plugin — reused, not forked.

## Narrative summary (OSF registration field)

This is Phase 2 of a mechanism-agnostic technosignature program whose Phase 1 (white dwarfs) is registered at OSF DOI 10.17605/OSF.IO/6YH7R. The same "anomaly-residual" method — look for a departure from a well-modelled natural baseline, try to explain it away with a pre-registered battery of natural hypotheses, and report the residual — is carried from stellar remnants to a *living* host: main-sequence K dwarfs, the longest-lived and most thermally-stable living stars, and (being small) the deepest, most morphologically-resolvable transit hosts. Where Phase 1 was anchored on infrared excess, Phase 2 is **anchored on transit morphology**: a living star's cool photosphere is bright in the IR, so that channel loses its contrast and is demoted to a calibrated-but-weak corroborating role. We search TESS/Kepler light curves for transit *shapes* and photometric departures that no natural occulter (planet, eclipsing binary, disintegrating body, starspot) can produce, run every candidate through a fixed battery (an automated difference-image centroid gate first, then EB / activity / planet / disintegrating-body / instrumental tests), and report the surviving residual together with a population upper limit `f_max` reported **separately per morphology family** (a flat occulter bounds tightly; a subtle asymmetric one loosely; the limit says which).

The detection threshold is not a guessed number but a **frozen procedure**: an outlier-blind, per-noise-cohort empirical null plus injection-recovery that *calculates* the family-wise bar (expected to land near the Kepler-style ~6–7σ regime) on the noise floor and on synthetic and known-object controls — before any real candidate is unblinded. The single assumption we retain is the precondition for there being anything to find at all — time for life to have *originated* — implemented honestly as an **activity-based youth floor** (we cannot measure a field K dwarf's age directly, so we use the age–rotation–activity relation as a youth proxy and say so). The analysis runs on the same validated population-agnostic core as Phase 1, with a new K-dwarf plugin; we expect, and would be content with, a clean explained null and a quantitative upper limit, with a byproduct catalogue of K-dwarf transit and activity characterisation of value independent of the technosignature framing.

## Research questions and hypotheses (OSF registration field)

**Research questions** (= prereg §2):

- **RQ1 (morphology).** Do any K dwarfs show a periodic transit whose *shape* — asymmetry, flat-bottomedness, box-versus-U, anomalous duration, or secondary structure — cannot be reproduced by any natural occulter (sphere, ring, eclipsing binary, disintegrating body) after those are explicitly fitted and excluded?
- **RQ2 (photometric departure).** Do any show a persistent or time-varying photometric signature departing from the natural rotation/granulation/activity model that survives the natural-explanation battery?
- **RQ3 (upper limit).** Absent any unexplained anomaly, what upper limit `f_max` can be placed on the prevalence of anomalous occulters/departures around main-sequence K dwarfs, as a function of depth, period, and morphology family?

**Hypotheses / expected outcome** — a discovery-style search, not a difference-of-means test, so we state expectations honestly rather than predict an effect we hope to find:

- **Default (expected) — the null.** Every flagged candidate is explained away by the pre-registered battery, yielding a clean null and the RQ3 upper limit. We expect this and would be content with it.
- **Alternative — a residual.** A transit/photometric anomaly survives every natural test. In order of prior probability: (a) a previously-unmodelled *natural* occulter or variability class — most likely, and a worthwhile result in itself; or, far less likely, (b) a genuinely structured/fluctuating anomaly with no natural account. **No claim of artificiality is made on the basis of this pipeline** — a surviving residual is a target for conventional astrophysical follow-up.
- **Pre-specified detection criterion.** "Survives" means exceeding the frozen, family-wise empirical-null threshold (*calculated* by the registered §6 procedure, not guessed) **and** passing every applicable battery item; all thresholds are fixed before any real candidate is unblinded.

For a null-expected search, predicting a detection would be dishonest: the registered prediction *is* the null plus an upper limit.

## Explanation of foreknowledge and managing unintended influences (OSF registration field)

**Has data been collected / analysed already?** The target data (TESS/Kepler light curves of the registered K-dwarf manifest) is public archival data — it physically exists and is downloadable — but the **candidate tail has not been analysed**: no K dwarf in the target sample has been searched for anomalies, and the sample manifest itself is not yet frozen. What *has* been touched, and is disclosed here, is (i) fully synthetic injection-recovery pilots (no real data), and (ii) detector validation on two *named, published, already-characterised* systems — KIC 12557548 / Kepler-1520 (a known disintegrating planet — and itself a K dwarf) and Kepler-8 b (a clean transiting planet) — run to confirm the detector and morphology metrics behave on real astrophysics, exactly as Phase 1 validated on WD 1856+534 b. These touch *known objects*, not the target sample, and reveal nothing about which (if any) target K dwarfs show anomalies. All of it is timestamped in the public git history.

**Managing foreknowledge — the study is built around it:**

- **Thresholds are *calculated*, not chosen.** The family-wise detection bar is computed by a frozen procedure (an outlier-blind, per-noise-cohort empirical null + injection-recovery; prereg §6 step 3) on the noise floor, synthetics, and known-object controls — never by inspecting real candidates — and frozen before the candidate tail is unblinded (step 4). We register the method, not a guessed number; a reviewer judges adherence.
- **Outlier-blind noise estimation** (MAD with downward-only σ-clipping) stops a genuine anomaly from inflating its own threshold and masking itself.
- **No results-driven choices.** A checksummed immutable manifest fixes the sample before any light curve is pulled; resource-staged tiers are nested and pre-declared, expanded only by available compute, never in reaction to a result; no boundary is ever loosened to rescue a candidate.
- **Prior knowledge as a *filter*, never an assumption.** Domain knowledge of known anomalous systems (KIC 8462852, WD 1145+017) is used only to *explain candidates away* via the battery, never to assume the residual set is empty.
- **Tamper-evident timeline.** The public, branch-protected git history and the archived AI-collaboration transcripts independently timestamp every decision relative to the data, so "method fixed, *then* data analysed" is externally verifiable, not merely asserted.

The honest summary: some public data and known-object/synthetic validation have been seen and disclosed; **none of the registered target sample has been searched**; and the procedure that will search it is frozen and auditable before it runs.

## Additional blinding during analysis (OSF registration field)

The primary blind is structural and already registered (prereg §6): detection thresholds and per-cohort nulls are *calculated* on the noise floor, synthetics, and known-object controls (step 3) and **frozen before the real candidate tail is unblinded** (step 4). During calibration the analyst is blind to the real candidate signals — the empirical null is built from the bulk noise distribution, never the tail — so no threshold can be set in response to a candidate. This is the particle-physics "keep the signal region hidden until the analysis is frozen" discipline, implemented via the step-3 / step-4 split.

Additional analysis-time blinding:

- **Automated, deterministic vetting.** At this sample scale (tens of thousands), candidate vetting is algorithmic, not by-eye: the difference-image centroid gate and the full natural-explanation battery run automatically at frozen thresholds. There is no human "looks promising / looks like junk" step that could import selection bias — the pipeline is a deterministic function of the frozen inputs.
- **Outlier-blind noise/cohort estimation.** The per-star noise metric (MAD with downward-only σ-clipping) is computed so a genuine dip cannot influence the noise floor or a star's cohort assignment — blinding the *calibration* to the very signals it might otherwise suppress.
- **Blind injection-recovery.** Completeness `C_i` is measured by injecting synthetic anomalies into the real light curves; the injected set is not surfaced to the analyst during threshold-setting (a salt-and-pepper blind), so the pipeline cannot be tuned to preferentially recover or suppress particular morphologies.

What we deliberately do **not** blind, and why — **object identity.** Cross-matching a candidate against SIMBAD / the literature / known-disk and eclipsing-binary catalogues is a *registered battery step*; blinding identity would disable it. The protection is directional instead: prior knowledge may only *explain a candidate away*, never *assume the residual set is empty* — it can subtract candidates, never manufacture confidence in a non-detection.

## Study design (OSF registration field)

This is an **observational survey/census**, not a manipulative experiment: we administer no conditions or treatments and randomize nothing about the stars — the units (individual main-sequence K dwarfs in a frozen, checksummed manifest) have fixed, given properties we *measure*, not assign. We use the experimental vocabulary only where it genuinely maps.

- **Primary design — single-group observational screen with a pre-calibrated decision rule.** Each star is a unit contributing a light curve; the measure is a per-star detection statistic (BLS SDE + aperiodic/variable-depth SNR) plus the binary outcome of a fixed natural-explanation battery. One group, no treatment/control arms; the "condition" a star is in — its noise/activity level — is *observed, not assigned*. The outcome (anomalous residual vs explained) is assessed by a frozen, automated decision rule, not by eye.
- **Stratification (descriptive blocking, not randomized blocks).** Stars are binned into noise/activity **cohorts** by an outlier-blind scatter metric, and the threshold is calibrated within each cohort. The strata are measured, not randomly assigned — "blocking" only in the descriptive sense.
- **Embedded injection-recovery sub-study — where controlled factorial/repeated-measures design genuinely applies.** To measure completeness `C_i`, synthetic signals are injected into the real light curves over a fully-crossed grid of **morphology family × depth × period** (factorial). Each star receives many injections (**within-subject / repeated measures**); recovery at the frozen threshold is the dependent measure; injection realizations are pseudo-randomized. Because each light curve is its own noise background across all injected conditions, the completeness comparison across depth/period/family is **paired (within-subject)**, while the comparison *across cohorts* is **between-subject** — so the overall design is **mixed**.
- **No counterbalancing** in the experimental sense (no presentation-order or carryover effects exist). The one ordering — the resource-staged tier sequence T₁ ⊂ T₂ ⊂ … — is fixed and pre-declared (cleanest first), expanded only by compute and never by a result; it is an analysis *order*, not a manipulated condition, and the family-wise bar is set once for the full census so order cannot bias the outcome.
- **Outcome assessment.** Primary outcomes: (RQ1/RQ2) the residuals surviving the battery, and (RQ3) the per-family `f_max(depth, period) = 3/ΣC_i`. All measures and thresholds are frozen before the real candidate tail is unblinded.

## Route, timing, provenance — same as Phase 1

- **Route:** OSF Open-Ended Registration (immutable, timestamped, DOI, unmoderated, created public).
- **Timing:** the invariant is unchanged — *no analysis of real K-dwarf candidate data before the plan is frozen and registered.* Registered before the final read-through completes; later changes are dated pre-data amendments while no real candidate is touched. Critically, the calibration/validation steps (prereg §6 step 3: noise-floor cohorts, injection-recovery, known-object controls) are themselves pre-registered *procedures* — we register the method, not the numbers, and a reviewer judges adherence.
- **Provenance:** identical stand — Gemini and Claude as co-designers, full transcripts published, investigator retains 100% accountability; one collaborator credited unnamed at their request.

## Status

- Pre-registration: **DRAFT — not yet registered.** To be frozen and registered on OSF before any K-dwarf light curve is analysed.
- OSF: _DOI to be recorded here on registration._
- **Subjects (OSF / bepress taxonomy):** _Physical Sciences and Mathematics › Astrophysics and Astronomy › Stars, Interstellar Medium and the Galaxy_ (primary) **and** _Physical Sciences and Mathematics › Statistics and Probability_ (the empirical-null / large-scale-inference methodology). The taxonomy has no SETI/astrobiology node, so the work is classified by its actual objects and methods. _(Phase 1's selection was not recorded at the time; the same pairing applies — white dwarfs also fall under "Stars, Interstellar Medium and the Galaxy" — and can be backfilled here.)_
- **Tags (OSF):** technosignatures, SETI, K dwarfs, main-sequence stars, transit photometry, transit morphology, TESS, Kepler, light curves, anomaly detection, box least squares, mechanism-agnostic, empirical null, false discovery rate, large-scale inference, look-elsewhere effect, injection-recovery, occurrence-rate upper limit, artificial transit signatures, astrostatistics. _("pre-registration" deliberately omitted as intrinsic; "Dyson sphere" omitted as it cuts against the mechanism-agnostic framing.)_
- Registered-version git tag: _`phase2-registered-1.0` → commit `<hash>` to be recorded on registration._
