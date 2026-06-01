# An Anomaly-Residual Search for Unexplained Thermal and Photometric Signatures Around White Dwarfs

*A mechanism-agnostic technosignature search — motivated by, but not presupposing, long-lived intelligence.*

A pre-registered, open search for **anomalous departures — static or time-varying — from the natural behavior of cooling stellar remnants** that resist explanation by known astrophysics, around catalogued white dwarfs.

> We make **no assumptions about how a long-lived civilization arises, what it wants, or what it builds** (no Dyson spheres, no energy-maximization, no efficiency/resilience optimization). We look for *something that fails to look like known nature*, then try to explain it away. The most likely interesting outcome is not life but **new natural astrophysics**; the most likely outcome overall is a clean null, which yields a quantitative upper limit. See [`preregistration.md`](preregistration.md).

## Status

✅ **Registered on OSF** (2026-06-01) — DOI [10.17605/OSF.IO/6YH7R](https://doi.org/10.17605/OSF.IO/6YH7R), frozen at git tag `registered-1.0`. Analysis is under way on real archival data, all of it post-dating the locked plan.

📊 **First results — Channel A (static infrared excess): a clean, *explained* null plus a quantitative upper limit (`f_max`).** See [`RESULTS.md`](RESULTS.md).

The repository is **public** with a force-push-protected `main`, so the entire drafting + analysis history is an independent, tamper-evident record that all analysis post-dates the registration.

## Why this design

- **Pre-registration first.** The hypotheses, sample cuts, natural-explanation battery, and scoring rule are fixed *before* any data is touched, so we cannot reason toward a result post hoc.
- **Anomaly-residual, not assume-the-signal.** Unlike "listen for a beacon we'd recognize" approaches (whose technology assumptions fail when the technology isn't the one we imagined), we only assume an anomaly leaves *some* imprint in channels we already survey.
- **Null is a success.** A clean null produces a publishable upper limit; surviving anomalies are published as unexplained, most likely as new natural phenomena. Success never depends on detecting intelligence.

## Repository layout

| Path | Contents |
|------|----------|
| [`preregistration.md`](preregistration.md) | The locked pre-registration document (the heart of the project) |
| [`REGISTRATION.md`](REGISTRATION.md) | Registration route, timing, and provenance decisions (the record of *why*) |
| [`AMENDMENTS.md`](AMENDMENTS.md) | Dated log of post-registration changes (pre-data = confirmatory; post-data = exploratory) |
| [`RESULTS.md`](RESULTS.md) | First results — Channel A: the explained null + the `f_max` upper limit |
| [`SOURCES.md`](SOURCES.md) | Data sources, pinned releases, determinism policy, fetched-artifact log |
| [`pipeline/`](pipeline/) | Analysis code (fetch → SED fitting → battery → upper limit), env lock, and the [implementation log](pipeline/IMPLEMENTATION_LOG.md) — developed post-registration |
| [`docs/`](docs/) | The [project glossary](docs/glossary.md), original brief, and archived AI-collaboration transcripts |
| [`data/`](data/) | Frozen, checksummed sample manifests + small reference grids. Bulk/derived data is fetched on demand, **not** tracked. |
| [`figures/`](figures/) | Result and diagnostic figures (`f_max.png`, QQ plots) |

## Open-science commitments

1. The pre-registration is timestamped on OSF before any project-specific data analysis.
2. All code, queries, the frozen sample manifest, the natural-explanation battery, and the residual catalogue are released here, with history post-dating registration.
3. Amendments to the registered plan are public, dated, and rationale-bearing; superseded versions are retained.

## License

- **Code** (`pipeline/`, notebooks, scripts): **Apache-2.0** — see [`LICENSE`](LICENSE). Chosen over MIT for its explicit patent grant and patent-retaliation clause.
- **Documents and data products** (the pre-registration, `docs/`, residual catalogues, manifests): **[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)**.

Copyright © 2026 Tonio Loewald. Drafting and analysis-design assistance from Google Gemini and Anthropic Claude (tools, not authors); see the pre-registration's Acknowledgments.
