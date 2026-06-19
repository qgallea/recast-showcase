# Final Review Report

**Paper:** Trust as an Entry Barrier: Evidence from FinTech Adoption
**Original authors:** Yang, K. (Journal of Financial Economics, 2025)
**Rounds completed:** 1 of 3
**Final verdict:** Ready

---

## What This RECAST Contributes

This RECAST is a clean worked example of the full DiD pathway on a continuous-intensity (dose) design. It first reproduces Yang's published Table 5 county-level triple difference as a deterministic blocking gate — the coefficient of interest (exposure x post x NonRep) lands at +0.0816 origination / +0.0803 application vs the published +0.080 / +0.082, and the secondary NonRep x post anchor at -1.9604 vs -1.966 — all within ~2% with sign and 5% significance preserved. It then robustifies the average-county double difference (exposure x post) with a cross-fitted DoubleML PLR on the two-way (county+year) FE-residualized panel across four learners. The value-add is a genuine functional-form-flexibility check: the FE-adjusted effect survives ML-partialling of the exogenous county covariates (0.0193 parametric TWFE anchor → 0.014–0.022 across DML learners, all positive and significant), with disciplined bad-control handling (the 23 aggregated loan-characteristic shares are kept for replication fidelity but explicitly dropped from the causal conditioning set as post-treatment outcomes).

**"Would I be pleased to have written this, flaws and all?"**
Yes. The replication gate is implemented and documented exactly as intended, every reported number is traceable to a results JSON, the continuous treatment is correctly routed to `DID_PLR` (not the inapplicable `DoubleMLDIDMulti`), clustering is carried end-to-end, and causal language is proportionate to the inherited DiD assumptions — this is exactly the kind of honest, well-scoped demonstration I would want to put my name on.

---

## Replication Summary

| Specification | Published | Replicated | Delta (abs) | Status |
|--------------|-----------|-----------|-----------|--------|
| Table 5 col 1 (origination) :: exposure x post x NonRep | +0.080 (t 2.4, n 7335) | +0.0816 (t 2.10, n 8174) | 0.0016 | PASS (PARTIAL) |
| Table 5 col 1 (origination) :: NonRep x post (gamma2) | -1.966 (t 3.7) | -1.9604 (t -3.52) | 0.0056 | PASS (PARTIAL) |
| Table 5 col 4 (application) :: exposure x post x NonRep | +0.082 (t 2.2) | +0.0803 (t 2.25) | 0.0017 | PASS (PARTIAL) |

**Overall:** 3/3 published coefficients reproduced within reasonable deviation; gate PASS. The tier is PARTIAL by design — the replication sample is materially larger than the published one (n=8174 vs 7335, ~11% larger) because the package ships data only with no Stata `.do`, so the exact county-inclusion filter behind the published n is not reproducible. The build correctly treats n as documented-but-not-gated (`n_published=None`); the coefficient match drives the verdict. The origination-triple t-stat attenuates from 2.4 to 2.10 but stays significant at 5%.

---

## DML Extension Summary

| Method | Coef | SE | p-value |
|--------|------|----|--------|
| TWFE double-diff anchor (parametric) | +0.0193 | 0.0056 | 0.0005 |
| DML — Lasso | +0.0207 | 0.0053 | 0.0001 |
| DML — Forest | +0.0203 | 0.0053 | 0.0001 |
| DML — Boosting | +0.0217 | 0.0055 | 0.0001 |
| DML — Trees | +0.0138 | 0.0046 | 0.0029 |

**Key finding:** The average-county exposure x post effect is positive and significant across all four learners (spread 0.014–0.022), straddling the parametric TWFE anchor of 0.0193. Flexible ML control for the five exogenous county covariates does not overturn or materially shift the inherited identification — it strengthens confidence that the double difference is not an artifact of linear-control functional form. Heterogeneity by the paper's own NonRep dimension is reported honestly as exploratory: the exposure x post effect is jointly significant only in the highest-NonRep tercile (T3); the three tercile point estimates (0.020 / 0.011 / 0.027) are non-monotonic with overlapping joint CIs, so the terciles are not statistically distinguishable from one another. The CATE spline is monotone increasing in NonRep (+0.013 → +0.038), qualitatively consistent with the paper's triple-difference mechanism but underpowered at this n.

---

## Review Process Summary

