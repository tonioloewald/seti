#!/usr/bin/env python3
"""Generate the figures for the K-dwarf bright-tier paper from committed artifacts.

Every figure is reconstructed from the frozen calibrations (kdwarf_calibration_{T0,T0T1}.json),
the per-stage residual / triage CSVs, and the noise floor (kdwarf_noise_floor.parquet) -- the
same files audit_T0_paper.py checks. No light curves are fetched; the residual diagnostics use
the committed per-sector coherence metrics, not re-derived photometry. Cascade counts that have a
committed CSV are recomputed and asserted against the paper's numbers (so the figure cannot
silently drift from the data); the two upstream candidate-generation levels, which live only in
the k04 search log, are taken from the recorded search result and labelled as such.

Output (figures/): kdwarf_cascade.png, kdwarf_fmax_depth.png, kdwarf_completeness.png,
kdwarf_noise_cohorts.png, kdwarf_residual_metrics.png
"""
import os, sys, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from core.stats import poisson_fmax                                   # noqa: E402
from core.noise import assign_cohorts                                 # noqa: E402

M = os.path.join(ROOT, "data", "manifests")
FIGDIR = os.path.join(ROOT, "figures")
DEPTHS = [0.005, 0.010, 0.020, 0.040, 0.080, 0.120]   # 0.150 row is the all-zero ceiling
FAM_STYLE = {                                          # family -> (label, colour)
    "box":      ("Flat occulter ('megastructure-like')", "#1a4b8c"),
    "tail":     ("Disintegrating dust-tail",             "#c0392b"),
    "triangle": ("Asymmetric (non-tail) occulter",       "#e67e22"),
    "planet":   ("Limb-darkened planet (control)",       "#7f8c8d"),
}


def load_cal(run):
    return json.load(open(os.path.join(M, f"kdwarf_calibration_{run}.json")))


def searched_cohort_counts(run, cal, tiers):
    """Number of searched stars per cohort -- the n_c that weight Sum C_i (mirrors the audit)."""
    nf = pd.read_parquet(os.path.join(ROOT, "data", "derived", "kdwarf_noise_floor.parquet"))
    nf["source_id"] = nf["source_id"].astype(str)
    sel = nf[(nf.status == "ok") & np.isfinite(nf.scatter_ppm) & (nf.tier.isin(tiers))].copy()
    edges = np.array(cal["cohort_edges_scatter"])
    sel["cohort"] = assign_cohorts(sel.scatter_ppm.to_numpy() / 1e6, edges)
    return sel, np.array([int((sel.cohort == c).sum()) for c in range(cal["n_cohorts"])])


def fmax_vs_depth(cal, n_c, fam):
    """f_max(depth) = 3 / Sum_c C_i(depth,c) * n_c, per the registered zero-detection bound."""
    out = []
    for d in DEPTHS:
        comp = cal["completeness"][fam][f"{d:.3f}"]
        sumCi = sum((comp[str(c)] or 0) * n_c[c] for c in range(len(n_c)))
        out.append(poisson_fmax(sumCi))
    return np.array(out)


# ---------------------------------------------------------------------------------------------
# Figure 1 -- the residual cascade (both tiers)
# ---------------------------------------------------------------------------------------------
def _verify(label, got, want):
    if got != want:
        raise SystemExit(f"CASCADE MISMATCH {label}: committed artifact={got}, paper={want}")


def cascade_counts(run, paper):
    """Recompute the committed-stage cascade from the CSVs and assert it matches the paper."""
    res = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals.csv"), dtype={"source_id": str})
    idn = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_identity.csv"), dtype={"source_id": str})
    cen = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_centroid.csv"), dtype={"source_id": str})
    ms = pd.read_csv(os.path.join(M, f"kdwarf_{run}_residuals_multisector.csv"), dtype={"source_id": str})
    tri = pd.read_csv(os.path.join(M, f"kdwarf_{run}_recurring_triage.csv"), dtype={"source_id": str})
    _verify(f"{run} residuals", len(res), paper["residuals"])
    _verify(f"{run} survive", int((idn.identity == "unknown").sum()), paper["survive"])
    _verify(f"{run} on_target", int((cen.centroid_verdict == "on_target").sum()), paper["on_target"])
    _verify(f"{run} recurs", int((ms.ms_verdict == "recurs").sum()), paper["recurs"])
    tv = tri.verdict
    triage = {k: int((tv == v).sum()) for k, v in
              [("EB", "eclipsing_binary"), ("planet", "natural_planet"),
               ("disint", "disintegrating_body"), ("RESIDUAL", "RESIDUAL")]}
    for k in triage:
        _verify(f"{run} triage {k}", triage[k], paper[k])
    return triage


