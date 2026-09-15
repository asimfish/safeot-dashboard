# T-1579 residual feedback pilot findings

All8 jobs exit0, exact2400 steps,100 raw evaluation episodes,checkpoint reload and frozen hashes verified. Old FAIL unchanged. eta=.05 is development only; budgets/targets unchanged.

|Env|Arm|Joint|Reward|Costs|Channel violation probability|Unpriced/overbudget channel-batches|
|---|---|---:|---:|---|---|---|
|DiagReachK2|residual|0.960|8.1592|[5.005078248977661, 4.099515998363495]|[0.0, 0.0]|0/0|
|DiagReachK2|lp|0.990|8.1354|[4.564066772460937, 4.332257447242736]|[0.0, 0.0]|0/1|
|DiagReachK2|max|0.990|8.1354|[4.564066772460937, 4.332257447242736]|[0.0, 0.0]|0/1|
|DiagReachK2|ppolag|0.970|8.1552|[5.020904388427734, 4.055614631175995]|[0.0, 0.0]|0/0|
|DiagReachK3|lp|1.000|8.1941|[5.770816855430603, 3.676432845592499, 8.442036924362183]|[0.0, 0.0, 0.0]|1/1|
|DiagReachK3|residual|1.000|8.7543|[5.617262425422669, 5.192970523834228, 9.740102634429931]|[0.0, 0.0, 0.0]|0/0|
|DiagReachK3|max|1.000|8.1941|[5.770819511413574, 3.6763764142990114, 8.441984615325929]|[0.0, 0.0, 0.0]|0/1|
|DiagReachK3|ppolag|1.000|8.7543|[5.621250877380371, 5.190444703102112, 9.741542749404907]|[0.0, 0.0, 0.0]|0/0|

Promotion: HOLD. The prospective conservative operational gate requires max no worse than residual-only and PPOLag in both reward and joint in both environments. This is not a statistical test.

Mechanism gate and training feedback checks establish that residual/max cannot leave a currently overbudget positive-budget channel unpriced. This is not deployment safety. Residual-only is ordinary Lagrangian feedback; max is not an exact LP dual. Standard PPOLag retains its native lambda update; diagnostic raw price converts its applied coefficient using the observed reward-GAE scale. rho is unused for PPOLag.

Early/late sums of positive batch-mean excess are saved separately in findings.json (not episode violation probability). Raw evaluation episode traces, training episode logs and shaped rollout rewards are retained; no unmeasured KL/occupancy claims. Tiny std uses explicit max(std,1e-8) and is logged; no clipping added.

Route: HOLD confirmation; preserve failed or dominated arms, no automatic40job launch.

New verified union hours=0.0062335826290978325; accumulated separate effective hours=7.807755050857861. Not continuous8h coverage.

Pilot interpretation: K2 max raises joint vs residual-only (.99 vs .96), but lowers reward (8.1354 vs8.1592). K3 max ties joint1 and loses reward vs residual-only (~.5602). LP increment is not established; do not expand dominated max arm. Original SafeOTDual and this PPOLag actor prototype remain distinct.
