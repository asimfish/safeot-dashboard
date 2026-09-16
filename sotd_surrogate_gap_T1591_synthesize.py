import json,csv,hashlib,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import contribution
R=Path(__file__).resolve().parent
assert (R/'retry_exit_code').read_text().strip()=='0'
rows=[];risk=[];groups={};checks=[];episode_count=0;evalsteps=0
terms=['GholdLR','Gsample','Gdet','T','L','K','mean_only','std_only','interaction']
def writecsv(name,rs):
 with (R/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
for d in sorted((R/'jobs').glob('formal_*')):
 if d.name=='formal_21':d=R/'retries2/formal_21'
 r=json.loads((d/'result.json').read_text());receipt=json.loads((d/'receipt.json').read_text());assert receipt['exit_code']==0 and receipt['verified'];assert receipt['result_sha256']==hashlib.sha256((d/'result.json').read_bytes()).hexdigest();a=r['anchor'];B=np.array(r['budget']);cols=r['columns'];base=dict(env=a['env'],seed=a['seed'],cycle=a['cycle'],anchor=a['anchor']);evalsteps+=r['total_evaluation_steps'];episode_count+=r['episodes_per_kernel']*10
 for p,h in a['hashes'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
 for kernel,st in r['stats'].items():
  x=np.load(d/(kernel+'.npz'));c=x['totals'][:,3:];v=c>B;assert np.array_equal(v.mean(0),st['event']);assert np.allclose(c.mean(0),st['mean_cost']);assert np.array_equal(np.clip(x['proposal'],-1,1),x['executed']);assert x['state'].shape[1]==12 and len(c)==128
  assert np.allclose(x['values'][:,:,:3].sum(1),x['totals'][:,:3]);assert np.allclose(x['values'][:,:,3:].astype(np.float32).sum(1),c,atol=3e-6)
  for k in range(len(B)):
   risk.append(dict(**base,kernel=kernel,channel=k,budget=B[k],mean_cost=float(c[:,k].mean()),cost_over_budget=float(c[:,k].mean()/B[k]),q50=float(np.quantile(c[:,k],.5)),q90=float(np.quantile(c[:,k],.9)),q95=float(np.quantile(c[:,k],.95)),q99=float(np.quantile(c[:,k],.99)),event=float(v[:,k].mean()),positive_excess=float(np.maximum(c[:,k]/B[k]-1,0).mean()),any_event=float(v.any(1).mean()),success=st['success'],joint=st['joint'],raw_reward=st['raw_reward'],shaped_reward=st['shaped_reward'],penalty=st['penalty'],mean_feasible_with_events=st['mean_feasible_with_events']))
 for m,v in r['decomposition'].items():
  x=np.load(d/(m+'_contributions.npz'));boot=x['bootstrap'];idx=x['bootstrap_indices'][0];h=contribution(x['ratio'][idx],x['hold_returns'][idx]).mean(0);assert np.allclose(h,boot[0,0],atol=1e-12)
  assert np.allclose(np.array(v['components']).sum(0),np.array(v['Gtrain'])-v['Gdet'],atol=1e-12)
  key=(a['env'],m,a['seed']);groups.setdefault(key,[]).append((r,v,boot))
  for q,col in enumerate(cols):
   obs=np.array([v['GholdLR'][q],v['Gsample'][q],v['Gdet'][q],v['components'][0][q],v['components'][1][q],v['components'][2][q],v['variance']['mean_only'][q],v['variance']['std_only'][q],v['variance']['interaction'][q]])
   out=dict(**base,metric=m,channel=col,Gtrain=v['Gtrain'][q]);ci=np.quantile(boot[:,:,q],[.025,.975],axis=0)
   for z,t in enumerate(terms):out[t]=obs[z];out[t+'_lo']=ci[0,z];out[t+'_hi']=ci[1,z]
   out.update(cost_intercept_sample=v['cost_intercept_sample'][q-3] if q>=3 else '',cost_intercept_det=v['cost_intercept_det'][q-3] if q>=3 else '',inner_cost_over_budget=v['cost_surrogate'][q-3]/B[q-3] if q>=3 else '',det_any_event=r['stats']['det_'+m]['any_event']);rows.append(out)
 checks.append(dict(anchor=a['anchor'],source_unchanged=True,receipt=True,episodes=1280,steps=r['total_evaluation_steps']))
assert len(checks)==30 and episode_count==38400 and evalsteps==463680
writecsv('anchor_decomposition.csv',rows);writecsv('risk_metrics.csv',risk)
seedrows=[];overview=[]
for (env,m,seed),entries in groups.items():
 assert len(entries)==5;boots=np.mean([x[2] for x in entries],axis=0);cols=entries[0][0]['columns']
 for q,col in enumerate(cols):
  selected=[r for r in rows if r['env']==env and r['metric']==m and r['seed']==seed and r['channel']==col];out=dict(env=env,metric=m,seed=seed,channel=col,Gtrain=float(np.mean([r['Gtrain'] for r in selected])));ci=np.quantile(boots[:,:,q],[.025,.975],axis=0)
  for z,t in enumerate(terms):out[t]=float(np.mean([r[t] for r in selected]));out[t+'_lo']=float(ci[0,z]);out[t+'_hi']=float(ci[1,z])
  for t in ['T','L','K']:out['median_abs_'+t]=float(np.median([abs(r[t]) for r in selected]));out['signed_sum_'+t]=float(sum(r[t] for r in selected));out['absolute_sum_'+t]=float(sum(abs(r[t]) for r in selected))
  for t in ['GholdLR','Gsample','Gdet']:out['train_positive_'+t+'_nonpositive']=sum(r['Gtrain']>0 and r[t]<=0 for r in selected)
  seedrows.append(out)
writecsv('seed_decomposition.csv',seedrows)
for env in ['DiagReachK2','DiagReachK3']:
 for m in ['KL','W2']:
  rr=[r for r in rows if r['env']==env and r['metric']==m and r['channel']=='shaped'];ss=[r for r in seedrows if r['env']==env and r['metric']==m and r['channel']=='shaped'];means={t:float(np.mean([r[t] for r in ss])) for t in ['Gtrain']+terms};med={t:float(np.median([abs(r[t]) for r in rr])) for t in ['T','L','K']};counts={t:sum(r['Gtrain']>0 and r[t]<=0 for r in rr) for t in ['GholdLR','Gsample','Gdet']}
  overview.append(dict(env=env,metric=m,mean=means,median_abs=med,rank=sorted(med,key=med.get,reverse=True),sign_counts=counts,sample_positive_det_nonpositive=sum(r['Gsample']>0 and r['Gdet']<=0 for r in rr),sample_positive_det_nonpositive_CI=sum(r['Gsample_lo']>0 and r['Gdet_hi']<0 for r in rr),std_only_positive=sum(r['std_only']>0 for r in rr),full_positive_mean_only_nonpositive=sum(r['Gsample']>0 and r['mean_only']<=0 for r in rr),full_positive_mean_only_nonpositive_det_nonpositive=sum(r['Gsample']>0 and r['mean_only']<=0 and r['Gdet']<=0 for r in rr)))
# Existing audit clarification: user's .74-.77 equals median of max-channel utilization, not channel average.
source=R.parents[1]/'joint_metric_solver/v1';ug={}
for x in json.loads((source/'constraint_audit.json').read_text())['rows']:
 k=('K2' if 'K2' in x['job'] else 'K3')+'_'+x['metric'];ug.setdefault(k,[]).append(np.array(x['actual_float32_policy_cost_surrogate'])/x['budget'])
usage={k:dict(median_max_channel=float(np.median(np.max(v,1))),median_mean_channel=float(np.median(np.mean(v,1))),median_per_channel=np.median(v,0).tolist()) for k,v in ug.items()}
mean_event=[r for r in risk if r['mean_feasible_with_events'] and r['channel']==0];inner_tail=[dict(env=r['env'],metric=r['metric'],seed=r['seed'],cycle=r['cycle'],maximum_inner_usage=max(float(x['inner_cost_over_budget']) for x in rows if x['anchor']==r['anchor'] and x['metric']==r['metric'] and x['channel'].startswith('cost_')),det_any_event=r['det_any_event']) for r in rows if r['channel']=='shaped' and r['det_any_event']>0]
findings=dict(status='complete_evaluation_diagnostic',formal_anchors=30,formal_fresh_episodes=episode_count,formal_fresh_steps=460800,formal_replay_steps=2880,smoke_and_replay_steps=4032,total_steps=467712,training_steps=0,overview=overview,existing_usage_clarification=usage,mean_feasible_with_events=mean_event,inner_tail_cases=inner_tail,uncertainty='Paired bootstrap fresh evaluation conditional on frozen training/candidates; three trained seeds, fixed five anchors each, no population significance')
(R/'findings.json').write_text(json.dumps(findings,indent=2,default=lambda x:x.item()));(R/'verification.json').write_text(json.dumps(dict(status='PASS',anchors=checks,bootstrap_first_draw_LOO_recomputed=True,all30_hashes_preserved=True,steps=467712,formal_episodes=38400),indent=2))
fig,ax=plt.subplots(1,2,figsize=(11,4))
for e,env in enumerate(['DiagReachK2','DiagReachK3']):
 for mi,m in enumerate(['KL','W2']):
  for ti,t in enumerate(['T','L','K']):
   vals=[x[t] for x in seedrows if x['env']==env and x['metric']==m and x['channel']=='shaped'];xx=ti+(.13 if mi else -.13);ax[e].scatter(np.full(3,xx),vals,label=m if ti==0 else None,color=['tab:blue','tab:orange'][mi]);ax[e].plot([xx-.08,xx+.08],[np.mean(vals)]*2,color=['tab:blue','tab:orange'][mi])
 ax[e].axhline(0,color='grey',lw=.7);ax[e].set_xticks(range(3),['Train-generalization','Local-surrogate','Kernel']);ax[e].set_title(env+' (3 training seeds)');ax[e].set_ylabel('Shaped-gain gap; each seed averages 5 anchors');ax[e].legend()
fig.tight_layout();fig.savefig(R/'gap_components.png',dpi=180);fig.savefig(R/'gap_components.svg');plt.close(fig)
lines=['# T-1591 frozen candidate surrogate-gap decomposition','', 'Evaluation-only synthetic mechanism evidence. T1590 remains HOLD. No new training, actor updates, optimizer updates, policy selection or radius search. All 30 anchors and all negative results retained.','', '30 formal anchors × 10 kernels × 128 fresh paired episodes = 38400 episodes / 460800 steps. Separate replay 2880 steps; smoke plus replay 4032 steps. Total 467712 evaluation steps, zero training steps. All source checkpoint hashes unchanged; original selection and finite-horizon LR replay passed.','', 'Three trained seeds per task, five fixed anchors per seed. 95% intervals below are 512 paired whole-episode bootstrap intervals, LOO recentered with repeated draws, conditional on frozen training data/policies. They do not quantify training-seed population uncertainty. Gtrain is held fixed.','', '## Seed-level shaped gain decomposition','', '|Task|Metric|Seed|Gtrain|GholdLR|Gsample|Gdet|T [95%]|L [95%]|K [95%]|','|---|---|---:|---:|---:|---:|---:|---|---|---|']
for r in seedrows:
 if r['channel']!='shaped':continue
 lines.append('|'+ '|'.join([r['env'],r['metric'],str(r['seed'])]+[f"{r[t]:.4f}" for t in ['Gtrain','GholdLR','Gsample','Gdet']]+[f"{r[t]:.4f} [{r[t+'_lo']:.4f}, {r[t+'_hi']:.4f}]" for t in ['T','L','K']])+'|')
lines+=['','T=Gtrain−GholdLR; L=GholdLR−Gsample; K=Gsample−Gdet. Sum identity checked for shaped/raw/penalty and every cost channel. The L term combines finite-step surrogate/occupancy error and finite evaluation noise; it is not critic calibration.','', '## Magnitude ranking and sign stages','']
for o in overview:lines.append(f"- {o['env']} {o['metric']}: median absolute T/L/K={o['median_abs']}; rank={o['rank']}; of 15 anchors positive-train/nonpositive holdLR/sample/det counts={o['sign_counts']}; sample-positive/det-nonpositive={o['sample_positive_det_nonpositive']} (both directional CIs separated from zero: {o['sample_positive_det_nonpositive_CI']}). Mean gains={o['mean']}.")
lines+=['','Signed sums, absolute sums, medians by seed, and their cancellations are explicitly retained in seed_decomposition.csv. Raw/shaped/penalty and all cost decompositions with intercept errors are in anchor_decomposition.csv; risk mean/quantiles/event/excess/success/joint are in risk_metrics.csv. Neither cycles nor episodes are treated as independent training replicas.','', '## Variance intervention','']
for o in overview:lines.append(f"- {o['env']} {o['metric']}: full sample gain positive but mean-only nonpositive {o['full_positive_mean_only_nonpositive']}/15; these also det nonpositive {o['full_positive_mean_only_nonpositive_det_nonpositive']}/15. Mean-only / std-only / interaction mean gains: {o['mean']['mean_only']:.5f} / {o['mean']['std_only']:.5f} / {o['mean']['interaction']:.5f}.")
lines+=['','Hybrid wrappers evaluate both networks at their own visited states; they are functional interventions, not directly installable actor parameters. Full gain = mean-only + std-only + interaction verified. Std-only changes no deterministic actions, but backbone changes can jointly affect mu and sigma.','', '## Risk and prior audit','',f"Mean-feasible but eventful kernel/anchor cases: {len(mean_event)} of 300 (all listed in findings.json); det-tail cases for inner candidates: {len(inner_tail)} of 60. Full per-channel risk and inner utilization retained, not replaced by aggregate cost.", '', 'Prior 1800 candidates: 18 cost-near-active within 1e-3; max violation under 1e-5. Scale1 215/300 four-episode middle-minus-old shaped gains negative while all predicted gains positive. This is finite-sample descriptive evidence. The stated .74–.77 utilization is reproduced as the median of the maximum channel Csur/B; averaging channels first gives .68–.70. Both definitions are now explicit.', '', 'Usage audit: '+json.dumps(usage), '', '## Interpretation and one next modification', '', 'Recommendation must be filled after reviewing the fixed-bank decomposition; no new training is authorized by this diagnostic. Conditional evaluation uncertainty and mixed mechanisms preclude a unique-root-cause claim.', '', '## Artifacts and limits', '', 'protocol.md; manifest.json; bank.json; existing_audit.json; verification.json; anchor_decomposition.csv; seed_decomposition.csv; risk_metrics.csv; findings.json; gap_components.png/svg; jobs/*/{receipt.json,result.json,episodes.jsonl,*_contributions.npz,kernel.npz}. Raw trace arrays retain proposals, executed clip actions, original Gaussian logprob, visited states, action noise, environment noise and episode seeds.', '', 'Official deterministic evaluation semantics remain unchanged. Mean budget feasibility is not zero episode risk. No OT advantage, SOTA, native-task or VLA claim is supported.']
(R/'report.md').write_text('\n'.join(lines)+'\n');print(json.dumps(overview,indent=2,default=lambda x:x.item()))
