# T-1585 independent joint transport audit

Verified 24/24 attempted training jobs. All verified jobs12000actualsteps,100raw finaleval and1000logged trainingepisodes,positiveparameterdelta,checkpoint andoptimizerstatesloadable. No oldresultsreused. Status complete.

## A: conditional transport algebra
Step1-4 finite LP at epsilon=eta=0 passes row marginals,multi-risk feasibility/infeasibility,soft price bound,same-objective optimum inheritance and safe-nonoptimal counterexample. Reward retained. Algebra_supplement verifies risk-score centering with matching Jshift and early/late spendingpenalty1.5/0. These are standard algebra, not empirical benefit.

## B: geometry
Selected fisher by frozen offline rule. Raw-unbounded K2seed180 reverted to recoveryzero-step and lost objective; preservedfailure. Fisher passed all6 nonlinear constraints and improves all6 localobjectives. Inexact CG maxrelative residual=0.0012406507056813361; not exact inverseFisher. Cost-gradient directions retained even whenlambda0. Offline improved surrogate is not proof of finalpolicy improvement.

|Axis/env/setting|Seeds|Mean joint|Mean raw reward|Mean deployment costs|Mean violation probability|
|---|---:|---:|---:|---|---|
|shaping/DiagReachK2/0|3|0.0000|10.9299|[9.298133808771768, 8.836669658025107]|[1.0, 1.0]|
|shaping/DiagReachK2/5|3|1.0000|9.3650|[5.5664048846562695, 5.59406888961792]|[0.0, 0.0]|
|shaping/DiagReachK3/0|3|0.0000|10.6173|[8.828439648946125, 7.987825458844504, 15.709297908147178]|[1.0, 1.0, 1.0]|
|shaping/DiagReachK3/5|3|0.6567|9.7732|[6.862153466542562, 6.194129195213318, 11.956013142267864]|[0.30333333333333334, 0.04, 0.0]|
|geometry/DiagReachK2/fisher|3|1.0000|8.8253|[5.026095007260641, 5.342239465713501]|[0.0, 0.0]|
|geometry/DiagReachK2/original|3|0.7767|8.4333|[4.687055770556132, 4.563961268266042]|[0.0, 0.0]|
|geometry/DiagReachK3/fisher|3|1.0000|9.2308|[6.36999822616577, 5.356561810175577, 10.597645632425944]|[0.0, 0.0, 0.0]|
|geometry/DiagReachK3/original|3|0.9967|9.2562|[6.4079909483591715, 5.656466234525045, 10.990193220774332]|[0.0, 0.0, 0.0]|

## Per-seed results
|Axis|Env|Seed|Setting|Joint|Raw reward|Train raw/shaped/penalty|
|---|---|---:|---|---:|---:|---|
|geometry|DiagReachK2|180|fisher|1.000|8.9532|7.2768/6.8656/0.4112|
|geometry|DiagReachK2|180|original|1.000|9.3199|7.4106/6.7384/0.6722|
|geometry|DiagReachK2|186|fisher|1.000|8.8132|7.0072/6.4740/0.5332|
|geometry|DiagReachK2|186|original|0.330|7.5241|6.3444/5.0302/1.3142|
|geometry|DiagReachK2|187|fisher|1.000|8.7095|6.9332/6.3971/0.5361|
|geometry|DiagReachK2|187|original|1.000|8.4558|6.9712/5.7958/1.1754|
|geometry|DiagReachK3|180|fisher|1.000|9.5864|7.4807/7.2250/0.2557|
|geometry|DiagReachK3|180|original|1.000|9.5069|7.3485/6.7076/0.6409|
|geometry|DiagReachK3|186|fisher|1.000|9.2789|7.5968/7.2608/0.3361|
|geometry|DiagReachK3|186|original|1.000|9.5122|7.7320/6.9460/0.7859|
|geometry|DiagReachK3|187|fisher|1.000|8.8270|7.2841/6.9565/0.3276|
|geometry|DiagReachK3|187|original|0.990|8.7496|7.2912/6.4213/0.8699|
|shaping|DiagReachK2|180|0|0.000|10.8773|9.3496/9.3496/0.0000|
|shaping|DiagReachK2|180|5|1.000|9.4081|7.8797/7.3833/0.4964|
|shaping|DiagReachK2|186|0|0.000|11.1446|9.9094/9.9094/0.0000|
|shaping|DiagReachK2|186|5|1.000|9.3722|8.1163/7.4811/0.6352|
|shaping|DiagReachK2|187|0|0.000|10.7676|9.7113/9.7113/0.0000|
|shaping|DiagReachK2|187|5|1.000|9.3148|8.1076/7.4631/0.6445|
|shaping|DiagReachK3|180|0|0.000|10.8210|9.5773/9.5773/0.0000|
|shaping|DiagReachK3|180|5|0.090|9.7267|7.9034/7.3309/0.5725|
|shaping|DiagReachK3|186|0|0.000|10.5552|9.5153/9.5153/0.0000|
|shaping|DiagReachK3|186|5|1.000|9.7918|8.4271/7.9746/0.4525|
|shaping|DiagReachK3|187|0|0.000|10.4756|9.5685/9.5685/0.0000|
|shaping|DiagReachK3|187|5|0.880|9.8010|8.6194/8.1410/0.4785|

