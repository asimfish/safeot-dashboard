# T1593：奖励目标对齐 2×2 的有界结果

**判决：HOLD_OBJECTIVE_RECIPE。关闭本轮固定配方，不扩种子或搜索。**

16 烟测、48 开发、12 独立机制锚点全部 exit 0，12 个 SS 对照完整精确回放。共 864528 次环境交互，含单列的 144 步原始奖励核验；其中开发梯度探索仅 288000 步。下列均值按三个训练种子汇总，312 回合不是训练重复。

## 直接结论

1. 外层 reward key 没有产生本轮路径差异：24 对训练的完整交互轨迹、决策、最终 actor/optimizer 状态及评估完全一致。全部 2696 个无观察事件的候选筛选样本，raw 与 shaped 均值相同（惩罚为零）；零次选择/验收翻转。重复 outer 配对轨迹不当作独立证据。这不表示 shaping 普遍无效，PPO 始终保留 shaping5。
2. 内层 raw 改动产生不同候选和训练效果。K2 两个 metric 奖励和联合成功率均下降；K3 奖励上升，其中 KL 出现事件、W2 保持三 seed 观察安全，但未超过最佳安全 SS 奖励。没有固定配置在两任务通过冻结门槛。
3. 原银行的局部 raw 候选在全部 12 个任务×metric×seed 汇总中提升真实 det raw 收益，但同单位 raw 乐观差也全部增大，且冻结候选的回合事件明显增加。这是约束筛选前候选的机制结果，不能替代最终部署模型的风险。
4. 16 个最终有事件的作业均找到与最终 checkpoint 参数完全相同的已接受 actor：其四回合验收零事件，独立 312 回合出现事件。支持有限屏幕漏检，不将最终风险倒填给更早不同参数的候选；外层重复配对亦计在这 16 作业中。

## 训练均值（outer 两种设置完全相同）

|任务|Metric|内层 shaped：raw reward / joint|内层 raw：raw reward / joint|
|---|---|---|---|
|DiagReachK2|KL|9.215463 / 1.000000|9.142500 / 0.971154|
|DiagReachK2|W2|9.249502 / 0.986111|9.196463 / 0.995726|
|DiagReachK3|KL|9.485178 / 1.000000|9.570985 / 0.994658|
|DiagReachK3|W2|9.383932 / 1.000000|9.460693 / 1.000000|

## 固定银行：raw-inner − shaped-inner（共同 raw 单位）

|任务|Metric|raw 乐观差变化|真实 det raw 收益变化|det P(any) 变化|
|---|---|---:|---:|---:|
|DiagReachK2|KL|+0.266953|+0.310046|+0.593750|
|DiagReachK2|W2|+0.259147|+0.309438|+0.598958|
|DiagReachK3|KL|+0.386239|+0.350065|+0.523438|
|DiagReachK3|W2|+0.358470|+0.312553|+0.606771|

raw 乐观差定义 Gtrain_raw−Gsample_raw，正变化表示更乐观；不是 raw/shaped 高估绝对值相减。每 seed 的两个预定锚点先汇总，再展示三 seed；完整配对条件 bootstrap、通道风险和 excess 见 CSV。训练结果、冻结候选机制、最终 screen 漏检是三种证据对象，不能混为单一路径因果证明。

## 下一路由与边界

本轮不继续训练。将证据交回导师裁决：改变 joint 奖励目标确能增加固定银行的任务收益，但同时暴露更高风险和残余代理乐观；当前四回合风险验收漏检仍未解决。既不据此删除 PPO shaping，也不宣布所有奖励 baseline 无效。OT 在匹配安全水平下没有满足本轮两任务共同增量门槛。T1590/T1592 旧 HOLD 保留，尚无 SafeOT/SOTA/native/VLA 结论。

以下为完整开发、机制及逐 seed 审计。
# T1593 reward objective alignment factorial

HOLD_OBJECTIVE_RECIPE

