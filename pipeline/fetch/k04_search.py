#!/usr/bin/env python3
"""Phase 2, step 4 (prereg §6.4): the search + natural-explanation battery.

Applies the FROZEN calibration (per-cohort threshold_sde from k03) to each star: a BLS SDE
above its cohort bar (or a strong variable-depth single-event) is a *candidate*, which is then
run through the battery and classified as an explained natural class or an unexplained RESIDUAL.

Two modes, deliberately separated for integrity:
  --test     (default): injection-recovery VALIDATION. Inject known forward-model signals into
             real light curves and confirm the search recovers them and the battery classifies
             them correctly (planet -> natural planet; box/asymmetric/tail -> flagged). Reveals
             NO real candidate -- safe to run before the production calibration is frozen.
  --unblind: the real search. Applies the frozen bar to the UN-injected real light curves and
             lists residual candidates. This LIFTS THE BLIND and must only be run against the
             production full-manifest calibration, after it is frozen and tagged. Not run here.

The difference-image centroid gate (prereg §5 item 0) needs target-pixel data, which the
compact (time,flux) cache lacks; candidates are flagged `needs_centroid_vet` for a downstream
TPF fetch (a small list, as in Phase 1). All other battery items work on the light curve.
"""
import os, sys, json, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect, single_event_detect            # noqa: E402
from core.transit import metrics, make_transit, multi_epoch_depths  # noqa: E402

NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
CAL = os.path.join(ROOT, "data", "derived", "kdwarf_calibration.json")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])


def _fold(t, f, period, t0):
    ph = ((t - t0) / period + 0.5) % 1.0 - 0.5
    o = np.argsort(ph)
    return ph[o], f[o]


def _binned_local(ph, f, half=0.12, nbin=80):
    edges = np.linspace(-half, half, nbin + 1)
    idx = np.clip(np.digitize(ph, edges) - 1, 0, nbin - 1)
    m = (ph >= -half) & (ph < half)
    prof = np.array([np.median(f[(idx == k) & m]) if np.any((idx == k) & m) else np.nan
                     for k in range(nbin)])
    cen = (edges[:-1] + edges[1:]) / 2
    g = ~np.isnan(prof)
    return cen[g], prof[g]


def battery(t, f, period, t0, scatter):
    """Light-curve battery features + verdict for a candidate."""
    ph, ff = _fold(t, f, period, t0)
    cen, prof = _binned_local(ph, ff)
    feat = {}
    if len(prof) < 8:
        return {"verdict": "unfoldable", **feat}
    m = metrics(cen, prof)
    feat.update({k: m[k] for k in ("depth", "flat_bottom", "asymmetry")})
    base = np.median(ff[np.abs(ph) > 0.25]) if np.any(np.abs(ph) > 0.25) else np.median(ff)
    d = feat["depth"]
    # secondary eclipse near phase 0.5 (eclipsing binary)
    sec = np.abs(ph - 0.5) < 0.05
    feat["secondary_depth"] = float(base - np.median(ff[sec])) if sec.sum() > 3 else 0.0
    # odd-even depth difference (eclipsing binary)
    epoch = np.floor((t - t0) / period + 0.5).astype(int)
    intr = np.abs(((t - t0) / period + 0.5) % 1.0 - 0.5) < 0.04
    do = base - np.median(f[intr & (epoch % 2 == 1)]) if (intr & (epoch % 2 == 1)).sum() > 3 else d
    de = base - np.median(f[intr & (epoch % 2 == 0)]) if (intr & (epoch % 2 == 0)).sum() > 3 else d
    feat["odd_even"] = float(abs(do - de) / (d + 1e-9))
    # sinusoid variance explained at P and 2P (rotation / ellipsoidal -> not a transit)
    x = (t - t0) / period
    A = np.column_stack([np.ones_like(x), np.cos(2*np.pi*x), np.sin(2*np.pi*x),
                         np.cos(4*np.pi*x), np.sin(4*np.pi*x)])
    coef, *_ = np.linalg.lstsq(A, f, rcond=None)
    feat["sin_r2"] = float(1 - np.sum((f - A @ coef)**2) / np.sum((f - f.mean())**2))
    # per-epoch depth coefficient of variation (disintegrating body)
    deps = [base - np.median(f[intr & (epoch == e)]) for e in np.unique(epoch)
            if (intr & (epoch == e)).sum() >= 3]
    deps = np.array([x for x in deps if np.isfinite(x)])
    feat["depth_cv"] = float(np.std(deps) / np.mean(deps)) if len(deps) >= 4 and np.mean(deps) > 0 else np.nan

    # ---- verdict (conservative; prior knowledge only explains away) -------------------
    if feat["sin_r2"] > 0.6:
        v = "activity/variability"
    elif feat["secondary_depth"] > 0.3 * d or feat["odd_even"] > 0.5:
        v = "eclipsing_binary"
    elif np.isfinite(feat["depth_cv"]) and feat["depth_cv"] > 0.5 and feat["asymmetry"] > 0.15:
        v = "disintegrating_body"
    elif feat["flat_bottom"] < 0.75 and feat["asymmetry"] < 0.1 and (not np.isfinite(feat["depth_cv"]) or feat["depth_cv"] < 0.4):
        v = "natural_planet"
    else:
        v = "RESIDUAL"                      # flat-bottomed / asymmetric / structured beyond natural
    return {"verdict": v, **feat}


