# Final Review Report

**Paper:** The Structure of Tariffs and Long-Term Growth
**Original authors:** Nunn, N. & Trefler, D. (American Economic Journal: Macroeconomics, 2010)
**Rounds completed:** 2 of 3
**Final verdict:** Ready

---

## What This RECAST Contributes

This RECAST does three things, all of them well. First, it re-establishes the Nunn–Trefler Table 4 headline results from the original data via a declared Stata-to-Python port: 3/3 coefficients SUCCESS at printed precision (absolute gaps 0.00016–0.00040), n = 63 throughout, classical SEs matched to the original `reg` convention. Second, it independently reproduces the published Baiardi & Naghi (2024) DML extension under a verified blinding protocol (SHA-256 freeze, timestamps audited by the technical referee): all 21 benchmarked DML cells land within one benchmark SE of B&N's Table 2 (max gap 0.00308), with all Monte-Carlo implementation flags clean. Third — and specific to this run — it serves as the Phase-2 regression test: the automated pipeline reproduced the Phase-1 hand-built results **bit-for-bit** (all 21 DML cells with |delta| = 0), which is direct evidence that the pipeline automation introduces no numerical drift.

Substantively, the DML extension qualifies the original finding the same way B&N's published paper does: the positive skill-bias-of-tariffs/growth association survives flexible nonlinear conditioning in sign across all 7 learners and all 3 treatments, but the point estimates roughly halve (e.g., `skill1_corr`: OLS 0.035 vs DML Best 0.019) and most 95% intervals cover zero at n = 63, with one benchmarked cell (`diffa`–Lasso, t ≈ 2.29) significant at 5%.

**"Would I be pleased to have written this, flaws and all?"**
Yes. A clean exact replication, a blinded 21/21 reproduction of a published DML benchmark, an honestly-labeled exploratory heterogeneity branch, and a bit-for-bit pipeline regression test — the round-1 general referee passed the same test explicitly, and both referees voted Accept in round 2. The flaws that remain are two one-word prose nits.

---

## Replication Summary

| Specification | Published | Replicated | Delta (%) | Status |
|--------------|-----------|-----------|-----------|--------|
| Table 4 col 1: growth on `skill1_corr` (t = 3.50) | 0.035 | 0.03484 | −0.46% | PASS (SUCCESS) |
| Table 4 col 2: growth on `diffa` (t = 3.29) | 0.016 | 0.01626 | +1.64% | PASS (SUCCESS) |
| Table 4 col 4: growth on `diffg` (t = 4.91) | 0.020 | 0.01960 | −1.98% | PASS (SUCCESS) |

**Overall:** 3/3 specs SUCCESS in a deterministic regime; replication gate PASS. All deltas are within printed rounding of the published table; replicated t-statistics (3.498, 3.286, 4.908) match the printed values to two decimals, and n = 63 matches in every spec.

---

## DML Extension Summary

PLR (partialling-out), K = 2 folds, 100 sample-split repetitions, median aggregation, B&N-adjusted SEs for the port rows. CIs below are theta ± 1.96 × SE; p-values approximate (normal for DML rows, t(44) for OLS).

| Treatment | Method | Coef | SE | 95% CI | p-value |
|-----------|--------|------|----|--------|---------|
| `skill1_corr` | OLS (replicated) | 0.0348 | 0.0100 | [0.0153, 0.0544] | 0.001 |
| | Best (DML port) | 0.0191 | 0.0111 | [−0.0027, 0.0409] | 0.086 |
| | Ensemble (DML port) | 0.0188 | 0.0122 | [−0.0051, 0.0427] | 0.122 |
| `diffa` | OLS (replicated) | 0.0163 | 0.0049 | [0.0066, 0.0260] | 0.002 |
| | Best (DML port) | 0.0103 | 0.0053 | [−0.0002, 0.0207] | 0.054 |
| | Ensemble (DML port) | 0.0100 | 0.0058 | [−0.0013, 0.0213] | 0.084 |
| `diffg` | OLS (replicated) | 0.0196 | 0.0040 | [0.0118, 0.0274] | <0.001 |
| | Best (DML port) | 0.0070 | 0.0052 | [−0.0031, 0.0171] | 0.177 |
| | Ensemble (DML port) | 0.0089 | 0.0055 | [−0.0019, 0.0197] | 0.107 |

**Key finding:** Under flexible ML controls every estimate stays positive but shrinks to roughly half the OLS magnitude and loses 5% significance in most cells — the lone significant benchmarked cell is `diffa`–Lasso (0.0110, SE 0.0048, CI [0.0016, 0.0204]); the package panel adds three isolated significant cells (`skill1_corr`–Lasso p = 0.038, `diffa`–Forest p = 0.035, `diffg`–Lasso p = 0.005). This exactly reproduces B&N's published pattern (21/21 cells consistent within one benchmark SE under blinding), so it is a validation of their finding rather than a new discovery. The exploratory heterogeneity branch (GATE/CATE over `init` and `human_cap`, joint 95% bands) finds no statistically detectable heterogeneity at n = 63.

---

## Review Process Summary

Round 1 produced two Minor-revision reports synthesized into 3 essential issues, 0 blocking, and 7 suggestions. The revision touched only `paper.tex` and the figure artifacts (no re-estimation; all numbers re-read from frozen JSONs). Round 2: both referees verified the fixes against the artifacts and JSONs and voted **Accept**.

