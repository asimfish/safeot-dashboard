# T-1591 frozen candidate surrogate-gap decomposition

Evaluation-only synthetic mechanism evidence. T1590 remains HOLD. No new training, actor updates, optimizer updates, policy selection or radius search. All 30 anchors and all negative results retained.

30 formal anchors × 10 kernels × 128 fresh paired episodes = 38400 episodes / 460800 steps. Separate replay 2880 steps; smoke plus replay 4032 steps. Valid smoke/formal/replay total 467712 evaluation steps; two failed replay attempts add 96 steps (8 episodes), grand total 467808 steps, zero training steps. All source checkpoint hashes unchanged; original selection and finite-horizon LR replay passed.

Three trained seeds per task, five fixed anchors per seed. 95% intervals below are 512 paired whole-episode bootstrap intervals, LOO recentered with repeated draws, conditional on frozen training data/policies. They do not quantify training-seed population uncertainty. Gtrain is held fixed.

## Seed-level shaped gain decomposition

|Task|Metric|Seed|Gtrain|GholdLR|Gsample|Gdet|T [95%]|L [95%]|K [95%]|
|---|---|---:|---:|---:|---:|---:|---|---|---|
|DiagReachK2|KL|180|1.8490|0.2421|0.2287|0.0997|1.6069 [1.4775, 1.7432]|0.0134 [-0.1102, 0.1259]|0.1290 [0.0729, 0.1944]|
|DiagReachK2|W2|180|1.8780|0.2353|0.2253|0.0882|1.6427 [1.5025, 1.7810]|0.0100 [-0.1190, 0.1295]|0.1370 [0.0795, 0.2044]|
|DiagReachK2|KL|186|1.2271|0.2093|0.1076|0.1303|1.0177 [0.9080, 1.1263]|0.1018 [0.0017, 0.1969]|-0.0227 [-0.0653, 0.0297]|
|DiagReachK2|W2|186|1.4092|0.2321|0.0812|0.0783|1.1770 [1.0339, 1.3117]|0.1510 [0.0299, 0.2731]|0.0029 [-0.0494, 0.0694]|
|DiagReachK2|KL|187|2.7625|0.8805|0.4727|-0.1794|1.8820 [1.5656, 2.1737]|0.4078 [0.1474, 0.6841]|0.6521 [0.5555, 0.7384]|
|DiagReachK2|W2|187|2.6566|0.8064|0.4307|-0.1025|1.8502 [1.5551, 2.1150]|0.3758 [0.1302, 0.6303]|0.5331 [0.4490, 0.6072]|
|DiagReachK3|KL|180|1.7012|0.6395|0.5143|0.4032|1.0617 [0.9088, 1.2230]|0.1252 [0.0073, 0.2443]|0.1111 [0.0399, 0.1784]|
|DiagReachK3|W2|180|1.7479|0.6759|0.5421|0.3889|1.0721 [0.9178, 1.2433]|0.1338 [0.0096, 0.2550]|0.1532 [0.0812, 0.2221]|
|DiagReachK3|KL|186|1.3565|0.3151|0.2698|0.1019|1.0414 [0.8935, 1.1677]|0.0453 [-0.0776, 0.1786]|0.1679 [0.1221, 0.2161]|
|DiagReachK3|W2|186|1.6658|0.3680|0.3041|0.0433|1.2978 [1.0895, 1.4633]|0.0640 [-0.1021, 0.2559]|0.2608 [0.2039, 0.3179]|
|DiagReachK3|KL|187|2.4293|0.4664|0.3801|-0.2901|1.9629 [1.7930, 2.1559]|0.0863 [-0.0531, 0.2207]|0.6703 [0.5866, 0.7478]|
|DiagReachK3|W2|187|2.4671|0.5145|0.4016|-0.2560|1.9526 [1.7742, 2.1556]|0.1128 [-0.0398, 0.2675]|0.6577 [0.5740, 0.7351]|

T=Gtrain−GholdLR; L=GholdLR−Gsample; K=Gsample−Gdet. Sum identity checked for shaped/raw/penalty and every cost channel. The L term combines finite-step surrogate/occupancy error and finite evaluation noise; it is not critic calibration.

## Magnitude ranking and sign stages

