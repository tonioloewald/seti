"""Generic loader for whitespace-delimited model-atmosphere grids.

Returns LinearND interpolators over (Teff, log g) for the requested columns. Used by the
white-dwarf plugin for the Bergeron grids; reusable for any tabulated model grid (e.g. a
giant-atmosphere MARCS/PHOENIX grid) by passing different column indices.
"""
import numpy as np
from scipy.interpolate import LinearNDInterpolator


def load_grid(path, col_index, teff_col=0, logg_col=1, min_cols=44,
              teff_range=(1000.0, 200000.0), logg_range=(6.5, 9.5)):
    """`col_index`: {name: column_index}. Skips header/metadata rows (fewer than
    `min_cols` whitespace tokens) and rows outside the (Teff, log g) ranges."""
    teff, logg, vals = [], [], {k: [] for k in col_index}
    for line in open(path):
        f = line.split()
        if len(f) < min_cols:
            continue
        try:
            t, g = float(f[teff_col]), float(f[logg_col])
            v = {k: float(f[i]) for k, i in col_index.items()}
        except (ValueError, IndexError):
            continue
        if not (teff_range[0] <= t <= teff_range[1] and logg_range[0] <= g <= logg_range[1]):
            continue
        teff.append(t); logg.append(g)
        for k in col_index:
            vals[k].append(v[k])
    pts = np.column_stack([teff, logg])
    return {k: LinearNDInterpolator(pts, np.array(vals[k])) for k in col_index}