| Issue | Raised (round) | Category | Resolved? | How |
|-------|---------------|----------|-----------|-----|
| E1: Figure 1 showed one `skill1_corr` panel while caption/text claimed all three treatments | 1 (refG) | Essential | Yes | Regenerated as 1×3 panel figure by pure re-plotting of frozen JSONs; round-2 spot-checks confirmed every plotted CI traces to the JSONs |
| E2 [C16]: Figure 1 caption mislabeled the SE convention of the "(DoubleML)" rows | 1 (refT) | Essential | Yes | Caption now labels all three conventions per row type (B&N-adjusted / CI-backsolved median / classical) plus a whisker-width warning; Table 5 note matched |
| E3 [C14]: Lasso-selection diagnostics absent (p = 153 vs ~31 obs/fold) | 1 (refT) | Essential | Yes (as disclosure) | New Section 5.1 paragraph discloses the gap, the risk, and the bound (port matches B&N Lasso cells to ~0.001, gaps −0.00025/0.00102/−0.00043); refT accepted this as proper under the no-re-run instruction |
| S1: "consistent" verdict rule unstated | 1 | Suggestion | Addressed | Rule added to gap-table note: \|ours − benchmark\| ≤ 1 × SE_bench; refG recomputed all 21 cells, worst case 0.98 MC SD / 0.383 benchmark SE margins hold |
| S2a/b/c: MC SD range 0.0019→0.0021; CATE window 8.81→8.84; abstract "(lasso marginal)" | 1 | Suggestion | Addressed | All three corrected and verified against the JSONs in round 2 |
| S3: per-row MC-flag column in Table 2 | 1 | Suggestion | Deferred | Flag is false for all 21 rows and stated in the note; a column of identical entries adds width, not information |
| S4: "automated referee review" phrasing | 1 | Suggestion | Addressed | Now "passed the pipeline's automated diagnostics gate with all checks green" |
| S5: GATE `distinguishable` flag semantics | 1 | Suggestion | Addressed | Text now attributes the flag to its computed quantity (any-group-vs-zero), pairwise claim grounded separately |
| S6: surface port-side nuisance RMSEs | 1 | Suggestion | Deferred | Requires re-running estimation with instrumented wrappers; disclosed in the E3 paragraph; logged as open framework work |
| S7: name the LassoCV-min vs 1-SE tuning difference | 1 | Suggestion | Addressed | Table 5 note names it and attributes the `diffa`–Lasso port/package gap (0.0110 vs 0.0062) |
| "to ≤ 0.001" wording in the E3 paragraph (actual worst gap 0.00102) | 2 (refG) | Suggestion | Open | One-word proof-stage edit |
| Conclusion: "two further isolated cells" should be "three" | 2 (refT) | Suggestion | Open | One-word edit; Section 5.3 already lists the three correctly |
| Notebook cell 25 still generates the old single-panel figure | 1–2 (changelog/both) | Process caveat | Yes | Fixed upstream in the framework builder; no longer a risk for future re-runs |

---

## Remaining Items

No essential issues remain. The paper is ready to share. The suggestions below would strengthen it further but are optional.

| # | Item | Category | Action needed |
|---|------|----------|---------------|
| 1 | Section 5.1 says the port matches the B&N Lasso cells "to ≤ 0.001"; the worst gap is 0.00102 (printed in the paper's own gap table) | Suggestion | Change to "≈ 0.001" or "≤ 0.0011" |
| 2 | Conclusion says the package panel adds "two further isolated cells" significant at 5%; Section 5.3 correctly lists three (`skill1_corr`–Lasso 0.038, `diffa`–Forest 0.035, `diffg`–Lasso 0.005) | Suggestion | Change "two" to "three" |
| 3 | Port-side per-learner nuisance RMSEs and lasso retained-feature counts are computed internally but not stored (deferred S6 / data side of E3) | Suggestion | Open framework work: instrument the wrappers at the next re-estimation; the paper already discloses the gap |

*Category: **Essential** = must fix before sharing · **Suggestion** = would improve, optional*

---

## Notes for the Reader

- **What the RECAST says about the original finding:** it confirms the direction and qualifies the strength. DML estimates stay positive everywhere but are roughly half the OLS magnitudes and mostly insignificant at 5% with n = 63 — precisely B&N's published conclusion, reproduced here blind. Note that Nunn & Trefler themselves framed Table 4 as a robust correlation, not causality; the RECAST inherits that frame and the DML relaxes only the functional form, never the identification.
- **Small-sample caveats are real but disclosed:** n = 63, K = 2 folds (~31 obs/fold), and 153 interaction features for the lasso (4.86 features per fold-observation). The lasso-selection diagnostic gap (Item 3) means we cannot rule out near-intercept lasso fits from the artifacts alone; agreement with B&N's cv.glmnet benchmark under the same p >> n condition is the external corroboration. A worthwhile manual check before treating this as final: re-run one repetition with instrumented wrappers and confirm the lasso retains a non-trivial feature set.
- **The heterogeneity section is exploratory and should stay that way:** no benchmark exists for the GATE/CATE quantities, joint bands cover zero, and "no statistically detectable heterogeneity" at n = 63 reflects low power, not evidence of homogeneity. The paper already refuses to interpret the narrow positive CATE window (init ≈ 8.54–8.84), correctly.
- **What the pipeline cannot verify:** data provenance (data_tariffs.dta is taken as the AEJ archive file), the original paper's theory and mechanism claims (Tables 5–9 of the original were out of scope), and the selection-on-observables assumption itself.
- **Process note:** this run doubles as the Phase-2 regression test — the automated pipeline matched the Phase-1 hand-built results bit-for-bit (all 21 DML cells |delta| = 0) and B&N's published Table 2 at 21/21 consistent plus 3/3 exact OLS replications under verified blinding. The one process risk flagged in review (the notebook figure cell that could overwrite the corrected three-panel figure on re-execution) has since been fixed in the framework builder.
