# Revision changelog — Round 1

Synthesis verdict: **Minor revision** (3 essential, 0 blocking). The DML-technical referee — the only referee with blocking authority — explicitly declined to block on every item, so all fixes are prose/disclosure plus one genuine library-flag correction. No code re-run was *required*; `build_project.py` was re-executed only to regenerate the artifacts with the corrected flag and the new disclosures (point estimates unchanged — same seed, same n_rep).

## Essential issues — all addressed

1. **[E1] GATE "groups are statistically distinguishable" over-claim (G + T/R2d).** *Genuine bug, fixed.*
   - `lib/recast_dml.py::_gate_record`: renamed the misleading `distinguishable` field → `any_group_significant`, and added `n_significant` / `n_groups`. The flag is now correctly documented as "≥1 group's joint CI excludes 0 — NOT a between-group separation test."
   - `website/tools/build_pages.py::_gate_blocks`: rewrote the GATE prose. It now reads `joint_ci_excludes_zero` and reports "individually significant (\*) in N of M subgroups; `gate()` does not test between-group differences and the point estimates overlap, so the subgroups are **not** shown to differ from one another (exploratory, underpowered)." For NonRep this renders as "significant in 1 of 3 subgroups."
   - Regenerated `hte_results.json` (now carries `any_group_significant`/`n_significant`/`n_groups`).

2. **[E2] Continuous-D estimand wording (T/C17).** Added to `estimand_statement.md`: "Because the treatment is a CONTINUOUS intensity, the PLR coefficient is a conditional-variance(of the treatment)-weighted average derivative, not an equally-weighted ATE."

3. **[E3] First-stage nuisance fit not surfaced (T/R2b).** Added a "Method & inference notes" bullet to `estimand_statement.md` reporting the per-learner out-of-fold nuisance RMSE (ml_l outcome vs ml_m treatment) with the interpretation that the treatment is much harder to predict than the outcome — reassuring for identification.

## Suggestions addressed (cheap, in the same Method & inference note)
- **C3 / n_rep=1:** disclosed the DiD pathway runs a single cross-fitting split, so the B&N median-SE adjustment is inactive; results are stable across all four learners (0.014–0.022) and sit on the parametric TWFE anchor (0.0193).
- **C2 / CV-Lasso:** disclosed the penalized learner uses CV-Lasso (valid DML inference, not the BCH post-selection guarantee).
- **Cluster count + learner agreement:** the note states 842 county clusters and the four-learner spread.

## Suggestions deferred (optional, non-binding)
- **C1** (expand the pairwise-interaction basis for Lasso inside the DID_PLR path): would change shared library behavior; disclosed via the CV-Lasso/main-effects note instead. Lasso (0.0207) already agrees with Forest/Boosting, so no material effect.
- **C18** (pin library versions in the artifacts): reproducibility-logging hygiene; deferred.
- **n-gap headline clause / robustness-range source / lead-with-CATE:** the n-gap is already documented in `replication_check.json` and the estimand statement; both GATE and CATE are shown.

RERUN_NEEDED: no