def fig_cascade():
    # committed-stage counts are recomputed + asserted; the two upstream rows (candidates, the
    # light-curve battery split) live only in the k04 search log and are quoted from the paper.
    tiers = {
        "T0": dict(searched=12100, candidates=4131, planet_b=1861, eb_b=1336, act_b=136, dis_b=33,
                   residuals=765, cleared=99, survive=666, blend=310, on_target=337, unc=19,
                   artifact=194, recurs=53, untestable=90,
                   EB=5, planet=35, disint=1, RESIDUAL=12),
        "T0T1": dict(searched=44202, candidates=15451, planet_b=6852, eb_b=4674, act_b=768, dis_b=121,
                     residuals=3036, cleared=215, survive=2821, blend=1580, on_target=1121, unc=120,
                     artifact=578, recurs=140, untestable=403,
                     EB=17, planet=92, disint=4, RESIDUAL=27),
    }
    for run, p in tiers.items():
        cascade_counts(run, p)        # raises if the committed CSVs disagree with these numbers

    fig, axes = plt.subplots(1, 2, figsize=(13, 7.2))
    for ax, (run, p) in zip(axes, tiers.items()):
        stages = [
            (f"{p['searched']:,} stars searched", p["searched"], "#dfe6ee"),
            (f"{p['candidates']:,} BLS candidates > bar", p["candidates"], "#bcd0e5"),
            (f"{p['residuals']:,} survive light-curve battery", p["residuals"], "#9bbad9"),
            (f"{p['survive']:,} survive identity x-check", p["survive"], "#7aa4cd"),
            (f"{p['on_target']:,} on-target (centroid)", p["on_target"], "#5a8fc1"),
            (f"{p['recurs']:,} recur (multi-sector)", p["recurs"], "#3a79b5"),
            (f"{p['RESIDUAL']} unexplained residuals", p["RESIDUAL"], "#c0392b"),
        ]
        n = len(stages)
        wmax = float(stages[0][1])
        for i, (label, val, col) in enumerate(stages):
            y = n - 1 - i
            w = max(0.34, 0.85 * np.sqrt(val / wmax))  # sqrt width, floored so small stages stay legible
            ax.barh(y, w, height=0.62, color=col, edgecolor="#333", linewidth=0.6,
                    align="center", left=(0.5 - w / 2))
            ax.text(0.5, y, label, ha="center", va="center", fontsize=9.2, color="#111",
                    fontweight="bold" if i == n - 1 else "normal")
        # battery / by-product annotations on the right
        ax.text(1.02, n - 1 - 1.5,
                f"battery removes:\n {p['planet_b']:,} planets\n {p['eb_b']:,} eclips. binaries\n"
                f" {p['act_b']} activity\n {p['dis_b']} disintegrating",
                fontsize=7.6, va="center", color="#444")
        ax.text(1.02, n - 1 - 5,
                f"by-products:\n {p['EB']} EB + {p['planet']} planet cand.\n {p['disint']} disintegrating\n"
                f"deferred:\n {p['untestable']} recurrence-untestable\n {p['unc']} uncentroidable",
                fontsize=7.6, va="center", color="#444")
        ax.set_xlim(-0.05, 1.45)
        ax.set_ylim(-0.6, n - 0.4)
        ax.axis("off")
        ax.set_title(f"{run}  (G < {'11' if run == 'T0' else '12'})", fontsize=12, fontweight="bold")
    fig.suptitle("Residual cascade: every candidate is explained away or carried forward, "
                 "never tuned in or out", fontsize=12.5, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = os.path.join(FIGDIR, "kdwarf_cascade.png")
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


# ---------------------------------------------------------------------------------------------
# Figure 2 -- the headline: f_max vs depth, by morphology family, both tiers
# ---------------------------------------------------------------------------------------------
def fig_fmax_depth():
    runs = {"T0": ([0], "--", "o"), "T0T1": ([0, 1], "-", "s")}
    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    for run, (tiers, ls, mk) in runs.items():
        cal = load_cal(run)
        _, n_c = searched_cohort_counts(run, cal, tiers)
        for fam, (flabel, col) in FAM_STYLE.items():
            if fam == "planet":
                continue
            f = fmax_vs_depth(cal, n_c, fam)
            lbl = f"{flabel} ({run})" if fam == "box" else (flabel if run == "T0T1" else None)
            ax.plot(np.array(DEPTHS) * 100, f, ls, marker=mk, ms=4, color=col, lw=1.6,
                    label=(f"{flabel} ({run})"))
    # depth window the search has teeth in
    ax.set_yscale("log")
    ax.set_xlim(0, 13.8)
    ax.axvspan(0, 0.3, color="0.92", zorder=0)
    ax.axvspan(13, 13.8, color="0.92", zorder=0)
    ax.text(0.4, 1.4e-4, "0.3% morphology floor", rotation=90, fontsize=7.2, va="bottom", color="#555")
    ax.text(13.4, 1.4e-4, "13% companion ceiling", rotation=90, fontsize=7.2, va="bottom", color="#555")
    ax.set_xlabel("Transit depth (%)")
    ax.set_ylabel(r"$f_{\max}$  (95% upper limit on signature prevalence)")
    ax.set_title("Population upper limit by anomaly morphology\n"
                 "(dashed = T0 G<11; solid = combined T0+T1 G<12)", fontsize=11)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=7.6, loc="upper left", framealpha=0.92)
    fig.tight_layout()
    out = os.path.join(FIGDIR, "kdwarf_fmax_depth.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out}")


