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
import os, sys, json, time, warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.detect import bls_detect, single_event_detect            # noqa: E402
from core.stats import poisson_fmax                                 # noqa: E402
from core.transit import metrics, make_transit, multi_epoch_depths, local_detrend  # noqa: E402

RUN = os.environ.get("KRUN", "T0")            # run label: T0 (G<11) | T0T1 (G<12) | T0T1T2 (G<13)
TIERS = {"T0": [0], "T0T1": [0, 1], "T0T1T2": [0, 1, 2]}.get(RUN, [0])
NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
CAL = os.path.join(ROOT, "data", "manifests", f"kdwarf_calibration_{RUN}.json")   # FROZEN, tagged
RESID = os.path.join(ROOT, "data", "manifests", f"kdwarf_{RUN}_residuals.csv")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])
# A transit deep enough to imply an occulter R > ~2.5 R_Jupiter is a stellar companion, not a
# planet or structure: depth = (R_occ/R_star)^2, R_star ~ 0.7 R_sun = 6.96 R_J, so R_occ = 2.5 R_J
# at depth ~0.13. Bigger than any planet/brown dwarf -> eclipsing binary. (Physical, not tuned.)
DEEP_EB_DEPTH = 0.13


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


def battery(t, f, period, t0, scatter, duration=None):
    """Light-curve battery features + verdict for a candidate.

    Morphology (depth / flat_bottom / asymmetry) is measured on a LOCALLY-DETRENDED fold
    (`core.transit.local_detrend`) so that irregular stellar activity surviving the global
    detrend does not distort the folded shape on active hosts. The activity gate (sin_r2), the
    eclipsing-binary tests (secondary / odd-even), and the red-noise-aware depth-variability
    test are computed on the RAW flux -- they measure the activity and differential depths
    directly, which a per-transit detrend would erase. `duration` is the BLS transit duration
    (days) used to size the detrend window; with duration=None the detrend is a no-op (so the
    raw-flux behaviour is recovered exactly)."""
    f_morph = local_detrend(t, f, period, t0, duration)
    phm, ffm = _fold(t, f_morph, period, t0)
    cen, prof = _binned_local(phm, ffm)
    feat = {}
    if len(prof) < 8:
        return {"verdict": "unfoldable", **feat}
    m = metrics(cen, prof)
    feat.update({k: m[k] for k in ("depth", "flat_bottom", "asymmetry")})
    # raw fold for the activity / EB / variability features (detrend must NOT touch these)
    ph, ff = _fold(t, f, period, t0)
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
    # per-epoch depth variability, RED-NOISE-AWARE: compare the epoch-to-epoch scatter of the
    # in-transit depth against the same scatter measured at OFF-transit phases (control "depths").
    # The control inherits the star's correlated/sector-to-sector noise, so only variability that
    # EXCEEDS it is genuine (a disintegrating body). A white-noise floor (scatter/sqrt(n)) under-
    # predicts red noise and over-flags noisy faint stars whose per-epoch depth merely tracks their
    # per-sector scatter; the empirical control floor measured here does not.
    phw = ((t - t0) / period + 0.5) % 1.0 - 0.5

    def _epoch_depths(center, hw=0.04):
        out = []
        for e in np.unique(epoch):
            mm = (np.abs(phw - center) < hw) & (epoch == e)
            if mm.sum() >= 3:
                out.append(base - np.median(f[mm]))
        return np.array([x for x in out if np.isfinite(x)])

    edeps = _epoch_depths(0.0)
    ctrl = [_epoch_depths(c) for c in (0.18, -0.18, 0.30, -0.30)]      # off-transit, off-secondary
    cstds = [np.std(c) for c in ctrl if len(c) >= 4]
    ctrl_std = float(np.median(cstds)) if cstds else np.nan
    if len(edeps) >= 4 and np.mean(edeps) > 0:
        feat["depth_cv"] = float(np.std(edeps) / np.mean(edeps))
        floor = ctrl_std if (np.isfinite(ctrl_std) and ctrl_std > 0) else scatter / np.sqrt(max(len(edeps), 1))
        feat["depth_excess"] = float(np.std(edeps) / floor) if floor > 0 else np.nan   # std / red-noise floor
        feat["depth_variable"] = bool(np.std(edeps) > 2.5 * floor and feat["depth_cv"] > 0.5)
    else:
        feat["depth_cv"] = np.nan; feat["depth_variable"] = False; feat["depth_excess"] = np.nan

    # ---- verdict (conservative; prior knowledge only explains away) -------------------
    # Asymmetry uses a SINGLE 0.15 boundary (planet below, anomalous above) -- no dead zone between
    # the planet and disintegrating cuts that would manufacture residuals from a threshold seam.
    if feat["sin_r2"] > 0.6:
        v = "activity/variability"
    elif feat["secondary_depth"] > 0.3 * d or feat["odd_even"] > 0.5 or d > DEEP_EB_DEPTH:
        v = "eclipsing_binary"             # secondary/odd-even, OR a depth implying R_occ > ~2.5 R_J
    elif feat["depth_variable"] and feat["asymmetry"] > 0.15:
        v = "disintegrating_body"
    elif feat["flat_bottom"] < 0.75 and feat["asymmetry"] < 0.15 and not feat["depth_variable"]:
        v = "natural_planet"               # U-shaped, symmetric, stable depth (red-noise-aware)
    else:
        v = "RESIDUAL"                     # flat-bottomed / asymmetric (>0.15) / genuinely variable
    return {"verdict": v, **feat}


