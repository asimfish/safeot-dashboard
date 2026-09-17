# T1604 bounded mechanism follow-up
Status: COMPLETE; no new training matrix.

## T1603 paired causal diagnostic
[
  {
    "env": "DiagReachK2",
    "mode": "monitor",
    "policies": 3,
    "reward": 9.438586078458316,
    "joint": 0.9928385416666666,
    "events": 22,
    "episodes": 3072
  },
  {
    "env": "DiagReachK2",
    "mode": "gate",
    "policies": 3,
    "reward": 9.420654275037455,
    "joint": 0.9977213541666666,
    "events": 7,
    "episodes": 3072
  },
  {
    "env": "DiagReachK3",
    "mode": "monitor",
    "policies": 3,
    "reward": 9.756520126224205,
    "joint": 1.0,
    "events": 0,
    "episodes": 3072
  },
  {
    "env": "DiagReachK3",
    "mode": "gate",
    "policies": 3,
    "reward": 9.727559526372426,
    "joint": 0.9996744791666666,
    "events": 1,
    "episodes": 3072
  }
]
Decision: HOLD

Gate/monitor differ only by eligibility mask, but effects are conditional on3 reused development training seeds; no population safety certificate or SOTA inference. Complete exact replays/publication belong to T1603 finalizer.

## Residual source audit
|Task|Seed|Fresh events|Final source|Last cycle|
|---|---:|---:|---|---:|
|DiagReachK2|180|0|pathwise_DT|24|
|DiagReachK2|186|0|pathwise_DT|18|
|DiagReachK2|187|7|pathwise_DT|22|
|DiagReachK3|180|1|pathwise_DT|24|
|DiagReachK3|186|0|pathwise_DT|24|
|DiagReachK3|187|0|pathwise_DT|22|

DiagReachK2 seed187: original optimization: {"max_cost": [5.87999963760376, 5.879998683929443], "sequential_max": [5.880000114440918, 5.879999160766602], "Bopt": [5.88, 5.88], "max_minus_Bopt": [-3.623962401277936e-07, -1.3160705565340436e-06], "logged_exact": true}; admission: {"max_cost": [5.9974141120910645, 5.999107837677002], "task_budget": [6.0, 6.0], "events": 0, "hash_match": true}
After-install unsafe-old fallback cycles: [24]. Full episode seeds/costs/overshoots in residual audit. Frozen actor unchanged; real and model event indicators agree.

DiagReachK3 seed180: original optimization: {"max_cost": [6.8600006103515625, 6.370000839233398, 12.075506210327148], "sequential_max": [6.860000133514404, 6.370000839233398, 12.075506210327148], "Bopt": [6.859999999999999, 6.37, 12.25], "max_minus_Bopt": [6.103515630684342e-07, 8.392333983309186e-07, -0.17449378967285156], "logged_exact": true}; admission: {"max_cost": [6.899567604064941, 6.442916393280029, 12.162984848022461], "task_budget": [7.0, 6.5, 12.5], "events": 0, "hash_match": true}
After-install unsafe-old fallback cycles: []. Full episode seeds/costs/overshoots in residual audit. Frozen actor unchanged; real and model event indicators agree.

## Counterexample smoke
[
  {
    "env": "DiagReachK2",
    "replacements": 4,
    "repair_accepted": true,
    "solver_queries": 22,
    "reward_before": 9.382332801818848,
    "reward_after": 9.317206382751465,
    "events_before": 1,
    "events_after": 1,
    "reward_delta": -0.06512641906738281,
    "counts": {
      "real_steps": 0,
      "search_model_steps": 12288,
      "validation_model_steps": 6144,
      "optimization_model_steps": 26400
    }
  },
  {
    "env": "DiagReachK3",
    "replacements": 0,
    "repair_accepted": false,
    "solver_queries": 0,
    "reward_before": 9.659826278686523,
    "reward_after": 9.659826278686523,
    "events_before": 0,
    "events_after": 0,
    "reward_delta": 0.0,
    "counts": {
      "real_steps": 0,
      "search_model_steps": 12288,
      "validation_model_steps": 6144,
      "optimization_model_steps": 0
    }
  }
]
K2 repairs4 discovered scenarios with22 primitive optimization forwards, but independent event count is0 before and after while reward drops; this is implementation evidence, not efficacy. K3 has no search violations at its predetermined anchor and does not trigger repair. No alternative anchor/margin selected.

## Formulation conclusion
Finite optimization max + finite admission zero events do not equal expectation/chance/almost-sure safety. K2 old can later be observed unsafe and still retained; rejection alone supplies no corrective policy. v4 already states realizability/statistical-margin conditions: this pathwise privileged-model branch bypasses old graph transport rather than proving it repaired. See formulation_gap.md for page9/20/21/22/57 mapping.

## Next route
No automatic matrix. next_protocol.md gives equal-resource ranked-vs-random training-scenario replacement design, with common original reward bank and independent validation; requires separate freeze of shared200-query allocation and correctness gates. Smoke does not yet support a performance benefit.

## Costs
{
  "audit_real_steps": 96,
  "audit_model_steps": 2496,
  "smoke_model_steps": 63264,
  "training_steps": 0
}
All original inputs unchanged; source exact=True