Training raw reward is deliveredshapedreward plus exact recorded spendingpenalty; native environment episode reward is alreadyshaped. Raw evaluation disables shaping. Per-episode cost/compliance/success andpenalty trajectories are in train_episodes.jsonl; raw evaluation episodes in result.json. Training cost sumfloat64 vsnativefloat32 rounding audited inacceptance.json; no deployment metric reconstructed frommeans. Optimizerstates reloadable, not an exactcontinuation validation including environmentRNG.

## Joint OT remaining conditions
Conditional actiontransport prevents cross-state/noise selection in the algebra but keeps oldstatedistribution fixed. Still needs calibrated action-risk/reward advantages,originalJ estimates,finite-support coverage,state-distribution-shift error andactualactor fitting error on target visitation. Same-objective support/trust requirements apply to Step4; arbitrarysafePPO bypass does not inherit optimality. No neural jointOT orOTvsKLperformance experiment run. Do not combine geometry andshaping axes as singlefactor evidence. OldFAIL/PDF/DERIVATION_PACKAGE unchanged.

## Final separate-axis judgment
Geometry: Fisher improves K2 meanjoint .7767→1 and rawreward8.4333→8.8253 with zero observed per-channel violations in botharms. In K3 meanjoint .9967→1, reward9.2562→9.2308; no uniform reward improvement. K2seed186 joint .33→1 supports geometry's causal influence under this fixed protocol. It does not establish that fixedgeometry caused all earlier failures, and the selected Fisher policy need not dominate on everyseed. These are3trainingseeds, not300independenttrainingreplicates.

Shaping: K2 coef0→5 changes joint0→1 and rawreward10.9299→9.3650; channel violation probabilities[1,1]→[0,0]. K3 joint0→.6567, rawreward10.6173→9.7732; violations[1,1,1]→[.3033,.04,0]. Mean costs alone conceal remaining K3 failures. The extra objective changes behavior and trades reward for budget compliance here; evidence contradicts a blanket claim that spending-shaping merely harms performance. It is not a guarantee and does not ensure K3 compliance for allseeds.

Do not combine bothaxis improvements as onefactor orattribute toOT. A jointreward-conditionaltransport program remains coherent under documented assumptions, while risk calibration,visitation-shift andactorfitting errors remain unverified. Next OT-versus-KL performance protocol is not launched. PDF,DERIVATION and oldFAIL remain intact.

Measuredupdatecompute geometry/DiagReachK2/original: mean9.727s; traincostmean=[4.364198213388523, 4.0413877336084845]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[2, 0, 0].

Measuredupdatecompute geometry/DiagReachK2/fisher: mean27.222s; traincostmean=[4.632593651592732, 4.314566994905472]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].

Measuredupdatecompute geometry/DiagReachK3/original: mean11.364s; traincostmean=[5.382815552800893, 4.493268553525209, 8.671939282914003]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 1].

Measuredupdatecompute geometry/DiagReachK3/fisher: mean33.998s; traincostmean=[5.521369970401128, 4.34125441211462, 8.648124790827433]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].

Measuredupdatecompute shaping/DiagReachK2/0: mean5.159s; traincostmean=[8.805254877964655, 8.07074196528395]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].

Measuredupdatecompute shaping/DiagReachK2/5: mean4.668s; traincostmean=[5.095004471460978, 4.865693318476279]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].

Measuredupdatecompute shaping/DiagReachK3/0: mean4.377s; traincostmean=[8.734305628448725, 7.520370350410541, 15.113996525565783]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].

Measuredupdatecompute shaping/DiagReachK3/5: mean5.466s; traincostmean=[5.955924082269271, 5.278554058929284, 10.089143038789432]; rejectedupdates=[0, 0, 0]; zeromotionupdates=[0, 0, 0].