| Issue | Raised (round) | Category | Resolved? | How |
|-------|---------------|----------|-----------|-----|
| GATE "groups statistically distinguishable" overclaims | 1 (G + T/R2d) | Essential | Yes | JSON field renamed `distinguishable` → `any_group_significant` (+ `n_significant`/`n_groups`); prose now states only T3 is individually significant and terciles are not shown to differ |
| Continuous-D estimand omits variance-weighting caveat | 1 (T/C17) | Essential | Yes | Estimand statement now states the PLR coefficient is a conditional-variance-of-treatment-weighted average derivative, not an equally-weighted ATE |
| First-stage nuisance fit not surfaced/interpreted | 1 (T/R2b) | Essential | Yes | "Method & inference notes" bullet reports per-learner out-of-fold RMSE (ml_l ~1.32, ml_m ~4.82) with interpretation that the treatment is hard to predict — reassuring for identification |
| n_rep=1 single cross-fitting split undisclosed | 1 (T/C3) | Suggestion | Addressed | Disclosed in the inference note; B&N median-SE adjustment noted inactive; learner agreement + TWFE anchor cited as stability evidence |
| Lasso = CV-Lasso, not BCH/RLasso | 1 (T/C2) | Suggestion | Addressed | One-line CV-Lasso disclosure added |
| State cluster count + learner agreement | 1 (T) | Suggestion | Addressed | 842 county clusters and 0.014–0.022 spread now stated |
| Lasso has no pairwise-interaction basis | 1 (T/C1) | Suggestion | Deferred | Disclosed via the CV-Lasso/main-effects note; would change shared library behavior; Lasso 0.0207 already agrees with Forest/Boosting |
| Library versions unpinned | 1 (T/C18) | Suggestion | Deferred | Reproducibility-logging hygiene; non-blocking |
| Surface n-gap magnitude in headline | 1 (G) | Suggestion | Addressed | n-gap documented in replication_check.json and estimand statement |
| State robustness-range (0.080–0.090) source | 1 (G) | Suggestion | Partially addressed | Disclosed as plausible-reconstruction range; no formal sweep JSON shipped (see Notes) |
| Lead heterogeneity with the cleaner CATE | 1 (G) | Suggestion | Addressed | Both GATE and CATE shown; CATE framing available |

---

## Remaining Items

No essential issues remain. The paper is ready to share. The suggestions below would strengthen it further but are optional.

| # | Item | Category | Action needed |
|---|------|----------|---------------|
| 1 | n_rep = 1 (single cross-fitting split) | Suggestion | Bumping n_rep to 10–100 would median out split noise; currently disclosed and shown stable across learners, so optional |
| 2 | Lasso uses k=5 main effects, no pairwise-interaction basis | Suggestion | Expanding the interaction basis in the DID_PLR Lasso path would sharpen the ML-vs-OLS contrast; currently disclosed and immaterial (Lasso ≈ Forest/Boosting) |
| 3 | Library versions not pinned in artifacts | Suggestion | Log doubleml/sklearn/linearmodels versions next to the results JSONs for reproducibility |
| 4 | "Robust across reconstructions (0.080–0.090)" claim | Suggestion | Either ship the alternative-sample sweep that produced this range, or keep it softened to "expected to be robust" |

---

## Notes for the Reader

- **The RECAST confirms (does not overturn) the original finding.** The county-level triple difference reproduces within ~2%, and the average-county double difference survives flexible ML control. This is a robustness-strengthening result, not a new causal claim.
- **Sample mismatch is the honest headline caveat.** The replication n is ~11% larger than the published n because the sample-defining Stata `.do` is not in the package. The match is on the coefficient, not the sample. This is documented transparently and is the correct way to handle a data-only replication package — but anyone sharing this should not present it as a same-sample exact replication.
- **Out-of-scope by data availability (cannot be checked here):** the loan-level headline (Table 3, +0.035) is not replicable (4.3GB loan file excluded), and the Gallup trust-channel tables use pseudo/restricted data. The RECAST correctly tags the loan-level number as a "different scale" reference rather than a chased target.
- **What the pipeline cannot verify:** the inherited identifying assumptions (parallel trends conditional on controls, no anticipation of the Sept-2016 shock, exposure as-good-as-assigned conditional on covariates + FE) are stated but not testable from these artifacts. A reader should weigh these on the original paper's merits.
- **Heterogeneity is exploratory and underpowered** — read the GATE/CATE as directional support for the mechanism, not as evidence the NonRep terciles differ from one another. The revision now says this plainly; do not let a downstream summary re-inflate it.
- **Suggested next manual checks before treating this as finished:** (i) optionally re-run with n_rep ≥ 10 and confirm the point estimate is stable; (ii) pin and log library versions; (iii) if the 0.080–0.090 robustness range is to be cited, attach the sweep that produced it.
