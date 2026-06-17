# Synthesis Report — Round 1 (Ashraf–Galor, IV path)

**Unified verdict:** Accept (with one disclosure suggestion).

## Contribution consensus
Both referees agree the IV-path replication is sound: the quadratic 2SLS with
the reconstructed Wooldridge generated instrument reproduces the published
hump coefficients (adiv 285.19, adiv_sqr −206.576) and the optimal-diversity
turning point (0.690) **exactly**, and the report honestly frames the
linearized PLIV extension (+7.4 / +9.2) as NOT comparable to the hump. The
general referee passed the pleased-test and recommends Accept.

## Quality control of the referee reports (synthesis's primary job)

The DML-technical referee returned "Major revision" with 4 essentials, **3 of
which are factual errors** that I verified against the filesystem and have
DOWNGRADED:

| Tech-referee essential | Verdict | Evidence |
|---|---|---|
| E1 "only 1 of 3 treatments ran; no dml_results.json/hte_results.json; no code_run/04" | **Downgraded — false** | `dml_results.json` (96 lines) and `hte_results.json` exist; the executed code is `code_run/run_ag.py` (143 lines), not `04_dml_extension.ipynb`; AG has **one** treatment (genetic diversity, entered quadratically) **by design**, not three. |
| E3 "paper.tex and DML table absent — prose checks unverifiable" | **Downgraded — false** | `paper/paper.tex` exists (433 lines) and the general referee read it without difficulty. |
| E4 "gap_table.json not produced" | **Downgraded — false** | `data/results/gap_table.json` exists (47 lines). |
| E2 "[C2] disclose CV-Lasso (not BCH/RLasso) in methodology" | **Kept as SUGGESTION** | Legitimate: the lib's penalized learner is `LassoCV`, not `hdm::rlasso`. Worth a one-line methodology disclosure, but not essential — it does not invalidate any estimate. |

**Root cause (recorded as a Phase-2.5 finding):** the DML-technical referee
skill assumed the standard notebook + multi-treatment project structure and
hardcoded `code_run/04_dml_extension.ipynb`; faced with this paper's bespoke
single-treatment `run_ag.py` (which the generated-instrument IV required), it
misread the layout as missing/truncated output rather than verifying. The
skill has been hardened (list `code_run/` first; verify absence before
flagging; count treatments from the JSON) so this false-positive class does
not recur.

### Essential issues
None remain after verification.

### Suggestions
1. **[C2]** Disclose in the methodology that the penalized learner is CV-Lasso
   (sklearn `LassoCV`), not the BCH-penalty RLasso (`hdm::rlasso`); note the
   theoretical-guarantee difference. *(general referee's 2 suggestions —
   minor wording — also fold in here.)*

### Referee disagreement
General = Accept; Technical = Major revision. Disagreement resolved in the
general referee's favor after disk verification showed the technical
referee's blocking-class items were factual misreads. Net verdict: **Accept**;
the single legitimate item is a non-binding disclosure.

RERUN_NEEDED: no
