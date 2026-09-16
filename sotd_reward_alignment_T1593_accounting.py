"""Post-run accounting only: no environment interactions or parameter updates."""
import json, csv, hashlib
from pathlib import Path
from datetime import datetime, timezone
R=Path(__file__).resolve().parent
receipts=json.loads((R/'receipts.json').read_text());manifest=json.loads((R/'manifest.json').read_text())
ledger=[];intervals=[]
for rec in receipts:
 p=R/'jobs'/rec['job'];j=json.loads((p/'job.json').read_text());d=json.loads((p/'result.json').read_text())
 if j['phase']=='mechanism': train=0;ev=d['steps'];episodes=d['episodes'];gradient=0
 else: train=j['steps'];ev=j['eval_episodes']*12;episodes=j['eval_episodes'];gradient=train//2
 ledger.append(dict(job=rec['job'],phase=j['phase'],pid=rec['pid'],exit_code=rec['exit_code'],verified=rec['verified'],training_steps=train,gradient_data_steps=gradient,evaluation_diagnostic_steps=ev,final_or_diagnostic_episodes=episodes,worker_wall_seconds=rec['end']-rec['start'],start_utc=datetime.fromtimestamp(rec['start'],timezone.utc).isoformat(),end_utc=datetime.fromtimestamp(rec['end'],timezone.utc).isoformat(),command=rec['command'],source_hashes_file='source_freeze.json',result_sha256=rec['result_sha256']))
 intervals.append((rec['start'],rec['end']))
merged=[]
for a,b in sorted(intervals):
 if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
 else:merged.append([a,b])
x=dict(jobs=ledger,controller_pid=manifest['pid'],start_utc=datetime.fromtimestamp(manifest['start'],timezone.utc).isoformat(),end_utc=datetime.fromtimestamp(manifest['end'],timezone.utc).isoformat(),controller_wall_seconds=manifest['end']-manifest['start'],worker_seconds_sum=sum(x['worker_wall_seconds'] for x in ledger),worker_union_seconds=sum(b-a for a,b in merged),training_steps=sum(x['training_steps'] for x in ledger),gradient_data_steps=sum(x['gradient_data_steps'] for x in ledger),evaluation_diagnostic_steps=sum(x['evaluation_diagnostic_steps'] for x in ledger),raw_step_gate_extra_steps=144,failures=[r for r in receipts if not r['verified']],interpretation='Worker wall time includes training/evaluation/I/O; not claimed as pure optimizer time or additional training hours. Formal final evaluations and mechanism diagnostics are not gradient data.')
x['actual_total_steps']=x['training_steps']+x['evaluation_diagnostic_steps']+144;assert x['actual_total_steps']==864528
(R/'run_accounting.json').write_text(json.dumps(x,indent=2))
rows=[]
for p in sorted((R/'jobs').glob('mechanism_*')):
 d=json.loads((p/'result.json').read_text())
 for label,g in d['gains'].items():
  for k,ch in enumerate(g['channels']):
   for index,name in enumerate(['optimism_sample','optimism_det','Gsample','Gdet','Ghold_timeLOO']):
    rows.append(dict(anchor=d['anchor']['anchor'],env=d['anchor']['env'],seed=d['anchor']['seed'],cycle=d['anchor']['cycle'],candidate=label,channel=ch,quantity=name,value=g[name][k],conditional_ci95_low=g['bootstrap_ci95'][0][index][k],conditional_ci95_high=g['bootstrap_ci95'][1][index][k]))
with (R/'mechanism_all_intervals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({k:v for k,v in x.items() if k!='jobs'},indent=2))
