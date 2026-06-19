"""Heterogeneity forest plots: subgroup treatment effects with confidence
intervals, one `hte_forest.png` per project that actually has a subgroup
analysis. Two shapes are handled:
  * PLR/IRM/DID_PLR `gate_<var>` blocks  -> group average treatment effects
    (GATE) per moderator, with joint (multiplier-bootstrap) CIs.
  * CDDF `cddf` block                    -> sorted-group effects (GATES) by
    predicted-effect quintile, best-learner, 90%-adjusted CIs.
Papers with no declared moderator (Djankov), no native gate/cate (Ashraf-Galor
PLIV -> not applicable), or unavailable group-time cells (Divine small-N
fallback) have no subgroup analysis to plot and are skipped — the page text
explains why.

Run from recast_fable/website/:  ../phase1/.venv/Scripts/python.exe tools/make_hte_figures.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]            # recast_fable
PROJECTS = ROOT / "phase2" / "projects"

TITLES = {
    "nunn_trefler_2010": "Heterogeneity — GATE by inherited moderators (PLR)",
    "teacher_training_2019": "Heterogeneity — sorted-group effects (CDDF GATES)",
    "trust_fintech_2025": "Heterogeneity — GATE by NonRep tercile (DID_PLR)",
}


def collect(hte):
    """Return (rows, kind) where rows = [(label, est, lo, hi, sig)]; kind in
    {'gate','gates'} or ([], None) when there is nothing to plot."""
    rows = []
    for k in sorted(hte):
        g = hte.get(k)
        if k.startswith("gate_") and isinstance(g, dict) and g.get("effect"):
            var = k[len("gate_"):]
            sep = g.get("joint_ci_excludes_zero", [])
            cij = g.get("ci_joint", [])
            for i, (grp, e) in enumerate(zip(g.get("groups", []), g["effect"])):
                lo, hi = (cij[i] if i < len(cij) else [None, None])
                rows.append((str(grp), e, lo, hi, bool(i < len(sep) and sep[i])))
    if rows:
        return rows, "gate"
    cddf = hte.get("cddf")
    if cddf:
        bg = cddf.get("best_gates")
        gates = (cddf.get("learners", {}).get(bg, {}) or {}).get("gates", {})
        gam, cis = gates.get("gamma", []), gates.get("ci", [])
        for i, e in enumerate(gam):
            lo, hi = (cis[i] if i < len(cis) else [None, None])
            sig = lo is not None and (lo > 0 or hi < 0)
            rows.append((f"G{i+1} (lowest→highest predicted effect)" if i in (0, len(gam) - 1)
                         else f"G{i+1}", e, lo, hi, sig))
        if rows:
            return rows, "gates"
    return [], None


for proj in sorted(PROJECTS.iterdir()):
    f = proj / "data" / "results" / "hte_results.json"
    if not f.exists():
        continue
    rows, kind = collect(json.load(open(f, encoding="utf-8")))
    if not rows:
        print("skip (no subgroup analysis):", proj.name)
        continue

    labels = [r[0] for r in rows]
    ys = list(range(len(rows)))[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 0.5 * len(rows) + 1.5))
    for yi, (lab, e, lo, hi, sig) in zip(ys, rows):
        col = "#2c5f8a" if sig else "#9aa6b2"
        if lo is not None and hi is not None:
            ax.plot([lo, hi], [yi, yi], color=col, lw=2.2, zorder=2)
        ax.plot(e, yi, "o", color=col, ms=7, zorder=3,
                markerfacecolor=col if sig else "white", markeredgecolor=col)
    ax.axvline(0, color="#888", ls="--", lw=1, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Subgroup effect (point estimate, "
                  + ("95% joint CI)" if kind == "gate" else "90%-adjusted CI)"))
    ax.set_title(TITLES.get(proj.name, f"Heterogeneity — {proj.name}"), fontsize=11)
    ax.margins(y=0.12)
    # legend: filled = CI excludes 0
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([0], [0], marker="o", color="#2c5f8a", lw=0, label="CI excludes 0"),
        Line2D([0], [0], marker="o", color="#9aa6b2", markerfacecolor="white",
               lw=0, label="CI overlaps 0")],
        fontsize=8, loc="best", frameon=False)
    fig.tight_layout()
    out = proj / "paper" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"hte_forest.{ext}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out / 'hte_forest.png'}  ({len(rows)} subgroups, {kind})")
