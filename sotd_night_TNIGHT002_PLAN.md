# Eight-hour SafeOT performance campaign — 2026-09-17

Owner authorization: continuously analyze weaknesses, improve, and validate experimentally for the next eight hours. Window is recorded in config.json: 01:28:36–09:28:36 CST. Stop admitting new work at the deadline; already running bounded jobs may finish. Implementation time, failed time, idle time and valid worker time are separate. No promise that eight wall-clock hours equals eight hours of valid training.

## Current state and correction

Read50incremental visible messages14078912–14079702. Latest response reports a384-step mirror comparison and a frozen-actor gradient check, with full integration and24jobs still pending. Inspection narrows those claims:

- mirror_gate_v2 compares two prescribed action sequences, not feedback policies; its sample/det labels are only action-sequence labels. It checks per-step rewards/costs and final position; full9D observation feedback is not checked.
- actor_gradient_gate differentiates `mu.square().sum()`, not the episodic reward or constraints through the environment. It is a neural-network connectivity smoke test, not proof that the proposed algorithm learns.
- pathwise_solver still accepts open-loop actions and detaches them in gradients(). It is not yet the required full-actor update.
- Original8failed workers had0real steps. A24-run queue is not running. Do not publish a performance result or claim closed-loop gate passed.

The independent mentor acceptance checker `check_closed_loop.py` defines the required interface below. The executor must not edit this checker to pass. Its output is an integrity check, not improvement evidence.

## Continuous execution

The detached tmux supervisor uses the authorized Anygent conversation API with execute=true and unique client IDs, every20minutes while idle. Running turns are followed by SSE, never interrupted. A queued user task is preserved. An uncertain POST is recorded and not replayed. Tokens remain in process environment, not repository files. STOP halts further mentor dispatches. Existing native/VLA processes are not restarted.

Each wake-up: read this plan, the task record and the campaign executor's state; inspect actual PIDs/config/checkpoints/counters before retrying; implement or analyze the next scientifically justified step. If workers are already healthy, analyze completed results and improve the next bounded protocol while they continue. Do not merely emit another plan. Every2completed batches or a failed hypothesis requires an outer-loop synthesis: what changed, why it did/did not help, what evidence decides the next branch.

## Independent deployment adapter acceptance

Executor creates `diagnostic_runs/deployment_pathwise/v1/closed_loop.py` exporting:

```python
def rollout(actor, params, config, init_pos, env_noise, action_noise, kernel):
    # init_pos [N,2], noises [N,12,2], all torch.double
    # config is asdict(frozen SyntheticEnvConfig), cost_limits supplied explicitly
    # actor is ORIGINAL 5060-parameter Gaussian actor; use params with functional_call
    # kernel = 'sample' or 'det'
    return {
        'states': ...,           # [N,12,9], BEFORE each action
        'proposal': ...,         # [N,12,2], mu or mu+exp(logstd)*z, before action clip
        'executed': ...,          # [N,12,2], clipped action
        'raw_rewards': ...,      # [N,12]
        'costs': ...,            # [N,12,K]
        'cumulative_costs': ..., # [N,12,K], AFTER each action
    }
```

All outputs are tensors. Build the9D observation with torch.stack/cat, not torch.tensor(list of differentiable tensors). Carry state and cumulative budget gradients through all12steps. Determine K from config.n_constraints / cost_limits, not the two-element safe_caps. Environment noise adds to position; action noise is separately scaled by actor std. Match all clips, raw reward, costs and remaining-budget observations. No model training or file mutation on module import.

Run the immutable mentor checker:

```bash
python3 mentor_reviews/eight_hour_20260917/check_closed_loop.py \
  --adapter diagnostic_runs/deployment_pathwise/v1/closed_loop.py \
  --out diagnostic_runs/deployment_pathwise/v1/closed_loop_gate.json
```

