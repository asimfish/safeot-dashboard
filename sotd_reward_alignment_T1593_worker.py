import sys,json,time,copy
from pathlib import Path
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'snapshot'))
import numpy as np,torch
import experiments.run_synthetic_multi_constraint as runner
from safeflow.ppo_lagrangian import PPOLagrangian
from core import metrics,interpolate,install,deltas,same
from joint_solver import update as joint_update
from risk import choose,accept
torch.set_num_threads(1);j=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[1]).parent;torch.manual_seed(j['seed']);np.random.seed(j['seed']);env=runner.make_synthetic_multi_constraint_env(j['env'],j['seed'],budget_shaping_coef=5);agent=runner.build_ppolag_agent(env,dict(total_steps=j['steps']//2,steps_per_epoch=240,budget_shaping_coef=5));assert not agent.executed_action_learning and all(p.requires_grad for p in agent.actor.parameters());B=np.array(env.cost_limits);steps=0;events=[];episodes=[];beta=None;c_w=None;accepted_updates=0;proposal_steps=0;start=time.time();initial=copy.deepcopy(agent.actor.state_dict())
def save(a,path):torch.save(dict(actor=a.actor.state_dict(),reward_critic=a.reward_critic.state_dict(),cost_critic=a.cost_critic.state_dict(),actor_optimizer=a.actor_optimizer.state_dict(),critic_optimizer=a.critic_optimizer.state_dict(),lambdas=a.lambdas,torch_rng=torch.get_rng_state(),numpy_rng=np.random.get_state(),actual_steps=steps),path)
def record_episode(phase,cycle,trace,ep,seed=None):
 penalty=sum(x['penalty'] for x in trace);v=np.array(ep['costs'])>B;row=dict(phase=phase,cycle=cycle,seed=seed,raw_reward=ep['reward']+penalty,shaped_reward=ep['reward'],penalty=penalty,costs=np.asarray(ep['costs']).tolist(),success=ep['success'],joint=bool(ep['success'] and not v.any()),violation=v.tolist(),trace=trace.copy());episodes.append(row)
 with (out/'training_episodes.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 return np.r_[ep['reward'],ep['costs']]
orig_step=env.step;explore=[];raw_batch=[];penalty_batch=[]
def measured(action):
 global steps
 before=env._ep_costs.copy();ns,r,c,done,info=orig_step(action);steps+=1;pen=5*float(np.maximum((before+c)/B.astype(np.float32)-env._step/12,0).sum());explore.append(dict(proposal=np.asarray(action).tolist(),executed_action=info['executed_action'].tolist(),raw_reward=r+pen,shaped_reward=r,penalty=pen,cost=c.tolist()))
 raw_batch.append(r+pen);penalty_batch.append(pen)
 if done:record_episode('exploration',len(events),explore,info['episode']);explore.clear()
 return ns,r,c,done,info
env.step=measured

def rollout(actor,seed,phase,cycle):
 global steps
 e=runner.make_synthetic_multi_constraint_env(j['env'],seed,budget_shaping_coef=5);s=e.reset();done=False;trace=[]
 while not done:
  with torch.no_grad():act=actor.deterministic(torch.tensor(s,dtype=torch.float32)).numpy()
  before=e._ep_costs.copy();ns,r,c,done,info=e.step(act);steps+=1;pen=5*float(np.maximum((before+c)/B.astype(np.float32)-e._step/12,0).sum());trace.append(dict(state=s.tolist(),proposal=act.tolist(),executed_action=info['executed_action'].tolist(),raw_reward=r+pen,shaped_reward=r,penalty=pen,cost=c.tolist()));s=ns
 return record_episode(phase,cycle,trace,info['episode'],seed)

def update(data,*,total_step=0):
 global beta,c_w,accepted_updates,proposal_steps
 cycle=len(events);assert len(raw_batch)==240;raw_tensor=torch.tensor(raw_batch,dtype=torch.float32);pen_tensor=torch.tensor(penalty_batch,dtype=torch.float32);raw_batch.clear();penalty_batch.clear();assert torch.allclose(data['rewards'],raw_tensor-pen_tensor,atol=1e-5,rtol=2e-7);joint_data=dict(data,raw_rewards=raw_tensor);torch.save(dict(raw=raw_tensor,shaped=data['rewards'].clone(),penalty=pen_tensor),out/f'cycle_{cycle:03d}_rewards.pt');oldactor=copy.deepcopy(agent.actor.state_dict());oldopt=copy.deepcopy(agent.actor_optimizer.state_dict());save(agent,out/f'cycle_{cycle:03d}_old.pt');torch.save(data,out/f'cycle_{cycle:03d}_batch.pt');shadow=copy.deepcopy(agent);grads=[]
 def grad_hook(*args):grads.append({n:float(p.grad.norm()) if p.grad is not None else None for n,p in shadow.actor.named_parameters()})
 hook=shadow.actor_optimizer.register_step_pre_hook(grad_hook);result=PPOLagrangian._update(shadow,data,total_step=total_step);hook.remove();proposal_steps+=len(grads);save(shadow,out/f'cycle_{cycle:03d}_proposal.pt');proposal_delta=deltas(oldactor,shadow.actor.state_dict());assert any(v>0 for k,v in proposal_delta.items() if k.startswith('backbone')) and proposal_delta['mu_head.weight']>0 and proposal_delta['log_std_head.weight']>0
 rng_t=torch.get_rng_state();rng_n=np.random.get_state()
 if c_w is None:
  anchor=copy.deepcopy(agent);anchor.actor_optimizer=torch.optim.SGD(anchor.actor.parameters(),lr=1);anchor_info=joint_update(anchor,data,B,metric='KL',scale=1)
  kk,ww=anchor_info['actual_raw_KL'],anchor_info['actual_raw_W2_squared']
  if not (anchor_info['accepted'] and anchor_info['parameter_delta']>0 and min(kk,ww)>1e-12):
   (out/'calibration_degenerate.json').write_text(json.dumps(anchor_info));raise RuntimeError('calibration_degenerate: no alternative radius')
  c_w=ww/kk;torch.set_rng_state(rng_t);np.random.set_state(rng_n);save(anchor,out/'anchor.pt');(out/'calibration.json').write_text(json.dumps(dict(c_W=c_w,anchor=anchor_info,environment_steps=0)))
 joint_shadows={};joint_infos={}
 for met in ['KL','W2']:
  joint=copy.deepcopy(agent);joint.actor_optimizer=torch.optim.SGD(joint.actor.parameters(),lr=1)
  ji=joint_update(joint,joint_data,B,metric=met,scale=j['scale'],c_w=c_w,estimator='time_loo',actor_reward_target=j['inner_reward']);torch.save(joint.audit_reward_baseline,out/f'cycle_{cycle:03d}_{met}_baseline.pt');joint_shadows[met]=joint;joint_infos[met]=ji
  torch.set_rng_state(rng_t);np.random.set_state(rng_n);save(joint,out/f'cycle_{cycle:03d}_{met}.pt');torch.save(dict(D=joint.audit_directions,delta=joint.audit_delta),out/f'cycle_{cycle:03d}_{met}_basis.pt')
 assert torch.equal(joint_shadows['KL'].audit_directions,joint_shadows['W2'].audit_directions)
 with torch.no_grad():
  km,kl=joint_shadows['KL'].actor(data['states']);wm,wl=joint_shadows['W2'].actor(data['states'])
 difference=dict(z_l2=float(np.linalg.norm(np.array(joint_infos['KL']['coordinates'])-np.array(joint_infos['W2']['coordinates']))),parameter_l2=float((joint_shadows['KL'].audit_delta-joint_shadows['W2'].audit_delta).norm()),mean_l2=float((km-wm).norm()),std_l2=float((kl.exp()-wl.exp()).norm()))
 fisher=joint_shadows[j['metric']];finfo=joint_infos[j['metric']]
 alphas=[0.,.5,1.];sources=['old','joint_'+j['metric'],'full_PPO'];candidates=[copy.deepcopy(agent.actor),copy.deepcopy(fisher.actor),copy.deepcopy(shadow.actor)];regs=[metrics(agent.actor,c,data['states']) for c in candidates]
 beta=0.;regvalues=[0.,0.,0.];seedbase=3100000000+j['seed']*100000+cycle*100
 sample_sets=[[rollout(c,seedbase+k,'select_'+str(alpha),cycle) for k in range(4)] for c,alpha in zip(candidates,alphas)];selection=[np.mean(x,0) for x in sample_sets]
 mode='excess';eligible=[0,2] if not finfo['accepted'] else [0,1,2]
 raw_sets=[[np.r_[ep['raw_reward'],np.array(ep['costs'],np.float32)] for ep in episodes if ep['cycle']==cycle and ep['phase']=='select_'+str(alpha)] for alpha in alphas]
 chosen,selection_recovery,selection_risks=choose(sample_sets,B,mode,eligible,reward_key=j['outer_reward'],raw_samples=raw_sets);scores=[x['actual_score'] for x in selection_risks];other_key='raw' if j['outer_reward']=='shaped' else 'shaped';other_selection=choose(sample_sets,B,mode,eligible,reward_key=other_key,raw_samples=raw_sets)[0]
 va=[];vo=[]
 for k in range(4):vo.append(rollout(agent.actor,seedbase+20+k,'accept_old',cycle));va.append(rollout(candidates[chosen],seedbase+20+k,'accept_candidate',cycle))
 raw_vo=[np.r_[ep['raw_reward'],np.array(ep['costs'],np.float32)] for ep in episodes if ep['cycle']==cycle and ep['phase']=='accept_old'];raw_va=[np.r_[ep['raw_reward'],np.array(ep['costs'],np.float32)] for ep in episodes if ep['cycle']==cycle and ep['phase']=='accept_candidate']
 accepted,recovery,oldrisk,newrisk=accept(vo,va,B,mode,reward_key=j['outer_reward'],raw_old=raw_vo,raw_new=raw_va);other_accept=accept(vo,va,B,mode,reward_key=other_key,raw_old=raw_vo,raw_new=raw_va)[0];va=np.mean(va,0);vo=np.mean(vo,0)
 # Middle slot always resets Adam; install copies candidate, never Fisher SGD state.
 rule=install(agent,shadow,candidates[chosen],alphas[chosen],accepted,oldactor,oldopt);ad=deltas(oldactor,agent.actor.state_dict());effective=bool(accepted and chosen>0 and any(v>0 for v in ad.values()));accepted_updates+=int(effective)

 oldmodule=copy.deepcopy(agent.actor);oldmodule.load_state_dict(oldactor);actual=metrics(oldmodule,agent.actor,data['states'])
 if accepted and alphas[chosen]>0:assert same(agent.actor.state_dict(),candidates[chosen].state_dict())
 info=dict(inner_reward=j["inner_reward"],outer_reward=j["outer_reward"],actual_score=scores,raw_selection=np.array([np.mean(x,0) for x in raw_sets]).tolist(),counterfactual_other_key=other_key,counterfactual_selection=other_selection,selection_reward_flip=bool(other_selection!=chosen),acceptance_reward_flip=bool(other_accept!=accepted),c_W=c_w,joint_infos=joint_infos,joint_difference=difference,source=sources[chosen],candidate_sources=sources,eligible=eligible,fisher_info=finfo,selection_risks=selection_risks,acceptance_old_risk=oldrisk,acceptance_new_risk=newrisk,channel_excess_change=(np.array(newrisk["excess"])-np.array(oldrisk["excess"])).tolist(),cycle=cycle,alpha=alphas[chosen],accepted=accepted,effective_update=effective,selection_recovery=selection_recovery,recovery=bool(recovery),optimizer_rule=rule,actual_regularizer=actual,beta=beta,regularizers=regs,selection=np.array(selection).tolist(),selection_scores=scores,validation_old=vo.tolist(),validation_new=va.tolist(),selection_error=(va-selection[chosen]).tolist(),proposal_parameter_deltas=proposal_delta,accepted_parameter_deltas=ad,gradient_norms=grads,requires_grad={n:p.requires_grad for n,p in agent.actor.named_parameters()},steps=steps,duals_before=agent.lambdas.tolist())
 events.append(info);save(agent,out/f'cycle_{cycle:03d}_postselection.pt');(out/'epochs.json').write_text(json.dumps(events,indent=2));print(json.dumps({k:info[k] for k in ['cycle','alpha','accepted','effective_update','optimizer_rule','validation_new','steps']}),flush=True);return result
agent._update=update;origdual=agent._update_lambdas
def dual(cost):
 origdual(cost);events[-1]['duals_after']=agent.lambdas.tolist();save(agent,out/f"cycle_{len(events)-1:03d}_after.pt");(out/'epochs.json').write_text(json.dumps(events,indent=2))
agent._update_lambdas=dual
history=agent.train();assert steps==j['steps'];save(agent,out/'training_checkpoint.pt');torch.save(agent.actor.state_dict(),out/'actor.pt');restored=copy.deepcopy(agent.actor);restored.load_state_dict(torch.load(out/'actor.pt',weights_only=True));assert same(restored.state_dict(),agent.actor.state_dict());checkopt=torch.optim.Adam(restored.parameters());checkopt.load_state_dict(agent.actor_optimizer.state_dict());assert same(checkopt.state_dict(),agent.actor_optimizer.state_dict())
e=runner.evaluate_actor(j['env'],j['seed']+1000,agent.actor,'cpu',j['eval_episodes']);final=deltas(initial,agent.actor.state_dict());d=dict(effective_config=dict(arm=j['arm'],reward_estimator='time_loo',inner_reward=j['inner_reward'],outer_reward=j['outer_reward'],risk_mode='excess',metric=j['metric'],scale=j['scale'],c_W=c_w,actual_steps=steps,exploration_steps=j['steps']//2,selection_steps=j['steps']*3//10,acceptance_steps=j['steps']//5,actor_optimizer_steps=accepted_updates,proposal_optimizer_steps=proposal_steps,actor_parameter_delta_l2=float(np.sqrt(sum(v*v for v in final.values()))),module_deltas=final,checkpoint_reload_equal=True,optimizer_reload_equal=True,seed=j['seed'],beta=beta,shaping=5),eval=e,cost_limits=B.tolist(),training_seconds=time.time()-start,training_summary=dict(episodes=len(episodes),raw_reward_mean=float(np.mean([x['raw_reward'] for x in episodes])),shaped_reward_mean=float(np.mean([x['shaped_reward'] for x in episodes])),penalty_mean=float(np.mean([x['penalty'] for x in episodes]))));(out/'result.json').write_text(json.dumps(d,indent=2))
