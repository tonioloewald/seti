#!/usr/bin/env python3
"""Phase 2, step 3 (prereg §6.3): calibrate-and-FREEZE the detection thresholds.

Real-data calibration on the cached light curves + noise floor from step 2. Produces the
frozen calibration that step 4 (unblind) applies. Order is the integrity crux:

  - Cohorts: bin the ok stars by their outlier-blind MAD scatter (prereg §5a).
  - Per-cohort empirical null: BLS on EVERY ok star's real light curve; the per-cohort null
    (delta0, sigma0, genomic-control lambda) is estimated from the BULK of the SDE
    distribution (Efron) -- robust to any real transit, which sits in the tail. FWER bar =
    delta0 + z*sigma0, z = Phi^-1(1-1/N_total), N_total = the WHOLE frozen manifest.
  - Per-family completeness C_i: inject the frozen forward-model library into a representative
    SUBSAMPLE of real light curves per cohort (completeness is a fraction, not per-star);
    recovery = SDE > the cohort bar (+ the variable-depth net for the tail family).

CRITICAL: this does **not** reveal which real stars exceed the bar -- it computes and freezes
the null, threshold, and C_i, and stops. Unblinding (listing survivors) is step 4. Parallel
(ProcessPool) over stars; deterministic.

Usage:  k03_calibrate.py [--workers N] [--inj-per-cohort N]
Output (committed-small): data/derived/kdwarf_calibration.json
"""
import os, sys, json, time, warnings
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.detect import bls_detect, single_event_detect                      # noqa: E402
from core.stats import empirical_null, cohort_threshold, fwer_sigma, poisson_fmax  # noqa: E402
from core.noise import cohort_edges, assign_cohorts                          # noqa: E402
from core.transit import make_transit, multi_epoch_depths                    # noqa: E402
from k04_search import battery                                               # noqa: E402

NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
LCDIR = os.path.join(ROOT, "data", "lightcurves")
OUT = os.path.join(ROOT, "data", "derived", "kdwarf_calibration.json")
MANIFEST_N = 175968                          # N_total: the whole frozen manifest (FWER bar)
N_COHORTS = 3
PERIODS = np.arange(0.5, 13.0, 0.02)
DURS = np.array([0.05, 0.1, 0.2])
DEPTHS = [0.005, 0.01, 0.02, 0.04, 0.08, 0.12, 0.15]   # spans the 0.13 depth->EB cut, to MEASURE
INJ_PERIODS = [3.1, 7.3]                                # the upper depth boundary, not extrapolate past it
FAMILIES = ["planet", "box", "tail", "triangle"]        # triangle = asymmetric-occulter anomaly
INJ_DUR = 0.12


def load_lc(sid):
    d = np.load(os.path.join(LCDIR, f"{sid}.npz"))
    return d["time"], d["flux"]


@lru_cache(maxsize=64)
def _templ(fam, dep):
    return make_transit(fam, depth=dep, npix=150)


def _sde(sid):
    try:
        t, f = load_lc(sid)
        return sid, float(bls_detect(t, f, PERIODS, DURS)["sde"])
    except Exception:
        return sid, np.nan


def _recover(task):
    """task=(sid, cohort, fam, dep, threshold, scatter, z) -> (cohort, recovered_bool)."""
    sid, cohort, fam, dep, threshold, scatter, z = task
    try:
        t, f = load_lc(sid)
    except Exception:
        return None
    tph, tfl = _templ(fam, dep)
    p = INJ_PERIODS[int(sid) % len(INJ_PERIODS)]
    t0 = t[0] + 0.3 * p
    frac = ((t - t0) / p + 0.5) % 1.0 - 0.5
    inj = np.interp(frac * p / (2 * INJ_DUR), tph, tfl, left=1.0, right=1.0)
    if fam == "tail":
        ed = multi_epoch_depths(60, dep, rng=np.random.default_rng(int(sid) % (2**32)))
        ep = np.clip(np.floor((t - t0) / p + 0.5).astype(int), 0, None)
        ep = np.minimum(ep - ep.min(), len(ed) - 1)
        inj = 1.0 - (1.0 - inj) * (ed[ep] / dep)
    fi = f * inj
    r = bls_detect(t, fi, PERIODS, DURS)
    det = r["sde"] > threshold
    if fam == "tail":
        det = det or single_event_detect(t, fi, scatter)["best_snr"] > z
    if not det:
        return (cohort, False)
    # classification-aware completeness: an injected ANOMALY counts as recovered only if it also
    # SURVIVES the battery as a residual. A flat occulter mislabelled 'planet', or a tail labelled
    # 'disintegrating_body', is explained away -> not recovered (no f_max credit). This bounds the
    # battery's anomaly->natural leakage directly in C_i. (The natural-control 'planet' family is
    # expected to classify as planet and so earns ~0 anomaly-completeness, by design.)
    verdict = battery(t, fi, r["period"], r["t0"], scatter)["verdict"]
    return (cohort, verdict == "RESIDUAL")