- DiagReachK2 KL: median absolute T/L/K={'T': 1.4226938732959338, 'L': 0.11896312472254764, 'K': 0.3160516321659088}; rank=['T', 'K', 'L']; of 15 anchors positive-train/nonpositive holdLR/sample/det counts={'GholdLR': np.int64(2), 'Gsample': np.int64(3), 'Gdet': np.int64(12)}; sample-positive/det-nonpositive=9 (both directional CIs separated from zero: 9). Mean gains={'Gtrain': 1.9462133390245333, 'GholdLR': 0.4439749841056108, 'Gsample': 0.2696671462307374, 'Gdet': 0.01684481849273046, 'T': 1.5022383549189227, 'L': 0.17430783787487347, 'K': 0.2528223310907682, 'mean_only': 0.27400637784351906, 'std_only': -0.003648807480931282, 'interaction': -0.0006904411440094312}.
- DiagReachK2 W2: median absolute T/L/K={'T': 1.4912255838415567, 'L': 0.15247832399089106, 'K': 0.3016853332519531}; rank=['T', 'K', 'L']; of 15 anchors positive-train/nonpositive holdLR/sample/det counts={'GholdLR': np.int64(2), 'Gsample': np.int64(3), 'Gdet': np.int64(12)}; sample-positive/det-nonpositive=9 (both directional CIs separated from zero: 8). Mean gains={'Gtrain': 1.9812613762639213, 'GholdLR': 0.42460798366437347, 'Gsample': 0.24569842666387562, 'Gdet': 0.021351803839206696, 'T': 1.5566533925995474, 'L': 0.1789095570004979, 'K': 0.2243466297785441, 'mean_only': 0.24980853150288262, 'std_only': -0.004021022344628969, 'interaction': -8.90954087177912e-05}.
- DiagReachK3 KL: median absolute T/L/K={'T': 1.1128582942178002, 'L': 0.1130665257181655, 'K': 0.5552815198898315}; rank=['T', 'K', 'L']; of 15 anchors positive-train/nonpositive holdLR/sample/det counts={'GholdLR': np.int64(0), 'Gsample': np.int64(0), 'Gdet': np.int64(12)}; sample-positive/det-nonpositive=12 (both directional CIs separated from zero: 12). Mean gains={'Gtrain': 1.8289802203964118, 'GholdLR': 0.4736587121182982, 'Gsample': 0.3880644006033738, 'Gdet': 0.07166380981604259, 'T': 1.3553215082781136, 'L': 0.08559431151492436, 'K': 0.31640059078733124, 'mean_only': 0.36001436909039813, 'std_only': 0.027706648502498866, 'interaction': 0.00034331157803535467}.
- DiagReachK3 W2: median absolute T/L/K={'T': 1.106087499448793, 'L': 0.10956528977273738, 'K': 0.6097431778907776}; rank=['T', 'K', 'L']; of 15 anchors positive-train/nonpositive holdLR/sample/det counts={'GholdLR': np.int64(1), 'Gsample': np.int64(0), 'Gdet': np.int64(12)}; sample-positive/det-nonpositive=12 (both directional CIs separated from zero: 11). Mean gains={'Gtrain': 1.9602845109701856, 'GholdLR': 0.5194536810681908, 'Gsample': 0.41593652466932934, 'Gdet': 0.05872300863265991, 'T': 1.440830829901995, 'L': 0.10351715639886144, 'K': 0.35721351703008014, 'mean_only': 0.3727260733644167, 'std_only': 0.0417213033263882, 'interaction': 0.0014891652390360832}.

Signed sums, absolute sums, medians by seed, and their cancellations are explicitly retained in seed_decomposition.csv. Raw/shaped/penalty and all cost decompositions with intercept errors are in anchor_decomposition.csv; risk mean/quantiles/event/excess/success/joint are in risk_metrics.csv. Neither cycles nor episodes are treated as independent training replicas.

## Variance intervention

- DiagReachK2 KL: full sample gain positive but mean-only nonpositive 1/15; these also det nonpositive 1/15. Mean-only / std-only / interaction mean gains: 0.27401 / -0.00365 / -0.00069.
- DiagReachK2 W2: full sample gain positive but mean-only nonpositive 1/15; these also det nonpositive 1/15. Mean-only / std-only / interaction mean gains: 0.24981 / -0.00402 / -0.00009.
- DiagReachK3 KL: full sample gain positive but mean-only nonpositive 0/15; these also det nonpositive 0/15. Mean-only / std-only / interaction mean gains: 0.36001 / 0.02771 / 0.00034.
- DiagReachK3 W2: full sample gain positive but mean-only nonpositive 0/15; these also det nonpositive 0/15. Mean-only / std-only / interaction mean gains: 0.37273 / 0.04172 / 0.00149.

