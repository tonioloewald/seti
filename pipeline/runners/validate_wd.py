#!/usr/bin/env python3
"""Regression test: reproduce the committed v1 Channel-A results through the refactored
core + white-dwarf plugin, and diff against them.

A clean pass proves the refactor is faithful (the plugin seam changed nothing). A mismatch
is a signal, not a nuisance: either a transcription slip in the extraction, or a latent
logic flaw in the original that re-implementation surfaced. Either way it's worth knowing.

Reproduces: (1) the per-band excess chi, (2) the W3/W4 battery class counts, (3) f_max.
Compares to data/derived/{ir_excess,battery_w34,f_max}.parquet. Read-only; writes nothing.
"""
import os, sys
import numpy as np, pandas as pd

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PIPE)
from core.excess import excess_chi                                    # noqa: E402
from core.sed import fit_excess_bb, mag_to_fnu, LN10_04               # noqa: E402
from core.fmax import survey_fmax                                     # noqa: E402
from populations.white_dwarf import WhiteDwarf                        # noqa: E402

ROOT = os.path.dirname(PIPE)
D = os.path.join(ROOT, "data", "derived")
OB = os.path.join(D, "optical_baseline.parquet")
AW = os.path.join(ROOT, "data", "raw", "allwise", "allwise_xmatch.parquet")
BANDS = ["w1", "w2", "w3", "w4"]
T_GRID = [30, 50, 75, 100, 150, 200, 300, 500, 1000]
F_GRID = [1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]
CLASS = {"cold": "COLD_candidate(<300K)", "disk": "natural_disk",
         "companion": "natural_companion", "hot": "hot(>4000K)", "fit_failed": "fit_failed"}


def s(d): d["source_id"] = d["source_id"].astype(str); return d


def main():
    wd = WhiteDwarf()
    ob = s(pd.read_parquet(OB))
    aw = s(pd.read_parquet(AW))
    df = aw.merge(ob[["source_id", "g_mag", "teff_h", "logg_h"]], on="source_id", how="left")
    params = {"teff": df["teff_h"].to_numpy(float),
              "logg": df["logg_h"].to_numpy(float), "g_mag": df["g_mag"].to_numpy(float)}
    ph = df["ph_qual"].astype(str).to_numpy()

    # ---- (1) excess chi ----
    rep = {"source_id": df["source_id"].to_numpy()}
    for i, b in enumerate(BANDS):
        wpred = wd.predict_photometry(params, b)
        wobs = df[f"{b}mpro"].to_numpy(float); werr = df[f"{b}mpro_error"].to_numpy(float)
        chi = excess_chi(wobs, wpred, werr)
        det = np.array([len(x) == 4 and x[i] in "ABC" for x in ph])
        chi = np.where(det & np.isfinite(chi) & np.isfinite(wpred), chi, np.nan)
        rep[f"{b}_pred_mag"] = wpred; rep[f"{b}_chi"] = chi
    rep = pd.DataFrame(rep)
    ref = s(pd.read_parquet(os.path.join(D, "ir_excess.parquet")))
    m = rep.merge(ref, on="source_id", suffixes=("_new", "_ref"))
    print("(1) EXCESS chi vs ir_excess.parquet:")
    ok1 = True
    for b in BANDS:
        a, c = m[f"{b}_chi_new"].to_numpy(), m[f"{b}_chi_ref"].to_numpy()
        both = np.isfinite(a) & np.isfinite(c)
        dmax = np.nanmax(np.abs(a[both] - c[both])) if both.any() else 0.0
        nmatch = int((np.isfinite(a) == np.isfinite(c)).all())
        ok = dmax < 1e-9 and nmatch
        ok1 &= ok
        print(f"    {b.upper()}: n_det new/ref={np.isfinite(a).sum()}/{np.isfinite(c).sum()}"
              f"  max|Δ|={dmax:.2e}  {'OK' if ok else 'MISMATCH'}")

    # ---- (2) battery class counts ----
    awb = aw[["source_id", "ph_qual"] + [f"{b}mpro" for b in BANDS] +
             [f"{b}mpro_error" for b in BANDS]]
    b34 = rep.merge(awb, on="source_id")
    s_ph = b34["ph_qual"].astype(str).to_numpy()
    cand = np.array([len(x) == 4 and (x[2] in "ABC" or x[3] in "ABC") for x in s_ph])
    b34 = b34[cand].reset_index(drop=True)
    classes = []
    for _, r in b34.iterrows():
        sp = str(r["ph_qual"]); lam, fexc, sig = [], [], []
        for j, b in enumerate(BANDS):
            if sp[j] not in "ABC":
                continue
            mobs, merr, mpred = r[f"{b}mpro"], r[f"{b}mpro_error"], r[f"{b}_pred_mag"]
            if not (np.isfinite(mobs) and np.isfinite(merr) and np.isfinite(mpred)):
                continue
            fo = float(mag_to_fnu(mobs, j + 1)); fp = float(mag_to_fnu(mpred, j + 1))
            if fo - fp > 0:
                lam.append(wd.lam_um[j + 1]); fexc.append(fo - fp); sig.append(fo * LN10_04 * merr)
        if len(lam) < 2:
            classes.append("unresolved_<2band")
        else:
            _, Tx, _, _ = fit_excess_bb(lam, fexc, sig)
            classes.append(CLASS[wd.regime(Tx)])
    cnt_new = dict(pd.Series(classes).value_counts())
    cnt_ref = dict(pd.read_parquet(os.path.join(D, "battery_w34.parquet"))["class"].value_counts())
    ok2 = cnt_new == cnt_ref
    print(f"\n(2) BATTERY class counts {'OK' if ok2 else 'MISMATCH'}:")
    print(f"    new: {cnt_new}")
    print(f"    ref: {cnt_ref}")

    # ---- (3) f_max ----
    obp = ob.dropna(subset=["teff_h", "logg_h", "g_mag"])
    F_bol = wd.bolometric_flux({"teff": obp["teff_h"].to_numpy(float),
                                "logg": obp["logg_h"].to_numpy(float),
                                "g_mag": obp["g_mag"].to_numpy(float)})
    fm = pd.DataFrame(survey_fmax(F_bol, T_GRID, F_GRID, wd.survey_depth5))
    fref = pd.read_parquet(os.path.join(D, "f_max.parquet"))
    mm = fm.merge(fref, on=["T_x_K", "f_lum"], suffixes=("_new", "_ref"))
    dC = int((mm["sum_Ci_new"] - mm["sum_Ci_ref"]).abs().max())
    ok3 = dC == 0
    print(f"\n(3) f_max vs f_max.parquet: max|Δ sum_Ci|={dC}  {'OK' if ok3 else 'MISMATCH'}")
    print(f"    headline T=100,f=0.1: new={fm[(fm.T_x_K==100)&(fm.f_lum==0.1)].f_max.iloc[0]:.2e}"
          f"  ref={fref[(fref.T_x_K==100)&(fref.f_lum==0.1)].f_max.iloc[0]:.2e}")

    print(f"\n{'ALL CHANNEL-A RESULTS REPRODUCED through core+plugin' if (ok1 and ok2 and ok3) else '** DISCREPANCY -- investigate **'}")


if __name__ == "__main__":
    main()
