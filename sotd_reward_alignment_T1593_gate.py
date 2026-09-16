import sys,json,copy,importlib.util,hashlib,csv
from pathlib import Path
import torch,numpy as np
R=Path(__file__).resolve().parent;S=R.parents[1]/'crossfit_reward_baseline/v1';sys.path.insert(0,str(R/'snapshot'))
import experiments.run_synthetic_multi_constraint as runner
from joint_solver import update
from core import same
from raw_utils import recorded_raw
from risk import choose,accept,risk
torch.set_num_threads(1);spec=importlib.util.spec_from_file_location('oldrisk',S/'risk.py');oldrisk=importlib.util.module_from_spec(spec);spec.loader.exec_module(oldrisk)
# Raw and shaped scores differ, risks and priority/recovery stay identical.
B=np.array([1.,1.]);samples=[np.array([[r,.5,.4]]*4,np.float32) for r in [3.,2.,1.]];raw=[np.array([[r,.5,.4]]*4,np.float32) for r in [3.,4.,5.]]
a,_,ra=choose(samples,B,'excess',reward_key='shaped',raw_samples=raw);b,_,rb=choose(samples,B,'excess',reward_key='raw',raw_samples=raw);assert (a,b)==(0,2)
for x,y in zip(ra,rb):assert all(x[k]==y[k] for k in ['mean_cost','event_probability','excess','mean_feasible','event_free','risk_pair'])
assert choose(samples,B,'excess')[0]==oldrisk.choose(samples,B,'excess')[0];assert accept(samples[0],samples[1],B,'excess')[0]==oldrisk.accept(samples[0],samples[1],B,'excess')[0];assert not accept(samples[0],samples[1],B,'excess',raw_old=raw[0],raw_new=raw[1])[0];assert accept(samples[0],samples[1],B,'excess',reward_key='raw',raw_old=raw[0],raw_new=raw[1])[0]
unsafe=[np.array([[1.,2.,.3]]*4,np.float32),np.array([[2.,1.5,.4]]*4,np.float32),np.array([[10.,3.,.4]]*4,np.float32)];assert choose(unsafe,B,'excess')[0]==oldrisk.choose(unsafe,B,'excess')[0]
records=[];steps=0
for env in ['DiagReachK2','DiagReachK3']:
 for seed in [180,186,187]:
  src=S/'jobs'/f'development_{env}_s{seed}_KL_time_loo';load=lambda n:torch.load(src/n,weights_only=False,map_location='cpu');ck=load('cycle_000_old.pt');data=load('cycle_000_batch.pt');raw,pen=recorded_raw(src,0);jd=dict(data,raw_rewards=raw);assert torch.allclose(data['rewards'],raw-pen,atol=1e-5,rtol=2e-7)
  e5=runner.make_synthetic_multi_constraint_env(env,2400000000+seed+(1000 if env.endswith('3') else 0),budget_shaping_coef=5);e0=runner.make_synthetic_multi_constraint_env(env,2400000000+seed+(1000 if env.endswith('3') else 0),budget_shaping_coef=0);assert np.array_equal(e5.reset(),e0.reset());limit=np.array(e5.cost_limits,np.float32);err=0
  for act in data['actions'][:12].numpy():
   before=e5._ep_costs.copy();s5,r5,c5,d5,i5=e5.step(act);s0,r0,c0,d0,i0=e0.step(act);steps+=2;penalty=5*float(np.maximum((before+c5)/limit-e5._step/12,0).sum());err=max(err,abs(r5+penalty-r0));assert np.array_equal(s5,s0) and np.array_equal(c5,c0) and err<1e-12
  agent=runner.build_ppolag_agent(e5,dict(total_steps=6000,steps_per_epoch=240));
  for name in ['actor','reward_critic','cost_critic']:getattr(agent,name).load_state_dict(ck[name])
  agent.critic_optimizer.load_state_dict(ck['critic_optimizer']);B=np.array(e5.cost_limits);cw=json.loads((src/'calibration.json').read_text())['c_W'];models={};Ds={}
  for target in ['shaped','raw']:
   for met in ['KL','W2']:
    x=copy.deepcopy(agent);x.actor_optimizer=torch.optim.SGD(x.actor.parameters(),lr=1);inf=update(x,jd,B,metric=met,c_w=cw,actor_reward_target=target);models[target,met]=x;Ds[target,met]=x.audit_directions
    if target=='shaped':assert same(x.actor.state_dict(),load('cycle_000_'+met+'.pt')['actor'])
   assert torch.equal(Ds[target,'KL'],Ds[target,'W2'])
  assert torch.equal(Ds['raw','KL'][:,1:],Ds['shaped','KL'][:,1:]);assert same(models['shaped','KL'].reward_critic.state_dict(),models['raw','KL'].reward_critic.state_dict());assert same(models['shaped','KL'].cost_critic.state_dict(),models['raw','KL'].cost_critic.state_dict())
  z=copy.deepcopy(agent);z.actor_optimizer=torch.optim.SGD(z.actor.parameters(),lr=1);update(z,dict(data,raw_rewards=data['rewards']),B,metric='KL',c_w=cw,actor_reward_target='raw');assert same(z.actor.state_dict(),models['shaped','KL'].actor.state_dict())
  records.append(dict(env=env,seed=seed,shaped_candidates_exact=True,cost_columns_exact=True,critic_targets_exact=True,zero_penalty_same_actor=True,raw_replay_max_error=err))
assert steps==144
rows=list(csv.DictReader((R.parents[1]/'surrogate_gap_decomposition/v1/anchor_decomposition.csv').open()));counts={}
for channel in ['shaped','raw']:
 rr=[r for r in rows if r['channel']==channel];counts[channel]=dict(n=len(rr),sample_positive_det_nonpositive=sum(float(r['Gsample'])>0 and float(r['Gdet'])<=0 for r in rr),train_positive_det_nonpositive=sum(float(r['Gtrain'])>0 and float(r['Gdet'])<=0 for r in rr))
assert counts['shaped']['sample_positive_det_nonpositive']==42 and counts['raw']['sample_positive_det_nonpositive']==14 and counts['raw']['train_positive_det_nonpositive']==23
bank=json.loads((R.parents[1]/'surrogate_gap_decomposition/v1/bank.json').read_text())['anchors'];new=set(s for b in bank if b['cycle'] in [6,18] for s in range(3830000000+b['anchor']*10000,3830000000+b['anchor']*10000+64));prior=set()
for folder in ['surrogate_gap_decomposition/v1/jobs','surrogate_gap_decomposition/v1/retries2','crossfit_reward_baseline/v1/jobs']:
 for p in (R.parents[1]/folder).rglob('episodes.jsonl'):
  for line in p.open():prior.add(json.loads(line)['seed'])
assert not new&prior and len(new)==768
(R/'gate.json').write_text(json.dumps(dict(status='PASS',records=records,extra_environment_steps=steps,prior_sign_counts=counts,mechanism_new_seed_count=len(new),prior_seed_overlap=0,risk_score_switch_only=True),indent=2));print(json.dumps(records))
