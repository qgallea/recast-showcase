# Final Review Report — Ashraf & Galor (2013), IV-path test

**Paper:** The Out of Africa Hypothesis, Human Genetic Diversity, and
Comparative Economic Development
**Original authors:** Ashraf, Q. & Galor, O. (American Economic Review, 2013)
**Role in Phase 2:** generalization test of the **IV / PLIV** path.
**Rounds completed:** 1 (Accept after synthesis QC).
**Final verdict:** Ready (with one optional disclosure).

---

## What this RECAST contributes

It exercises the pipeline's instrumental-variables path for the first time,
on a deliberately hard case: a **quadratic, hump-shaped** structural model
(genetic diversity has an interior-optimum effect on development) identified
by a **generated instrument** (Wooldridge two-step on migratory distance from
East Africa). The replication reproduces the published Table 2 (col 5) result
**exactly**: adiv 285.19 (published 285.190), adiv_sqr −206.576 (exact), and
the optimal-diversity turning point **0.690 vs 0.690**. The adiv row is graded
PARTIAL only because its robust SE differs by 0.001 (the last printed digit)
in the generated-instrument reconstruction — substantively a perfect
replication.

**"Flaws and all, would I be pleased to have produced this?"** Yes — and
specifically because the extension is *honest about what it cannot do*.

## The key methodological result

The estimand router sends IV→PLIV, but single-treatment **linear PLIV cannot
represent a hump**. The pipeline recognized this: it raised a
`functional_form_warning`, ran the linearized PLIV as an explicitly-labeled
exploratory slope (Forest +7.39, p=0.23; Lasso +9.18, p=0.04), and stated
plainly that these are **not comparable** to the quadratic coefficients and
do **not** estimate "the effect of diversity." Producing a single linear IV
slope and passing it off as the AG effect would have been the failure mode;
the pipeline avoided it.

## Review process

The general referee recommended Accept (0 essential). The DML-technical
referee returned Major revision with 4 essentials — but synthesis QC found 3
were **factual misreads**: it claimed paper.tex, dml_results.json,
hte_results.json, and gap_table.json were missing (all verified present on
disk, 433/96/5/47 lines) and that "1 of 3 treatments ran" (AG has one
treatment, quadratic, by design). Root cause: the technical-referee skill
assumed the standard notebook + multi-treatment layout and could not see this
paper's bespoke `run_ag.py` script. The skill has been hardened to list
`code_run/` and verify absence before flagging. The one legitimate point
(disclose CV-Lasso vs RLasso) is recorded as a suggestion.

## Remaining items
| # | Item | Category | Action |
|---|---|---|---|
| 1 | Methodology should disclose the penalized learner is CV-Lasso, not BCH-RLasso | Suggestion | Optional one-line note |

No essential issues remain.

## Notes for the reader
- The headline replication (the hump + turning point) is exact; trust it.
- The DML extension is **functional-form-limited by construction** — linear
  PLIV is the wrong tool for a hump-shaped effect. This is a genuine boundary
  of the current pipeline, not a data problem: faithfully extending AG would
  need a nonlinear-IV or dose-response estimand the framework does not yet
  implement.
- n = 21 (the limited HGDP-CEPH sample): DML cross-fitting asymptotics are
  unreliable at this size — a second reason the PLIV number is exploratory.
- Generated-instrument IV required per-paper replication code; the generic
  OLS-only stage 3 does not cover it. Logged as a framework follow-up.
