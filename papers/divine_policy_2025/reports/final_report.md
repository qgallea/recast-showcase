# Final Review Report

**Paper:** Divine Policy: The Impact of Religion in Government
**Original authors:** Bentzen, J. S., Pizzigolotto, A. & Sperling, L. L. (American Economic Journal: Applied Economics, 2025)
**Rounds completed:** 1 of 3
**Final verdict:** Ready

---

## What This RECAST Contributes

This RECAST demonstrates the DiD pathway end-to-end on a 2025 staggered difference-in-differences study, and it does the hard, honest part well: when the paper's headline religiosity/attitudes outcomes turned out to rest on restricted GSS microdata that is not shipped in the package, the pipeline did not fudge them — it re-scoped to the paper's *reproducible* mechanism (the log count of faith-based nonprofits, built from the included NCCS panel and Sager faith-based-law timing) and re-estimated it with cross-fitted DML. The most valuable engineering here is the routing-plus-fallback discipline: a staggered binary panel DiD is correctly sent to Callaway–Sant'Anna (DoubleMLDIDMulti), that estimator is genuinely infeasible at this N (50 states, 6 never-treated, single-state cohorts, empty per-(g,t) nuisance cells), and the pipeline degrades gracefully to the canonical DML two-way-FE fallback (`DoubleMLPLR`, partialling-out, clustered on `fipsstat`), flagged loudly everywhere with the exact CS2021 staggered-heterogeneity caveat. The substantive payoff: three structurally different learners (Forest +0.0391, Lasso +0.0358, Boosting +0.0414, all p < 0.025) and the non-stochastic parametric TWFE anchor (+0.0377, SE 0.0162) all coincide, and all are directionally consistent with the published positive nonprofit effect (+2,258 organizations).

**"Would I be pleased to have written this, flaws and all?"**
Yes — it is a faithful, transparently-scoped demonstration whose every number traces to a results JSON, whose fallback and partial-replication limits are disclosed rather than hidden, and whose claims are proportionate to a small-N design.

---

## Replication Summary

| Specification | Published | Replicated | Delta (%) | Status |
|--------------|-----------|-----------|-----------|--------|
| Faith-based-NPO count effect (two-way-FE DiD; treated × post) | + and significant (+2,258 orgs, back-of-envelope; stacked event-study, manuscript p.4) | +0.0377 log points (SE 0.0162, t 2.33, CI [0.006, 0.069]) | directional only (no numeric target) | PASS (consistent) |

**Overall:** 1/1 reproducible spec within scope, tier = PARTIAL / gate = PASS. The comparison is **directional** (same sign + individually significant), not a numeric match — the original is a Stata stacked event-study reporting a level (+2,258 orgs), while this RECAST runs a simplified static DiD on the log count reconstructed in Python. Two genuine, well-documented restrictions drive the PARTIAL tier: (a) the paper's headline religiosity/conservative-attitudes outcomes use restricted GSS microdata (GSS7218_R3.dta) that is not shipped, and (b) the original stacked build is in Stata, which is unavailable here.

---

## DML Extension Summary

| Method | Coef | SE | 95% CI | p-value |
|--------|------|----|--------|---------|
| TWFE DiD (parametric anchor) | +0.0377 | 0.0162 | [0.006, 0.069] | t = 2.33 |
| DML – Forest | +0.0391 | 0.0154 | [0.0089, 0.0693] | 0.011 |
| DML – Lasso (CV-Lasso) | +0.0358 | 0.0158 | [0.0049, 0.0667] | 0.023 |
| DML – Boosting | +0.0414 | 0.0171 | [0.0080, 0.0749] | 0.015 |

**Key finding:** Replacing the linear size control (`log_npo`) with flexible ML nuisances barely moves the estimate — the three learners span +0.0358 to +0.0414 (spread < 16%), all individually significant, all landing essentially on top of the non-stochastic TWFE anchor. The value-add is first-stage robustness, not a new estimand: the DML rows target the *same* `_post_treated` TWFE DiD as the replication, only with the single size control partialled out by ML. Heterogeneity (the natural CS group/time/event-study decomposition) is honestly reported as *unavailable* — the fallback strips the group-time cells — rather than fabricated (`heterogeneity_detected: null`, `exploratory: true`).

---

## Review Process Summary

