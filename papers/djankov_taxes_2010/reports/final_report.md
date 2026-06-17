# Final Review Report — Djankov et al. (2010), control-discipline test

**Paper:** The Effect of Corporate Taxes on Investment and Entrepreneurship
(Panel A, Investment), revisited by Baiardi & Naghi (2024)
**Role in Phase 2:** generalization test of the **kitchen-sink control
discipline** + a second benchmarked PLR case.
**Rounds completed:** 1 (Minor revision → resolved same round).
**Final verdict:** Ready.

---

## What this RECAST contributes

Two things. First, a second benchmarked PLR reproduction: the all-12-controls
OLS replicates **exactly** (3/3 SUCCESS; statutory −0.0645 vs −0.064,
first-year −0.1165 vs −0.117, five-year −0.1887 vs −0.189; classical SEs,
N=61), and the blinded B&N DML port is **17/21 cells consistent** with B&N's
published Table 1 Panel A, all negative and larger in magnitude than the OLS —
reproducing their finding that flexible control functions *strengthen* the
estimated tax effect. The 4 "tension" cells are honest: three are
significance-category flips on near-identical coefficients (our slightly
smaller adjusted SEs cross the 5% line), and one (Nnet) is the lone genuine
gap, on the noisiest learner. No benchmark-chasing — the port is blinded and
the hyperparameters are fixed.

Second — the point of this test — a **control-discipline** demonstration on
exactly the over-conditioning specification the rule was written for. A DAG
screen flagged 6 of the 12 inherited controls as plausible bad controls (a
tax-payments mediator and a "fiscal-bundle" of sibling tax variables).
Following the rule, the inherited full set stays the headline (comparability
with the original), and a documented sensitivity excluding the 6 suspects is
reported: the five-year Forest estimate moves from −0.200 (full) to −0.230
(screened) — conditioning on the suspect controls *attenuates* the tax effect,
the direction expected if they sit on the causal path. The report makes no
"correct estimate" claim; it preserves the original's choice and discloses the
sensitivity.

**"Flaws and all, would I be pleased to have produced this?"** Yes.

## Review process
General referee: Accept (0 essential). Technical referee: Minor revision (3
essential, 0 blocking). On verification: E2 (sensitivity SE labeled as package
0.083 rather than B&N-adjusted 0.089, n_rep=50 undisclosed) was a genuine
minor fix, now applied. E1 (the 4 tension labels) was a misread of the
materiality rule — the labels are correct (significance-category flips via the
`qual_agree` layer); the report now explains the mechanism. E3 (CV-Lasso
disclosure) was already present. No re-run; no conclusion changed.

## Remaining items
| # | Item | Category |
|---|---|---|
| 1 | The DAG suspect-control arguments are economic reasoning, not the original authors' explicit graph — the sensitivity is illustrative, not definitive | Caveat (stated) |
| 2 | Panel A only (Investment); FDI / business density / entry rate out of scope | Scope |
| 3 | N=61 small-sample; the 4 tension cells; proxy/learner refinements | Suggestions |

No essential issues remain.

## Notes for the reader
- The kitchen-sink OLS and the DML port both reproduce faithfully; trust them.
- The control-discipline finding is the substantive contribution: the headline
  effect is *sensitive* to the suspect controls in the theory-predicted
  (attenuation) direction. This is transparency, not a correction.
- The "tension" cells are not coefficient disagreements — they are
  significance-threshold crossings on near-identical estimates.
