## DML-Technical Referee Report
**Round:** 1
**Overall verdict:** Minor revision

### Benchmark alignment
RECAST routes this open-access, continuous-intensity ("dose") panel DiD to `DID_PLR` — a two-way (county+time) within transform plus a DoubleML PLR (`score="partialling out"`) on the exposure×post interaction, clustered by county (`recast_dml.doubleml_did_plr`). This is the correct canonical analogue of a TWFE DiD for a continuous treatment, and (correctly) does NOT misuse `DoubleMLDIDMulti` (which requires binary staggered timing) or generic-ML GATES (defined for RCT-binary treatments, CDDF 2018). Clustering is carried through on both the replication (`PanelOLS ... cluster_entity=True`) and extension (`DoubleMLData(... cluster_cols=id_col)`) sides — a clean C19 pass. The two material deviations from the strictest recipe are (1) `n_rep = 1` (no repetition averaging), and (2) the penalized-learner (Lasso) path is fed only the 5 raw controls with no pairwise-interaction basis. Neither is sign/significance-changing here, so neither blocks; both warrant disclosure.

### Checklist results
- **C1 — Pairwise interactions for penalized learners:** ESSENTIAL (Issue 1) — `doubleml_did_plr` calls `make_learners` directly, never `interaction_design`; Lasso sees 5 raw controls only.
- **C2 — RLasso/PostRLasso availability:** ESSENTIAL (Issue 2) — Lasso = `LassoCV`, no BCH/hdmpy λ; valid DML inference but not BCH guarantees; undisclosed.
- **C3 — Number of repetitions:** ESSENTIAL (Issue 3) — `n_rep=1` (config.yaml + build_project.py). Not <20-rep BLOCKING territory because the estimate is not an MC median, but single-split sensitivity is undisclosed.
- **C4 — "Best" selection logic:** N/A — no Best/Ensemble refit in this DID_PLR path; four learners reported side-by-side, ml_l and ml_m use the same learner.
- **C5 — SE aggregation formula:** PASS (vacuously) — code uses the B&N `median(sqrt(SE_k² + (θ_k−med)²))` form; at n_rep=1 it degenerates to the package SE, and the report uses `obj.se` consistently.
- **C6 — Generic-ML proxy construction:** N/A — observational + continuous treatment; generic ML correctly NOT run (`generic_ml_admissible=false`).
- **C7 — Causal-forest class matches identification:** N/A — no causal forest; heterogeneity via PLR `gate()`/`cate()`.
- **C8 — K-folds adaptive:** PASS — K=5 on N=8194 (≥200).
- **C9 — Nuisance trimming:** N/A — PLR, no propensity model.
- **C10 — Feature-importance wording:** PASS — no causal-moderator language; GATE/CATE labeled EXPLORATORY.
- **C11 — Declared learners all present:** PASS — all four (Lasso/Forest/Boosting/Trees) present with finite coef/SE; no silent drop.
- **C12 — NeuralNet capacity vs N:** N/A — NN not in the learner set.
- **C13 — Best coefficient plausibility:** N/A — no Best refit.
- **C14 — Output completeness:** PASS — gap table, dml_results (with nuisance_loss per learner), hte_results (GATE+CATE), forest_plot.png all present; CLAN N/A (no generic ML).
- **C15 — Model-class routing vs treatment type:** PASS — continuous treatment → PLR; heterogeneity is PLR gate/cate, labeled exploratory; no IRM/GATES on a continuous treatment.
- **C16 — SE-convention labeling:** PASS — replication = cluster(FIPS) t-stats; extension = clustered DoubleML SE; both labeled, no mixing within a column.
- **C17 — Estimand wording under heterogeneity:** ESSENTIAL (Issue 4) — continuous-D estimand described as "average partial effect"/"average-county double difference" without the conditional-variance-weighted-average-derivative caveat the spec L6/C17 requires for continuous D.
- **C18 — Version pinning:** ESSENTIAL (Issue 5) — no library versions recorded in config.yaml or results JSONs; port-vs-run reproducibility not pinned.
- **C19 — Clustering carried through:** PASS — replication and extension both cluster on FIPS; `cluster_cols=id_col` passed to DoubleMLData.
- **R2a — Score appropriate / CIs from DML SE:** PASS — partialling-out PLR; CIs from `obj.confint()`, not post-residualization OLS.
- **R2b — Nuisance MSE/R² reported honestly:** ESSENTIAL (Issue 6) — only RMSE (`nuisance_loss` ml_l≈1.32, ml_m≈4.79–5.50) is logged, not surfaced in the report, and never interpreted (no R²; reader cannot judge first-stage fit).
- **R2c — Joint (simultaneous) CIs:** PASS — `gate.confint(joint=True, n_rep_boot=2000)` and `cate.confint(... joint=True)`.
- **R2d — Heterogeneity claims proportionate to power:** ESSENTIAL (Issue 7) — report states "groups are statistically distinguishable," but the GATE joint CIs all overlap each other heavily (T1 0.020, T2 0.011, T3 0.027; only T3 excludes zero); the `distinguishable` flag only means "≥1 group CI excludes 0," not that groups differ from one another.
- **R2e — Benchmark-mode arithmetic:** N/A — not benchmark/gap-table-vs-B&N mode; the gap table compares to the paper's own published Table 5, recomputable from replication_results.json.