def search_one(t, f, scatter, threshold, z):
    r = bls_detect(t, f, PERIODS, DURS)
    se = single_event_detect(t, f, scatter)
    is_cand = (r["sde"] > threshold) or (se["best_snr"] > z and se["n_events"] >= 2)
    if not is_cand:
        return None
    b = battery(t, f, r["period"], r["t0"], scatter, r["duration"])
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


def _unblind_one(task):
    """task=(sid, cohort, threshold, scatter, z) -> candidate dict (with sid) or None."""
    sid, cohort, threshold, scatter, z = task
    try:
        d = np.load(os.path.join(LCDIR, f"{sid}.npz"))
        res = search_one(d["time"], d["flux"], scatter, threshold, z)
    except Exception:
        return None
    if res is None:
        return None
    return {"source_id": sid, "cohort": int(cohort), **res}


def unblind_mode():
    """The real search: apply the FROZEN T0 calibration to the un-injected T0 light curves,
    list residual candidates, report per-family f_max. This lifts the blind."""
    if not os.path.exists(CAL):
        raise SystemExit(f"frozen calibration not found: {CAL} (run k03 + freeze/tag first).")
    cal = json.load(open(CAL))
    workers = int(sys.argv[sys.argv.index("--workers")+1]) if "--workers" in sys.argv else 6
    z = cal["fwer_sigma"]
    edges = np.array(cal["cohort_edges_scatter"])
    from core.noise import assign_cohorts
    nf = pd.read_parquet(NOISE); nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf["status"] == "ok") & np.isfinite(nf["scatter_ppm"]) & (nf["tier"].isin(TIERS))].copy()
    ok["cohort"] = assign_cohorts(ok["scatter_ppm"].to_numpy()/1e6, edges)
    thr = {int(c): cal["cohorts"][c]["threshold_sde"] for c in cal["cohorts"]}
    print(f"UNBLINDING {RUN}: {len(ok)} stars against frozen bars "
          f"{ {c: round(thr[c],1) for c in thr} } SDE ...", flush=True)

    tasks = [(r["source_id"], int(r["cohort"]), thr[int(r["cohort"])], r["scatter_ppm"]/1e6, z)
             for _, r in ok.iterrows()]
    cands = []; t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_unblind_one, t) for t in tasks]
        for i, fut in enumerate(as_completed(futs)):
            r = fut.result()
            if r is not None:
                cands.append(r)
            if (i+1) % 2000 == 0:
                print(f"  searched {i+1}/{len(tasks)} ({time.time()-t0:.0f}s, {len(cands)} candidates)",
                      flush=True)

    df = pd.DataFrame(cands)
    print(f"\n=== {RUN} UNBLIND RESULT ===\n  {len(ok)} stars searched; {len(df)} candidates above the bar.")
    if len(df):
        vc = df["verdict"].value_counts()
        print("  battery verdicts:")
        for v, n in vc.items():
            print(f"    {v:22s} {n}")
        resid = df[df["verdict"] == "RESIDUAL"].sort_values("sde", ascending=False)
        cols = ["source_id", "cohort", "sde", "period", "depth", "flat_bottom", "asymmetry",
                "depth_cv", "se_snr", "verdict"]
        resid[cols].to_csv(RESID, index=False)
        print(f"\n  {len(resid)} RESIDUALS (verdict=RESIDUAL) -> {RESID}")
        print("  These are NOT detections: each requires the difference-image centroid gate "
              "(TPF) and identity / known-planet cross-check before it is a real residual.")
        if len(resid):
            print("  top residuals by SDE:")
            for _, r in resid[cols].head(8).iterrows():
                print(f"    {r.source_id}  SDE={r.sde:.1f}  P={r.period:.3f}d  d={r.depth*100:.2f}%  "
                      f"flat={r.flat_bottom:.2f} asym={r.asymmetry:.3f}")
    # per-family f_max from the frozen completeness x searched cohort counts (zero-residual basis)
    print("\n  per-family f_max (3/sum C_i over searched {RUN} stars; the limit IF residuals clear):")
    for fam in cal["completeness"]:
        ds = "0.010" if "0.010" in cal["completeness"][fam] else list(cal["completeness"][fam])[0]
        sumCi = sum((cal["completeness"][fam][ds][str(c)] or 0) * int((ok["cohort"] == c).sum())
                    for c in range(cal["n_cohorts"]))
        print(f"    {fam:8s} (1% depth): f_max = {poisson_fmax(sumCi):.2e}  (sum C_i = {sumCi:.0f})")


if __name__ == "__main__":
    if "--unblind" in sys.argv[1:]:
        unblind_mode()
    else:
        test_mode()
