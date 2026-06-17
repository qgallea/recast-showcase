# Synthesis Report — Round 1 (Djankov taxes, control-discipline test)

**Unified verdict:** Minor revision → all items resolved in a same-round
prose/label pass (no re-run, no blocking).

## Contribution consensus
Both referees agree the run is sound: 3/3 exact OLS replication of the
all-controls kitchen-sink spec; a benchmark-faithful B&N DML port (17/21
consistent); and the distinctive control-discipline contribution (6/12
controls DAG-flagged, inherited set kept as headline, documented sensitivity
reported). General referee: Accept. Technical referee: Minor revision (3
essentials, 0 blocking).

## Quality control of the technical referee's 3 essentials (verified on disk)

| Item | Disposition | Evidence |
|---|---|---|
| E1 [R2e] "4 tension labels not reproducible; only Nnet qualifies" | **Labels CORRECT per rule; clarity added** | Verified: 3 of the 4 tensions are **significance-category flips** (gap < 1 SE_bench but the 5% significance verdict differs — e.g. five-year Lasso ours −0.193/0.085 significant vs B&N −0.178/0.096 not), which `stochastic_agreement`'s `qual_agree` layer labels tension by design; Nnet is the one genuine gap-tension (0.105, 1–2 SE). The referee applied only the gap layer and missed `qual_agree`. The labels stand; the report now explains the significance-flip mechanism explicitly (paper §DML rows). |
| E2 [C16] "sensitivity SE mislabeled (0.083 package, not 0.089 B&N-adj); n_rep=50 undisclosed" | **Fixed** | Confirmed: the suspect-controls sensitivity used n_rep=50 and the row showed the package SE 0.083. Corrected to the B&N-adjusted SE 0.089 in `gap_table.json` and `paper.tex` (both the gap table and the control-discipline table), with `n_rep=50` disclosed. |
| E3 [C2] "CV-Lasso not BCH/RLasso" | **Already resolved** | The methodology already discloses CV-Lasso vs RLasso; retained. |

### Essential issues
None remain after the prose/label pass.

### Suggestions (carried)
General referee's 3 + technical's 4 (proxy/learner notes, additional-panel
scope, etc.) — non-binding; logged for the framework backlog.

### Referee disagreement
General Accept vs Technical Minor revision, resolved: E2 was a genuine
(minor) fix now applied; E1 was a misread of the materiality rule (labels
verified correct, clarity added); E3 already addressed. Net verdict: **Ready**.

RERUN_NEEDED: no
