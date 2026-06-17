# Changelog — Round 1

All edits are to `paper/paper.tex` and `paper/figures/forest_plot.{png,pdf}`. No notebook
was edited and no estimation was re-run; every number used was read from the frozen result
JSONs (`data/results/dml_results.json`, `replication_results.json`, `hte_results.json`,
`gap_table.json`). `paper.pdf` was recompiled (pdflatex x2, clean compile) so the PDF
matches the revised source and the regenerated figure.

### Essential issues addressed

- **Issue (E1):** Figure 1 artifact contradicted its caption and text — `forest_plot.png/pdf`
  showed a single `skill1_corr` panel (12 rows) while the caption and the line-159 sentence
  claimed all three treatments were shown.
  **Location:** `paper/figures/forest_plot.png`, `paper/figures/forest_plot.pdf`;
  caption of Figure `\ref{fig:forest}` (Section 5.2).
  **Change:** Regenerated the forest plot (the synthesis's preferred fix) as a 1x3 panel
  figure — one panel per treatment (`skill1_corr`, `diffa`, `diffg`) — by pure re-plotting
  of the frozen numbers; no re-analysis. Each panel reproduces the original cell-25 row
  construction exactly: 7 "(B&N port)" rows (`theta` +/- 1.96 x `se_median` from
  `dml_results.json.bn_port`), 4 "(DoubleML)" rows (package `coef` with the asymmetric
  `ci` field from `dml_results.json.package`), and 1 "OLS (replicated)" row
  (`replicated_coef` +/- 1.96 x `replicated_se` from `replication_results.json`), same
  row order, marker style, zero line, and dpi (150) as the prior artifact. PNG and PDF are
  saved from the same matplotlib figure object, so the two artifacts match by construction.
  The lone 5%-significant benchmarked cell (`diffa`–Lasso port, CI [0.0016, 0.0204]) and
  the significant package cells (`diffg`–Lasso, `diffa`–Forest) are now visibly displayed.
  The caption was updated to "one panel per treatment". The script used (run with the
  phase-1 venv Python) is reproduced in full at the bottom of this changelog for audit.
  **Status:** Resolved.
  **Caveat for the orchestrator:** `code_build/04_dml_extension.ipynb` cell 25 still
  generates the old single-panel figure. Per the synthesis ("No re-estimation needed") and
  the round instructions ("no notebook edit needed"), the notebook was deliberately not
  touched. If notebook 04 is ever re-executed in a later round, cell 25 will overwrite the
  three-panel artifact with the single-panel version; the plotting cell should be updated
  (append-only, `## Revision Round N`) at that point.

- **Issue (E2 / [C16]):** Figure 1 caption mislabeled the SE convention of the package rows
  ("DML rows use the B&N-adjusted standard errors"), although the "(DoubleML)" rows are
  built from `confint()` CIs (CI-backsolved median aggregation), a materially different
  convention (skill1_corr–Lasso: 0.0103 vs 0.0131).
  **Location:** Caption of Figure `\ref{fig:forest}` (Section 5.2); note of
  Table `\ref{tab:dml_pkg}` (Section 5.3).
  **Change:** Caption now labels each row type separately: "(B&N port)" rows = B&N-adjusted
  SEs (median across repetitions of sqrt(SE_k^2 + (theta_k - median theta)^2)); "(DoubleML)"
  rows = the package's `confint()` intervals under the CI-backsolved median convention;
  "OLS (replicated)" rows = classical SEs. Added the warning sentence that whisker-width
  differences between port and package rows partly reflect the convention, not only the
  learner. Also took up the synthesis's optional sub-action: the Table 5 note now names the
  package's median-aggregation convention and states that its `confint()` intervals (used in
  the figure) are CI-backsolved medians, not the B&N-adjusted formula.
  **Status:** Resolved.

