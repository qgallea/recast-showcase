"""Generate the four RECAST paper pages from the Phase-2 artifacts.

One-time author tool (NOT a build dependency): reads each project's
paper_spec / estimand_statement / replication_check / gap_table / final_report
+ referee files, copies the figure and the review markdown, and emits a rich,
static `index.qmd` per paper. Re-runnable. The gap table uses ONE generic
renderer (all four JSONs share the row schema panel/estimator/original/ours/
benchmark/verdict + optional difference); the referee tabset is file-driven so
papers with fewer rounds/referees (Ashraf-Galor, Djankov) don't get broken tabs.

Run from recast_fable/website/:
    ../phase1/.venv/Scripts/python.exe tools/build_pages.py
"""
import json
import shutil
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]          # recast_fable/website
ROOT = WEB.parent                                  # recast_fable
PROJECTS = ROOT / "phase2" / "projects"

# ── per-paper editorial content (the part a human supplies) ──────────────────
PAPERS = {
    "nunn_trefler_2010": {
        "method": "PLR", "topic": "Trade & Growth", "regime": "deterministic",
        "desc": "OLS cross-country growth on the skill bias of initial tariffs",
        "headline": "DML roughly halves the OLS skill-bias/growth effect and drops "
        "5% significance for most learners; the automated pipeline reproduced the "
        "hand-built analysis bit-for-bit and matched the benchmark 21/21.",
        "added": "The DML extension is a clean robustness verdict: across all seven "
        "learners and all three treatments the positive skill-bias/growth association "
        "keeps its sign, but the point estimates roughly halve (e.g. 0.035 → 0.019 for "
        "the correlation measure) and most 95% intervals cover zero at n = 63. That "
        "matches the Baiardi–Naghi finding and the original authors' own reading that "
        "much of the OLS coefficient reflects the endogeneity of tariff policy. The "
        "exploratory tercile heterogeneity finds nothing distinguishable at this sample "
        "size, and says so. Most importantly for the pipeline itself, this run is the "
        "regression test: the automation reproduced the hand-built notebook to zero "
        "numerical drift.",
        "walkthrough": True,
    },
    "teacher_training_2019": {
        "method": "IRM + generic ML", "topic": "Education (RCT)", "regime": "stochastic",
        "desc": "binary RCT of a teacher professional-development program",
        "headline": "The null average effect, the CLAN sorting (9/10), and the GATES "
        "shape reproduce — but the BLP heterogeneity slope diverges from the benchmark "
        "(0.20 vs 0.65). Reported as implementation sensitivity, not a win.",
        "added": "This is the most informative result on the site because it is not "
        "clean. The average effect reproduces the known null, and the rank-dependent "
        "heterogeneity structure reproduces (which students/teachers sort to the tails: "
        "CLAN 9/10 directions, the GATES shape). But the *scale* of the heterogeneity — "
        "the headline BLP β₂ — is a third of the benchmark and statistically "
        "insignificant. A blocking referee finding (omitted randomization strata) was "
        "fixed and the run repeated; restoring the strata moved β₂ only from 0.178 to "
        "0.200, which *eliminated* that explanation rather than closing the gap. RECAST "
        "reports this as genuine implementation sensitivity of generic-ML heterogeneity "
        "inference — not evidence against the benchmark, and certainly not a success it "
        "did not earn.",
    },
    "ashraf_galor_2013": {
        "method": "PLIV (IV)", "topic": "Deep roots & Growth", "regime": "deterministic",
        "desc": "quadratic IV of genetic diversity on long-run development",
        "headline": "The quadratic IV hump replicates exactly (optimal-diversity turning "
        "point 0.690); a linear PLIV cannot represent a hump, so the extension is labeled "
        "functional-form-limited rather than passed off as the effect.",
        "added": "The replication is essentially perfect: the hump-shaped 2SLS "
        "coefficients reproduce and the implied optimal diversity (0.690) matches the "
        "published value exactly, even with a generated instrument and only 21 countries. "
        "The extension is where honesty matters: the estimand router sends IV to a linear "
        "PLIV, but a single linear slope cannot represent a hump — so RECAST runs the "
        "PLIV, labels it a *linearized exploratory* quantity that is not comparable to "
        "the quadratic coefficients, and declines to present it as 'the effect of "
        "diversity.' The pipeline recognizing the boundary of its own tool is the point.",
        "exec_note": "executed via a bespoke `run_ag.py` script (the generated-instrument "
        "IV needed per-paper code), so there is no pipeline notebook for this paper; it "
        "also went through a single referee round.",
    },
    "djankov_taxes_2010": {
        "method": "PLR", "topic": "Public Finance", "regime": "deterministic",
        "desc": "corporate-tax effects on investment under all-controls OLS",
        "headline": "The all-12-controls OLS replicates 3/3 exactly and the DML port is "
        "17/21 consistent with the benchmark; a control-discipline screen flags 6 of 12 "
        "controls and discloses the resulting sensitivity (−0.200 → −0.230).",
        "added": "This run targets the over-conditioning failure mode directly. The "
        "'kitchen-sink' OLS reproduces exactly and the DML port strengthens the tax "
        "effect, matching the benchmark on 17 of 21 cells (the four 'tension' cells are "
        "significance-category flips on near-identical coefficients, not disagreements). "
        "The contribution is control discipline: a screen flags 6 of 12 inherited "
        "controls as plausible bad controls (a tax-payments mediator and a fiscal-bundle "
        "of sibling tax variables). Per the rule, the inherited full set stays the "
        "headline for comparability, and a documented sensitivity excluding the suspects "
        "is reported — the five-year estimate moves −0.200 → −0.230, the attenuation you "
        "would expect if those controls sit on the causal path. No claim is made that "
        "either number is the 'true' effect.",
    },
    "trust_fintech_2025": {
        "method": "DID_PLR", "topic": "Finance (DiD)", "regime": "stochastic",
        "desc": "continuous-intensity DiD: Wells-Fargo-scandal exposure × post on FinTech adoption",
        "verdict": "Extension demo",
        "headline": "A continuous-treatment difference-in-differences. The estimand router "
        "correctly chose PLR on the two-way-FE-residualized panel (DID_PLR) — NOT the "
        "staggered DoubleMLDIDMulti, which is invalid for a continuous dose. The paper's "
        "effect (exposure × post → FinTech mortgage share) replicates (TWFE 0.019, t=3.5) "
        "and the DML extension confirms it: 0.020–0.022 across learners, all significant.",
        "added": "The cleanest DiD case on the site. Treatment is a continuous Wells-Fargo-"
        "exposure intensity interacted with the post-2016-scandal period — a 'dose' DiD, not "
        "binary staggered adoption — so the router sends it to DID_PLR: unit + time fixed "
        "effects absorbed by a two-way within transform, then DoubleML PLR on the interaction, "
        "clustered by county (the DML analogue of a two-way-FE DiD). On the 842-county panel "
        "the headline effect survives and slightly strengthens under flexible ML control "
        "(0.019 → 0.020–0.022), so the conclusion is robust, not an artifact of the linear "
        "control specification. The trust-mechanism (Gallup) tables use restricted pseudo data "
        "and are out of scope.",
        "did_fig_cap": "Continuous-intensity DiD: TWFE replication vs the DML (DID_PLR) extension across learners (95% CIs).",
        "downloads_note": "county panel range-extracted from the 1.4 GB Mendeley package "
        "(HMDA_FIPS.dta) without downloading the 4.3 GB loan-level file; built by the project's "
        "`build_project.py`.",
    },
    "divine_policy_2025": {
        "method": "DID → DID_PLR", "topic": "Religion & Policy (DiD)", "regime": "stochastic",
        "desc": "staggered binary DiD: faith-based-initiative adoption on religious-nonprofit prevalence",
        "verdict": "Extension demo",
        "headline": "A staggered BINARY DiD that stress-tested the pipeline. DoubleMLDIDMulti "
        "(Callaway–Sant'Anna) is infeasible on a 50-state panel, so the pipeline gracefully fell "
        "back to the DML two-way-FE estimator (loudly flagged). The effect on religious-nonprofit "
        "share is positive but underpowered: TWFE +0.0016 (t=1.4); DML +0.0018–0.0025, "
        "significant for one of three learners.",
        "added": "This run is valuable precisely because it found a limit. The design is "
        "staggered adoption of state faith-based initiatives, so the router routes it to "
        "DoubleMLDIDMulti. But with only 50 states (6 never-treated, several single-state "
        "cohorts) the Callaway–Sant'Anna ML estimator hits empty per-(g,t) nuisance cells and "
        "cannot be fit. Rather than crash, the pipeline falls back to the DML two-way-FE "
        "estimator on a treated × post indicator and labels it loudly — because TWFE under "
        "staggered heterogeneity is exactly what Callaway–Sant'Anna exists to correct. The "
        "estimate is directionally consistent with the paper (faith-based initiatives → more "
        "faith-based nonprofits) but small and significant for only one learner at this sample "
        "size. The paper's headline GSS attitudes outcome lives in restricted files not shipped "
        "in the package, so this recast targets the religious-nonprofit outcome that is included.",
        "did_fig_cap": "Staggered DiD: TWFE replication vs the DML extension (DoubleMLDIDMulti infeasible at 50 states → DID_PLR fallback) across learners (95% CIs).",
        "downloads_note": "state×year panel reconstructed in Python from the openICPSR raw files "
        "(Sager faith-based-law timing + the 14.4M-row NCCS nonprofit panel) by the project's "
        "`build_project.py`; the GSS attitudes outcome is restricted and not included.",
    },
}

