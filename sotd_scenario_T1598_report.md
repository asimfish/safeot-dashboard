# T1598 N100 results

Decision: HOLD; complete 6/6. All failures retained. Scenario-count single intervention, additional privileged model compute. N100 empirical max is not population safety or CVaR.95.

|Task|Seed|Reward|Joint|Any event|Reward delta vs N20|
|---|---:|---:|---:|---:|---:|
|DiagReachK2|180|9.464341|0.983974|0.016026|-0.030376|
|DiagReachK2|186|9.539203|0.990385|0.009615|0.166957|
|DiagReachK2|187|9.495054|0.964744|0.035256|0.066616|
|DiagReachK3|180|9.821225|0.983974|0.016026|0.066849|
|DiagReachK3|186|9.810307|1.000000|0.000000|0.647753|
|DiagReachK3|187|9.847739|0.961538|0.038462|0.000171|

## Final installation attribution
All six final actors exactly match last effective installation. See final_attribution.json for per-channel original-scene gaps and independent evaluation excess. Gap is null for a PPO-installed final actor; never substitute the unused middle candidate risk. This posthoc analysis is not a causal proof. Both task means improved vs N20, but five policies remain eventful; HOLD. Privileged model compute and repeatedly used development seeds preclude independent-confirmation/SOTA claims.
