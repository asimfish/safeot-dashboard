# Independent dual-only stability results

Old T-DO-001 strict superiority gate remains FAIL. This new protocol was separately authorized, not retroactive promotion. All23 jobs verified, fixed snapshots, exact steps, nonzero optimizer activity and checkpoint reload.

|Environment/method|Seeds|Mean joint|Worst joint|Mean reward|
|---|---:|---:|---:|---:|
|DiagReachK2/dual|5|0.9060|0.5300|9.1132|
|DiagReachK2/ppolag|5|0.9680|0.9100|9.1867|
|DiagReachK3/dual|5|0.9900|0.9500|9.5838|
|DiagReachK3/ppolag|5|0.9620|0.8200|9.6635|

## Separate2400-step mechanism ablation

- frozen: joint=1.0, reward=8.806377, costs=[5.100496954917908, 5.413221840858459].
- zero: joint=1.0, reward=8.807100, costs=[5.092411041259766, 5.417747921943665].
- dual: joint=1.0, reward=8.483787, costs=[4.463222460746765, 5.19490177154541].

Dynamic LP in the ablation is nonzero2/10epochs; zero and frozen already achieve joint1, with higher reward. Dynamic contribution to improved task success is not established. No lambda sweep.

Historical development LP was feasible10/10 each, nonzero dual2/10 K2 and4/10 K3, zero fallback. Reward GAE std minima1.0963/1.1331; gradient equivalence is not causal evidence.

## Noise and infeasible support

Same-action, fixed-initial-state noise cohorts: PPOLag template20/20 LP feasible, all dual0 (inactive, not informative price stability). Critical old SafeFlow template1/20 cohorts infeasible, feasible y-dual range0..1.26079. Removing path weights does not eliminate optimistic selection in the price-generating LP.

Current training logged 0 infeasible epochs and 0 tiny-GAE-scale epochs. Every epoch is in epoch_audit.json; raw/applied lambda and fallback preserved. Explicit stale-lambda fallback is not safety. Scale denominator std+1e-8 preserves previous code; no hidden clipping or large-lambda safety claim.

## Interpretation and receipts

Only exploratory paired training-seed deltas, worst seed and averages. No formal noninferiority/significance/power. Environment results are separate; no claim of superiority, original-SafeOT falsification or VLA/native coverage. Paired differences in findings.json.

New successful-worker union=0.032146h; summed worker-hours=0.120876h; total separate effective intervals=7.801521h. Not continuous overnight coverage; no waiting counted.

Route: synthesize stability and sparse/noisy dual signal; no additional training configurations dispatched. PDF unchanged.
