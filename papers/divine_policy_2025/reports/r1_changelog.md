# Revision changelog — Round 1

Synthesis verdict: **Minor revision** (1 essential, 0 blocking). The DML-technical referee — the only referee with blocking authority — marked its sole essential (C3 / n_rep=1) ESSENTIAL but explicitly NOT blocking, and stated prose disclosure satisfies it. All fixes are disclosure edits; `build_project.py` was re-executed only to regenerate the estimand statement (point estimates unchanged — same seed, n_rep, n_folds).

## Essential issue — addressed

1. **[E1] Single cross-fitting repetition (n_rep = 1) (T/C3).** Added a "Method & inference notes" bullet to `estimand_statement.md`: the DML fallback runs a single split (n_rep=1, n_folds=3), so the B&N median-SE adjustment is inactive (`bn_se_median` equals the analytic SE); inference is DoubleML's analytic SE clustered by state. The estimate is stable — three structurally different learners coincide (+0.036 to +0.041, all p<0.025) and land on the parametric TWFE anchor (+0.038) — so single-split noise is immaterial.

## Suggestions addressed
- **S1 / `log_npo` bad-control risk (G):** added a "Control caveat" to `estimand_statement.md` — conditioning on `log_npo` (count of ALL nonprofits) makes this a within-sector composition/share effect; if FBI adoption raised total counts, `log_npo` is partly post-treatment and would attenuate the estimate toward zero, so it cannot manufacture the positive sign.

## Suggestions deferred (optional, non-binding)
- **S2 / C8** (raise n_folds 3→5): kept at 3 to preserve the published point estimates; DML SEs are cross-fit-consistent for any K≥2 and the referee notes no expected effect on the conclusion.
- **S3 / C18** (version pinning), **S4 / C2** (CV-Lasso disclosure — noted here), **S5** (directional-benchmark rule — the gap-table note already explains the directional comparison), **S6** (mark DML rows exploratory — they carry `original:"-"`/`benchmark:"-"`), **S7** (same-estimand note): low-cost polish, deferred.

RERUN_NEEDED: no
