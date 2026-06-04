"""The Population plugin interface.

A Population specialises the agnostic core for one class of stars by answering three
questions: what does the *bare* star look like photometrically (the natural baseline),
how bright is it bolometrically (for the upper limit), and which excess temperatures are
*natural* (disk/companion) versus a residual to chase. Everything statistical/SED-related
is supplied by `core`, identically for every population.
"""
from core.sed import WISE_F0, WISE_LAM_UM, WISE_LAM_M


class Population:
    name = "base"
    bands = ["w1", "w2", "w3", "w4"]
    F0 = WISE_F0
    lam_um = WISE_LAM_UM
    lam_m = WISE_LAM_M
    survey_depth5 = {1: 16.9, 2: 16.0, 3: 11.5, 4: 8.0}   # AllWISE 5-sigma (Vega mag)
    channels = {"excess", "variability", "transit"}

    def predict_photometry(self, params, band):
        """Predicted apparent magnitude of the *bare* star in `band`.
        `params` is a dict of equal-length arrays (e.g. teff, logg, anchor optical mag)."""
        raise NotImplementedError

    def bolometric_flux(self, params):
        """Apparent bolometric flux (W/m^2) of the bare star, for f_max."""
        raise NotImplementedError

    def regime(self, T_x):
        """Classify an excess blackbody temperature: a natural regime ('disk'/'companion'),
        a residual ('cold'), or 'hot'/'fit_failed'."""
        raise NotImplementedError