SS/SR/RS/RR: firstletter jointactor reward, secondletter outer score; S=shaped,R=raw. PPOalwaysshaping5. Only timeLOO,scale1; c_W common originalshaped anchor. Costs/critics/duals/risks/kernel unchanged. Rawtarget is not shapingenv0 training.

## Full development (three training seeds)

|Task|Metric|Cell|Raw reward|Success|Joint|P(any)|Worst joint|Cost mean|Channel events|Excess|
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
|DiagReachK2|KL|SS|9.215463|1.000000|1.000000|0.000000|1.000000|[5.281164, 5.483342]|[0.0, 0.0]|[0.0, 0.0]|
|DiagReachK2|KL|SR|9.215463|1.000000|1.000000|0.000000|1.000000|[5.281164, 5.483342]|[0.0, 0.0]|[0.0, 0.0]|
|DiagReachK2|KL|RS|9.142500|1.000000|0.971154|0.028846|0.955128|[5.689736, 5.477079]|[0.028846, 0.0]|[0.000211, 0.0]|
|DiagReachK2|KL|RR|9.142500|1.000000|0.971154|0.028846|0.955128|[5.689736, 5.477079]|[0.028846, 0.0]|[0.000211, 0.0]|
|DiagReachK2|W2|SS|9.249502|1.000000|0.986111|0.013889|0.958333|[5.419058, 5.623175]|[0.0, 0.013889]|[0.0, 3.5e-05]|
|DiagReachK2|W2|SR|9.249502|1.000000|0.986111|0.013889|0.958333|[5.419058, 5.623175]|[0.0, 0.013889]|[0.0, 3.5e-05]|
|DiagReachK2|W2|RS|9.196463|1.000000|0.995726|0.004274|0.993590|[5.634883, 5.490099]|[0.004274, 0.0]|[3.1e-05, 0.0]|
|DiagReachK2|W2|RR|9.196463|1.000000|0.995726|0.004274|0.993590|[5.634883, 5.490099]|[0.004274, 0.0]|[3.1e-05, 0.0]|
|DiagReachK3|KL|SS|9.485178|1.000000|1.000000|0.000000|1.000000|[6.398155, 6.020819, 11.316251]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|KL|SR|9.485178|1.000000|1.000000|0.000000|1.000000|[6.398155, 6.020819, 11.316251]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|KL|RS|9.570985|1.000000|0.994658|0.005342|0.987179|[6.651288, 6.158283, 11.736028]|[0.005342, 0.0, 0.0]|[2.6e-05, 0.0, 0.0]|
|DiagReachK3|KL|RR|9.570985|1.000000|0.994658|0.005342|0.987179|[6.651288, 6.158283, 11.736028]|[0.005342, 0.0, 0.0]|[2.6e-05, 0.0, 0.0]|
|DiagReachK3|W2|SS|9.383932|1.000000|1.000000|0.000000|1.000000|[6.017932, 5.812024, 10.793813]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|W2|SR|9.383932|1.000000|1.000000|0.000000|1.000000|[6.017932, 5.812024, 10.793813]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|W2|RS|9.460693|1.000000|1.000000|0.000000|1.000000|[6.451259, 5.783951, 11.150525]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|
|DiagReachK3|W2|RR|9.460693|1.000000|1.000000|0.000000|1.000000|[6.451259, 5.783951, 11.150525]|[0.0, 0.0, 0.0]|[0.0, 0.0, 0.0]|

Everyseed in results.csv; actual312episodes in eval_episodes.csv. Factorialinner/outer/interaction effects forreward/success/joint/everyriskchannel/install are in factorial_seed_effects.csv, pairedseed notepisode replication. Raw/shaped/penalty training and risk are phase-separated in training_curves.csv; selection counterfactuals on identical pools and acceptance on identical actualpairs are only local counterfactuals, not learnedpolicy substitutes.

