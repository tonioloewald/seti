#!/usr/bin/env python3
"""Phase 2, step 4 battery: identity / known-object cross-check (prereg §5).

The registered battery uses prior knowledge as a *filter*: a candidate that coincides with a
known planet, TESS Object of Interest, eclipsing binary, or catalogued variable is *explained
away*, never used to assume the residual set is empty. This stage cross-matches the raw T0
residual list (k04) against:

  - NASA Exoplanet Archive confirmed planets (pscomppars)
  - TESS Objects of Interest (toi)
  - SIMBAD object types (eclipsing binaries, variables, etc.)

A residual matching any of these is annotated as explained; the survivors (no known identity)
pass to the difference-image centroid gate (k06). Coordinates come from the frozen manifest.

Output: data/manifests/kdwarf_T0_residuals_identity.csv  (residuals + identity annotation)
"""
import os, sys, io, time, json, urllib.parse, urllib.request, warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from astropy.coordinates import SkyCoord
import astropy.units as u

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.environ.get("KRUN", "T0")            # T0 (default) | T0T1 (combined)
MAN = os.path.join(ROOT, "data", "manifests", "kdwarf_sample.csv.gz")
RESID = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals.csv")
OUT = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals_identity.csv")
RAW = os.path.join(ROOT, "data", "raw", "exoarchive")
TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
MATCH_RADIUS = 6.0          # arcsec: same-source identification
# SIMBAD object-type codes that genuinely EXPLAIN a periodic dip. A code that merely
# identifies the star (PM* high proper motion, Em* emission, X X-ray, Star, *) is NOT an
# explanation and must survive to the centroid gate -- prior knowledge filters, never assumes.
EB_CODES = {"EB*", "Al*", "bL*", "WU*", "EclBin"}                         # eclipsing binaries
BIN_CODES = {"SB*", "**", "El*", "RS*", "SB?", "**?"}                     # binaries (can eclipse)
VAR_CODES = {"BY*", "RotV*", "RotV", "V*", "Pu*", "Ce*", "RR*", "dS*",    # variables
             "Mi*", "LP*", "sr*", "Er*", "Or*", "TT*", "a2*", "Ro*", "Fl*"}


def tap_csv(query, dest):
    os.makedirs(RAW, exist_ok=True)
    if not os.path.exists(dest):
        url = f"{TAP}?query={urllib.parse.quote(query)}&format=csv"
        print(f"  fetching {os.path.basename(dest)} ...", flush=True)
        with urllib.request.urlopen(url, timeout=180) as r:
            open(dest, "wb").write(r.read())
    return pd.read_csv(dest)


def cone_match(res, cat, radius_as):
    """Boolean mask: which residuals lie within radius of any catalogue source."""
    if len(cat) == 0:
        return np.zeros(len(res), bool)
    rc = SkyCoord(res["ra_deg"].to_numpy()*u.deg, res["dec_deg"].to_numpy()*u.deg)
    cc = SkyCoord(cat["ra"].to_numpy()*u.deg, cat["dec"].to_numpy()*u.deg)
    _, sep, _ = rc.match_to_catalog_sky(cc)
    return sep.arcsec < radius_as


def simbad_otype(coord):
    try:
        from astroquery.simbad import Simbad
        s = Simbad(); s.add_votable_fields("otype")
        t = s.query_region(coord, radius=MATCH_RADIUS * u.arcsec)
        if t is None or len(t) == 0:
            return ""
        return str(t["otype"][0])
    except Exception:
        return "err"


def main():
    res = pd.read_csv(RESID, dtype={"source_id": str})
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    res = res.merge(man, on="source_id", how="left")
    print(f"raw residuals: {len(res)}", flush=True)

    # ---- catalogue cross-matches (confirmed planets, TOIs) -----------------------------
    planets = tap_csv("select ra,dec,pl_name from pscomppars",
                      os.path.join(RAW, "confirmed_planets.csv"))
    tois = tap_csv("select ra,dec,toi from toi", os.path.join(RAW, "toi.csv"))
    res["known_planet"] = cone_match(res, planets, MATCH_RADIUS)
    res["known_toi"] = cone_match(res, tois, MATCH_RADIUS)
    print(f"  confirmed-planet matches: {res['known_planet'].sum()} | "
          f"TOI matches: {res['known_toi'].sum()}", flush=True)

    # ---- SIMBAD object types for the rest (parallel) -----------------------------------
    todo = res[~(res["known_planet"] | res["known_toi"])]
    print(f"  SIMBAD query for {len(todo)} remaining ...", flush=True)
    otypes = {}; t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(simbad_otype, SkyCoord(r.ra_deg*u.deg, r.dec_deg*u.deg)): r.source_id
                for r in todo.itertuples()}
        for i, fut in enumerate(as_completed(futs)):
            otypes[futs[fut]] = fut.result()
            if (i+1) % 200 == 0:
                print(f"    simbad {i+1}/{len(todo)} ({time.time()-t0:.0f}s)", flush=True)
    res["simbad_otype"] = res["source_id"].map(otypes).fillna("")

    def classify(r):
        if r["known_planet"]:
            return "known_planet"
        if r["known_toi"]:
            return "known_TOI"
        ot = str(r["simbad_otype"]).strip()
        if ot in EB_CODES:
            return "known_eclipsing_binary"
        if ot in BIN_CODES:
            return "known_binary"
        if ot in VAR_CODES:
            return "known_variable"
        return "unknown"          # PM*/Em*/X/Star/* identify the star, not the dip -> survive
    res["identity"] = res.apply(classify, axis=1)
    res.to_csv(OUT, index=False)

    vc = res["identity"].value_counts()
    print("\n=== IDENTITY CROSS-CHECK ===")
    for k, n in vc.items():
        print(f"  {k:28s} {n}")
    surv = res[res["identity"] == "unknown"]
    print(f"\n  {len(surv)} residuals survive identity (no known planet/EB/variable) -> centroid gate (k06).")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
