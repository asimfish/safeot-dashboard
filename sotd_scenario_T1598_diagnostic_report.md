# T1598 scenario audit

New batch, separate from expired eight-hour window. Zero real environment interactions in this audit.

|Env|Seed|Arm|Solver accepted|Recovery|Query failure|Pathwise installs|PPO installs|
|---|---:|---|---:|---:|---:|---:|---:|
|DiagReachK2|180|ST|2|22|1|0|3|
|DiagReachK2|180|DT|25|0|0|7|3|
|DiagReachK2|186|ST|0|23|2|0|6|
|DiagReachK2|186|DT|25|0|0|6|2|
|DiagReachK2|187|ST|0|25|0|0|1|
|DiagReachK2|187|DT|25|0|0|4|0|
|DiagReachK3|180|ST|3|19|3|1|6|
|DiagReachK3|180|DT|25|0|0|8|3|
|DiagReachK3|186|ST|2|18|5|0|5|
|DiagReachK3|186|DT|25|0|0|10|4|
|DiagReachK3|187|ST|0|23|2|0|3|
|DiagReachK3|187|DT|25|0|0|9|0|

All 12 final actors exactly equal the last effective postselection actor. A rejected middle checkpoint is the original actor, not the rejected optimizer solution.

9 accepted DT middle objects were strictly event-free on original20 and eventful on fresh256. This supports a scenario-coverage diagnostic, not a generalization guarantee or training causal proof. All24 objects retained. Model transitions 73728 fresh +5760 replay. N100 single-factor comparison admitted after exact replay and transaction gates.

|Object|Env|Seed|Cycle|Kind|Original event|Fresh event|Fresh reward|
|---:|---|---:|---:|---|---:|---:|---:|
|0|DiagReachK2|180|0|middle|0.000000|0.000000|4.979745|
|1|DiagReachK2|180|12|middle|0.050000|0.136719|9.478066|
|2|DiagReachK2|180|24|middle|0.050000|0.121094|9.496151|
|3|DiagReachK2|180|24|final|0.050000|0.113281|9.495831|
|4|DiagReachK2|186|0|middle|0.050000|0.132812|6.490554|
|5|DiagReachK2|186|12|middle|0.050000|0.000000|9.350420|
|6|DiagReachK2|186|24|middle|0.000000|0.042969|9.370760|
|7|DiagReachK2|186|24|final|0.000000|0.042969|9.370760|
|8|DiagReachK2|187|0|middle|0.000000|0.101562|9.246367|
|9|DiagReachK2|187|12|middle|0.000000|0.183594|9.499036|
|10|DiagReachK2|187|24|middle|0.000000|0.191406|9.487983|
|11|DiagReachK2|187|24|final|0.000000|0.058594|9.438279|
|12|DiagReachK3|180|0|middle|0.000000|0.000000|5.025312|
|13|DiagReachK3|180|12|middle|0.000000|0.101562|9.715752|
|14|DiagReachK3|180|24|middle|0.000000|0.093750|9.743937|
|15|DiagReachK3|180|24|final|0.000000|0.093750|9.743937|
|16|DiagReachK3|186|0|middle|0.000000|0.000000|6.875874|
|17|DiagReachK3|186|12|middle|0.000000|0.082031|9.755324|
|18|DiagReachK3|186|24|middle|0.050000|0.140625|9.703971|
|19|DiagReachK3|186|24|final|0.000000|0.000000|9.153776|
|20|DiagReachK3|187|0|middle|0.000000|0.003906|9.263666|
|21|DiagReachK3|187|12|middle|0.050000|0.054688|9.853240|
|22|DiagReachK3|187|24|middle|0.000000|0.113281|9.863338|
|23|DiagReachK3|187|24|final|0.050000|0.046875|9.845892|

## Mentor seed supplement handled
Actual frozen extra80 formula uses env*10000000+seed*10000+cycle*100. All12000 IDs distinct; all15 run-pair intersections zero. Saved tapes agree. No runtime source edited or jobs restarted. See seed_namespace_audit.json and seed_correction_response.md. Both exact N20 replays and N100 transaction smokes passed; six-job development dispatched with four active workers.