- **Issue (E3 / [C14]):** Lasso-selection diagnostics absent for the penalized learner —
  neither `dml_results.json` nor the notebook records how many of the 153 candidate
  features the lasso retains in either nuisance.
  **Location:** Section 5.1 (Design), new paragraph "Lasso-selection diagnostics: a
  disclosed transparency gap," inserted after the Protocol paragraph.
  **Change:** Implemented the cheapest compliant fix per the round instructions (disclosure,
  no re-run): the new paragraph (i) states that per-feature selection diagnostics are not
  captured by the current port/package wrappers — the port wrapper discards the fitted
  model after producing out-of-fold predictions and the package wrapper stores aggregates
  only; (ii) states what adding them would require (re-running the estimation stage with
  instrumented wrappers logging the retained-feature count per nuisance x repetition x
  fold, or recomputing a single repetition); (iii) flags it as a known transparency gap
  inherited from the framework's wrappers; and (iv) notes the substantive risk T identified
  (at p = 153 vs ~31 obs per fold the lasso can collapse to a near-intercept predictor)
  while recording that the gap cannot affect the reported estimates (port matches the B&N
  benchmark to <= 0.001 in the Lasso cells). Estimation was NOT re-run, per instructions.
  **Status:** Resolved as disclosure (the data-side fix remains open framework work; see
  deferred S6, which the same paragraph partially covers).

### Suggestions addressed

- **Suggestion (S1):** "Consistent" verdict rule never stated in prose.
  **Change:** Added to the gap-table (Table `\ref{tab:gap}`) note: a DML row is
  "consistent" when |ours - benchmark| <= 1 x the benchmark SE; OLS rows are "exact" when
  the ported coefficient agrees with the published value within printed rounding. This is
  the rule T's R2e audit verified recomputes exactly, making the "all 21 consistent"
  headline falsifiable.

- **Suggestion (S2a):** Table 2 note MC SD lower bound said 0.0019 (a package-panel value)
  but the minimum across the 21 benchmarked port rows is 0.0021.
  **Change:** Gap-table note now reads "ranges from 0.0021 to 0.0152" (verified against
  `dml_results.json.bn_port`: min = diffg–Forest 0.00208, max = skill1_corr–Nnet 0.01515).

