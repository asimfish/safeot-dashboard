# T-1587 deployment-aligned joint prototype

Statuscomplete; verified32/32 smoke/development jobs. Noformal result substituted bysmoke. Newarms restrictedbiascapacity,not equalcapacitybaselineproof. Common12000traininginteractions includeeverycandidate andvalidationrollout; final312detepisodes separate.

|Environment/arm|Seeds|Joint|Raw reward|Meancost|Channel violation probability|
|---|---:|---:|---:|---|---|
|DiagReachK2/ppolag|3|1.0000|9.3657|[5.566162923462371, 5.596695318690732]|[0.0, 0.0]|
|DiagReachK2/fisher|3|1.0000|8.8247|[5.025248442450141, 5.343321518510835]|[0.0, 0.0]|
|DiagReachK2/joint_kl|3|1.0000|8.6608|[4.759096132384406, 4.281425829371835]|[0.0, 0.0]|
|DiagReachK2/joint_ot|3|1.0000|8.6587|[4.753886739922385, 4.28732957646378]|[0.0, 0.0]|
|DiagReachK3/ppolag|3|0.6528|9.7732|[6.860804033075643, 6.195773116034321, 11.956279108666967]|[0.3066239316239316, 0.0405982905982906, 0.0]|
|DiagReachK3/fisher|3|1.0000|9.2299|[6.369199231139615, 5.358453826517121, 10.598857249969091]|[0.0, 0.0, 0.0]|
|DiagReachK3/joint_kl|3|0.9882|8.7763|[5.690512413143093, 5.0233550652479515, 9.728838693382395]|[0.0, 0.0, 0.0]|
|DiagReachK3/joint_ot|3|0.9893|8.7759|[5.6898092265821925, 5.02070094887008, 9.725604481167265]|[0.0, 0.0, 0.0]|

## Per-seed results
|Env|Seed|Arm|Joint|Reward|Updates|Rejectfraction|Recoveryfraction|
|---|---:|---|---:|---:|---:|---:|---:|
|DiagReachK2|180|fisher|1.0000|8.9542|50|0.000|0.000|
|DiagReachK2|180|joint_kl|1.0000|8.6696|3|0.880|0.000|
|DiagReachK2|180|joint_ot|1.0000|8.6699|3|0.880|0.000|
|DiagReachK2|180|ppolag|1.0000|9.4082|696|0.000|0.000|
|DiagReachK2|186|fisher|1.0000|8.8095|50|0.000|0.000|
|DiagReachK2|186|joint_kl|1.0000|8.6256|7|0.720|0.000|
|DiagReachK2|186|joint_ot|1.0000|8.6190|6|0.760|0.000|
|DiagReachK2|186|ppolag|1.0000|9.3756|668|0.000|0.000|
|DiagReachK2|187|fisher|1.0000|8.7104|50|0.000|0.000|
|DiagReachK2|187|joint_kl|1.0000|8.6872|3|0.880|0.000|
|DiagReachK2|187|joint_ot|1.0000|8.6871|3|0.880|0.000|
|DiagReachK2|187|ppolag|1.0000|9.3132|732|0.000|0.000|
|DiagReachK3|180|fisher|1.0000|9.5866|50|0.000|0.000|
|DiagReachK3|180|joint_kl|0.9647|8.7069|2|0.920|0.000|
|DiagReachK3|180|joint_ot|0.9679|8.7064|2|0.920|0.000|
|DiagReachK3|180|ppolag|0.0801|9.7290|692|0.000|0.000|
|DiagReachK3|186|fisher|1.0000|9.2757|50|0.000|0.000|
|DiagReachK3|186|joint_kl|1.0000|8.8352|7|0.720|0.000|
|DiagReachK3|186|joint_ot|1.0000|8.8350|7|0.720|0.000|
|DiagReachK3|186|ppolag|1.0000|9.7922|732|0.000|0.000|
|DiagReachK3|187|fisher|1.0000|8.8272|50|0.000|0.000|
|DiagReachK3|187|joint_kl|1.0000|8.7868|5|0.800|0.000|
|DiagReachK3|187|joint_ot|1.0000|8.7865|5|0.800|0.000|
|DiagReachK3|187|ppolag|0.8782|9.7984|716|0.000|0.000|