## Frozen decision

[
  {
    "metric": "KL",
    "combo": "SR",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "KL",
          "combo": "SR",
          "reward": 9.215463222182082,
          "joint": 1.0,
          "success": 1.0,
          "any_event": 0.0,
          "cost_mean": [
            5.281164488731286,
            5.483342207395114
          ],
          "event": [
            0.0,
            0.0
          ],
          "excess": [
            0.0,
            0.0
          ],
          "worst_joint": 1.0,
          "worst_reward": 9.085808356854418,
          "all_seed_observed_safe": true
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "KL",
          "combo": "SR",
          "reward": 9.485177616287011,
          "joint": 1.0,
          "success": 1.0,
          "any_event": 0.0,
          "cost_mean": [
            6.398155236855533,
            6.020819154050614,
            11.316251218828379
          ],
          "event": [
            0.0,
            0.0,
            0.0
          ],
          "excess": [
            0.0,
            0.0,
            0.0
          ],
          "worst_joint": 1.0,
          "worst_reward": 9.427121689426077,
          "all_seed_observed_safe": true
        }
      }
    ]
  },
  {
    "metric": "KL",
    "combo": "RS",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "KL",
          "combo": "RS",
          "reward": 9.142500127155063,
          "joint": 0.9711538461538461,
          "success": 1.0,
          "any_event": 0.028846153846153844,
          "cost_mean": [
            5.689736417725555,
            5.477079242213159
          ],
          "event": [
            0.028846153846153844,
            0.0
          ],
          "excess": [
            0.00021146590213829946,
            0.0
          ],
          "worst_joint": 0.9551282051282052,
          "worst_reward": 8.994914557128094,
          "all_seed_observed_safe": false
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "KL",
          "combo": "RS",
          "reward": 9.57098459411848,
          "joint": 0.9946581196581197,
          "success": 1.0,
          "any_event": 0.005341880341880341,
          "cost_mean": [
            6.651288054437718,
            6.158283011016683,
            11.736027612645401
          ],
          "event": [
            0.005341880341880341,
            0.0,
            0.0
          ],
          "excess": [
            2.648243828425318e-05,
            0.0,
            0.0
          ],
          "worst_joint": 0.9871794871794872,
          "worst_reward": 9.464925675246363,
          "all_seed_observed_safe": false
        }
      }
    ]
  },
  {
    "metric": "KL",
    "combo": "RR",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "KL",
          "combo": "RR",
          "reward": 9.142500127155063,
          "joint": 0.9711538461538461,
          "success": 1.0,
          "any_event": 0.028846153846153844,
          "cost_mean": [
            5.689736417725555,
            5.477079242213159
          ],
          "event": [
            0.028846153846153844,
            0.0
          ],
          "excess": [
            0.00021146590213829946,
            0.0
          ],
          "worst_joint": 0.9551282051282052,
          "worst_reward": 8.994914557128094,
          "all_seed_observed_safe": false
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "KL",
          "combo": "RR",
          "reward": 9.57098459411848,
          "joint": 0.9946581196581197,
          "success": 1.0,
          "any_event": 0.005341880341880341,
          "cost_mean": [
            6.651288054437718,
            6.158283011016683,
            11.736027612645401
          ],
          "event": [
            0.005341880341880341,
            0.0,
            0.0
          ],
          "excess": [
            2.648243828425318e-05,
            0.0,
            0.0
          ],
          "worst_joint": 0.9871794871794872,
          "worst_reward": 9.464925675246363,
          "all_seed_observed_safe": false
        }
      }
    ]
  },
  {
    "metric": "W2",
    "combo": "SR",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "W2",
          "combo": "SR",
          "reward": 9.249501909408119,
          "joint": 0.9861111111111112,
          "success": 1.0,
          "any_event": 0.013888888888888888,
          "cost_mean": [
            5.419058301000514,
            5.623175135025612
          ],
          "event": [
            0.0,
            0.013888888888888888
          ],
          "excess": [
            0.0,
            3.487185874895461e-05
          ],
          "worst_joint": 0.9583333333333334,
          "worst_reward": 9.108127078625168,
          "all_seed_observed_safe": false
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "W2",
          "combo": "SR",
          "reward": 9.383932252238573,
          "joint": 1.0,
          "success": 1.0,
          "any_event": 0.0,
          "cost_mean": [
            6.017932245364555,
            5.812023957570394,
            10.793813382458483
          ],
          "event": [
            0.0,
            0.0,
            0.0
          ],
          "excess": [
            0.0,
            0.0,
            0.0
          ],
          "worst_joint": 1.0,
          "worst_reward": 9.29697274973531,
          "all_seed_observed_safe": true
        }
      }
    ]
  },
  {
    "metric": "W2",
    "combo": "RS",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "W2",
          "combo": "RS",
          "reward": 9.196463307368917,
          "joint": 0.9957264957264957,
          "success": 1.0,
          "any_event": 0.004273504273504273,
          "cost_mean": [
            5.634883447590037,
            5.490099145815922
          ],
          "event": [
            0.004273504273504273,
            0.0
          ],
          "excess": [
            3.079165760268513e-05,
            0.0
          ],
          "worst_joint": 0.9935897435897436,
          "worst_reward": 8.994914557128094,
          "all_seed_observed_safe": false
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "W2",
          "combo": "RS",
          "reward": 9.46069260487417,
          "joint": 1.0,
          "success": 1.0,
          "any_event": 0.0,
          "cost_mean": [
            6.451258847346672,
            5.78395076134266,
            11.150525457838661
          ],
          "event": [
            0.0,
            0.0,
            0.0
          ],
          "excess": [
            0.0,
            0.0,
            0.0
          ],
          "worst_joint": 1.0,
          "worst_reward": 9.201176203817475,
          "all_seed_observed_safe": true
        }
      }
    ]
  },
  {
    "metric": "W2",
    "combo": "RR",
    "passed": false,
    "tasks": [
      {
        "env": "DiagReachK2",
        "passed": false,
        "best_safe_SS": 9.215463222182082,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK2",
          "metric": "W2",
          "combo": "RR",
          "reward": 9.196463307368917,
          "joint": 0.9957264957264957,
          "success": 1.0,
          "any_event": 0.004273504273504273,
          "cost_mean": [
            5.634883447590037,
            5.490099145815922
          ],
          "event": [
            0.004273504273504273,
            0.0
          ],
          "excess": [
            3.079165760268513e-05,
            0.0
          ],
          "worst_joint": 0.9935897435897436,
          "worst_reward": 8.994914557128094,
          "all_seed_observed_safe": false
        }
      },
      {
        "env": "DiagReachK3",
        "passed": false,
        "best_safe_SS": 9.485177616287011,
        "required_margin": 0.05,
        "candidate": {
          "env": "DiagReachK3",
          "metric": "W2",
          "combo": "RR",
          "reward": 9.46069260487417,
          "joint": 1.0,
          "success": 1.0,
          "any_event": 0.0,
          "cost_mean": [
            6.451258847346672,
            5.78395076134266,
            11.150525457838661
          ],
          "event": [
            0.0,
            0.0,
            0.0
          ],
          "excess": [
            0.0,
            0.0,
            0.0
          ],
          "worst_joint": 1.0,
          "worst_reward": 9.201176203817475,
          "all_seed_observed_safe": true
        }
      }
    ]
  }
]

