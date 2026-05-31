# Frozen sample manifests

This directory holds the **immutable, checksummed** sample definitions referenced in
[`../../preregistration.md`](../../preregistration.md) §3.

A manifest is the exact list of *Gaia* source IDs (plus the selection thresholds that
produced it) that constitutes the registered target sample. Once committed at registration
time, a manifest is **never edited in place** — any change to the sample is made via a new,
dated manifest accompanied by a documented amendment to the pre-registration.

Each manifest should be accompanied by:
- a checksum (e.g. `SHA256SUMS`) of the manifest file, and
- a short header recording the parent catalogue version (Gaia EDR3), the `P_WD` cut, and all
  quality cuts applied.

Bulk photometry and derived SED/light-curve products are **not** stored here (see `.gitignore`).
