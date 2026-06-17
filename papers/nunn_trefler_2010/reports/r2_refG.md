# General Referee Report

**Round:** 2 (verification pass)
**Overall verdict:** Accept

## Verification of round-1 essential fixes

1. **E1 — Forest plot vs. caption (my round-1 essential issue): RESOLVED, verified against the artifact.** `paper/figures/forest_plot.png` now shows three panels (`skill1_corr -> growth`, `diffa -> growth`, `diffg -> growth`), 12 rows each (7 "(B&N port)", 4 "(DoubleML)", 1 "OLS (replicated)"), identical row order across panels. I spot-checked the plotted values against the frozen JSONs: the lone significant benchmarked cell, `diffa`–Lasso port (theta 0.011019, B&N-adjusted SE 0.004811, CI [0.0016, 0.0204]), is now displayed with its whisker visibly clear of zero, as are the significant package cells `diffg`–Lasso (ci [0.0027, 0.0210]) and `diffa`–Forest (ci [0.0006, 0.0200]); the widest interval is `skill1_corr`–Nnet port ([-0.0178, 0.0447]) as the JSON implies; the OLS rows match `replication_results.json` (e.g., `skill1_corr` [0.0153, 0.0544]). The caption (now "one panel per treatment") and the line-161 sentence ("visualizes all estimates") are both true of the artifact. PNG and PDF carry the same write timestamp (saved from one figure object) and `paper.pdf` was recompiled afterwards, so the artifacts are in sync.

2. **E2 — Caption SE-convention labeling: RESOLVED.** The caption now labels each row type's convention separately (B&N-adjusted SEs for port rows; package `confint()` CI-backsolved-median intervals for "(DoubleML)" rows; classical SEs for OLS rows) and warns that whisker-width differences partly reflect the convention. This is accurate: the package `ci` fields in `dml_results.json` are genuinely asymmetric around the coefficient (e.g., `skill1_corr`–Lasso ci [-0.00081, 0.04135] vs. coef ± 1.96 SE [0.00113, 0.04135]), so plotting them as a distinct convention is the honest choice. The Table 5 note's matching language is consistent with the caption.

3. **E3 — Lasso-selection diagnostics (technical referee's issue): resolved as a disclosure paragraph**, which is within the round's no-re-run instruction; I verify only its report-consistency, which is fine except for one wording nit (below).

## Verification of suggestion edits (all sound)

- **S1 (verdict rule):** the gap-table note now states "consistent" = |ours − benchmark| ≤ 1 × SE_bench. I recomputed all 21 cells from `dml_results.json.bn_port` against the printed benchmarks: the rule holds everywhere; the worst case is `diffa`–Forest at 0.383 benchmark SE. The headline claim is now falsifiable and true.
- **S2a (MC SD range):** gap-table note now reads 0.0021–0.0152; verified (min `diffg`–Forest port 0.00208, max `skill1_corr`–Nnet port 0.01515). Section 5.3's separate "0.0019–0.0152" is also correct in its own scope (it covers the package panel, whose minimum is `diffg`–Forest package 0.00188) — the two ranges are not a contradiction, though a two-word scope marker ("across both panels") would forestall reader confusion.
- **S2b (CATE window):** "8.54–8.84" verified against `hte_results.json.cate_init` (joint lower band positive from grid 8.5415 through 8.8427, 11 grid points; max lower edge 0.0039, matching the text's "at most 0.0039").
- **S2c (abstract):** "(one lasso cell significant)" present; matches Section 5.2's t ≈ 2.29 finding.
- **S4 (diagnostics-gate phrasing):** Introduction now says "passed the pipeline's automated diagnostics gate with all checks green." Exact.
- **S5/S7 (other referees' items):** the `distinguishable`-flag semantics fix and the LassoCV-vs-1-SE tuning attribution (0.0110 vs. 0.0062) are present and consistent with the JSONs.
- **S3, S6 deferred** with stated cost–benefit reasons; suggestions are non-binding, so deferral does not affect the verdict.

## New issues introduced by the revision

None essential. Two minor notes for the record:

1. **"≤ 0.001" overstates by a hair.** The new lasso-diagnostics paragraph (Section 5.1) says the port matches the published B&N values "to ≤ 0.001 in the Lasso cells," but the `diffa`–Lasso gap is 0.00102 — printed as 0.00102 in the report's own gap table two pages earlier. Substantively irrelevant (the cell is "consistent" under the stated rule with margin to spare); a proof-stage change to "to ≈ 0.001" or "to ≤ 0.0011" would make the sentence exactly true. Suggestion only.
2. **Process caveat (orchestrator, not the paper):** the changelog discloses that `code_build/04_dml_extension.ipynb` cell 25 still generates the old single-panel figure; if that notebook is ever re-executed, it will overwrite the corrected three-panel artifact. The plotting cell should be updated at the next re-run, per the changelog's own note. This does not affect the current report, whose artifacts I verified directly.

## Comments

The revision does exactly what round 1 asked, by pure re-plotting of frozen numbers with no re-estimation, and the suggestion edits make the report's central claims falsifiable rather than asserted. I verified the regenerated figure cell-by-cell against `dml_results.json` and `replication_results.json`, recomputed the verdict rule for all 21 benchmarked cells, and re-checked the CATE window and MC SD ranges; everything traces. No essential issues remain open and nothing in the revision degrades the report. Accept.