## OT separately

[
  {
    "env": "DiagReachK2",
    "combo": "SS",
    "reward_W2_minus_KL": 0.03403868722603676,
    "both_all_seed_observed_safe": false
  },
  {
    "env": "DiagReachK2",
    "combo": "SR",
    "reward_W2_minus_KL": 0.03403868722603676,
    "both_all_seed_observed_safe": false
  },
  {
    "env": "DiagReachK2",
    "combo": "RS",
    "reward_W2_minus_KL": 0.053963180213854045,
    "both_all_seed_observed_safe": false
  },
  {
    "env": "DiagReachK2",
    "combo": "RR",
    "reward_W2_minus_KL": 0.053963180213854045,
    "both_all_seed_observed_safe": false
  },
  {
    "env": "DiagReachK3",
    "combo": "SS",
    "reward_W2_minus_KL": -0.10124536404843809,
    "both_all_seed_observed_safe": true
  },
  {
    "env": "DiagReachK3",
    "combo": "SR",
    "reward_W2_minus_KL": -0.10124536404843809,
    "both_all_seed_observed_safe": true
  },
  {
    "env": "DiagReachK3",
    "combo": "RS",
    "reward_W2_minus_KL": -0.11029198924430972,
    "both_all_seed_observed_safe": false
  },
  {
    "env": "DiagReachK3",
    "combo": "RR",
    "reward_W2_minus_KL": -0.11029198924430972,
    "both_all_seed_observed_safe": false
  }
]

