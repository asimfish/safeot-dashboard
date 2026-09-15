# Actor-aligned development and difficult-seed extension

Verified21 jobs,18development plus3extension; all exit0, exact steps,100raw eval/checkpoint reload/frozen source hashes. No old results reused. Prototype changes actor objective, finite-time baseline, optimization and critic targets together; not single-factor attribution or SafeOTDual result.

|Phase|Env|Seed|Arm|Joint|Reward|Costs|Violation probability|
|---|---|---:|---|---:|---:|---|---|
|development|DiagReachK2|180|aligned|1.000|8.6648|[4.917310590744019, 4.194319834709168]|[0.0, 0.0]|
|development|DiagReachK2|180|lp|0.990|8.1354|[4.564066772460937, 4.332257447242736]|[0.0, 0.0]|
|development|DiagReachK2|180|ppolag|0.970|8.1552|[5.020904388427734, 4.055614631175995]|[0.0, 0.0]|
|development|DiagReachK2|186|aligned|0.000|6.4646|[2.4172576761245725, 2.1482647371292116]|[0.0, 0.0]|
|development|DiagReachK2|186|lp|0.770|8.6525|[4.544455962181091, 5.913132734298706]|[0.0, 0.23]|
|development|DiagReachK2|186|ppolag|0.150|8.9148|[5.0317993211746215, 6.115184593200683]|[0.0, 0.85]|
|development|DiagReachK2|187|aligned|0.000|7.1250|[2.21530442237854, 4.470280632972718]|[0.0, 0.0]|
|development|DiagReachK2|187|lp|1.000|9.1797|[5.690717606544495, 5.159208798408509]|[0.0, 0.0]|
|development|DiagReachK2|187|ppolag|1.000|8.8701|[5.177825160026551, 5.151106677055359]|[0.0, 0.0]|
|development|DiagReachK3|180|aligned|1.000|8.9405|[5.95768033027649, 4.58469295501709, 9.543481721878052]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|180|lp|1.000|8.1941|[5.770816855430603, 3.676432845592499, 8.442036924362183]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|180|ppolag|1.000|8.7543|[5.621250877380371, 5.190444703102112, 9.741542749404907]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|186|aligned|1.000|8.1656|[5.931079244613647, 2.9148501801490783, 7.856500539779663]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|186|lp|0.000|7.2130|[3.594296622276306, 3.2113966155052185, 5.867593216896057]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|186|ppolag|0.020|7.9547|[4.1663716650009155, 4.984073753356934, 8.08996877193451]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|187|aligned|1.000|9.0706|[5.598425278663635, 5.533224711418152, 10.034183435440063]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|187|lp|1.000|8.8951|[5.415453767776489, 5.6184298706054685, 9.91932207107544]|[0.0, 0.0, 0.0]|
|development|DiagReachK3|187|ppolag|1.000|8.9541|[5.468309507369995, 5.692668957710266, 10.04734658241272]|[0.0, 0.0, 0.0]|
|extension|DiagReachK3|186|aligned|1.000|9.5122|[6.372675523757935, 5.868747005462646, 11.176790885925293]|[0.0, 0.0, 0.0]|
|extension|DiagReachK3|186|lp|1.000|9.5823|[6.4838898229599, 5.8902511262893675, 11.274140825271607]|[0.0, 0.0, 0.0]|
|extension|DiagReachK3|186|ppolag|1.000|9.7918|[6.782363939285278, 6.14306387424469, 11.824736003875733]|[0.0, 0.0, 0.0]|

## Mechanism and boundaries
Undiscounted time-to-go centered by leave-one-out time means, weighted by1/episodes. Actor has no critic dependence. Cost-unit/terminal identities and zero-price gradients pass. Solver uses gradient-span coordinates with both KL and coordinate trust bounds; approximate reward-subproblem multipliers recovered via NNLS, stationarity reported, no inherited price. Recovery solves a different slack objective and has lambda=null. Prediction is a sampled surrogate, not actual next-rollout cost or safety.

