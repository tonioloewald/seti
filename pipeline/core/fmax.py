"""Survey-depth zero-detection upper limit f_max(T_x, f) (§5.7) — agnostic."""
import numpy as np
from core.sed import bb_fraction, mag_to_fnu, WISE_F0
from core.stats import poisson_fmax


def survey_fmax(F_bol, T_grid, f_grid, depth5, F0=WISE_F0, bands=(1, 2, 3, 4)):
    """Zero-detection bound over a population.

    F_bol  : per-object apparent bolometric flux (W/m^2) of the bare star.
    depth5 : {band: 5-sigma limiting magnitude}.
    A star *constrains* an excess of temperature T and luminosity fraction f if that
    excess would exceed the 5-sigma depth in some band; f_max = 3 / sum_i C_i.
    Returns a list of {T_x_K, f_lum, sum_Ci, f_max}.
    """
    F_bol = np.asarray(F_bol, float); F_bol = F_bol[np.isfinite(F_bol)]
    depth_jy = {b: float(mag_to_fnu(depth5[b], b, F0)) for b in bands}
    rows = []
    for T in T_grid:
        thresh = min(depth_jy[b] / bb_fraction(b, T) for b in bands)   # W/m^2 at f=1
        for f in f_grid:
            sumC = int(np.sum(F_bol >= thresh / f))
            rows.append({"T_x_K": T, "f_lum": f, "sum_Ci": sumC, "f_max": poisson_fmax(sumC)})
    return rows
