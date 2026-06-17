# Final Review Report

**Paper:** Does Teacher Training Actually Work? Evidence from a Large-Scale Randomized Evaluation of a National Teacher Training Program
**Original authors:** Loyalka, Popova, Li & Shi (*American Economic Journal: Applied Economics*, 2019)
**Benchmark for the heterogeneity branch:** Baiardi & Naghi (2024), generic-ML re-analysis of one arm contrast
**Rounds completed:** 2 of 3
**Final verdict:** Ready

---

## What This RECAST Contributes

This is the Phase-2 generalization test on a binary-treatment RCT, and that framing is the whole point. The earlier regression-test paper (Nunn-Trefler, continuous treatment) had no published generic-ML target to aim at; here the heterogeneity branch finally has a real external benchmark — Baiardi & Naghi's (B&N) generic-ML analysis of the same teacher-training experiment — so the pipeline can be tested on the question it was actually built to answer: does an independent, blinded implementation of the Chernozhukov-Demirer-Duflo-Fernández-Val (CDDF) generic-ML protocol reproduce a published heterogeneity result?

The answer is a genuinely informative split. The ATE null reproduces (IRM ATE indistinguishable from zero under flexible nuisances, matching the published null). The *rank-dependent* outputs reproduce: CLAN gets 9 of 10 most/least-affected directions right, and GATES reproduces the qualitative quintile shape. But the *scale-dependent* headline — the BLP β₂ heterogeneity slope — diverges hard: B&N report β₂ = 0.651 (p = 0.0003); this RECAST gets 0.200 (p = 0.56). That is not a near-miss, it is a different conclusion about whether detectable treatment-effect heterogeneity exists at all. The value of the RECAST is that it isolates *where* generic-ML inference is robust (sorting/direction) and where it is implementation-sensitive (the magnitude and significance of the heterogeneity slope), on a real published case.

**"Would I be pleased to have written this, flaws and all?"**
Yes. The divergence is reported as the finding rather than buried or explained away, the one specification change most likely to have been a bug on our side (the blockZ omission) was hunted down and ruled out, and the paper refuses to claim either that it refuted B&N or that it confirmed homogeneity — which is the honest reading of the power situation.

---

## Replication Summary

The replication regime is **stochastic** — the original Loyalka replication package is not on disk, the analysis sample is B&N's prepared file, and there are no deterministic printed-precision targets. Specification fidelity (carrying the conditioning set variable-for-variable) is therefore the only replication check available, which is precisely why the round-1 blockZ issue mattered.

| Specification | Published / Benchmark | Replicated (ours) | Delta | Status |
|--------------|-----------|-----------|-----------|--------|
| OLS ITT (clustered) | 0.002, CI90 [-0.068, 0.072] (B&N) | 0.0018 (SE 0.0298), n=9,676 | -0.0002 | PASS (consistent, both null) |

**Overall:** The single benchmarkable replication cell (the ITT point estimate) lands within noise of the benchmark; both are null. Tier verdict is **PARTIAL** with the gate **PASS**, correctly reflecting that "PARTIAL" here means "no deterministic target existed," not "a target was missed."

---

## DML Extension Summary

The DML extension has two parts: an IRM ATE (the confirmatory extension) and the CDDF generic-ML heterogeneity protocol (the benchmarked part). The headline is the BLP β₂ comparison.

| Quantity | Benchmark (B&N) | Ours (NeuralNet, best) | Verdict |
|--------|------|------|------|
| BLP β₁ (level) | 0.002, p=1.0 | 0.0082, CI90 [-0.119, 0.141], p=0.91 | consistent |
| **BLP β₂ (heterogeneity slope)** | **0.651, CI90 [0.312, 0.99], p=0.0003** | **0.200, CI90 [-0.310, 0.695], p=0.56** | **divergent** |
| GATES quintile shape | bottom<0, top>0, middle null (qualitative) | -0.053, +0.033, +0.039, +0.043, +0.044; 0/5 significant | shape-consistent, significance NOT reproduced |
| CLAN directions | — | 9/10 directions match | consistent (1 flip: student baseline math) |

IRM ATE (extension, no per-learner benchmark): Forest -0.0068 (0.0452); Boosting -0.0827 (0.0851). Both null.

