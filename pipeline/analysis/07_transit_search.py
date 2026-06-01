#!/usr/bin/env python3
"""Step 7: Channel B — transit search on the bright (TESS-observable) WD subset.

Registered as a SECONDARY, candidate-generating channel (§5.4): TESS is photon-starved
on faint WDs, so this runs only on the bright subset (G < 14). For each WD it downloads
a TESS light curve (SPOC preferred, then TESS-SPOC/QLP), flattens it, and runs Box Least
Squares to find the strongest periodic dip, recording period, depth, duration, and a
periodogram peak S/N. High-S/N transit-like signals are candidates for morphology +
difference-image centroid vetting (§5.2 items 6-9) — NOT yet anomaly claims.

Validated: recovers WD 1856+534 b at P=1.408 d. Resumable (per-target checkpoint).
Output (gitignored): data/derived/transit_search.parquet
"""
import os, time, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
from astropy.coordinates import SkyCoord
import astropy.units as u
from lightkurve import search_lightcurve

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OB = os.path.join(ROOT, "data", "derived", "optical_baseline.parquet")
MAN = os.path.join(ROOT, "data", "manifests", "wd_sample.csv.gz")
OUT = os.path.join(ROOT, "data", "derived", "transit_search.parquet")
GMAX = 14.0
PERIODS = np.arange(0.1, 13.0, 0.0008)


def process(coord):
    sr = search_lightcurve(coord, mission="TESS", radius=5 * u.arcsec)
    if len(sr) == 0:
        return {"status": "no_data"}
    sub = None
    for auth in ["SPOC", "TESS-SPOC", "QLP"]:
        s = sr[[a == auth for a in sr.table["author"]]]
        if len(s):
            sub = s; break
    if sub is None:
        return {"status": "no_usable_author"}
    lc = sub[0].download().remove_nans().normalize()
    flat = lc.flatten(window_length=401).remove_outliers(sigma=5)
    pg = flat.to_periodogram(method="bls", period=PERIODS)
    pw = np.asarray(pg.power.value)
    snr = float((pg.max_power.value - np.median(pw)) / (np.std(pw) + 1e-12))
    return {"status": "ok", "author": sub.table["author"][0],
            "sector": int(lc.meta.get("SECTOR", -1)), "n_pts": len(lc),
            "period_d": float(pg.period_at_max_power.value),
            "depth": float(pg.depth_at_max_power),
            "duration_d": float(pg.duration_at_max_power.value),
            "bls_snr": snr}


def main():
    ob = pd.read_parquet(OB).dropna(subset=["g_mag"])
    man = pd.read_csv(MAN)[["source_id", "ra_deg", "dec_deg"]]
    tgt = ob[ob["g_mag"] < GMAX].merge(man, on="source_id")[
        ["source_id", "g_mag", "ra_deg", "dec_deg"]].reset_index(drop=True)
    done = {}
    if os.path.exists(OUT):
        prev = pd.read_parquet(OUT)
        done = {int(s): True for s in prev["source_id"]}
        rows = prev.to_dict("records")
    else:
        rows = []
    print(f"bright WDs (G<{GMAX}): {len(tgt)}; already done: {len(done)}", flush=True)
    t0 = time.time()
    for i, r in tgt.iterrows():
        sid = int(r["source_id"])
        if sid in done:
            continue
        rec = {"source_id": sid, "g_mag": float(r["g_mag"])}
        try:
            rec.update(process(SkyCoord(r["ra_deg"], r["dec_deg"], unit="deg")))
        except Exception as e:
            rec["status"] = f"err:{type(e).__name__}"
        rows.append(rec)
        if i % 10 == 0:
            pd.DataFrame(rows).to_parquet(OUT, index=False)
            ok = sum(1 for x in rows if x.get("status") == "ok")
            print(f"  {i+1}/{len(tgt)}  ({time.time()-t0:.0f}s, {ok} with LC)", flush=True)
    res = pd.DataFrame(rows)
    res.to_parquet(OUT, index=False)
    ok = res[res["status"] == "ok"]
    print(f"done: {len(res)} processed, {len(ok)} with usable light curves", flush=True)
    if len(ok):
        cand = ok.sort_values("bls_snr", ascending=False).head(12)
        print("  top transit-like signals (BLS S/N) -- candidates for morphology/centroid vet:")
        for _, c in cand.iterrows():
            print(f"    {int(c['source_id'])} G={c['g_mag']:.1f}  P={c['period_d']:.3f}d  "
                  f"depth={c['depth']:.3f}  snr={c['bls_snr']:.1f}", flush=True)


if __name__ == "__main__":
    main()
