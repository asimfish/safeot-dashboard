import json,hashlib,csv
from pathlib import Path
import numpy as np,torch
from core import same
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
assert (R/'exit_code').read_text().strip()=='0' and (R/'watcher_exit_code').read_text().strip()=='0';receipts=read(R/'receipts.json');assert len(receipts)==76 and all(x['exit_code']==0 and x['verified'] for x in receipts)
for name,h in read(R/'source_freeze.json').items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
for name,h in read(R/'parent_source_hashes.json').items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,name
assert read(R/'development_gate.json')['pairs']['time_control_full_replays']==12
for p in (R/'jobs').glob('development_*'):
 for i in range(25):
  x=torch.load(p/f'cycle_{i:03d}_rewards.pt',weights_only=False);assert torch.allclose(x['shaped'],x['raw']-x['penalty'],atol=1e-5,rtol=2e-7)
  old=torch.load(p/f'cycle_{i:03d}_batch.pt',weights_only=False);assert torch.equal(old['rewards'],x['shaped'])
  for m in ['KL','W2']:
   b=torch.load(p/f'cycle_{i:03d}_{m}_baseline.pt',weights_only=False);expected=x['shaped'] if b['actor_reward_target']=='shaped' else x['raw'];target=expected.reshape(20,12).flip(1).cumsum(1).flip(1).reshape(-1);assert torch.equal(target,b['targets'])
for p in (R/'jobs').glob('mechanism_*'):
 r=read(p/'result.json');assert r['steps']==7680 and r['source_unchanged'] and r['CRN'];B=np.array([6,6] if r['anchor']['env'].endswith('2') else [7,6.5,12.5]);old=dict(np.load(p/'sample_old.npz'))
 for kernel,st in r['stats'].items():
  x=dict(np.load(p/(kernel+'.npz')));v=x['totals'][:,3:]>B;assert np.array_equal(v.mean(0),st['event']);assert np.array_equal(x['environment_noise'],old['environment_noise']);assert np.array_equal(x['state'][:,0],old['state'][:,0]);assert np.array_equal(np.clip(x['proposal'],-1,1),x['executed']);assert len(x['totals'])==64
  if kernel.startswith('sample'):assert np.array_equal(x['noise'],old['noise'])
 for label,g in r['gains'].items():
  q=0 if label.startswith('shaped') else 1;assert abs(g['Gtrain'][q]-r['solver'][label]['reward_gain'])<1e-5
 assert np.array_equal(np.load(p/'rawKL_contributions.npz')['bootstrap_indices'],np.load(p/'shapedKL_contributions.npz')['bootstrap_indices'])
assert len(list(csv.DictReader((R/'results.csv').open())))==48;assert len(list(csv.DictReader((R/'eval_episodes.csv').open())))==14976;f=read(R/'findings.json');assert f['ledger']['actual_total']==864528
(R/'final_verification.json').write_text(json.dumps(dict(status='PASS',smoke=16,development=48,mechanism=12,all76_exit0=True,exact_SS_full_replays=12,raw_shaped_actor_critic_targets=True,source_hashes_preserved=True,mechanism_CRN_proposals_risks=True,actual_total_steps=864528),indent=2));print('PASS:76jobs,12exactSS controls,rawtarget/PPO invariants,mechanismCRN and 864528 steps')
