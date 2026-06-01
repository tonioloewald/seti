# Results

Results from running the registered pipeline (tag `registered-1.0`) on real archival
data. All numbers are reproducible from the committed code (`pipeline/`), the frozen
manifests (`data/manifests/`), and the pinned sources (`SOURCES.md`); granular build
decisions are in [`pipeline/IMPLEMENTATION_LOG.md`](pipeline/IMPLEMENTATION_LOG.md).

**Scope of this document (v1).** It covers **Channel A — the static infrared excess**,
end to end. Time-variability (the §1.1 highest-value signature), Channel B (transits),
and Channel C (accretion clean-zone) are in progress and not yet reported here. This is
a first, un-reviewed pass with the stated caveats below — not a final paper.

---

## The pipeline run

| Stage | Result |
|-------|--------|
| Frozen sample (Gaia EDR3 WDs, `P_WD>0.75`) | **359,073** white dwarfs |
| AllWISE cross-match (Gaia precomputed) | **16,924** with W1–W4 photometry (4.7%) |
| — per-band detections | W1 16,897 · W2 9,081 · **W3 650** · **W4 339** |
| Optical photosphere baseline (Bergeron DA) | 295,406 with a pure-H Teff (median 10,883 K) |

## Channel A — static infrared excess

### Validation: the known debris-disk population is recovered

Fitting a blackbody to the **923** W3/W4-excess SEDs (the cooler bands, where the
photosphere is negligible so any detection is a real excess) yields, for the 705 with
≥2 excess bands:

- **536 natural** sources — 426 warm debris disks + 110 cool/brown-dwarf companions —
  with **median T_x ≈ 511 K**, exactly the textbook white-dwarf debris-disk regime.

That the pipeline cleanly recovers the expected astrophysics is the key validation: the
"explain-away" machinery demonstrably explains the things it should.

### The cold-candidate gauntlet (the explain-away in action)

104 objects instead fit a **cold** (T_x < 300 K) blackbody — the potentially interesting
regime. Each was put through the registered natural-explanation battery:

| Filter | Survivors |
|--------|-----------|
| cold-fit candidates | 104 |
| − contamination flags (`cc_flags`, `ext_flag`) | 97 |
| − W3/W4 reliability (ph_qual A/B, S/N ≥ 5) | 12 |
| − **cirrus** (SFD `E(B-V)`; all 12 had 0.30–1.22) | **0** |

**Zero survive.** Every cold candidate has a concrete natural cause — a marginal
detection, a contaminated frame, or (for all 12 that reached the last filter) Galactic
cirrus in the WISE beam. A null reached by *explanation*, not assertion.

### Result: a clean, explained null

Channel A's static-excess branch finds **no unexplained infrared excess** at any
temperature, while recovering ~536 natural disks/companions. This is the *expected*
outcome (§4.A: WISE's reddest band is 22 µm, so it cannot detect genuinely cold dust),
and it is consistent with the pre-registered prediction of a valuable null.

## RQ4 — the cold-excess upper limit `f_max`

With zero unexplained excesses, the registered zero-detection bound
`f_max = 3.0 / Σ_i C_i` (§5.7) was computed over all **295,406** WDs with a photosphere,
using survey-depth injection-recovery (a WD constrains an excess of temperature `T_x`
and bolometric-luminosity fraction `f` if it would have exceeded the AllWISE 5σ depth).

![f_max](figures/f_max.png)

Three regimes (see figure):

- **T_x ≲ 50 K — WISE-blind.** Below W4's reach → unconstrained. The genuinely cold,
  most-interesting regime needs far-IR (Herschel / JWST-MIRI).
- **~50–300 K — the cold-anomaly window** (a cold excess is both WISE-detectable *and*
  distinguishable from a warm disk). With zero found, **`f_max ≈ few×10⁻³ to 10⁻⁴`**.
  *E.g. at `T_x = 100 K` reprocessing 10% of the WD's light (`f = 0.1`):
  `f_max ≈ 3×10⁻⁴`* — fewer than ~0.03% of white dwarfs host such an unexplained excess.
- **T_x ≳ 300 K** — any excess is classified as a natural debris disk (~536 found, all
  natural); the tight numbers there are a generic IR-excess limit, **not** an anomaly limit.

In plain terms: **fewer than ~0.01–0.1% of (predominantly solar-neighborhood) white
dwarfs host an unexplained cold (50–300 K) infrared excess**, with the colder regime
currently beyond WISE's reach.

## Channel A — time-variability (NEOWISE)

The §1.1 highest-value signature is a *fluctuating* excess — something a static disk
cannot fake. We pulled NEOWISE-R multi-epoch W1/W2 light curves for the IR-excess
candidate set (**80,379 clean epochs for 807 WDs**, via a bulk IRSA-TAP spatial
cross-match) and computed, per source, the reduced χ² (amplitude) and the **Stetson J**
index (correlated W1/W2 variability — the "structured" proxy), both empirical-null
calibrated. The NEOWISE per-epoch errors are well-calibrated (χ²_red null centred at 1.00).

Of **540** WDs with ≥10 epochs, **17** show significant correlated variability:

- **14 are natural** — debris-disk variability (a known phenomenon; §5.2 item 1) or
  brown-dwarf "weather." Several show striking ~0.4–1.3 mag events over the decade
  (`figures/variability_examples.png`) — useful variable-disk candidates in their own right.
- **3** were flagged only because the *static* battery hadn't classified their excess
  (single-band or hot fit); their light curves are marginal (few epochs / large errors) or
  consistent with bright-source systematics — candidates for further scrutiny, most likely
  natural, **not** compelling anomalies.

So the variability layer **works** (it cleanly recovers real disk variability) and finds
**no compelling anomalous fluctuation** — a null for the highest-value signal, with a
variable-disk byproduct. *Scope caveat:* this v1 searched only the IR-excess population; a
full-sample variability search (to catch pure transients with no static excess) is a
future extension.

## Caveats (this is a v1)

- **Nominal, uniform WISE depths** for `f_max`; position-dependent depths would refine it.
- **AllWISE detections only** for the excess search; the non-detected majority enters the
  limit through survey depth, not forced photometry. **CatWISE/unWISE** would deepen W1/W2.
- **DA (pure-H) photosphere grid**; DB/He WDs use the same grid for now.
- **Solar-neighborhood selection bias** and possible local-environment effects on the
  natural baseline (stated in §3) apply to the interpretation of `f_max`.
- The cirrus ceiling, natural-temperature boundaries, and trial-factor are pre-data
  choices logged in `IMPLEMENTATION_LOG.md`; some are flagged for empirical refinement.

## Reproducibility

Sample/cross-match/baseline: `pipeline/fetch/01–03`, `pipeline/build/01`. Channel-A
analysis: `pipeline/analysis/01_ir_excess` → `02_empirical_null` (diagnostic) →
`03_battery` → `04_vet_cold` → `05_upper_limit`. Figures in `figures/`. Bulk data is
fetched on demand (gitignored) per `SOURCES.md`; the recipe is committed.

## What's next

1. **Time-variability** (NEOWISE W1/W2) — the fluctuating-anomaly search (§1.1); in progress.
2. **`f_max` refinements** — CatWISE/unWISE forced photometry; position-dependent depths.
3. **Channel B** (TESS transit morphology) and **Channel C** (accretion clean-zone).
4. Domain-expert review (entering as pre-data amendments, §8).
