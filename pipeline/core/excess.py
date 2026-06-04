"""Calibrated per-band infrared-excess significance (Channel A, Stage 1) — agnostic."""
import numpy as np
from core.sed import LN10_04


def excess_chi(mag_obs, mag_pred, mag_err):
    """Per-band excess significance. Positive => observed brighter than the predicted
    bare-star photosphere (an excess). Referenced to the *observed* flux error, so it
    stays bounded by detection S/N when the photosphere is negligible (cold bands)::

        chi = (1 - f_pred/f_obs) / (ln10*0.4 * mag_err),  f_pred/f_obs = 10^(-0.4 dm)

    with dm = mag_pred - mag_obs.
    """
    dm = np.asarray(mag_pred, float) - np.asarray(mag_obs, float)
    return (1.0 - np.power(10.0, -0.4 * dm)) / (LN10_04 * np.asarray(mag_err, float))