- development DiagReachK2 seed180: accepted10/10, recovery0, nonzero-price0, maxKKT=0.0013169368218764591, next-rollout prediction MAE=[0.36929456389147824, 0.6947051026637365]; final critic MSE=[3.48447585105896, 4.468383312225342].
- development DiagReachK2 seed186: accepted10/10, recovery0, nonzero-price0, maxKKT=0.0002589388861998581, next-rollout prediction MAE=[0.5892911913403672, 0.4647444650403454]; final critic MSE=[11.434383392333984, 4.60488748550415].
- development DiagReachK2 seed187: accepted10/10, recovery0, nonzero-price0, maxKKT=0.0003406814067204755, next-rollout prediction MAE=[0.6469084619979779, 0.416811758544472]; final critic MSE=[5.439892292022705, 4.275237083435059].
- development DiagReachK3 seed180: accepted10/10, recovery0, nonzero-price0, maxKKT=0.00017903107875579677, next-rollout prediction MAE=[0.39287002042687164, 0.6896116590910766, 0.6389146649669815]; final critic MSE=[2.4852991104125977, 6.39643669128418].
- development DiagReachK3 seed186: accepted10/10, recovery0, nonzero-price0, maxKKT=0.0007044615132792853, next-rollout prediction MAE=[0.8492438982066539, 0.4717297693367425, 0.8801594450032496]; final critic MSE=[17.007286071777344, 10.470667839050293].
- development DiagReachK3 seed187: accepted10/10, recovery0, nonzero-price0, maxKKT=0.00019414044205876956, next-rollout prediction MAE=[0.5108142723682829, 0.6996898643808486, 0.6745528095359601]; final critic MSE=[3.437079668045044, 8.037958145141602].
- extension DiagReachK3 seed186: accepted50/50, recovery0, nonzero-price0, maxKKT=0.0038122159850615487, next-rollout prediction MAE=[0.49487650057636046, 0.34159160389574, 0.6285828421053944]; final critic MSE=[0.42972347140312195, 1.484628677368164].

Prediction error compares successive batches from different samples, so includes sampling variance and distribution change. Critic MSE is measured against same-batch finite returns, not a held-out accuracy estimate. Since actor does not use critics, critic error cannot directly explain these actor updates. Full KL/rejection/slack/predictions and cumulative training excess are preserved. Baseline critic errors refer to their original discounted targets and are not pooled with finite targets.

## Route
Confirmation gate: HOLD; no20job confirmation. Preserve dominated/unstable outcomes. No hyperparameter search.. Operational thresholds were fixed before results, not formal power/significance.
New effective successful-worker union=0.036694h; separately accumulated=7.860417h. Not continuous8h coverage. OldFAIL remains and PDF unchanged.

## Final synthesis and next single-factor question
K2 development mean joint: aligned .3333, PPOLag .7067, LP .9200; rewards7.4182/8.6467/8.6559. K3 development mean joint: aligned1, PPOLag .6733, LP .6667; rewards8.7255/8.5544/8.1007. These are3training seeds per environment, not300independent training replicates. K3seed186 at12000steps all joint1; aligned reward9.5122 vsPPOLag9.7918 andLP9.5823. No confirmatory expansion.

All110 aligned updates across development and extension accepted,0recovery,0nonzero cost multiplier. Thus K3 development gains cannot be credited to active constraint prices. K2 failed seeds186/187 are success0 with no observed evaluation violations and safe mean costs; not a rejection loop. Actor installation matches the solved empirical surrogate (cost discrepancy<=3.2e-7), KL<=.010000005; next-rollout prediction MAE remains roughly .34-.88 depending channel/job and includes sampling variance. This supports implementation consistency, not accurate real-MDP prediction. Maximum subspace KKT stationarity is .003813, approximate rather than exact. No full-parameter optimality claim.

Legacy trainer stdout lambda_mean=.001 and history lambda trajectory are unused scaffold state for aligned only, NOT the prototype multiplier. Actual subproblem prices are epochs.json lambda_raw; in recovery they would be null. Baseline lines retain native meanings. Finite critic errors cannot directly cause the aligned updates because no critic estimates enter its actor objective. Diagnostics do not yet separate finite-return estimator changes from restricted local optimizer dynamics.

Next proposed single-factor investigation (not launched): keep finite-return reward/cost surrogates, KL direction/radius, budgets and data fixed, compare frozen gradient-span coordinates versus refreshing the actor-gradient span within the same local solve. First use saved preupdate batches to check objective gains and parameter/KKT differences. This targets optimizer-subspace restriction without adding penalties or price floors. It remains an untested hypothesis, not an explanation established by these results.

Compute cost on mandatory12000job: aligned11.24seconds of measured update work versusPPOLag3.87 andLP3.37, with0additional environment samples; hardware timings are descriptive only. Final checkpoints contain model states and actor reload verification; no claim of optimizer-continuation checkpoint because all12000jobs restarted from the same original seed by protocol. Initial optimizer/RNG/batch checkpoints retained separately.