Hybrid wrappers evaluate both networks at their own visited states; they are functional interventions, not directly installable actor parameters. Full gain = mean-only + std-only + interaction verified. Std-only changes no deterministic actions, but backbone changes can jointly affect mu and sigma.

## Risk and prior audit

Mean-feasible but eventful kernel/anchor cases: 224 of 300 (all listed in findings.json); det-tail cases for inner candidates: 10 of 60. Full per-channel risk and inner utilization retained, not replaced by aggregate cost.

Prior 1800 candidates: 18 cost-near-active within 1e-3; max violation under 1e-5. Scale1 215/300 four-episode middle-minus-old shaped gains negative while all predicted gains positive. This is finite-sample descriptive evidence. The stated .74–.77 utilization is reproduced as the median of the maximum channel Csur/B; averaging channels first gives .68–.70. Both definitions are now explicit.

Usage audit: {"K2_KL": {"median_max_channel": 0.7432320853013651, "median_mean_channel": 0.6815382093151838, "median_per_channel": [0.7127375379886447, 0.679057985233338]}, "K2_W2": {"median_max_channel": 0.7447560222684473, "median_mean_channel": 0.6848012298060026, "median_per_channel": [0.7082768698713948, 0.6758357610852253]}, "K3_KL": {"median_max_channel": 0.7733801465776652, "median_mean_channel": 0.6976230636614966, "median_per_channel": [0.740794834731996, 0.6920988034320921, 0.6716570707875866]}, "K3_W2": {"median_max_channel": 0.7715610215154757, "median_mean_channel": 0.6961661482724579, "median_per_channel": [0.7399731247877029, 0.6923159454200584, 0.6690518202749764]}}

## Interpretation and one next modification

The largest median-absolute term is T in all four task/metric groups (1.106–1.491 versus K 0.302–0.610 and L 0.110–0.152). Every seed-averaged T interval is positive. This is optimizer-selected in-sample optimism/generalization evidence, not proof that time-centering is biased or that an estimator repair will improve learning. Most of the mean shaped T is the penalty-return component: approximately 89–93%, with raw-return T only 0.109–0.180. Shaping is held fixed; this does not imply removing it improves safety.

Propose ONE next estimator change, not implemented here: in a new copy of joint_solver.py, at finite_targets/centered before constructing reward gradient D and evaltheta gain, replace the time-only reward baseline with an episode-cross-fitted state/time/remaining-budget conditional baseline trained on the SAME undiscounted shaped MC return. For each held-out episode fold, baseline predictions must use only other episodes and exclude its actions/noise; use the resulting advantage consistently for both the reward direction and LR objective. Keep cost surrogate, KL/W2 distance, shaping5, original budgets, external excess screen and official det unchanged. This is one reward-advantage estimation intervention, not a policy-kernel switch, two-bias response model, or new safety proof. Define a bounded fixed fitting recipe in a future protocol; do not tune it on this bank or use these fresh diagnostic rollouts for learning. Within-batch cross-fitting adds fitting compute but zero environment interactions; with only 20 episodes a conditional baseline may underfit or be unstable and needs a separate correctness/variance gate. Extra samples, if later needed, must be charged equally and preregistered. These finite-H MC targets transfer only where complete episodic reward/budget data exist; native/VLA validity is unestablished.

A deployment mismatch remains: sample gain positive and det gain nonpositive in 42/60 anchor/candidate pairs, 40 with both directional conditional intervals away from zero. Variance-only intervention explains only 2/42 by the operational criterion full-sample gain positive, mean-only nonpositive and det nonpositive. Thus neither “only std was optimized” nor “only the deployment kernel caused failure” fits the whole bank. No additional modification or training is initiated.

## Artifacts and limits

