import json,sys,copy
from pathlib import Path
import numpy as np,torch
R=Path(__file__).resolve().parent;S=R.parents[1]/'crossfit_reward_baseline/v1/jobs';sys.path.insert(0,str(R/'snapshot'))
import experiments.run_synthetic_multi_constraint as runner
from core import same,metrics
from risk import choose,accept,risk

def load(p):return torch.load(p,weights_only=False,map_location='cpu')
def read(p):return json.loads(p.read_text())
def job(p):
 j=read(p/'job.json');d=read(p/'result.json');c=d['effective_config'];assert c['actual_steps']==j['steps'] and c['checkpoint_reload_equal'] and c['optimizer_reload_equal'];assert len(d['eval']['episodes'])==j['eval_episodes']
 tr=[json.loads(x) for x in (p/'training_episodes.jsonl').read_text().splitlines()];assert sum(len(x['trace']) for x in tr)==j['steps'];epochs=read(p/'epochs.json');B=np.array(d['cost_limits']);assert len(epochs)*480==j['steps']
 for e in epochs:
  i=e['cycle'];samples=[]
  for a in [0.,.5,1.]:
   eps=[x for x in tr if x['cycle']==i and x['phase']=='select_'+str(a)];assert len(eps)==4;samples.append([np.r_[x['shaped_reward'],x['costs']].astype(np.float32) for x in eps])
  rawsamples=[[np.r_[x['raw_reward'],np.array(x['costs'],np.float32)] for x in tr if x['cycle']==i and x['phase']=='select_'+str(a)] for a in [0.,.5,1.]]
  k,rec,rs=choose(samples,B,'excess',e['eligible'],reward_key=j['outer_reward'],raw_samples=rawsamples);assert e['alpha']==[0.,.5,1.][k]
  va=[[np.r_[x['shaped_reward'],x['costs']].astype(np.float32) for x in tr if x['cycle']==i and x['phase']==phase] for phase in ['accept_old','accept_candidate']];rv=[[np.r_[x['raw_reward'],np.array(x['costs'],np.float32)] for x in tr if x['cycle']==i and x['phase']==phase] for phase in ['accept_old','accept_candidate']];yes,recovery,o,n=accept(*va,B,'excess',reward_key=j['outer_reward'],raw_old=rv[0],raw_new=rv[1]);assert yes==e['accepted'] and recovery==e['recovery']
  old=load(p/f'cycle_{i:03d}_old.pt');prop=load(p/f'cycle_{i:03d}_proposal.pt');fish=load(p/f"cycle_{i:03d}_{j['metric']}.pt");post=load(p/f'cycle_{i:03d}_postselection.pt');after=load(p/f'cycle_{i:03d}_after.pt')
  if yes and k==2:want=prop['actor'];opt=prop['actor_optimizer']
  elif yes and k==1:
   want=fish['actor'];opt=copy.deepcopy(old['actor_optimizer']);opt['state']={}
  else:want=old['actor'];opt=old['actor_optimizer']
  assert same(post['actor'],want) and same(post['actor_optimizer'],opt)
  assert all(same(post[key],prop[key]) for key in ['reward_critic','cost_critic','critic_optimizer'])
  assert same(post['actor'],after['actor']) and same(post['actor_optimizer'],after['actor_optimizer'])
  assert all(e['requires_grad'].values()) and all(np.isfinite(list(e['proposal_parameter_deltas'].values())))
 ck=load(p/'training_checkpoint.pt');ag=runner.build_ppolag_agent(runner.make_synthetic_multi_constraint_env(j['env'],j['seed']),dict(total_steps=j['steps']//2,steps_per_epoch=240));ag.actor.load_state_dict(ck['actor']);ag.actor_optimizer.load_state_dict(ck['actor_optimizer']);assert same(ag.actor_optimizer.state_dict(),ck['actor_optimizer'])
 for ep in d['eval']['episodes']:
  assert np.allclose(np.sum([x['cost'] for x in ep['trace']],0),ep['costs'],atol=2e-6)
  assert np.array_equal(np.array(ep['costs'])>B,ep['violations']);assert bool(ep['success'] and not any(ep['violations']))==ep['joint_pass']
 return dict(status='PASS',cycles=len(epochs),steps=j['steps'],eval_episodes=j['eval_episodes'])
def pairs(phase):
 ps=sorted((R/'jobs').glob(phase+'*'));groups={}
 for p in ps:
  j=read(p/'job.json');groups.setdefault((j['env'],j['seed']),[]).append(p)
 count_replayed=0
 for key,paths in groups.items():
  assert len(paths)==8
  for label in ['old','proposal']:
   cs=[load(p/f'cycle_000_{label}.pt') for p in paths];assert all(same(cs[0][k],c[k]) for c in cs[1:] for k in ['actor','reward_critic','cost_critic','actor_optimizer','critic_optimizer','torch_rng','numpy_rng'])
  assert all(same(load(paths[0]/'cycle_000_batch.pt'),load(p/'cycle_000_batch.pt')) for p in paths)
  anchors=[load(p/'anchor.pt') for p in paths];assert all(same(anchors[0]['actor'],x['actor']) for x in anchors[1:])
  cw=[read(p/'calibration.json')['c_W'] for p in paths];assert all(x==cw[0] for x in cw)
  bases=[load(p/'cycle_000_KL_basis.pt')['D'] for p in paths];assert all(torch.equal(bases[0][:,1:],x[:,1:]) for x in bases)
  for estimator in ['shaped','raw']:
   matched=[p for p in paths if read(p/'job.json')['inner_reward']==estimator];assert len(matched)==4
   for met in ['KL','W2']:
    cc=[load(p/f'cycle_000_{met}.pt') for p in matched];assert all(same(cc[0]['actor'],x['actor']) for x in cc[1:])
  for a in paths:
   j=read(a/'job.json')
   if phase!='development' or j['combo']!='SS':continue
   old=S/f"development_{j['env']}_s{j['seed']}_{j['metric']}_time_loo";assert old.exists()
   for i in range(25):
    for label in ['old','proposal','postselection','after','KL','W2']:
     x,y=load(a/f'cycle_{i:03d}_{label}.pt'),load(old/f'cycle_{i:03d}_{label}.pt');assert all(same(x[k],y[k]) for k in ['actor','reward_critic','cost_critic','actor_optimizer','critic_optimizer','torch_rng','numpy_rng','lambdas']),(a,i,label)
    assert same(load(a/f'cycle_{i:03d}_batch.pt'),load(old/f'cycle_{i:03d}_batch.pt'))
    x,y=read(a/'epochs.json')[i],read(old/'epochs.json')[i]
    for k in ['alpha','accepted','effective_update','selection','validation_old','validation_new']:assert x[k]==y[k],(a,i,k)
    for met in ['KL','W2']:assert x['joint_infos'][met]['coordinates']==y['joint_infos'][met]['coordinates']
   assert read(a/'result.json')['eval']==read(old/'result.json')['eval']
   assert (a/'training_episodes.jsonl').read_text()==(old/'training_episodes.jsonl').read_text();count_replayed+=1
 return dict(status='PASS',groups=len(groups),time_control_full_replays=count_replayed,all_first_batch_PPO_RNG_calibration_equal=True)
if __name__=='__main__':
 torch.set_num_threads(1);phase=sys.argv[1];results={p.name:job(p) for p in sorted((R/'jobs').glob(phase+'*'))};out=dict(jobs=results,pairs=pairs(phase));(R/(phase+'_gate.json')).write_text(json.dumps(out,indent=2));print(json.dumps(out))
