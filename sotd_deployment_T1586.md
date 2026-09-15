# T-1586 frozen deployment-policy audit

All24 finalpolicies reproduce exact old100det episode seeds at1e-6 absolute reward/cost tolerance andexactsuccess/joint. All48phasejobs exit0; 14976newpairedmodeepisodes plus2400reproductionepisodes. Modelparametersunchanged,0trainingsteps/0traininghours. Per-transitionenvironment RNG hash pairing verified.

|Policy|Mode|Mean costs|Channel violation probabilities|Any violation|Joint|Raw reward|Expected-cost point feasible|
|---|---|---|---|---:|---:|---:|---|
|geometry_DiagReachK2_s180_c5_fisher|det|[5.270202370790335, 5.337294824612447]|[0.0, 0.0]|0.0000|1.0000|8.9534|True|
|geometry_DiagReachK2_s180_c5_fisher|sample|[4.963449070086846, 5.127247613974107]|[0.08012820512820513, 0.04807692307692308]|0.1250|0.7949|7.9469|True|
|geometry_DiagReachK2_s180_c5_original|det|[5.719608157108992, 5.227210301619309]|[0.022435897435897436, 0.0]|0.0224|0.9776|9.3214|True|
|geometry_DiagReachK2_s180_c5_original|sample|[5.61722407127038, 5.06429697229312]|[0.33974358974358976, 0.15064102564102563]|0.4487|0.5032|8.6859|True|
|geometry_DiagReachK2_s186_c5_fisher|det|[5.055888877465175, 5.459360492535127]|[0.0, 0.0]|0.0000|1.0000|8.8012|True|
|geometry_DiagReachK2_s186_c5_fisher|sample|[5.093512974106348, 4.965955015940544]|[0.14102564102564102, 0.07692307692307693]|0.2019|0.6058|7.6507|True|
|geometry_DiagReachK2_s186_c5_original|det|[3.529906396682446, 3.589634290872476]|[0.0, 0.0]|0.0000|0.3526|7.5270|True|
|geometry_DiagReachK2_s186_c5_original|sample|[3.538799169927071, 3.375669612716406]|[0.07051282051282051, 0.08653846153846154]|0.1442|0.2692|6.3093|True|
|geometry_DiagReachK2_s187_c5_fisher|det|[4.751579365669152, 5.2317973130788555]|[0.0, 0.0]|0.0000|1.0000|8.7119|True|
|geometry_DiagReachK2_s187_c5_fisher|sample|[4.64907615001385, 4.648255256888194]|[0.09935897435897435, 0.0641025641025641]|0.1603|0.6955|7.5079|True|
|geometry_DiagReachK2_s187_c5_original|det|[4.813537768828563, 4.8734902158761635]|[0.0, 0.0]|0.0000|1.0000|8.4551|True|
|geometry_DiagReachK2_s187_c5_original|sample|[4.722975035508473, 4.547795125307181]|[0.15064102564102563, 0.15384615384615385]|0.2788|0.3590|7.7521|True|
|geometry_DiagReachK3_s180_c5_fisher|det|[6.36216383255445, 6.193633314890739, 11.459743349980085]|[0.0, 0.0, 0.0]|0.0000|1.0000|9.5858|True|
|geometry_DiagReachK3_s180_c5_fisher|sample|[6.2778223890524645, 5.638051026524642, 10.806297383247278]|[0.1858974358974359, 0.14102564102564102, 0.07371794871794872]|0.2949|0.6410|8.5847|True|
|geometry_DiagReachK3_s180_c5_original|det|[6.327477904466482, 5.758697758882474, 11.033219759280865]|[0.0, 0.0, 0.0]|0.0000|1.0000|9.5086|True|
|geometry_DiagReachK3_s180_c5_original|sample|[6.150485274883417, 5.521965020742172, 10.598290921785892]|[0.23717948717948717, 0.17307692307692307, 0.08333333333333333]|0.3814|0.5224|8.6872|True|
|geometry_DiagReachK3_s186_c5_fisher|det|[6.4665811489789915, 4.892991775121445, 10.259572839125608]|[0.0, 0.0, 0.0]|0.0000|1.0000|9.2680|True|
|geometry_DiagReachK3_s186_c5_fisher|sample|[6.463286795677283, 4.683649201423694, 10.02578877332883]|[0.11858974358974358, 0.022435897435897436, 0.00641025641025641]|0.1346|0.7821|8.4349|True|
|geometry_DiagReachK3_s186_c5_original|det|[6.381212060268108, 5.8752164825415, 11.190553365609585]|[0.0, 0.0, 0.0]|0.0000|1.0000|9.5148|True|
|geometry_DiagReachK3_s186_c5_original|sample|[6.301802755166323, 5.693309278060228, 10.91878752830701]|[0.25, 0.15384615384615385, 0.08653846153846154]|0.3846|0.5801|8.9877|True|
|geometry_DiagReachK3_s187_c5_fisher|det|[6.2841092348098755, 4.985661526521047, 10.079921786601727]|[0.0, 0.0, 0.0]|0.0000|1.0000|8.8304|True|
|geometry_DiagReachK3_s187_c5_fisher|sample|[6.124028705633604, 4.6924125743217955, 9.593345119402958]|[0.18269230769230768, 0.035256410256410256, 0.009615384615384616]|0.2179|0.5513|7.7287|True|
|geometry_DiagReachK3_s187_c5_original|det|[6.522459325117943, 5.337213395497738, 10.758177042007446]|[0.0, 0.0, 0.0]|0.0000|0.9968|8.7514|True|
|geometry_DiagReachK3_s187_c5_original|sample|[6.4323341487309875, 4.77216637134552, 10.033585027242319]|[0.28205128205128205, 0.10256410256410256, 0.035256410256410256]|0.3782|0.3462|8.1607|True|
|shaping_DiagReachK2_s180_c0_ppolag|det|[9.00559847477155, 8.92454293752328]|[1.0, 1.0]|1.0000|0.0000|10.8709|False|
|shaping_DiagReachK2_s180_c0_ppolag|sample|[8.773327868718367, 8.726383375815857]|[1.0, 1.0]|1.0000|0.0000|10.3539|False|
|shaping_DiagReachK2_s180_c5_ppolag|det|[5.690125443996528, 5.551710597979716]|[0.0, 0.0]|0.0000|1.0000|9.4023|True|
|shaping_DiagReachK2_s180_c5_ppolag|sample|[5.675052985166892, 5.503505758750133]|[0.2403846153846154, 0.0641025641025641]|0.2660|0.7340|9.1399|True|
|shaping_DiagReachK2_s186_c0_ppolag|det|[10.06615270101107, 9.225974440574646]|[1.0, 1.0]|1.0000|0.0000|11.1340|False|
|shaping_DiagReachK2_s186_c0_ppolag|sample|[9.985129591746208, 9.111849919343607]|[1.0, 1.0]|1.0000|0.0000|10.9824|False|
|shaping_DiagReachK2_s186_c5_ppolag|det|[5.471490051501837, 5.772151477825948]|[0.0, 0.0]|0.0000|1.0000|9.3733|True|
|shaping_DiagReachK2_s186_c5_ppolag|sample|[5.438741576977265, 5.722932684115874]|[0.08333333333333333, 0.11217948717948718]|0.1827|0.8173|9.2091|True|
|shaping_DiagReachK2_s187_c0_ppolag|det|[8.825528505520943, 8.357437589229681]|[1.0, 1.0]|1.0000|0.0000|10.7635|False|
|shaping_DiagReachK2_s187_c0_ppolag|sample|[8.790571515376751, 8.290468550645388]|[1.0, 1.0]|1.0000|0.0000|10.5820|False|
|shaping_DiagReachK2_s187_c5_ppolag|det|[5.534415998519996, 5.456764633838947]|[0.0, 0.0]|0.0000|1.0000|9.3138|True|
|shaping_DiagReachK2_s187_c5_ppolag|sample|[5.514849870632856, 5.383620039010659]|[0.14423076923076922, 0.035256410256410256]|0.1603|0.8397|9.0621|True|
|shaping_DiagReachK3_s180_c0_ppolag|det|[9.485512125186432, 8.4737536020768, 16.852600287168453]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.8150|False|
|shaping_DiagReachK3_s180_c0_ppolag|sample|[9.337814590869806, 8.30465978384018, 16.537000879263267]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.5763|False|
|shaping_DiagReachK3_s180_c5_ppolag|det|[7.095057035103823, 6.0103388505104265, 12.005395760902992]|[0.9006410256410257, 0.0, 0.0]|0.9006|0.0994|9.7235|False|
|shaping_DiagReachK3_s180_c5_ppolag|sample|[6.987614671389262, 5.919585504592994, 11.806341611422026]|[0.48717948717948717, 0.10256410256410256, 0.19230769230769232]|0.5321|0.4647|9.2750|True|
|shaping_DiagReachK3_s186_c0_ppolag|det|[8.47530967149979, 7.953195712505242, 15.321840011156523]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.5556|False|
|shaping_DiagReachK3_s186_c0_ppolag|sample|[8.338775284779377, 7.8746165205270815, 15.10877441137265]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.3360|False|
|shaping_DiagReachK3_s186_c5_ppolag|det|[6.787689193701133, 6.145429715132102, 11.832314274249933]|[0.003205128205128205, 0.0, 0.0]|0.0032|0.9968|9.7903|True|
|shaping_DiagReachK3_s186_c5_ppolag|sample|[6.757231359298412, 6.085580540009034, 11.740237822899452]|[0.22435897435897437, 0.03205128205128205, 0.04487179487179487]|0.2372|0.7628|9.5627|True|
|shaping_DiagReachK3_s187_c0_ppolag|det|[8.526751576325832, 7.533196505827782, 14.953282762796452]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.4742|False|
|shaping_DiagReachK3_s187_c0_ppolag|sample|[8.450152534704943, 7.444842343146984, 14.790728682126755]|[1.0, 1.0, 1.0]|1.0000|0.0000|10.2519|False|
|shaping_DiagReachK3_s187_c5_ppolag|det|[6.700074406770559, 6.422960244692289, 12.023015813949781]|[0.0, 0.125, 0.003205128205128205]|0.1250|0.8750|9.7994|True|
|shaping_DiagReachK3_s187_c5_ppolag|sample|[6.63985793865644, 6.35280461036242, 11.88738923195081]|[0.2467948717948718, 0.32371794871794873, 0.15384615384615385]|0.4487|0.5513|9.5671|True|

