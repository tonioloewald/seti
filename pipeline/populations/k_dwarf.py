"""K-dwarf population plugin (Phase 2). One plugin, two channels.

Channel A (IR excess): the natural baseline is the K-dwarf *photosphere*. Lacking a stellar
  atmosphere grid in-repo, we approximate it as a blackbody at Teff anchored to the observed
  Gaia G -- a good approximation across W1-W4, which for a 3900-5300 K dwarf is the
  Rayleigh-Jeans tail. (Upgrade path: drop in a BT-Settl / PHOENIX grid via
  core.grids.load_grid, exactly as white_dwarf.py uses the Bergeron grid -- the Population
  interface is identical, so only __init__/predict_photometry change.) Natural excess
  regimes: a cold/warm debris disk and a cool stellar/substellar companion; an excess
  outside both is the residual to chase.
    Known approximation error (honest): the blackbody over-reddens the colours by ~0.2-0.3
    mag (real W1 is depressed by CO/H2O) and, more importantly, the G-anchored bolometric
    underestimates F_bol by ~1.6x (real K-dwarf BC_G ~= -0.5 vs the blackbody's +0.06,
    molecular bands depressing G relative to bolometric). This biases only the *weak*,
    self-weighting IR f_max contrast -- never Channel B -- and is the first thing the grid
    swap fixes. It is documented here so the bias is on the record, not hidden.

Channel B (transit morphology): supplies the quadratic limb-darkening coefficients -- the
  only star-specific input core.transit needs -- so the forward-modelled anomaly library and
  morphology metrics run on K-dwarf-shaped transits.

Nothing here is statistical; all of that lives in core, identically for every population.
"""
import numpy as np
from core.sed import H, C, K, SIGMA, WISE_F0, WISE_LAM_M
from populations.base import Population

# Gaia DR3 G band (Vega system): effective wavelength and zero-point flux density.
G_LAM_M = 0.6230e-6
G_F0_JY = 3228.75
JY_SI = 1e-26

# quadratic limb-darkening (a1, a2) in the TESS band vs Teff at log g ~ 4.5, solar Z
# (Claret 2017, TESS passband), linearly interpolated across the K-dwarf range.
_LD_TEFF = np.array([3900.0, 4250.0, 4600.0, 5000.0, 5300.0])
_LD_A1 = np.array([0.52, 0.49, 0.46, 0.43, 0.41])
_LD_A2 = np.array([0.16, 0.18, 0.20, 0.21, 0.22])

DISK = (40.0, 400.0)       # natural cold/warm debris disk (K)
COMP = (1500.0, 4000.0)    # natural cool stellar / substellar companion (K)


def _bnu(T, lam_m):
    """Planck B_nu(T) at wavelength lam_m (SI, W/m^2/Hz/sr)."""
    nu = C / lam_m
    return (2 * H * nu ** 3 / C ** 2) / np.expm1(H * nu / (K * np.asarray(T, float)))


class KDwarf(Population):
    name = "k_dwarf"
    survey_depth5 = {1: 16.9, 2: 16.0, 3: 11.5, 4: 8.0}    # AllWISE 5-sigma (Vega mag)

    def predict_photometry(self, params, band):
        """Apparent WISE mag of the bare K-dwarf photosphere = G + blackbody colour
        (W_n - G) at Teff. The (R/d)^2 normalisation cancels in the colour; only the
        Vega zero-points survive."""
        T = np.asarray(params["teff"], float)
        g = np.asarray(params["g_mag"], float)
        b = int(band[1])                                   # 'w1' -> 1
        color = -2.5 * np.log10(_bnu(T, WISE_LAM_M[b]) / _bnu(T, G_LAM_M)
                                * G_F0_JY / WISE_F0[b])
        return g + color

    def bolometric_flux(self, params):
        """Apparent bolometric flux (W/m^2): a blackbody anchored to the observed G.
        (R/d)^2 = F_nu,G / (pi B_nu(T,G)); F_bol = (R/d)^2 sigma T^4."""
        T = np.asarray(params["teff"], float)
        g = np.asarray(params["g_mag"], float)
        fnu_g = G_F0_JY * 10 ** (-0.4 * g) * JY_SI         # W/m^2/Hz
        solid = fnu_g / (np.pi * _bnu(T, G_LAM_M))         # (R/d)^2
        return solid * SIGMA * T ** 4

    def regime(self, T_x):
        """Classify an excess blackbody temperature. Natural: 'disk' (debris) or
        'companion' (cool star/BD). Residual: 'cold', 'warm' (the 400-1500 K gap -- too
        warm for debris, too cool for a star), 'hot', or 'fit_failed'."""
        if not np.isfinite(T_x):
            return "fit_failed"
        if T_x < DISK[0]:
            return "cold"
        if T_x <= DISK[1]:
            return "disk"
        if T_x < COMP[0]:
            return "warm"
        if T_x <= COMP[1]:
            return "companion"
        return "hot"

    # ---- Channel B -------------------------------------------------------------------
    def limb_darkening(self, teff):
        """Quadratic limb-darkening (a1, a2) in the TESS band for core.transit, the only
        star-specific input the transit forward-models and morphology metrics require."""
        return (float(np.interp(teff, _LD_TEFF, _LD_A1)),
                float(np.interp(teff, _LD_TEFF, _LD_A2)))
