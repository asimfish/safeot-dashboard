# T1592 cross-fitted reward baseline development

HOLD_THIS_RECIPE

One component: reward advantage baseline only. Cost advantages/Jhat/budgets/shaping5/Fisher CG/KL/W2/SLSQP/PPOshadow/critics/duals/excess screen/det unchanged. Reward D0 changes as part of the intervention; cost direction columns stay exact on shared data. Twenty leave-one-episode-out ridge fits use only other19 episodes; frozen recipe, no tuning.

## Development (three training seeds per cell)

|Task|Metric|Estimator|Mean raw reward|Mean joint|Mean P(any)|Worst joint|All seeds observed-safe|
|---|---|---|---:|---:|---:|---:|---|
|DiagReachK2|KL|time_loo|9.215463|1.000000|0.000000|1.000000|True|
|DiagReachK2|KL|cf_state|9.292089|0.998932|0.001068|0.996795|False|
|DiagReachK2|W2|time_loo|9.249502|0.986111|0.013889|0.958333|False|
|DiagReachK2|W2|cf_state|9.337499|0.997863|0.002137|0.993590|False|
|DiagReachK3|KL|time_loo|9.485178|1.000000|0.000000|1.000000|True|
|DiagReachK3|KL|cf_state|9.528672|0.964744|0.035256|0.900641|False|
|DiagReachK3|W2|time_loo|9.383932|1.000000|0.000000|1.000000|True|
|DiagReachK3|W2|cf_state|9.524430|0.996795|0.003205|0.990385|False|

Full per-seed results/paired deltas in results.csv and paired_training.csv. Official raw deterministic evaluator unchanged; final312 episodes never used for fitting/selection. Eval counterfactual shaped return is computed for accounting only, with official reward left raw.

## Frozen recipe decision

[
  {
    "metric": "KL",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "cf": {
          "env": "DiagReachK2",
          "metric": "KL",
          "estimator": "cf_state",
          "reward": 9.292088858195825,
          "joint": 0.9989316239316239,
          "any_event": 0.0010683760683760683,
          "worst_joint": 0.9967948717948718,
          "worst_reward": 9.236396082290687,
          "observed_safe_all_seeds": false,
          "seeds": [
            {
              "seed": 180,
              "reward": 9.236396082290687,
              "joint": 0.9967948717948718,
              "success": 1.0,
              "any_event": 0.003205128205128205
            },
            {
              "seed": 186,
              "reward": 9.352326310879624,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            },
            {
              "seed": 187,
              "reward": 9.287544181417166,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            }
          ]
        },
        "best_safe_time_reward": 9.215463222182082,
        "required_increment": 0.05,
        "endpoint": 9.365684
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "cf": {
          "env": "DiagReachK3",
          "metric": "KL",
          "estimator": "cf_state",
          "reward": 9.528672198305218,
          "joint": 0.9647435897435898,
          "any_event": 0.035256410256410256,
          "worst_joint": 0.9006410256410257,
          "worst_reward": 9.313750918758645,
          "observed_safe_all_seeds": false,
          "seeds": [
            {
              "seed": 180,
              "reward": 9.820100211233989,
              "joint": 0.9006410256410257,
              "success": 1.0,
              "any_event": 0.09935897435897435
            },
            {
              "seed": 186,
              "reward": 9.313750918758645,
              "joint": 0.9935897435897436,
              "success": 1.0,
              "any_event": 0.00641025641025641
            },
            {
              "seed": 187,
              "reward": 9.452165464923018,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            }
          ]
        },
        "best_safe_time_reward": 9.485177616287011,
        "required_increment": 0.05,
        "endpoint": 9.229855
      }
    ]
  },
  {
    "metric": "W2",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "cf": {
          "env": "DiagReachK2",
          "metric": "W2",
          "estimator": "cf_state",
          "reward": 9.33749932807968,
          "joint": 0.9978632478632479,
          "any_event": 0.0021367521367521365,
          "worst_joint": 0.9935897435897436,
          "worst_reward": 9.26139294112434,
          "observed_safe_all_seeds": false,
          "seeds": [
            {
              "seed": 180,
              "reward": 9.417461859923973,
              "joint": 0.9935897435897436,
              "success": 1.0,
              "any_event": 0.00641025641025641
            },
            {
              "seed": 186,
              "reward": 9.333643183190725,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            },
            {
              "seed": 187,
              "reward": 9.26139294112434,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            }
          ]
        },
        "best_safe_time_reward": 9.215463222182082,
        "required_increment": 0.05,
        "endpoint": 9.365684
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "cf": {
          "env": "DiagReachK3",
          "metric": "W2",
          "estimator": "cf_state",
          "reward": 9.524429727088432,
          "joint": 0.9967948717948718,
          "any_event": 0.0032051282051282055,
          "worst_joint": 0.9903846153846154,
          "worst_reward": 9.44894906635192,
          "observed_safe_all_seeds": false,
          "seeds": [
            {
              "seed": 180,
              "reward": 9.673820763286345,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            },
            {
              "seed": 186,
              "reward": 9.44894906635192,
              "joint": 0.9903846153846154,
              "success": 1.0,
              "any_event": 0.009615384615384616
            },
            {
              "seed": 187,
              "reward": 9.450519351627028,
              "joint": 1.0,
              "success": 1.0,
              "any_event": 0.0
            }
          ]
        },
        "best_safe_time_reward": 9.485177616287011,
        "required_increment": 0.05,
        "endpoint": 9.229855
      }
    ]
  }
]

