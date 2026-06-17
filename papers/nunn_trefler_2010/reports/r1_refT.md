# DML-Technical Referee Report

**Round:** 1
**Overall verdict:** Minor revision

## Benchmark alignment

The extension is a close, faithful implementation of the B&N (2024) Table-2 recipe for the tariffs application: PLR/DML2, K=2 at n=63, 100 sample-split repetitions, median aggregation, the B&N-adjusted SE (median-of-sqrt variant, matching `dml_tariffs_T2.R:181`), interactions (17 -> 153 features) fed only to the penalized learner exactly as B&N's `xL`/`xx` split, separate-argmin "Best" composition, and learner hyperparameters that track `ML_Functions.R`/`dml_tariffs_T2.R` line-for-line (Forest nodesize 5/ntree 1000/mtry p/3; rpart minsplit 20/minbucket 7 with CV-min cp pruning; gbm depth 2/shrinkage .01/1000 trees/bag .8/minobs 3 with 2-fold CV stopping; nnet size 3/decay .001/maxit 1000 with min-max scaling; cv.glmnet 10-fold with the lambda.1se default). All 21 benchmarked cells land within one benchmark SE of the published values (max gap 0.00308, Best/skill1_corr), all Monte-Carlo implementation flags are false, and the gap-table arithmetic recomputes exactly from `dml_results.json` + `benchmark_results.json`. The two findings below are disclosure-level (a missing lasso-selection diagnostic and one mislabeled SE convention in the forest-plot caption); neither can move any reported number.

## Checklist results