## Preselected K3s180c5 policy
- det: mean costs[7.095057035103823, 6.0103388505104265, 12.005395760902992],95%CI[[7.086773895549142, 7.103340174658503], [6.003232759742827, 6.0174449412780255], [11.992749187400573, 12.018042334405411]]; channelviolations[0.9006410256410257, 0.0, 0.0],joint0.09935897435897435,rawreward9.723466109187926.
- sample: mean costs[6.987614671389262, 5.919585504592994, 11.806341611422026],95%CI[[6.920936722160175, 7.054292620618349], [5.8687203318578645, 5.970450677328123], [11.715336005659156, 11.897347217184896]]; channelviolations[0.48717948717948717, 0.10256410256410256, 0.19230769230769232],joint0.46474358974358976,rawreward9.275022487421873.
Pairedsample-minus-det: {"policy": "shaping_DiagReachK3_s180_c5_ppolag", "difference": "sample-minus-det", "cost_difference_mean": [-0.10744236371456048, -0.09075334591743274, -0.19905414948096642], "cost_difference_ci95": [[-0.17276860789301135, -0.04211611953610961], [-0.14128699608739614, -0.040219695747469336], [-0.28906414845353484, -0.109044150508398]], "reward_difference": -0.4484436217660553, "reward_difference_ci95": [-0.48177671079152196, -0.4151105327405886], "joint_difference": 0.36538461538461536, "joint_difference_bootstrap_ci95": [0.3076923076923077, 0.42628205128205127], "violation_difference": [-0.41346153846153844, 0.10256410256410256, 0.19230769230769232], "violation_difference_bootstrap_ci95": [[-0.47435897435897434, -0.3525641025641026], [0.07051282051282051, 0.13782051282051283], [0.15384615384615385, 0.23717948717948717]]}

