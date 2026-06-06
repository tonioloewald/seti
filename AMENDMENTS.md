# Amendments log

This file records every change to the registered plan ([`preregistration.md`](preregistration.md)) made **after** the Open Science Framework (OSF) registration, in service of the open-science commitments in §8 of the pre-registration.

The OSF registration is an immutable, timestamped snapshot of the *original plan*. The
**authoritative record of every post-registration amendment is this file plus the public git
history** (on `main`, force-push-protected) in the repository that is **linked from the accepted
OSF registration**: each commit is timestamped and tamper-evident, which establishes the order
of every decision relative to the data — and that is what keeps the work honest. (OSF's native
registration-Update mechanism is unavailable for this Open-Ended Registration, so the linked
repository *is* the amendment record rather than a mere companion to it. A separate OSF
registration per amendment is optional and not required for confirmatory status.)

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
| 2026-06-01 | **pre-data (v2)** | §5.3, §5.7 | **Deeper W1/W2 (CatWISE2020 / unWISE) extension** — full plan frozen in [`preregistration_v2_unwise.md`](preregistration_v2_unwise.md): deeper excess search + tighter warm-regime `f_max`, identical excess statistic / empirical null / battery as v1. **Committed before any CatWISE2020/unWISE photometry of the sample was examined** (no-peeking declaration in that file). | External-review priority. Pre-registered to keep it confirmatory under the §5.3 extensibility clause. |

### Planned amendments (intent recorded before the new data are examined)

To preserve confirmatory status under the §5.3/§8 extensibility clause, the following are
recorded **now**, before the relevant data are fetched or analysed. Each will be filed as a
formal OSF Registration Update (by the human author) before execution.

- **Deeper W1/W2 (CatWISE2020 / unWISE).** ✅ **Now registered** — see
  [`preregistration_v2_unwise.md`](preregistration_v2_unwise.md) (the v2 row above). Fetch and
  analysis proceed *after* that freeze.
- **Far-infrared (Herschel / JWST-MIRI).** Required to constrain the sub-50 K regime that WISE
  cannot reach. Two distinct, limited modes: (a) deep facilities (JWST/MIRI mid-IR; Herschel
  far-IR, archival/decommissioned) are **pointed**, so they characterise *individual* candidates
  but cannot give a blind *population* limit; (b) all-sky far-IR surveys that *could* be
  cross-matched (**AKARI-FIS 65–160 µm, IRAS**) are far too shallow (~Jy vs the µJy–mJy of WD
  dust) to detect WD-level excess. **Possible tractable step (noted 2026-06-01):** an
  AKARI-FIS/IRAS all-sky cross-match purely to *extend the f_max figure into the far-IR and
  demonstrate* (rather than assert) that the <50 K regime stays unconstrained even with all-sky
  far-IR. Modest value; do only if a reviewer presses. Genuine sub-50 K progress needs a deep
  far-IR *survey* facility that does not currently exist (SPICA cancelled; PRIMA only proposed).

---

*Before registration, the plan is edited directly in `preregistration.md` (tracked in git); this log begins at the moment of OSF registration. Amendment rows above are filed as OSF Registration Updates by the human author of record; this file and the git history are the human-readable companion.*

---

# Phase 2 (Main-Sequence K Dwarfs) — amendments log

Post-registration changes to the Phase-2 registered plan ([`preregistration_kdwarf.md`](preregistration_kdwarf.md)), which is a **separate** OSF Open-Ended Registration (see [`REGISTRATION.md`](REGISTRATION.md) → "Phase 2"). Registered baseline: git tag **`phase2-registered-1.0` → commit `c404b73`**, submitted to OSF 2026-06-05. The same confirmatory (pre-data) vs exploratory (post-data) rules as Phase 1 apply; because OSF's update flow is unavailable for Open-Ended Registrations, this file + the git history are the authoritative amendment record.

| Date | Type | Section(s) | Change | Rationale |
|------|------|-----------|--------|-----------|
| 2026-06-05 | housekeeping | header, Status | Flip status DRAFT → registered; record the registered git tag and date. Registration **approved, public, and immutable** at <https://osf.io/2akn3/> (10:30 UTC); DOI pending OSF minting (expected `10.17605/OSF.IO/2AKN3`). | Records the registration event itself; no methodological change. |
| 2026-06-05 | pre-data | §3 (sample); §6 step 1 | **Froze the K-dwarf sample manifest** from Gaia DR3 (`gaiadr3.gaia_source`): **175,968** stars. Registered core cuts (Teff 3900–5300 K, logg_gspphot > 4.3, RUWE < 1.4, parallax_over_error > 10) in-query; plus two pre-data implementation decisions of the registered §3 selection — the **hard limit G < 13** (the most inclusive of the §3 indicative scales; brighter tiers are the analysis *order* within it) and the **main-sequence box** (M_G within ±1.5 mag of ridge `5.5 + 2.83·(BP_RP − 0.85)`, BP_RP ∈ [0.78, 1.84]). Manifest sha256 `ffe47bc2b0591e4ee7c24705e6741b59b88bf6fac69fa674e0347bbac0d606d4`; builder `pipeline/fetch/k01_kdwarf_manifest.py`; tag `phase2-manifest-1.0`. | Registered-method elaboration; the selection is frozen **before any light curve is pulled**. The box removed 1,681 (<1 %) — a generous sanity cut on top of the logg dwarf selection, not a tight isochrone. Gaia DR3 is static so the query reproduces byte-identically. |
| 2026-06-06 | post-data (methods correction) | §5 (`f_max` / C_i) | **Classification-aware completeness.** Corrected the per-star completeness C_i used in `f_max` to require an injected anomaly to be *detected **and** survive the battery as a residual*, not merely BLS-detected — so a flat occulter mislabelled "planet", or a tail labelled "disintegrating body", earns no `f_max` credit (bounds the battery's anomaly→natural leakage directly). Prompted by adversarial (Gemini) review of the T0 draft, after unblinding. **The detection bars (7.6/7.7/8.5 SDE) are unchanged, so the candidate cascade and the null are unaffected**; only the limit is refined, and conservatively. Effect: f_max(flat occulter) ≈ 2.8×10⁻⁴ (unchanged — leakage negligible for this clean morphology), f_max(disintegrating-tail) ≈ 3.4×10⁻⁴ (weaker — it partially mimics a natural class). | Post-data, but candidate-independent and conservative: it changes the *limit's* completeness definition, not which objects were flagged. Flagged as a methods correction, not a result-tuning change. |

*No threshold or boundary was ever tuned to a candidate. The calibration/validation procedure (prereg §6 step 3), the K-dwarf plugin, and the synthetic/known-object pilots are all pre-data and remain confirmatory.*
