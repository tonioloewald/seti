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