## Interpretation
Eachrow conditions on onefrozenfinalactor;312episode samplesestimate thatpolicy,not312trainingreplicates. Fullcostquantiles,pairuncertainty andWilsonintervals are in findings.json. Expectedmean-cost feasibility andper-episodeviolationprobability differ; mean feasibility doesnotimply safeepisodes. Modeeffects may differ acrosspolicies andbothremainreported; we donotselectthebetter-scoringmode.

Officialdet meansGaussianmu,thenenvironmentclipanddynamics tanh. samplemode calls originalGaussianactor.sample,withseparateTorchactionstream andindependentNumPyenvironmentstream. Gaussianproposal logprob only describespreclipproposal. Everyrawproposal,executedaction,rawreward,cost,policyhash is stored.

Lasttrainingbatch refers topre-final-updateactor andfinite sample; thisaudit isolatesmodegap at thesamefinalactor,notthatwholehistoricalgap. Itdoesnotmeasurelastupdateeffect independently orcertifyrisk calibration. Seealgebra_and_contract.md forbothdeployment-kernelroutes andnonconvexsafesupport counterexample. Neitherroutechosen; officialevaluationunchanged; newjointOTvsKLprotocol notstarted. Old24trainingconclusions,FAIL,PDF/DERIVATIONunchanged.

