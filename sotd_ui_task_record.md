# T-1484: Complete benchmark task dashboard

Status: review

All945pinned benchmark entries are visible:402Safety-Gymnasium tracks and543Safety-CHORES scenarios. The page supports search, benchmark/group/status filters, pagination, full CSV export and per-method/seed expansion. Unadapted, unqueued and failed tasks remain in the denominator. No scientific acceptance is inferred from queue completion.

Changed: all-tasks.html; one navigation entry in index.html andsotd.html. Existing experiments, protocols, scientific results and other dashboard collectors are preserved.

Validation: real Chromium desktop/mobile browser checks; all945rows; CHORES543/Fetch172/SG402/unfrozenSG220filters;48methodcells forCarGoal2; failedcells retained; CSV/JSON/hash/6216-cell accounting; noJavaScript errors. The dataset is refreshed by the existing data publisher.

Operational acceleration:5090nativequeue12to20workers;12liveworkerspreserved,8pendingcellsstarted,zerotrainingrestarts; 2Msteps/312finalepisodes unchanged. Totalformalworkers256atverification. Newpairedfeedbackcohort6fulltrainersrunningseparately; all4operationalgatespassed.

Scientificgoalsremainopen.763inventoryentriesstillawaittheirfullprotocol/adapters. Thispage makes that backlog explicit.