protocol.md; manifest.json; bank.json; existing_audit.json; verification.json; anchor_decomposition.csv; seed_decomposition.csv; risk_metrics.csv; findings.json; gap_components.png/svg; jobs/*/{receipt.json,result.json,episodes.jsonl,*_contributions.npz,kernel.npz}. Raw trace arrays retain proposals, executed clip actions, original Gaussian logprob, visited states, action noise, environment noise and episode seeds.

Official deterministic evaluation semantics remain unchanged. Mean budget feasibility is not zero episode risk. No OT advantage, SOTA, native-task or VLA claim is supported.

## Replay failure and precision accounting

Initial formal_21 and first retry failed the unchanged 1e-6 summary tolerance before any new bank sampling. Both failed in the first old-policy four-episode replay (48 steps each). The diagnostic trace used np.r_ with a float32 cost array, rounding step rewards; reconstructing episode rewards from that rounded trace and reducing in float64 differed from the original episode accumulator plus float32 summary by up to 1.90735e-6. Final retry uses the actual environment episode accumulator and original np.r_/mean reduction. It passes without relaxing tolerance; all original failure logs and exit1 receipts remain. The fresh-bank rollout code/data precision is unchanged across the 30 successful jobs. precision_audit.py independently recomputes reward algebra on recorded transitions (no env.step/new samples) and bounds the tiny stored-return rounding. It is a numerical representation limit, not a learning effect.

The initial detached controller has exit1, the isolated retry exits0, and final synthesis is separately verified. This is not relabeled as an unbroken exit0 campaign. All 30 formal anchor receipts are now verified; two independent smoke anchors also passed. No completed bank was repeated.

## Raw return and shaping-penalty decomposition (three seed means)

|Task|Metric|Channel|Gtrain|GholdLR|Gsample|Gdet|T|L|K|
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
|DiagReachK2|KL|raw|0.10246|-0.00618|-0.00704|0.02306|0.10863|0.00087|-0.03010|
|DiagReachK2|KL|penalty|-1.84375|-0.45015|-0.27671|0.00622|-1.39360|-0.17344|-0.28292|
|DiagReachK2|W2|raw|0.12095|-0.00108|-0.00164|0.03143|0.12203|0.00056|-0.03307|
|DiagReachK2|W2|penalty|-1.86031|-0.42568|-0.24734|0.01007|-1.43463|-0.17835|-0.25741|
|DiagReachK3|KL|raw|0.22429|0.08051|0.08375|0.07866|0.14378|-0.00324|0.00509|
|DiagReachK3|KL|penalty|-1.60469|-0.39315|-0.30431|0.00700|-1.21154|-0.08884|-0.31131|
|DiagReachK3|W2|raw|0.27065|0.09055|0.09472|0.07237|0.18010|-0.00417|0.02235|
|DiagReachK3|W2|penalty|-1.68963|-0.42890|-0.32122|0.01365|-1.26073|-0.10768|-0.33487|

## Inner mean slack with observed det events

|Task|Metric|Seed|Cycle|max inner Csur/B|Det P(any)|
|---|---|---:|---:|---:|---:|
|DiagReachK2|KL|180|12|0.92163|0.59375|
|DiagReachK2|W2|180|12|0.94613|0.84375|
|DiagReachK2|KL|180|18|0.94705|0.38281|
|DiagReachK2|W2|180|18|0.94697|0.34375|
|DiagReachK2|KL|180|24|0.89274|0.00781|
|DiagReachK2|W2|180|24|0.89193|0.00781|
|DiagReachK3|KL|186|18|0.93047|0.97656|
|DiagReachK3|W2|186|18|0.95858|1.0|
|DiagReachK3|KL|187|12|0.7206|0.01562|
|DiagReachK3|W2|187|12|0.70787|0.01562|

These ten cases include K3 seed187 cycle12 with inner utilization .708/.721 yet 2/128 deterministic episodes exceeding a budget. Cost intercept and surrogate-vs-rollout differences are separately available; neither mean slack nor finite observed zero events is a safety certificate.

Stored float32 reward trace precision audit: maximum absolute episode shaped/raw/penalty discrepancies versus independent recorded-transition reward algebra were 1.999e-6 / 1.999e-6 / 1.938e-6. This is far below reported mechanism differences; no tolerance was relaxed to pass original selection replay.

## Homepage persistence audit

The real producer dashboard_push.py:651–653 reads experiments/safeot_dual/progress_feed.json, owner T-1484. Scope was expanded before an additive T1591 source entry; all 35 prior source/remote entries and owner remain. Latest removal traced to 8184ddf (T-1484 dashboard claim alignment), which explicitly deleted T1590 from the generated feed. Merely editing the data-branch JSON would not persist through the producer. This task records both source hashes and publishes the source-backed feed without changing status/gap_plan or the producer code. Future deliberate edits by another owner can still alter it; no claim of immunity to future overwrites.
