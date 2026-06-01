#!/usr/bin/env python3
"""Step 8: Channel B vetting — morphology + identity on the top BLS signals.

Channel B is candidate-generating, not calibrated (§5.4): a high BLS S/N is NOT a
detection. Each top signal is put through the registered discriminants (§5.2 items 6-8):

  1. MORPHOLOGY — fold on the BLS period: is it a box (flat baseline + brief dip =
     transit-like) or a continuous sinusoid (ellipsoidal/reflection/pulsation =
     stellar variability)? Metrics: BLS duty cycle (duration/period), flat-top
     fraction (fraction of the folded curve at the bright baseline; high => transit),
     and sinusoid variance-explained at P and 2P (high => variable, not transit).
  2. IDENTITY — SIMBAD cone search: already a known eclipsing binary / pulsating WD /
     variable? A known natural classification explains it away.

(Difference-image centroid / BEB vetting, §5.2 item 9, is the next stage for anything
that survives morphology + identity.)

source_id is handled as a STRING throughout (19-digit Gaia IDs overflow float64's exact
range; see IMPLEMENTATION_LOG 2026-06-01 source_id-corruption entry).
Output: figures/transit_candidates.png + console verdicts.
"""
import os, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from lightkurve import search_lightcurve

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "data", "derived", "transit_search.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
FIG = os.path.join(ROOT, "figures", "transit_candidates.png")
NTOP = 9
DUTY_TRANSIT = 0.06   # below this duty cycle a dip is transit-shaped, not sinusoidal


def simbad_class(coord):
    try:
        from astroquery.simbad import Simbad
        s = Simbad()
        s.add_votable_fields("otype")
        t = s.query_region(coord, radius=6 * u.arcsec)
        if t is None or len(t) == 0:
            return "(no SIMBAD source)"
        return f"{t['main_id'][0]} [{t['otype'][0]}]"
    except Exception as e:
        return f"(simbad {type(e).__name__})"


def fold_metrics(flat, period):
    ph = ((flat.time.value - flat.time.value[0]) / period) % 1.0
    f = np.asarray(flat.flux)
    nb = 50
    idx = np.clip((ph * nb).astype(int), 0, nb - 1)
    binned = np.array([np.median(f[idx == k]) if np.any(idx == k) else np.nan
                       for k in range(nb)])
    b = binned[~np.isnan(binned)]
    base = np.median(b[b > np.percentile(b, 60)])
    depth = base - b.min()
    if depth <= 0:
        return ph, f, dict(flat_top=np.nan, sin_r2=np.nan)
    flat_top = float(np.mean(b > base - 0.25 * depth))
    x = np.linspace(0, 1, len(b), endpoint=False)
    A = np.column_stack([np.ones_like(x), np.cos(2*np.pi*x), np.sin(2*np.pi*x),
                         np.cos(4*np.pi*x), np.sin(4*np.pi*x)])
    coef, *_ = np.linalg.lstsq(A, b, rcond=None)
    sin_r2 = float(1.0 - np.sum((b - A @ coef)**2) / np.sum((b - b.mean())**2))
    return ph, f, dict(flat_top=flat_top, sin_r2=sin_r2)


def verdict(m, duty):
    # Robust discriminants: a high duty cycle OR high sinusoid variance-explained
    # means a smooth continuous modulation (ellipsoidal/reflection/pulsation), not a
    # transit. flat_top is reported but NOT used to decide — it is noise-dominated for
    # the shallow (~mmag), faint-WD signals here, so it would mislabel real dips.
    if duty > 0.15 or (not np.isnan(m["sin_r2"]) and m["sin_r2"] > 0.85):
        return "VARIABLE (sinusoidal — not a transit)"
    if duty < DUTY_TRANSIT:
        return "TRANSIT-shaped → centroid/BEB vet next"
    return "ambiguous → inspect"


def main():
    r = pd.read_parquet(RES)
    r["source_id"] = r["source_id"].astype(str)
    ok = r[r["status"] == "ok"].sort_values("bls_snr", ascending=False).head(NTOP)
    man = pd.read_csv(MAN, dtype={"source_id": str})[["source_id", "ra_deg", "dec_deg"]]
    ok = ok.merge(man, on="source_id", how="left")
    assert ok["ra_deg"].notna().all(), "unmatched source_id — id corruption regression"
    fig, axes = plt.subplots(3, 3, figsize=(15, 11))
    print(f"{'source_id':>20} {'G':>5} {'P(d)':>7} {'duty':>5} {'flatTop':>7} "
          f"{'sinR2':>6} {'snr':>6}  verdict | SIMBAD")
    for ax, (_, c) in zip(axes.ravel(), ok.iterrows()):
        coord = SkyCoord(c.ra_deg, c.dec_deg, unit="deg")
        duty = c.duration_d / c.period_d
        try:
            sr = search_lightcurve(coord, mission="TESS", radius=5*u.arcsec)
            sub = sr[[a == "SPOC" for a in sr.table["author"]]]
            lc = sub[0].download().remove_nans().normalize()
            flat = lc.flatten(window_length=401).remove_outliers(sigma=5)
            ph, f, m = fold_metrics(flat, c.period_d)
            ax.plot(ph, f, ".", ms=1, alpha=0.4)
            v = verdict(m, duty)
        except Exception as e:
            m = dict(flat_top=np.nan, sin_r2=np.nan)
            v = f"(err {type(e).__name__})"
        sm = simbad_class(coord)
        ax.set_title(f"{c.source_id}\nP={c.period_d:.3f}d snr={c.bls_snr:.0f} | {v[:22]}",
                     fontsize=8)
        ax.set_xlabel("phase"); ax.set_ylabel("norm flux")
        print(f"{c.source_id:>20} {c.g_mag:>5.1f} {c.period_d:>7.3f} {duty:>5.2f} "
              f"{m['flat_top']:>7.2f} {m['sin_r2']:>6.2f} {c.bls_snr:>6.1f}  {v} | {sm}",
              flush=True)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, dpi=110)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()
