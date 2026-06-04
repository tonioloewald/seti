"""Spectral-energy-distribution helpers and photometric constants (population-agnostic).

Defaults are the WISE system, but every function takes the zero-points / wavelengths as
arguments so a different survey (or a giant-atmosphere search) can pass its own.
"""
import numpy as np

# physical constants (SI)
H, C, K, SIGMA = 6.62607e-34, 2.99792458e8, 1.380649e-23, 5.670374e-8
HCK = 14387.77                      # h c / k in um*K
FBOL0 = 2.518e-8                    # W/m^2 for apparent m_bol = 0 (IAU 2015)
LN10_04 = 0.4 * np.log(10.0)        # d(flux)/flux per magnitude

# WISE photometric system
WISE_F0 = {1: 309.540, 2: 171.787, 3: 31.674, 4: 8.363}          # Vega zero-points (Jy)
WISE_LAM_UM = {1: 3.3526, 2: 4.6028, 3: 11.5608, 4: 22.0883}      # band eff. wavelength (um)
WISE_LAM_M = {b: v * 1e-6 for b, v in WISE_LAM_UM.items()}


def mag_to_fnu(mag, band, F0=WISE_F0):
    """Vega magnitude -> flux density (Jy)."""
    return F0[band] * 10 ** (-0.4 * np.asarray(mag, float))


def bb_fraction(band, T, lam_m=WISE_LAM_M):
    """pi*B_nu(nu_band, T) / (sigma T^4) in Jy per unit apparent bolometric flux (W/m^2).

    i.e. the band flux density produced by an excess that reprocesses one W/m^2 of
    bolometric flux as a temperature-T blackbody."""
    nu = C / lam_m[band]
    Bnu = (2 * H * nu**3 / C**2) / np.expm1(H * nu / (K * T))
    return np.pi * Bnu / (SIGMA * T**4) * 1e26


def fit_excess_bb(lam_um, fexc, sig, Tgrid=None):
    """Best (T, Omega>=0) blackbody for excess fluxes; returns (chi2, T_x, Omega, dof)."""
    lam = np.asarray(lam_um, float); fexc = np.asarray(fexc, float); sig = np.asarray(sig, float)
    if Tgrid is None:
        Tgrid = np.logspace(np.log10(40.0), np.log10(5000.0), 200)
    best = (np.inf, np.nan, np.nan)
    for T in Tgrid:
        B = (1.0 / lam**3) / np.expm1(HCK / (lam * T))
        denom = np.sum(B * B / sig**2)
        Om = max(np.sum(fexc * B / sig**2) / denom if denom > 0 else 0.0, 0.0)
        chi2 = np.sum(((fexc - Om * B) / sig) ** 2)
        if chi2 < best[0]:
            best = (chi2, T, Om)
    return best[0], best[1], best[2], len(lam) - 1
