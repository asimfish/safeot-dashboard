# Remaining performance gap: independent review, 2026-09-17

## What was actually checked

`audit.py` reads six frozen T1593 raw-inner/raw-outer KL controls, six completed candidate-span runs, and six completed interaction-allocation runs. It recomputes outcomes and update accounting from `epochs.json`, `training_episodes.jsonl`, final episode costs, and actual actor tensors. It performs **zero new environment steps**. `audit.json` includes every input SHA256 and per-cycle evidence.

Conversation recovery initially read 50 visible messages, IDs **14084494–14086719**, followed by incremental messages. The last completed executor reply described A/C completion, a passing independent closed-loop/episodic-gradient gate, and the still-pending pathwise transaction integration. Message 14086545 was additionally read through the detail endpoint. The eight-hour supervisor remains the sole automatic dispatch owner.

## Three distinct gaps

1. **Surrogate feasibility does not carry over to deployment.** All 420 joint candidates were accepted by the local solver and their installed sampled-surrogate costs were within the original budgets. However, **320/420** candidates failed even mean-cost feasibility in their four-episode deterministic screen; **348/420** had at least one screened episode event. Four episodes give a noisy diagnostic, not a population-risk estimate. These correlated development cycles are not 420 independent experiments. Nevertheless, the count identifies a strong discrepancy between the quantity optimized and the quantity screened. Expanding a direction basis cannot itself repair that discrepancy.

2. **The complete update pipeline does not enforce the local solver's trust region.** There were 100 effective installed updates: 39 joint updates, all within KL 0.01 plus the existing numerical tolerance, and 61 full-PPO updates, **56 exceeding 0.01001**. The maximum installed KL was **0.04164960235**. `worker.py` computes regularizers but eligibility is `[0,1,2]` whenever the joint solver accepts; `beta=0`. Thus the radius is a property of the middle candidate, not a bound on the policy actually installed by the complete algorithm. This is a formulation/implementation boundary, not evidence that exceeding this radius caused all violations. A strict common eligibility ablation is needed before a causal conclusion.

3. **Four observed-safe acceptance episodes miss residual risk.** In all **14/18** final-unsafe runs, the last installed actor is tensor-identical to the final actor and passed the four-episode acceptance screen with zero observed events. The independent final 312 episodes then contain events. This confirms screen non-detection for that same policy; it does not locate the earliest harmful update or prove population safety for other policies. Merely relabeling zero observations as a safety certificate is not a repair.

## Results retained, without claiming a win

| Recipe | K2 mean raw reward | K2 mean joint | K3 mean raw reward | K3 mean joint |
|---|---:|---:|---:|---:|
| Original raw/raw KL | 9.142500 | 0.971154 | 9.570985 | 0.994658 |
| Add PPO residual to direction basis | 9.117156 | 0.973291 | 9.520794 | 0.986111 |
| Increase learning share to 60% | 9.125004 | 0.996795 | 9.509269 | 0.976496 |

Each row has three training seeds per task; full per-seed data remain in `audit.json`. The six reused controls are not new experiments. These are narrow synthetic diagnostic tasks, not new native safeRL or VLA benchmark wins. Source/config replay requirements remain in force before labeling treatment differences as controlled causal effects.

## Two accounting corrections

- The earlier **0/150 restoration** statement concerns the *inner SLSQP slack-restoration solve*. Outer acceptance recovery did run: original 6/150, span 9/150, allocation 4/120. These are different mechanisms. A recovery modification is still not the highest priority, but it must not be rejected on the false premise that neither stage ran.
- Allocation results retain stale `effective_config` labels of 6000 exploration / 3600 selection / 2400 acceptance. Actual trace lengths are **7200/2880/1920**, totaling 12000, in all six allocation runs. Correct derived receipts by an explicit erratum; retain original result files and hashes. The training budget itself is not violated by this metadata error.

## Improvement order and theoretical meaning

First complete the already preregistered deployment-kernel × risk-functional experiment using the now-verified closed-loop adapter. It addresses the first discrepancy directly. The adapter's gradient gate does not validate the solver/installation transaction or demonstrate a performance gain. This is a known-dynamics oracle diagnostic; model-query privilege and compute remain separate.

Then run `UNIFORM_UPDATE_PROTOCOL.md`, a small independent model-free test of the second discrepancy. It changes candidate eligibility only, preserves interaction counts and all risk/reward tests, and does not alter the ongoing four-arm pathwise experiment. The expected invariant is that every installed update satisfies the same declared geometry bound. Higher safe reward is a separate empirical question; the filter can also reduce learning.

The existing pathwise protocol already requires N=20 empirical tail constraints to be represented by all per-scenario inequalities. This avoids placing a nonsmooth maximum inside the nonlinear constraint callback; it is an implementation requirement, not a newly invented intervention. Keep K+1 aggregate-risk direction columns separate from the 20×K constraint rows. Do not change the risk level, actor, or outer transaction while integrating it.

The executor's newer `transaction_smoke_attempt2.py` is still only an auxiliary actor-gradient/optimizer check: it uses 40 actual rollouts, zero model environment noise, one Adam step on reward plus a fixed 0.1 excess penalty, and writes `checkpoint_reload=true` without loading the checkpoint. It does not implement the original candidate selection/independent acceptance transaction, KL/Fisher/SLSQP solve, mean/tail factorial, or N=20 model batch. Its successful process exits cannot qualify the 24-job training matrix. See `INTEGRATION_GUIDANCE.md` for a bounded route to complete the actual worker instead of adding more weaker gates.

The broader theoretical lesson is to specify **which deployed policy, risk functional, and installed update** each guarantee covers. CPO relates expected policy returns to policy divergence; practical TRPO explicitly introduces approximations. Neither reference licenses treating a bound on one candidate as a bound on an unrestricted alternative selected afterward. Sources: [CPO, ICML 2017](https://proceedings.mlr.press/v70/achiam17a.html), [TRPO, ICML 2015](https://proceedings.mlr.press/v37/schulman15.html). Application to this code is our inference, verified above through installation logs.

No theorem, PDF, old result, native/VLA worker, budget, or reward definition is changed by this review.