# ---------------------------------------------------------------------------------------------
# Figure 3 -- classification-aware completeness C_i vs depth, by morphology
# ---------------------------------------------------------------------------------------------
def fig_completeness():
    cal = load_cal("T0T1")
    _, n_c = searched_cohort_counts("T0T1", cal, [0, 1])
    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    grid_depths = [0.005, 0.010, 0.020, 0.040, 0.080, 0.120, 0.150]
    for fam, (flabel, col) in FAM_STYLE.items():
        comp = cal["completeness"][fam]
        # n-weighted mean across cohorts + min/max band
        mean, lo, hi = [], [], []
        for d in grid_depths:
            vals = np.array([comp[f"{d:.3f}"][str(c)] or 0 for c in range(3)])
            mean.append(np.average(vals, weights=n_c))
            lo.append(vals.min())
            hi.append(vals.max())
        x = np.array(grid_depths) * 100
        ax.plot(x, mean, "-o", ms=4, color=col, lw=1.7, label=flabel)
        ax.fill_between(x, lo, hi, color=col, alpha=0.12)
    ax.axvline(13, color="#555", ls=":", lw=1)
    ax.text(12.6, 0.04, "13% companion ceiling\n(occulter reclassified, search blind)",
            rotation=90, fontsize=7.0, va="bottom", ha="left", color="#555")
    ax.axvspan(0, 0.3, color="0.92", zorder=0)
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Injected transit depth (%)")
    ax.set_ylabel(r"Classification-aware completeness $C_i$  (detected AND survives battery)")
    ax.set_title("Recovery is morphology-aware: a flat occulter is recovered, its natural\n"
                 "look-alikes are (correctly) explained away (combined T0+T1)", fontsize=11)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8, loc="center right")
    fig.tight_layout()
    out = os.path.join(FIGDIR, "kdwarf_completeness.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out}")


# ---------------------------------------------------------------------------------------------
# Figure 4 -- the noise cohorts: the threshold is computed from the noise floor, not chosen
# ---------------------------------------------------------------------------------------------
def fig_noise_cohorts():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for ax, (run, tiers) in zip(axes, [("T0", [0]), ("T0T1", [0, 1])]):
        cal = load_cal(run)
        sel, n_c = searched_cohort_counts(run, cal, tiers)
        edges_ppm = np.array(cal["cohort_edges_scatter"]) * 1e6
        s = sel.scatter_ppm.to_numpy()
        bins = np.logspace(np.log10(max(s.min(), 50)), np.log10(np.percentile(s, 99.5)), 60)
        cohort_cols = ["#2ca25f", "#fdae6b", "#de2d26"]
        for c in range(3):
            ax.hist(s[sel.cohort == c], bins=bins, color=cohort_cols[c], alpha=0.75,
                    label=(f"cohort {c}: {cal['cohorts'][str(c)]['median_scatter_ppm']:.0f} ppm, "
                           f"bar {cal['cohorts'][str(c)]['threshold_sde']:.1f} SDE  (n={n_c[c]:,})"))
        for e in edges_ppm:
            ax.axvline(e, color="#222", ls="--", lw=1)
        ax.set_xscale("log")
        ax.set_xlabel("Per-star out-of-transit scatter (ppm, outlier-blind)")
        ax.set_ylabel("Stars")
        ax.set_title(f"{run}  ({len(sel):,} searched)", fontsize=11, fontweight="bold")
        ax.legend(fontsize=7.4, loc="upper right")
        ax.grid(True, alpha=0.2)
    fig.suptitle("Equal-count noise cohorts: the detection bar is set per cohort from the noise "
                 "floor (dashed = cohort edges)", fontsize=12, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGDIR, "kdwarf_noise_cohorts.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out}")


