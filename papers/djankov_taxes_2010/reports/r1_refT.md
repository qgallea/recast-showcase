## DML-Technical Referee Report
**Round:** 1
**Project:** djankov_taxes_2010 (Djankov et al. 2010, corporate taxes -> investment; B&N 2024 Table 1 Panel A)
**Overall verdict:** Minor revision

### Benchmark alignment
The extension is a faithful port of the Baiardi & Naghi (2024) Table 1 Panel A
PLR pipeline (DML2, K=2 at N=61, n_rep=100, median aggregation, B&N adjusted
median SE) for three mutually-exclusive continuous tax treatments (statutory,
effective, effective_5yr — confirmed from dml_results bn_port + package keys).
Routing (sel-on-obs + continuous -> PLR partialling-out) is correct
(recast_dml.route_estimand 2.1-4); the penalized-learner interaction basis is
built (12 -> 78); the notebook is genuinely BLINDED to benchmark_results.json
and uses fixed library hyperparameters, so there is NO benchmark-chasing. All
21 DML gap-table differences and the control-discipline sensitivity difference
recompute exactly from the package. The single material deviation is a
verdict-labeling inconsistency: three of the four cells labeled "tension" are
well inside 1x the benchmark SE and are "consistent" under the project's own
documented two-layer rule. No conclusion changes, so nothing is BLOCKING.

### Checklist results
- C1 Pairwise interactions (penalized) — PASS. interaction_design builds
  k + k(k-1)/2 = 12 + 66 = 78 features for Lasso (recast_dml.py:256-265);
  interactions_used=true, n_features_after_interactions=78
  (k(k+1)/2 == k+k(k-1)/2 identically). Lasso features_per_fold_obs=2.557,
  trees=0.393 — both recomputed exactly.
- C2 RLasso/PostRLasso — ESSENTIAL (T3, already disclosed). CV-Lasso+1se, not
  BCH plug-in; disclosed in paper.tex 343-348. Adequate; keep.
- C3 n_rep — PASS. n_rep=100 everywhere (config, dml_results, package cells).
  B&N ite=100.
- C4 "Best" selection — PASS. Separate argmins for outcome (best_y) and
  treatment (best_d) nuisances, refit when different (recast_dml.py:457-460).
- C5 SE aggregation — PASS. median(sqrt(SE_k^2 + (theta_k - median theta)^2))
  (recast_dml.py:472); matches B&N R code; stated in se_formula and paper 336.
- C6 Generic-ML proxy — N/A. Observational + continuous treatment;
  generic_ml_admissible=false; none run. Correct (causal-forest would be the
  canonical observational heterogeneity tool, but none declared).
- C7 Causal-forest class — N/A. causal_forest.enabled=false.
- C8 K-folds adaptive — PASS. K=2 at N=61 (<200), matching B&N nfold=2.
- C9 Nuisance trimming — N/A. PLR, no propensity model.
- C10 Feature-importance wording — N/A. No CF importances.
- C11 Declared learners present — PASS. missing_learners=[], fit_failures={};
  7 learners (4 package + Nnet/Ensemble/Best via port).
- C12 NeuralNet capacity — PASS. Port Nnet hidden_layer_sizes=(3,) at N<100
  (recast_dml.py:337) — exactly the rule. (CDDF NeuralNet (20,) never ran.)
- C13 Best plausibility — PASS. Best 5yr -0.198 sits inside learner spread, near
  Forest/Lasso; no best_outside_spread.
- C14 Output completeness — PASS. Lasso diagnostics non-null; CLAN N/A;
  interactions_used reporting matches the executed feature set.
- C15 Routing vs treatment type — PASS. Continuous -> PLR (not IRM); no
  GATES/generic-ML on a continuous treatment; heterogeneity labeled EXPLORATORY.
- C16 SE-convention labeling — ESSENTIAL (T2). DML port rows correctly labeled
  B&N-adjusted median SE (verified). But the control-discipline row prints
  0.083 (= package se) while the note calls it "the same B&N-adjusted median
  SE as the port" (true value 0.089). Per-column label slip; fix.
- C17 Estimand wording — PASS. estimand_statement.md and paper.tex 184-198 agree:
  continuous-D PLR coefficient = conditional-variance-weighted average of
  local-slope (derivative) effects, explicitly NOT an ATE/dose-response; the
  paper states it never calls the DML coefficient "the ATE" (197-198).
- C18 Version pinning — PASS. library_versions recorded (doubleml 0.11.3,
  sklearn 1.9.0, numpy 2.4.6, pandas 3.0.3).
- C19 Clustering — N/A. cluster_structure=null; cluster_cols=null on both sides;
  original not clustered.
- R2a Score / DML SEs — PASS. partialling-out; inference from per-rep DML draws.
- R2b Nuisance honesty — PASS. Per-learner RMSE reported; small-n caveat in
  paper 350-357. ml_l~5, ml_m~6-8 are large but disclosed as a small-N property.
