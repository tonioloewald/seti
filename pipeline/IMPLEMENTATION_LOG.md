# Implementation decisions log

The pre-registration (`../preregistration.md`) fixes the *methodology*; building the
pipeline requires concrete implementation choices that elaborate it. This log records
those choices, dated, with rationale and the registered section they implement, so the
record stays complete and honest.

### A note on "pre-data" for an archival reanalysis

This is a reanalysis of *existing* archival data, so "pre-data" cannot mean "before the
data exists." Our integrity invariant is narrower and explicit: the **procedures and
thresholds are specified independently of the findings, and never tuned to include or
exclude particular objects.** Detection thresholds come from the registered empirical
null + injection-recovery (§5.3), not from inspecting the excess list. The choices below
are of that kind — principled elaborations made while building/validating the machinery,
not selections made to produce a desired result. They are **pre-data amendments**
(confirmatory) in the sense of §8.

---

## 2026-06-01 — Channel-A detection pipeline (steps 1–3)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 1 | Parent sample frozen at `P_WD > 0.75` from the pinned Gentile Fusillo 2021 catalogue; manifest = `source_id, ra, dec, parallax, parallax_over_error, p_wd`. | The registered §3 confidence gate; matches the catalogue's published ~359k high-confidence count. | §3, §6.1 |
| 2 | Optical baseline (Gaia G/BP/RP + Teff_H/logg_H) taken **from the pinned catalogue**, not re-queried from the Gaia archive. | Identical EDR3 values; avoids a redundant 359k archive pull; fully deterministic from the pinned source. | §3, §5.3 |
| 3 | AllWISE photometry obtained via the Gaia archive's **precomputed `source_id`-keyed cross-match** (`allwise_best_neighbour` → `allwise_original_valid`), not fuzzy positional matching. | Deterministic, authoritative, reproducible. | §3 |
| 4 | Photosphere model = **DA (pure-H) Bergeron/Bédard 2020 grid**, evaluated at the catalogue's `(Teff_H, logg_H)`. DB/He grids fetched but not yet used. | §5.3 specifies Koester/Bergeron DA/DB synthetic photometry; most WDs are DA; DB extension deferred. | §5.3 (H0) |
| 5 | Photospheric W1–W4 predicted by **anchoring on observed Gaia G** via the distance-independent model colour `(Wn − G3)`. | G is the most precise Gaia band; colours are distance-independent; the optical is assumed photospheric (any disk/companion is negligible in G). | §5.3 (H0) |
| 6 | Per-band excess significance `χ = (f_obs − f_pred) / σ(f_obs)`, computed **only where AllWISE reports a detection** (`ph_qual ∈ {A,B,C}`). Non-detections (`U`) are upper limits, deferred to the censored-likelihood layer. | Standard excess metric; error referenced to the *observed* flux so it stays bounded by detection S/N when the photosphere is negligible (cold bands). | §5.3 (Stage 1) |
| 7 | `log g` clipped to the grid range [7.0, 9.0]; `Teff` used within [1500, 150000] K. | Stay within the model grid; WD `log g` is almost always 7.5–8.5. | §5.3 |

*Detection thresholds are NOT set here — they come from the empirical-null calibration
and injection-recovery (next steps), per §5.3.*

## 2026-06-01 — sequencing correction (the registered design caught an out-of-order step)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 8 | The **empirical null is applied to the post-battery natural-model residual `A`**, not to the raw excess χ. `pipeline/analysis/02_empirical_null.py` is retained as a **diagnostic** only. | §5.3 defines `A` = badness-of-fit of the *best natural model*; the empirical null's "bulk = null" assumption only holds after the natural-explanation battery. The diagnostic confirmed this directly: for W3/W4 the *detected* population is entirely excess sources (no bare WD is detectable there), so its bulk is debris disks, not the photospheric null (σ₀ collapsed to ~0.3). The correct order is **excess → battery → A → empirical null → flag**. | §5.3 |
| — | Valid finding retained from the diagnostic: the **photosphere-prediction scatter is ~3σ (λ≈10 in W1/W2)** — the textbook errors badly underestimate real scatter, so empirical calibration is essential (it inflates the threshold ~3×, preventing thousands of false flags). | The genomic-control inflation factor doing its job. | §5.3 |
| 9 | Natural-explanation battery v1 fits a blackbody to each W3/W4-excess SED -> T_x. Natural-regime boundaries (pre-data): **debris disk 300-1500 K, cool/BD companion 1500-4000 K**. An excess with T_x in those ranges is natural; T_x<300 K ("cold") or no acceptable fit is a residual to vet further. | §5.3's "T_x inside/outside natural regimes" logic. The boundaries are a literature-based v1 choice; §5.2 item 1 calls for deriving the disk range empirically from known WD disks — a refinement TODO. | §5.2, §5.3 |
| — | Cold-fit candidates (T_x<300 K) are **NOT** treated as anomalies on the blackbody fit alone. The remaining battery filters — cirrus/background (item 3) and W3/W4 detection reliability — and the final A-based empirical null must be applied first. (Of 104 cold-fits, 97 pass cc_flags but 68 are W4-driven; vetting pending.) | "Try to explain them away" (§5); avoids the god-of-the-gaps failure mode (§5.6). | §5.2, §5.6 |
| 10 | Cirrus vet (battery item 3): flag a cold candidate if SFD `E(B-V) > 0.15` at its position (queried from IRSA). Pre-data ceiling; the result is insensitive to it here (see below). | The cold W3/W4 "excess" in a dusty field is Galactic cirrus, not circumstellar (§5.2 item 3, §5.3 cirrus term). | §5.2, §5.3 |