# referee files in display order: (relative path in review_history, tab label, dest name)
REVIEW_FILES = [
    ("round_1/refG.md",       "Round 1 · General",        "r1_refG.md"),
    ("round_1/refT.md",       "Round 1 · DML-technical",  "r1_refT.md"),
    ("round_1/synthesis.md",  "Round 1 · Synthesis",      "r1_synthesis.md"),
    ("round_1/changelog_1.md","Round 1 · Revision log",   "r1_changelog.md"),
    ("round_2/refG.md",       "Round 2 · General",        "r2_refG.md"),
    ("round_2/refT.md",       "Round 2 · DML-technical",  "r2_refT.md"),
    ("final_report.md",       "Final report",             "final_report.md"),
]


def esc(s):
    return str(s).replace("|", "\\|")


def render_gap_table(gap):
    """Generic renderer for all four gap_table shapes."""
    rows = gap.get("rows", [])
    out = []
    # group by panel, preserving order
    panels = []
    for r in rows:
        p = r.get("panel", "")
        if p not in panels:
            panels.append(p)
    # which optional columns are informative across the whole table?
    has_original = any(str(r.get("original", "-")).strip() not in ("-", "", "n/a")
                       for r in rows)
    has_diff = any(r.get("difference") is not None for r in rows)
    for p in panels:
        prs = [r for r in rows if r.get("panel", "") == p]
        ptitle = (p[:1].upper() + p[1:]) if p else p   # tidy lowercase panel keys
        out.append(f"\n**{ptitle}**\n")
        header = ["Estimator"]
        if has_original:
            header.append("Original")
        header += ["Ours", "Benchmark"]
        if has_diff:
            header.append("Δ")
        header.append("Verdict")
        out.append("| " + " | ".join(header) + " |")
        out.append("|" + "|".join(["---"] * len(header)) + "|")
        for r in prs:
            cells = [esc(r.get("estimator", ""))]
            if has_original:
                cells.append(esc(r.get("original", "-")))
            cells += [esc(r.get("ours", "")), esc(r.get("benchmark", ""))]
            if has_diff:
                d = r.get("difference")
                cells.append("" if d is None else f"{d:+.4f}")
            v = str(r.get("verdict", ""))
            # bold a divergent / failure verdict so it stands out
            if any(k in v.lower() for k in ("diverg", "fail", "flip")):
                v = f"**{v}**"
            cells.append(esc(v))
            out.append("| " + " | ".join(cells) + " |")
    # verdict counts
    vc = gap.get("verdict_counts")
    if vc:
        out.append("\n*Verdict counts:* " +
                   ", ".join(f"{k} {v}" for k, v in vc.items()) + ".")
    # callouts
    for key, title in (("functional_form_warning", "Functional-form limitation"),
                       ("note", "Note"), ("tension_note", "On the “tension” cells")):
        txt = gap.get(key)
        if txt:
            out.append(f"\n::: {{.callout-warning}}\n## {title}\n{txt}\n:::\n")
    # blinding / sha provenance
    sha = gap.get("dml_results_sha256_prefix") or gap.get("dml_results_sha")
    if sha or gap.get("blinding"):
        prov = gap.get("blinding", "Benchmark comparison computed after the DML "
                       "results were frozen.")
        line = prov
        if sha:
            line += f" (frozen `dml_results.json` sha256 `{sha}`)"
        out.append(f"\n[{line}]{{.text-muted-sm}}")
    return "\n".join(out)


