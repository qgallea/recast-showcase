# Synthesis Report — Round 1

**Unified verdict:** Minor revision

### Contribution consensus

Both referees are unambiguously positive. G finds the RECAST adds real value on all three axes — clean declared Stata-to-Python port (3/3 SUCCESS at printed precision), independent blinded reproduction of all 21 benchmarked B&N DML cells, and a power-honest exploratory heterogeneity branch — and passes the pleased-test. T's benchmark-alignment assessment confirms the implementation tracks the B&N (2024) Table-2 recipe line-for-line (interaction basis, K=2, 100 reps, median aggregation, B&N-adjusted SE variant, separate-argmin Best, learner hyperparameters), with all 21 cells within one benchmark SE under a verified blinding protocol and **zero BLOCKING findings**. The panel consensus is that this RECAST validates both the original result and the published B&N extension; the bar for blocking is correspondingly high, and nothing meets it.

### Essential issues (must be addressed — paper cannot stand as-is)

| # | Issue | Raised by | Scientific justification | Action |
|---|-------|-----------|-------------------------|--------|
| E1 | **Figure 1 artifact contradicts its caption and text (panel coverage).** `forest_plot.png` shows a single `skill1_corr` panel (12 rows); caption (`paper.tex:164`) and text (line 159) claim all three treatments are shown with 95% CIs. | G | The lone 5%-significant benchmarked cell is `diffa`–Lasso; the reader is told they are seeing visual CI evidence for exactly that treatment, but the artifact does not display it. The report is misleading about its own evidence. | Regenerate Figure 1 with all three treatment panels (or rescope caption + line-159 sentence to `skill1_corr` only) and ensure the PNG artifact matches the PDF. No re-estimation needed. |
| E2 | **[C16] Figure 1 caption mislabels the SE convention of the package rows.** Caption states "DML rows use the B&N-adjusted standard errors," but the four "(DoubleML)" rows per treatment are built from `confint()` CIs (CI-backsolved median convention, doubleml `resampling.rst:219-223`); conventions differ materially (skill1_corr–Lasso: 0.0103 vs 0.0131). | T | Spec L4/C16: any display mixing SE conventions must label each. A reader will attribute whisker-width differences to learners rather than to the convention — exactly the mixing C16 prohibits. | Amend the Figure 1 caption (and ideally legend labels): "(B&N port)" rows = B&N-adjusted SEs (median-of-sqrt); "(DoubleML)" rows = package CI-backsolved median CIs. Optionally name the package convention in Table 5's note. |
| E3 | **[C14] Lasso-selection diagnostics absent for the penalized learner.** Neither `dml_results.json` nor the notebook records how many of the 153 candidate features the lasso retains in either nuisance (port discards the fitted model; package coefficients never inspected). | T | With p = 153 vs ~31 obs per fold and a 1-SE rule, the lasso can select zero features and collapse to the training mean. Lasso is the single significant DML cell in two panels (`diffa` port, `diffg` package); the reader needs evidence it is a genuine selection fit, not a near-intercept predictor. | In `code_run/04_dml_extension.ipynb`, log median non-zero lasso coefficients for `ml_l`/`ml_m` per treatment (or recompute on one rep), add to `dml_results.json` (e.g. `lasso_selection`), plus one sentence in Section 5.3 notes. |

**Note on E3:** the fix touches notebook code, but T — the only referee with BLOCKING authority — explicitly classified it ESSENTIAL, not BLOCKING: it is append-only disclosure (computable on a single rep) that cannot change any reported estimate, sign, or significance (the port already matches the B&N benchmark to ≤ 0.001 in the Lasso cells). The /stage 4 cascade re-run is therefore **not** triggered.

### Suggestions (would improve but are optional)

