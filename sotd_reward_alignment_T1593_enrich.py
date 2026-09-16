import json,csv,inspect,dataclasses,sys,hashlib
from pathlib import Path
import numpy as np,torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'snapshot'))
import experiments.run_synthetic_multi_constraint as runner
f=json.loads((R/'findings.json').read_text());rows=list(csv.DictReader((R/'results.csv').open()));effects=list(csv.DictReader((R/'factorial_seed_effects.csv').open()));s=(R/'report.md').read_text();s+='\n## Per-seed reward/joint/any-event outcomes\n\n|Task|Metric|Cell|Seed|Raw reward|Joint|P(any)|\n|---|---|---|---:|---:|---:|---:|\n'
for r in rows:s+='|'+'|'.join([r['env'],r['metric'],r['combo'],r['seed']]+[f"{float(r[k]):.6f}" for k in ['reward','joint','any_event']])+'|\n'
s+='\n## Factorial raw reward effects (individual training seeds)\n\n|Task|Metric|Seed|Inner main effect|Outer main effect|Interaction|\n|---|---|---:|---:|---:|---:|\n'
for r in effects:
 if r['endpoint']=='reward':s+='|'+'|'.join([r['env'],r['metric'],r['seed']]+[f"{float(r[k]):.6f}" for k in ['inner_effect','outer_effect','interaction']])+'|\n'
s+='\nMain effects average the otherfactor as preregistered; interaction is RR−RS−SR+SS. Eachfactor effect contains all3 pairedseeds. These are not a merged algorithm-effect claim or significance test. Full channel/anyrisk effects inCSV. Allresultreward andsuccess are officialrawdet; displayed shaped eval is only counterfactual bookkeeping.\n'
# Post-run exact constructor binding, not new policy training or environment stepping.
original=runner.PPOLagrangian;signature=inspect.signature(original)
def capture(**kwargs):
 bound=signature.bind(**kwargs);bound.apply_defaults();return dict(bound.arguments)
runner.PPOLagrangian=capture;inventory=[]
for p in sorted((R/'jobs').glob('development_*')):
 j=json.loads((p/'job.json').read_text());env=runner.make_synthetic_multi_constraint_env(j['env'],j['seed'],budget_shaping_coef=5);bound=runner.build_ppolag_agent(env,dict(total_steps=j['steps']//2,steps_per_epoch=240,budget_shaping_coef=5));bound.pop('env');ck=torch.load(p/'training_checkpoint.pt',weights_only=False,map_location='cpu');inventory.append(dict(job=j,provenance='Exact constructor binding from frozen builder plus signature defaults, reconstructed post-run; optimizer groups read from actual checkpoint. Zero environment steps.',PPO_constructor=bound,environment=dataclasses.asdict(env.config),actor_optimizer_groups=ck['actor_optimizer']['param_groups'],critic_optimizer_groups=ck['critic_optimizer']['param_groups'],checkpoint_actual_steps=ck['actual_steps'],joint_actor_target=j['inner_reward'],joint_critic_target='shaped MC unchanged',outer_reward_key=j['outer_reward'],joint_timeLOO=True,c_W=json.loads((p/'calibration.json').read_text())['c_W'],shield=False))
runner.PPOLagrangian=original;(R/'effective_runtime_inventory.json').write_text(json.dumps(inventory,indent=2,default=lambda x:x.tolist() if isinstance(x,np.ndarray) else str(x)))
rr=list(csv.DictReader((R/'training_curves.csv').open()));fig,axs=plt.subplots(2,2,figsize=(11,7))
for ei,env in enumerate(['DiagReachK2','DiagReachK3']):
 for met in ['KL','W2']:
  for combo in ['SS','SR','RS','RR']:
   rs=[x for x in rr if (x['env'],x['metric'],x['combo'],x['phase'])==(env,met,combo,'exploration')]
   for ki,key in enumerate(['penalty','excess']):
    vals=[np.mean([max(json.loads(x[key])) if key=='excess' else float(x[key]) for x in rs if int(x['cycle'])==cy]) for cy in range(25)];axs[ei,ki].plot(np.arange(1,26)*480,vals,label=met+'/'+combo,linestyle='-' if met=='KL' else '--');axs[ei,ki].set_title(env+' '+key)
 for ax in axs[ei]:ax.legend(fontsize=6,ncol=2);ax.set_xlabel('Total interactions; half gradient-data')
fig.tight_layout();fig.savefig(R/'training_penalty_excess.png',dpi=170);fig.savefig(R/'training_penalty_excess.svg');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(11,4))
for ki,key in enumerate(['optimism_raw_delta','det_raw_delta']):
 for i,env in enumerate(['DiagReachK2','DiagReachK3']):
  for j,met in enumerate(['KL','W2']):
   rs=[x for x in f['mechanism_seed_pairs'] if (x['env'],x['metric'])==(env,met)];y=np.array([x[key] for x in rs]);lo=np.array([x[key+'_lo'] for x in rs]);hi=np.array([x[key+'_hi'] for x in rs]);axs[ki].errorbar(i*2+j+np.array([-.15,0,.15]),y,yerr=np.maximum(0,np.stack([y-lo,hi-y])),fmt='o',capsize=2,color=['tab:blue','tab:orange'][j])
 axs[ki].axhline(0,color='grey',lw=.7);axs[ki].set_xticks(range(4),['K2KL','K2W2','K3KL','K3W2']);axs[ki].set_title(key+' raw-inner minus shaped-inner');axs[ki].set_ylabel('3seed summaries; conditional eval95% interval')
fig.tight_layout();fig.savefig(R/'mechanism_pairs.png',dpi=170);fig.savefig(R/'mechanism_pairs.svg');plt.close(fig)
fail=json.loads((R/'safety_failures.json').read_text());n=sum(x['earliest_checkpoint_matched_observed_safe_screen_with_final_events'] is not None for x in fail);s+=f'\n## Checkpoint-matched screening failures\n\nOf{len(fail)} finalunsafe jobs, {n} have an accepted actor exactly matching finalparameters, withzeroevents inits4acceptance episodes butevents inindependent312finalepisodes. This establishes finite-screen non-detection for thatpolicy, not thefirsterror amongdifferentearlierpolicies. Allinitialold andunsafe-recovery classifications retained.\n';s+='\nNoheldoutfinalepisode is used forselection or stopping. Additionalconfiginventory is post-run reconstruction fromfrozenconstructor+checkpointmetadata, not anotherin-training sensor. Solver/actor work remains finiteFisher subspace; thisexperimentdoesnotestablish a deploymentconsistent fullMDP OTguarantee.\n';(R/'report.md').write_text(s);f['checkpoint_matched_screen_miss_jobs']=n;(R/'findings.json').write_text(json.dumps(f,indent=2));print(f['status'],'unsafe jobs',len(fail),'matched missed-screen',n)
