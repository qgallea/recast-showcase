# DML-Technical Referee Report

**Round:** 2 (verification pass)
**Overall verdict:** Accept

## Scope

Verification of the round-1 essential fixes (E2/[C16], E3/[C14]; E1 artifact checked for
integrity since it shares the display with C16) against `paper/paper.tex`,
`paper/figures/forest_plot.{png,pdf}`, and the frozen result JSONs. Per the implicit
bargain, no new essential issues are raised on material visible in round 1.

## Fix verification

1. **[C16] Forest-plot caption SE-convention labeling — VERIFIED FIXED.**
   The Figure 1 caption now labels all three conventions per row type and each label is
   technically accurate:
   - "(B&N port)" rows = B&N-adjusted SEs, the median across repetitions of
     sqrt(SE_k^2 + (theta_k - median theta)^2) — matches the figure construction
     (theta +/- 1.96 x `se_median` from `dml_results.json.bn_port`) and
     `dml_tariffs_T2.R:181`.
   - "(DoubleML)" rows = the package's `confint()` intervals under the CI-backsolved
     median convention — verified against the doubleml resampling docs (per-repetition
     CIs combined via median; reported `se` backsolved from the median CI at 1.96) and
     numerically: for skill1_corr-Lasso, (ci_hi - coef)/1.96 = 0.0102588 = the stored
     `se` exactly; the CI is asymmetric ([-0.0008, 0.0413]) as a median-of-bounds
     aggregate should be.
   - "OLS (replicated)" rows = classical SEs, matching the declared port convention.
   The caption adds the requested warning that whisker-width differences between port
   and package rows partly reflect the convention; the optional sub-action (naming the
   package convention in the Table 5 note) was also done and is accurate.

2. **[C14] Lasso-selection diagnostics — RESOLVED AS DISCLOSURE; ACCEPTABLE.**
   No re-run was ordered this round, and the skill's ESSENTIAL tier permits documenting
   why a diagnostic is unavailable. The new Section 5.1 paragraph does this properly:
   it states what is missing and why (port wrapper discards the fitted model; package
   wrapper stores aggregates only), what recording it would require (instrumented
   wrappers per nuisance x repetition x fold, or one recomputed repetition), flags it as
   framework work, names the substantive risk T identified (p = 153 vs ~31 obs/fold,
   possible near-intercept collapse), and correctly bounds the impact: the port matches
   the published B&N Lasso cells to ~0.001 (gaps -0.00025, 0.00102, -0.00043), and the
   published benchmark itself comes from cv.glmnet under the same p >> n condition, so
   benchmark agreement is external corroboration that the reported numbers do not hinge
   on the missing diagnostic. The data-side instrumentation remains correctly logged as
   open framework work (deferred S6, acknowledged in the same paragraph).

3. **E1 artifact integrity (general referee's issue; checked because it shares Figure 1).**
   The regenerated figure is a 1x3 panel display (skill1_corr, diffa, diffg), 12 rows per
   panel (7 port, 4 package, 1 OLS), consistent row order; PNG and PDF were saved from the
   same figure object (both timestamped together) and `paper.pdf` was recompiled after.
   Spot checks against the frozen JSONs: diffa-Lasso port CI [0.0016, 0.0204] is displayed
   above zero; package skill1_corr-Lasso point/CI match `dml_results.json.package`.

## No-new-problems check (numbers unchanged)

Programmatic re-verification against the frozen JSONs (untouched: `dml_results.json`
2026-06-12 16:00, `gap_table.json` 20:55, predating the 21:18-21:19 figure/tex edits):

- Table 3 (21 port cells, theta and SE) matches `bn_port` exactly at printed rounding;
  Table 5 (12 package cells, coef/SE/p) matches `package` exactly. Zero mismatches.
- GATE Table 6 matches `hte_results.json` exactly (all six effects and joint CIs).
- Replication numbers unchanged.
- The only numeric edits were the corrections requested in round 1, both verified:
  gap-table note MC SD range 0.0021-0.0152 (port `theta_mc_sd` min 0.00208, max 0.01515)
  and CATE window 8.54-8.84 (positive lower band spans grid 8.5415-8.8427, max lower
  edge 0.00389, matching "at most 0.0039").
- Section 5.3's retained "0.0019-0.0152" is correct in its context: the pooled
  port+package MC SD range is 0.00188-0.01515, and that sentence compares port vs
  package cells; the S2a fix was correctly scoped to the 21 port rows in the gap-table
  note only.
- Suggestion fixes spot-checked: verdict-rule sentence matches the R2e-verified rule;
  S5 relabel is accurate ("the flag tests whether any group effect differs from zero");
  S7's 0.0110-vs-0.0062 attribution matches the JSONs; abstract and introduction
  rewordings are faithful. Deferrals of S3 and S6 are reasonable and documented.

No new problem was introduced by the revision.

## Suggestions (non-binding; pre-existing, not raisable as essential under the bargain)

1. Conclusion says the package panel adds "two further isolated cells" at 5%, but
   Section 5.3 correctly lists three (skill1_corr-Lasso p=0.038, diffa-Forest p=0.035,
   diffg-Lasso p=0.005). "two" should read "three" next time the section is touched.
2. The changelog's own caveat stands: `code_build/04_dml_extension.ipynb` cell 25 still
   generates the old single-panel figure; if notebook 04 is ever re-executed, update the
   plotting cell first so it does not overwrite the three-panel artifact.

---

*Verdict rationale: both of my round-1 essential items are resolved (one fixed, one
properly resolved-as-disclosed under the no-re-run instruction), the E1 artifact is
internally consistent with its caption and the frozen results, all printed numbers
re-verify against the result JSONs, and the revision introduced no new defects.
Zero BLOCKING findings; zero open essential issues. Accept.*
