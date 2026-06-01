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