### RESULT — Channel-A detection branch: a clean, *explained* null (2026-06-01)

The 104 cold-fit (T_x<300 K) candidates resolve completely: **7** fail cc_flags/ext; **85** fail W3/W4 reliability (marginal/low-S/N detections); the remaining **12** are **all in high-cirrus fields** (E(B-V) 0.30–1.22 — every one well above any plausible ceiling, so the conclusion is threshold-independent). **Zero survive.**

So the WISE-detection branch of Channel A yields **no unexplained cold excess** — every candidate has a natural cause — while correctly recovering ~536 warm debris disks/companions (median T_x ≈ 511 K). This is the *expected* null (§4.A: WISE cannot detect genuinely cold excess), reached by explanation rather than assertion. The real cold-anomaly sensitivity and `f_max` come from the upper-limit / forced-photometry layer (next).

## 2026-06-01 — upper limit `f_max(T_x, f)` (§5.7, RQ4)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 11 | `f_max` via **survey-depth injection-recovery**: a WD constrains an excess of temperature `T_x` and bolometric-luminosity fraction `f` if that excess's flux density exceeds the **nominal AllWISE 5σ depth** (W1 16.9 / W2 16.0 / W3 11.5 / W4 8.0 mag) in some band. `C_i`=that boolean; `f_max = 3.0/ΣC_i` (zero unexplained detections). Apparent bolometric flux from the Bergeron BC anchored on observed G (distance-independent). | §5.7 zero-detection bound; uses the population (all 295,406 WDs with a photosphere), not just AllWISE detections. | §5.7 |
| — | **Three-regime anomaly interpretation:** `T_x<~50 K` WISE-blind (unconstrained); **~50–300 K cold-anomaly window** = a cold excess is WISE-detectable AND distinguishable from a warm disk → the registered RQ4 constraint; `>300 K` excesses are natural disks (not an anomaly limit). | A warm "anomaly" is indistinguishable from a debris disk; a sub-50 K excess is below W4. Honest scope. | §4.A, §5.7 |
| — | Refinement TODO (future pre-data amendment): position-dependent WISE depths; CatWISE/unWISE forced photometry to deepen W1/W2; far-IR (Herschel/JWST-MIRI) for `T_x<50 K`. | Nominal uniform depths are a v1; the cold (<50 K) regime needs far-IR. | §5.4, §4.A |

**RESULT (RQ4):** in the cold-anomaly window (~50–300 K), with **zero** unexplained excesses found, `f_max ≈ few×10⁻³ to 10⁻⁴` of white dwarfs (depending on `T_x` and `f`). E.g. at `T_x=100 K, f=0.1`: `f_max ≈ 3×10⁻⁴`. Below ~50 K the search is WISE-blind. The registered, expected, *valuable* null with a quantitative bound. Figure: `figures/f_max.png`.

## 2026-06-01 — time-variability (NEOWISE W1/W2; §1.1, §5.3)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 12 | NEOWISE-R multi-epoch via **bulk IRSA-TAP spatial cross-match** (upload Gaia positions; replaced a per-source cone approach that hung on an un-timed-out query). Variability = reduced χ² (amplitude) + **Stetson J** (correlated W1/W2 = "structured"). Empirical-null calibrated; flag amplitude AND correlation; vet vs disk variability / brown-dwarf weather / W1 saturation. | §1.1 (dynamic = highest value); §5.3 variability statistic. Correlated two-band variability is robust to single-band noise. | §1.1, §5.3 |
| — | Scope (v1): the IR-excess candidate set only. Full-sample variability (pure transients with no static excess) deferred. | Tractable v1; NEOWISE per-epoch needs W1/W2-bright sources anyway. | §5.3 |

