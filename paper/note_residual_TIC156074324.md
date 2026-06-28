# Research note — an unclassified deep transiter surfaced by the Phase-2 K-dwarf search

**Gaia DR3 1397924585409290240 = TYC 3490-591-1 = TIC 156074324**

*Part of the pre-registered technosignature search (OSF [osf.io/2akn3](https://osf.io/2akn3/)). This
note records the single residual that the frozen Phase-2 battery cannot auto-classify in the
G < 13 (T0T1T2) tier. It is **not** a detection claim of any kind; it is the honest output of a
search designed to surface what it cannot explain.*

## Summary

The G < 13 run of the K-dwarf transit-morphology search (61,178 stars; frozen calibration
`phase2-calibration-T0T1T2`; battery v4) leaves, after the full identity → centroid → multi-sector →
triage cascade, **one** morphology-resolvable residual that survives every discriminant in the battery
when its metrics are evaluated at the **true** orbital period: a clean, deep, recurring,
sub-stellar-radius transit on a quiet-spectral-type K dwarf, **not present in any planet, TOI,
eclipsing-binary, or variable-star catalogue we cross-checked**. Its nature is undetermined from
photometry alone. We report it; we do not adjudicate it.

## The host

| Quantity | Value | Source |
|---|---|---|
| Gaia DR3 | 1397924585409290240 | Gaia DR3 |
| Aliases | TYC 3490-591-1, TIC 156074324 | SIMBAD |
| RA, Dec (deg) | 237.3531, +46.1396 | Gaia DR3 |
| Spectral type | K1V | SIMBAD |
| T_eff | 4866 K | Gaia DR3 (gspphot) |
| log g | 4.46 | Gaia DR3 (gspphot) |
| G, V | 10.70, 11.00 | Gaia DR3 / SIMBAD |
| Distance | 85.7 pc (ϖ = 11.69 mas) | Gaia DR3 |
| RUWE | 1.06 | Gaia DR3 |

The RUWE of 1.06 indicates a clean single-star astrometric solution — no evidence of an unresolved
companion dominating the astrometry. SIMBAD carries it only as a star (`otype = *`), with **no**
variability or binarity classification.

## The signal

Detected by the registered BLS (periods 0.5–13 d) on the stitched TESS FFI light curve:

| Metric | Value | Note |
|---|---|---|
| Period | **2.94 d** | true BLS period (see alias caveat) |
| Epoch t0 | 1931.59 (BTJD) | |
| Depth | ~6.3% (BLS) / ~7.2% (deepest bin) | face-value FFI photometry |
| SDE | 11.0 | well above the cohort bar (9.0) |
| Single-event SNR | 273 | strong |
| Sectors detected | 12 | recurs across all |
| Per-transit depth CV | 0.11 | stable; no dropout epochs |

Battery discriminants, evaluated **at the true 2.94 d period**:

| Test | Value | Reading |
|---|---|---|
| secondary eclipse depth | ≈ 0 (−0.0004) | no secondary → not a classic EB |
| odd–even depth difference | 0.008 | none → not a 2×-period EB |
| asymmetry | 0.028 | symmetric → not grazing/comet-tail |
| flat-bottomedness | 0.67 | moderately flat (not V-shaped, not a perfect box) |
| sinusoid variance (P, 2P) | 0.083 | not a rotational/ellipsoidal modulation |
| difference-image centroid | on-target | not a background blend (passed k06) |

It survives the activity gate and the v4 activity-robust local detrend — the detrend was implemented
specifically for this host (its sinusoid-activity index is 0.001 while it sits at the 94th percentile
of residual-set photometric scatter, 1739 ppm; see `pipeline/IMPLEMENTATION_LOG.md`, P2-v4) — and the
signal persists.

### Radius

Taking the depth at face value, R_p/R_★ = √(depth) ≈ 0.25–0.27. With R_★ ≈ 0.72 R_☉ (from T_eff,
log g), this gives **R_p ≈ 1.7–1.9 R_J** — sub-stellar (below the battery's depth→radius
eclipsing-binary cut at ~13% depth / 2.5 R_J), but at the **large** end of the gas-giant radius
distribution.

## Period-alias caveat (important)

The multi-sector triage stage (k08) re-derived the period as 11.74 d — a **4× harmonic alias** of the
true 2.94 d period. At the alias period the folded profile smears and the morphology metrics are
corrupted: the triage CSV reports `flat_bottom = 1.00`, which is an artifact of folding at the wrong
period, **not** a genuine flat-bottomed occulter. All metrics in the tables above are recomputed at
the true 2.94 d period. (This aliasing is a methodological item flagged for the pipeline: k08's
period should be reconciled to the k04 BLS period before its morphology metrics are used. See
`pipeline/runners/plot_resolvable_residuals.py`.)

## Catalogue cross-checks

- **TESS / ExoFOP (TIC 156074324):** no TOI, no SPOC threshold-crossing event, no disposition, no
  community observing notes. *Caveat:* the ExoFOP TCE record reflects TESS **2-minute** SPOC
  processing; this detection is from FFI photometry, so the absence of a SPOC TCE may simply mean the
  star was not a 2-minute target in the relevant sectors, rather than a non-detection by SPOC.
- **SIMBAD:** no variable-star or eclipsing-binary type; no associated planet.
- **Literature:** no references to this object as a variable, EB, or planet host.

So it is uncatalogued as a transiting/variable object to the depth of these checks.

## Interpretation — what it could be, and what it is not

The morphology (symmetric, flat-ish, no secondary, no odd–even, stable depth, on-target) is
**consistent with a genuine transit of a sub-stellar companion**. The two leading mundane hypotheses:

1. **An uncatalogued transiting giant** — an inflated hot Jupiter at the large end of the radius
   distribution, at a classic 2.94 d hot-Jupiter period. We cannot call it a planet: that requires a
   **mass** (radial velocities), which we do not have. A ~1.8 R_J radius is large for a planet and is
   itself worth noting.
2. **A grazing or low-mass eclipsing binary** whose secondary eclipse is too faint to detect in this
   band. The symmetric, flat-ish (not V-shaped) profile argues against a grazing geometry, and no
   secondary or odd–even signal is seen — but photometry alone cannot exclude a sufficiently faint
   stellar/sub-stellar companion.

It is **not** a technosignature claim and **not** a confirmed planet. It is the one residual the
frozen, pre-registered battery cannot classify — exactly the object such a search exists to surface,
carried as *unexplained* under the registered report-don't-adjudicate rule.

## Follow-up that would resolve it (external)

- **Radial velocities** → a mass: planet vs. brown dwarf vs. low-mass star.
- **Inspect any TESS 2-minute / QLP data** for a SPOC TCE and an independent depth.
- **Reconnaissance spectroscopy** → confirm K1V, check for a double-lined (SB2) companion.

---

*Diagnostics, figures, and the reproducing scripts are committed:
`figures/note_1397924585409290240_fold.png`, `figures/kdwarf_T0T1T2_standout_1397924585409290240.png`,
`data/manifests/kdwarf_T0T1T2_resolvable_truePeriod_morphology.txt`,
`pipeline/runners/plot_note_figure.py`. Search provenance: `docs/phase2_status.md`,
`pipeline/IMPLEMENTATION_LOG.md` (P2-unblind / P2-unblind-resid).*
