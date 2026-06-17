"""Coefficient-plot figures for the DiD recast pages: TWFE replication vs the DML
extension across learners (95% CIs). Writes forest_plot.png into each DiD project's
paper/figures/ so build_pages.py copies it like every other paper."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]            # recast_fable
PROJECTS = ROOT / "phase2" / "projects"
TITLES = {
    "trust_fintech_2025": "Trust as an Entry Barrier (FinTech) — continuous-intensity DiD",
    "divine_policy_2025": "Divine Policy — staggered DiD (DID_PLR fallback)",
}


def coef_ci(r):
    h = r.get("headline_att")
    if h:
        return h["coef"], h["ci"][0], h["ci"][1]
    return r["coef"], r["ci"][0], r["ci"][1]


for slug, title in TITLES.items():
    proj = PROJECTS / slug
    if not (proj / "data" / "results" / "dml_results.json").exists():
        print("skip (no results):", slug)
        continue
    res = json.load(open(proj / "data/results/dml_results.json", encoding="utf-8"))
    rc = json.load(open(proj / "data/results/replication_check.json", encoding="utf-8"))
    learners = res["specifications"][0]["learners"]

    labels, coefs, los, his, colors = [], [], [], [], []
    pc = rc["per_coefficient"][0]
    c, se = pc["replicated_coef"], pc["replicated_se"]
    labels.append("TWFE (replication)")
    coefs.append(c); los.append(c - 1.96 * se); his.append(c + 1.96 * se)
    colors.append("#b5462f")
    for ln, r in learners.items():
        c, lo, hi = coef_ci(r)
        labels.append(f"DML · {ln}"); coefs.append(c); los.append(lo); his.append(hi)
        colors.append("#2c5f8a")

    ys = list(range(len(labels)))[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 0.55 * len(labels) + 1.2))
    for yi, c, lo, hi, col in zip(ys, coefs, los, his, colors):
        ax.plot([lo, hi], [yi, yi], color=col, lw=2.2)
        ax.plot(c, yi, "o", color=col, ms=7)
    ax.axvline(0, color="#888", ls="--", lw=1)
    ax.set_yticks(ys); ax.set_yticklabels(labels)
    ax.set_xlabel("DiD effect (point estimate, 95% CI)")
    ax.set_title(title, fontsize=11)
    ax.margins(y=0.12)
    fig.tight_layout()
    out = proj / "paper" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"forest_plot.{ext}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out / "forest_plot.png")
