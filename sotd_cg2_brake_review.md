# CG2 brake candidate review

Exploratory, fixed-checkpoint comparisons; all complete seeds retained. No SOTA claim.

| Arm / setting | Seeds | Reward mean ± SD | Δ reward vs native | Hard events | Soft-feasible seeds | Joint gate |
|---|---:|---:|---:|---:|---:|---|
| CG2_fdpi_lp_m0.78sched_r2 / K16 pf0.02 std1 brake g>0.15 scales0.5,0 | 3 | 12.145 ± 1.253 | -2.318 (-16.0%) | 1/936 | 2/3 | fail |
| CG2_fdpi_lp_m0.78sched_r2 / K16 pf0.02 std1 brake g>0.2 scales0.5,0 | 3 | 12.251 ± 1.246 | -2.212 (-15.3%) | 2/936 | 2/3 | fail |
| CG2_fdpi_lp_m0.78sched_r2 / K16 pf0.02 std1 brake g>0.3 scales0.5,0 | 3 | 12.217 ± 1.221 | -2.245 (-15.5%) | 2/936 | 2/3 | fail |
| CG2_fdpi_lp_m0.78sched_r2 / K16 pf0.02 std1 brake g>0.5 scales0.5,0 | 3 | 12.311 ± 1.244 | -2.151 (-14.9%) | 2/936 | 2/3 | fail |
| CG2_fdpi_lp_m0.8sched1500k_r2 / K16 pf0.05 std1 brake g>0.3 scales0.5,0 | 3 | 17.000 ± 1.629 | -2.343 (-12.1%) | 5/936 | 1/3 | fail |

## Findings

1. Pooled low hard-event rates cannot establish every-seed soft-budget compliance.
2. Adaptive candidate sweeps are exploratory; risk intervals do not correct selection across settings.
3. Native comparisons use the same checkpoints and canonical reset blocks; evaluator versions stay separate.

Next experiment: Diagnose the failed soft channel and hard-filter fallback on recorded transitions before a new fixed-budget candidate; do not expand the same braking threshold sweep.

Per-seed measurements and confidence bounds are in the accompanying JSON.
