import sys,json,time,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'snapshot'))
import torch,numpy as np
import experiments.run_synthetic_multi_constraint as runner
from common import targets,contribution,lr,RecordingRNG,load_actor,bootstrap
from core import same
torch.set_num_threads(1);j=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[1]).parent;bank=json.loads((R/'bank.json').read_text())['anchors'];b=bank[j['anchor']];src=Path(b['source']);cycle=b['cycle'];N=j['episodes'];count=0;start=time.time();B=np.array(runner.SYNTHETIC_CONFIGS[b['env']].budgets) if hasattr(runner.SYNTHETIC_CONFIGS[b['env']],'budgets') else None
for p,h in b['hashes'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
load=lambda name:torch.load(src/name,weights_only=False,map_location='cpu');cks={m:load(f'cycle_{cycle:03d}_{m}.pt') for m in ['old','KL','W2']};env=runner.make_synthetic_multi_constraint_env(b['env'],b['seed'],budget_shaping_coef=5);B=np.array(env.cost_limits);actors={m:load_actor(runner,env,c) for m,c in cks.items()};initial={m:copy.deepcopy(a.state_dict()) for m,a in actors.items()};data=load(f'cycle_{cycle:03d}_batch.pt');old_epoch=json.loads((src/'epochs.json').read_text())[cycle];assert torch.equal(load(f'cycle_{cycle:03d}_KL_basis.pt')['D'],load(f'cycle_{cycle:03d}_W2_basis.pt')['D'])
assert len(data['states'])==240 and data['dones'].reshape(20,12)[:,-1].bool().all() and not data['dones'].reshape(20,12)[:,:-1].bool().any()
cols=['shaped','raw','penalty']+['cost_'+str(i) for i in range(len(B))]
# Train returns use original float32 reward/cost arrays; penalty is reconstructed independently.
cost=data['costs'].reshape(20,12,-1).numpy();pen=5*np.maximum(np.cumsum(cost,1)/B.astype(np.float32)-np.arange(1,13,dtype=np.float32)[None,:,None]/12,0).sum(-1);reward=data['rewards'].reshape(20,12).numpy();trainvals=np.concatenate([reward[...,None],(reward+pen)[...,None],pen[...,None],cost],-1);traintarget=targets(trainvals);trainrat={};traincon={};Gtrain={};Jhat=data['costs'].reshape(20,12,-1).sum(1).mean(0).double().numpy()
for m in ['KL','W2']:
 trainrat[m]=lr(actors[m],actors['old'],data['states'],data['actions']).reshape(20,12);traincon[m]=contribution(trainrat[m],traintarget);Gtrain[m]=traincon[m].mean(0);info=old_epoch['joint_infos'][m]
 assert abs(Gtrain[m][0]-info['reward_gain'])<1e-5,(m,Gtrain[m][0],info['reward_gain'])
 assert np.max(np.abs(Jhat+Gtrain[m][3:]-info['actual_predicted_cost']))<1e-7
# Original sample equivalence, logprob convention, and det hybrid unit identities, zero new environment interactions.
obs=data['states'][:1];torch.manual_seed(1591);expected,lp=actors['old'].sample(obs);gen=torch.Generator().manual_seed(1591)
with torch.no_grad():
 mu,ls=actors['old'](obs);actual=mu+ls.exp()*torch.randn(mu.shape,generator=gen);assert torch.equal(expected,actual);assert torch.allclose(lp,actors['old'].log_prob(obs,actual))
 for m in ['KL','W2']:
  mq,lq=actors[m](obs);assert torch.equal(mq,actors[m].deterministic(obs));assert torch.equal(mu,actors['old'].deterministic(obs))

def rollout(kernel,seed):
 global count,last_exact_episode_return
 mode,met,*hybrid=kernel.split('_');e=runner.make_synthetic_multi_constraint_env(b['env'],seed,budget_shaping_coef=5);s=e.reset();rec=RecordingRNG(e.rng);e.rng=rec;generator=torch.Generator().manual_seed(900000000000+seed);a=actors[met];trace=[];initial_pos=s[:2].copy();done=False
 while not done:
  with torch.no_grad():
   st=torch.tensor(s,dtype=torch.float32);mu,ls=a(st)
   if hybrid:
    mo,lo=actors['old'](st)
    if hybrid[0]=='mean':ls=lo
    else:mu=mo
   noise=torch.randn(mu.shape,generator=generator) if mode=='sample' else torch.zeros_like(mu);proposal=mu+ls.exp()*noise if mode=='sample' else mu;logp=torch.distributions.Normal(mu,ls.exp()).log_prob(proposal).sum().item()
  before=e._ep_costs.copy();ns,r,c,done,info=e.step(proposal.numpy());count+=1;penalty=5*float(np.maximum((before+c)/B.astype(np.float32)-e._step/12,0).sum());trace.append(dict(state=s.copy(),proposal=proposal.numpy(),executed=info['executed_action'].copy(),action_noise=noise.numpy(),mu=mu.numpy(),logstd=ls.numpy(),logprob=logp,values=np.r_[r,r+penalty,penalty,c]));s=ns
 last_exact_episode_return=info['episode']['reward'];assert len(trace)==12;total=np.sum([t['values'] for t in trace],0);total[3:]=info['episode']['costs'];return trace,total,float(info['episode']['success']),np.array(rec.noises),initial_pos

# Reproduce old/KL selection on its original four paired seeds; counted separately.
replay=[];base=3100000000+b['seed']*100000+cycle*100
for met,idx in [('old',0),('KL',1)]:
 replayed=[]
 for k in range(4):
  t=rollout('det_'+met,base+k)[1];replayed.append(np.r_[last_exact_episode_return,t[3:].astype(np.float32)])
 means=np.mean(replayed,0);expected=np.array(old_epoch['selection'][idx]);assert np.allclose(means,expected,atol=1e-6,rtol=0),(means,expected,means-expected);replay.append(dict(metric=met,reproduced=means.tolist(),expected=expected.tolist(),reduction='original float32 np.r_ then mean'))
gate_steps=count
kernels=['sample_old','sample_KL','sample_W2','sample_KL_mean','sample_KL_std','sample_W2_mean','sample_W2_std','det_old','det_KL','det_W2'];base=(3810000000 if j['phase']=='smoke' else 3800000000)+b['anchor']*10000;totals={};stats={};arrays={};record_file=out/'episodes.jsonl';episode_seeds=list(range(base,base+N))
for kernel in kernels:
 traces=[];ts=[];ss=[];noises=[];positions=[]
 with record_file.open('a') as f:
  for seed in episode_seeds:
   tr,t,s,no,pos=rollout(kernel,seed);traces.append(tr);ts.append(t);ss.append(s);noises.append(no);positions.append(pos);v=t[3:]>B;f.write(json.dumps(dict(kernel=kernel,seed=seed,action_seed=900000000000+seed,values=t.tolist(),success=s,violations=v.tolist(),joint=bool(s and not v.any())))+'\n')
 totals[kernel]=np.array(ts);C=totals[kernel][:,3:];V=C>B
 a={key:np.array([[x[key] for x in ep] for ep in traces]) for key in traces[0][0]};a.update(totals=totals[kernel],success=np.array(ss),environment_noise=np.array(noises),initial_position=np.array(positions),episode_seeds=np.array(episode_seeds));arrays[kernel]=a;np.savez_compressed(out/(kernel+'.npz'),**a)
 stats[kernel]=dict(raw_reward=float(totals[kernel][:,1].mean()),shaped_reward=float(totals[kernel][:,0].mean()),penalty=float(totals[kernel][:,2].mean()),mean_cost=C.mean(0).tolist(),cost_over_B=(C.mean(0)/B).tolist(),excess=np.maximum(C/B-1,0).mean(0).tolist(),event=V.mean(0).tolist(),any_event=float(V.any(1).mean()),success=float(np.mean(ss)),joint=float(np.mean(np.array(ss)*(~V.any(1)))),mean_feasible=bool(np.all(C.mean(0)<=B)),mean_feasible_with_events=bool(np.all(C.mean(0)<=B) and V.any()))
 assert np.array_equal(a['environment_noise'],arrays['sample_old']['environment_noise']) and np.array_equal(a['initial_position'],arrays['sample_old']['initial_position'])
 if kernel.startswith('sample'):assert np.array_equal(a['action_noise'],arrays['sample_old']['action_noise'])
 assert np.array_equal(np.clip(a['proposal'],-1,1),a['executed'])
 print(json.dumps(dict(kernel=kernel,episodes=N,steps=count)),flush=True)
old=arrays['sample_old'];newtarget=targets(old['values']);results={};boots={}
for met in ['KL','W2']:
 ratios=lr(actors[met],actors['old'],old['state'].reshape(-1,old['state'].shape[-1]),old['proposal'].reshape(-1,2)).reshape(N,12);hcon=contribution(ratios,newtarget);hold=hcon.mean(0);scon=totals['sample_'+met]-totals['sample_old'];dcon=totals['det_'+met]-totals['det_old'];sam=scon.mean(0);det=dcon.mean(0);comps=np.stack([Gtrain[met]-hold,hold-sam,sam-det]);assert np.allclose(comps.sum(0),Gtrain[met]-det,atol=1e-12)
 meancon=totals['sample_'+met+'_mean']-totals['sample_old'];stdcon=totals['sample_'+met+'_std']-totals['sample_old'];interaction=scon-meancon-stdcon;assert np.allclose(scon,meancon+stdcon+interaction,atol=1e-12)
 boot,draws=bootstrap(ratios,newtarget,totals,Gtrain[met],met,512,159100+b['anchor']+(1000 if j['phase']=='smoke' else 0));boots[met]=boot;np.savez_compressed(out/(met+'_contributions.npz'),train=traincon[met],holdLR=hcon,sample=scon,det=dcon,mean_only=meancon,std_only=stdcon,interaction=interaction,ratio=ratios,hold_returns=newtarget.numpy(),bootstrap=boot,bootstrap_indices=draws)
 results[met]=dict(Gtrain=Gtrain[met].tolist(),GholdLR=hold.tolist(),Gsample=sam.tolist(),Gdet=det.tolist(),components=comps.tolist(),component_names=['training_sample_generalization','finite_step_surrogate_occupancy','execution_kernel_gain'],bootstrap_ci95=np.quantile(boot,[.025,.975],axis=0).tolist(),bootstrap_channels=['GholdLR','Gsample','Gdet','T','L','K','mean_only','std_only','interaction'],variance=dict(mean_only=meancon.mean(0).tolist(),std_only=stdcon.mean(0).tolist(),interaction=interaction.mean(0).tolist()),cost_intercept_sample=(Jhat-totals['sample_old'][:,3:].mean(0)).tolist(),cost_intercept_det=(Jhat-totals['det_old'][:,3:].mean(0)).tolist(),train_Jhat=Jhat.tolist(),cost_surrogate=(Jhat+Gtrain[met][3:]).tolist(),original_solver=old_epoch['joint_infos'][met])
assert count==10*N*12+96
for p,h in b['hashes'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for met,a in actors.items():assert same(initial[met],a.state_dict())
res=dict(status='verified',anchor=b,phase=j['phase'],columns=cols,budget=B.tolist(),episodes_per_kernel=N,fresh_bank_steps=10*N*12,replay_steps=gate_steps,total_evaluation_steps=count,training_steps=0,checkpoint_hashes_unchanged=True,policy_parameters_unchanged=True,CRN_environment_and_action=True,proposal_logprob_unit='per timestep joint action Gaussian density, unclipped',replay=replay,stats=stats,decomposition=results,seconds=time.time()-start);(out/'result.json').write_text(json.dumps(res,indent=2));print(json.dumps(dict(status='verified',steps=count,seconds=time.time()-start)),flush=True)
