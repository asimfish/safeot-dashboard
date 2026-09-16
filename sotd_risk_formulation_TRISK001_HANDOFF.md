# T-RISK-001 → T1594 handoff

The external experiment agent remains owner of T1594. This mentor task only produced a separate review and recomputed existing artifacts; no experiment files, actor, checkpoint, protocol, or old PDF was changed.

- T1593: completed and published; HOLD_OBJECTIVE_RECIPE remains.
- T1594: only task_start.md existed at the last check. Platform reported `Selected model is at capacity` twice (internal messages 14068743, 14071816); no audit/training process existed. Delivery is not execution.
- Corrective guidance delivered: guidance-20260916-risk-audit-correction-1594-02, message 14071783. It replaces the earlier contradictory automatic first-hit+CP training instruction. Reverse channel creation returned 409, no bound reply conversation; no token issued.
- Read DERIVATION_REVIEW.md and summary.json here before continuing. No reason to repeat the 24-job T1593 training-signal calculation or 48-candidate frozen-bank calculation except verification.
- New facts: 53/1500 channel-batch first-hit advantages are zero, 1447 nonzero; no event flag/cost mismatch. Frozen first-hit LR risk-change MAE is .040671 against stochastic evaluation versus .379501 against deterministic evaluation. These are correlated, posthoc diagnostics, not training results.
- Still needed from T1594: canonical actor-hash deduplication across all72 jobs, validation-selection conditionality audit, matched-final-actor screen provenance, true-gradient checks if necessary, and a budget-consistent next protocol. Four-sample CP rejecting every candidate does not establish a good algorithm. No risk-budget relaxation, test reuse, or reward-target search is authorized by this handoff.
- Next design priority: learn/estimate risk for the actual deterministic deployment kernel while retaining original reward and budgets. Independent calibration and error controls are required; first-hit relabeling of Gaussian training trajectories is insufficient by itself.
- Minor T1593 prose discrepancy: report direct conclusion 2 says both K2 metrics lost joint success; its own table shows W2 joint improving .986111→.995726. Tables and HOLD decision remain valid; report prose correction belongs to its owner, not this task.
- Resume via the project's task entry before edits; this mentor task temporarily uses the shared task session. T1594 files are untouched. Preserve existing native/VLA processes.

Reproduce locally:

```bash
python3 mentor_reviews/risk_formulation_20260916/audit_existing.py
python3 mentor_reviews/risk_formulation_20260916/verify.py
```