A rawobjective gain is not an OTinnovation. W2vsKL only comparable as safe reward if samecell bothobserved-safe; no root-cause sufficiency or formal significance claims.

## Paired fixed-bank mechanism: raw-inner minus shaped-inner, common RAW units

|Task|Metric|Seed|Raw optimism delta [conditional95%]|Real sample raw gain delta|Real det raw gain delta [conditional95%]|
|---|---|---:|---|---:|---|
|DiagReachK2|KL|180|0.06942 [0.01700,0.11983]|0.44018|0.45435 [0.44545,0.46521]|
|DiagReachK2|W2|180|0.07006 [0.01739,0.11955]|0.43797|0.44501 [0.43596,0.45604]|
|DiagReachK2|KL|186|0.26479 [0.22840,0.30075]|0.26323|0.26254 [0.25902,0.26590]|
|DiagReachK2|W2|186|0.27371 [0.23089,0.31390]|0.31732|0.32495 [0.32054,0.32958]|
|DiagReachK2|KL|187|0.46665 [0.42710,0.50675]|0.38170|0.21325 [0.20933,0.21726]|
|DiagReachK2|W2|187|0.43366 [0.39653,0.46998]|0.32464|0.15836 [0.15446,0.16227]|
|DiagReachK3|KL|180|0.49863 [0.46557,0.53663]|0.18168|0.23393 [0.22662,0.24161]|
|DiagReachK3|W2|180|0.46203 [0.42908,0.49870]|0.20270|0.25380 [0.24808,0.26002]|
|DiagReachK3|KL|186|0.16030 [0.13589,0.18149]|0.20321|0.21236 [0.20429,0.22069]|
|DiagReachK3|W2|186|0.16781 [0.13970,0.19435]|0.27300|0.22738 [0.21907,0.23629]|
|DiagReachK3|KL|187|0.49979 [0.45207,0.54553]|0.52618|0.60390 [0.59923,0.60910]|
|DiagReachK3|W2|187|0.44557 [0.40600,0.48315]|0.44769|0.45648 [0.45244,0.46114]|

Allcandidate Gtrain/Ghold/Gsample/Gdet andbootstrap intervals separately raw/shaped/penalty/cost in mechanism_anchors.csv. The primary raw optimism is Gtrain_raw−Gsample_raw for everycandidate; no subtraction acrossrewardunits. 512wholeepisodepaired bootstraps recenterLOO eachdraw; fixedGtrain, conditional evaluationuncertainty only. Three trainingseeds, twofixedanchors each, not24newtrainingreplicas.

## Safety failures and inference limits