def search_one(t, f, scatter, threshold, z):
    r = bls_detect(t, f, PERIODS, DURS)
    se = single_event_detect(t, f, scatter)
    is_cand = (r["sde"] > threshold) or (se["best_snr"] > z and se["n_events"] >= 2)
    if not is_cand:
        return None
    b = battery(t, f, r["period"], r["t0"], scatter)
    return {"sde": r["sde"], "period": r["period"], "depth": r["depth"], "t0": r["t0"],
            "se_snr": se["best_snr"], "se_events": se["n_events"],
            "needs_centroid_vet": True, **b}


def load_cohorts():
    cal = json.load(open(CAL))
    nf = pd.read_parquet(NOISE); nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf["status"] == "ok") & np.isfinite(nf["scatter_ppm"])].copy()
    edges = np.array(cal["cohort_edges_scatter"])
    from core.noise import assign_cohorts
    ok["cohort"] = assign_cohorts(ok["scatter_ppm"].to_numpy() / 1e6, edges)
    thr = {int(c): cal["cohorts"][c]["threshold_sde"] for c in cal["cohorts"]}
    return ok, thr, cal["fwer_sigma"]


def test_mode():
    """Inject known signals into real LCs; confirm recovery + correct classification."""
    ok, thr, z = load_cohorts()
    rng = np.random.default_rng(0)
    samp = ok.sample(min(24, len(ok)), random_state=1)
    print("INJECTION TEST (no real candidate revealed):")
    print(f"  {'family':>9} {'recovered':>10} {'verdict (majority)':>22}")
    for fam in ["planet", "box", "triangle", "tail"]:
        rec = 0; verdicts = []
        for _, r in samp.iterrows():
            d = np.load(os.path.join(LCDIR, f"{r['source_id']}.npz"))
            t, f = d["time"], d["flux"]
            tph, tfl = make_transit(fam, depth=0.02, npix=150)
            p = 3.1; t0 = t[0] + 0.3 * p
            frac = ((t - t0) / p + 0.5) % 1.0 - 0.5
            inj = np.interp(frac * p / (2 * 0.12), tph, tfl, left=1.0, right=1.0)
            if fam == "tail":
                ed = multi_epoch_depths(60, 0.02, rng=rng)
                ep = np.minimum(np.clip(np.floor((t-t0)/p+0.5).astype(int), 0, None), len(ed)-1)
                ep -= ep.min(); inj = 1 - (1 - inj) * (ed[np.minimum(ep, len(ed)-1)] / 0.02)
            res = search_one(t, f * inj, r["scatter_ppm"]/1e6, thr[int(r["cohort"])], z)
            if res:
                rec += 1; verdicts.append(res["verdict"])
        vc = pd.Series(verdicts).value_counts()
        top = f"{vc.index[0]} ({vc.iloc[0]}/{len(verdicts)})" if len(verdicts) else "-"
        print(f"  {fam:>9} {rec}/{len(samp):>8} {top:>22}")
    print("\nExpect: all recovered; planet -> natural_planet; box -> RESIDUAL; "
          "tail -> disintegrating_body/RESIDUAL; triangle -> natural_planet or RESIDUAL.")


def unblind_mode():
    raise SystemExit("REFUSED: --unblind lifts the blind and must run only against the frozen "
                     "PRODUCTION calibration (full-manifest), after it is tagged. Not the proof.")


if __name__ == "__main__":
    if "--unblind" in sys.argv[1:]:
        unblind_mode()
    else:
        test_mode()
