# T1603 Independent det scenario admission
Status COMPLETE; decision HOLD.

Frozen A and final E use distinct paired1024scene banks. No eval data trains/selects/refits. Original task budgets, margin.02, raw/raw objectives and PPO shaping5 fixed. Mean feasible is not event-free; zero observations do not prove zero risk. Synthetic privileged model/reused3developmentseeds per task only.

|Task|Seed|Mode|Fresh reward|Joint|Any event|Effective updates|Unsafe fallback|Final source|
|---|---:|---|---:|---:|---:|---:|---:|---|
|DiagReachK2|180|gate|9.376600|1.000000|0.000000|9|8|pathwise_DT|
|DiagReachK2|180|monitor|9.392940|0.985352|0.014648|10|12|pathwise_DT|
|DiagReachK2|186|gate|9.484580|1.000000|0.000000|12|0|pathwise_DT|
|DiagReachK2|186|monitor|9.517527|1.000000|0.000000|10|12|pathwise_DT|
|DiagReachK2|187|gate|9.400783|0.993164|0.006836|7|7|pathwise_DT|
|DiagReachK2|187|monitor|9.405292|0.993164|0.006836|6|8|pathwise_DT|
|DiagReachK3|180|gate|9.709893|0.999023|0.000977|8|1|pathwise_DT|
|DiagReachK3|180|monitor|9.761254|1.000000|0.000000|11|0|pathwise_DT|
|DiagReachK3|186|gate|9.758690|1.000000|0.000000|21|1|pathwise_DT|
|DiagReachK3|186|monitor|9.750310|1.000000|0.000000|12|0|pathwise_DT|
|DiagReachK3|187|gate|9.714096|1.000000|0.000000|8|3|pathwise_DT|
|DiagReachK3|187|monitor|9.757996|1.000000|0.000000|11|3|pathwise_DT|

## Paired gate-minus-monitor by training seed
[
  {
    "env": "DiagReachK2",
    "seed": 180,
    "reward_delta": -0.016339843400976387,
    "any_event_delta": -0.0146484375,
    "joint_delta": 0.0146484375
  },
  {
    "env": "DiagReachK2",
    "seed": 186,
    "reward_delta": -0.0329469654182674,
    "any_event_delta": 0.0,
    "joint_delta": 0.0
  },
  {
    "env": "DiagReachK2",
    "seed": 187,
    "reward_delta": -0.004508601443342359,
    "any_event_delta": 0.0,
    "joint_delta": 0.0
  },
  {
    "env": "DiagReachK3",
    "seed": 180,
    "reward_delta": -0.051361114919578135,
    "any_event_delta": 0.0009765625,
    "joint_delta": -0.0009765625
  },
  {
    "env": "DiagReachK3",
    "seed": 186,
    "reward_delta": 0.00837921423610058,
    "any_event_delta": 0.0,
    "joint_delta": 0.0
  },
  {
    "env": "DiagReachK3",
    "seed": 187,
    "reward_delta": -0.04389989887185222,
    "any_event_delta": 0.0,
    "joint_delta": 0.0
  }
]

## Frozen margin02-minus-margin0 (new data, no learning)
[
  {
    "env": "DiagReachK2",
    "seed": 180,
    "reward_delta": -0.07441931690459569,
    "any_event_delta": -0.01171875,
    "joint_delta": 0.01171875
  },
  {
    "env": "DiagReachK2",
    "seed": 186,
    "reward_delta": -0.0234075563145155,
    "any_event_delta": -0.015625,
    "joint_delta": 0.015625
  },
  {
    "env": "DiagReachK2",
    "seed": 187,
    "reward_delta": -0.08767359600083174,
    "any_event_delta": -0.04296875,
    "joint_delta": 0.04296875
  },
  {
    "env": "DiagReachK3",
    "seed": 180,
    "reward_delta": -0.05861124076110118,
    "any_event_delta": -0.0302734375,
    "joint_delta": 0.0302734375
  },
  {
    "env": "DiagReachK3",
    "seed": 186,
    "reward_delta": -0.0613666157992128,
    "any_event_delta": -0.021484375,
    "joint_delta": 0.021484375
  },
  {
    "env": "DiagReachK3",
    "seed": 187,
    "reward_delta": -0.08823967640656029,
    "any_event_delta": -0.02734375,
    "joint_delta": 0.02734375
  }
]

## Costs and limitations
{
  "train_real": 144000,
  "old_eval_real": 44928,
  "fresh_eval_real": 147456,
  "frozen_A_real": 147456,
  "gate_train_real": 2880,
  "optimization_model": 6538800,
  "admission_model": 2764800,
  "gate_optimization_model": 166800,
  "gate_admission_model": 55296,
  "preflight_model": 48
}
{
  "receipt_interval_union_seconds": 3982.9115607738495,
  "worker_receipt_seconds": 11554.831379175186,
  "failed_receipt_seconds": 0,
  "meaning": "process receipt intervals include IO/evaluation/optimization, not pure training time"
}

Next: HOLD; inspect rejection/old retention/unsafe fallback and reward tradeoff. No margin/threshold/search or large benchmark expansion.
All6 monitor complete replay checks: 6
Failures: []