# ---------------------------------------------------------------------------------------------
# Figure 5 -- where the resolvable residuals sit in the diagnostic metric space
# ---------------------------------------------------------------------------------------------
RESOLVABLE = {  # source_id -> short label (the three distinct objects of section 4.2)
    "1397924585409290240": "deep transit,\nactive host",
    "5615925139763813248": "weak / near-blend",
    "93357127133226496":  "floor-depth,\nintermittent",
}


def fig_residual_metrics():
    # pool the triage tables of both tiers; dedupe by source_id keeping the combined-run row
    frames = []
    for run in ("T0", "T0T1"):
        t = pd.read_csv(os.path.join(M, f"kdwarf_{run}_recurring_triage.csv"), dtype={"source_id": str})
        t["run"] = run
        frames.append(t)
    tri = pd.concat(frames).drop_duplicates("source_id", keep="last")
    classes = {"natural_planet": ("Planet", "#7aa4cd", "o"),
               "eclipsing_binary": ("Eclipsing binary", "#e67e22", "^"),
               "disintegrating_body": ("Disintegrating", "#9b59b6", "D"),
               "RESIDUAL": ("Residual", "#c0392b", "s")}

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
    # panel A: shape space (flat-bottomedness vs asymmetry)
    axA = axes[0]
    for verdict, (lbl, col, mk) in classes.items():
        sub = tri[(tri.verdict == verdict)]
        axA.scatter(sub.flat_bottom, sub.asymmetry, s=14, c=col, marker=mk, alpha=0.55,
                    edgecolors="none", label=lbl)
    axA.axhline(0.15, color="#555", ls=":", lw=1)
    axA.text(0.01, 0.16, "asymmetry boundary (0.15)", fontsize=7.5, color="#555")
    axA.set_xlabel("Flat-bottomedness (0 = U-shaped planet, 1 = flat occulter)")
    axA.set_ylabel("Light-curve asymmetry")
    axA.set_title("Shape space", fontsize=11)
    axA.grid(True, alpha=0.2)
    axA.legend(fontsize=7.6, loc="upper right")

    # panel B: per-sector coherence (depth dispersion vs depth-scatter correlation)
    axB = axes[1]
    for verdict, (lbl, col, mk) in classes.items():
        sub = tri[(tri.verdict == verdict)]
        axB.scatter(sub.sec_depth_cv, sub.sec_depth_scatter_corr, s=14, c=col, marker=mk,
                    alpha=0.55, edgecolors="none")
    axB.set_xlabel("Per-sector depth dispersion (CV)")
    axB.set_ylabel("Corr(per-sector depth, per-sector scatter)")
    axB.set_title("Per-sector coherence  (noise tracks scatter -> upper-right)", fontsize=11)
    axB.grid(True, alpha=0.2)

    # mark the three resolvable residuals on both panels
    for sid, name in RESOLVABLE.items():
        row = tri[tri.source_id == sid]
        if row.empty:
            continue
        r = row.iloc[0]
        for ax, (xc, yc) in [(axA, (r.flat_bottom, r.asymmetry)),
                             (axB, (r.sec_depth_cv, r.sec_depth_scatter_corr))]:
            if pd.isna(xc) or pd.isna(yc):
                continue
            ax.scatter([xc], [yc], s=120, facecolors="none", edgecolors="black", linewidths=1.4, zorder=5)
            ax.annotate(name, (xc, yc), textcoords="offset points", xytext=(8, 6),
                        fontsize=7.4, fontweight="bold")
    fig.suptitle("The three morphology-resolvable residuals (circled): each sits at the margin of a "
                 "natural class, none is a flat occulter", fontsize=11.5, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out = os.path.join(FIGDIR, "kdwarf_residual_metrics.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"wrote {out}")


def main():
    fig_cascade()
    fig_fmax_depth()
    fig_completeness()
    fig_noise_cohorts()
    fig_residual_metrics()
    print("\nAll figures written to figures/kdwarf_*.png")


if __name__ == "__main__":
    main()