| # | Issue | Raised by | Action |
|---|-------|-----------|--------|
| S1 | The "consistent" verdict rule is never stated in prose, though T verified it recomputes exactly as `|gap| <= 1 x se_bench`. | G (rule confirmed by T's R2e audit) | Add one sentence in Section 4 / Table 2 notes stating the tolerance, making the headline "all 21 consistent" claim falsifiable. |
| S2 | Small numeric precision fixes: (a) Table 2 note MC SD lower bound is 0.0019 (package panel) but the 21 benchmarked port rows' minimum is 0.0021; (b) CATE positive-band window over `init` extends to ≈8.84 (lower edge +0.0002 at 8.8427), not 8.81 as printed (`paper.tex:221`); (c) abstract's "(lasso marginal)" understates Section 5.2's own t ≈ 2.29 finding. | G (item b also raised by T — deduplicated, same edit) | Correct 0.0019 → 0.0021 in scope; 8.81 → 8.84; rephrase abstract to "(one lasso cell significant)". |
| S3 | MC-implementation flag shown only as an aggregate note. | G | Add a per-row flag column to Table 2 (one column; robust to future flag flips). |
| S4 | Introduction's "passed an automated referee review with all diagnostics green" conflates the diagnostics gate with independent review. | G | Rephrase to "passed the pipeline's automated diagnostics gate". |
| S5 | GATE `distinguishable` flag tests "any group differs from zero," while `paper.tex:219` reads it as terciles "indistinguishable *from one another*." Conclusion happens to be right. | T | Add a pairwise tercile-difference contrast or rename the flag so the printed claim matches the computed quantity. |
| S6 | Port-side per-learner nuisance RMSEs are computed in `bn_dml_one_rep` but discarded; the package panel carries all of R2b's weight. | T | Surface port-side RMSE medians in `dml_results.json` and consider an R²-style normalization so "0.216–0.237" is interpretable. |
| S7 | Package Lasso uses CV-min lambda; port uses the 1-SE rule. Unnamed, this leaves the "implementation details" sentence in Section 5.3 uncheckable. | T | Name the tuning difference in the Table 5 note — it precisely explains the diffa–Lasso port/package gap (0.0062 vs 0.0110). |

### Blocking issues (require re-running a notebook)

| # | Issue | Raised by | Canonical citation | Notebook to fix | Specific action |
|---|-------|-----------|--------------------|-----------------|-----------------|

*None. T (the only referee with BLOCKING authority) marked zero findings BLOCKING: every benchmarked cell reproduces the canonical B&N values within one benchmark SE under a verified blinding protocol, and both of T's essential items are disclosure/prose fixes that cannot change sign, significance, or magnitude.*

### Downgraded items

None. G raised exactly one essential issue and T raised two — well within the proportionality norm (0–3) — and all three carry explicit scientific justifications (misleading visual evidence for the lone significant treatment; prohibited SE-convention mixing with a canonical doubleml citation; possible degenerate lasso fits behind the only significant DML cells). No signal-jamming detected; no downgrades required.

### Referee disagreements

None. Both referees independently reach "Minor revision," both independently verified the gap-table arithmetic against the results JSONs (G by hand, T programmatically) and agree it recomputes exactly, and their essential findings are complementary rather than contradictory.

**Deduplication decision (flagged candidate):** G's essential "forest-plot artifact contradicts caption/text" and T's [C16] "forest-plot caption mislabels SE convention" target the same display but are **distinct defects** under the same-edit test: G's fix (add the missing `diffa`/`diffg` panels, or rescope the caption to `skill1_corr`) would not correct the SE-convention mislabel, and T's caption fix would not add the missing panels. They are kept as separate issues (E1, E2) — but the revision agent should resolve both in a single regeneration pass over Figure 1 and its caption. By contrast, G's suggestion 2(b) and T's suggestion 4 (CATE window endpoint 8.84 vs 8.81) **are** the same issue — one edit at `paper.tex:221` fixes both — and were merged into S2(b).

### Already resolved (suppressed from this round)

None — this is round 1; no prior changelogs exist.

---

RERUN_NEEDED: no
