"""White-dwarf population plugin (extracted verbatim from the v1 pipeline's logic).

Natural baseline: a DA (pure-H) Bergeron/Bedard 2020 photosphere, evaluated at the
catalogue (Teff_H, log g_H) and anchored on the observed Gaia G via the
distance-independent model colour (W_n - G3). Natural regimes: warm debris disk
(300-1500 K) and cool/substellar companion (1500-4000 K); a T_x < 300 K cold fit or no
acceptable fit is the residual.
"""
import os
import numpy as np
from core.grids import load_grid
from core.sed import FBOL0
from populations.base import Population

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DA_GRID = os.path.join(_ROOT, "data", "models", "bergeron", "Table_DA")
# data-column indices in the Bergeron grid ("log g" is two header tokens, so positions
# are taken from the fixed data layout, not the header)
_COL = {"G3": 38, "W1": 17, "W2": 18, "W3": 19, "W4": 20, "Mbol": 3}
DISK = (300.0, 1500.0)
COMP = (1500.0, 4000.0)


class WhiteDwarf(Population):
    name = "white_dwarf"

    def __init__(self):
        self.interp = load_grid(_DA_GRID, _COL)

    def _tg(self, params):
        return params["teff"], np.clip(params["logg"], 7.0, 9.0), params["g_mag"]

    def predict_photometry(self, params, band):
        teff, logg, g = self._tg(params)
        B = band.upper()
        # apparent photospheric mag = G_obs + model colour (W_n - G3)
        return g + (self.interp[B](teff, logg) - self.interp["G3"](teff, logg))

    def bolometric_flux(self, params):
        teff, logg, g = self._tg(params)
        m_bol = g + (self.interp["Mbol"](teff, logg) - self.interp["G3"](teff, logg))
        return FBOL0 * 10 ** (-0.4 * m_bol)

    def regime(self, T_x):
        if not np.isfinite(T_x):
            return "fit_failed"
        if T_x < DISK[0]:
            return "cold"
        if T_x <= DISK[1]:
            return "disk"
        if T_x <= COMP[1]:
            return "companion"
        return "hot"
