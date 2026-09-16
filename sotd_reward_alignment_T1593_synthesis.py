import json,csv,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parent;f=json.loads((R/'findings.json').read_text());rr=list(csv.DictReader((R/'mechanism_risks.csv').open()));out=[]
for env in ['DiagReachK2','DiagReachK3']:
 for m in ['KL','W2']:
  for seed in [180,186,187]:
   for mode in ['sample','det']:
    a=[x for x in rr if (x['env'],x['seed'],x['kernel'])==(env,str(seed),mode+'_raw'+m)];b=[x for x in rr if (x['env'],x['seed'],x['kernel'])==(env,str(seed),mode+'_shaped'+m)];assert len(a)==len(b)==2
    d={k:float(np.mean([float(x[k]) for x in a])-np.mean([float(x[k]) for x in b])) for k in ['raw_reward','shaped_reward','penalty','any_event','success','joint']}
    for k in ['cost_mean','event','excess']:d[k]=(np.mean([json.loads(x[k]) for x in a],0)-np.mean([json.loads(x[k]) for x in b],0)).tolist()
    out.append(dict(env=env,metric=m,seed=seed,kernel=mode,**d))
with (R/'mechanism_risk_seed_pairs.csv').open('w') as h:
 w=csv.DictWriter(h,fieldnames=list(out[0]));w.writeheader();w.writerows([{k:json.dumps(v) if isinstance(v,list) else v for k,v in x.items()} for x in out])
n=nonzero=sf=af=0
for p in (R/'jobs').glob('development_*'):
 for e in json.loads((p/'epochs.json').read_text()):
  sf+=e['selection_reward_flip'];af+=e['acceptance_reward_flip']
  for risk in e['selection_risks']:
   if risk['event_free']:n+=1;nonzero+=abs(risk['raw_reward']-risk['shaped_reward'])>1e-6
f['outer_score_diagnostic']=dict(event_free_candidate_screens=n,nonzero_penalty_in_these_screens=nonzero,selection_key_flips=sf,acceptance_key_flips=af,all24trained_outer_pairs_exact=True,duplicate_pair_trajectories_not_independent=True)
f['mechanism_raw_optimism_decreased_seed_groups']=sum(x['optimism_raw_delta']<0 for x in f['mechanism_seed_pairs']);f['mechanism_raw_det_reward_increased_seed_groups']=sum(x['det_raw_delta']>0 for x in f['mechanism_seed_pairs']);(R/'findings.json').write_text(json.dumps(f,indent=2))
lines=['# T1593：奖励目标对齐 2×2 的有界结果','', '**判决：HOLD_OBJECTIVE_RECIPE。关闭本轮固定配方，不扩种子或搜索。**','', '16 烟测、48 开发、12 独立机制锚点全部 exit 0，12 个 SS 对照完整精确回放。共 864528 次环境交互，含单列的 144 步原始奖励核验；其中开发梯度探索仅 288000 步。下列均值按三个训练种子汇总，312 回合不是训练重复。','', '## 直接结论','', '1. 外层 reward key 没有产生本轮路径差异：24 对训练的完整交互轨迹、决策、最终 actor/optimizer 状态及评估完全一致。全部 2696 个无观察事件的候选筛选样本，raw 与 shaped 均值相同（惩罚为零）；零次选择/验收翻转。重复 outer 配对轨迹不当作独立证据。这不表示 shaping 普遍无效，PPO 始终保留 shaping5。','2. 内层 raw 改动产生不同候选和训练效果。K2 两个 metric 奖励和联合成功率均下降；K3 奖励上升，其中 KL 出现事件、W2 保持三 seed 观察安全，但未超过最佳安全 SS 奖励。没有固定配置在两任务通过冻结门槛。','3. 原银行的局部 raw 候选在全部 12 个任务×metric×seed 汇总中提升真实 det raw 收益，但同单位 raw 乐观差也全部增大，且冻结候选的回合事件明显增加。这是约束筛选前候选的机制结果，不能替代最终部署模型的风险。','4. 16 个最终有事件的作业均找到与最终 checkpoint 参数完全相同的已接受 actor：其四回合验收零事件，独立 312 回合出现事件。支持有限屏幕漏检，不将最终风险倒填给更早不同参数的候选；外层重复配对亦计在这 16 作业中。','', '## 训练均值（outer 两种设置完全相同）','', '|任务|Metric|内层 shaped：raw reward / joint|内层 raw：raw reward / joint|','|---|---|---|---|']
for env in ['DiagReachK2','DiagReachK3']:
 for m in ['KL','W2']:
  a=next(x for x in f['groups'] if (x['env'],x['metric'],x['combo'])==(env,m,'SS'));b=next(x for x in f['groups'] if (x['env'],x['metric'],x['combo'])==(env,m,'RS'));lines.append(f"|{env}|{m}|{a['reward']:.6f} / {a['joint']:.6f}|{b['reward']:.6f} / {b['joint']:.6f}|")
lines+=['', '## 固定银行：raw-inner − shaped-inner（共同 raw 单位）','', '|任务|Metric|raw 乐观差变化|真实 det raw 收益变化|det P(any) 变化|','|---|---|---:|---:|---:|']
for env in ['DiagReachK2','DiagReachK3']:
 for m in ['KL','W2']:
  a=[x for x in f['mechanism_seed_pairs'] if (x['env'],x['metric'])==(env,m)];b=[x for x in out if (x['env'],x['metric'],x['kernel'])==(env,m,'det')];lines.append(f"|{env}|{m}|{np.mean([x['optimism_raw_delta'] for x in a]):+.6f}|{np.mean([x['det_raw_delta'] for x in a]):+.6f}|{np.mean([x['any_event'] for x in b]):+.6f}|")
lines+=['', 'raw 乐观差定义 Gtrain_raw−Gsample_raw，正变化表示更乐观；不是 raw/shaped 高估绝对值相减。每 seed 的两个预定锚点先汇总，再展示三 seed；完整配对条件 bootstrap、通道风险和 excess 见 CSV。训练结果、冻结候选机制、最终 screen 漏检是三种证据对象，不能混为单一路径因果证明。','', '## 下一路由与边界','', '本轮不继续训练。将证据交回导师裁决：改变 joint 奖励目标确能增加固定银行的任务收益，但同时暴露更高风险和残余代理乐观；当前四回合风险验收漏检仍未解决。既不据此删除 PPO shaping，也不宣布所有奖励 baseline 无效。OT 在匹配安全水平下没有满足本轮两任务共同增量门槛。T1590/T1592 旧 HOLD 保留，尚无 SafeOT/SOTA/native/VLA 结论。','', '以下为完整开发、机制及逐 seed 审计。','']
(R/'report.md').write_text('\n'.join(lines)+(R/'report.md').read_text());print('synthesis complete',f['status'])