It actually steps the frozen environment384times, checks every field, compares full-actor derivatives of real episode reward and each cost to two fixed parameter directions at three step sizes, checks det pure-std behavior and a nonzero original-actor parameter installation. Calls and source hashes are recorded. Run again only after code changes or a failed test requires revalidation. This is stronger than the previous dummy-loss gate, but the actual solver/transaction smoke must still pass.

## Priority A — independent model-free improvement first

**Hypothesis: the joint solver's K+1 direction span excludes useful directions produced by its PPO backbone.** This can be tested independently while the differentiable oracle is being repaired; it need not wait for the oracle. In the original six KL/raw-inner/raw-outer development runs,18fixed checkpoints(cycles0,12,24) have PPO parameter-update residual outside D of0.9943–0.9998 in Euclidean norm (preflight_existing.json). This only establishes a distinct parameter direction, not that the residual is useful in action space or yields higher reward.

- New bounded task/scope: `diagnostic_runs/candidate_span/v1/`. Copy the frozen T1593 worker/solver rather than the rejected T1595 worker.
- Keep original reward/cost surrogates, raw inner/raw outer, KL0.01, Fisher damping/CG, PPO shadow, selection, optimizer/critic transactions,25×480actual steps,312finaldetepisodes.
- Treatment only: append the normalized residual of actual full-PPO parameter delta after projection onto existing D. Use torch.linalg.lstsq in double, retain original D columns. If residualnorm≤1e-10×max(deltanorm,1), report inactive rather than fabricate a new column. Span(D,residual)=Span(D,delta_PPO). Optimize all coordinates jointly with the same actual KL/cost constraints. This differs from merely placing PPO in the outer candidate pool.
- Seeds180,186,187 ×K2/K3 =6new12k jobs. Exact old-mode first-two-cycle replay at seed180 for both tasks is required. Reuse the6completed RR/KL controls only after source/config/checkpoint replay verification; otherwise run6matched controls and log why.
- Gate: installed float32 KL check, cost units/gradient-target separation, nonzero actor updates, correct candidate slot/momenta, actual12000step counts and exactly312final episodes. No extra tuning.
- Measure raw reward, each event rate, any-event/joint success, direction rank and action displacement, selection/acceptance rejection rate, and solve time. All seeds retained.

## Priority B — deployment kernel × risk functional

Complete T1595 correctly using the independent adapter checker, then implement the frozen24job SM/ST/DM/DT protocol in `mentor_reviews/deployment_pathwise_20260917/PROTOCOL.md`. Original actor, full closed-loop gradients, N20, original transaction mechanism, model-query ledger,8one-cycle smoke checks, then24development runs. This is a privileged known-dynamics diagnostic; it never counts as fair model-free superiority. Gates must compare actual code outputs, not constantPASSfields.

## Priority C — learning-versus-screening interaction allocation

**Hypothesis: only6000of12000actual steps currently supply learning data, so part of the endpoint gap comes from interaction allocation.** Use the verified model-free T1593 control implementation, not the oracle. New scope `diagnostic_runs/interaction_allocation/v1/`.

- One predefined alternative:30exploration episodes/update =360steps; unchanged3×4episode candidate screen=144; old/new4+4acceptance=96.20cycles×600=12000actualsteps,7200learning/2880selection/1920acceptance. Baseline20episodes×25cycles gives6000/3600/2400.
- This changes allocation and update cadence together; label the complete allocation intervention, not a pure gradient-variance ablation. Keep rewards/budgets/network/optimizer/metric and selection rules fixed; do not silently change PPO mini-batch options to force equal optimization counts.
- K2/K3×180,186,187=6newjobs; reuse or reproduce baseline as under A. One-cycle counters and every terminal boundary must pass before launch. Track actual gradient steps/episodes and installation counts, not nominal hp.total_steps.

## Branches after measured progress, not blind grids