- **C1 — PASS.** Pairwise interactions present for the penalized learner only (17 -> 153 = k + k(k-1)/2), matching B&N: `recast_dml.py:383` (`X_int if m == "Lasso" else X_raw`) mirrors `Moment_Functions.R:63-67` (xL for Lasso/RLasso/Ridge/Elnet, xx otherwise); package path identical via `expand_interactions = learner_name == "Lasso"` (`recast_dml.py:487`).
- **C2 — N/A.** The canonical tariffs Table-2 menu itself contains no RLasso/PostRLasso (`dml_tariffs_T2.R:133-135`: Forest, Trees, Lasso, Nnet, Ensemble; Boosting separately). The port's CV-lasso with the 1-SE rule (`_fit_predict_lasso_1se`) matches B&N's `cv.glmnet` + `predict` default `s="lambda.1se"` (`ML_Functions.R:28,35`). Matching the benchmark is the correct call here.
- **C3 — PASS.** n_rep = 100 in port, package, and the heterogeneity refit; B&N `ite <- 100` (`dml_tariffs_T2.R:157`).
- **C4 — PASS.** Separate argmins for outcome and treatment nuisances, composed by cross-pairing residuals: `recast_dml.py:419-421` (`best_y`, `best_d`, theta from `resid_y[best_y]`, `resid_d[best_d]`) = `Moment_Functions.R:296-310` (min1/min2) and `:399` (`lm(ry[min1] ~ rz[min2] - 1)`).
- **C5 — PASS.** `median(sqrt(SE_k^2 + (theta_k - median theta)^2))` — median **of** the sqrt terms (`recast_dml.py:434`), identical to `dml_tariffs_T2.R:181`; the variant used is stated in the lib comment and in `dml_results.json.se_formula`. The CDDF sqrt-of-median variant is not silently mixed in.
- **C6 — N/A.** Generic ML correctly **not** run: router returns `generic_ml_admissible: false` for sel-on-obs continuous; no homemade proxy anywhere.
- **C7 — N/A.** Causal forest disabled in `config.yaml` with a documented reason (B&N's CF check for tariffs is in an untranscribed online appendix); no CF class to audit.
- **C8 — PASS.** K=2 at N=63 in the port (hard-wired 2 folds, `bn_dml_one_rep`) and the package path (`n_folds=2 if len(df) < 200 else 5`, notebook cell 7); B&N `nfold=2`.
- **C9 — N/A.** PLR partialling-out; no propensity model. (B&N pass `trim=c(0.01,0.99)` but the plinear branch of `Moment_Functions.R` never uses it.)
- **C10 — N/A.** No feature importances are computed or reported.
- **C11 — PASS.** `missing_learners == []`; the full declared 7-learner menu (Lasso/Trees/Boosting/Forest/Nnet/Ensemble/Best) is delivered by the faithful port; the 4-learner package subset is documented in `missing_learners_reason`; `fit_failures == {}`.
- **C12 — PASS.** Port Nnet is `hidden_layer_sizes=(3,)` at N=63 (`recast_dml.py:299`), satisfying the N<100 rule and matching B&N's `Nnet size=3` country-level setting (`dml_tariffs_T2.R:131`). The package menu excludes Nnet by design.
- **C13 — PASS.** No `best_outside_spread` condition: Best = 0.0191 / 0.0103 / 0.0070 lies inside the individual-learner range for all three treatments (e.g., skill1_corr learners span 0.0134-0.0188 with SEs ~0.010-0.016).
- **C14 — ESSENTIAL (finding 1).** Lasso-selection diagnostics are null/absent for the penalized learner in both port and package outputs. CLAN part N/A (generic ML correctly not run).
- **C15 — PASS.** Continuous treatments -> PLR with partialling-out score; GATES/generic ML not applied; heterogeneity is PLR `gate()`/`cate()` and is labeled EXPLORATORY everywhere (route, hte_results.json, gap table Panel D, paper Section 6).
- **C16 — ESSENTIAL (finding 2).** Tables are correctly per-convention labeled (gap-table note: classical for OLS rows, B&N-adjusted for DML rows; Table 5 note: "package-reported SEs"), but the forest-plot caption mislabels the package rows' convention.
- **C17 — PASS.** Continuous-D wording is "conditional-variance-weighted average of derivative (local slope) effects, NOT an average dose-response" in both `estimand_statement.md` (line 8) and `paper.tex` (estimand block + Limitation 2); they agree verbatim.
- **C18 — PASS.** Versions recorded in `dml_results.json.library_versions` (numpy 2.4.6, pandas 3.0.3, doubleml 0.11.3, sklearn 1.9.0) and restated in the paper; API usage matches the pinned versions (`LassoCV(alphas=<int>)` is valid post-sklearn-1.5; `nuisance_loss`, `gate()/cate()` with `confint(joint=True)` exist in doubleml 0.11.x).
- **C19 — PASS.** `paper_spec.cluster_structure` is null (original Table 4 uses plain `reg`, classical SEs); extension is consistently unclustered on both sides; `clustered: false` recorded per cell.
- **R2a — PASS.** Partialling-out score throughout. The port's no-intercept residual-on-residual OLS with HC0 variance (`_no_intercept_ols_hc0`) is algebraically the DML PLR influence-function variance and replicates `Moment_Functions.R:451-454` (`lm(... -1)` + `vcovHC type='HC'`); the package rows use DoubleML's own SEs/CIs.
- **R2b — PASS.** Per-learner nuisance RMSEs reported (package side: `nuisance_rmse` + `first_stage_feasibility`, incl. the honest 4.857 features-per-fold-obs ratio for Lasso) and interpreted in Table 5 notes and Limitation 3. No broken fits to exclude. Suggestion 2 asks for the port-side analogue.
- **R2c — PASS.** GATE and CATE intervals are joint via Gaussian multiplier bootstrap: `confint(level=0.95, joint=True, n_rep_boot=2000)` (`recast_dml.py:596,610`), per doubleml heterogeneity docs; the paper reads them as joint bands.
- **R2d — PASS.** The paper's headline heterogeneity claim is "no statistically detectable heterogeneity," with joint CIs covering zero and the narrow positive CATE window explicitly discounted. No over-claiming. (Flag-semantics nit in Suggestion 1.)
- **R2e — PASS.** All 21 DML differences, verdict labels (all `|gap| <= 1 x se_bench` -> consistent), and MC flags (`|gap| > 2 x mc_sd_ours` -> all false) recompute exactly from `dml_results.json` + `benchmark_results.json` (verified programmatically); the 3 OLS "exact" rows match at printed rounding. Blinding is documented (SHA-256 prefix `dcd883cff19d9e4e` in `gap_table.json`), and file timestamps confirm order: nuisance RMSEs and all DML checkpoints frozen 13:46-16:00, gap table built 20:55 — no tuning-toward-benchmark channel.

## Essential issues (BLOCKING marked)

1. **[C14] Lasso-selection diagnostics absent for the penalized learner** — ESSENTIAL
   - **Canonical behavior:** C14 requires non-null selection diagnostics for penalized learners; the design follows B&N's `xL` basis (`dml_tariffs_T2.R:77-100`), where the lasso faces p = 153 candidate features against ~31 training observations per fold (`first_stage_feasibility` correctly logs `features_per_fold_obs: 4.857`).
   - **Observed:** Neither `data/results/dml_results.json` nor the notebook records how many features the lasso retains in either nuisance (port `_fit_predict_lasso_1se`, `recast_dml.py:230-243`, discards the fitted model; package `LassoCV` pipeline coefficients never inspected).
   - **Why it matters:** At p >> n_fold with a 1-SE rule the lasso can select zero features and collapse to the training mean. The Lasso column is the single significant DML cell in two panels (diffa port, diffg package), so the reader needs evidence that "Lasso" is a genuine selection fit rather than a near-intercept predictor. This is disclosure, not magnitude: it cannot change the estimates (port matches the B&N benchmark to <= 0.001 in the Lasso cells), hence not BLOCKING.
   - **Required fix:** In `code_run/04_dml_extension.ipynb`, log the median (across reps x folds) number of non-zero lasso coefficients for `ml_l` and `ml_m` per treatment (port: return the count from `_fit_predict_lasso_1se` or recompute on one rep; package: read `named_steps['lassocv'].coef_`), add it to `dml_results.json` (e.g., `lasso_selection`), and one sentence in paper Section 5.3's notes.

2. **[C16] Forest-plot caption mislabels the SE convention of the package rows** — ESSENTIAL
   - **Canonical behavior:** Spec L4/C16: every display mixing SE conventions must label each convention. The DoubleML aggregated CI at n_rep>1 is the CI-backsolved median convention (doubleml resampling docs, `resampling.rst:219-223`), distinct from the B&N-adjusted median-of-sqrt SE.
   - **Observed:** Notebook cell 25 builds the figure with port rows as theta +/- 1.96 x B&N-adjusted SE but package rows from `r["ci"]` (DoubleML `confint()`); `paper.tex:164` states "DML rows use the B&N-adjusted standard errors", which is wrong for the four "(DoubleML)" rows per treatment. (Empirically the conventions differ materially: skill1_corr-Lasso package se 0.0103 vs B&N-adjusted 0.0131.)
   - **Why it matters:** A reader comparing port and package whiskers will attribute width differences to learners rather than to the SE convention; this is exactly the mixing C16 prohibits. Prose-only; no estimate changes — not BLOCKING.
   - **Required fix:** Amend the Figure 1 caption (and ideally the legend labels) to: "(B&N port)" rows use B&N-adjusted SEs (median of sqrt terms); "(DoubleML)" rows use the package's CI-backsolved median CIs. Optionally name the package convention in Table 5's note as well.

## Suggestions (non-binding)

1. **GATE "distinguishable" flag semantics.** Notebook cell 23 sets `distinguishable = any(joint CI excludes zero)` — a does-any-group-differ-from-zero test — while `paper.tex:219` reads it as "terciles statistically indistinguishable *from one another*". The conclusion is right here (the joint CIs overlap each other massively), but add a pairwise tercile-difference contrast (or rename the flag) so the printed claim matches the computed quantity.
2. **Port-side nuisance fit reporting.** `bn_dml_one_rep` computes per-fold RMSEs for the Best selection but discards them; surface their medians per learner in `dml_results.json` (the package panel currently carries all of R2b's weight), and consider reporting an R^2-style normalization (e.g., RMSE relative to sd(Y)=~ and sd(D)) so "0.216-0.237" is interpretable.
3. **Name the lasso-tuning difference.** The package Lasso uses CV-min lambda (`LassoCV` default) while the port uses the 1-SE rule (cv.glmnet default). Naming this in the Table 5 note would turn the "implementation details of the lasso pipelines" sentence (paper Section 5.3) into a checkable statement and explains the diffa-Lasso gap (0.0062 vs 0.0110) precisely.
4. **CATE window endpoint.** The positive lower-band window over `init` extends to grid point 8.84 (lower edge 0.0002 at 8.8427), not 8.81 as printed (`paper.tex:221`). Trivial prose correction next time the section is touched.

---

*Verdict rationale: zero BLOCKING findings — every benchmarked cell reproduces the canonical B&N values within one benchmark SE under a verified blinding protocol, and both ESSENTIAL items are disclosure/prose fixes that cannot change sign, significance, or magnitude.*
