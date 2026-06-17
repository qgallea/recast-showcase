## Synthesis Report — Round 1

**Unified verdict:** Major revision

(G returned "Minor revision"; T returned "Major revision." The unified verdict
follows the more severe, because T raised a BLOCKING issue — B1 requires a
stage-4 cascade re-run, which by definition cannot be a minor revision. T is the
referee with blocking authority, so its severity governs the cascade.)

### Contribution consensus

Both referees endorse the contribution. G's assessment is clearly positive
("Pleased-to-have-produced test: yes, flaws and all"): a blinded, independently
implemented head-to-head of the CDDF generic-ML protocol against Baiardi & Naghi
(2024) on the same frozen sample, a design-faithful school-level-splitting
variant for a cluster-randomized trial, and an IRM ATE extension confirming the
published null — with the headline β₂ divergence (0.178, p = 0.581 vs benchmark
0.651, p = 0.0003) framed as an informative implementation-sensitivity finding
rather than benchmark-chasing. T's benchmark-alignment assessment agrees the
implementation is "close to the CDDF/B&N canon on most dimensions" (canonical
aux-split proxies, school-level splits, known RCT propensity, weighted CDDF
BLP/GATES with cluster-robust SEs, variational aggregation, Λ-criteria best
learner matching the benchmark NN, IRM carrying `cluster_cols="schid"`). T flags
**two material deviations** — the blockZ strata omission (B1, blocking) and the
variational CI coverage mislabel (E4). The panel believes this RECAST adds value;
the bar for blocking is therefore appropriately high, and only the one
citation-backed design-fidelity break clears it.

### Essential issues (must be addressed — paper cannot stand as-is)