| Issue | Raised (round) | Category | Resolved? | How |
|-------|---------------|----------|-----------|-----|
| C3 — single cross-fitting repetition (n_rep = 1) makes the B&N median-SE adjustment vacuous | 1 (T) | Essential (not blocking) | Yes | "Method & inference notes" bullet added to `estimand_statement.md`: states the DiD pathway runs a single split (n_rep=1, n_folds=3), so `bn_se_median` equals the analytic SE and the B&N machinery is inactive; inference is DoubleML's analytic SE clustered by state |
| S1 — `log_npo` is a partial-denominator / bad-control risk | 1 (G) | Suggestion | Addressed | "Control caveat" added to `estimand_statement.md`: frames this as a within-sector composition/share effect; notes attenuation biases toward zero, so the control cannot manufacture the positive sign |
| S2 / C8 — K-folds = 3 below the K ≥ 5 norm | 1 (T) | Suggestion | Deferred | Kept at K=3 to preserve published point estimates; DML SEs are cross-fit-consistent for any K ≥ 2, no expected effect on the conclusion |
| S3 / C18 — no library-version record | 1 (T) | Suggestion | Deferred | Auditability hygiene only; low-cost polish |
| S4 / C2 — CV-Lasso vs BCH disclosure | 1 (T) | Suggestion | Deferred (noted) | One-feature nuisance; immaterial to inference |
| S5 — state the directional-benchmark rule in the report | 1 (G) | Suggestion | Addressed | The gap-table note already explains the directional (sign + significance) comparison |
| S6 — mark DML rows as exploratory | 1 (G) | Suggestion | Addressed | DML rows carry `original: "-"` / `benchmark: "-"`; HTE artifact carries `exploratory: true` |
| S7 — clarify DML and parametric estimates target the identical estimand | 1 (T) | Suggestion | Deferred | Low-cost note; the staggered-TWFE caveat already frames the DML number as an approximate average ATT |

The single round was a **Minor revision** with **no blocking issues**. The only essential (C3) was raised by the DML-technical referee — the sole referee with blocking authority — who explicitly marked it ESSENTIAL but NOT blocking and stated that prose disclosure alone satisfies it, because the canonical fix (n_rep ≥ 100) would not plausibly move sign, significance, or magnitude > 20% given the tight agreement across learners and the non-stochastic anchor. That disclosure is now present and accurate.

---

## Remaining Items

| # | Item | Category | Action needed |
|---|------|----------|---------------|
| 1 | K-folds = 3 (vs K ≥ 5 norm) | Suggestion | Optional: rerun with `n_folds = 5` (N=1050 / 50 clusters supports it) — no expected effect on the conclusion |
| 2 | No library-version record (doubleml / sklearn / linearmodels) | Suggestion | Optional: pin versions alongside the results JSON for auditability |
| 3 | CV-Lasso (not BCH) used for penalized nuisance | Suggestion | Optional: one-line methodology note; immaterial for a one-feature nuisance |
| 4 | n_rep = 1 (single split) | Suggestion | Optional: rerun with `n_rep ≥ 100` to activate the B&N median-SE machinery — already disclosed as inactive, so this is polish, not a fix |

No essential issues remain. The paper is ready to share. The suggestions above would strengthen it further but are optional.

---

## Notes for the Reader

- **The RECAST qualifies-and-confirms, not overturns.** The reproducible mechanism (more faith-based nonprofits after a state adopts a faith-based-initiative law) holds with the same sign and significance under both the parametric anchor and three ML learners. The headline religiosity/attitudes results are *not* tested here — they depend on restricted GSS microdata — so this is a confirmation of the nonprofit channel only.
- **Interpret the DML number as an approximate average ATT, not the Callaway–Sant'Anna group-time estimate.** Under staggered timing with treatment-effect heterogeneity, two-way-FE DiD is exactly what CS2021 corrects; that caveat is carried consistently across the estimand statement, the gap-table note, and the results JSONs. The fallback was forced by genuine infeasibility (small cross-section, too few never-treated units, empty (g,t) cells), not chosen for convenience.
- **The benchmark comparison is directional by design.** "Consistent" means same sign and individually significant — not a numeric match — because the original reports a level effect from a Stata stacked event-study and this RECAST reports a log-points effect from a Python static DiD. A reader should not read the four "consistent" rows as a quantitative replication of +2,258 organizations.
- **One honest caveat to keep in mind when sharing:** the sole inherited control, `log_npo` (count of *all* nonprofits, of which faith-based orgs are a subset), makes this a within-sector composition/share effect. If FBI adoption also raised total nonprofit counts, `log_npo` is partly post-treatment and would attenuate the estimate toward zero — which means it cannot manufacture the positive sign, but the framing is worth stating plainly. A cheap one-line sensitivity (estimate without the control) would close the loop if anyone questions it.
- **What the pipeline cannot verify:** the provenance and construction of the NCCS faith-based-org classification, whether the Python panel reconstruction exactly matches the authors' Stata stacked build, and the theory linking faith-based-initiative laws to nonprofit formation. These are manual checks for anyone treating this as more than a methods demonstration. The small-N design (50 states) is a real limitation but a proportionate one, not a fatal flaw — and it is disclosed everywhere it matters.
