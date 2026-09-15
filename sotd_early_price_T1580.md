# T-1580 early price intervention findings

Frozen residual_feedback/v1 source copied byte-for-byte. Three-arm protocol preceded results; no residual branch or radius/epoch sweep. All completed jobs verify2400 actual steps,100 raw eval, optimizer activity, checkpoint reload and frozen source hashes.

|Seed|Arm|Joint|Success|Reward|Costs|Violation probabilities|
|---|---|---:|---:|---:|---|---|
|180|drop1y|1.0|1.0|8.757247|[5.6016868257522585, 5.218806371688843, 9.74869873046875]|[0.0, 0.0, 0.0]|
|180|drop3y|1.0|1.0|8.260569|[5.868261041641236, 3.801068744659424, 8.658102693557739]|[0.0, 0.0, 0.0]|
|180|original|1.0|1.0|8.194102|[5.770816855430603, 3.676432845592499, 8.442036924362183]|[0.0, 0.0, 0.0]|
|186|drop1all|0.03|0.03|7.726337|[4.520727519989014, 3.7162151193618773, 7.236551203727722]|[0.0, 0.0, 0.0]|
|186|original|0.0|0.0|7.212969|[3.594296622276306, 3.2113966155052185, 5.867593216896057]|[0.0, 0.0, 0.0]|
|187|drop1all|1.0|1.0|8.895139|[5.415453767776489, 5.6184298706054685, 9.91932207107544]|[0.0, 0.0, 0.0]|
|187|original|1.0|1.0|8.895139|[5.415453767776489, 5.6184298706054685, 9.91932207107544]|[0.0, 0.0, 0.0]|

## Reproduction and fixed-batch update
Baseline reproduces all10 epoch costs/LP duals/ESS and final raw reward/joint/costs at absolute tolerance1e-6. Epoch1 J=[1.226481,2.887852,2.897288], raw y=.52766949. All branches load the same seed-specific saved preupdate models, critics, optimizers, RNG, data and noncallable environment state after checking identical collected batch and model tensors. Runtime counted_step wrappers retained; v1 serialization failure preserved.

- seed180 drop1y: sample logratio KL=0.03114699; deterministic action delta from preupdate=0.16409369; postupdate delta vs original=0.04582676.
- seed180 drop3y: sample logratio KL=0.03254088; deterministic action delta from preupdate=0.12176433; postupdate delta vs original=0.00000000.
- seed180 original: sample logratio KL=0.03254088; deterministic action delta from preupdate=0.12176433; postupdate delta vs original=0.00000000.
- seed186 drop1all: sample logratio KL=0.03540102; deterministic action delta from preupdate=0.12974134; postupdate delta vs original=0.09062818.
- seed186 original: sample logratio KL=0.03473522; deterministic action delta from preupdate=0.12710698; postupdate delta vs original=0.00000000.
- seed187 drop1all: sample logratio KL=0.01083056; deterministic action delta from preupdate=0.05983490; postupdate delta vs original=0.00000000.
- seed187 original: sample logratio KL=0.01083056; deterministic action delta from preupdate=0.05983490; postupdate delta vs original=0.00000000.

KL is mean(logp_pre-logp_post) on saved240 behavior state-actions, not exact population KL and can be negative. Grad norms are after clipping; full cost/reward advantages and optimizer-step norms retained in dual_epochs.json. Fixed-batch differences alone do not establish long-term effects.

## Routing
Development gate: PASS_LOCAL_ONLY. Reward>.05 gain, joint no worse and no channel violation increase were fixed before results; not statistical significance.
New seeds186/187 were tested under separately frozen first-update ALL-price cancellation; do not conflate with seed180 y-only intervention.

Theory-only neighborhood design in neighborhood_design.md: empirical path KL and state-mass constraints restrict selection but do not impose causal dynamics or certify realizability. No trained radius selected. Nonzero optimal dual under safe behavior is not inherently incorrect. No superiority over PPOLag established. Old FAIL and PDF unchanged.
New successful-worker union=0.01596803h; separate cumulative=7.82372308h; failedv1 not counted. No continuous8h claim.

## Final mechanism judgment
Seed180 isolates a local early-price effect: cancelling only first-update y increases final reward by0.563145 with joint1 and no observed channel violations, while cancelling only epoch3 y gives smaller reward gain0.066467. This is a deterministic paired development intervention, not formal significance or a general causal explanation. Newseed186 first-price removal raises reward by0.513368 but joint only0→.03; learning failure persists. Newseed187 has first LP price [0.0, 0.0, 0.0] and unchanged update/results: a no-op control, not affirmative improvement evidence. No stable method-level fix established; no more epochs/radii trained. Earlier PPOLag seed180 reward8.7543 remains the matched development reference, not evidence of superiority.
