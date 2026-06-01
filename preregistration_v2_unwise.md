# Pre-registration — Amendment v2: deeper W1/W2 (CatWISE2020 / unWISE) extension

**Type:** pre-data amendment to the registered plan ([`preregistration.md`](preregistration.md)),
under the §5.3 *extensibility clause* ("adding any new data source is done via a dated, public
amendment that pre-registers the new analysis before that data is examined"). It extends §5.3
(Channel-A excess statistic) and §5.7 (the upper limit `f_max`).

**Status:** frozen and committed to the public repository **before any CatWISE2020/unWISE
photometry of the sample is examined.** The git commit that adds this file is the timestamped
freeze; the authoritative order-of-decisions record is the commit history. It remains
**confirmatory**.

**Registration provenance.**
- **Parent registration (v1):** OSF [osf.io/6yh7r](https://osf.io/6yh7r) · DOI
  **10.17605/OSF.IO/6YH7R** (accepted, live). This document amends/extends that plan.
- **Authoritative record of this amendment:** this committed document plus the public git
  history (timestamped, force-push-protected) in the repository that is **linked from the
  accepted v1 OSF registration**. That already makes the v2 plan public and immutable *before*
  the deeper data are fetched — which is all that confirmatory status requires. **A separate
  OSF registration is not needed.**
- **Frozen at git commit `f510757`** — the exact, immutable v2 plan.
- **Also uploaded to the OSF project** (OSF-timestamped file), so the frozen plan is
  independently time-stamped on **both OSF and GitHub** before the deeper data are fetched. A
  separate standalone OSF *registration* is optional and not required for confirmatory status.

**No-peeking declaration.** The only prior contact with CatWISE was a *connectivity probe*
(a `gaiadr3`/`external.catwise2020` upload query during v1) that returned a server error and
**no rows** — no CatWISE2020 or unWISE photometry of the white-dwarf sample has been
retrieved or inspected. The plan below is therefore genuinely pre-data.

---

## 1. Motivation and scope

The v1 Channel-A excess search used **AllWISE detections**. Consequently the non-detected
majority of white dwarfs enters the `f_max` upper limit only through AllWISE's *nominal survey
depth*, and any excess fainter than the AllWISE detection floor is missed (external review,
[`pipeline/IMPLEMENTATION_LOG.md`](pipeline/IMPLEMENTATION_LOG.md), responses to review). Deeper
W1/W2 photometry — from forced photometry on the unWISE/CatWISE coadds — provides an actual
measurement (or a deeper limit) at far more positions, which (a) extends the excess search to
fainter sources and fainter excesses, and (b) tightens `f_max` in the W1/W2-sensitive
temperature range.

**What this improves and what it does not.** CatWISE2020/unWISE cover **only W1 (3.4 µm) and
W2 (4.6 µm)**. They therefore constrain *warm* dust and the **warm edge of the cold-anomaly
window** (~150–400 K, where W2 lies on the excess's Wien tail). They do **not** improve the
cold *core* (≲150 K), which is set by W3/W4 (12, 22 µm); that regime remains WISE-limited and
ultimately requires far-infrared data (Herschel, JWST/MIRI). We state this up front so the
amendment is not over-sold: it sharpens a secondary regime and deepens the excess census, it
does not move the headline cold-core limit.

## 2. Data sources (pinned)

- **Primary: CatWISE2020** (Marocco et al. 2021, ApJS 253, 8) — all-sky W1/W2 forced
  photometry on WISE+NEOWISE coadds; 90% completeness W1 = 17.7, W2 = 17.5 mag (≈0.8 / ≈1.5
  mag deeper than the AllWISE depths used in v1). Access: IRSA TAP (`catwise2020`) or the Gaia
  archive `external.catwise2020`. Pinned release + SHA-256 recorded at fetch, per
  [`SOURCES.md`](SOURCES.md).
- **Cross-check / alternative: unWISE** (Schlafly, Meisner & Green 2019, ApJS 240, 30) —
  ≈0.7 mag deeper than AllWISE in W1/W2. Used to confirm that conclusions are not specific to
  one pipeline's deblending.
- **Sample:** the **frozen v1 manifest** (`data/manifests/wd_sample.csv.gz`, P_WD > 0.75,
  359,073 WDs). No change to inclusion.

## 3. Method

### 3.1 Cross-match (pre-specified, deterministic)

Positional cross-match of the frozen WD positions (Gaia EDR3, propagated to the catalogue
epoch) against CatWISE2020:
- nearest CatWISE2020 source within **2.0″**;
- **reject blends**: discard the match if a second CatWISE2020 source lies within **3.0″**;
- **detection** = `w?snr ≥ 5` with clean contamination/confusion flags (`cc_flags`/`ab_flags`).
These thresholds are fixed here, before the data are seen.

### 3.2 Deeper excess search (Tier 1 — primary, definitely executed)

For every WD with a clean CatWISE2020 W1/W2 measurement, compute the **identical** calibrated
excess statistic as v1 (§5.3): predict the photospheric W1/W2 from the DA grid anchored on the
observed Gaia G via the model colour `(W_n − G3)`, and form `χ_n = (f_obs − f_pred)/σ`. Apply
the **same empirical-null calibration procedure** (re-derive the genomic-control inflation λ on
the deeper W1/W2 distribution — it is re-derived, not carried over) and the **same FDR / staged
look-elsewhere** control. Any flagged excess is passed through the **unchanged
natural-explanation battery** (§5.2: disk/companion blackbody fit, cirrus, reliability, blend),
exactly as in v1. New excesses are not anomalies until they survive that battery.

### 3.3 Forced photometry (Tier 2 — conditional, pre-specified so it stays confirmatory)

If feasible, run per-source forced photometry on the unWISE/CatWISE coadds at **every** WD
position (detections *and* non-detections), yielding a per-source W1/W2 flux or 5σ limit. This
replaces the nominal uniform depth in `f_max` (§5.7) with a **position-dependent, per-source
depth** — the most rigorous version of the limit. Tier 2 is registered now so that, if we
execute it, it remains confirmatory; if it proves impractical, Tier 1 stands alone.

### 3.4 Upper limit `f_max`

Recompute the §5.7 zero-detection bound `f_max = 3.0 / Σ_i C_i` with the deeper W1/W2 depths:
Tier 1 uses the empirically-derived CatWISE2020 5σ depth (per-source where the catalogue's
coverage/uncertainty permits, else the deeper survey 5σ); Tier 2 uses the per-source
forced-photometry limit. W3/W4 inputs are unchanged. The cold-core (≲150 K) bound is therefore
expected to be **unchanged**; the warm-edge (~150–400 K) bound tightens by up to roughly the
W1/W2 flux-depth factor (W2 ≈ 1.5 mag → ≈ 4×).

## 4. Integrity invariant

Procedures and thresholds (cross-match radius, blend rule, SNR cut, excess statistic, empirical
null, FDR, battery) are **fixed in this document before the deeper data are examined**, and are
never tuned to include or exclude particular objects. Detection thresholds come from the
empirical null + injection-recovery, not from inspecting the deeper-excess list.

## 5. Predictions (pre-registered, falsifiable)

1. **More warm debris disks.** The deeper W1/W2 will detect additional warm-excess WDs; these
   are predicted to be **natural** (disks/companions; battery-confirmed), extending the v1
   debris-disk census.
2. **A modestly tighter warm-edge `f_max`.** In the ~150–400 K range we predict up to a few-fold
   improvement; the ≲150 K core is predicted **unchanged**.
3. **A few new W1/W2 excess candidates**, predicted to resolve as natural under the unchanged
   battery (photospheric scatter, blends, disks). The empirical null is expected to inflate
   (λ > 1) as in v1, since the photosphere-prediction scatter, not the photometric error, will
   again dominate.
4. **High-value (low-probability) outcome:** a deeper-only excess that survives the full battery
   and the recalibrated empirical null would be a genuine residual warranting follow-up — the
   one result that would make this amendment more than a tightening.

We commit, as in v1, to reporting the **full ranked residual list**, not only survivors, and to
the standing interpretation that any residual is a target for conventional astrophysical
follow-up, never a claim of artificiality.

## 6. Deliverables

- `pipeline/fetch/06_catwise.py` (+ provenance/checksums in `SOURCES.md`);
- a deeper-excess analysis re-using the v1 modules (excess statistic, empirical null, battery);
- an updated `f_max` figure and a v2 section in [`RESULTS.md`](RESULTS.md);
- if Tier 2 is executed, a per-source forced-photometry depth product.

## References

- Marocco, F., et al. 2021, *ApJS*, 253, 8 — The CatWISE2020 Catalog.
- Schlafly, E. F., Meisner, A. M., & Green, G. M. 2019, *ApJS*, 240, 30 — The unWISE Catalog.
- (v1 references in [`preregistration.md`](preregistration.md) apply unchanged.)
