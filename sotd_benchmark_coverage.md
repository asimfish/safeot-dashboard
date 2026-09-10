# 完整基准覆盖核对

更新时间：2026-09-10T21:13:32.865216+08:00

当前主线：Safety-Gymnasium；SafeVLA所用Safety-CHORES。完整覆盖是五目标的必要条件，不能代替奖励/安全优势检验。

| 基准 / 系列 | 官方任务配置或场景数 | 含观察/版本的待覆盖数 | 有旧证据指针 | 完整矩阵验收 |
|---|---:|---:|---:|---|
| Safety-CHORES / FetchType | 172 | 172 | 0 | 未完成 |
| Safety-CHORES / ObjectNavType | 200 | 200 | 200 | 未完成 |
| Safety-CHORES / PickupType | 171 | 171 | 0 | 未完成 |
| Safety-Gymnasium / Registry / Run | 0 | 10 | 0 | 未完成 |
| Safety-Gymnasium / Safe Isaac Gym / Multi-Agent | 6 | 6 | 0 | 未完成 |
| Safety-Gymnasium / Safe Isaac Gym / Single-Agent | 6 | 6 | 0 | 未完成 |
| Safety-Gymnasium / Safe Multi-Agent / MultiGoal | 6 | 30 | 0 | 未完成 |
| Safety-Gymnasium / Safe Multi-Agent / Velocity | 8 | 8 | 0 | 未完成 |
| Safety-Gymnasium / Safe Navigation | 60 | 120 | 15 | 未完成 |
| Safety-Gymnasium / Safe Velocity | 6 | 12 | 5 | 未完成 |
| Safety-Gymnasium / Safe Vision | 105 | 210 | 0 | 未完成 |

Safety-Gymnasium：官方表格197个配置；另保留14个注册配置，其中9个MultiGoal配置有文档/实现差异。共402个观察/版本轨道。Base、Debug和Gymnasium API转换别名不作为独立任务。

Safety-CHORES：200 ObjectNav +171 Pickup +172 Fetch =543场景/策略，三类官方最大步数均600。旧Dual ObjectNav评测396/400有效、196/200成对完成；四个初始化失败保留。minival名称不等于抽样：已核对其200个ID正好等于完整发布清单。

最低矩阵草案：每个任务/轨道覆盖3个SafeOT软/中/硬工作点和2个对照、3个独立训练种子。SG共有6030个训练+终档评测槽；CHORES共有8145个场景评测槽（每个任务类型15个策略，共45个策略）。这些是待冻结的最低工作量，不是已启动任务数，也不是完整SOTA比较器数量。

执行顺序：
- 30109 + aliyun: audit vector Navigation/Velocity/Run adapters then complete all robots and difficulties
- 30314 GPUs0-5: finish current VLA cohort; validate Pickup/Fetch models and full543 scenario evaluation
- separate fresh cohorts: visual, multi-agent and Isaac adapters; never alter existing frozen jobs

验收约束：
- Source correction: the earlier afc6a34 snapshot simplifies task definitions. This v2 inventory pins the verified official main ae966e5. The old inventory and failed operational attempt remain archived; no formal full-suite training used them.
- 197 counts documented task/robot/difficulty configurations, not training runs. Vision observations and velocityv0/v1 remain separate tracks.
- 14 additional registry configurations: Run0 x5robots and MultiGoal x3levels xCar/Doggo/Racecar. The latter9 conflict with the two documented multi-agent robots and block whole-suite closure.
- 402 Safety-Gymnasium tracks and543 Safety-CHORES scenarios are different units; no combined percentage.
- Zero qualified new-matrix tasks means the new whole-suite protocol has not been frozen/audited, not that all historical experiments are absent or invalid.
- Draft minimum has5method/operating-point slots x3training seeds. Multi-algorithm and finer epsilon sweeps add cells; full SOTA comparator set still requires per-family literature/protocol audit.
- Do not use development-exposed evaluation scenes as a fresh held-out claim; report full official suite plus a separately frozen generalization evaluation.
- Do not merge changed constraint semantics, hard thresholds, cost scaling, horizons, model selection or simulator versions into native-benchmark comparisons.

完整任务见 sotd_benchmark_tasks.csv；逐任务/方法/种子缺口见 sotd_benchmark_backlog.csv；所有未适配、失败、缺种子和协议不一致项保留，禁止缩小分母。现有冻结队列继续，补齐协议后按完整系列派发。

[Safety-Gymnasium官方目录](https://github.com/PKU-Alignment/safety-gymnasium/tree/ae966e511b9927f06b39c727ca5c650136a4e696)；[SafeVLA官方评测清单](https://github.com/PKU-Alignment/SafeVLA/tree/2aa82559d272b5f888e53433e258914057f15bed/benchmark)
