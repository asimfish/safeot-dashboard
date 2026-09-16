import json
from pathlib import Path
R=Path(__file__).resolve().parent;bank=json.loads((R.parents[1]/'surrogate_gap_decomposition/v1/bank.json').read_text())['anchors'];new={s for b in bank if b['cycle'] in [6,18] for s in range(3830000000+b['anchor']*10000,3830000000+b['anchor']*10000+64)};seen=set();sources=set(Path(b['source']) for b in bank)
for root in ['crossfit_reward_baseline/v1/jobs','joint_metric_solver/v1/jobs']:
 sources.update(p for p in (R.parents[1]/root).glob('development_*'))
for p in sources:
 for l in (p/'training_episodes.jsonl').open():
  s=json.loads(l).get('seed')
  if s is not None:seen.add(s)
 d=json.loads((p/'result.json').read_text());seen.update(x['seed'] for x in d['eval']['episodes']);seen.add(d['effective_config']['seed'])
for root in ['surrogate_gap_decomposition/v1/jobs','surrogate_gap_decomposition/v1/retries2','crossfit_reward_baseline/v1/jobs']:
 for p in (R.parents[1]/root).rglob('episodes.jsonl'):
  for l in p.open():seen.add(json.loads(l)['seed'])
assert not new&seen;(R/'seed_audit.json').write_text(json.dumps(dict(status='PASS',new_seed_min=min(new),new_seed_max=max(new),unique_new_seeds=len(new),known_prior_unique_seeds=len(seen),overlap=0),indent=2));print('seed audit PASS')