- R2c Joint CIs — N/A. No GATE/CATE computed.
- R2d Heterogeneity power — N/A. No heterogeneity claims.
- R2e Benchmark arithmetic + two-layer labels — ESSENTIAL (T1). Differences
  recompute exactly; no sign-tuning; port blinded/untuned. BUT materiality
  LABELS contradict the documented rule (issue 1).

### Essential issues (BLOCKING marked)

1. **[R2e] Four "tension" labels inconsistent with the documented materiality
   rule** — ESSENTIAL (NOT BLOCKING).
   - **Canonical behavior:** recast_dml.stochastic_agreement (lines 240-245):
     |gap| <= se_bench -> "consistent"; se_bench < |gap| <= 2*se_bench ->
     "tension". Primary (MC-implementation) layer flags only if
     |gap| > 2*mc_sd_ours.
   - **Observed:** gap_table.json + paper.tex label 4 five-year cells "tension":
     Lasso (gap -0.0155, |gap|/se=0.16), Boosting (+0.0208, 0.23), Ensemble
     (+0.0122, 0.12), Nnet (+0.105, 1.04). Under the documented rule ONLY Nnet
     is "tension"; Lasso/Boosting/Ensemble are deep inside 1x se -> "consistent".
     None trips the MC-implementation layer (all |gap| < 2*mc_sd_ours). The
     reproducible counts are ~20 consistent / 1 tension, not 17 / 4. (Note: the
     audit-prompt heads-up that the tension cells are "Lasso/Trees ~0.02-0.035"
     is itself off — Trees (0.0243) is labeled consistent; the labeled set is
     Lasso/Boosting/Ensemble/Nnet.)
   - **Why it matters:** No conclusion changes — the labels are MORE conservative
     than the rule warrants (over-flagging disagreement, the opposite of
     benchmark-chasing), all four are reported with the same sign, and the Nnet
     0.105 gap is explicitly called out. But the 3/17/4 verdict counts printed in
     the abstract, gap-table note (paper.tex 261), Sec 4.3, Limitations, and
     Conclusion are not reproducible from the stated two-layer rule.
   - **Required fix:** Either (a) re-label via stochastic_agreement so only Nnet
     (5yr) is "tension", and update the 3/17/4 counts everywhere; or (b) if a
     stricter gap-table threshold was used intentionally, state it explicitly in
     the gap-table note and reconcile it with the lib's stochastic_agreement.
     Do not leave two un-reconciled definitions of "tension" in the repo.

2. **[C16] Control-discipline sensitivity SE convention mislabeled and n_rep
   undisclosed** — ESSENTIAL.
   - **Canonical behavior:** spec L4 — every column's SE convention labeled.
   - **Observed:** Gap-table note (paper.tex 268-270) and Table 3 (442-443) show
     -0.230 (0.083) and call it "the same B&N-adjusted median SE as the port."
     0.083 = package se (0.08343, suspect_controls_sensitivity.json); the
     B&N-adjusted median SE is bn_se_median = 0.0892. The CI [-0.387,-0.066] and
     p=0.006 are package quantities. The sensitivity also ran at n_rep=50
     (notebook cell 3d374cce: min(n_rep,50)), not 100 — undisclosed.
   - **Why it matters:** Sign and significance hold under either SE, so no
     conclusion changes, but the label is wrong and the reduced n_rep is hidden.
   - **Required fix:** Either report the sensitivity SE as 0.089 (to match the
     "same convention as the port" claim) or relabel the row as
     package-convention; and disclose n_rep=50 for the sensitivity fit.

3. **[C2] CV-Lasso vs BCH disclosure** — ESSENTIAL (already satisfied; keep).
   - **Canonical behavior:** Belloni-Chernozhukov-Hansen (2014) plug-in penalty.
   - **Observed:** CV-Lasso+1se (recast_dml.py:268-281); paper.tex 343-348
     discloses this and that BCH guarantees do not transfer.
   - **Required fix:** None; retain the disclosure verbatim.

### Suggestions (non-binding)
1. estimand_statement "Population: analysis sample n=85" is a slight misnomer —
   every estimate is on complete-case N=61. State n=61 (estimation sample) with
   the 85-row file as provenance, to match the gap table and paper body.
2. The gap-table "difference" is ours-minus-benchmark on the stored (not
   displayed) point estimate; Forest 5yr shows 0.0040 vs recomputed 0.0039
   (rounding of stored -0.20005). Harmless; note it computes on stored values.
3. Surface the package-DoubleML 5yr coefficients (e.g. Forest -0.195, CI
   [-0.352,-0.036]) in the gap table, not only the forest plot, since Sec 4.2
   (367) leans on the package CI for the significance claim.
4. State in the methodology that the B&N-port per-split SE is the HC0
   partialled-out SE (recast_dml._no_intercept_ols_hc0) feeding the adjusted
   median, so readers can distinguish it from the package SE.
