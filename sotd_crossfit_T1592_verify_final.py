import json,hashlib,csv
from pathlib import Path
import numpy as np,torch
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
assert (R/'exit_code').read_text().strip()=='0';assert (R/'watcher_exit_code').read_text().strip()=='0';rs=read(R/'receipts.json');assert len(rs)==44 and all(r['verified'] and r['exit_code']==0 for r in rs)
for p,h in read(R/'source_freeze.json').items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
for p,h in read(R/'parent_source_hashes.json').items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
assert read(R/'development_gate.json')['pairs']['time_control_full_replays']==12
count=0
for p in sorted((R/'jobs').glob('mechanism_*')):
 r=read(p/'result.json');assert r['source_unchanged'] and r['CRN'] and r['steps']==7680;B=np.array(r['anchor']['env']=='DiagReachK2' and [6,6] or [7,6.5,12.5]);sample={}
 for k,s in r['stats'].items():
  x=dict(np.load(p/(k+'.npz')));assert len(x['totals'])==64 and x['state'].shape[1]==12;C=x['totals'][:,3:];V=C>B;assert np.array_equal(V.mean(0),s['event']);assert np.allclose(C.mean(0),s['cost_mean']);assert np.array_equal(np.clip(x['proposal'],-1,1),x['executed']);sample[k]=x
 for k,x in sample.items():
  assert np.array_equal(x['environment_noise'],sample['sample_old']['environment_noise'])
  if k.startswith('sample'):assert np.array_equal(x['noise'],sample['sample_old']['noise'])
 assert np.array_equal(np.load(p/'timeKL_contributions.npz')['bootstrap_indices'],np.load(p/'cfKL_contributions.npz')['bootstrap_indices'])
 for label in ['cfKL','cfW2']:
  x=torch.load(p/(label+'.pt'),weights_only=False);b=x['baseline'];assert len(b['folds'])==20
  for f in b['folds']:assert f['heldout_episode'] not in f['fit_episodes'] and len(f['fit_episodes'])==19 and np.min(f['feature_std'])>=1e-6
 count+=1
assert count==12;f=read(R/'findings.json');assert f['ledger']['grand_environment_steps']==478848;assert len(list(csv.DictReader((R/'results.csv').open())))==24;assert len(list(csv.DictReader((R/'mechanism_anchors.csv').open())))==48
(R/'final_verification.json').write_text(json.dumps(dict(status='PASS',development=24,smoke=8,mechanism=12,exact_time_control_replays=12,all44_exit0=True,source_hashes_unchanged=True,baseline_folds_and_CRN_and_risk=True,total_environment_steps=478848),indent=2));print('PASS:44 receipts,12 exact controls, fixed sources,12 mechanism anchors, full478848 environment-step ledger.')