## Scope and numerical audit
Gate verifies exactdetkernel,terminalcostunits,realGaussianKL/W2,rewardgradient,sameobjectivefeasiblecandidate,softactive andinfeasiblefixtures. Runtimeactorreg recomputed;prices from sameSLSQP constrainedresponseprogram withupperbound2,notoldLPfloor. Nonconvexquadraticrisks andrestrictedneuralparameterization meanonlylocalapproximation. Covariancesfixed,W2mean-shiftquadraticexactauxGaussianOTspecialcase,notfulldiscreteOT. Risks aredetepisodeestimates,oldstochasticcriticunused.

Allfit/validationdata accounted:5400fit+6600acceptancevalidation steps,newarms;baseline12000normaltraining. Seededcounterfactualrolloutsallcounted,notdynamicsgradientprivilege. Trainingraw/shaped/penalty separated inresults.csv. Modelandoptimizerstate before/afterstored; finitevalidation isnotstatisticalsafetycertificate. Rejectingcandidates doesnotestablishsafety.

## Riskprediction diagnostics
- {"job": "development_DiagReachK2_s180_joint_kl", "mean_abs_cost_prediction_error": [0.1431211832891026, 0.0955497436534401], "mean_reward_prediction_error": 0.019068129220381813, "nonzero_price_cycles": 1, "max_price": 0.0577336613399089, "mean_actual_bias_step": 0.022700742781162263, "beta": 1.2340043046976528}
- {"job": "development_DiagReachK2_s180_joint_ot", "mean_abs_cost_prediction_error": [0.14311824093028352, 0.09553784083857264], "mean_reward_prediction_error": 0.018797907263829964, "nonzero_price_cycles": 1, "max_price": 0.05438621106477179, "mean_actual_bias_step": 0.022700620889663695, "beta": 0.8333333333333333}
- {"job": "development_DiagReachK2_s186_joint_kl", "mean_abs_cost_prediction_error": [0.10881381285487592, 0.08453104310429961], "mean_reward_prediction_error": -0.028739828679054683, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.02774152811616659, "beta": 1.851233739763119}
- {"job": "development_DiagReachK2_s186_joint_ot", "mean_abs_cost_prediction_error": [0.10887453296225573, 0.08400077032513814], "mean_reward_prediction_error": -0.026373494936599257, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.025779065694659948, "beta": 0.8333333333333333}
- {"job": "development_DiagReachK2_s187_joint_kl", "mean_abs_cost_prediction_error": [0.13654450827238349, 0.08022797770988042], "mean_reward_prediction_error": -0.12417039168213244, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.003179287128150463, "beta": 1.9372129168419596}
- {"job": "development_DiagReachK2_s187_joint_ot", "mean_abs_cost_prediction_error": [0.13654407109909897, 0.08022642180222814], "mean_reward_prediction_error": -0.1236818763690907, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.0031841927766799926, "beta": 0.8333333333333333}
- {"job": "development_DiagReachK3_s180_joint_kl", "mean_abs_cost_prediction_error": [0.14834078889238633, 0.09747158058636841, 0.19054128086335947], "mean_reward_prediction_error": -0.6885156748662601, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.021229056119918824, "beta": 1.2340442239802105}
- {"job": "development_DiagReachK3_s180_joint_ot", "mean_abs_cost_prediction_error": [0.14830541783658344, 0.09748821953776655, 0.19039970469393427], "mean_reward_prediction_error": -0.6845484761765619, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.0212151300907135, "beta": 0.8333333333333333}
- {"job": "development_DiagReachK3_s186_joint_kl", "mean_abs_cost_prediction_error": [0.11541535017816042, 0.08354715232850779, 0.1253525533052194], "mean_reward_prediction_error": -0.05630595095152003, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.023648622240871192, "beta": 1.84994779976975}
- {"job": "development_DiagReachK3_s186_joint_ot", "mean_abs_cost_prediction_error": [0.11540974423189308, 0.08355455160521448, 0.12534366777569342], "mean_reward_prediction_error": -0.05662500923741586, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.023708711452782152, "beta": 0.8333333333333333}
- {"job": "development_DiagReachK3_s187_joint_kl", "mean_abs_cost_prediction_error": [0.13876609191803801, 0.08311069279374753, 0.17496363836368395], "mean_reward_prediction_error": -0.20652252102338145, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.0036451268754899503, "beta": 1.8952979153177518}
- {"job": "development_DiagReachK3_s187_joint_ot", "mean_abs_cost_prediction_error": [0.13878554231074142, 0.08311223978554437, 0.1749667710394977], "mean_reward_prediction_error": -0.205917462645913, "nonzero_price_cycles": 0, "max_price": 0.0, "mean_actual_bias_step": 0.0036547920200973747, "beta": 0.8333333333333333}