Only a fixedmetric meeting BOTH tasks all3seed safety and +.05 against best safe timeLOO plus endpoint is promising. Missing safe control is not a win. OT value must be assessed separately through CF_W2 vs CF_KL at equal observed safety; no CF-only success is automatically OT contribution.

## Independent mechanism (CF minus time, average two fixed anchors per training seed)

|Task|Metric|Seed|Optimism delta [95% conditional]|True sample shaped delta|True det raw delta [95% conditional]|
|---|---|---:|---|---:|---|
|DiagReachK2|KL|180|0.04427 [-0.03843,0.12682]|0.08411|0.04446 [0.03806,0.05022]|
|DiagReachK2|W2|180|0.01060 [-0.06689,0.08878]|0.08289|0.04585 [0.03919,0.05144]|
|DiagReachK2|KL|186|-0.23224 [-0.28293,-0.18604]|0.07569|0.06285 [0.05923,0.06659]|
|DiagReachK2|W2|186|-0.24779 [-0.30348,-0.19770]|0.07883|0.09440 [0.09087,0.09772]|
|DiagReachK2|KL|187|3.06680 [2.98174,3.15277]|0.01749|-0.36226 [-0.36758,-0.35628]|
|DiagReachK2|W2|187|2.42823 [2.35072,2.50027]|-0.02320|-0.35662 [-0.36119,-0.35181]|
|DiagReachK3|KL|180|-0.08932 [-0.14991,-0.03520]|-0.14460|-0.02714 [-0.03317,-0.02150]|
|DiagReachK3|W2|180|0.04430 [-0.01538,0.10101]|-0.13622|-0.02405 [-0.02848,-0.01963]|
|DiagReachK3|KL|186|0.03622 [-0.04181,0.13222]|-0.01066|-0.11968 [-0.12498,-0.11462]|
|DiagReachK3|W2|186|-0.02006 [-0.12106,0.09588]|0.09763|-0.18553 [-0.19119,-0.17998]|
|DiagReachK3|KL|187|-0.20464 [-0.25079,-0.15863]|-0.03175|0.04781 [0.04475,0.05070]|
|DiagReachK3|W2|187|-0.72829 [-0.78663,-0.65914]|-0.17030|-0.08009 [-0.08259,-0.07774]|

Optimism means estimator-specific Gtrain minus complete fresh stochastic gain, not OOF residual MSE. Full candidate raw/shaped/penalty/sample/det/risk retained in mechanism_anchors.csv and mechanism_risks.csv. Fresh Ghold uses common timeLOO on all candidates, not refitted CF. Paired512 whole-episode bootstrap only measures fresh evaluation noise conditional on frozen original bank/candidates; training n=3, anchors not independent training replicas. Reduction in optimism with worse true gain/risk is calibration improvement without performance improvement.

