# Changelog — Round 1 (Djankov taxes)

Round-1 verdict: Minor revision (1 general Accept + 3 technical essentials, 0
blocking). All addressed in a same-round prose/label pass; no re-run.

### Essential issues addressed
- **E2 [C16] sensitivity SE convention + n_rep disclosure.** Resolved.
  - `data/results/gap_table.json`: the control-discipline sensitivity row now
    reports the B&N-adjusted SE (0.089) instead of the package SE (0.083), and
    discloses `n_rep=50`.
  - `paper/paper.tex` + `paper/tables/table_replication.tex`: the screened-set
    row updated to $-0.230$ (0.089) with `n_rep=50` noted, consistent with the
    B&N-adjusted convention used for the headline rows.
- **E1 [R2e] tension-label explanation.** Resolved (labels verified correct).
  Synthesis QC confirmed the 4 tension labels are correct per
  `stochastic_agreement`: 3 are significance-category flips (sub-0.04 gaps but
  the 5% verdict differs), 1 (Nnet) a genuine gap-tension. Added a paragraph to
  `paper.tex` §"DML rows" explaining the significance-flip mechanism, and a
  `tension_note` to `gap_table.json`. No numbers changed.
- **E3 [C2] CV-Lasso disclosure.** Already present in the methodology; retained.

### Suggestions
General (3) + technical (4) suggestions logged as non-binding framework
backlog items; none affects a conclusion.

RERUN_NEEDED: no
