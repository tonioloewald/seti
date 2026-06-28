# Methods note — the one T0T1T2 "residual" was an eclipsing binary our battery under-vetted

**Gaia DR3 1397924585409290240 = TYC 3490-591-1 = TIC 156074324**

*Part of the pre-registered technosignature search (OSF [osf.io/2akn3](https://osf.io/2akn3/)). This
note records a methodological finding, not a discovery. The single morphology-resolvable residual that
the frozen G < 13 (T0T1T2) battery could not auto-classify turned out, on external cross-check and an
exploratory re-vet, to be an **eclipsing binary** — surfaced as a "residual" only because of a blind
spot in our secondary-eclipse test. We record the object's true disposition, the blind spot, and the
fix.*

> **Correction history.** Earlier commits (`499dc70`, `658cf51`, `9f85869`) described this object as
> an "uncatalogued deep transiter" of undetermined nature. That was wrong: it is an eclipsing binary.
> This note supersedes that framing. The error and its cause are documented below because they are the
> scientifically useful part.

## Disposition: eclipsing binary

The object is a K1V dwarf (T_eff 4866 K, R_★ ≈ 0.72 R_☉, d = 85.7 pc, RUWE 1.06). The signal is a
**2.935 d eclipsing binary** with a clear secondary eclipse:

- **SPOC** (TESS 2-minute, sectors 14–78) reports it as a multi-sector target with full Data
  Validation and **four TCEs**. TCE_1: P = 2.935 d, depth 8.6%, MES 690. **TCE_2: same period,
  epoch offset by half a phase, depth 1.7%, MES 122 — the secondary eclipse.** A 1.7% secondary at
  φ = 0.5 is the textbook signature of a low-mass eclipsing companion. SPOC detected it; the TESS
  team never promoted it to a TOI (consistent with an EB disposition).
- **Our own data confirm it:** folding the FFI light curve at the true 2.935 d period and measuring
  the secondary on a window matched to the eclipse duration recovers a secondary at **0.7% (FFI) and
  77σ significance** (`pipeline/runners/revet_secondary.py`). The companion contributes ~1.7% of the
  system light → an M-dwarf-class secondary. Not a planet, not an anomaly.

## Why our frozen battery missed it — two compounding blind spots

1. **k08 period aliasing.** The multi-sector triage stage re-derived the period as 11.74 d — a 4×
   harmonic alias of the true 2.935 d. At an alias period the folded profile smears, the morphology
   metrics are corrupted (it is what produced the spurious `flat_bottom = 1.00`), and the v4 local
   detrend is defeated (its windows land at the wrong phase).
2. **The secondary-eclipse test was insensitive to narrow / shallow secondaries.** The frozen battery
   measured the secondary as a **median over a ±0.05-phase window** (≈ 3× the eclipse width, which
   dilutes a narrow secondary to ~0: this object's secondary measured 0.0) and fired only if
   `secondary_depth > 0.3 × primary_depth`. This EB's secondary/primary ratio is 1.7%/8.6% = 0.20 <
   0.30, so even a correctly-measured secondary would not have tripped the relative threshold. The
   physically correct test is the **statistical significance** of a secondary at φ = 0.5, measured on
   a window **matched to the eclipse**, regardless of its depth relative to the primary.

## The fix, and its exploratory consequences

The secondary test in `k04.battery` now measures the secondary on a duration-matched window and flags
an EB on **significance** (secondary > `SECONDARY_SIGMA` = 6σ vs out-of-eclipse scatter), replacing the
diluting wide-median + 0.3×primary rule; the odd-even in-transit selection is likewise matched to the
eclipse. The injection regression (`k04 --test`) is preserved — box → RESIDUAL (22/24), planet →
natural_planet (23/24) — so detection and the flat-occulter completeness that `f_max(box)` rests on are
unchanged; injected occulters have no secondary and are not spuriously reclassified.

Applied as an **exploratory post-data re-vet** to the T0T1T2 recurring-candidate list (at each
object's true BLS period), the corrected secondary test reclassifies **~5 of the 64 residuals as
eclipsing binaries** (including this object at 77σ and `2561459808901475584`, a second resolvable
residual, at ~11σ), and — as a validation by-product — finds that **~2 of the 107 `natural_planet`
objects also have strong secondaries** (near-equal eclipse depths), i.e. the same blind spot leaked a
few EBs into the planet class too. Of the six morphology-resolvable residuals, two are now EBs; the
other four are low-significance / asymmetric and remain unexplained (marginal), none a clean
flat-bottomed occulter.

## Integrity framing

T0T1T2 was already unblinded, and G < 13 is the manifest's faintest tier, so this fix is inherently
**post-data / exploratory** under the registered stopping rule — it is **not** applied as a corrected
confirmatory result. The frozen confirmatory output stands (the battery flagged residuals; Option A:
reported, not adjudicated). This note + the exploratory re-vet are the *follow-up* that explains them —
exactly the report-then-follow-up model the registration intends. The detection bars, the cohort
nulls, the completeness `C_i`, and `f_max` are untouched. Logged in `AMENDMENTS.md` (post-data /
exploratory) and `pipeline/IMPLEMENTATION_LOG.md`.

## The general lesson

In an agnostic deviation-search, surfaced anomalies = (real deviations) + (holes in the "natural"
model). This object was the second kind. The episode is the methodology working as intended: a residual
was surfaced and *not* explained away in prose, an external cross-check (SPOC) and a corrected test
resolved it robustly, and the blind spot it exposed was closed. Every closed blind spot makes a
surviving residual mean more.

---

*Reproducing artifacts: `pipeline/runners/revet_secondary.py` (re-vet),
`data/manifests/kdwarf_T0T1T2_secondary_revet.csv` (per-object secondary metrics),
`figures/note_1397924585409290240_fold.png`. SPOC DV: MAST TIC 156074324, sectors 14–78.*
