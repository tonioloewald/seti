# Pipeline

Analysis code for the search, to be developed **after** the pre-registration is timestamped
(per the open-science commitments in [`../preregistration.md`](../preregistration.md) §6).

Planned stages (see pre-registration §6 for the locked analysis plan):

1. **Sample selection** — build and freeze the *Gaia* EDR3 white-dwarf manifest (§3 cuts).
2. **Cross-match** — WISE/NEOWISE (+ Spitzer/2MASS/far-IR where available); assemble SEDs.
3. **SED fitting** — bare-WD cooling model vs. the natural-explanation alternatives (§5);
   compute IR-excess significance and best-fit excess temperature across the scanned band.
4. **Sensitivity characterization** — injection-recovery on synthetic signals to produce the
   detectability-vs-temperature curve (underwrites the RQ4 upper limit).
5. **Light-curve vetting** — TESS light curves for the IR-flagged subset (Channel B).
6. **Accretion-state test** — clean-inner-zone check for polluted systems (Channel C).
7. **Scoring & catalogue** — per-object anomaly/residual scores; ranked residual catalogue.
8. **Upper limit** — prevalence constraint as a function of assumed signal properties.

Nothing in this directory should run against real target data until registration is complete.