16 finalunsafe jobs. safety_failures.json retains firsteffectiveaccept andevery lateraccept with4episodeold/newrisk. It identifies earliestaccepted actor identical tofinal checkpoint before linking its4sample screen toindependent312eval. Earliernonmatching candidates have noindependentrisklabel; finalfailure cannot retroactively classify them asacceptanceerrors. Recovery oldunsafe/channeltradeoffs are explicit. Nofinaleval changes candidates/stopping/checkpoints.

## Gates/accounting/source

Rawsame-action/noise shaping5/0 gate144steps; rawrecovery maxerror below1e-12. Prior60bankcounts confirmed42shaped vs14raw sample-positive/det-nonpositive, and23raw train-positive/det-nonpositive; no claimthatremovingPPOshaping solvesit. Sixfirstbatch shapecandidates exact,costD/critic unchanged,zeroPenalty equality; smoke commonPPO/RNG/calibration;12SS controls require full25cycle/312eval exact replay. Originalbatch unchanged; actor target tensor separate; optimizer/critictransaction checks retained.

{
  "development_training": 576000,
  "gradient_data": 288000,
  "selection": 172800,
  "acceptance": 115200,
  "development_final_eval": 179712,
  "smoke_training": 15360,
  "smoke_eval": 1152,
  "mechanism_diagnostic": 92160,
  "planned_total": 864384,
  "raw_reward_gate": 144,
  "actual_total": 864528
}

No fitting/extra learning samples. All76jobs andnegative outcomes retained; source snapshots/hashes unchanged. Four-episode screening low power remains independent. No automaticradius/feature/seed/CF search or native/VLA expansion. Papers/DERIVATION/PDF read-only.

## Per-seed reward/joint/any-event outcomes

|Task|Metric|Cell|Seed|Raw reward|Joint|P(any)|
|---|---|---|---:|---:|---:|---:|
|DiagReachK2|KL|RR|180|9.326187|0.964744|0.035256|
|DiagReachK2|KL|RS|180|9.326187|0.964744|0.035256|
|DiagReachK2|KL|SR|180|9.258067|1.000000|0.000000|
|DiagReachK2|KL|SS|180|9.258067|1.000000|0.000000|
|DiagReachK2|W2|RR|180|9.284244|0.993590|0.006410|
|DiagReachK2|W2|RS|180|9.284244|0.993590|0.006410|
|DiagReachK2|W2|SR|180|9.270043|1.000000|0.000000|
|DiagReachK2|W2|SS|180|9.270043|1.000000|0.000000|
|DiagReachK2|KL|RR|186|9.106399|0.955128|0.044872|
|DiagReachK2|KL|RS|186|9.106399|0.955128|0.044872|
|DiagReachK2|KL|SR|186|9.302515|1.000000|0.000000|
|DiagReachK2|KL|SS|186|9.302515|1.000000|0.000000|
|DiagReachK2|W2|RR|186|9.310231|1.000000|0.000000|
|DiagReachK2|W2|RS|186|9.310231|1.000000|0.000000|
|DiagReachK2|W2|SR|186|9.108127|0.958333|0.041667|
|DiagReachK2|W2|SS|186|9.108127|0.958333|0.041667|
|DiagReachK2|KL|RR|187|8.994915|0.993590|0.006410|
|DiagReachK2|KL|RS|187|8.994915|0.993590|0.006410|
|DiagReachK2|KL|SR|187|9.085808|1.000000|0.000000|
|DiagReachK2|KL|SS|187|9.085808|1.000000|0.000000|
|DiagReachK2|W2|RR|187|8.994915|0.993590|0.006410|
|DiagReachK2|W2|RS|187|8.994915|0.993590|0.006410|
|DiagReachK2|W2|SR|187|9.370336|1.000000|0.000000|
|DiagReachK2|W2|SS|187|9.370336|1.000000|0.000000|
|DiagReachK3|KL|RR|180|9.637614|0.996795|0.003205|
|DiagReachK3|KL|RS|180|9.637614|0.996795|0.003205|
|DiagReachK3|KL|SR|180|9.585912|1.000000|0.000000|
|DiagReachK3|KL|SS|180|9.585912|1.000000|0.000000|
|DiagReachK3|W2|RR|180|9.570398|1.000000|0.000000|
|DiagReachK3|W2|RS|180|9.570398|1.000000|0.000000|
|DiagReachK3|W2|SR|180|9.520693|1.000000|0.000000|
|DiagReachK3|W2|SS|180|9.520693|1.000000|0.000000|
|DiagReachK3|KL|RR|186|9.610414|1.000000|0.000000|
|DiagReachK3|KL|RS|186|9.610414|1.000000|0.000000|
|DiagReachK3|KL|SR|186|9.442500|1.000000|0.000000|
|DiagReachK3|KL|SS|186|9.442500|1.000000|0.000000|
|DiagReachK3|W2|RR|186|9.610503|1.000000|0.000000|
|DiagReachK3|W2|RS|186|9.610503|1.000000|0.000000|
|DiagReachK3|W2|SR|186|9.334131|1.000000|0.000000|
|DiagReachK3|W2|SS|186|9.334131|1.000000|0.000000|
|DiagReachK3|KL|RR|187|9.464926|0.987179|0.012821|
|DiagReachK3|KL|RS|187|9.464926|0.987179|0.012821|
|DiagReachK3|KL|SR|187|9.427122|1.000000|0.000000|
|DiagReachK3|KL|SS|187|9.427122|1.000000|0.000000|
|DiagReachK3|W2|RR|187|9.201176|1.000000|0.000000|
|DiagReachK3|W2|RS|187|9.201176|1.000000|0.000000|
|DiagReachK3|W2|SR|187|9.296973|1.000000|0.000000|
|DiagReachK3|W2|SS|187|9.296973|1.000000|0.000000|

