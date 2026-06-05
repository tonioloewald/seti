"""Population-agnostic transit forward-models and morphology metrics (Channel B).

The point of Channel B's injection-recovery is NOT to calibrate completeness on box
transits and hope the morphology metrics fire on everything else. We forward-model an
explicit *library* of anomaly shapes and a natural-planet negative control, so that

  (1) per-star completeness C_i -- and therefore f_max = 3/Sum(C_i) -- is reported
      *per morphology family*, not collapsed onto a single box (a flat occulter is
      easy; a subtle asymmetric louver is not, and the limit must say so); and
  (2) the morphology metrics are *validated* to separate the anomalous families from
      the natural-planet locus, with the noise level at which separation fails made
      explicit (the cadence/SNR caveat, quantified).

Geometry is exact: an opaque (or graded-opacity) mask is swept across a quadratically
limb-darkened stellar disk and the blocked surface brightness is integrated on a grid.
Any shape -- circle, tilted rectangle ("louver"), triangle, head+dust-tail -- is just a
different mask, so the same code path produces the natural baseline and every anomaly.

Nothing here knows what kind of star it is: the population plugin supplies the limb-
darkening coefficients (band-dependent) and the transit depth scale; everything else is
identical for white dwarfs, K dwarfs, or giants.
"""
import numpy as np

# Default quadratic limb-darkening (TESS band, K-dwarf-ish; Claret 2017). A plugin
# overrides these per population/band -- they are *inputs*, not constants of the search.
LD_TESS_KDWARF = (0.45, 0.20)


def _disk(npix, u1, u2):
    """Normalised limb-darkened stellar brightness on an npix x npix grid over [-1,1]^2.
    Quadratic law I(mu) = 1 - u1(1-mu) - u2(1-mu)^2, mu = sqrt(1-r^2). Sums to 1."""
    ax = np.linspace(-1.0, 1.0, npix)
    X, Y = np.meshgrid(ax, ax)
    r2 = X * X + Y * Y
    inside = r2 < 1.0
    mu = np.sqrt(np.clip(1.0 - r2, 0.0, 1.0))
    I = np.where(inside, 1.0 - u1 * (1.0 - mu) - u2 * (1.0 - mu) ** 2, 0.0)
    s = I.sum()
    return X, Y, I / s


def _mask_circle(X, Y, xc, yc, rp):
    return (X - xc) ** 2 + (Y - yc) ** 2 < rp * rp


def _mask_rect(X, Y, xc, yc, w, h, theta):
    c, s = np.cos(-theta), np.sin(-theta)
    xr = c * (X - xc) - s * (Y - yc)
    yr = s * (X - xc) + c * (Y - yc)
    return (np.abs(xr) < w / 2.0) & (np.abs(yr) < h / 2.0)


def _mask_triangle(X, Y, xc, yc, size, theta):
    # right-ish triangle, vertices give a leading point and a trailing flat edge ->
    # asymmetric ingress/egress. Barycentric point-in-triangle test.
    v = np.array([[size, 0.0], [-size, size * 0.8], [-size, -size * 0.8]])
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    v = v @ R.T + np.array([xc, yc])
    (x1, y1), (x2, y2), (x3, y3) = v
    d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    a = ((y2 - y3) * (X - x3) + (x3 - x2) * (Y - y3)) / d
    b = ((y3 - y1) * (X - x3) + (x1 - x3) * (Y - y3)) / d
    g = 1.0 - a - b
    return (a >= 0) & (b >= 0) & (g >= 0)


def _opacity_tail(X, Y, xc, yc, rp, tail_len, tau0):
    """Graded opacity: opaque head (circle) + exponential dust tail trailing in -x.
    Returns a transmission-deficit field in [0,1] (1 = fully opaque)."""
    head = _mask_circle(X, Y, xc, yc, rp).astype(float)
    near_y = np.exp(-((Y - yc) ** 2) / (2 * (rp * 1.3) ** 2))
    behind = (X < xc)
    tail = behind * near_y * (1.0 - np.exp(-tau0 * np.exp((X - xc) / tail_len)))
    return np.clip(np.maximum(head, tail), 0.0, 1.0)