## Route
Jointarm gates:{'joint_kl': False, 'joint_ot': False};confirmation:HOLD: no5seedexpansion orparametersearch.. Exploratory3trainingseeds;312episodesnottrainingreplicates. Allraw failuresretained. NoPDF/oldFAIL/globaltrainerchanges.

## Final outcome and failure localization
All8smokes and24development jobs verifiedexit0. Eachformalpolicy consumed12000realsteps; jointarms5400fit+6600acceptancevalidation;final312rawdetepisodes separate. Eacharmshaping5,oldbudgets/targetsunaltered. No5seedconfirmation: bothjointarms fail the preregisteredreward/joint gate againstFisher; neitherOT-relative-KLconsistentincrement exists.

Jointarms accepted53/300developmentcycles, rejected247/300. Reconstructedresponsemodels reproduceeachloggedcandidateprediction to1e-8 and savedbesidecheckpoints. All247rejections classifiedasindependentrewardcheckfailure,notpredictedslack,riskunderpredictioncrossingbudget,orfailedrecovery. Constraintsmostlyinactive(2nonzeropricecycles across300). Thus0observedevalviolations cannot be creditedtoactivejointduals orsafeOTtransport. K3seed180 retains taskfailures despitenoviolation.

Validation-new minuspredicted shapedreward averages approximately-.044(K2) and-.316(K3); meanabscostpredictionerrors~.09-.16/channel. This supportsrewardresponseoptimism/acceptance mismatch as an observed bottleneck; itdoesnot separatefittedmodelerror,smallvalidationnoise andrestrictedbiascapacity causally. Actorinstallation andKL/W2 recomputation pass,so noobservedpolicy-installation discrepancy. Dataallocation spends55%ofinteractions onacceptancechecks;baselinestrain onallsteps. Baselinecomparisons arebudget-matched diagnostic systems,not equalcapacity/updatecountablation.

Next single-factor proposal,notlaunched: keepbiasparameterization,griddata,interactionbudget,regularizer/calibration andvalidation fixed; comparecurrentcontinuousquadraticresponse optimizer withfinite-grid joint-objective enumeration onthealreadyobservedcandidates. Firstaudit onsavedcycles whetherquadraticoff-gridcandidates predictgain unavailableonobservedgrid. This targetsresponse/solver selection,not morepenalties orswitchingdeploymentmode. It remainsuntested,not a promisedfix. No native/PDF/oldFAIL changes.

DiagReachK2/ppolag: meanwalltime24.50s includinginit/training/finaleval; meanacceptedoptimizerupdates698.67; meantrainraw/shaped/penalty=[8.034520037305782, 7.442480478666653, 0.5920395586391289].

DiagReachK2/fisher: meanwalltime42.99s includinginit/training/finaleval; meanacceptedoptimizerupdates50.00; meantrainraw/shaped/penalty=[7.0723787669329345, 6.578882693696866, 0.4934960732360681].

DiagReachK2/joint_kl: meanwalltime9.67s includinginit/training/finaleval; meanacceptedoptimizerupdates4.33; meantrainraw/shaped/penalty=[8.01952612269564, 7.290211802806888, 0.7293143198887507].

DiagReachK2/joint_ot: meanwalltime9.48s includinginit/training/finaleval; meanacceptedoptimizerupdates4.00; meantrainraw/shaped/penalty=[8.019159762706005, 7.2900281082050435, 0.7291316545009613].

DiagReachK3/ppolag: meanwalltime26.44s includinginit/training/finaleval; meanacceptedoptimizerupdates713.33; meantrainraw/shaped/penalty=[8.316646744009615, 7.8154976057477406, 0.5011491382618746].

DiagReachK3/fisher: meanwalltime56.57s includinginit/training/finaleval; meanacceptedoptimizerupdates50.00; meantrainraw/shaped/penalty=[7.453874435327445, 7.147434429379299, 0.3064400059481462].

DiagReachK3/joint_kl: meanwalltime8.21s includinginit/training/finaleval; meanacceptedoptimizerupdates4.67; meantrainraw/shaped/penalty=[8.204113660319505, 7.460556360745289, 0.7435572995742162].

DiagReachK3/joint_ot: meanwalltime8.18s includinginit/training/finaleval; meanacceptedoptimizerupdates4.67; meantrainraw/shaped/penalty=[8.203828262369413, 7.461642401695826, 0.7421858606735864].
