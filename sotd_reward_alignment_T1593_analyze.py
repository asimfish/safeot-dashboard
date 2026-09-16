import json,csv,hashlib,sys
from pathlib import Path
import numpy as np,torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from core import same
R=Path(__file__).resolve().parent
assert (R/'exit_code').read_text().strip()=='0'
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,default=lambda x:x.item()))
def csvout(name,rows):
 with (R/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[];evals=[];curves=[];epochs_rows=[];failures=[]
for p in sorted((R/'jobs').glob('development_*')):
 j=read(p/'job.json');d=read(p/'result.json');rec=read(p/'receipt.json');assert rec['verified'] and rec['exit_code']==0;B=np.array(d['cost_limits']);e=d['eval'];C=np.array([x['costs'] for x in e['episodes']]);V=C>B;base={k:j[k] for k in ['env','seed','metric','combo','inner_reward','outer_reward']};base['job']=p.name;pen=[]
 for ep in e['episodes']:
  cs=np.array([x['cost'] for x in ep['trace']],np.float32);pp=5*float(np.maximum(np.cumsum(cs,0)/B.astype(np.float32)-np.arange(1,13,dtype=np.float32)[:,None]/12,0).sum());pen.append(pp);evals.append(dict(**base,eval_seed=ep['seed'],raw_reward=ep['reward'],counterfactual_shaped=ep['reward']-pp,penalty=pp,success=ep['success'],joint=ep['joint_pass'],costs=json.dumps(ep['costs']),events=json.dumps(ep['violations']),any_event=bool(any(ep['violations'])),excess=json.dumps(np.maximum(np.array(ep['costs'])/B-1,0).tolist())))
 tr=[json.loads(l) for l in (p/'training_episodes.jsonl').open()];ee=read(p/'epochs.json');cfg=d['effective_config'];assert len(ee)==25;events=[]
 for x in ee:
  cy=x['cycle'];info=x['joint_infos'][j['metric']]
  for phase in ['exploration','selection','acceptance']:
   rr=[q for q in tr if q['cycle']==cy and (q['phase']=='exploration' if phase=='exploration' else q['phase'].startswith('select_') if phase=='selection' else q['phase'].startswith('accept_'))];c=np.array([q['costs'] for q in rr]);v=c>B;curves.append(dict(**base,cycle=cy,steps=(cy+1)*480,phase=phase,episodes=len(rr),raw_reward=float(np.mean([q['raw_reward'] for q in rr])),shaped_reward=float(np.mean([q['shaped_reward'] for q in rr])),penalty=float(np.mean([q['penalty'] for q in rr])),joint=float(np.mean([q['joint'] for q in rr])),any_event=float(v.any(1).mean()),cost_mean=json.dumps(c.mean(0).tolist()),event=json.dumps(v.mean(0).tolist()),excess=json.dumps(np.maximum(c/B-1,0).mean(0).tolist())))
  epochs_rows.append(dict(**base,cycle=cy,source=x['source'],accepted=x['accepted'],effective_update=x['effective_update'],selection_flip=x['selection_reward_flip'],acceptance_flip=x['acceptance_reward_flip'],actual_score=json.dumps(x['actual_score']),raw_selection=json.dumps(x['raw_selection']),shaped_selection=json.dumps(x['selection']),reward_key=x['outer_reward'],solver_active=info['distance_active'],solver_accepted=info['accepted'],solver_recovery=info['recovery'],actor_reward_target=info['actor_reward_target'],actor_gain=info['reward_gain'],actor_target_return=info['actor_target_return_mean'],critic_shaped_return=info['finite_reward_return_mean'],Jhat=json.dumps(info['Jhat']),predicted_cost=json.dumps(info['actual_predicted_cost']),seconds=info['seconds']))
  if x['accepted'] and x['effective_update']:
   old=x['acceptance_old_risk'];new=x['acceptance_new_risk'];kind='observed_safe_screen' if old['event_free'] and new['event_free'] else 'old_already_unsafe_recovery_channel_tradeoff' if np.any(np.array(new['excess'])>old['excess']) else 'old_already_unsafe_recovery';events.append(dict(cycle=cy,source=x['source'],classification=kind,old_four_episode_risk=old,new_four_episode_risk=new,raw_shaped_scores_recorded=True))
 row=dict(**base,reward=e['reward_mean'],success=e['success_rate'],joint=e['joint_pass'],any_event=float(V.any(1).mean()),cost_mean=json.dumps(C.mean(0).tolist()),event=json.dumps(V.mean(0).tolist()),excess=json.dumps(np.maximum(C/B-1,0).mean(0).tolist()),counterfactual_shaped_reward=float(e['reward_mean']-np.mean(pen)),penalty=float(np.mean(pen)),gradient_steps=cfg['exploration_steps'],selection_steps=cfg['selection_steps'],acceptance_steps=cfg['acceptance_steps'],actual_steps=cfg['actual_steps'],PPO_optimizer_steps=cfg['proposal_optimizer_steps'],installs=cfg['actor_optimizer_steps'],middle_selected=sum(x['source']=='joint_'+j['metric'] for x in ee),middle_installed=sum(x['source']=='joint_'+j['metric'] and x['effective_update'] for x in ee),selection_reward_flips=sum(x['selection_reward_flip'] for x in ee),acceptance_reward_flips=sum(x['acceptance_reward_flip'] for x in ee),wall_seconds_training_finaleval=d['training_seconds']);rows.append(row)
 if V.any():
  final=torch.load(p/'training_checkpoint.pt',weights_only=False,map_location='cpu')['actor'];matching=[]
  for ev in events:
   post=torch.load(p/f"cycle_{ev['cycle']:03d}_postselection.pt",weights_only=False,map_location='cpu')['actor'];ev['same_actor_as_final']=same(post,final)
   if ev['same_actor_as_final']:matching.append(ev)
  initial_actor=torch.load(p/'cycle_000_old.pt',weights_only=False,map_location='cpu')['actor'];first_confirmed=next((x for x in matching if x['new_four_episode_risk']['event_free']),None)
  failures.append(dict(**base,final_matches_initial_actor=same(initial_actor,final),first_cycle_old_four_episode_risk=ee[0]['acceptance_old_risk'],earliest_checkpoint_matched_observed_safe_screen_with_final_events=first_confirmed,final_eval_any_event=float(V.any(1).mean()),final_event_by_channel=V.mean(0).tolist(),final_episode_seeds=[x['seed'] for x in e['episodes']],first_effective_accept=events[0] if events else None,earliest_accepted_actor_identical_to_final=matching[0] if matching else None,all_effective_accepts=events,interpretation='Only matching-final actors have independent312episode risk evidence; other earlier candidates remain unmeasured. Observed-safe4 vs finalevents supports finite-screen missed risk for identical actor, not a claimed earliest causal learning error.'))
assert len(rows)==48;csvout('results.csv',rows);csvout('eval_episodes.csv',evals);csvout('training_curves.csv',curves);csvout('epoch_diagnostics.csv',epochs_rows);dump(R/'safety_failures.json',failures)
groups=[];factorial=[]
for env in ['DiagReachK2','DiagReachK3']:
 for met in ['KL','W2']:
  for combo in ['SS','SR','RS','RR']:
   rr=[r for r in rows if (r['env'],r['metric'],r['combo'])==(env,met,combo)];groups.append(dict(env=env,metric=met,combo=combo,reward=float(np.mean([r['reward'] for r in rr])),joint=float(np.mean([r['joint'] for r in rr])),success=float(np.mean([r['success'] for r in rr])),any_event=float(np.mean([r['any_event'] for r in rr])),cost_mean=np.mean([json.loads(r['cost_mean']) for r in rr],0).tolist(),event=np.mean([json.loads(r['event']) for r in rr],0).tolist(),excess=np.mean([json.loads(r['excess']) for r in rr],0).tolist(),worst_joint=min(r['joint'] for r in rr),worst_reward=min(r['reward'] for r in rr),all_seed_observed_safe=all(r['joint']==1 and r['any_event']==0 for r in rr)))
  for seed in [180,186,187]:
   rr={r['combo']:r for r in rows if (r['env'],r['metric'],r['seed'])==(env,met,seed)}
   for metric in ['reward','success','joint','any_event','installs','middle_selected','middle_installed']+['cost_mean','event','excess']:
    vals={c:np.asarray(json.loads(r[metric]) if metric in ['cost_mean','event','excess'] else r[metric]) for c,r in rr.items()};inn=((vals['RS']-vals['SS'])+(vals['RR']-vals['SR']))/2;out=((vals['SR']-vals['SS'])+(vals['RR']-vals['RS']))/2;inter=vals['RR']-vals['RS']-vals['SR']+vals['SS'];factorial.append(dict(env=env,metric=met,seed=seed,endpoint=metric,inner_effect=json.dumps(inn.tolist()),outer_effect=json.dumps(out.tolist()),interaction=json.dumps(inter.tolist())))
csvout('factorial_seed_effects.csv',factorial);decisions=[]
for met in ['KL','W2']:
 for combo in ['SR','RS','RR']:
  tasks=[]
  for env in ['DiagReachK2','DiagReachK3']:
   g=next(g for g in groups if (g['env'],g['metric'],g['combo'])==(env,met,combo));safe=[x for x in groups if x['env']==env and x['combo']=='SS' and x['all_seed_observed_safe']];best=max((x['reward'] for x in safe),default=None);ok=g['all_seed_observed_safe'] and best is not None and g['reward']>=best+.05 and (env!='DiagReachK2' or g['reward']>9.365684);tasks.append(dict(env=env,passed=ok,best_safe_SS=best,required_margin=.05,candidate=g))
  decisions.append(dict(metric=met,combo=combo,passed=all(t['passed'] for t in tasks),tasks=tasks))
mech=[];mrisk=[];mp={}
for p in sorted((R/'jobs').glob('mechanism_*')):
 r=read(p/'result.json');a=r['anchor'];base={k:a[k] for k in ['env','seed','cycle','anchor']};assert r['source_unchanged'] and r['steps']==7680
 for label,g in r['gains'].items():
  for q,ch in enumerate(g['channels']):
   ci=np.array(g['bootstrap_ci95']);mech.append(dict(**base,candidate=label,channel=ch,Gtrain=g['Gtrain'][q],Ghold=g['Ghold_timeLOO'][q],Gsample=g['Gsample'][q],Gdet=g['Gdet'][q],optimism=g['optimism_sample'][q],optimism_lo=ci[0,0,q],optimism_hi=ci[1,0,q],Gdet_lo=ci[0,3,q],Gdet_hi=ci[1,3,q],hold_episode_contribution_std=g['hold_contribution_std'][q],sample_episode_contribution_std=g['sample_contribution_std'][q]))
 for kernel,st in r['stats'].items():mrisk.append(dict(**base,kernel=kernel,raw_reward=st['raw_reward'],shaped_reward=st['shaped_reward'],penalty=st['penalty'],joint=st['joint'],success=st['success'],any_event=st['any_event'],cost_mean=json.dumps(st['cost_mean']),event=json.dumps(st['event']),excess=json.dumps(st['excess'])))
 for met in ['KL','W2']:
  raw=r['gains']['raw'+met];sh=r['gains']['shaped'+met];rb=np.load(p/('raw'+met+'_contributions.npz'))['bootstrap'];sb=np.load(p/('shaped'+met+'_contributions.npz'))['bootstrap'];mp.setdefault((a['env'],met,a['seed']),[]).append(dict(optimism_raw_delta=raw['optimism_sample'][1]-sh['optimism_sample'][1],sample_raw_delta=raw['Gsample'][1]-sh['Gsample'][1],det_raw_delta=raw['Gdet'][1]-sh['Gdet'][1],sample_shaped_delta=raw['Gsample'][0]-sh['Gsample'][0],det_shaped_delta=raw['Gdet'][0]-sh['Gdet'][0],bootstrap=rb-sb))
assert len(mp)==12;csvout('mechanism_anchors.csv',mech);csvout('mechanism_risks.csv',mrisk);mpairs=[]
for (env,met,seed),rr in mp.items():
 assert len(rr)==2;ci=np.quantile(np.mean([x['bootstrap'] for x in rr],0),[.025,.975],axis=0);out=dict(env=env,metric=met,seed=seed)
 for key,index in [('optimism_raw_delta',(0,1)),('sample_raw_delta',(2,1)),('det_raw_delta',(3,1)),('sample_shaped_delta',(2,0)),('det_shaped_delta',(3,0))]:out[key]=float(np.mean([x[key] for x in rr]));out[key+'_lo']=float(ci[0,index[0],index[1]]);out[key+'_hi']=float(ci[1,index[0],index[1]])
 mpairs.append(out)
csvout('mechanism_seed_pairs.csv',mpairs);status='PROMISING_REQUIRES_FRESH_CONFIRMATION' if any(x['passed'] for x in decisions) else 'HOLD_OBJECTIVE_RECIPE';ot=[]
for env in ['DiagReachK2','DiagReachK3']:
 for combo in ['SS','SR','RS','RR']:
  k=next(x for x in groups if (x['env'],x['metric'],x['combo'])==(env,'KL',combo));w=next(x for x in groups if (x['env'],x['metric'],x['combo'])==(env,'W2',combo));ot.append(dict(env=env,combo=combo,reward_W2_minus_KL=w['reward']-k['reward'],both_all_seed_observed_safe=k['all_seed_observed_safe'] and w['all_seed_observed_safe']))
ledger=dict(development_training=576000,gradient_data=288000,selection=172800,acceptance=115200,development_final_eval=179712,smoke_training=15360,smoke_eval=1152,mechanism_diagnostic=92160,planned_total=864384,raw_reward_gate=144,actual_total=864528)
f=dict(status=status,groups=groups,decisions=decisions,OT_contrasts=ot,mechanism_seed_pairs=mpairs,ledger=ledger,unsafe_jobs=len(failures),seed_replicas=3,limitations='Exploratory. Allrisk samples finite; no zero-risk/novelty/native/VLA claim. Factorial effects paired withinseed; mechanism oldKLbank separate fromlearning. Independentfinal risk only attributable to checkpoint-identical accepted actors.');dump(R/'findings.json',f)
fig,axs=plt.subplots(2,3,figsize=(14,7))
for ei,env in enumerate(['DiagReachK2','DiagReachK3']):
 for met in ['KL','W2']:
  for combo in ['SS','SR','RS','RR']:
   rr=[x for x in curves if (x['env'],x['metric'],x['combo'],x['phase'])==(env,met,combo,'exploration')]
   for ki,key in enumerate(['raw_reward','shaped_reward','any_event']):axs[ei,ki].plot(np.arange(1,26)*480,[np.mean([x[key] for x in rr if x['cycle']==cy]) for cy in range(25)],label=met+'/'+combo,linestyle='-' if met=='KL' else '--');axs[ei,ki].set_title(env+' '+key);axs[ei,ki].set_xlabel('Total interaction steps; half gradient-data')
 for ax in axs[ei]:ax.legend(fontsize=6,ncol=2)
fig.tight_layout();fig.savefig(R/'training_curves.png',dpi=170);fig.savefig(R/'training_curves.svg');plt.close(fig)
lines=['# T1593 reward objective alignment factorial','',status,'','SS/SR/RS/RR: firstletter jointactor reward, secondletter outer score; S=shaped,R=raw. PPOalwaysshaping5. Only timeLOO,scale1; c_W common originalshaped anchor. Costs/critics/duals/risks/kernel unchanged. Rawtarget is not shapingenv0 training.','', '## Full development (three training seeds)','', '|Task|Metric|Cell|Raw reward|Success|Joint|P(any)|Worst joint|Cost mean|Channel events|Excess|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for g in groups:lines.append('|'+ '|'.join([g['env'],g['metric'],g['combo']]+[f"{g[k]:.6f}" for k in ['reward','success','joint','any_event','worst_joint']]+[str(np.round(g[k],6).tolist()) for k in ['cost_mean','event','excess']])+'|')
lines+=['','Everyseed in results.csv; actual312episodes in eval_episodes.csv. Factorialinner/outer/interaction effects forreward/success/joint/everyriskchannel/install are in factorial_seed_effects.csv, pairedseed notepisode replication. Raw/shaped/penalty training and risk are phase-separated in training_curves.csv; selection counterfactuals on identical pools and acceptance on identical actualpairs are only local counterfactuals, not learnedpolicy substitutes.','', '## Frozen decision','',json.dumps(decisions,indent=2),'', '## OT separately','',json.dumps(ot,indent=2),'','A rawobjective gain is not an OTinnovation. W2vsKL only comparable as safe reward if samecell bothobserved-safe; no root-cause sufficiency or formal significance claims.','', '## Paired fixed-bank mechanism: raw-inner minus shaped-inner, common RAW units','', '|Task|Metric|Seed|Raw optimism delta [conditional95%]|Real sample raw gain delta|Real det raw gain delta [conditional95%]|','|---|---|---:|---|---:|---|']
for x in mpairs:lines.append(f"|{x['env']}|{x['metric']}|{x['seed']}|{x['optimism_raw_delta']:.5f} [{x['optimism_raw_delta_lo']:.5f},{x['optimism_raw_delta_hi']:.5f}]|{x['sample_raw_delta']:.5f}|{x['det_raw_delta']:.5f} [{x['det_raw_delta_lo']:.5f},{x['det_raw_delta_hi']:.5f}]|")
lines+=['','Allcandidate Gtrain/Ghold/Gsample/Gdet andbootstrap intervals separately raw/shaped/penalty/cost in mechanism_anchors.csv. The primary raw optimism is Gtrain_raw−Gsample_raw for everycandidate; no subtraction acrossrewardunits. 512wholeepisodepaired bootstraps recenterLOO eachdraw; fixedGtrain, conditional evaluationuncertainty only. Three trainingseeds, twofixedanchors each, not24newtrainingreplicas.','', '## Safety failures and inference limits','',f'{len(failures)} finalunsafe jobs. safety_failures.json retains firsteffectiveaccept andevery lateraccept with4episodeold/newrisk. It identifies earliestaccepted actor identical tofinal checkpoint before linking its4sample screen toindependent312eval. Earliernonmatching candidates have noindependentrisklabel; finalfailure cannot retroactively classify them asacceptanceerrors. Recovery oldunsafe/channeltradeoffs are explicit. Nofinaleval changes candidates/stopping/checkpoints.','', '## Gates/accounting/source','', 'Rawsame-action/noise shaping5/0 gate144steps; rawrecovery maxerror below1e-12. Prior60bankcounts confirmed42shaped vs14raw sample-positive/det-nonpositive, and23raw train-positive/det-nonpositive; no claimthatremovingPPOshaping solvesit. Sixfirstbatch shapecandidates exact,costD/critic unchanged,zeroPenalty equality; smoke commonPPO/RNG/calibration;12SS controls require full25cycle/312eval exact replay. Originalbatch unchanged; actor target tensor separate; optimizer/critictransaction checks retained.', '',json.dumps(ledger,indent=2),'', 'No fitting/extra learning samples. All76jobs andnegative outcomes retained; source snapshots/hashes unchanged. Four-episode screening low power remains independent. No automaticradius/feature/seed/CF search or native/VLA expansion. Papers/DERIVATION/PDF read-only.']
(R/'report.md').write_text('\n'.join(lines)+'\n');print(json.dumps(dict(status=status,groups=groups),indent=2))
