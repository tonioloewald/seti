"""Population-level statistics: empirical null + genomic-control inflation, flag
threshold, Poisson zero-detection bound. Borrowed wholesale from large-scale inference
(Efron 2004; Devlin & Roeder 1999) — none of it is astronomy-specific."""
import numpy as np


def empirical_null(x):
    """Empirical null from the bulk of the data: robust location (median) and an inflated
    lower-half scale. Returns (delta0, sigma0, lambda) with lambda = sigma0**2 the
    genomic-control inflation factor (lambda≈1 means the theoretical null is adequate)."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size == 0:
        return np.nan, np.nan, np.nan
    d0 = np.median(x)
    s0 = max(d0 - np.percentile(x, 15.865), 1e-6)
    return float(d0), float(s0), float(s0 * s0)


def flag_threshold(delta0, sigma0, z=3.5):
    """Inflation-aware flag level: delta0 + z*sigma0 on the empirical-null scale."""
    return delta0 + z * sigma0


def poisson_fmax(sum_Ci, conf=3.0):
    """95% one-sided upper limit on the host fraction given zero detections over an
    effective sample size sum_Ci: f_max = conf / sum_Ci (conf=3 for 95%)."""
    return conf / sum_Ci if sum_Ci > 0 else np.inf
