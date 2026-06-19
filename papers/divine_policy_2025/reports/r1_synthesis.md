## Synthesis Report — Round 1

**Unified verdict:** Minor revision

### Contribution consensus
Both referees agree this RECAST adds value. G judges the replication "faithfully scoped" — it reproduces the paper's *reproducible* mechanism (count of faith-based nonprofits from the included NCCS panel) after the headline religiosity outcomes proved unrecoverable from unshipped restricted GSS microdata, re-estimates with cross-fitted DML, and discloses its fallback honestly (passes the pleased-to-have-produced test). T confirms the benchmark alignment is correct: a staggered binary panel DiD is routed to rule 2.1-8a (DoubleMLDIDMulti / Callaway–Sant'Anna), that estimator is genuinely infeasible at N=50 states / 6 never-treated / single-state cohorts, and the pipeline degrades to the canonical DML-TWFE fallback (`DoubleMLPLR`, `partialling out`, clustered on `fipsstat`), flagged loudly everywhere with the CS2021 caveat. **No deviation rises to a sign / significance / magnitude(>20%) threat:** three structurally different learners (+0.0358 / +0.0391 / +0.0414, all p<0.025) and the non-stochastic TWFE anchor (+0.0377, SE 0.0162) all coincide and are directionally consistent with the published +2,258-organization finding. T raises no BLOCKING issue.

### Essential issues (must be addressed — paper cannot stand as-is)
| # | Issue | Raised by | Scientific justification | Action |
|---|-------|-----------|-------------------------|--------|
| E1 | **[C3] Single cross-fitting repetition (n_rep = 1)** | T | Valid and canonical: B&N `dml_tariffs_T2.R` sets `ite <- 100`; the median-θ / median-SE aggregation requires many repetitions to average out cross-fit split randomness, and at n_rep=1 `bn_se_median == se` — the B&N adjustment is vacuous. T itself states this is **NOT conclusion-threatening** (three learners coincide, spread <16%, non-stochastic TWFE anchor lands on top, low-variance nuisance). Kept ESSENTIAL because the report should not leave the reader believing the B&N median-SE machinery is active when it is inactive. | Either (a) rerun the DiD_PLR fallback with `n_rep ≥ 100`, OR (b) add a sentence in the report/methodology stating the DiD pathway runs a single split and the B&N median-SE adjustment is therefore inactive. Prose disclosure alone satisfies E1 — it is **not** blocking. |

### Suggestions (would improve but are optional)
| # | Issue | Raised by | Action |
|---|-------|-----------|--------|
| S1 | **`log_npo` is a partial denominator / bad-control risk** — conditioning `log_fb` on log count of *all* nonprofits reframes the estimand toward a within-sector composition/share effect; if FBI adoption raised total NPO counts, `log_npo` is partly post-treatment and could attenuate. | G | Add one sentence to the estimand statement clarifying this is a within-sector composition effect. Attenuation biases *toward* zero, so it cannot manufacture the positive sign — non-binding. |
| S2 | **[C8] K-folds = 3 below the K≥5 norm** | T | Raise `n_folds` from 3 to 5; N=1050 with 50 clusters comfortably supports K=5. DML SEs cross-fit-consistent for any K≥2 — no expected effect on the conclusion. |
| S3 | **[C18] No library-version record** | T | Record doubleml / sklearn / linearmodels versions alongside the results JSON. |
| S4 | **[C2] CV-Lasso vs BCH disclosure** | T | Note in methodology that the penalized-learner nuisance uses CV-Lasso, which has valid DML inference but not BCH post-selection guarantees. One-feature nuisance, immaterial. |
| S5 | **State the directional-benchmark rule in the report** | G | Add a one-line note that "consistent" = same sign and individually significant (not a numeric match). |
| S6 | **Mark the headline DML numbers as exploratory** | G | Add a small "exploratory" flag on the three DML rows (which carry `original: "-"` / `benchmark: "-"`). |
| S7 | **Clarify DML and parametric estimates target the identical estimand** | T | One-line note that the DML "extension" rows are the same `_post_treated` TWFE DiD as the replication, only with ML nuisances partialling out the single size control — the value-add is first-stage robustness, not a new estimand. |

### Blocking issues (require re-running a notebook)
*None. T — the only referee empowered to block — explicitly marked its sole essential issue (E1 / C3) as ESSENTIAL but NOT BLOCKING, with a documented argument that the canonical fix (n_rep≥100) would not plausibly move sign, significance, or magnitude >20%. No code re-run is required for the result to stand.*

### Downgraded items
- **[C8] K-folds = 3 → suggestion (S2).** T's checklist labeled C8 "ESSENTIAL (minor)" but in the same line stated "DML SEs cross-fit-consistent for any K≥2; immaterial here → suggestion." No scientific argument that the paper is uninterpretable or misleading at K=3.
- **[C18] Version pinning → suggestion (S3).** Missing version metadata is an auditability/reproducibility hygiene gap, not a defect that makes the present result uninterpretable or misleading.

### Referee disagreements
None. G and T independently reach "Minor revision." G finds no essential issues; T finds one essential (non-blocking). The total list (1 essential, 0 blocking, 7 suggestions) is proportionate and shows no over-refereeing.

### Already resolved (suppressed from this round)
None — this is Round 1; there are no prior changelogs.

RERUN_NEEDED: no