def _lightcurve(maskfun, b, x_path, npix, u1, u2, depth_scale):
    """Sweep a mask (function of grid + head-x) across the disk at impact parameter b;
    return blocked-flux fraction at each x, scaled so peak depth == depth_scale."""
    X, Y, I = _disk(npix, u1, u2)
    raw = np.array([(I * maskfun(X, Y, xc, b)).sum() for xc in x_path])
    peak = raw.max()
    if peak <= 0:
        return np.zeros_like(raw)
    return raw / peak * depth_scale


def make_transit(kind, depth=0.01, b=0.1, rp=0.1, npix=300, n=181,
                 ld=LD_TESS_KDWARF, span=1.6, **kw):
    """Forward-model one transit. Returns (phase, flux) with phase in [-0.5,0.5]*span
    (transit centred at 0) and flux normalised to 1 out of transit.

    kind: 'planet'  -- limb-darkened circular disk (natural negative control, U-shape)
          'box'     -- opaque circular disk (flat floor; easy anomaly / megastructure)
          'louver'  -- tilted thin opaque rectangle (Arnold-type asymmetric flat floor)
          'triangle'-- opaque triangle (strong ingress/egress asymmetry)
          'tail'    -- opaque head + exponential dust tail (KIC 12557548-like; pair with
                       per-epoch depth variation via multi_epoch_depths()).
    """
    u1, u2 = ld
    x = np.linspace(-span, span, n)            # head-x crossing the disk
    if kind == "planet":
        f = 1.0 - _lightcurve(lambda X, Y, xc, yc: _mask_circle(X, Y, xc, yc, rp),
                              b, x, npix, u1, u2, depth)
    elif kind == "box":
        # opaque disk but read against a *flat* (no-LD) floor: same circle mask, the
        # flat bottom emerges because a large opaque disk covers near-limb annuli too.
        f = 1.0 - _lightcurve(lambda X, Y, xc, yc: _mask_circle(X, Y, xc, yc, rp),
                              b, x, npix, 0.0, 0.0, depth)
    elif kind == "louver":
        w, h, th = kw.get("w", 0.06), kw.get("h", 0.5), kw.get("theta", 0.6)
        f = 1.0 - _lightcurve(lambda X, Y, xc, yc: _mask_rect(X, Y, xc, yc, w, h, th),
                              b, x, npix, u1, u2, depth)
    elif kind == "triangle":
        sz, th = kw.get("size", 0.18), kw.get("theta", 0.0)
        f = 1.0 - _lightcurve(lambda X, Y, xc, yc: _mask_triangle(X, Y, xc, yc, sz, th),
                              b, x, npix, u1, u2, depth)
    elif kind == "tail":
        tl, tau = kw.get("tail_len", 0.25), kw.get("tau0", 3.0)
        f = 1.0 - _lightcurve(
            lambda X, Y, xc, yc: _opacity_tail(X, Y, xc, yc, rp, tl, tau),
            b, x, npix, u1, u2, depth)
    else:
        raise ValueError(f"unknown transit kind: {kind!r}")
    return x / (2 * span), f


def inject_periodic(time, kind, depth, period, t0, duration, ld=LD_TESS_KDWARF,
                    epoch_depths=None, **kw):
    """Multiplicative transit signal sampled onto `time`: tile a forward-modelled template
    (make_transit) at `period`/`t0`, each transit `duration` (days) wide. Returns a flux
    factor (~1 out of transit, dipping in) to multiply into a light curve. `epoch_depths`
    (from multi_epoch_depths) scales each epoch independently for a disintegrating body."""
    tph, tfl = make_transit(kind, depth=depth, ld=ld, **kw)        # template in [-0.5,0.5]
    t = np.asarray(time, float)
    frac = ((t - t0) / period + 0.5) % 1.0 - 0.5                   # orbital phase [-0.5,0.5)
    tphase = frac * period / (2.0 * duration)                     # template spans 2*duration
    inj = np.interp(tphase, tph, tfl, left=1.0, right=1.0)
    if epoch_depths is not None:                                   # per-epoch depth scaling
        ep = np.floor((t - t0) / period + 0.5).astype(int)
        ep0 = ep - ep.min()
        scale = np.where(ep0 < len(epoch_depths), epoch_depths[np.clip(ep0, 0, len(epoch_depths)-1)] / depth, 1.0)
        inj = 1.0 - (1.0 - inj) * scale
    return inj