1. **Restoration changes are deprioritized:** original six RR/KL runs triggered recovery0/150cycles. Do not spend the night comparing two restoration rules that never execute. Reopen only if a new verified recipe actually triggers recovery and logs a specific reward loss.
2. **Geometry:** if a recipe improves safe reward on both tasks, compare KL to GaussianW2 using the previously frozen first-batch calibration, unchanged estimator/risk/cadence. SixnewW2jobs plus matching verifiedKLcontrol; log actual metric, state weighting and model privilege. No epsilon/radius sweep.
3. **Learning horizon:** only if a safe promising recipe still improves during its last five cycles, compare that recipe and its appropriate original control at48000actualsteps (K2/K3×three seeds×two recipes=12jobs). Keep independent source paths, step ledger, last-checkpoint rule; do not pool12k and48k as equal budget.
4. **Learned-model transfer:** if DT oracle succeeds, freeze a separate bounded protocol replacing privileged dynamics with a fitted model from allowed training data. Report held-out transition/gradient/constraint calibration before new learning. This is desirable but not allowed to delay the already implementable A/C runs. No test-rollout fitting.
5. **Confirmation:** at most two preselected promising recipes, original joint control and PPO-Lag, on five fresh training seeds (proposed91300–91304; verify unused before freezing). Same per-recipe actual interaction budget and one fresh held-out eval seed set. At most40jobs. Select recipes before seeing confirmation outcomes; preserve all results. Pilot development winners are not SOTA.

Prepare new hypotheses when evidence warrants them, but freeze prediction, changed variables, controls, budget, data split and failure rule before launch. No repetition of already rejected normalization/shaping/CF/radius recipes merely to fill runtime. If two attempts on one mechanism fail, analyze and pivot to an independent branch.

## Shared acceptance and resource rules

- Primary outcome: higher **raw** reward at original channel budgets, with no observed final any-channel violation and no loss of joint task success. Candidate advancement: both task means exceed the corresponding verified best-safe control by≥0.05; show PPO-Lag endpoints separately. Zero observations are not a zero-probability certificate. Mean costs alone do not pass safety.
- If a change is informative but does not pass that performance threshold, label it mechanism evidence, not success; further experiments require a specific new hypothesis.
- Seeds are statistical units; reused controls/identical actors are not new replications. Canonical tensor hash + exact equality. Development evaluations already inspected are not fresh confirmation.
- Initial4CPU single-thread workers; allow6then8only after measured stable throughput and resource checks. Local affinity currently128CPUs/load≈80, not a reservation. Do not kill/renice unrelated tasks. GPU0–5authorization persists but small MLPs do not need GPU occupation; use appropriate already-authorized idle resources if a genuinely GPU-heavy verified branch exists. No new paid resources.
- Every worker has actual counters, unique config/source/checkpoint hashes, valid checkpoint reload, PID/start time, progress timestamps, finite wall-time bound and failure exit. Do not use24simultaneous unbounded workers. Freeze code hashes per job; edits go into new version/attempt folders, never change the meaning of a running run.
- Reserve the final30minutes for confirmation already admitted and collection/analysis. Do not start new long jobs beyond remaining time merely to keep the process busy. Already admitted jobs may finish after cutoff, with their admission time and tail reported separately.
- Maintain executor-owned `campaign_state.json`, `hypotheses.jsonl`, `findings.md`, `jobs.jsonl`, and a detached collector/controller. Each batch updates dashboard via existing publication workflow, preserving old entries and labels. Count planned/running/verified/failed separately. Report actual valid active wall time and aggregate worker-hours separately.
- At deadline save final summary: each hypothesis supported/refuted/inconclusive, tested code change, original/after reward and safety with per-seed rows, failure count, valid compute hours, remaining gaps and recommended next action. No paper/PDF edits.

## Provenance

This is a new bounded campaign; the previous T1578 window ended and is not resumed. That older summary reported7.5837valid hours, explicitly short of8; do not carry it into this window. Known related method references and theoretical caveats are in the T-PATH protocol and T-RISK review. Scope is performance research; scientific five-goal/ICLR acceptance remains open.
