# DML-Technical Referee Report
**Round:** 2 (verification pass)
**Overall verdict:** Accept

This is a verification pass against `changelog_1.md`. Under the implicit bargain
(Berk et al. 2017) I raise no new round-1-visible essentials; I only verify the
documented fixes against the executed artifacts and confirm no new defect was
introduced. All five items (B1 + E1–E4) verify against code, not just JSON, and
the central finding (β₂ divergent) was sharpened, not benchmark-chased.

### B1 [C6/C19] — blockZ randomization strata restored — VERIFIED (blocking cleared)
- **Code fix is real, not a JSON edit.** Notebook cell `c2020f19` defines
  `add_fixed_effects(df, ident, drop_first=False)`, which one-hots
  `paper_spec.identification.fixed_effects` and returns `base + fe_cols`. The
  executed cell prints 6 dummies (`blockZ_17/18/19/27/28/29`), and `controls`
  (now 30 = 24 + 6) is the single covariate object passed to BOTH estimation
  paths:
  - IRM nuisances: `rd.doubleml_model(..., controls, ...)` (cell `7a33c99d`).
  - CDDF proxy covariate set: `rd.run_cddf(dsub, ..., controls, ...)` (cell
    `0aeb6f09`) — so B(Z)/S(Z) condition on the strata (`recast_dml.py:679,
    684-689`).
- **JSON confirms:** `dml_results.n_features_raw = 30`,
  `n_features_after_interactions = 30`; `hte_results.covariates_include_fixed_effects`
  lists the 6 dummies; `hte_results.propensity = 0.5131` computed on the
  estimation sample (suggestion S-prop partially adopted). Replication side used
  `drop_first=True` (5 dummies, `replication_results.fixed_effects_included`),
  correctly avoiding intercept collinearity.
- **β₂ re-run reported honestly, NOT tuned.** Executed output: NeuralNet (best)
  β₂ = 0.199556 (`hte_results.cddf.learners.NeuralNet.blp.beta2`); the changelog's
  "0.1996" is this value, not a rounded benchmark target. Movement from the
  round-1 0.178 is +0.0216 — well inside one benchmark-implied SE (0.206) and
  far from B&N's 0.651. The gap is −0.4514 (recomputed exactly; gap_table row
  verdict still **"divergent"**, ≈ 2.19 benchmark-SEs). Candidate (c) is
  therefore **eliminated**, not confirmed (paper §5.5/§candidates,
  lines 442–451). ITT moved 0.0066 → 0.0018 (`replication_results.replicated_coef
  = 0.0018078`), which is *toward* the null benchmark 0.002 but both are null —
  not a sign/significance change and not chased. **Blocking cleared.**
- **No new defect:** with blockZ in the IRM nuisances, `propensity_diag` shows
  m̂∈[0.022,0.974] (Forest) / [0.010,0.984] (Boosting), trimmed_share 0.0 — no
  new overlap/trimming pathology introduced.

### E1 [C3] n_rep = 20 disclosure — VERIFIED (prose)
`dml_results.n_rep` still 20 (unbenchmarked IRM rows; benchmarked CDDF kept
`n_splits = 100`, confirmed in every `hte_results.cddf.learners.*.n_splits`).
Boosting MC-dispersion qualifier added per the round-1 ask. Acceptable as
disclosed; no re-run owed for this item.

### E2 [C9/R2b] Propensity diagnostics — VERIFIED (lib + report)
- Library fix is real: `recast_dml.py:584-601` adds `nuisance_loss_metric`
  (ml_m ⇒ `"logloss"`, ml_g0/g1 ⇒ `"rmse"`) and, for IRM, `propensity_diag`
  (min/max + below/above-threshold shares + trimmed_share).
- JSON confirms both learner blocks carry `nuisance_loss_metric` with
  `"ml_m": "logloss"` and `propensity_diag` with `trimmed_share: 0.0`.
- Paper §IRM (lines 638-647) relabels the m column as log-loss, reports the m̂
  ranges and zero trimmed share, and notes both propensity log-losses (0.800,
  0.903) exceed the known-constant entropy 0.693 (expected under school-level
  randomization). The mislabel is corrected.
- Minor non-blocking note: `propensity_diag.known_propensity_entropy` is `null`
  in the JSON (the 0.693 figure is computed in paper prose only). Harmless —
  not an essential, and not round-1-visible; carried as a framework follow-up.

### E3 [C1/C14] interactions_used — VERIFIED
Builder now conditions `interactions_used` on a penalized learner running
(cell `4b7e866f`: `_PENALIZED` set; `penalized_ran` False here). JSON:
`interactions_used: false`, `interactions_note` = "no penalized learner ran;
tree learners used the raw controls, no interaction basis constructed",
`n_features_after_interactions = 30` (= raw). Paper §6 (lines 611-623)
matches. The false "300 engineered features" claim is gone.

### E4 [C16/R2a] Variational CI convention — VERIFIED
- `cddf_one_split` / `run_cddf` default `alpha = 0.05` (`recast_dml.py:658, 767`);
  per-split bounds use `conf_int(alpha=alpha)` (lines 703-704, 726), and
  `run_cddf` medians those bounds (lines 785-791). The notebook explicitly passes
  `alpha=0.05` (cell `0aeb6f09`). Per-split 95% bounds medianed ⇒ coverage
  ≥ 1−2α = 90%, the CDDF variational guarantee, matching B&N's "90% CIs".
- JSON: every learner block has `"alpha": 0.05`;
  `hte_results.cddf.ci_convention` = "90% adjusted (median of per-split 95%
  bounds; CDDF variational, coverage >= 90%); p-values doubled". CIs widened as
  predicted (β₂ [−0.287, 0.639] → [−0.310, 0.695]); homogeneity non-rejection
  unchanged. p-value doubling preserved (`min(1.0, 2*median)`, lines 787-793).

### No-tuning / blinding confirmation
- β₂ still divergent at 0.1996 (gap −0.4514 ≈ 2.19 benchmark-SEs); the fix moved
  it 2 cents toward but nowhere near the benchmark, and the verdict label is
  unchanged.
- All 13 numeric gap-table differences recompute from `hte_results.json` /
  `replication_results.json` + `benchmark_results.json` (β₂ gap and ITT gap
  re-verified to 4 dp).
- Blinding intact: notebook never reads `benchmark_results.json`; `gap_table.json`
  records the SHA-256 freeze of `dml_results.json` and the orchestrator-recomputed
  gap. The B1 fix is justified by the spec's pre-registered `_blocks_note`
  (design fidelity), so it is blinding-safe.

### Deferred items (acknowledged, none conclusion-affecting)
S1 proxy-NN capacity sensitivity, S2 CLAN clustering caveat, stratum-specific
propensities, per-split β₂ draw persistence — all documented in the changelog as
framework follow-ups. None changes a reported conclusion (all heterogeneity
inference remains null; CLAN directions unaffected). Consistent with the round-1
suggestion grading.

### Verdict
All round-1 fixes verified against the executed code and frozen artifacts; the
revision introduced no new problem; the central divergence was sharpened, not
chased. The single blocking issue (B1) is cleared. **Accept.**
