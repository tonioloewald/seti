#!/usr/bin/env python3
"""Step 13: vet the flagged NEOWISE variables from the brightness-limited sample.

The expanded variability search (review point #4) covers all W1<15.5 WDs, including BARE
WDs with no static excess — so the v1 vetting (which keyed off the battery excess class)
no longer applies. Bare variable WDs have their own natural explanations, tested here:

  1. IDENTITY — SDSS spectral class (CV = cataclysmic/accreting binary; intrinsically
     variable) and SIMBAD object type (known variable / binary / etc.).
  2. BLEND/CONTAMINATION — NEOWISE's W1/W2 PSF is ~6", so a comparable-or-brighter star
     within the beam can be the true variable. The dominant false positive (the NEOWISE
     analogue of Channel B's background eclipsing binary). Flag a Gaia neighbour within
     ~6" that is not much fainter than the WD.

Anything that is isolated, spectroscopically un-flagged, and SIMBAD-quiet is a residual
to inspect more closely. source_id as STRING. Output: data/derived/variable_vetting.parquet
"""
import os, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from astropy.coordinates import SkyCoord
import astropy.units as u

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VAR = os.path.join(ROOT, "data", "derived", "variability.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
SPEC = os.path.join(ROOT, "data", "derived", "sdss_spectral.parquet")
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
OUT = os.path.join(ROOT, "data", "derived", "variable_vetting.parquet")
BEAM = 6.0   # NEOWISE W1/W2 PSF FWHM ~6"


def s(d): d["source_id"] = d["source_id"].astype(str); return d


def simbad_otype(coord):
    try:
        from astroquery.simbad import Simbad
        S = Simbad(); S.add_votable_fields("otype")
        t = S.query_region(coord, radius=6 * u.arcsec)
        return f"{t['main_id'][0]} [{t['otype'][0]}]" if (t is not None and len(t)) else "—"
    except Exception as e:
        return f"(simbad {type(e).__name__})"


def nearest_neighbour(coord, wd_g):
    """Return (sep_arcsec, dG) of the nearest Gaia source that isn't the WD itself."""
    try:
        from astroquery.gaia import Gaia
        q = (f"SELECT ra,dec,phot_g_mean_mag FROM gaiadr3.gaia_source WHERE "
             f"1=CONTAINS(POINT(ra,dec),CIRCLE(POINT({coord.ra.deg},{coord.dec.deg}),0.0056))")
        j = Gaia.launch_job(q).get_results().to_pandas()
        seps = ((j.ra - coord.ra.deg)**2 + (j.dec - coord.dec.deg)**2)**0.5 * 3600
        j = j.assign(sep=seps).sort_values("sep")
        j = j[j.sep > 0.5]                      # drop the WD itself
        if len(j) == 0:
            return np.nan, np.nan
        n = j.iloc[0]
        return float(n.sep), float(n.phot_g_mean_mag - wd_g) if np.isfinite(wd_g) else np.nan
    except Exception:
        return np.nan, np.nan


def main():
    v = s(pd.read_parquet(VAR))
    fl = v[v["variable_flag"]].copy()
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    spec = s(pd.read_parquet(SPEC)).drop_duplicates("source_id")[["source_id", "spec_class"]]
    ob = s(pd.read_parquet(OB))[["source_id", "g_mag"]]
    d = fl.merge(man, on="source_id").merge(spec, on="source_id", how="left").merge(
        ob, on="source_id", how="left").sort_values("z_J", ascending=False)
    print(f"flagged variables to vet: {len(d)}")
    rows = []
    for _, r in d.iterrows():
        c = SkyCoord(r.ra_deg, r.dec_deg, unit="deg")
        sm = simbad_otype(c)
        sep, dG = nearest_neighbour(c, r.g_mag)
        cls = str(r.spec_class)
        # verdict
        if cls == "CV":
            verdict = "CV (accreting binary) — natural"
        elif isinstance(r.spec_class, str) and r.spec_class not in ("nan",) and \
                any(k in cls for k in ("MS", "+", "STAR")):
            verdict = "binary/contaminated spectrum — natural"
        elif np.isfinite(sep) and sep < BEAM and (not np.isfinite(dG) or dG < 1.5):
            verdict = f"BLEND: Gaia neighbour {sep:.1f}\" dG={dG:+.1f} in NEOWISE beam — natural"
        elif any(k in sm for k in ["EB*", "CV*", "Variable", "RR", "binary", "**", "Sy", "WD*+"]):
            verdict = "SIMBAD known variable/binary — natural"
        else:
            verdict = "residual — isolated, unclassified (inspect)"
        rows.append({**r.to_dict(), "simbad": sm, "nbr_sep": sep, "nbr_dG": dG,
                     "verdict": verdict})
        print(f"  {r.source_id}  chi2red={r.chi2red:.1f} J={r.stetson_J:.2f} "
              f"spec={cls:>6}  nbr={sep:.1f}\"/dG={dG:+.1f}  {sm[:28]:28}  -> {verdict}",
              flush=True)
    res = pd.DataFrame(rows)
    res.to_parquet(OUT, index=False)
    nat = res["verdict"].str.contains("natural").sum()
    resid = res["verdict"].str.startswith("residual").sum()
    print(f"\n  natural (CV/binary/blend/known-variable): {nat}/{len(res)}")
    print(f"  residual (isolated, unclassified): {resid}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
