# Preregistered common-KL eligibility ablation

Task: T-MENTOR-1600. Follow-up within T-NIGHT-002's existing admission deadline, **2026-09-17 09:28:36 CST**. This adds one bounded hypothesis; it does not restart completed A/C jobs or modify the ongoing T1595 factorial.

## Hypothesis and prediction

In the current transaction, unrestricted full-PPO candidates bypass the joint candidate's KL radius. Applying a common KL eligibility condition to all proposed candidates might improve safe reward by excluding oversized updates. The invariant prediction is zero installed KL violations; the performance hypothesis can fail if the mask starves learning or the dominant problem is objective mismatch. Merely satisfying the invariant is not a performance win.

## Exact change

Start an isolated executor-owned `diagnostic_runs/uniform_update_gate/v1/` from frozen T1593 raw/raw KL code. Do not edit `diagnostic_runs/deployment_pathwise/v1/` or either completed branch for this experiment.

In `worker.py`, preserve old behavior under `uniform_update_gate=false`. For treatment only, after building the original eligibility set and computing regularizers:

```python
eligible = [i for i in original_eligible
            if i == 0 or (np.isfinite(regs[i]['KL']) and regs[i]['KL'] <= 0.01001)]
```

The original local radius is 0.01; 1e-5 is the existing installation tolerance, not an expanded hyperparameter grid. Keep the old actor eligible. Keep solver-rejected joint candidates excluded. Do **not** rescale/interpolate PPO parameters, change Adam momenta rules, change the actor basis, change risk thresholds, or alter sample allocation. Keep full shadow optimization and **all three candidate screens** even if one candidate is ineligible, so treatment and control both consume exactly 12000 interactions. Each final accepted actor must satisfy the measured same-state old-to-installed forward Gaussian KL condition. This is auxiliary Gaussian geometry, not a claim about deterministic Dirac-policy KL or population safety.

Keep `risk.py` choose/accept scoring and per-channel risk definitions unchanged. Preserve current critic and dual transactions, including critic advancement when actor selection rejects. Source labels and configuration flags must expose the new eligibility rule. Record each candidate's KL, original eligibility, revised eligibility, selected source, rejection reason, actual installed KL, and effective/no-op updates.

## Integrity checks before development

1. Snapshot and hash all source/config files; use new attempt folders and never overwrite old failures. Verify imports with one worker before dispatching the matrix.
2. Gate-off replay for seed180 on both K2/K3, first two complete cycles, exactly reproduces frozen T1593 actor/optimizer/decision traces. No final evaluation needed. Gate-off computations must not consume extra RNG. If exact replay fails, fix the implementation before proceeding; if original sources cannot be recovered, run explicitly matched fresh controls and report that substitution.
3. Reuse saved candidate metrics as fixed microcases: old remains eligible, over-radius full-PPO is excluded, solver-rejected middle remains excluded, in-radius PPO preserves its original optimizer transaction. Include a case where the original selector chose over-radius PPO and assert the changed selection can never install it. Masking may change selection but cannot reconstruct unavailable counterfactual acceptance outcomes from old logs.
4. Two treatment smoke jobs, K2/K3 seed180, two cycles each. They must finish the actual 960-step ledger and preserve the original transaction invariants. Do not gate development on favorable reward. Keep all invalid or failed runs visible.

## Bounded development matrix

- Six treatment runs: K2/K3 × seeds180,186,187; 25 cycles ×480 =12000 actual training interactions per run; 312 final deterministic evaluation episodes. Final checkpoint only; original raw reward, channel budgets, horizon and actor architecture.
- Reuse the six T1593 raw/raw KL controls only after replay/hash verification. Otherwise add exactly six matched controls with their own provenance. No radius, seed, or mask-threshold sweep.
- Training cost is 72000 interactions for six treatment runs, plus separately recorded smoke/control costs. Final evaluation is 1872 episodes/22464 steps. Per-worker timeout and admission cutoff follow the night PLAN; initially four one-thread CPU workers. The independent pathwise branch has priority when CPU contention is material.

## Decision and follow-up

Report every seed's raw reward, per-channel event count/excess, any-event count and joint success; show paired development differences and installed-source/step-size/no-op rates. All six runs remain in the report. The development seeds have already been explored, so a promising result requires fresh-seed confirmation from the existing night plan.

For promotion retain the night criterion: no observed final channel event in any treatment seed, no joint-success regression, and both task reward means at least 0.05 above their verified best safe reference means, with PPO-Lag endpoints shown separately. Zero events do not certify zero risk.

- Invariant holds but reward falls/no-op rises: reject as a sufficient performance remedy. Do not launch a radius sweep. Later a projected proposal would be a separate, explicit algorithm and optimizer-state intervention.
- Safety/reward unchanged: reject this mechanism as the primary explanation under this setting.
- Safe reward improves: confirm on fresh seeds before introducing W2 or integrating the mask into a new version of the pathwise factorial.

Publish completed A/C findings and this audit on the existing dashboard with links to full evidence; distinguish original local-solver radius from this new whole-pipeline eligibility condition. Do not change manuscript guarantees until evidence supports the revised algorithm.