def render_replication(rc):
    """Tiered replication block from replication_check.json (det. or stochastic)."""
    regime = rc.get("regime", "deterministic")
    gate = rc.get("gate", "")
    tier = rc.get("overall_tier", "")
    pcs = rc.get("per_coefficient", [])
    out = [f"**Regime:** {regime} · **Gate:** {gate} · **Overall tier:** {tier}\n"]
    if regime == "stochastic":
        r = pcs[0] if pcs else {}
        out.append(f"No deterministic published target is available, so replication is "
                   f"a documented *partial*. Our estimate: "
                   f"**{r.get('replicated_coef'):.4f}** (SE {r.get('replicated_se'):.4f}), "
                   f"n = {r.get('n_replicated')}.")
        if r.get("explanation"):
            out.append(f"\n[{esc(r['explanation'])}]{{.text-muted-sm}}")
        return "\n".join(out)
    # deterministic: a small table
    out.append("| Coefficient | Published | Replicated | n | Tier |")
    out.append("|---|---|---|---|---|")
    for r in pcs:
        name = r.get("spec") or r.get("variable") or ""
        pub_c = r.get("published_coef")
        rep_c = r.get("replicated_coef")
        pub_s = r.get("published_stat", r.get("published_se"))
        rep_s = r.get("replicated_stat", r.get("replicated_se"))
        kind = r.get("stat_kind", "se")
        pub = f"{pub_c} ({pub_s} {kind})" if pub_s is not None else f"{pub_c}"
        rep = (f"{rep_c:.4f} ({rep_s:.3f})" if isinstance(rep_c, (int, float))
               and rep_s is not None else f"{rep_c}")
        n = r.get("n_replicated", r.get("n_published", ""))
        out.append(f"| {esc(name)} | {esc(pub)} | {esc(rep)} | {n} | {r.get('tier','')} |")
    return "\n".join(out)


