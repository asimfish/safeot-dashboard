# T-1589 Candidate support × episode excess factorial

Completed 8 two-cycle smoke and 24 development jobs, all exit0;288000 actual development interactions plus7488 separate final officialdet episodes. Route: HOLD_NO_EXPANSION. No beta search, no old baseline reruns.

## Recomputed T1588 evidence
450cycles:341 selectedalpha0, distinct from325 accepted noops. No feasible nonzero:52; feasible but shaped gain absent:287, of which284 also lack raw gain; only3 raw gains offset by shaping, only2 gains removed by regularizer.1350 candidate screens:1179 mean-feasible,120 already show an event among four samples.100 effective updates:18 accepted sample-event candidates;15 introduce observed events when old paired samples were event-free. Counts reproduce exactly in stall_audit.json; not population/root-cause evidence.

## Factorial development
| Task | Arm | Raw reward | Joint | Worst seed joint | Channel event probabilities |
|---|---|---:|---:|---:|---|
| DiagReachK2 | A_mean | 9.311346 | 0.826923 | 0.698718 | [0.07478632478632478, 0.09935897435897435] |
| DiagReachK2 | A_excess | 9.193951 | 0.990385 | 0.971154 | [0.009615384615384616, 0.0] |
| DiagReachK2 | B_mean | 9.258856 | 0.922009 | 0.766026 | [0.07799145299145299, 0.0] |
| DiagReachK2 | B_excess | 9.215463 | 1.000000 | 1.000000 | [0.0, 0.0] |
| DiagReachK3 | A_mean | 9.536889 | 0.857906 | 0.573718 | [0.0, 0.1420940170940171, 0.0] |
| DiagReachK3 | A_excess | 9.488824 | 0.993590 | 0.980769 | [0.006410256410256411, 0.0, 0.0] |
| DiagReachK3 | B_mean | 9.476963 | 1.000000 | 1.000000 | [0.0, 0.0, 0.0] |
| DiagReachK3 | B_excess | 9.485178 | 1.000000 | 1.000000 | [0.0, 0.0, 0.0] |

## Installation and selection
| Task | Arm | Effective /75 | Selected old | Rejected | Effective with sample event | New event from safe old |
|---|---|---:|---:|---:|---:|---:|
| DiagReachK2 | A_mean | 15 | 59 | 5 | 4 | 3 |
| DiagReachK2 | A_excess | 17 | 54 | 4 | 0 | 0 |
| DiagReachK2 | B_mean | 19 | 53 | 5 | 3 | 3 |
| DiagReachK2 | B_excess | 21 | 52 | 3 | 0 | 0 |
| DiagReachK3 | A_mean | 23 | 52 | 2 | 3 | 3 |
| DiagReachK3 | A_excess | 18 | 56 | 4 | 0 | 0 |
| DiagReachK3 | B_mean | 18 | 55 | 2 | 1 | 1 |
| DiagReachK3 | B_excess | 20 | 49 | 10 | 1 | 0 |

## Gates and controls
A_mean exactly reproduces all six old full_none development runs: all25 cycles actor/critics/optimizer/RNG/batch, selection/acceptance, final actor and all312 raw eval episodes. Smoke validates first-cycle original parity. Four arms share bitwise initialization and first PPO/Fisher shadows. Every cycle independently audited source installation, actor/Adam rollback, PPO-only main critic updates, risks and final episode costs. Failed Fisher solvers excluded from selection, not relabeled valid; checkpoints and Adam reload. All frozen source hashes match.
New arms allocate6000 exploration,3600selection,2400acceptance. Both shadows computed everycycle; RNG restored after Fisher. The middle support replacement also changes actor-installation behavior; it does not identify a pure gradient-direction effect. Fisher is not SafeOT/OT evidence.

## Paired contrasts (training seeds are the units)
DiagReachK2 risk_on_A: reward differences [0.0, -0.184091, -0.168093]; joint differences [0.0, 0.189103, 0.301282].
DiagReachK2 support_on_mean: reward differences [0.024012, 0.090821, -0.272301]; joint differences [-0.205128, 0.189103, 0.301282].
DiagReachK2 risk_on_B: reward differences [-0.031166, -0.097551, -0.001462]; joint differences [0.233974, 0.0, 0.0].
DiagReachK2 interaction: reward differences [-0.031166, 0.08654, 0.16663]; joint differences [0.233974, -0.189103, -0.301282].
DiagReachK3 risk_on_A: reward differences [-0.194809, 0.050616, 0.0]; joint differences [0.426282, -0.019231, 0.0].
DiagReachK3 support_on_mean: reward differences [-0.024468, 0.053564, -0.208873]; joint differences [0.426282, 0.0, 0.0].
DiagReachK3 risk_on_B: reward differences [0.0, 0.0, 0.024644]; joint differences [0.0, 0.0, 0.0].
DiagReachK3 interaction: reward differences [0.194809, -0.050616, 0.024644]; joint differences [-0.426282, 0.019231, 0.0].

