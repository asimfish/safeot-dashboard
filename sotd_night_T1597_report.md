# Night campaign: verified results, no performance promotion

Prepared 2026-09-17T09:03:35.106365+08:00; task T-1597. Publication catch-up for completed A/C/T1595/T1596. Prior failures and HOLD decisions remain unchanged. No new training in this task.

## Receipt-backed execution
42 development jobs: A6 + C6 + pathwise24 + uniform-KL6 = 504,000 actual training interactions. Including receipt-backed smoke/replay yields 54 successful jobs and 511,680 trace-counted training interactions, 157,248 final evaluation steps, and 5,324,160 privileged model transitions. Failed/missing-receipt auxiliary runs and checker interactions are excluded from this successful-receipt ledger, not erased or assigned zero. Original import failures remain engineering failures; an auxiliary 480-step run lacked shell exit receipt and is reported separately.

Pathwise passed the independent original-environment closed-loop/episodic-gradient checker and eight complete transaction smoke checks. All 24 development jobs exited 0 and passed final source/step/transaction/trace verification. This is privileged synthetic diagnostic evidence, not a fair model-free gain.

## Pathwise results (three training-seed means)
|Task|Arm|Raw reward|Joint|Any-event|
|---|---|---:|---:|---:|
|DiagReachK2|SM|9.178330|0.991453|0.008547|
|DiagReachK2|ST|9.022716|0.983974|0.016026|
|DiagReachK2|DM|8.994082|0.994658|0.005342|
|DiagReachK2|DT|9.431801|0.950855|0.049145|
|DiagReachK3|SM|9.423433|0.997863|0.002137|
|DiagReachK3|ST|9.445710|0.996795|0.003205|
|DiagReachK3|DM|9.441518|0.966880|0.033120|
|DiagReachK3|DT|9.588166|0.942308|0.057692|

SM/ST use sample model kernel; DM/DT use deterministic model kernel. M is sample mean cost; T constrains all 20 sampled scenario costs. Every arm has at least one final observed event; none passes the preregistered all-seed safety/reward advancement gate. This refutes sufficiency of these tested configurations, not the full family of pathwise methods or SafeOT. No W2/fresh-seed expansion.

## Uniform KL eligibility
The only change masked candidates whose auxiliary old||new Gaussian KL exceeded 0.01001; all real screens/optimizer transactions stayed unchanged. Exact two-cycle control replay passed both tasks. Six jobs exited 0. The installed-KL invariant held but performance did not.
|Task|Raw reward|Joint|Any-event|Reward delta vs matched control|
|---|---:|---:|---:|---:|
|DiagReachK2|8.759747|0.978632|0.021368|-0.382753|
|DiagReachK3|8.510612|0.580128|0.091880|-1.060373|

HOLD: no radius sweep; geometrical eligibility does not establish deterministic-policy safety. Per-seed costs/events/excess and effective update counts are preserved in the CSV.

## Earlier A/C results
|Branch|Task|Seed|Raw reward|Joint|Any-event|
|---|---|---:|---:|---:|---:|
|A|DiagReachK2|180|9.332338|0.926282|0.073718|
|A|DiagReachK2|186|9.024217|1.000000|0.000000|
|A|DiagReachK2|187|8.994915|0.993590|0.006410|
|A|DiagReachK3|180|9.459672|0.987179|0.012821|
|A|DiagReachK3|186|9.717847|0.971154|0.028846|
|A|DiagReachK3|187|9.384863|1.000000|0.000000|
|C|DiagReachK2|180|8.978002|0.993590|0.006410|
|C|DiagReachK2|186|9.205967|0.996795|0.003205|
|C|DiagReachK2|187|9.191045|1.000000|0.000000|
|C|DiagReachK3|180|9.577720|0.993590|0.006410|
|C|DiagReachK3|186|9.579003|0.961538|0.038462|
|C|DiagReachK3|187|9.371084|0.974359|0.025641|

Both branches fail all-seed event-free advancement. C actual allocation is 7200/2880/1920, correcting its stale original effective-config label without changing old files. Original inner recovery=0 does not imply outer recovery=0.

## Wall time is not worker-hours
Receipt audit as of 2026-09-16T23:02:26.388263+00:00: successful-worker interval union 0.871327 h; summed worker-hours 2.855046 h. Both include startup/serialization/evaluation and are not pure gradient-compute measurements. Eight effective experiment hours were **not achieved**. Uncovered intervals cannot be separated exactly into implementation/failed/idle time from these receipts. Further empty monitoring turns add no experimental activity.

## Boundaries and next decision
312 evaluation episodes estimate each frozen policy; three training seeds remain only three training repetitions. No observed events do not imply zero risk. All four bounded branches are held; native/VLA and manuscript claims are unchanged. Next work must be a new bounded hypothesis grounded in logs, not repeated status checks or radius/seed search.
