#!/usr/bin/env python3
"""Step 9: Channel B — difference-image centroid (BEB) vetting (§5.2 item 9).

The mandatory final test for a transit-shaped candidate. TESS pixels are 21", so an
eclipsing binary up to ~1' away bleeds into the target's aperture and mimics a shallow
transit (a "background eclipsing binary", BEB). Difference imaging localises the source
of the flux dip: build the mean pixel image IN transit and OUT of transit; the difference
(out - in) is positive wherever flux dropped during the event. The flux-weighted centroid
of that difference image is the *physical location of the variable source*.

  - centroid on the target white dwarf  -> signal is on-target (cannot be explained away
    as a blend; would warrant real follow-up);
  - centroid offset toward a neighbour  -> background/blended eclipsing binary = natural.

For each finalist: download the SPOC target-pixel file for the discovery sector, rebuild
the light curve, re-derive the BLS ephemeris (period, t0, duration), form the difference
image, measure the centroid offset from the WD, and overlay Gaia neighbours.

source_id handled as STRING throughout. Output: figures/centroid_vet.png + verdicts.
"""
import os, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from lightkurve import search_targetpixelfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "data", "derived", "transit_search.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
FIG = os.path.join(ROOT, "figures", "centroid_vet.png")
PIXSCALE = 21.0  # arcsec / TESS pixel
FINALISTS = ["2660358032257156736", "6348672845649310464", "5274517467840296832"]


def gaia_neighbours(ra, dec, radius_arcsec=60):
    from astroquery.gaia import Gaia
    q = (f"SELECT ra, dec, phot_g_mean_mag FROM gaiadr3.gaia_source WHERE "
         f"1=CONTAINS(POINT(ra,dec),CIRCLE(POINT({ra},{dec}),{radius_arcsec/3600.0}))")
    return Gaia.launch_job(q).get_results().to_pandas()


def vet_one(ax, sid, ra, dec, period_hint):
    coord = SkyCoord(ra, dec, unit="deg")
    sr = search_targetpixelfile(coord, mission="TESS", radius=5 * u.arcsec)
    sub = sr[[a == "SPOC" for a in sr.table["author"]]]
    if len(sub) == 0:
        ax.set_title(f"{sid}\n(no SPOC TPF)", fontsize=8); return dict(sid=sid, verdict="no TPF")
    tpf = sub[0].download(quality_bitmask="default")
    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask).remove_nans()
    flat = lc.flatten(window_length=401).remove_outliers(sigma=5)
    pg = flat.to_periodogram(method="bls",
                             period=np.arange(max(0.2, period_hint*0.5), period_hint*1.5, 0.0008),
                             duration=np.array([0.005, 0.01, 0.02, 0.04, 0.08]))
    period = pg.period_at_max_power.value
    t0 = pg.transit_time_at_max_power.value
    dur = max(pg.duration_at_max_power.value, 0.02)

    t = tpf.time.value
    phase = ((t - t0 + 0.5 * period) % period) - 0.5 * period
    intr = np.abs(phase) < 0.5 * dur
    oot = (np.abs(phase) > dur) & (np.abs(phase) < 3 * dur)
    flux = tpf.flux.value
    img_in = np.nanmean(flux[intr], axis=0)
    img_oot = np.nanmean(flux[oot], axis=0)
    diff = img_oot - img_in            # positive where flux dropped during transit

    # flux-weighted centroid of the (positive) difference image
    ny, nx = diff.shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    w = np.clip(diff, 0, None)
    if w.sum() <= 0:
        ax.set_title(f"{sid}\n(no diff signal)", fontsize=8)
        return dict(sid=sid, verdict="no diff-image signal")
    cx, cy = (w * xx).sum() / w.sum(), (w * yy).sum() / w.sum()
    # target's pixel position within the cutout
    tx, ty = tpf.wcs.world_to_pixel(coord)
    off_pix = float(np.hypot(cx - tx, cy - ty))
    off_as = off_pix * PIXSCALE

    # render: difference image + target (white) + centroid (red) + neighbours (cyan)
    ax.imshow(diff, origin="lower", cmap="viridis")
    ax.plot(tx, ty, "*", color="white", ms=15, mec="k", label="WD")
    ax.plot(cx, cy, "x", color="red", ms=11, mew=2.5, label="dip centroid")
    try:
        nb = gaia_neighbours(ra, dec)
        wd_g = nb.iloc[((nb.ra-ra)**2+(nb.dec-dec)**2).values.argmin()].phot_g_mean_mag
        for _, n in nb.iterrows():
            px, py = tpf.wcs.world_to_pixel(SkyCoord(n.ra, n.dec, unit="deg"))
            if 0 <= px < nx and 0 <= py < ny and abs(n.phot_g_mean_mag - wd_g) > 0.2:
                ax.plot(px, py, "o", mfc="none", mec="cyan", ms=8 + max(0, 20-n.phot_g_mean_mag))
    except Exception:
        pass
    verdict = ("ON-TARGET → real, needs follow-up" if off_pix < 0.7 else
               "OFF-TARGET → background/blended EB (natural)")
    ax.set_title(f"{sid}\nP={period:.3f}d  offset={off_pix:.2f}px ({off_as:.0f}\")\n{verdict}",
                 fontsize=7.5)
    ax.legend(fontsize=6, loc="upper right")
    return dict(sid=sid, period=period, offset_pix=off_pix, offset_arcsec=off_as, verdict=verdict)


def main():
    r = pd.read_parquet(RES); r["source_id"] = r["source_id"].astype(str)
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    d = r[r.source_id.isin(FINALISTS)].merge(man, on="source_id")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.2))
    print(f"{'source_id':>20} {'P(d)':>7} {'offset_px':>9} {'offset\"':>8}  verdict")
    for ax, sid in zip(axes, FINALISTS):
        row = d[d.source_id == sid].iloc[0]
        try:
            res = vet_one(ax, sid, row.ra_deg, row.dec_deg, row.period_d)
        except Exception as e:
            res = dict(sid=sid, verdict=f"err {type(e).__name__}: {e}")
            ax.set_title(f"{sid}\n{res['verdict'][:40]}", fontsize=8)
        print(f"{sid:>20} {res.get('period',float('nan')):>7.3f} "
              f"{res.get('offset_pix',float('nan')):>9.2f} {res.get('offset_arcsec',float('nan')):>8.1f}"
              f"  {res['verdict']}", flush=True)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=120)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()