**Key finding:** The central heterogeneity magnitude diverges, and — critically — this survived restoring the pre-registered county strata (see Review Process below). β₂ moved only 0.178 → 0.200 when the strata were put back, i.e. ~2 cents, well inside one benchmark-implied SE (~0.21) and nowhere near 0.651. So the gap is not the blockZ bug; it is a real signal about how sensitive the generic-ML heterogeneity slope is to implementation choices (proxy capacity, school-level vs. student-level splitting, and B&N's own unverifiable code). The 90%-adjusted CI [-0.310, 0.695] still overlaps most of B&N's [0.312, 0.99], so the paper correctly declines to claim refutation — it has neither detected heterogeneity nor proven it absent.

---

## Review Process Summary

Round 1 was a **Major revision**: the synthesis carried **1 blocking issue, 4 essential items, and 8 suggestions**. The blocking issue (B1) was caught by the DML-technical referee, not the general referee — exactly the kind of design-fidelity break a specialist audit is for.

| Issue | Round | Category | Resolved? | How |
|-------|-------|----------|-----------|-----|
| B1: blockZ randomization strata omitted from every covariate set (OLS, IRM nuisances, generic-ML proxies, BLP/GATES controls) — contradicted the spec's `fixed_effects: ["blockZ"]` | 1 | **Blocking** | Yes | Fixed in the *generic builder + shared library* (not a one-off notebook edit), then the stage-4→6 cascade was re-run. `n_features_raw` 24→30; strata now in every covariate set. Verified against executed code in round 2. |
| E1: n_rep=20 on IRM side (vs B&N's 100) | 1 | Essential | Yes | Disclosed, pre-registered deviation; Boosting MC-dispersion qualifier added. Benchmarked CDDF quantity kept the full 100 splits. |
| E2: propensity diagnostics — trimmed share unreported, log-loss mislabeled "RMSE", worse-than-constant fit undisclosed | 1 | Essential | Yes | Library now logs `propensity_diag` and `nuisance_loss_metric`; m̂ ranges and zero trimmed share reported; column relabeled log-loss. |
| E3: `interactions_used: true` / "300 engineered features" contradicted the executed code | 1 | Essential | Yes | Now `false` with a note; the interaction basis is correctly reserved for penalized learners, none of which ran. |
| E4: variational CIs mislabeled — per-split 90% bounds medianed and called "90% CIs" (actually 80% coverage) | 1 | Essential | Yes | Re-run with per-split alpha=0.05 → genuine 90%-adjusted CIs matching B&N's convention. CIs widened; homogeneity non-rejection unchanged. |
| S1: estimand-statement provenance wording ("from original code" under a no-code port; selection-on-observables phrasing for an RCT) | 1 | Suggestion | Yes | Reworded to "documented specification (original code not on disk)" and "unconfoundedness holds by randomization (stratified)." |
| S6/S7/S8: gap-table second layer, β₁-coincidence note, CLAN median-arithmetic note, truncated IRM strings | 1 | Suggestion | Yes (partial on S6) | Second-layer implementation note added to BLP rows; β₁ and median-difference notes added; truncated strings fixed. Per-split β₂ draw persistence deferred. |
| S3/S4/S5: proxy-NN capacity sensitivity, CLAN clustering caveat, stratum-specific propensities | 1 | Suggestion | Deferred | Documented as framework follow-ups; none changes a conclusion. |

**Round 2** was a verification pass: **both referees Accept.** All five round-1 fixes (B1 + E1–E4) were verified against the executed code and frozen artifacts, not just the prose. Blinding was re-checked after the re-run — the SHA-256 of the new `dml_results.json` (`c6d1b7660c2c57be`) matches both the gap table's recorded freeze and the paper's title footnote, confirming the gap table was genuinely recomputed by the orchestrator after the results were frozen. No new contradiction was introduced.

The most important outcome: restoring the strata moved β₂ by ~0.02 and the gap persisted, so **candidate explanation (c) (blockZ omission as the cause of the divergence) was eliminated.** The bug that *was* present (blockZ omission) was caught and fixed and did *not* explain the gap; the divergence is honest, not an artifact.

---

## Remaining Items

No essential issues remain. The paper is ready to share. The suggestions below would strengthen it further but are optional.

| # | Item | Category | Action needed |
|---|------|----------|---------------|
| 1 | Proxy NeuralNet capacity: (20,) hidden units at aux-half N≈4,800; the capacity rule suggests (100,). A wider-proxy sensitivity speaks directly to the attenuation candidate. | Suggestion | Optional sensitivity run; would tighten the "implementation-sensitivity" claim. |
| 2 | CLAN uses unclustered Welch t-tests; for teacher-level moderators the effective N is ~schools, so "every CLAN difference is significant" overstates precision (B&N practice is also unclustered). | Suggestion | One-sentence caveat; direction verdicts unaffected. |
| 3 | Stratum-specific known propensities and stratum-aware school splits (CDDF practice in stratified RCTs). | Suggestion | Optional refinement; current propensity now correctly computed on the estimation sample (0.5131). |
| 4 | `propensity_diag.known_propensity_entropy` is `null` in the JSON; the 0.693 entropy comparison lives only in the paper prose. | Suggestion | Cosmetic artifact-completeness fix. |
| 5 | Persist per-split β₂ draws so the MC-implementation layer of the gap-table verdict is fully recomputable for the generic-ML rows. | Suggestion | Framework follow-up. |

---

## Notes for the Reader

- **What the RECAST does to the original finding:** it *confirms* the published ATE null under flexible nuisances and *qualifies* the heterogeneity story. It does not overturn anything in Loyalka et al.; rather, it raises a methodological flag about reproducing B&N's generic-ML heterogeneity claim. Read the β₂ divergence as a statement about generic-ML implementation sensitivity, not as evidence that B&N are wrong — the paper is careful about this and so should the reader be.

- **Honest limitations to carry if you share this:** (i) B&N's teacher-training generic-ML code is not in their replication package, so the benchmark side is unverifiable — this is stamped on the gap-table rows and is the single biggest reason the divergence cannot be fully adjudicated; (ii) the replication regime is stochastic with no deterministic target, so "PARTIAL/PASS" is the correct and honest tier, not a failed match; (iii) the learner menu was bounded by compute (Forest + Boosting on the IRM side; the full CDDF protocol used the canonical proxies), and n_rep=20 on the unbenchmarked IRM rows is a disclosed, pre-registered deviation.

- **What the automated pipeline cannot verify:** the benchmark numbers themselves (B&N's code is off-disk), the original Loyalka 4-arm labeling (reconstructed from B&N's design description), and whether the residual β₂ gap is driven by proxy capacity, the school-level splitting design choice, or B&N's implementation — these are the open scientific questions, not pipeline defects.

- **Suggested manual checks before treating this as finished:** run suggestion #1 (wider proxy NN) if you want to pin down the attenuation channel, and add the one-sentence CLAN clustering caveat (#2). Neither changes a conclusion; both would pre-empt a real referee's first two questions.

- **Bottom line:** this is a clean generalization test. The pipeline caught its own most dangerous bug (a silent spec-fidelity break on the headline benchmarked quantity), fixed it in the shared library so it can't recur, re-ran honestly, and the headline finding survived. The divergence is the contribution, and it is well-evidenced.
