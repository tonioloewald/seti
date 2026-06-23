#!/usr/bin/env python3
"""Validate the activity-robust morphology fix (local per-transit detrending) on injections.

The k04 --test regression confirms the detrend does not break box/planet/tail separation on a
random (mostly quiet) sample. This runner tests the thing the fix is FOR: morphology on
photometrically ACTIVE hosts, where irregular variability surviving the global detrend distorts
the folded shape and the sin_r2 gate (coherent P/2P only) does not catch it.

Design (candidate-blind): active and quiet host sets are selected by an OBJECTIVE per-star
activity index computed from the light curve itself (90-10 percentile range of ~2 h-binned
medians) over a sample of tier-2 (G 12-13) ok stars -- NOT from any residual/candidate list. A
clean planet and a clean box are injected at a fixed ephemeris into each host, and the battery
classifies the injected signal with the per-transit detrend ON (duration passed) and OFF
(duration=None), evaluated at the true injected ephemeris so the test isolates morphology from
detection.

Success criteria:
  - Active-host PLANET: fraction classified natural_planet should RISE with the detrend on
    (the fix restores the U-shape distorted by activity).
  - Active-host BOX: fraction classified RESIDUAL should be PRESERVED with the detrend on
    (the fix must not flatten away a real flat occulter).
  - Quiet hosts: both ~unchanged (the detrend is ~a no-op on an already-flat baseline).

No real candidate is revealed; this lifts no blind.
"""
import os, sys
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
sys.path.insert(0, os.path.join(ROOT, "pipeline", "fetch"))
from core.transit import inject_periodic                              # noqa: E402
from k04_search import battery                                        # noqa: E402

LCDIR = os.path.join(ROOT, "data", "lightcurves")
NOISE = os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet")
INJ_DEPTH = 0.02
INJ_PERIOD = 3.5
INJ_DUR = 0.15            # days; full transit duration of the injected signal
N_SCAN = 2000            # tier-2 ok stars to scan for the activity index
N_PICK = 150             # active (top) and quiet (bottom) hosts each


def activity_index(t, f):
    """Objective slow-variability amplitude: 90-10 percentile range of ~2 h-binned medians.
    Insensitive to white noise (binning averages it down) and to a single transit (a narrow
    dip barely moves the 10th percentile of many bins)."""
    t = np.asarray(t, float); f = np.asarray(f, float)
    if t.size < 50:
        return np.nan
    bins = np.arange(t.min(), t.max() + 0.083, 0.083)        # ~2 h
    idx = np.clip(np.digitize(t, bins) - 1, 0, len(bins) - 2)
    meds = np.array([np.median(f[idx == k]) for k in range(len(bins) - 1) if np.any(idx == k)])
    if meds.size < 10:
        return np.nan
    return float(np.percentile(meds, 90) - np.percentile(meds, 10))


def classify(t, f, scatter, detrend):
    """Battery verdict for an injected signal at the known ephemeris, detrend on/off."""
    t0 = t[0] + 0.3 * INJ_PERIOD
    return battery(t, f, INJ_PERIOD, t0, scatter,
                   duration=(INJ_DUR if detrend else None))["verdict"]


def main():
    nf = pd.read_parquet(NOISE); nf["source_id"] = nf["source_id"].astype(str)
    ok = nf[(nf.status == "ok") & np.isfinite(nf.scatter_ppm) & (nf.tier == 2)]
    samp = ok.sample(min(N_SCAN, len(ok)), random_state=7)
    rows = []
    for _, r in samp.iterrows():
        p = os.path.join(LCDIR, f"{r.source_id}.npz")
        if not os.path.exists(p):
            continue
        try:
            d = np.load(p); t, f = d["time"], d["flux"]
        except Exception:
            continue
        ai = activity_index(t, f)
        if np.isfinite(ai):
            rows.append((r.source_id, r.scatter_ppm / 1e6, ai))
    df = pd.DataFrame(rows, columns=["source_id", "scatter", "ai"]).sort_values("ai")
    print(f"scanned {len(df)} tier-2 LCs; activity index "
          f"P10={df.ai.quantile(.1):.4f} median={df.ai.median():.4f} P90={df.ai.quantile(.9):.4f}")

    sets = {"ACTIVE (top)": df.tail(N_PICK), "quiet (bottom)": df.head(N_PICK)}
    t0_rng = np.random.default_rng(0)
    print(f"\ninject depth={INJ_DEPTH:.0%} P={INJ_PERIOD}d dur={INJ_DUR}d; battery at true ephemeris\n")
    print(f"  {'host set':>16} {'family':>7} {'detrend':>8} {'target verdict':>16} {'rate':>6}")
    summary = {}
    for label, hosts in sets.items():
        for fam, target in [("planet", "natural_planet"), ("box", "RESIDUAL")]:
            for detrend in (False, True):
                hits = tot = 0
                for _, h in hosts.iterrows():
                    d = np.load(os.path.join(LCDIR, f"{h.source_id}.npz"))
                    t, f = d["time"], d["flux"]
                    t0 = t[0] + 0.3 * INJ_PERIOD
                    inj = inject_periodic(t, fam, INJ_DEPTH, INJ_PERIOD, t0, INJ_DUR)
                    v = battery(t, f * inj, INJ_PERIOD, t0, h.scatter,
                                duration=(INJ_DUR if detrend else None))["verdict"]
                    tot += 1; hits += (v == target)
                rate = hits / max(tot, 1)
                summary[(label, fam, detrend)] = rate
                print(f"  {label:>16} {fam:>7} {'ON' if detrend else 'off':>8} "
                      f"{target:>16} {rate:6.2f}")
    # headline deltas
    print("\n  --- effect of the detrend (ON - off) ---")
    for label in sets:
        dp = summary[(label, "planet", True)] - summary[(label, "planet", False)]
        db = summary[(label, "box", True)] - summary[(label, "box", False)]
        print(f"  {label:>16}: planet->natural_planet {dp:+.2f}   box->RESIDUAL {db:+.2f}")
    print("\nWant: ACTIVE planet delta strongly POSITIVE (fix recovers planets); "
          "ACTIVE box delta ~0 (flat occulter preserved); quiet deltas ~0 (no-op).")


if __name__ == "__main__":
    main()
