"""Population-agnostic core of the anomaly-residual pipeline.

Nothing in `core` knows what kind of star it is looking at. It supplies the reusable
machinery — calibrated excess statistic, empirical-null/genomic-control calibration,
SED/blackbody helpers, the survey-depth upper limit, model-grid loading — that a
`populations` plugin specialises by providing a *natural baseline* and *natural regimes*.
"""
