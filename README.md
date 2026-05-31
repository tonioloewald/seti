# SETI: An Anomaly-Residual Search for Signs of Persistence Around White Dwarfs

A pre-registered, open search for **persistent departures from the natural behavior of cooling stellar remnants** — anomalies that resist explanation by known astrophysics — around catalogued white dwarfs.

> We make **no assumptions about how a long-lived civilization arises, what it wants, or what it builds** (no Dyson spheres, no energy-maximization, no efficiency/resilience optimization). We look for *something that fails to look like known nature*, then try to explain it away. The most likely interesting outcome is not life but **new natural astrophysics**; the most likely outcome overall is a clean null, which yields a quantitative upper limit. See [`preregistration.md`](preregistration.md).

## Status

🔒 **Pre-registration draft — NOT yet registered.** No project-specific data analysis has been run.

This repository is **private** until the pre-registration is timestamped on the Open Science Framework (OSF). Once registered, it becomes **public**, and its commit history serves as an independent, public record that all analysis post-dates the locked plan.

## Why this design

- **Pre-registration first.** The hypotheses, sample cuts, natural-explanation battery, and scoring rule are fixed *before* any data is touched, so we cannot reason toward a result post hoc.
- **Anomaly-residual, not assume-the-signal.** Unlike "listen for a beacon we'd recognize" approaches (whose technology assumptions fail when the technology isn't the one we imagined), we only assume an anomaly leaves *some* imprint in channels we already survey.
- **Null is a success.** A clean null produces a publishable upper limit; surviving anomalies are published as unexplained, most likely as new natural phenomena. Success never depends on detecting intelligence.

## Repository layout

| Path | Contents |
|------|----------|
| [`preregistration.md`](preregistration.md) | The locked pre-registration document (the heart of the project) |
| [`docs/`](docs/) | Background notes, including the original project brief |
| [`data/`](data/) | Frozen, checksummed sample manifests (Gaia source IDs + cuts). Bulk/derived data is **not** tracked. |
| [`pipeline/`](pipeline/) | Analysis code (sample selection, cross-match, SED fitting, anomaly scoring) — to be developed **after** registration |
| [`notebooks/`](notebooks/) | Exploratory and sensitivity-analysis notebooks |

## Open-science commitments

1. The pre-registration is timestamped on OSF before any project-specific data analysis.
2. All code, queries, the frozen sample manifest, the natural-explanation battery, and the residual catalogue are released here, with history post-dating registration.
3. Amendments to the registered plan are public, dated, and rationale-bearing; superseded versions are retained.

## License

- **Code** (`pipeline/`, notebooks, scripts): **Apache-2.0** — see [`LICENSE`](LICENSE). Chosen over MIT for its explicit patent grant and patent-retaliation clause.
- **Documents and data products** (the pre-registration, `docs/`, residual catalogues, manifests): **[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)**.

Copyright © 2026 Tonio Loewald. Drafting and analysis-design assistance from Google Gemini and Anthropic Claude (tools, not authors); see the pre-registration's Acknowledgments.