### Essential issues (BLOCKING marked)
1. **[C1] Lasso receives no pairwise-interaction basis** — ESSENTIAL
   - **Canonical behavior:** B&N `dml_tariffs_T2.R` feeds penalized learners k → k+k(k−1)/2 features so Lasso is not shrunken OLS.
   - **Observed:** `doubleml_did_plr` calls `make_learners` directly; unlike `doubleml_model` (`expand_interactions = learner_name=="Lasso"`), it never calls `interaction_design`. Lasso here sees only the 5 raw county controls on the FE-residualized panel.
   - **Why it matters:** the ML-vs-OLS contrast for the Lasso column is weak (Lasso ≈ linear). Not BLOCKING: Lasso (0.0207) sits with Forest (0.0203)/Boosting (0.0217), all positive and significant, so sign/significance/magnitude do not move >20%.
   - **Required fix:** either expand interactions in the DID_PLR Lasso path or add one sentence disclosing that the penalized learner uses only main effects (k=5) on the residualized panel.

2. **[C2] No BCH/RLasso penalty** — ESSENTIAL
   - **Canonical behavior:** BCH-penalty lasso (hdmpy / BCH-λ) gives the post-double-selection guarantees (Belloni-Chernozhukov-Hansen 2014).
   - **Observed:** `make_learners` Lasso = `LassoCV(cv=5)`. CV-Lasso has valid DML inference but not BCH theory.
   - **Required fix:** one-line methodology disclosure; no re-run needed.

3. **[C3] n_rep = 1 (no repetition averaging)** — ESSENTIAL
   - **Canonical behavior:** B&N `ite <- 100`; ≥100 reps median out cross-fitting split noise.
   - **Observed:** config.yaml `n_rep: 1`; build_project.py `n_rep=1`; dml_results `"n_rep": 1`.
   - **Why it matters:** single-split → the reported point/SE depend on one fold draw. Not BLOCKING (the estimate is not presented as an MC median, four learners agree, and a TWFE anchor exists), but the report should disclose split sensitivity or bump n_rep.
   - **Required fix:** raise n_rep to ≥10–100 in build_project.py, OR add a "single cross-fitting split; results stable across learners" caveat.

4. **[C17] Continuous-D estimand wording** — ESSENTIAL
   - **Canonical behavior:** for continuous D, the PLR coefficient is a conditional-variance(of D)-weighted average derivative, not "the ATE"/a clean average effect (spec L6).
   - **Observed:** estimand_statement.md and index.qmd call it "the FE-adjusted average partial effect"/"the average-county double difference" with no weighting caveat.
   - **Required fix:** add the variance-weighted-average-derivative caveat to estimand_statement.md.

5. **[C18] Versions unpinned** — ESSENTIAL
   - **Observed:** config.yaml records only n_rep/learners; no doubleml/sklearn/linearmodels versions in any artifact.
   - **Required fix:** log library versions alongside the results JSONs.

6. **[R2b] Nuisance fit not surfaced/interpreted** — ESSENTIAL
   - **Observed:** `nuisance_loss` (RMSE only) is in dml_results.json but absent from index.qmd; no R²; no honest read of first-stage fit.
   - **Required fix:** surface per-learner nuisance R²/RMSE in the report with one interpretive sentence.

7. **[R2d] "Groups statistically distinguishable" overclaims** — ESSENTIAL
   - **Canonical behavior:** at modest power, say groups are indistinguishable when joint CIs overlap.
   - **Observed:** index.qmd "groups are statistically distinguishable," but hte_results `ci_joint` for T1/T2/T3 overlap heavily and only T3 excludes zero; `distinguishable=true` is set by `any(joint_ci_excludes_zero)`, which is NOT a between-group test.
   - **Required fix:** rephrase to "the high-NonRep tercile effect is individually significant; terciles are NOT statistically distinguishable from one another (joint CIs overlap)."

### Suggestions (non-binding)
1. Report the four learners' agreement (0.014–0.022) explicitly as a robustness signal alongside the TWFE anchor 0.0193.
2. Consider adding an Ensemble/median-of-learners column for a single headline extension number.
3. State the cluster count (n_ids=842) next to the clustered-SE claim so readers can judge the asymptotics.
4. Note that ml_m RMSE (≈4.8–5.5) is large relative to ml_l (≈1.3): the treatment (exposure×post) is hard to predict from the 5 controls, which is reassuring for identification but worth one sentence.
5. If n_rep is raised, log per-split draws (dml_reps) so C5 aggregation can be audited directly.
