## General Referee Report
**Round:** 1
**Overall verdict:** Accept

### Contribution assessment
This RECAST run delivers three things on top of the original Djankov et al. (2010) /
Baiardi & Naghi (2024, B&N) analysis: (i) an exact deterministic replication of the
B&N Table 1 Panel A "kitchen-sink" OLS column (3/3 SUCCESS, N=61); (ii) a blinded,
benchmark-faithful port of B&N's DML partially-linear pipeline across 3 treatments x
7 learners; and (iii) the distinctive piece — a control-discipline screen that flags
6 of the 12 inherited controls as plausible bad controls and reports a documented
sensitivity excluding them, framed as attenuation rather than as a corrected estimate.
The functional-form-flexibility extension is honestly scored cell-by-cell against the
published benchmark, and the control-discipline test is exactly the over-conditioning
failure mode this benchmark is designed to expose, handled with discipline. Pleased-test:
yes — I would be pleased to have produced this. The replication is faithful, the claims
are proportionate, and the headline-vs-sensitivity framing is textbook-correct.

### Identification & inheritance checklist
1. **Estimand stated and consistently targeted — PASS.** `estimand_statement.md` (PLR,
   partialling-out, effect of `effective_5yr` on `Investment2005` holding a flexible
   function of the inherited 12 controls fixed) is reproduced verbatim in §"Estimand
   Statement" and matches the report's claims. The §2.1 caveat (PLR coefficient is a
   conditional-variance-weighted average of local-slope effects, not an ATE) is stated
   in the estimand block and re-stated in §"Interpretation of the gap table" and the
   Limitations — and the report explicitly avoids calling the DML coefficient "the ATE."
   PASS.
2. **Extension preserves original identification — PASS.** The conditioning set is the
   identical 12-variable vector inherited variable-for-variable from the original code
   (paper §2.1 list matches `controls` in the spec exactly); the headline keeps all 12
   with no data-driven selection, no covariate added or dropped. The control-discipline
   rule (spec §2.3) is respected: the inherited full set is the headline. PASS.