**RESULT:** 540 light curves (≥10 epochs); 17 significantly variable; 14 natural (disk variability / BD weather), 3 battery-unclassified-excess variables that are marginal or systematic on inspection — **no compelling anomalous fluctuation**. NEOWISE errors well-calibrated (χ²_red null = 1.00). A null for the highest-value signal, with a variable-disk byproduct. Figure: `figures/variability_examples.png`.

## 2026-06-01 — Channel B (TESS transit morphology; §4.B, §5.4)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 13 | Channel B runs on the **bright subset only** (Gaia G < 14 → 157 WDs; G<15 → 566, of 359k). BLS (`astropy`/`lightkurve`) on each SPOC/TESS-SPOC/QLP light curve; record period, depth, duration, periodogram peak S/N. Validated end-to-end on WD 1856+534 b (recovered P=1.4080 d vs truth 1.4079). | §5.4: TESS is photon-starved on faint WDs, so Channel B is **secondary / candidate-generating, not calibrated**. Bright WDs have the only usable TESS photometry. | §4.B, §5.4 |
| 14 | Vetting discriminants (§5.2 items 6–8): **duty cycle** (duration/period) + **sinusoid variance-explained at P and 2P**. High duty or high sin-R² ⇒ smooth modulation (ellipsoidal/reflection/pulsation) = stellar variability, not a transit. `flat_top` reported but NOT decisive (noise-dominated for shallow faint-WD signals). Plus a **SIMBAD identity** check. | A box (flat baseline + brief dip) is transit-like; a continuous sinusoid is not. Identity catches already-catalogued variables. | §5.2 |
| — | **Physical prior:** a planet transiting a WD (Earth-sized star) gives a **deep/total** eclipse; an observed dip of ≲1% therefore is **not** a transit *of the WD* — it is diluted, i.e. blended (a background eclipsing binary in TESS's 21″ pixels) or systematics. The shallow-depth argument is itself a strong natural filter. | §5.2 item 9 (difference-image / BEB vetting); WD geometry. | §5.2, §4.B |

### BUG FOUND & FIXED — `source_id` float64 corruption (integrity-relevant)

While vetting, a sanity check ("do all flagged candidates trace back to the parent
sample?") **failed**: 99/157 Channel-B result `source_id`s were absent from the parent
catalogue. Root cause: a 19-digit Gaia `source_id` exceeds float64's exact-integer range
(2⁵³ ≈ 9×10¹⁵). In `07_transit_search.py` the per-target loop pulled the id from a
**pandas `iterrows()` row that contained only numeric columns**, so pandas upcast the
whole row (and the int64 id) to float64, silently corrupting the trailing ~3 digits.
The **BLS results were unaffected** (coordinates are genuinely float and lossless), so
only the id *labels* were wrong.

**Blast-radius audit (all of `pipeline/`):** the corruption requires an **all-numeric**
iterrows row. Every Channel-A script that touches `source_id` either (a) keys it through
a *vectorised* merge before any row iteration, or (b) iterates a row that **also carries
a string column** (`ph_qual` / `class`), which forces the row to `object` dtype and
preserves the int64 id. Verified directly: battery 923/923, cold candidates 104/104,
variability 540/540, NEOWISE epochs 80,379/80,379 — **all `source_id`s valid and in the
parent sample. No Channel-A result is affected.** Only step 07 was vulnerable.

**Fix:** (1) `07` now indexes the id column by position (never via a numeric iterrows
row); (2) **`source_id` is carried as a STRING** throughout Channel B (and adopted as the
standard — strings cannot be coerced to float, round-trip exactly through CSV/Parquet, and
are identifiers not quantities); (3) the existing `transit_search.parquet` was **repaired
in place** by re-labelling from the (order-preserved) target list, *verified* by an exact
row-by-row `g_mag` match before relabelling — equivalent to a re-run since BLS depends only
on the unchanged coordinates.

**Channel-A string hardening + re-run verification.** Although the audit proved no
Channel-A result was corrupted, `source_id` was converted to a **string at every load
and producer** across the whole pipeline (build/01, analysis/01–06, fetch/02 & 04) for
defence-in-depth, then the **entire Channel-A compute chain was re-run on the cached
(pinned) archive pulls** and diffed column-by-column against a pre-change snapshot.
**Every science output is identical** — optical baseline (359,073), excess χ sums,
battery class counts (426 disk / 110 companion / 104 cold / …), cold funnel (12→0),
`f_max`, variability (17 flagged) — with `source_id` now a validated string. The change
is provably inert on the results; only the id representation changed. (The committed
parent manifest `wd_sample.csv.gz` was left untouched — read as string — so its pinned
checksum stays valid.)

**RESULT — Channel B v1:** of 157 bright WDs, 136 had usable TESS light curves. The
strongest signals are **stellar variability, not transits**: of the top 9 by BLS S/N, six
are smooth sinusoidal modulations (duty 0.19–0.33, sin-R² 0.4–0.99) and SIMBAD confirms
most are already catalogued (WG 21, FBS 0702+616, WG 17 [binary], HZ 43B [known WD+dM],
SH 2-216 [PN central star], a high-proper-motion star). **Three** signals are transit-
shaped (duty ≤0.02, low sin-R², no SIMBAD entry): Gaia `2660358032257156736` (P=0.258 d),
`6348672845649310464` (P=4.088 d), `5274517467840296832` (P=5.394 d). All three are
**shallow (0.7–1.2%)** — far too shallow for a planet transiting the WD itself — and each
has a faint Gaia neighbour (ΔG≈3.9–4.9, 1–3% flux) whose flux, under a deep eclipse,
matches the observed depth.

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 15 | **Difference-image centroid (BEB) vetting** (`09_centroid_vet.py`): download the SPOC target-pixel file, form the mean in-transit and out-of-transit images, and locate the flux-weighted centroid of the (out−in) difference. Centroid on the WD ⇒ on-target; offset ⇒ background/blended eclipsing binary. | The mandatory §5.2 item-9 test; the only way to tell an on-target transit from a blend in TESS's 21″ pixels. | §5.2 item 9 |

**RESULT — centroid vetting:** all three transit-shaped finalists are **OFF-TARGET** — the
dip centroid is offset from the white dwarf by **0.76 / 0.76 / 1.56 px (16 / 16 / 33″)**,
in each case toward the field/neighbour. They are **confirmed background/blended eclipsing
binaries**, not transits of the WDs. **Channel B closes as a clean, fully-vetted null — no
transit-of-a-WD anomaly.** Figures: `figures/transit_candidates.png`, `figures/centroid_vet.png`.

## 2026-06-01 — Channel C (accretion clean-zone; RQ3, §5.5)

| # | Decision | Rationale | Implements |
|---|----------|-----------|------------|
| 16 | Polluted (accreting) WDs identified from the **same pinned catalogue's** `sdssspec.dat` table (SDSS visual spectral classes; `fetch/05_sdss_spectral.py`): every WD class containing **Z** (Ca H&K metal lines). 1,137 in the P_WD>0.75 sample. | Deterministic, citable, no new survey — a different table of an already-pinned release (pre-data amendment, SOURCES.md). | §5.5, RQ3 |
| 17 | "Inner dust / disk-bearing" = membership in the **calibrated W3/W4 battery** excess classes, NOT a raw W1/W2 χ cut. | Channel A showed W1/W2 excess χ is inflation-dominated (λ≈10); a raw cut there manufactures false-positive disks (it gave a spurious 18.5% vs 6.4% with the calibrated criterion). | §5.3, §5.5 |
| 18 | Elevation rule applied verbatim from §5.6: a clean-zone object counts **only if coincident with a Channel-A or -B survivor**. | Clean-zone is common/natural (items 10–11), so corroborating-only — no standalone threshold. | §5.5, §5.6 |

**RESULT — Channel C:** of 1,137 polluted WDs, 157 have AllWISE coverage; **10 (6.4%) are
disk-bearing, 147 (93.6%) have a clean inner zone** — i.e. a clean inner zone is the norm,
consistent with the literature's small WD-disk fraction (the WISE-covered polluted subset is
bright/nearby-biased, so ~6% vs the literature few-% is expected). With **0 Channel-A and 0
Channel-B survivors**, the clean-zone set coincides with the A∪B survivors in **0 objects** →
Channel C elevates nothing, exactly as its corroborating-only registration anticipates. It
leaves a characterised polluted-WD / clean-zone catalogue as a byproduct
(`data/derived/channel_c_clean_zone.parquet`). **All three registered channels now complete
— three clean nulls.**
