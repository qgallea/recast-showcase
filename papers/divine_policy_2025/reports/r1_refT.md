## DML-Technical Referee Report
**Round:** 1
**Overall verdict:** Minor revision

### Benchmark alignment
The routing is correct: a staggered **binary** panel DiD is sent to rule 2.1-8a (DoubleMLDIDMulti / Callaway–Sant'Anna). DoubleMLDIDMulti is genuinely infeasible at this N (50 states, 6 never-treated, single-state cohorts → CS per-(g,t) cross-fitting throws `n_splits=5 > n_samples=4` and "0 sample(s)" errors, captured in `dml_results.json`), so `_did_plr_fallback` (recast_dml.py) estimates the DML two-way-FE analogue: a `DoubleMLPLR` with `partialling out` score on a `_post_treated` indicator over a two-way (unit+time) within-transformed panel, clustered on `fipsstat`. This is the canonical DML-TWFE fallback and is loudly and accurately flagged everywhere (dml_results.json `se_method`/`note`, estimand_statement.md, index.qmd "bottom line"). The one real deviation from the canonical recipe is **n_rep = 1** (no Monte-Carlo averaging of the cross-fit; the B&N median-SE adjustment is vacuous). K-folds = 3 on N=1050 is below the K≥5 norm but defensible given 50 clusters. No deviation rises to a sign/significance/magnitude(>20%) threat — three independent learners and the parametric TWFE anchor all coincide at +0.036…+0.041, all p < 0.025.

### Checklist results
- **C1** Pairwise interactions for penalized learners — **N/A**: only one control (`log_npo`); k(k−1)/2 = 0 interactions, so the Lasso design equals the raw single-feature design (no collapse possible).
- **C2** RLasso/PostRLasso availability — **N/A**: fallback PLR uses CV-Lasso (`LassoCV`) for nuisance; valid DML inference, no BCH guarantee. One-feature nuisance, immaterial. Disclose CV-Lasso (not BCH) in methodology.
- **C3** Number of repetitions — **ESSENTIAL**: `n_rep = 1` (config.yaml, dml_results.json `n_rep:1`). Canon B&N `ite <- 100`. Not BLOCKING here (see issue 1).
- **C4** "Best" selection logic — **N/A**: no Ensemble/"Best" refit in the DiD_PLR fallback; three learners reported side-by-side.
- **C5** SE aggregation formula — **PASS (degenerate)**: code uses `median(sqrt(SE_k² + (θ_k−median θ)²))`, the correct B&N form; with n_rep=1 it reduces to the single SE (tied to C3).
- **C6** Generic-ML proxy construction — **N/A**: observational DiD; generic-ML correctly NOT run (`generic_ml_admissible:false`).
- **C7** Causal-forest class matches identification — **N/A**: no causal forest fit on this path.
- **C8** K-folds adaptive — **ESSENTIAL (minor)**: n_folds = 3 on N=1050 (50 clusters); rule wants K≥5. DML SEs cross-fit-consistent for any K≥2; immaterial here → suggestion 1.
- **C9** Nuisance trimming — **N/A**: PLR `partialling out` score (no propensity in the score); no IRM/propensity to trim.
- **C10** Feature-importance wording — **N/A**: no CF importances reported.
- **C11** Declared learners all present — **PASS**: Forest, Lasso, Boosting all fit and reported; no silent drop.
- **C12** NeuralNet capacity vs N — **N/A**: no NeuralNet on this path.
- **C13** Best coefficient plausibility — **N/A**: no "Best"/Ensemble refit.
- **C14** Output completeness — **PASS**: `group_time_atts` empty by construction (CS infeasible) and explicitly explained; no silently-empty CLAN.
- **C15** Model-class routing vs treatment type — **PASS**: binary D → DID → PLR-`partialling out` fallback; no IRM-on-continuous, no GATES on an estimated propensity.
- **C16** SE-convention labeling — **PASS**: all columns are cluster-on-`fipsstat` SEs (same convention); estimand statement states "SE clustered by state."
- **C17** Estimand wording under heterogeneity — **PASS**: labeled "approximate average ATT, not the CS group-time estimate," carrying the staggered-TWFE caveat (subsumes the overlap/Goodman-Bacon weighting nuance). estimand_statement.md and index.qmd agree.
- **C18** Version pinning — **ESSENTIAL (minor)**: no library-version record in config/results; can't verify build==run pinning → suggestion 2.
- **C19** Clustering carried through — **PASS**: DoubleMLPLR built with `cluster_cols=fipsstat`; TWFE replication clustered by entity. Both sides clustered.
- **R2a** Score appropriate + CIs from DML SEs — **PASS**: `obj.se`/`obj.confint()`/`obj.pval` from DoubleMLPLR (orthogonal, clustered), not post-residualization OLS.
- **R2b** Nuisance loss reported/honest — **PASS**: `nuisance_loss` per learner (ml_l ≈ 0.06, ml_m ≈ 0.26); non-degenerate, reported.
- **R2c** Joint (simultaneous) CIs — **N/A**: no multi-group GATE/CATE read (single ATT; group-time cells unavailable).
- **R2d** Heterogeneity claims proportionate to power — **PASS**: HTE explicitly reported as unavailable; no over-claiming.
- **R2e** Benchmark-mode arithmetic — **N/A / PASS**: not benchmark mode (no independent B&N revisit). Gap-table verdicts recompute correctly (TWFE CI [0.006,0.069] and all DML CIs exclude 0 → "consistent"; counts 4). No tuning-toward-benchmark.

### Essential issues (BLOCKING marked)
1. **[C3] Single cross-fitting repetition (n_rep = 1)** — ESSENTIAL (not BLOCKING)
   - **Canonical behavior:** B&N `dml_tariffs_T2.R` sets `ite <- 100`; the median-θ / median-SE aggregation requires many repetitions to average out cross-fit split randomness.
   - **Observed:** `config.yaml n_rep:1`, `dml_results.json "n_rep":1` for all three learners; `bn_se_median == se` (aggregation is vacuous at n_rep=1).
   - **Why it matters / why NOT blocking:** with a single split the reported SE/point carry split-specific noise. But the canonical fix (n_rep≥100) would not plausibly move sign/significance/magnitude >20%: the three structurally different learners coincide (0.0358 / 0.0391 / 0.0414, spread < 16%), and the non-stochastic parametric TWFE anchor is 0.0377 (se 0.0162) — essentially on top of the DML estimates. The nuisance task (one control, FE-residualized, near-deterministic `_post_treated`) is low-variance. Hence ESSENTIAL disclosure, not a conclusion-threatening defect.
   - **Required fix:** rerun the DiD_PLR fallback with `n_rep ≥ 100` (or, at minimum, state in the report that the DiD pathway runs a single split and that the B&N median-SE adjustment is therefore inactive). Only the call in `build_project.py` (`n_rep=1`) needs raising.

### Suggestions (non-binding)
1. **K-folds:** raise `n_folds` from 3 to 5 — N=1050 with 50 clusters comfortably supports K=5 and matches the canonical K≥5 rule (no expected effect on the conclusion).
2. **Version pinning (C18):** record doubleml/sklearn/linearmodels versions alongside the results JSON so build==run pinning is auditable.
3. **C2 disclosure:** note in the methodology that the penalized-learner nuisance uses CV-Lasso (`LassoCV`), which has valid DML inference but not the BCH post-selection guarantees.
4. **Report transparency:** the index.qmd "DML extension" rows are the *same* `_post_treated` TWFE DiD as the replication, only with ML nuisances partialling out the single size control; a one-line note that the DML and parametric estimates therefore target the identical estimand (and that the value-add is robustness of the first stage, not a new estimand) would prevent a reader over-reading the "extension."