## Factorial raw reward effects (individual training seeds)

|Task|Metric|Seed|Inner main effect|Outer main effect|Interaction|
|---|---|---:|---:|---:|---:|
|DiagReachK2|KL|180|0.068120|0.000000|0.000000|
|DiagReachK2|KL|186|-0.196116|0.000000|0.000000|
|DiagReachK2|KL|187|-0.090894|0.000000|0.000000|
|DiagReachK2|W2|180|0.014201|0.000000|0.000000|
|DiagReachK2|W2|186|0.202104|0.000000|0.000000|
|DiagReachK2|W2|187|-0.375421|0.000000|0.000000|
|DiagReachK3|KL|180|0.051703|0.000000|0.000000|
|DiagReachK3|KL|186|0.167914|0.000000|0.000000|
|DiagReachK3|KL|187|0.037804|0.000000|0.000000|
|DiagReachK3|W2|180|0.049705|0.000000|0.000000|
|DiagReachK3|W2|186|0.276372|0.000000|0.000000|
|DiagReachK3|W2|187|-0.095797|0.000000|0.000000|

Main effects average the otherfactor as preregistered; interaction is RR−RS−SR+SS. Eachfactor effect contains all3 pairedseeds. These are not a merged algorithm-effect claim or significance test. Full channel/anyrisk effects inCSV. Allresultreward andsuccess are officialrawdet; displayed shaped eval is only counterfactual bookkeeping.

## Checkpoint-matched screening failures

Of16 finalunsafe jobs, 16 have an accepted actor exactly matching finalparameters, withzeroevents inits4acceptance episodes butevents inindependent312finalepisodes. This establishes finite-screen non-detection for thatpolicy, not thefirsterror amongdifferentearlierpolicies. Allinitialold andunsafe-recovery classifications retained.

Noheldoutfinalepisode is used forselection or stopping. Additionalconfiginventory is post-run reconstruction fromfrozenconstructor+checkpointmetadata, not anotherin-training sensor. Solver/actor work remains finiteFisher subspace; thisexperimentdoesnotestablish a deploymentconsistent fullMDP OTguarantee.
