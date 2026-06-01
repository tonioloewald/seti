# Amendments log

This file records every change to the registered plan ([`preregistration.md`](preregistration.md)) made **after** the Open Science Framework (OSF) registration, in service of the open-science commitments in §8 of the pre-registration.

The OSF registration is an immutable, timestamped snapshot. Each amendment below is **also filed as a formal Update to the OSF Registration** — OSF's native, immutable update mechanism, which is the *authoritative* record. This file and the public git history (on `main`, force-push-protected once the repository is made public) are the human-readable companion, establishing the order of every decision relative to the data — which is what keeps the work honest.

Each entry states:
- **What** changed (section + summary),
- **Why**,
- **Type** — one of:
  - **pre-data amendment** — made *before* any real target data was analyzed (e.g. from expert review). Remains **confirmatory**.
  - **post-data change** — made *after* real data was seen. Flagged **exploratory / post-hoc**; never presented as confirmatory.

| Date | Type | Section(s) | Change | Rationale |
|------|------|-----------|--------|-----------|
| 2026-06-01 | pre-data | §3, §5.3 | Channel-A detection-pipeline implementation decisions (sample freeze; optical baseline from the pinned catalogue; AllWISE via Gaia precomputed cross-match; DA-grid photosphere; Gaia-G-anchored excess statistic; log g/Teff grid bounds). | Concrete elaborations of the registered method — see [`pipeline/IMPLEMENTATION_LOG.md`](pipeline/IMPLEMENTATION_LOG.md). Procedures fixed independent of findings; detection thresholds still come from the empirical null + injection-recovery (§5.3). |
| 2026-06-01 | pre-data | §5.2–5.7 | Channel-A battery + upper limit; Channel B (transit BLS + mandatory difference-image centroid vetting); Channel C polluted-WD identification via the **same pinned catalogue's** `sdssspec.dat` SDSS spectral classes. | Registered-method elaborations; all thresholds from the empirical null / injection-recovery, not candidate inspection (decisions #8–#18 in the implementation log). |
| 2026-06-01 | confirmatory (registered extension) | §5.3 | Time-variability search extended from the IR-excess set to the **brightness-limited** sample (all AllWISE WDs with W1<15.5). | The registration already named the full-sample variability search as a future extension; executed here (prompted by external review). Bias-reducing — it can only *add* candidates, not remove them — and the outcome remained a clean null. Decisions #21–#22. |
| 2026-06-01 | robustness | §5.3, §5.7 | DA-photosphere assumption checked against the DB grid (cold null) and against confirmed-DA-only / non-DA-excluded subsets (f_max); `source_id` carried as a string pipeline-wide. | Responses to external review; results unchanged. Decisions #19–#20. |

### Planned amendments (intent recorded before the new data are examined)

To preserve confirmatory status under the §5.3/§8 extensibility clause, the following are
recorded **now**, before the relevant data are fetched or analysed. Each will be filed as a
formal OSF Registration Update (by the human author) before execution.

- **unWISE / CatWISE forced photometry (priority v2).** Deepen W1/W2 by forced photometry on
  the unWISE/CatWISE coadds at every WD position, so the non-detected majority enters the
  upper limit through an actual measurement/limit rather than the nominal AllWISE survey
  depth. Pre-registered analysis: identical excess statistic and empirical-null calibration as
  Channel A, applied to the deeper W1/W2; recompute `f_max` in the warm/W1–W2-sensitive
  regime. Flagged by external review as the most pressing limitation.
- **Far-infrared (Herschel / JWST-MIRI).** Required to constrain the sub-50 K regime that WISE
  cannot reach; targeted follow-up of any future candidate, not a survey-wide pass.

---

*Before registration, the plan is edited directly in `preregistration.md` (tracked in git); this log begins at the moment of OSF registration. Amendment rows above are filed as OSF Registration Updates by the human author of record; this file and the git history are the human-readable companion.*
