# General Referee Report

**Round:** 2 (verification pass)
**Overall verdict:** Accept

### Scope of this pass

Round 2 is a verification pass under the implicit bargain (Berk, Harvey &
Hirshleifer 2017): I verify the round-1 fixes against the artifacts and check
that the revision introduced no new contradiction. I raise no new essential
issue for anything visible in round 1. My round-1 verdict was Minor revision
with one essential item (blockZ strata inheritance) plus five suggestions.

### Verification of the round-1 essential item (blockZ inheritance) — RESOLVED

The single essential item is fully reconciled across every artifact, not just
in prose:

1. **OLS replication.** `replication_results.json` / `replication_check.json`
   now record `fixed_effects_included = [blockZ_18, 19, 27, 28, 29]` (5
   dummies, drop-first), `replicated_coef = 0.0018078`, `replicated_se =
   0.029820`. Table 1 prints 0.0018 (0.0298) and lists the strata row. Match.
2. **IRM nuisances.** `dml_results.json` `n_features_raw = 30` (was 24);
   `n_features_after_interactions = 30`. Table 7 and Section 6 state 30
   covariates = 24 controls + 6 blockZ levels. Match.
3. **Generic-ML proxy / BLP / GATES sets.** `hte_results.json`
   `covariates_include_fixed_effects = [blockZ_17,18,19,27,28,29]` (all 6
   one-hot). Section 5.1 lists exactly these 6. Match.
4. **Estimand statement.** Now reads "30 controls ... including 6 one-hot
   fixed-effect levels for ['blockZ']"; the spec's `fixed_effects:
   ["blockZ"]` and `_blocks_note` ("entered as fixed effects / one-hot in
   nuisances") are now honored everywhere. The round-1 tension between the
   "variable-for-variable inheritance" claim and a silently dropped
   spec-declared element is gone: the conditioning set is genuinely complete.

The OLS-vs-nuisance dummy-count difference (5 drop-first in OLS, 6 one-hot in
the tree/penalized nuisances) is correct and is stated correctly in both
places — it is not a contradiction.

### Verification: estimand-statement provenance wording (round-1 Suggestion 1)

`estimand_statement.md` now reads "variable-for-variable from the documented
specification (original code not on disk)" and "unconfoundedness holds by
randomization (stratified)." The port declaration is honored; the prior
internal contradiction (claiming inheritance "from the original code" under a
no-code port regime) is removed. Section 4 embeds the statement verbatim and
flags the S1 correction. Resolved.

### Verification: divergence framing now that candidate (c) is eliminated — HONEST

This is the crux of the round, and it is handled exactly as the implicit
bargain would hope. The re-run with strata restored moved
`hte_results.cddf.NeuralNet.blp.beta2` to 0.199556 (CI [-0.3095, 0.6948], p =
0.5599) — the gap table β₂ row (0.1996, [-0.310, 0.695], p = 0.5599) and the
abstract/Sections 5.2, 5.5, and the Conclusion all trace to this. The paper
states the change was 0.178 → 0.200 (Δ = 0.022, "well inside one standard
error and nowhere near the benchmark's 0.651") and concludes candidate (c) is
**eliminated, not confirmed.** Section 5.5 now carries only candidates (a),
(b), (d); (c) is explicitly dropped. The framing is anti-benchmark-chasing:
the gap *survives* the one change most likely to have been a coding error on
RECAST's side, and all remaining candidates are argued to make the RECAST test
more conservative (school-level splits, noisier proxy attenuation,
unverifiable benchmark code) rather than the benchmark invalid. The
power-honesty paragraph still declines both detection and refutation. This is
a sharpened, more defensible version of the round-1 finding.

### Verification: blinding integrity post-rerun

The blinding chain was re-verified after the re-run, not carried stale: I
recomputed SHA-256 of the current `dml_results.json` = `c6d1b7660c2c57be`,
which matches both `gap_table.json.dml_results_sha256_prefix` and the paper's
title footnote. So the gap table was genuinely recomputed by the orchestrator
against the new strata-included frozen results.

### Other round-1 items spot-checked (all consistent)

- E4 CI relabel: `ci_convention` = "90% adjusted (median of per-split 95%
  bounds; CDDF variational, coverage >= 90%)"; all BLP/GATES tables labeled
  90% CDDF-adjusted. Consistent.
- E2 propensity diagnostics: `dml_results` records `propensity_diag` (Forest
  m̂∈[0.022,0.974], Boosting m̂∈[0.010,0.984], trimmed share 0.0) and
  `nuisance_loss_metric.ml_m = logloss`; Table 7 note relabels the column and
  notes the learners underperform the constant p≈0.513. Consistent.
- E3 `interactions_used = false` with `interactions_note`; Section 6 matches.
- E1 n_rep=20 disclosure with the Boosting MC-dispersion qualifier present.
- S6 gap-table second layer present on both BLP rows; IRM benchmark strings
  no longer truncated. S7 β₁-coincidence note and S8 median-difference note
  present; the `female` example (medianed diff -0.0702 vs median-means
  difference -0.0637) matches `hte_results.json`. Verdict counts (11/1/1/1/2)
  reconcile with the 16 rows.

### Revision-introduced problems

None found. Number traceability remains intact after regeneration: the OLS,
β₁/β₂, GATES gammas and G5−G1 contrast, all 10 NeuralNet CLAN cells, the IRM
ATE rows, and the diagnostics all match their JSON sources on re-check. No
new internal contradiction was introduced by the strata re-run; the
direction-of-bias and "more conservative" arguments are unchanged and still
correct.

### Comments

The revision did the right thing in the right place: the fix was made in the
generator/shared library (so blockZ inheritance cannot be lost on
regeneration) and the stage-4→6 cascade was honestly re-run, with the β₂ gap
*persisting* and reported as such. The most valuable outcome of round 1 is
exactly this: the one specification change that could most plausibly have been
a RECAST-side error was tested and ruled out, so the implementation-sensitivity
finding is now better evidenced than it was. My round-1 essential item is
resolved, the wording suggestion is resolved, and the divergence framing is
trustworthy as written. I recommend Accept.