def main():
    args = sys.argv[1:]
    def opt(n, d, c=str): return c(args[args.index(n)+1]) if n in args else d
    workers = opt("--workers", 6, int)
    inj_per = opt("--inj-per-cohort", 300, int)

    nf = pd.read_parquet(NOISE); nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf["status"] == "ok") & np.isfinite(nf["scatter_ppm"])].reset_index(drop=True)
    print(f"ok stars: {len(ok)} | workers {workers} | inj/cohort {inj_per}", flush=True)
    scat = ok["scatter_ppm"].to_numpy() / 1e6
    edges = cohort_edges(scat, n_cohorts=N_COHORTS)
    ok["cohort"] = assign_cohorts(scat, edges)

    # ---- phase A: per-cohort null from real BLS SDE (all stars, parallel) --------------
    t0 = time.time(); sde = {}
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_sde, s) for s in ok["source_id"]]
        for i, fut in enumerate(as_completed(futs)):
            sid, v = fut.result(); sde[sid] = v
            if (i + 1) % 1000 == 0:
                print(f"  null BLS {i+1}/{len(ok)} ({time.time()-t0:.0f}s)", flush=True)
    ok["sde"] = ok["source_id"].map(sde)
    z = fwer_sigma(MANIFEST_N)
    cohorts = {}
    for c in range(N_COHORTS):
        s = ok.loc[ok["cohort"] == c, "sde"].to_numpy(); s = s[np.isfinite(s)]
        d0, s0, lam = empirical_null(s)
        cohorts[c] = {"n": int(len(s)),
                      "median_scatter_ppm": float(np.median(ok.loc[ok["cohort"] == c, "scatter_ppm"])),
                      "delta0": d0, "sigma0": s0, "lambda": lam,
                      "threshold_sde": cohort_threshold(d0, s0, MANIFEST_N)}
        print(f"  cohort {c}: n={len(s)}  scatter~{cohorts[c]['median_scatter_ppm']:.0f}ppm  "
              f"lambda={lam:.2f}  bar={cohorts[c]['threshold_sde']:.1f} SDE", flush=True)

    # ---- phase B: per-family C_i on a per-cohort subsample (parallel) ------------------
    print("injection-recovery (subsampled per cohort)...", flush=True)
    sub = pd.concat([ok[ok["cohort"] == c].sample(min(inj_per, (ok["cohort"] == c).sum()),
                                                   random_state=c) for c in range(N_COHORTS)])
    tasks, Cgrid = [], {fam: {f"{d:.3f}": {} for d in DEPTHS} for fam in FAMILIES}
    for fam in FAMILIES:
        for dep in DEPTHS:
            for _, r in sub.iterrows():
                tasks.append((r["source_id"], int(r["cohort"]), fam, dep,
                              cohorts[int(r["cohort"])]["threshold_sde"], r["scatter_ppm"]/1e6, z))
    agg = {(fam, f"{d:.3f}", c): [] for fam in FAMILIES for d in DEPTHS for c in range(N_COHORTS)}
    keys = [(t[2], f"{t[3]:.3f}") for t in tasks]
    tA = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_recover, t): (t[2], f"{t[3]:.3f}") for t in tasks}
        for j, fut in enumerate(as_completed(futs)):
            res = fut.result()
            if res is not None:
                fam_dep = futs[fut]; agg[(fam_dep[0], fam_dep[1], res[0])].append(res[1])
            if (j + 1) % 2000 == 0:
                print(f"  inject {j+1}/{len(tasks)} ({time.time()-tA:.0f}s)", flush=True)
    for fam in FAMILIES:
        for dep in DEPTHS:
            ds = f"{dep:.3f}"
            for c in range(N_COHORTS):
                v = agg[(fam, ds, c)]; Cgrid[fam][ds][c] = float(np.mean(v)) if v else np.nan
            print(f"  {fam:7s} {dep*100:.1f}%:  " +
                  "  ".join(f"c{c}={Cgrid[fam][ds][c]:.2f}" for c in range(N_COHORTS)), flush=True)

    # ---- illustrative per-family f_max (scale subsample C_i to the full cohort counts) --
    fmax = {}
    for fam in FAMILIES:
        ds = "0.010" if "0.010" in Cgrid[fam] else list(Cgrid[fam])[0]
        sumCi = sum((Cgrid[fam][ds][c] or 0) * (ok["cohort"] == c).sum() for c in range(N_COHORTS))
        fmax[fam] = poisson_fmax(sumCi) if sumCi > 0 else None

    cal = {"n_ok": int(len(ok)), "n_total_manifest": MANIFEST_N, "n_cohorts": N_COHORTS,
           "inj_per_cohort": inj_per, "fwer_sigma": float(z),
           "cohort_edges_scatter": [float(e) for e in edges], "cohorts": cohorts,
           "completeness": Cgrid, "illustrative_fmax_at_1pct": fmax,
           "note": ("Frozen Phase-2 detection calibration (T0 / G<11). Noise floor + synthetic "
                    "injections only; no real candidate revealed. Step 4 applies threshold_sde."),
           "grids": {"periods": [0.5, 13.0, 0.02], "durations": [float(x) for x in DURS],
                     "inj_depths": DEPTHS, "inj_periods": INJ_PERIODS}}
    json.dump(cal, open(OUT, "w"), indent=2)
    print(f"\nwrote {OUT}\nillustrative per-family f_max (1%):",
          {k: (round(v, 4) if v else None) for k, v in fmax.items()})


if __name__ == "__main__":
    main()
