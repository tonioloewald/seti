# Phase 1 Results: A Calibrated Null

*Accessible companion to the technical [`RESULTS.md`](../RESULTS.md) and the draft paper
[`paper/draft.md`](../paper/draft.md). This summary was drafted in collaboration with Gemini
and then corrected against the actual pipeline outputs — see the two accuracy notes below,
kept visible in the spirit of the project's radical transparency.*

We have completed the first end-to-end run of the pipeline on archival data, covering over
**359,000** high-confidence white dwarfs. As predicted in the project's pre-registration, the
result is a clean, fully-explained **null**.

A null result here is a scientific success, not a failure. It proves the "explain-away"
machinery works — the pipeline cleanly recovers hundreds of known natural debris disks and
companions, the known transiting planet WD 1856+534 b, the textbook variable-dust-disk WD
GD 56, and a population of cataclysmic variables — and it lets us set a hard, quantitative
boundary on how common true anomalies can be.

## Channel A — Infrared Excess & Time-Variability

**Static excess.** We searched for white dwarfs emitting more infrared light than their
photospheres should.
- *Initial flags:* 104 candidates with a "cold" (< 300 K) infrared excess — the regime most
  likely to host a genuine anomaly.
- *Explanation:* each was put through the natural-explanation battery. 7 failed contamination
  flags; **85 were marginal or low-significance detections** that failed the W3/W4
  reliability test; the **12** that survived to the final filter were **every one in a
  high-cirrus field** (looking through Galactic dust), well above any plausible threshold.
- *Result:* **zero** unexplained static anomalies.

**Time-variability.** We looked for infrared signals that fluctuate over time — the
highest-value signature of an active anomaly. *(This search was deliberately re-run on the
bright, **bare** white-dwarf population — not just stars that already showed a static excess
— to remove a selection bias that would otherwise have left us blind to sporadic events.)*
- *Initial flags:* scanning ~860 white dwarfs, the pipeline flagged 35 with significant
  correlated variability.
- *Explanation:* **28 are known natural phenomena** — mostly cataclysmic variables (accreting
  binary stars), variable dust disks (e.g. GD 56), or blended background stars in the
  telescope beam. The remaining **7 are weak, isolated, low-significance signals** consistent
  with the statistical-noise tail of the search — none compelling.
- *Result:* **no** unexplained dynamic anomaly.

## Channel B — Transit Morphology

We searched the light curves of the 157 brightest white dwarfs for anomalous brightness dips.
- *Initial flags:* 3 stars with transit-shaped dips.
- *Explanation:* because white dwarfs are Earth-sized, a true planetary transit would cause a
  deep dip — yet these were shallow (~1%). Difference-image centroiding showed the light was
  actually dropping on **faint background stars** sharing the telescope pixel (offset by
  16–33″), not on the white dwarfs themselves.
- *Result:* **zero** unexplained transits.

## Channel C — Accretion Clean-Zone

We examined 894 "polluted" white dwarfs (actively consuming rocky debris). Of the 112 with
good infrared data, **107 have a clean inner zone** (no detectable dust) and 5 are
disk-bearing.
- *Result:* a clean inner zone counts as an anomaly only if it corroborates a survivor from
  Channel A or B — and there are zero survivors, so this channel yields **no anomalies**. It
  does leave a useful catalogue of clean-zoned polluted white dwarfs for ordinary
  astrophysical study.

## The bottom line: the f_max upper limit

With zero anomalies found, we can set a mathematical upper limit on how common they could be:
**fewer than 0.01%–0.1% of white dwarfs in the local stellar neighbourhood host an
unexplained cold (50–300 K) infrared excess.** We have shown this limit is robust to the
assumed photospheric atmosphere.

*Caveat:* anomalies colder than ~50 K are invisible to the WISE data used in this pass and
remain unconstrained until far-infrared data (JWST, Herschel) are integrated.

## Next steps

- **Deeper W1/W2 (unWISE / CatWISE forced photometry)** — *the priority v2 amendment.* The
  excess search currently uses AllWISE detections, so the non-detected majority enters the
  upper limit only through nominal survey depth. Forced photometry on the deeper unWISE/CatWISE
  coadds would give an actual measurement (or deeper limit) at every position, tightening the
  bound in the warm/W1–W2-sensitive regime.
- **Far-infrared (JWST / Herschel)** — required to say anything about the sub-50 K regime.
- **Domain-expert review** of the full pass before submission.

> **A note on the variability search.** Searching the full bright sample — not just stars
> that already showed a static excess — was always part of the registered plan; §5.3 named
> the full-sample variability search as a planned extension. We simply executed it. It can
> only *add* candidates, never remove them, so there is no harm and every benefit in
> reporting it. This is not a heroic catch; it is the pre-established approach doing its job,
> and we include the extra results because we are being transparent at every step. The
> deeper-photometry improvement (unWISE/CatWISE) is the most pressing boundary to push for v2.
