#!/usr/bin/env python3
"""Reproducible physical-sanity checks for the K-dwarf plugin (no data needed).

There is no committed K-dwarf reference to regression-test against yet (the sample is not
pulled until after the OSF freeze), so this asserts that the plugin's *physics* is sane:
IR colours redden monotonically into the WISE bands, the bolometric anchor is positive and
within a documented factor of the blackbody expectation, regime boundaries classify as
specified, and the limb-darkening interpolation is monotone across the K-dwarf range.
"""
import os, sys
import numpy as np

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPE)
from core.sed import FBOL0                                  # noqa: E402
from populations.k_dwarf import KDwarf, DISK, COMP          # noqa: E402


def main():
    kd = KDwarf()
    p = {"teff": np.array([4600.0]), "g_mag": np.array([10.0])}
    w = {b: float(kd.predict_photometry(p, b)[0]) for b in ["w1", "w2", "w3", "w4"]}

    # (1) photospheric colours redden monotonically G->W1->...->W4 (Rayleigh-Jeans)
    gw = [10.0 - w[b] for b in ["w1", "w2", "w3", "w4"]]
    assert all(np.diff(gw) > 0), f"G-W colours not monotonically reddening: {gw}"

    # (2) bolometric flux positive; m_bol within a documented 1 mag of G (blackbody BC)
    fbol = float(kd.bolometric_flux(p)[0])
    mbol = -2.5 * np.log10(fbol / FBOL0)
    assert fbol > 0 and abs(mbol - 10.0) < 1.0, f"bolometric anchor off: m_bol={mbol:.2f}"

    # (3) regime boundaries classify as specified
    assert kd.regime((DISK[0] + DISK[1]) / 2) == "disk"
    assert kd.regime((DISK[1] + COMP[0]) / 2) == "warm"      # the residual gap
    assert kd.regime((COMP[0] + COMP[1]) / 2) == "companion"
    assert kd.regime(DISK[0] - 10) == "cold"
    assert kd.regime(COMP[1] + 1000) == "hot"
    assert kd.regime(np.nan) == "fit_failed"

    # (4) limb darkening monotone and bracketed across the K-dwarf range
    a1 = [kd.limb_darkening(t)[0] for t in (3900, 4600, 5300)]
    assert a1[0] > a1[1] > a1[2], f"LD a1 not monotone in Teff: {a1}"

    print("K-dwarf plugin sanity checks PASS")
    print(f"  4600 K, G=10:  " + "  ".join(f"{b.upper()}={w[b]:.2f}" for b in w))
    print(f"  G-W colours (redden): {[round(x,2) for x in gw]}")
    print(f"  m_bol={mbol:.2f} (BC_G={mbol-10:+.2f}; blackbody approx, see docstring)")
    print(f"  LD a1 @ (3900,4600,5300) K: {[round(x,2) for x in a1]}")


if __name__ == "__main__":
    main()