## Verified / excluded / unresolved mechanisms
Verified: at fixed finalparameters andpairedinitial/environmentnoise, deployedmodechangescost/reward/risk. Across24policies, sample-minus-det joint ispositive1,negative17,tied6; rawreward islowerfor all24. These counts describe thisfixedpolicycollection andarenot independenttraining-levelsignificance. All24policies retained,notjustpreselectedexample.

Det has17/24 point-estimateexpected-feasible policies and14/24 withzeroobservedany-violation; sample has18/24point-estimateexpected-feasible but0/24zeroobservedany-violation. Neitherpointestimate norzeroobservations establishtrueguarantees. The preselectedpolicy samplexmean6.9876 has95%CI[6.9209,7.0543],crossing7; itsanyepisodeviolation.5321. Detxmean7.0951 hasCI[7.0868,7.1033],xviolation.9006. Sample-minus-det xcost=-.10744,paired95%CI[-.17277,-.04212]; rawrewarddifference=-.44844. Modegap ismeasured,notchosenasbetterdeployment.

Excluded for thiscomparison: differentweights oroptimizerupdates,incorrectoldseed reconstruction,environment RNG depletionbysampling,missingproposalclip accounting. Actualmodecomparison usesidenticalfinalactorsandnoise; itdoesnotuseaveragedtrainingepisodes.

Unresolved: oldlastbatchx6.321 vsfinalsamplemean6.9876 also differs. Thatremaininggap caninclude lastactorupdate andfinitebatchvariance; currentstudyhasnotseparatedthose. The frozenmodegap alonecannotexplainentirehistoricaltraining-versusdetdifference orprovewhichriskpredictorfailed. Officialdetstandard unchanged. Chooseactualkernel T(q) andrisksemantics beforefuturejointOT/KLprotocol; do notswitch tosample toclaimrepair.
