# T-1484: Complete benchmark task dashboard

Status: review

All945pinned benchmark entries are visible:402Safety-Gymnasium tracks and543Safety-CHORES scenarios. The page supports search, benchmark/group/status filters, pagination, full CSV export and per-method/seed expansion. Unadapted, unqueued and failed tasks remain in the denominator. No scientific acceptance is inferred from queue completion.

Changed: all-tasks.html; one navigation entry in index.html andsotd.html. Existing experiments, protocols, scientific results and other dashboard collectors are preserved.

Validation: real Chromium desktop/mobile browser checks; all945rows; CHORES543/Fetch172/SG402/unfrozenSG220filters;48methodcells forCarGoal2; failedcells retained; CSV/JSON/hash/6216-cell accounting; noJavaScript errors. The dataset is refreshed by the existing data publisher.

Operational acceleration:5090nativequeue12to20workers;12liveworkerspreserved,8pendingcellsstarted,zerotrainingrestarts; 2Msteps/312finalepisodes unchanged. Totalformalworkers256atverification. Newpairedfeedbackcohort6fulltrainersrunningseparately; all4operationalgatespassed.

Scientificgoalsremainopen.763inventoryentriesstillawaittheirfullprotocol/adapters. Thispage makes that backlog explicit.


2026-09-11 pixel continuation (Refs: T-1484): realRGB+all-sensor CNN adapter and full170×8×3=4080 matrix deployed. The page explains environment checks, training/load gates and formal training separately. All945 rows remain;10296 total cells,352 frozenSG tracks and593 unfrozen task/scenario entries. Validation:20 behavior/matrix/fleet regressions,eight realdevelopment training+load checks,109dataartifact checks anddesktop/mobile table tests. Science andwhole-benchmark acceptance remainopen.
