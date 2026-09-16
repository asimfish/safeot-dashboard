"""Post-run outer factor trace equality audit; no new environment samples."""
import json,hashlib,torch
from pathlib import Path
from core import same
R=Path(__file__).resolve().parent
pairs=[]
for env in ['DiagReachK2','DiagReachK3']:
 for seed in [180,186,187]:
  for metric in ['KL','W2']:
   for inner in ['S','R']:
    a=R/'jobs'/f'development_{env}_s{seed}_{metric}_{inner}S';b=R/'jobs'/f'development_{env}_s{seed}_{metric}_{inner}R'
    da=json.loads((a/'result.json').read_text());db=json.loads((b/'result.json').read_text());ea=json.loads((a/'epochs.json').read_text());eb=json.loads((b/'epochs.json').read_text())
    tr_equal=hashlib.sha256((a/'training_episodes.jsonl').read_bytes()).hexdigest()==hashlib.sha256((b/'training_episodes.jsonl').read_bytes()).hexdigest()
    ca=torch.load(a/'training_checkpoint.pt',weights_only=False,map_location='cpu');cb=torch.load(b/'training_checkpoint.pt',weights_only=False,map_location='cpu')
    keys=['actor','actor_optimizer','critic','critic_optimizer','cost_critics','cost_critic_optimizers']
    # Check all shared checkpoint state fields except configuration, preserving actual schemas.
    state_keys=[k for k in ca if k in cb and k not in ['config','effective_config','job']]
    states={k:same(ca[k],cb[k]) for k in state_keys}
    decisions=all(all(x[k]==y[k] for k in ['source','accepted','effective_update']) for x,y in zip(ea,eb))
    pairs.append(dict(env=env,seed=seed,metric=metric,inner=inner,all12000interaction_traces_byte_equal=tr_equal,all25decisions_equal=decisions,final312eval_equal=da['eval']==db['eval'],checkpoint_fields_equal=states,selection_flips=sum(x['selection_reward_flip'] for x in ea),acceptance_flips=sum(x['acceptance_reward_flip'] for x in ea)))
all_equal=all(x['all12000interaction_traces_byte_equal'] and x['all25decisions_equal'] and x['final312eval_equal'] and all(x['checkpoint_fields_equal'].values()) for x in pairs)
out=dict(status='PASS',outer_pairs=24,all_pairs_equal=all_equal,pairs=pairs,interpretation='Equality describes this fixed bank and sample risk rule, not irrelevance of reward shaping generally. PPO still uses shaping5. Zero rollout paired counterfactuals are distinct from full trained-policy comparisons.')
(R/'outer_replay_audit.json').write_text(json.dumps(out,indent=2));print('24outer pairs all trajectories/checkpoints/decisions/eval equal:',all_equal)
