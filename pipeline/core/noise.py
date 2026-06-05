"""Outlier-blind noise characterisation and cohort assignment (pre-registration step 3a).

The per-cohort empirical null only works if a star's noise level is measured *without* its
own transit dips contaminating the estimate -- otherwise a genuinely deep anomaly inflates
its own variance, gets binned into a 'noisy' cohort, raises its own threshold, and masks
itself (the data-leak fixed in prereg s.5a). So the noise metric is the MAD of the
out-of-transit continuum after iteratively clipping *downward* excursions only.

Population-agnostic: works on any normalised light-curve flux.
"""
import numpy as np

MAD_K = 1.4826    # MAD -> Gaussian-sigma scale factor


def robust_scatter(flux, n_iter=3, clip=3.0):
    """Outlier-blind scatter: MAD of the continuum after iteratively masking points more
    than `clip` MAD *below* the median (transit dips). Upward excursions are kept -- only
    dips are removed -- so a deep transit cannot inflate the star's own noise estimate."""
    f = np.asarray(flux, float)
    keep = np.isfinite(f)
    if keep.sum() < 5:
        return np.nan
    for _ in range(n_iter):
        med = np.median(f[keep])
        mad = MAD_K * np.median(np.abs(f[keep] - med))
        if mad <= 0:
            break
        keep &= f > med - clip * mad            # drop downward outliers (dips) only
    med = np.median(f[keep])
    return float(MAD_K * np.median(np.abs(f[keep] - med)))


def cohort_edges(scatters, n_cohorts=5):
    """Fixed percentile edges that split a population's scatters into n equal-count cohorts.
    Computed once from the whole manifest (prereg s.5c) and then frozen, so later tiers
    cannot shift the binning."""
    q = np.linspace(0, 100, n_cohorts + 1)[1:-1]
    s = np.asarray(scatters, float)
    return np.percentile(s[np.isfinite(s)], q)


def assign_cohorts(scatters, edges):
    """Cohort index (0..len(edges)) for each star, by its outlier-blind scatter against the
    frozen `edges`. A quiet star lands in a low cohort and is judged against other quiet
    stars; an active star self-segregates without a hard activity cut."""
    return np.digitize(np.asarray(scatters, float), np.asarray(edges))