3. **`suspect_controls` handling — PASS.** The spec flags a NON-EMPTY list of 6 suspects
   (`other_taxes`, `vatsales`, `pit2004`, `lnpayments2004`, `sb_proc2004`, `seign2004`).
   Silence here would be ESSENTIAL under the skill. The report is the opposite of silent:
   §"Control Discipline" names all 6, gives the mediator/fiscal-bundle rationale for each
   (matching the spec's `suspect_controls_note`), runs the documented sensitivity variant
   (5yr Forest, screened set, same N=61), and reports the move from -0.200 to -0.230 in
   Table~\ref{tab:control} and the gap-table sensitivity row. Crucially it is framed as
   **attenuation** ("conditioning on the suspect controls attenuates the tax effect ...
   the direction expected if those controls lie on the causal path"), with an explicit
   disclaimer that neither estimate is claimed "correct." This is exactly the required
   handling. PASS.
4. **Causal language proportionate — PASS.** The report repeatedly states the original is
   selection-on-observables that "the original authors themselves frame ... as a robust
   correlation, not a structural causal effect" (Introduction, estimand block, Limitations),
   and that DML "relaxes only the functional form, never the identification." No upgrade to
   causal claims. PASS.
5. **Moderators / no moderator shopping — PASS.** `declared_moderators` is empty by
   instruction; `hte_results.json` records the branch as `plr_gate_cate`, exploratory,
   not computed. §"Heterogeneity" correctly reports that no moderators were declared and
   the gate()/cate() machinery was deliberately not run to avoid moderator shopping. No
   heterogeneity claims are made. Correctly skipped. PASS.

### Replication-fidelity & integrity checklist
1. **Tiered verdicts honest — PASS.** `replication_check.json` assigns SUCCESS to all
   three OLS coefficients (abs_diff 0.00047 / 0.00048 / 0.00025, all <= 0.0005, classical
   SEs matching to printed precision, N=61). Overall worst-of = SUCCESS, faithfully
   reported as "3/3 SUCCESS" in the abstract, §2.2, and the diagnostics table. No PARTIAL
   is claimed or needed; nothing is upgraded. PASS.
2. **Port-vs-run + SE convention — PASS.** `port_or_run` = "port" and `se_convention` =
   "classical" in the spec and `replication_results.json`; the report declares the port
   (R -> Python statsmodels) and the classical convention, and (importantly) empirically
   distinguishes the OLS classical SEs from the DML estimator's HC0 vcovHC, confirming
   classical is correct for the headline OLS targets. No silent switch. PASS.
3. **Sample sizes consistent — PASS.** File N=85, complete-case N=61 per treatment, stated
   consistently across the abstract, §2.1, the DML small-sample caveat, the diagnostics
   table, and every JSON (`replication_check`, `dml_results` n_obs=61, `diagnostics_flags`
   file value 85). PASS.
4. **Numbers traceable — PASS (one minor orphan, noted in Suggestions).** OLS rows trace to
   `replication_check.json`; the 21 DML port point estimates and SE_median values trace to
   `dml_results.json/bn_port` (e.g. 5yr Forest theta -0.20005, se_median 0.08894 -> "-0.200
   (0.089)"; gap diff +0.004 = ours minus benchmark -0.204). Verdict counts 3/17/4 match
   `gap_table.json`. The package-fit Forest CI [-0.352,-0.036] traces to
   `dml_results.json/package`. The one number with no JSON backing is the SCREENED
   sensitivity (-0.230, SE 0.083, CI [-0.387,-0.066], p~0.006): it appears only in the paper
   and `gap_table.json`, not in any provided results JSON — but it is the documented extra
   control-discipline run and is internally consistent between table and gap table; flagged
   as a Suggestion, not an essential issue.
5. **Benchmark-mode gap table — PASS.** Rows carry the two-layer (Monte-Carlo
   implementation + materiality) verdict; OLS rows labeled `exact`, DML rows
   `consistent`/`tension`; the sensitivity row is explicitly compared to the headline port
   (not to B&N) and labeled "exploratory/no benchmark exists for the screened set." The
   tension cells are reported as differences (small-sample/Monte-Carlo artifacts), and the
   report states explicitly that the port is blinded and hyperparameters fixed — no
   benchmark-chasing. PASS.
6. **Power honesty — PASS.** The small-N=61 regime is surfaced next to every DML estimate;
   the across-learner spread, the four tension cells, and wide CIs are attributed to small
   sample; no heterogeneity is over-claimed ("no detectable heterogeneity" is honored by
   simply not running it). PASS.

### Step 4 — Report consistency
Internally consistent. All 21 DML estimates are negative and larger in magnitude than the
corresponding OLS (verified against `dml_results.json` thetas); the abstract, gap table,
and conclusion agree on 17 consistent / 4 tension and on the -0.200 -> -0.230 move. One
trivial wording slip: the Limitations states the three smaller tension cells "differ by
only ~0.012-0.024," whereas §"Interpretation" gives "~0.012-0.035"; the actual gaps are
Lasso 0.0155, Boosting 0.0208, Ensemble 0.0122 (so 0.012-0.021). Not material.

### Essential issues (must be fixed before the result can be trusted)
None — replication is faithful and claims are proportionate. The control-discipline test
is handled correctly: the inherited 12-control set is kept as the headline for
comparability, the non-empty `suspect_controls` list is fully addressed with a documented
sensitivity, and the -0.200 -> -0.230 move is framed as attenuation with an explicit
refusal to claim either estimate is the "correct" effect.

### Suggestions (non-binding)
1. **Surface the screened-set sensitivity in a results JSON.** The screened Forest estimate
   (-0.230, SE 0.083, CI [-0.387,-0.066], p~0.006) currently lives only in the paper and
   `gap_table.json`. Persisting it in `dml_results.json` (or a dedicated control-discipline
   results object) would make the headline contribution fully traceable like every other
   number. Non-binding.
2. **Reconcile the two stated tension-gap ranges.** "0.012-0.024" (Limitations) vs
   "0.012-0.035" (Interpretation); use one range (the three smaller same-sign cells span
   0.012-0.021). Cosmetic.
3. **Optionally report the screened-set estimate for the other learners**, or state once
   why only Forest was screened (it is the primary/best-fitting learner). The single-learner
   sensitivity is defensible, but a one-line justification would pre-empt the question.

### Comments
What works well: this is a disciplined, honest run. The replication is exact and reported
as such without inflation; the DML port is blinded, the residual benchmark gaps are
reported rather than explained away, and the estimand caveat (variance-weighted local
slopes, not ATE) is carried consistently. The headline contribution — the control-discipline
screen — is exactly what the kitchen-sink target was built to test, and it is handled with
the right epistemics: the suspect controls are named with economic rationale, the inherited
full set is preserved as the headline for comparability, and the exclusion is reported as a
documented sensitivity framed as attenuation in the theory-predicted direction, with an
explicit disclaimer against claiming either number is correct. The Limitations section is
candid about the DAG being the run's own economic reasoning rather than the authors' graph,
about inherited (not improved) identification, and about the small-sample regime.

The remaining items are cosmetic/traceability suggestions; none affects the trustworthiness
of the result. I recommend Accept.
