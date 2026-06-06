# Phase 2 — T0 (G<11) results

First tier of the registered K-dwarf search (OSF [osf.io/2akn3](https://osf.io/2akn3/),
plan `preregistration_kdwarf.md`). T0 = the brightest tier, main-sequence K dwarfs with
G < 11, executed against the frozen calibration `phase2-calibration-T0`.

## Sample and calibration

- **Searched:** 12,100 G<11 K dwarfs with a usable TESS light curve (of ~12,500 in tier; the
  rest are saturated-bright failures). Outlier-blind noise floor per star (k02).
- **Calibration (frozen, tag `phase2-calibration-T0`):** 3 noise cohorts of ~4,108 stars —
  quiet 507 ppm (λ=0.71, bar 7.6 SDE), mid 938 ppm (λ=0.68, 7.7), active 1268 ppm (λ=1.02,
  8.5). Family-wise bar set for the full N_total = 175,968 manifest. Per-cohort completeness
  C_i self-weights with activity (planet/box ≈0.96 quiet → 0.77–0.85 active at 1% depth).

## Search and battery cascade

| Stage | Survivors |
|------:|:----------|
| BLS candidates above the per-cohort bar | 4,131 |
| Light-curve battery residuals (not planet/EB/activity) | 1,358 |
| After identity cross-check (135 known planets/TOIs/EBs/binaries/variables cleared) | 1,223 |
| After difference-image centroid gate (546 background blends killed) | 616 on-target |
| After multi-sector recurrence (388 single-sector red-noise artifacts rejected) | 86 recurring + 78 single-sector-only + 64 no-data |
| Deep multi-sector battery on the 86 recurring | 16 characterised natural + 70 sub-resolution |

## Result

**No anomalous transit signature.** In the morphology-resolvable regime — transit depth
≳ 0.3%, where the registered folded-profile SNR floors apply and completeness C_i ≈ 0.96 —
**zero candidates are unexplained**: every one resolves to an eclipsing binary, a transiting
planet, a background blend, a red-noise single-sector artifact, or a known object.

The 86 recurring transits triaged (deep multi-sector battery): 6 eclipsing binaries
(up to 26% deep, one seen in 14 sectors), 10 transiting planets, and 70 sub-resolution
detections — all below 0.3% depth (45 below 0.1%), where flat-bottom / asymmetry / depth-CV
are noise-dominated and a shape cannot be measured. **None** has the high-value signature
(a deep, flat-bottomed or structured occulter); the apparently "anomalous" shapes are the
metric artifacts the positive control already characterised at low SNR.

## Population upper limit

Completeness is **classification-aware**: an injected anomaly counts only if it is detected *and*
survives the battery as a residual (corrected post-review; see AMENDMENTS.md 2026-06-06). The
per-family Poisson zero-detection bounds at 1% depth over the searched T0 population are
**f_max ≈ 2.8×10⁻⁴ for flat-occulter anomalies** (ΣC_i ≈ 10,900; leakage negligible — a flat
occulter is reliably classified anomalous, C_i ≈ 0.96) and **≈ 3.4×10⁻⁴ for disintegrating-tail-like
anomalies** (ΣC_i ≈ 8,950; weaker — partially explained as a natural disintegrating body). Both
weaken toward shallower depths as C_i falls; below ~0.3% depth (the pre-registered pilot's
resolution floor) the search has no morphology teeth and places no anomaly constraint.

## Byproduct catalogue

A by-product of the search, of value independent of the technosignature framing (registration
§7): the recurring real transits — 6 newly-flagged eclipsing-binary candidates and 10
transiting-planet candidates among K dwarfs not previously catalogued as such, plus the wider
planet-regime recurring set.

## Inconclusive / follow-up sets (documented, not detections)

- **142 recurrence-untestable** — 78 with only one TESS SPOC sector, plus 64 whose cached
  light curve is a QLP (FFI) product rather than SPOC, so multi-sector SPOC recurrence cannot
  be tested (a retry confirmed these are not transient failures). Await further coverage /
  SPOC processing, or a QLP-inclusive recurrence pass.
- **70 sub-resolution recurring** — real repeating dips below the shape-resolving depth
  (<0.3%); characterisable only with more/deeper photometry.

None is a detection, and none sits in the morphology-resolvable regime: all 142
recurrence-untestable candidates and all 70 sub-resolution ones are either below 0.3% depth
or single-sector marginal. They are flagged for conventional follow-up per the registered
stopping rule. The resolvable-regime result — zero unexplained anomalies — is unaffected by
them.

## Provenance

Pipeline: frozen manifest (`phase2-manifest-1.0`) → `pipeline/fetch/k02`–`k08` on the
validated population-agnostic core. Residual lists at each stage in `data/manifests/`
(`kdwarf_T0_residuals*.csv`). No real candidate was inspected before the calibration was
frozen and tagged; the cascade above lifts the blind exactly once (k04 `--unblind`).