## Frozen operational gate
{
  "DiagReachK2": {
    "no_seed_channel_event_regression": true,
    "mean_joint_noninferior": true,
    "mean_reward_noninferior": false
  },
  "DiagReachK3": {
    "no_seed_channel_event_regression": true,
    "mean_joint_noninferior": true,
    "mean_reward_noninferior": false
  }
}
Route HOLD_NO_EXPANSION. Three training seeds exploratory; no powered superiority, no zero-risk claim. Even if promising, further confirmation needs a separate fresh-seed protocol.

## Contextual original baselines
DiagReachK2 ppolag: reward9.365684,joint1.000000,events[0.0, 0.0]; exact snapshot/eval protocol/12000steps receipts reused, no new runs.
DiagReachK2 fisher: reward8.824721,joint1.000000,events[0.0, 0.0]; exact snapshot/eval protocol/12000steps receipts reused, no new runs.
DiagReachK3 ppolag: reward9.773210,joint0.652778,events[0.3066239316239316, 0.0405982905982906, 0.0]; exact snapshot/eval protocol/12000steps receipts reused, no new runs.
DiagReachK3 fisher: reward9.229855,joint1.000000,events[0.0, 0.0, 0.0]; exact snapshot/eval protocol/12000steps receipts reused, no new runs.

## Limits and artifacts
Excess changes the risk functional, not a numerical bug fix: four event-free episodes cannot certify population safety. Recovery minimizes a lexicographic maximum/sum excess and can trade channels; per-channel changes remain logged. Mean constraint compliance and event probability are reported separately. No final eval used for selection; evaluation_shaped return is a post-hoc diagnostic computed from raw traces, never an optimization or selection input.
findings.json and results.csv retain every seed including failures and costs/event/excess; contrasts.csv contains all paired contrasts. jobs/ retains commands/PIDs/exits/receipts, per-cycle old/PPO/Fisher/post/after states, raw/shaped per-episode traces and final312 episodes. manifest/protocol frozen before outcomes. Parent T1588 evidence, global trainers, DERIVATION and PDF unchanged.

## Additional audit and interpretation
600 development cycles passed independent Gaussian regularizer recomputation, full-backbone/mean/logstd proposal-gradient activity, RNG restoration after Fisher, exact prescribed seed-bank separation, acceptance event/excess recomputation, raw-minus-shaped penalty identities and environment action clipping checks. Expanded effective configurations are saved per job. compute_audit.json separates actual PPO minibatch calls, Fisher solver work and installed actor updates.
DiagReachK2: B_excess−A_mean raw reward -0.095882, joint +0.173077; B_excess−Fisher raw reward +0.390743, joint +0.000000; B_excess−PPOLag raw reward -0.150221, joint +0.000000.
DiagReachK3: B_excess−A_mean raw reward -0.051711, joint +0.142094; B_excess−Fisher raw reward +0.255323, joint +0.000000; B_excess−PPOLag raw reward -0.288033, joint +0.347222.
The combined B_excess candidate achieves observed joint1 in both tasks, but lowers mean raw reward versus A_mean in both, so the frozen development criterion fails. This is a safety/reward tradeoff, not unchanged-reward repair. Relative to the contextual Fisher baseline it has higher reward at the same observed joint/event rates; relative to safe K2 PPOLag it has lower reward. No powered superiority or population safety claim follows.
A_excess still has nonzero final event risk and introduces an x-channel event rate in K3 despite removing y events. Thus empirical screening fixes the observed acceptance semantic mismatch, not all deployment risk. B support replacement improves observed learning in some settings, but changes candidate set and optimizer installation jointly; it does not isolate pure gradient geometry. Neither effect is OT-specific. All alpha0 calls retain their real interaction cost. Stop this version under the prospective criterion; any new tradeoff acceptance rule or fresh-seed test would require a separately frozen protocol.

## Per-channel means and positive excess
| Task | Arm | Mean episode cost | Mean normalized positive excess |
|---|---|---|---|
| DiagReachK2 | A_mean | [5.719117, 5.581873] | [0.000703, 0.001112] |
| DiagReachK2 | A_excess | [5.515909, 5.415998] | [0.0001, 0.0] |
| DiagReachK2 | B_mean | [5.371652, 5.43035] | [0.000934, 0.0] |
| DiagReachK2 | B_excess | [5.281164, 5.483342] | [0.0, 0.0] |
| DiagReachK3 | A_mean | [6.268541, 6.254178, 11.422574] | [0.0, 0.001785, 0.0] |
| DiagReachK3 | A_excess | [6.3274, 6.076748, 11.332763] | [4.7e-05, 0.0, 0.0] |
| DiagReachK3 | B_mean | [6.634013, 5.974047, 11.539096] | [0.0, 0.0, 0.0] |
| DiagReachK3 | B_excess | [6.398155, 6.020819, 11.316251] | [0.0, 0.0, 0.0] |
