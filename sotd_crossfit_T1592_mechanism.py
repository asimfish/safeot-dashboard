import os,sys,json,time,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;S=R.parents[1]/'joint_metric_solver/v1';sys.path.insert(0,str(R/'snapshot'))
import numpy as np,torch
import experiments.run_synthetic_multi_constraint as runner
from joint_solver import update,finite_targets,centered
from sampling_common import targets,contribution,lr,RecordingRNG
from core import same
j=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[1]).parent;torch.set_num_threads(1);start=time.time();b=json.loads((R.parents[1]/'surrogate_gap_decomposition/v1/bank.json').read_text())['anchors'][j['anchor']];assert b['cycle'] in [6,18];src=Path(b['source']);cy=b['cycle'];load=lambda p:torch.load(p,weights_only=False,map_location='cpu');data=load(src/f'cycle_{cy:03d}_batch.pt');ck=load(src/f'cycle_{cy:03d}_old.pt');env=runner.make_synthetic_multi_constraint_env(b['env'],b['seed'],budget_shaping_coef=5);B=np.array(env.cost_limits);agent=runner.build_ppolag_agent(env,dict(total_steps=6000,steps_per_epoch=240));agent.actor.load_state_dict(ck['actor']);agent.reward_critic.load_state_dict(ck['reward_critic']);agent.cost_critic.load_state_dict(ck['cost_critic']);agent.critic_optimizer.load_state_dict(ck['critic_optimizer']);cw=json.loads((src/'calibration.json').read_text())['c_W'];actors={'old':copy.deepcopy(agent.actor)};info={};train={};sourcehash={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in b['hashes']};assert sourcehash==b['hashes'];N=64;steps=0
for est in ['time_loo','cf_state']:
 for metric in ['KL','W2']:
  label=('time' if est=='time_loo' else 'cf')+metric;x=copy.deepcopy(agent);x.actor_optimizer=torch.optim.SGD(x.actor.parameters(),lr=1);ii=update(x,data,B,metric=metric,c_w=cw,estimator=est);info[label]=ii;actors[label]=copy.deepcopy(x.actor)
  if est=='time_loo':assert same(x.actor.state_dict(),load(src/f'cycle_{cy:03d}_{metric}.pt')['actor'])
  torch.save(dict(actor=x.actor.state_dict(),D=x.audit_directions,baseline=x.audit_reward_baseline,solver=ii),out/(label+'.pt'));ratio=lr(x.actor,agent.actor,data['states'],data['actions']);A=x.audit_reward_baseline['advantage'];A=torch.as_tensor(A,dtype=torch.double).reshape(-1).numpy();train[label]=float(((ratio-1)*A).sum()/20)
assert torch.equal(load(out/'timeKL.pt')['D'][:,1:],load(out/'cfKL.pt')['D'][:,1:]);assert torch.equal(load(out/'cfKL.pt')['D'],load(out/'cfW2.pt')['D']);assert torch.equal(load(out/'timeKL.pt')['D'],load(out/'timeW2.pt')['D'])
initial={k:copy.deepcopy(a.state_dict()) for k,a in actors.items()};arrays={};stats={};base=3820000000+b['anchor']*10000;seeds=list(range(base,base+64))
def rollout(label,mode,seed):
 global steps
 e=runner.make_synthetic_multi_constraint_env(b['env'],seed,budget_shaping_coef=5);s=e.reset();rec=RecordingRNG(e.rng);e.rng=rec;gen=torch.Generator().manual_seed(900000000000+seed);tr=[];done=False;actor=actors[label]
 while not done:
  with torch.no_grad():
   mu,ls=actor(torch.tensor(s,dtype=torch.float32));noise=torch.randn(mu.shape,generator=gen) if mode=='sample' else torch.zeros_like(mu);u=mu+ls.exp()*noise if mode=='sample' else mu;logp=torch.distributions.Normal(mu,ls.exp()).log_prob(u).sum().item()
  before=e._ep_costs.copy();ns,r,c,done,inf=e.step(u.numpy());steps+=1;pen=5*float(np.maximum((before+c)/B.astype(np.float32)-e._step/12,0).sum());tr.append(dict(state=s.copy(),proposal=u.numpy(),executed=inf['executed_action'].copy(),noise=noise.numpy(),mu=mu.numpy(),logstd=ls.numpy(),logprob=logp,values=np.concatenate([np.array([r,r+pen,pen],dtype=np.float64),c])));s=ns
 assert len(tr)==12;total=np.sum([t['values'] for t in tr],0);total[0]=inf['episode']['reward'];total[1]=total[0]+total[2];total[3:]=inf['episode']['costs'];return tr,total,inf['episode']['success'],np.array(rec.noises)
