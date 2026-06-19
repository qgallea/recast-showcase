## Synthesis Report — Round 1

**Unified verdict:** Minor revision

### Contribution consensus
Both referees endorse the contribution. G calls it "a clean, well-scoped worked example of the replication gate" — the published Table 5 triple difference reproduces within reasonable deviation (origination 0.0816 vs 0.080, application 0.0803 vs 0.082, NonRep×post anchor −1.9604 vs −1.966), the gate PASSes as PARTIAL with per-coefficient explanations, and the continuous-intensity treatment is correctly routed to `DID_PLR`. T's benchmark-alignment assessment agrees the routing is canonical ("the correct canonical analogue of a TWFE DiD for a continuous treatment") and explicitly confirms RECAST does NOT misuse `DoubleMLDIDMulti` or generic-ML GATES, and that clustering is carried through end-to-end (C19 PASS). T flags two real deviations from the strictest B&N recipe (`n_rep=1`; penalized learner sees only 5 raw controls) but states neither is sign/significance/magnitude-changing and **declines to BLOCK on any item**. The panel verdict is therefore positive with prose-level fixes — the bar for blocking is correctly not met.

### Essential issues (must be addressed — paper cannot stand as-is)
| # | Issue | Raised by | Scientific justification | Action |
|---|-------|-----------|-------------------------|--------|
| 1 | **GATE "groups are statistically distinguishable" overclaims** | G (essential), T (R2d) | Verified against `hte_results.json`: tercile effects 0.0202 / 0.0108 / 0.0269 are non-monotonic with heavily overlapping joint CIs; only T3 excludes zero. The library `distinguishable` flag is `bool(any(joint_ci_excludes_zero))` — a "≥1 group nonzero" test, NOT a between-group separation test. The prose presents it as between-group separation on the very dimension that is the DML analogue of the paper's central triple-difference mechanism. Misleading as written; violates the small-n honesty rule. | Reword the heterogeneity prose to: the exposure×post effect is jointly significant only in the highest-NonRep tercile (T3); the three tercile point estimates are non-monotonic with overlapping joint CIs, so the terciles are not statistically distinguishable from one another. Rename the JSON field to `any_group_significant` so the name stops implying separation. |
| 2 | **Continuous-D estimand wording omits the variance-weighting caveat** | T (C17) | For a continuous treatment, the PLR coefficient is a conditional-variance(of D)-weighted average derivative, not a clean ATE / "average partial effect" (spec L6). A reader could over-read it as an unweighted ATE. | Add one clause to `estimand_statement.md` noting the PLR coefficient is a conditional-variance-weighted average derivative of the continuous exposure intensity, not an equally-weighted ATE. |
| 3 | **First-stage nuisance fit not surfaced or interpreted** | T (R2b) | `nuisance_loss` (RMSE only) is present in `dml_results.json` but absent from the report, with no R² and no interpretive sentence. A reader cannot judge first-stage fit quality, which is part of honest DML reporting. | Surface per-learner nuisance RMSE in the report with one interpretive sentence — note that ml_m RMSE being large relative to ml_l means exposure×post is hard to predict from the 5 controls, which is reassuring for identification. |

### Suggestions (would improve but are optional)
| # | Issue | Raised by | Action |
|---|-------|-----------|--------|
| 1 | Lasso path uses no pairwise-interaction basis (C1) | T | Not blocking (Lasso 0.0207 ≈ Forest/Boosting). Expand interactions or disclose the penalized learner uses k=5 main effects only. |
| 2 | No BCH/RLasso penalty (C2) | T | Add a one-line methodology disclosure (CV-Lasso, not BCH). |
| 3 | n_rep = 1 (single cross-fitting split) (C3) | T | Not blocking. Raise n_rep or add a "single split; results stable across learners" caveat. |
| 4 | Library versions unpinned (C18) | T | Log library versions alongside the results JSONs. |
| 5 | n-gap magnitude under-foregrounded in headline | G | Add one clause noting the sample is materially larger (8174 vs 7335) and deliberately un-gated. |
| 6 | State the robustness-range source | G | Cite where the 0.080–0.090 alternative-sample estimates live or soften to "expected to be robust." |
| 7 | Lead heterogeneity with the cleaner CATE | G | The CATE spline (+0.013…+0.038, monotone in NonRep) supports the mechanism more cleanly than the noisier tercile GATE. |
| 8 | State cluster count + report learner agreement | T | Show n_ids=842 next to the clustered-SE claim; report the four-learner spread (0.014–0.022) as a robustness signal. |

### Blocking issues (require re-running a notebook)
*None.* The technical referee — the only referee with BLOCKING authority — explicitly declined to block on every item, stating that sign, significance, and magnitude do not move and that no re-run is required for any fix. All essential items are prose/disclosure edits.

### Downgraded items
- **C1 (Lasso interactions), C2 (BCH lasso), C3 (n_rep=1):** T marked these "ESSENTIAL." Downgraded to **suggestions** — T itself states each is NOT blocking, the result does not move (four learners agree, TWFE anchor present), and the prescribed fix in each case is "one sentence of disclosure / no re-run needed." They improve transparency but the paper is neither misleading nor uninterpretable without them.
- **C18 (version pinning):** Downgraded to **suggestion** — a reproducibility-logging improvement, not a fix without which the paper misleads or cannot be read.
- **Signal-jamming note:** T produced 7 "essential" items; a well-functioning review carries 0–3. After validating each against the essential bar, 3 survive (GATE overclaim, estimand wording, nuisance fit) — all with concrete scientific arguments — and 4 are reclassified as suggestions.

### Referee disagreements
None of substance. G and T independently converge on the single most important item (the GATE "distinguishable" overclaim) and reach the same overall verdict (Minor revision).

### Already resolved (suppressed from this round)
None — this is Round 1 with no prior changelogs.

RERUN_NEEDED: no
