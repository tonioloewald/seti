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


def single_event_detect(time, flux, scatter, widths_pts=(3, 5, 9, 15, 25)):
    """Aperiodic / variable-depth detector: matched-filter the light curve with box dips of
    several widths at every epoch, scoring each by its dip SNR = (depth * sqrt(w)) / scatter.
    Returns the strongest single dip and the count of significant (SNR>5) events -- catches a
    fluctuating-depth tail or a one-off dimming that a constant-depth periodic search dilutes.

    Point-based (assumes roughly uniform cadence within a sector); the production version
    windows in time across gaps. `scatter` is the outlier-blind per-point noise (core.noise).
    """
    f = np.asarray(flux, float)
    good = np.isfinite(f)
    base = np.median(f[good])
    if not np.isfinite(scatter) or scatter <= 0:
        return {"best_snr": np.nan, "n_events": 0, "best_width": 0, "best_idx": -1}
    fclean = np.where(good, f, base)
    snr_max = np.zeros(f.size)
    w_at = np.zeros(f.size, int)
    dep_at = np.zeros(f.size)
    for w in widths_pts:
        if w % 2 == 0 or w >= good.sum():
            continue                                        # odd widths only (exact length)
        pad = w // 2                                        # edge-pad with base, not zeros,
        fp = np.r_[np.full(pad, base), fclean, np.full(pad, base)]  # so boundaries aren't fake dips
        sm = np.convolve(fp, np.ones(w) / w, mode="valid")  # length == f.size
        deficit = base - sm
        snr = deficit * np.sqrt(w) / scatter                # dip SNR at each epoch
        better = snr > snr_max
        snr_max = np.where(better, snr, snr_max)
        w_at = np.where(better, w, w_at)
        dep_at = np.where(better, deficit, dep_at)
    i = int(np.argmax(snr_max))                             # per-epoch max across widths, then
    n_events = _count_runs(snr_max > 5.0)                   # count distinct dips once (no frags)
    return {"best_snr": float(snr_max[i]), "n_events": int(n_events),
            "best_width": int(w_at[i]), "best_idx": i, "best_depth": float(dep_at[i])}


def _count_runs(mask):
    """Number of contiguous True runs in a boolean array (distinct dip events)."""
    if not mask.any():
        return 0
    return int(np.sum(np.diff(np.r_[0, mask.astype(int)]) == 1))
