# Registration plan and decisions

This note records the deliberate choices around registering this pre-registration, so the reasoning is archived alongside the work (consistent with the open-science commitments in [`preregistration.md`](preregistration.md) §8).

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

- Pre-registration: **drafted, sealed, not yet registered** (as of 2026-06-01).
- OSF registration DOI: _to be added on registration._
- Registered-version git tag: `registered-1.0` _(to be applied to the commit matching the OSF snapshot)._
