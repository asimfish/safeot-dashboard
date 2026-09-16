# T-1588 Full actor joint finite-candidate development

10 smoke + 30 development verified; 360000 real development interactions and 9360 separate official deterministic evaluation episodes. Route: HOLD_NO_EXPANSION. Three training seeds per group; 312 episodes estimate each frozen policy, not independent training repeats.

| Task | Arm | Raw reward | Joint | Worst seed joint | Per-channel violation probability |
|---|---|---:|---:|---:|---|
| DiagReachK2 | ppolag | 9.365684 | 1.000000 | 1.000000 | [0.0, 0.0] |
| DiagReachK2 | fisher | 8.824721 | 1.000000 | 1.000000 | [0.0, 0.0] |
| DiagReachK2 | full_none | 9.311346 | 0.826923 | 0.698718 | [0.07478632478632478, 0.09935897435897435] |
| DiagReachK2 | full_kl | 9.318407 | 0.831197 | 0.698718 | [0.07051282051282051, 0.09935897435897435] |
| DiagReachK2 | full_ot | 9.318407 | 0.831197 | 0.698718 | [0.07051282051282051, 0.09935897435897435] |
| DiagReachK3 | ppolag | 9.773210 | 0.652778 | 0.080128 | [0.3066239316239316, 0.0405982905982906, 0.0] |
| DiagReachK3 | fisher | 9.229855 | 1.000000 | 1.000000 | [0.0, 0.0, 0.0] |
| DiagReachK3 | full_none | 9.536889 | 0.857906 | 0.573718 | [0.0, 0.1420940170940171, 0.0] |
| DiagReachK3 | full_kl | 9.404996 | 0.978632 | 0.958333 | [0.013888888888888888, 0.007478632478632479, 0.0] |
| DiagReachK3 | full_ot | 9.455112 | 0.836538 | 0.573718 | [0.013888888888888888, 0.14957264957264957, 0.0] |

## Implementation audit
450 actor/Adam/critic transactions and 450 actual Gaussian KL/W2 recomputations passed; all source hashes match frozen manifest. All 18 full-actor jobs changed backbone, mean-head weights and logstd-head weights, with nonzero proposal gradients every cycle. Checkpoints and actor optimizer states reload. Rejection/alpha0 restores actor and moments; alpha.5 resets moments; alpha1 adopts shadow moments. Critics adopt trained shadow state; native dual updates once per exploration batch.
The full-worker field actor_optimizer_steps counts effective installed proposals, not minibatch Adam steps; shadow_adam_steps in findings reports actual proposal optimizer calls. Baseline update-count fields have different semantics and are not treated as equal compute.

## Interaction and deployment accounting
Each new arm: 6000 stochastic exploration + 3600 candidate selection + 2400 acceptance = 12000 actual interactions. Each baseline: 12000 ordinary training interactions. All shaping5, unchanged budgets/targets. Final 312 raw deterministic episodes never select updates. Regularizers act on auxiliary Gaussians; risk screens evaluate deterministic mean → environment clip → tanh dynamics. Finite 4-episode mean screens do not certify per-episode safety. New arms are a capacity/data matched regularizer ablation; baseline comparisons are resource matched systems, not equal optimizer work.

## Bounded prior quadratic diagnostic
{
  "cases": 36,
  "evaluation_episodes": 396,
  "evaluation_steps": 4752,
  "training_steps": 0,
  "mean_grid_minus_quadratic_validation": 0.10610544106417555,
  "grid_better": 30,
  "grid_worse": 2,
  "quadratic_validation_minus_predicted": -0.18496745292852418,
  "grid_validation_minus_fit": -0.01923403377521835
}
Only 396 new evaluation episodes (4752 interactions), zero training. Grid fit observations selected candidates; new paired validations are independent of fit but reuse the prescribed old validation seeds. These 36 local comparisons do not establish improved final training or isolate all capacity/resource effects. First-attempt serialization failures remain in the parent directory; attempt2 changed Python-float serialization only and reused four verified baseline smoke jobs.

## Frozen decision
{
  "full_none": {
    "DiagReachK2": false,
    "DiagReachK3": false
  },
  "full_kl": {
    "DiagReachK2": false,
    "DiagReachK3": false
  },
  "full_ot": {
    "DiagReachK2": false,
    "DiagReachK3": false
  }
}
OT incremental criterion: False. No statistical superiority/noninferiority or SafeOT contribution established by these three-seed results. No automatic confirmation if HOLD. Original trainers, old evidence, derivation and PDF are untouched.

## Data
Per-seed costs, raw reward, joint and channel violation probabilities: results.csv and findings.json. Per-episode training/evaluation traces, commands/PIDs/exit codes and all model/optimizer snapshots: jobs/. Protocol and manifest were frozen before outcomes.
full_none: effective proposals 38/150, rejected 7, accepted no-op 105, recovery checks 7.
full_kl: effective proposals 31/150, rejected 8, accepted no-op 111, recovery checks 4.
full_ot: effective proposals 31/150, rejected 10, accepted no-op 109, recovery checks 6.

## Additional controls and failure localization
All six paired environment/seed groups have bitwise-identical initial actor/optimizers and first full proposal across the three new arms. Full effective configurations reconstructed from the frozen builder and job inputs are separately labeled in effective_configs/, with original observed runtime config retained. Per-job elapsed wall times (training plus final eval and serialization) come from receipts; baseline training_seconds in findings only sums logged update time and must not be compared with full-worker elapsed time.
The 450 cycles comprise 100 effective accepted full-network proposals, 325 accepted alpha0 no-ops, and 25 rejections. Selection, rather than widespread post-selection reward rejection, is the dominant observed stall here; this is descriptive, not proof of its cause. No-op samples still consumed the fixed real interaction budget. Full actor capacity is verified, but the short proposal direction and 4-episode empirical mean screen do not provide a safe learned policy guarantee. Final per-policy expected-cost feasibility is separated from episode violation in final_mean_vs_event.json.
K2 all new arms lose joint success relative to both safe baselines. K3 KL offers a reward/risk tradeoff relative to Fisher but retains nonzero event violations; OT does not reproduce its safety. Frozen promotion fails; stop this version rather than expand. A next distinct hypothesis would test calibration of the finite-sample mean screen versus deployment risk under the same interaction budget, but it is not implemented or claimed successful in this task. Capacity, proposal learning budget, and sample selection remain different factors; no single-cause conclusion follows.
