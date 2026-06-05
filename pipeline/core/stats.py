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


def _norm_ppf(u):
    """Standard-normal inverse CDF (quantile) via Acklam's rational approximation -- z such
    that P(Z<z)=u. No scipy dependency."""
    if not (0.0 < u < 1.0):
        return -np.inf if u <= 0 else np.inf
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if u < plow:
        x = np.sqrt(-2 * np.log(u))
        return (((((c[0]*x+c[1])*x+c[2])*x+c[3])*x+c[4])*x+c[5]) / ((((d[0]*x+d[1])*x+d[2])*x+d[3])*x+1)
    if u > phigh:
        x = np.sqrt(-2 * np.log(1 - u))
        return -(((((c[0]*x+c[1])*x+c[2])*x+c[3])*x+c[4])*x+c[5]) / ((((d[0]*x+d[1])*x+d[2])*x+d[3])*x+1)
    x = u - 0.5
    r = x * x
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*x / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def _norm_isf(p):
    """Inverse survival function: z such that P(Z>z)=p."""
    return _norm_ppf(1.0 - p)


def fwer_sigma(n_total):
    """Gaussian-equivalent family-wise threshold z so the expected number of pure-noise
    false alarms across n_total stars is < 1: z = Phi^{-1}(1 - 1/n_total). The per-star BLS
    SDE already maxes over that star's period/phase trials, so its empirical null absorbs the
    *within*-star look-elsewhere; only the cross-star n_total factor remains here."""
    return _norm_isf(1.0 / n_total)


def cohort_threshold(delta0, sigma0, n_total):
    """Per-cohort detection threshold on the empirical-null scale: delta0 + z*sigma0 with
    z = fwer_sigma(n_total). Genomic-control inflation is already baked into sigma0, so a
    heavy-tailed cohort gets a proportionally higher bar -- the quiet cohorts are not
    penalised for it."""
    return delta0 + fwer_sigma(n_total) * sigma0