| # | Issue | Raised by | Scientific justification | Action |
|---|-------|-----------|-------------------------|--------|
| E1 | n_rep = 20 on the IRM side (vs B&N `ite <- 100`; skill C3 floor 100, 20–99 graded essential). Disclosed, pre-registered deviation; disclosure judged acceptable. | T (C3) | Affected rows are unbenchmarked, both confirm a null, and the B&N-adjusted SE charges for cross-split variation. One honesty nuance: "MC noise is small" holds for Forest (mc_sd/SE ≈ 0.45) but is strained for Boosting (≈ 0.69). | Add one sentence qualifying the Boosting MC dispersion. Since B1 forces a stage-4 re-run anyway, lift n_rep to 100 if the per-cell budget allows; otherwise the disclosed n_rep = 20 justification stands. No standalone re-run demanded. |
| E2 | Propensity diagnostics: trimmed share unreported; `ml_m` log-loss stored/labeled as "RMSE"; worse-than-constant propensity fit (Forest 0.779, Boosting 0.884 > entropy 0.693) undisclosed. | T (C9 + R2b) | The IRM score divides by m̂(1−m̂); a worse-than-chance, overfit propensity is exactly where trimming bites — the reader needs the trimmed share (or m̂ range) to trust the ATE rows. The mislabel makes the propensity column uninterpretable (0.88 "RMSE" on a binary outcome is absurd; as log-loss it is merely poor). | In the B1 re-run, log trimmed share (or min/max of m̂) per learner into `dml_results.json`; relabel the `ml_m` entry as log-loss in Table 5 notes; add one sentence noting the propensity learners underperform the known constant (and that the known-propensity option exists in an RCT). Prose + logging only; both nulls insensitive. |
| E3 | `interactions_used: true` / "300 engineered features" contradicts executed code — Forest/Boosting fit on the raw 24 controls; Lasso (the only learner that expands interactions) never ran. | T (C1/C14) | The methodology description of the headline DML extension is factually wrong about its feature set. No estimate changes (tree/boosting need no interaction basis — C1's exception), but a replicator following the paper builds the wrong design matrix. | Correct the JSON metadata (condition `interactions_used` on a penalized learner actually running) and the §6 sentence to "on the 24 inherited controls (the interaction basis is reserved for penalized learners, none of which ran)." |
| E4 | Variational CI mislabel: medians of per-split **90%** bounds reported as "90% CIs," but the CDDF guarantee makes the median of per-split (1−α) bounds only **1−2α = 80%** coverage. | T (C16/R2a) | All BLP/GATES intervals (Tables 2–3, gap table) are too narrow for the labeled coverage, and the headline interval comparison (ours [−0.287, 0.639] vs benchmark [0.312, 0.99]) mixes conventions. Correcting *widens* our CIs, so the non-rejection of homogeneity is unchanged — hence essential, not blocking — but the cross-implementation comparison must be like-for-like. | In the B1 re-run, pass per-split alpha = 0.05 and label the medianed bounds as the 90% adjusted CIs (matching the benchmark's per-split-95% → 90% convention); or, at minimum, relabel current intervals as 80%-coverage with a gap-table note. |

### Suggestions (would improve but are optional)

| # | Issue | Raised by | Action |
|---|-------|-----------|--------|
| S1 | Estimand-statement provenance + RCT-identification wording. (a) "inherited variable-for-variable from the original code" contradicts the declared **port** regime ("no original code on disk"); controls actually come from B&N's variable-description PDF, some added by B&N beyond the original Loyalka set. (b) "the original paper's selection-on-observables claim" mischaracterizes an RCT — conditional exogeneity holds by randomization. | **G (Suggestion 1) + T (Suggestion 4)** — *deduplicated*; both edit the same estimand-statement provenance/identification sentence | Reword to "variable-for-variable from the documented B&N specification" and replace the selection-on-observables phrasing with "guaranteed by randomization (stratified by county)." Note: with B1 forcing the estimand statement to be touched anyway (the "from the original code" claim is also inaccurate re: strata FEs — see B1), fold this wording fix into that edit. |
| S2 | One informative sensitivity check: re-run the generic-ML protocol for the selected NeuralNet learner only, with blockZ one-hot added to the proxy covariate set, labeled as a disclosed post-hoc sensitivity (motivated by the spec's `_blocks_note`, not the benchmark). The single most informative check on candidate (c). | G (Suggestion 2) | Optional. Partially subsumed by B1, which already restores blockZ to all covariate sets in the full re-run; this learner-restricted variant becomes redundant if B1 is executed in full. If compute is tight and B1 is done only minimally, this is the bounded-cost fallback. |
| S3 | Proxy NN capacity sensitivity: CDDF NeuralNet proxy uses (20,) hidden units at aux-half N ≈ 4,800; the capacity rule indicates (100,) at N ≥ 500. A wider-proxy sensitivity speaks directly to attenuation candidate (d). | T (Suggestion 1) | Optional sensitivity, justified by the capacity rule (not the benchmark gap). |
| S4 | CLAN clustering caveat: CLAN uses unclustered Welch t-tests; for teacher-level variables (constant within school) the effective N is ~schools, so "every CLAN difference is statistically significant" (§5.4) overstates precision. CDDF/B&N practice is also unclustered. | T (Suggestion 2) | Add a one-sentence caveat; direction verdicts unaffected. |
| S5 | Propensity refinements: p is the full-sample student treated share (0.5130) while estimation uses the complete-case sample (n = 9,676); design propensity is school-level (101/201 ≈ 0.5025), stratified by county. | T (Suggestion 3) | In the re-run, compute p on the estimation sample; consider stratum-specific known propensities and stratum-aware school splits (CDDF practice in stratified RCTs). |
| S6 | Render the two-layer gap-table verdict label. Rows carry only the materiality layer; the spec's benchmark-mode format calls for two (materiality + MC-implementation flag). The second layer would mostly read "benchmark implementation unverifiable (no B&N code on disk)" — worth stamping on the β₂ row. Also fix the truncated benchmark strings in the two IRM rows ("…our IRM ATE ro"). | **G (Suggestion 3) + T (Suggestion 5)** — *deduplicated*; both ask to render the second/MC-implementation layer of the gap-table verdict | Persist per-split β₂ draws (analogous to `dml_reps.parquet`) so the `stochastic_agreement` MC-implementation layer is recomputable for the generic-ML rows; render both layers; fix the malformed IRM benchmark strings. |
| S7 | Confirm the β₁ benchmark cell: the gap table's BLP-β₁ benchmark (0.002, CI90 [−0.068, 0.072], p = 1.0) is digit-for-digit identical to the OLS benchmark row. | G (Suggestion 4) | If B&N's BLP β₁ genuinely coincides with their OLS estimate, say so in a table note; if the orchestrator reused the OLS row as a β₁ proxy, label it as such. |
| S8 | Note the median-aggregation arithmetic in Table 5: the CLAN "Diff." column is the median-over-splits difference, which need not equal the difference of median group means (e.g., `female`: −0.080 vs −0.084 implied; both correct per `hte_results.json`). | G (Suggestion 5) | Add a one-line table note to pre-empt the appearance of an arithmetic error. |

### Blocking issues (require re-running a notebook)

| # | Issue | Raised by | Canonical citation | Notebook to fix | Specific action |
|---|-------|-----------|--------------------|-----------------|-----------------|
| B1 | **blockZ randomization-strata fixed effects omitted from every estimation covariate set, contradicting the spec.** Spec `paper_spec.json` line 49 declares `"fixed_effects": ["blockZ"]` and the `_blocks_note` (line 59) pre-registers blockZ as "a valid stratification control (entered as fixed effects / one-hot in nuisances)," but it entered neither the generic-ML proxies, nor the BLP/GATES control set X1 = [1, B], nor the IRM nuisances (`dml_results.json` `n_features_raw: 24`; notebook cell 23 passes only the 24 `controls` to `rd.run_cddf`, cell 7 only `controls` to `rd.doubleml_model`). The paper itself flags this as candidate explanation (c) — the deviation was discovered, not chosen. | **G (essential) + T (BLOCKING)** — *deduplicated; same edit fixes both, kept BLOCKING per T's authority + canonical citation* | CDDF 2018 (Chernozhukov et al., NBER WP 24678, §3) — strata conditioning in stratified-RCT applications; estimand statement / spec §2.3 variable-for-variable inheritance; `paper_spec.json` `_blocks_note`. | Notebook 04 (stage 4 → 6 cascade) | Append one-hot blockZ dummies (6 strata) to the covariate list passed to both `rd.run_cddf` (cell 23) and `rd.doubleml_model` (cell 7), and include them in the BLP/GATES X1 controls; re-run the stage-4→6 cascade and regenerate the gap table. Keep the school-level splits (design-faithful; candidate (b) needs no fix). Blinding-safe: justified by the spec's `_blocks_note`, written at stage 1 before the gap table existed — design fidelity, not tuning. **Direction note (from G):** with county-stratified randomization the strata are balanced by design, so the null-ATE point estimate is not at risk — this is a precision/specification-fidelity fix on the headline benchmarked β₂, not a threat to the ATE conclusion. |

*Why B1 is blocking and E4 is not, though both are CI/specification matters: B1
changes the **inputs** to the estimators (the covariate matrices), so the point
estimates and the gap table must be recomputed — code, not prose. E4 is a
relabeling/coverage-convention fix that, while ideally re-run with alpha = 0.05,
can in the limit be addressed by relabeling existing output; it does not by
itself change which conclusion holds. E1–E3 are likewise prose/logging fixes that
ride along on the B1 re-run rather than requiring it.*

### Downgraded items

None. Every "essential"-marked item carried a scientific argument tied to a
specific checklist criterion (G's lone essential = B1, which carried a direction
argument and a fidelity argument; T's E1–E4 each cite a C-criterion with a
mechanism). No essential was found to be a suggestion in disguise. G did **not**
attempt to mark anything blocking, so no G→essential downgrade of a blocking
claim was needed.

### Proportionality check

Borderline-high but within tolerance. Final counts: **1 blocking, 4 essential
(E1–E4; B1 is counted under blocking, not double-counted), 8 suggestions** — 13
total items. Two dedup merges (B1: G+T; S1: G+T; S6: G+T) already collapsed the
raw count. The skill's signal-jamming trip is 8+ essentials from one referee or
10+ total looking like over-refereeing; here T raised 4 essentials + 1 blocking,
each with a distinct C-criterion and a stated mechanism (attenuation, score
division by m̂(1−m̂), wrong design matrix, coverage arithmetic), so this is a
thorough audit rather than padding. The blocking count (1) and essential count
(4) sit at the high end of the "0–2 blocking / 0–3 essential" guideline; the
extra essential (4 vs 3) is justified because each is a genuinely separable code
or reporting defect on the headline DML extension, not a restatement. No
downgrade warranted on proportionality grounds.

### Referee disagreements

No substantive disagreement. The only divergence is in overall verdict label
(G: minor revision; T: major revision), which resolves cleanly in T's favor
because T holds blocking authority and B1 forces a cascade re-run. On the one
issue both raised (blockZ), they agree on substance and direction; they differ
only on severity tier (G: essential; T: blocking), and the skill resolves this
in T's favor (only T blocks; T supplied the canonical citation and the >20%
plausible-movement argument on the headline benchmarked β₂). G's framing that the
null ATE is not at risk is fully compatible with T's blocking call — both are
preserved in the B1 row.

### Already resolved (suppressed from this round)

None. This is round 1; no prior changelogs exist.

RERUN_NEEDED: yes