## Gates and accounting

Algebra, leakage, shuffle, constant/collinear design, real neural gradient, fixed-baseline, cost-column identity gates passed before training. Smoke common actor/PPO/RNG/calibration and transactions passed. Time controls undergo exact25cycle and312episode replay; development_gate.json is the authoritative result. Ridge/source/feature/fold/OOF records retained in every cycle baseline checkpoint.

{
  "development_training": 288000,
  "development_gradient_data": 144000,
  "development_selection": 86400,
  "development_acceptance": 57600,
  "development_final_eval_episodes": 7488,
  "development_final_eval_steps": 89856,
  "smoke_training": 7680,
  "smoke_eval_steps": 1152,
  "mechanism_eval_steps": 92160,
  "extra_training_rollouts": 0,
  "grand_environment_steps": 478848
}

All validation and candidate-selection rollouts charged in12000; only6000steps feed PPO gradient per training job. No fresh mechanism rollout used to fit candidates. Twelve mechanism banks add92160 diagnostic steps, not training. Actor installs/PPO optimizer steps/compute/solver distance activity/phase-specific costs recorded separately.

## Boundaries

Synthetic mechanism evidence only. No global joint convexity, statistical superiority, zero-risk, SOTA/native/VLA claim. Four-episode screen low power is unchanged. This frozen recipe is closed after this development decision; no radius/ridge/features scan or automatic native/VLA extension.

## OT-specific contrast (separate from baseline estimation)

[
  {
    "env": "DiagReachK2",
    "CF_W2_minus_CF_KL_reward": 0.04541046988385489,
    "both_all_seed_observed_safe": false,
    "interpretation": "not a like-safe reward advantage"
  },
  {
    "env": "DiagReachK3",
    "CF_W2_minus_CF_KL_reward": -0.0042424712167861145,
    "both_all_seed_observed_safe": false,
    "interpretation": "not a like-safe reward advantage"
  }
]

## Full trained-seed outcomes

|Task|Metric|Estimator|Seed|Raw reward|Joint|P(any)|
|---|---|---|---:|---:|---:|---:|
|DiagReachK2|KL|time_loo|180|9.258067|1.000000|0.000000|
|DiagReachK2|KL|time_loo|186|9.302515|1.000000|0.000000|
|DiagReachK2|KL|time_loo|187|9.085808|1.000000|0.000000|
|DiagReachK2|KL|cf_state|180|9.236396|0.996795|0.003205|
|DiagReachK2|KL|cf_state|186|9.352326|1.000000|0.000000|
|DiagReachK2|KL|cf_state|187|9.287544|1.000000|0.000000|
|DiagReachK2|W2|time_loo|180|9.270043|1.000000|0.000000|
|DiagReachK2|W2|time_loo|186|9.108127|0.958333|0.041667|
|DiagReachK2|W2|time_loo|187|9.370336|1.000000|0.000000|
|DiagReachK2|W2|cf_state|180|9.417462|0.993590|0.006410|
|DiagReachK2|W2|cf_state|186|9.333643|1.000000|0.000000|
|DiagReachK2|W2|cf_state|187|9.261393|1.000000|0.000000|
|DiagReachK3|KL|time_loo|180|9.585912|1.000000|0.000000|
|DiagReachK3|KL|time_loo|186|9.442500|1.000000|0.000000|
|DiagReachK3|KL|time_loo|187|9.427122|1.000000|0.000000|
|DiagReachK3|KL|cf_state|180|9.820100|0.900641|0.099359|
|DiagReachK3|KL|cf_state|186|9.313751|0.993590|0.006410|
|DiagReachK3|KL|cf_state|187|9.452165|1.000000|0.000000|
|DiagReachK3|W2|time_loo|180|9.520693|1.000000|0.000000|
|DiagReachK3|W2|time_loo|186|9.334131|1.000000|0.000000|
|DiagReachK3|W2|time_loo|187|9.296973|1.000000|0.000000|
|DiagReachK3|W2|cf_state|180|9.673821|1.000000|0.000000|
|DiagReachK3|W2|cf_state|186|9.448949|0.990385|0.009615|
|DiagReachK3|W2|cf_state|187|9.450519|1.000000|0.000000|