for mode in ['sample','det']:
 for label in actors:
  kernel=mode+'_'+label;trs=[];tot=[];success=[];envnoise=[]
  with (out/'episodes.jsonl').open('a') as f:
   for seed in seeds:
    tr,t,s,no=rollout(label,mode,seed);trs.append(tr);tot.append(t);success.append(s);envnoise.append(no);v=t[3:]>B;f.write(json.dumps(dict(kernel=kernel,seed=seed,action_seed=900000000000+seed,values=t.tolist(),success=s,violations=v.tolist(),joint=bool(s and not v.any())))+'\n')
  a={key:np.array([[t[key] for t in tr] for tr in trs]) for key in trs[0][0]};a.update(totals=np.array(tot),success=np.array(success),environment_noise=np.array(envnoise),episode_seeds=np.array(seeds));arrays[kernel]=a;C=a['totals'][:,3:];v=C>B;stats[kernel]=dict(raw_reward=float(a['totals'][:,1].mean()),shaped_reward=float(a['totals'][:,0].mean()),penalty=float(a['totals'][:,2].mean()),cost_mean=C.mean(0).tolist(),cost_over_B=(C.mean(0)/B).tolist(),excess=np.maximum(C/B-1,0).mean(0).tolist(),event=v.mean(0).tolist(),any_event=float(v.any(1).mean()),success=float(np.mean(success)),joint=float(np.mean(np.array(success)*(~v.any(1)))))
  assert np.array_equal(a['environment_noise'],arrays['sample_old']['environment_noise']);assert np.array_equal(a['state'][:,0],arrays['sample_old']['state'][:,0]);assert np.array_equal(np.clip(a['proposal'],-1,1),a['executed'])
  if mode=='sample':assert np.array_equal(a['noise'],arrays['sample_old']['noise'])
  np.savez_compressed(out/(kernel+'.npz'),**a);print(json.dumps(dict(kernel=kernel,steps=steps)),flush=True)
old=arrays['sample_old'];target=targets(old['values']);draws=np.random.default_rng(159200+b['anchor']).integers(0,N,(512,N));results={}
for label in list(actors)[1:]:
 ratio=lr(actors[label],actors['old'],old['state'].reshape(-1,9),old['proposal'].reshape(-1,2)).reshape(N,12);hc=contribution(ratio,target);sc=arrays['sample_'+label]['totals']-old['totals'];dc=arrays['det_'+label]['totals']-arrays['det_old']['totals'];boots=[]
 for idx in draws:
  h=contribution(ratio[idx],target[idx]).mean(0);s=sc[idx].mean(0);d=dc[idx].mean(0);boots.append(np.r_[train[label]-s[0],train[label]-d[0],s[:3],d[:3],h[:3]])
 boots=np.array(boots);np.savez_compressed(out/(label+'_contributions.npz'),hold_timeLOO=hc,sample=sc,det=dc,ratio=ratio,bootstrap=boots,bootstrap_indices=draws);results[label]=dict(Gtrain_shaped=train[label],Gsample=sc.mean(0).tolist(),Gdet=dc.mean(0).tolist(),Ghold_timeLOO=hc.mean(0).tolist(),optimism_sample=train[label]-float(sc[:,0].mean()),optimism_det=train[label]-float(dc[:,0].mean()),hold_contribution_std=hc.std(0,ddof=1).tolist(),sample_contribution_std=sc.std(0,ddof=1).tolist(),bootstrap_ci95=np.quantile(boots,[.025,.975],axis=0).tolist(),bootstrap_columns=['optimism_sample','optimism_det','sample_shaped','sample_raw','sample_penalty','det_shaped','det_raw','det_penalty','hold_shaped','hold_raw','hold_penalty'])
assert steps==7680 and all(same(initial[k],a.state_dict()) for k,a in actors.items());assert sourcehash=={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sourcehash};r=dict(status='verified',anchor=b,source_hashes=sourcehash,c_W=cw,solver=info,stats=stats,gains=results,steps=steps,episodes=640,training_steps=0,common_hold_estimator='timeLOO on fresh old data; not CF refit',CRN=True,source_unchanged=True,seconds=time.time()-start);(out/'result.json').write_text(json.dumps(r,indent=2));print(json.dumps(dict(status='verified',seconds=time.time()-start)),flush=True)