def citation(spec):
    ident = spec.get("identification", {})
    authors = spec.get("authors") or []
    auth = ", ".join(authors) if isinstance(authors, list) else str(authors)
    yr = spec.get("year", "")
    title = spec.get("title", "")
    jour = spec.get("journal", "")
    doi = ident.get("doi") or spec.get("doi") or ""
    cite = f"{auth} ({yr}). *{title}*. *{jour}*."
    if doi:
        cite += f" [doi:{doi}](https://doi.org/{doi})"
    return cite


def strip_h1(md):
    lines = md.splitlines()
    if lines and lines[0].lstrip().startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).lstrip("\n")


def build(slug, meta):
    proj = PROJECTS / slug
    spec = json.load(open(proj / "data" / "paper_spec.json", encoding="utf-8"))
    rc = json.load(open(proj / "data" / "results" / "replication_check.json", encoding="utf-8"))
    gap = json.load(open(proj / "data" / "results" / "gap_table.json", encoding="utf-8"))
    dest = WEB / "papers" / slug
    (dest / "reports").mkdir(parents=True, exist_ok=True)

    # assets: figure
    fig = proj / "paper" / "figures" / "forest_plot.png"
    has_fig = fig.exists()
    if has_fig:
        shutil.copyfile(fig, dest / "forest_plot.png")
    # estimand statement (strip its leading H1 to avoid a duplicate heading)
    est_src = proj / "data" / "estimand_statement.md"
    if est_src.exists():
        (dest / "estimand_statement.md").write_text(
            strip_h1(est_src.read_text(encoding="utf-8")), encoding="utf-8")
    # review files
    tabs = []
    rh = proj / "paper" / "review_history"
    for rel, label, name in REVIEW_FILES:
        src = rh / rel
        if src.exists():
            shutil.copyfile(src, dest / "reports" / name)
            tabs.append((label, name))

    authors = spec.get("authors") or []
    auth_disp = ", ".join(authors) if isinstance(authors, list) else str(authors)
    title = spec.get("title", slug)
    year = spec.get("year", "")
    journal = spec.get("journal", "")
    ident = spec.get("identification", {})
    doi = ident.get("doi") or spec.get("doi") or ""

    fm = [
        "---",
        f'title: "{title}"',
        f'author: "{auth_disp}"',
        f'date: "{year}"',
        'date-format: "YYYY"',
        f'description: "{meta["desc"]}"',
        "categories:",
        f'  - "{meta["method"]}"',
        f'  - "{meta["topic"]}"',
        f'  - "{year}"',
        f'  - "{meta.get("verdict", "Ready")}"',
    ]
    if has_fig:
        fm.append("image: forest_plot.png")
    fm += [
        f'paper-journal: "{journal}"',
        f'paper-doi: "{doi}"',
        f'recast-path: "{meta["method"]}"',
        f'replication-regime: "{meta["regime"]}"',
        "---",
    ]

    body = []
    # 1. summary + glance
    body.append("## Summary\n")
    body.append(f"**Citation:** {citation(spec)}\n")
    body.append(f"{meta['headline']}\n")
    body.append("::: {.glance}")
    for k, v in (("Method path", meta["method"]),
                 ("Replication", meta["regime"]),
                 ("Review verdict", meta.get("verdict", "Ready")),
                 ("Identification", ident.get("type", "—"))):
        body.append(f'<div class="g"><span class="k">{k}</span>'
                    f'<span class="v">{v}</span></div>')
    body.append(":::\n")

    # 2. estimand
    if est_src.exists():
        body.append("## Estimand & identification\n")
        body.append("{{< include estimand_statement.md >}}\n")

    # 3. replication
    body.append("## Replication\n")
    body.append(render_replication(rc) + "\n")

    # 4. gap table
    body.append("## The gap table\n")
    body.append("Original result, our replication/extension, the published benchmark "
                "(where one exists), and the verdict. The estimator never saw the "
                "benchmark — it is compared only after the results were frozen.\n")
    body.append(render_gap_table(gap) + "\n")

    # 5. extension + figure
    body.append("## Causal-ML extension\n")
    if has_fig:
        cap = (meta.get("did_fig_cap")
               or ("The hump-shaped IV effect (quadratic 2SLS); the linear-PLIV slope is a "
                   "separate, non-comparable quantity." if slug == "ashraf_galor_2013"
                   else "Estimates and 95% intervals across learners (and OLS)."))
        body.append(f"![{cap}](forest_plot.png)\n")
    body.append("Per-learner numbers are in the gap table above. ")
    if meta.get("did_fig_cap"):
        body.append("All learners are the DML difference-in-differences estimator "
                    "described above.\n")
    elif slug == "ashraf_galor_2013":
        body.append("The displayed learners are Forest and Lasso; both are the "
                    "linearized PLIV, reported as exploratory.\n")
    elif slug == "teacher_training_2019":
        body.append("The displayed BLP learner is the neural-network proxy (the "
                    "Λ-criterion best, matching the benchmark).\n")
    else:
        body.append("The preferred display learner is *Best* (the lowest-nuisance-RMSE "
                    "composition).\n")

    # 6. honest verdict
    body.append("## What causal ML added\n")
    body.append(meta["added"] + "\n")

    # 7. referee tabset (only when the project went through AI review)
    body.append("## AI peer review\n")
    if tabs:
        n_round2 = sum(1 for _, n in tabs if n.startswith("r2_"))
        rounds = 2 if n_round2 else 1
        body.append(f"The extension was reviewed over **{rounds} "
                    f"round{'s' if rounds > 1 else ''}** by two isolated referees "
                    f"(general + DML-technical) with a synthesis quality-control step. "
                    f"The reports are embedded verbatim.\n")
        body.append("::: {.panel-tabset}\n")
        for label, name in tabs:
            body.append(f"## {label}\n")
            body.append(f"{{{{< include reports/{name} >}}}}\n")
        body.append(":::\n")
    else:
        body.append("This run is a **replication + causal-ML extension demonstration** of the "
                    "difference-in-differences pathway; it has not yet been put through the "
                    "two-referee AI review (unlike the studies above).\n")

    # 8. downloads
    body.append("## Downloads & reproducibility\n")
    dl = []
    if meta.get("walkthrough"):
        dl.append("- [Hand-built walkthrough notebook (.ipynb)]"
                  "(../../downloads/recast_phase1_nunn_trefler.ipynb) — the analysis "
                  "this run reproduced bit-for-bit.")
    if meta.get("exec_note"):
        dl.append(f"- Note: {meta['exec_note']}")
    if meta.get("downloads_note"):
        dl.append(f"- Data: {meta['downloads_note']}")
    dl.append("- Full result artifacts (gap table, frozen estimates, referee reports) "
              "live in the project's `data/results/` and `paper/review_history/`.")
    body.append("\n".join(dl) + "\n")

    (dest / "index.qmd").write_text("\n".join(fm) + "\n\n" + "\n".join(body),
                                    encoding="utf-8")
    print(f"  {slug}: page written ({len(tabs)} review tabs, fig={has_fig})")


def main():
    print("Generating paper pages:")
    for slug, meta in PAPERS.items():
        build(slug, meta)
    # phase-1 walkthrough notebook -> downloads/
    nb = ROOT / "phase1" / "notebooks" / "recast_phase1_nunn_trefler.ipynb"
    if nb.exists():
        (WEB / "downloads").mkdir(exist_ok=True)
        shutil.copyfile(nb, WEB / "downloads" / "recast_phase1_nunn_trefler.ipynb")
        print(f"  copied walkthrough notebook -> downloads/")
    print("done.")


if __name__ == "__main__":
    main()