All mechanism anchors come from the prespecified original KL_s1 trajectories in T1591, cycles6/18. These fixed-data comparisons do not substitute for the independently learned CF policies or establish long-run causality.

## Runtime and estimator limits

Timing column wall_seconds_training_and_final_eval includes official final evaluation, matching the parent worker timer boundary. Baseline-fit seconds count both metric shadows: CF fits20folds per solve,40 per cycle because KL/W2 shadows are both computed. Those fits consume compute, not extra simulator steps. effective_runtime_inventory.json reconstructs frozen builder settings and reads actual optimizer groups from checkpoints; it does not claim an additional in-training config sensor.

OOF residual MSE is only regression error. Recorded LR episode-contribution dispersion is also not the full parameter-gradient covariance. Even if optimism falls, reduced genuine sample/det gain or degraded safety cannot count as a successful policy repair. Final risks remain empirical; 0/312 events does not imply zero risk.

## Synthesis and route

**HOLD_THIS_RECIPE.** Every CF task/metric cell has at least one seed with observed final episode budget violations; none meets the frozen all-seed safety condition. CF K2 rewards also remain below safePPOLag9.365684. CF K3 rewards9.528672(KL)/9.524430(W2) remain below best safe timeLOO9.485178+.05=9.535178. Allfour meanrawreward increases are therefore not success under the joint criterion. No additional seeds, radii, ridge weights or features are dispatched.

|Task|Metric|Mean CF−time optimism|Mean CF−time true sample shaped gain|Mean CF−time true det raw gain|
|---|---|---:|---:|---:|
|DiagReachK2|KL|0.959609|0.059100|-0.084982|
|DiagReachK2|W2|0.730348|0.046173|-0.072124|
|DiagReachK3|KL|-0.085912|-0.062338|-0.033002|
|DiagReachK3|W2|-0.234684|-0.069632|-0.096553|

The episode-crossfit estimator does not consistently reduce optimizer-selected optimism: six of12 task/metric/seed summaries decrease and six increase (correlated contrasts, not12independent trainingreplicas). In K2 seed187 the increase is +3.067 KL/+2.428 W2 while true deterministic raw gain falls by about.362/.357. K3 average optimism decreases, yet true sample shaped and det raw gains both fall; improved calibration here is not improved policy performance. This is evidence against this frozen recipe, not against all conditional baselines or all OT approaches. OOF regression residuals cannot override the paired rollout evidence.

CF_W2−CF_KL meanrawreward is +.045410 onK2 and −.004242 onK3, but neither setting is all-seed observed-safe on bothtasks. No matched-safe OT advantage is established. Three seeds are exploratory; no significance or zero-risk claim. The unchanged four-episode deployment screen remains an independent limitation; no new repair is implemented in this task.

## Per-channel final risks (mean of three policy estimates)

|Task|Metric|Estimator|Mean episode cost vector|Channel event probabilities|Mean normalized positive excess|
|---|---|---|---|---|---|
|DiagReachK2|KL|time_loo|[5.281164, 5.483342]|[0.0, 0.0]|[0.0, 0.0]|
|DiagReachK2|KL|cf_state|[5.360773, 5.556057]|[0.001068, 0.0]|[3e-06, 0.0]|
|DiagReachK2|W2|time_loo|[5.419058, 5.623175]|[0.0, 0.013889]|[0.0, 3.5e-05]|
|DiagReachK2|W2|cf_state|[5.537804, 5.337101]|[0.0, 0.002137]|[0.0, 3e-06]|
|DiagReachK3|KL|time_loo|[6.398155, 6.020819, 11.316251]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|KL|cf_state|[6.67209, 5.973749, 11.552552]|[0.007479, 0.029915, 0.0]|[1.8e-05, 0.000204, 0.0]|
|DiagReachK3|W2|time_loo|[6.017932, 5.812024, 10.793813]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|W2|cf_state|[6.55471, 5.617332, 11.092086]|[0.003205, 0.0, 0.0]|[1.1e-05, 0.0, 0.0]|
