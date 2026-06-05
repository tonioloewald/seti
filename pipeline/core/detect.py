"""Transit detection statistics (pre-registration steps 3b/3c, channel B).

Two detectors run in parallel (prereg s.4): BLS for periodic box/U transits -- the primary
gate that catches anything planet-shaped regardless of exotic morphology -- and an aperiodic
single-event / variable-depth matched filter that does NOT assume a constant depth or strict
periodicity, so a disintegrating dust tail or a one-off deep dip is not silently discarded as
noise. Neither depends on morphology; morphology (core.transit) characterises survivors.

Population-agnostic: both operate on a normalised light curve. Detection statistics are
returned raw; the empirical-null calibration (core.stats / core.noise) turns them into a
family-wise threshold.
"""
import numpy as np
from astropy.timeseries import BoxLeastSquares


def bls_detect(time, flux, periods, durations):
    """Box-Least-Squares periodic search. Returns the best period/depth/duration/epoch and
    the signal-detection-efficiency SDE = (peak - median)/std of the power spectrum -- the
    per-star detection statistic whose empirical null sets the threshold."""
    t = np.asarray(time, float)
    f = np.asarray(flux, float)
    m = np.isfinite(t) & np.isfinite(f)
    bls = BoxLeastSquares(t[m], f[m])
    pg = bls.power(periods, durations)
    p = np.asarray(pg.power, float)
    i = int(np.argmax(p))
    sde = float((p[i] - np.median(p)) / (np.std(p) + 1e-12))
    return {"period": float(pg.period[i]), "duration": float(pg.duration[i]),
            "depth": float(pg.depth[i]), "t0": float(pg.transit_time[i]),
            "depth_snr": float(pg.depth_snr[i]), "sde": sde}


def single_event_detect(time, flux, scatter, durations_d=(0.05, 0.1, 0.2, 0.4, 0.8),
                        min_pts=3, snr_floor=5.0):
    """Aperiodic / variable-depth detector, **gap-aware** (windows in real time, not point
    indices): for each trial box duration (days) and each epoch as box centre, sum the flux
    deficit over the points that actually fall within +/- duration/2 in time, and score by the
    dip SNR = depth * sqrt(n_in_box) / scatter. Catches a fluctuating-depth tail or a one-off
    dimming that a constant-depth periodic search dilutes; robust to the gaps and uneven
    cadence of real TESS/Kepler light curves (a box spanning a data gap is scored by the
    points it truly contains, not by index width).

    `scatter` is the outlier-blind per-point noise (core.noise.robust_scatter). Returns the
    strongest single dip and the count of distinct significant (SNR>snr_floor) events.
    Vectorised per duration via searchsorted + cumulative sums.
    """
    t = np.asarray(time, float)
    f = np.asarray(flux, float)
    m = np.isfinite(t) & np.isfinite(f)
    t, f = t[m], f[m]
    if t.size < min_pts or not np.isfinite(scatter) or scatter <= 0:
        return {"best_snr": np.nan, "n_events": 0, "best_duration": 0.0, "best_time": np.nan,
                "best_depth": np.nan}
    o = np.argsort(t); t, f = t[o], f[o]
    base = np.median(f)
    csum = np.concatenate([[0.0], np.cumsum(f)])            # prefix sums for O(1) window means
    snr_max = np.zeros(t.size)
    dur_at = np.zeros(t.size)
    dep_at = np.zeros(t.size)
    for W in durations_d:
        lo = np.searchsorted(t, t - W / 2.0, side="left")  # window [t-W/2, t+W/2] per centre
        hi = np.searchsorted(t, t + W / 2.0, side="right")
        n = hi - lo
        ok = n >= min_pts
        mean = np.where(ok, (csum[hi] - csum[lo]) / np.maximum(n, 1), base)
        deficit = base - mean
        snr = np.where(ok, deficit * np.sqrt(n) / scatter, 0.0)
        better = snr > snr_max
        snr_max = np.where(better, snr, snr_max)
        dur_at = np.where(better, W, dur_at)
        dep_at = np.where(better, deficit, dep_at)
    i = int(np.argmax(snr_max))
    n_events = _count_runs(snr_max > snr_floor)
    return {"best_snr": float(snr_max[i]), "n_events": int(n_events),
            "best_duration": float(dur_at[i]), "best_time": float(t[i]),
            "best_depth": float(dep_at[i])}


def _count_runs(mask):
    """Number of contiguous True runs in a boolean array (distinct dip events)."""
    if not mask.any():
        return 0
    return int(np.sum(np.diff(np.r_[0, mask.astype(int)]) == 1))