def multi_epoch_depths(n_epochs, mean_depth, cv=0.6, dropout=0.15, rng=None):
    """Per-epoch depth sequence for a disintegrating body: lognormal scatter (coeff. of
    variation cv) plus a dropout fraction of near-zero epochs. Used to drive 'tail'
    injections so the variable-depth detector and depth-CV metric are exercised."""
    rng = np.random.default_rng(0) if rng is None else rng
    sigma = np.sqrt(np.log(1 + cv * cv))
    d = mean_depth * np.exp(rng.normal(-sigma * sigma / 2, sigma, n_epochs))
    d[rng.random(n_epochs) < dropout] *= 0.05
    return d


# ---- morphology metrics (computed on a single folded/processed transit) --------------

def metrics(phase, flux):
    """Morphology discriminants for one transit. All are dimensionless and defined so a
    natural limb-darkened planet sits near zero on the anomaly axes.

      depth          : 1 - min(flux)
      flat_bottom    : fraction of in-transit flux within the deepest 10% of the dip
                       (box/occulter -> high; limb-darkened U -> low)  [box-vs-U]
      asymmetry      : |normalised 3rd moment (skew)| of the flux-deficit vs time
                       (triangle/tail -> high; symmetric box/planet -> ~0)
      duration_frac  : fraction of the window in transit (duty-cycle proxy)
    """
    f = np.asarray(flux, float)
    t = np.asarray(phase, float)
    # robust bright baseline = median of the top quartile (always non-empty, immune to a
    # flat 1.0 out-of-transit level that an empty `f > pctl` selection would NaN out).
    fs = np.sort(f)
    base = np.median(fs[-max(5, f.size // 4):])
    # robust floor = median of the deepest ~5% (NOT the single min, which one negative
    # noise spike would inflate, destabilising flat_bottom on a folded profile).
    floor = np.median(fs[:max(3, f.size // 20)])
    d = base - floor
    out = {"depth": float(d)}
    if d <= 0 or not np.isfinite(d):
        return {**out, "flat_bottom": np.nan, "asymmetry": np.nan, "duration_frac": np.nan}
    deficit = np.clip(base - f, 0.0, None)
    intransit = deficit > 0.5 * d
    out["duration_frac"] = float(intransit.mean())
    # box-vs-U: fraction of in-transit flux sitting within the deepest 10% of the dip
    out["flat_bottom"] = float((deficit > 0.9 * d).sum() / max(intransit.sum(), 1))
    # asymmetry: offset of the full deficit-centroid from the midpoint of the deep core
    # (the >half-depth window), in units of the core half-width. A symmetric box/planet
    # gives ~0 (centroid sits at the core centre); a disintegrating tail's low, extended
    # egress trail pulls the centroid past the core -> large. Robust to a flat floor,
    # where a single argmin would jitter, because it uses integrated deficit, not a point.
    core = f < (base - 0.5 * d)
    if core.sum() < 2:
        out["asymmetry"] = np.nan
        return out
    j = np.where(core)[0]
    t_mid = 0.5 * (t[j[0]] + t[j[-1]])
    half_width = 0.5 * (t[j[-1]] - t[j[0]])
    t_cen = np.sum(deficit * t) / np.sum(deficit)
    out["asymmetry"] = float(abs(t_cen - t_mid) / (half_width + 1e-12))
    return out