- **Suggestion (S2b, = T's suggestion 4):** CATE positive-band window over `init` printed
  as 8.54–8.81; the window actually extends to grid point 8.8427 (lower edge +0.0002).
  **Change:** Section 6, "8.54--8.81" -> "8.54--8.84" (verified against
  `hte_results.json.cate_init`: ci_joint_lo > 0 from grid 8.5415 through 8.8427).

- **Suggestion (S2c):** Abstract's "(lasso marginal)" understated Section 5.2's own
  t ~ 2.29 finding.
  **Change:** Abstract now reads "(one lasso cell significant)", the synthesis's wording.

- **Suggestion (S4):** Introduction's "passed an automated referee review with all
  diagnostics green" conflated the diagnostics gate with independent review.
  **Change:** Rephrased to "passed the pipeline's automated diagnostics gate with all
  checks green" (Section 1, last sentence).

- **Suggestion (S5):** `distinguishable` flag tests "any group differs from zero," but the
  text read it as terciles "indistinguishable from one another."
  **Change:** Took the rename/relabel branch of T's either/or action (no new analysis):
  Section 6 now attributes `distinguishable = false` to its computed quantity ("the flag
  tests whether *any* group effect differs from zero, not pairwise contrasts") and keeps
  the — correct — pairwise-indistinguishability statement as a separate clause grounded in
  the wide, heavily overlapping joint intervals. The printed claim now matches the
  computed quantity.

- **Suggestion (S7):** Package Lasso uses CV-min lambda; port uses the 1-SE rule; unnamed,
  the "implementation details" sentence in Section 5.3 was uncheckable.
  **Change:** Table 5 note now names the difference (`LassoCV` CV-minimum vs the benchmark
  R code's `cv.glmnet` 1-SE rule) and states that it accounts for the `diffa`–Lasso
  port/package gap (0.0110 vs 0.0062), exactly as T suggested.

### Suggestions deferred

- **Suggestion (S3):** Add a per-row MC-implementation-flag column to Table 2.
  **Reason:** Deferred — low benefit relative to cost. The flag is `false` for all 21 DML
  rows and the table note already states this explicitly per row scope ("`false` for all
  21 DML rows"); adding a 7th column of identical entries to an already-`footnotesize`
  6-column table widens it without adding information. Worth revisiting only if a future
  re-run flips any flag.

- **Suggestion (S6):** Surface port-side per-learner nuisance RMSE medians in
  `dml_results.json` and add an R^2-style normalization.
  **Reason:** Deferred — the per-repetition port RMSEs were computed in `bn_dml_one_rep`
  but discarded, so surfacing them requires re-running the estimation stage with modified
  wrappers (new analysis; the synthesis triggered no re-run this round). The disclosure
  side is addressed at low cost: the new Section 5.1 paragraph (E3) now states explicitly
  that the port computes per-repetition nuisance RMSEs internally but does not store them,
  and that the reported RMSE aggregates are package-side only.

### Blocking issues addressed

None — the synthesis records zero BLOCKING findings; no notebook was edited and no re-run
is triggered.

---

### Audit detail: exact paper.tex edits

1. Figure `\ref{fig:forest}` caption (Section 5.2): rewrote SE-convention sentence;
   "for the three treatments" -> "one panel per treatment" [E1, E2].
2. New paragraph "\textbf{Lasso-selection diagnostics: a disclosed transparency gap.}"
   inserted between the Protocol paragraph and Section 5.2's heading [E3, S6-disclosure].
3. Table `\ref{tab:gap}` note: inserted verdict-rule sentence [S1]; "$0.0019$" -> "$0.0021$" [S2a].
4. Table `\ref{tab:dml_pkg}` note: named the package CI convention [E2-optional] and the
   Lasso tuning difference with the 0.0110-vs-0.0062 attribution [S7].
5. Section 6 CATE paragraph: "8.54--8.81" -> "8.54--8.84" [S2b].
6. Abstract: "(lasso marginal)" -> "(one lasso cell significant)" [S2c].
7. Introduction, final sentence: "passed an automated referee review with all diagnostics
   green" -> "passed the pipeline's automated diagnostics gate with all checks green" [S4].
8. Section 6 GATE paragraph: flag-semantics fix for `distinguishable = false` [S5].

### Audit detail: figure regeneration script

Run from the project root with
`C:\Users\qgallea\Dropbox\work\claude_code\recast_fable\phase1\.venv\Scripts\python.exe`:

```python
# Revision Round 1 (E1+E2): regenerate forest plot with all three treatment
# panels, pure re-plotting of frozen numbers from data/results/*.json.
# Row construction and style replicate code_build/04_dml_extension.ipynb cell 25.
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(".")
RESULTS = PROJECT / "data" / "results"

dml = json.load(open(RESULTS / "dml_results.json"))
rep = json.load(open(RESULTS / "replication_results.json"))
bn_port, pkg = dml["bn_port"], dml["package"]
rep_by_treat = {s["treatment"]: s for s in rep["specs"]}

treatments = ["skill1_corr", "diffa", "diffg"]
outcome = "growth"

fig, axes = plt.subplots(1, 3, figsize=(14, 6.2), sharey=True)
ref_labels = None
for ax, d_col in zip(axes, treatments):
    labels, est, lo, hi = [], [], [], []
    for m, v in bn_port[d_col].items():
        labels.append(f"{m} (B&N port)")
        est.append(v["theta"])
        lo.append(v["theta"] - 1.96 * v["se_median"])
        hi.append(v["theta"] + 1.96 * v["se_median"])
    for ln, r in pkg.get(d_col, {}).items():
        labels.append(f"{ln} (DoubleML)")
        est.append(r["coef"]); lo.append(r["ci"][0]); hi.append(r["ci"][1])
    r0 = rep_by_treat[d_col]
    labels.append("OLS (replicated)")
    est.append(r0["replicated_coef"])
    lo.append(r0["replicated_coef"] - 1.96 * r0["replicated_se"])
    hi.append(r0["replicated_coef"] + 1.96 * r0["replicated_se"])
    if ref_labels is None:
        ref_labels = labels
    assert labels == ref_labels, "row order differs across panels"
    ypos = np.arange(len(labels))
    ax.errorbar(est, ypos, xerr=[np.array(est) - np.array(lo),
                                 np.array(hi) - np.array(est)],
                fmt="o", capsize=3)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_title(f"{d_col} -> {outcome}")
axes[0].set_yticks(np.arange(len(ref_labels)), ref_labels)
fig.suptitle("Estimate comparison: OLS vs. DML (PLR), 95% CIs", y=0.99)
fig.tight_layout()
(PROJECT / "paper" / "figures").mkdir(parents=True, exist_ok=True)
fig.savefig(PROJECT / "paper" / "figures" / "forest_plot.png", dpi=150)
fig.savefig(PROJECT / "paper" / "figures" / "forest_plot.pdf")
print("forest plot regenerated: 3 panels,", len(ref_labels), "rows each")
```

---

RERUN_NEEDED: no
