import json,hashlib,csv
from pathlib import Path
R=Path(__file__).resolve().parent
for i in range(30):
 d=R/('retries2/formal_21' if i==21 else f'jobs/formal_{i:02d}');r=json.loads((d/'result.json').read_text());q=json.loads((d/'receipt.json').read_text());assert q['verified'] and q['exit_code']==0 and r['training_steps']==0 and r['fresh_bank_steps']==15360;assert r['checkpoint_hashes_unchanged'];assert sum(1 for l in (d/'episodes.jsonl').open())==1280
 for p,h in r['anchor']['hashes'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
for i in [0,15]:assert json.loads((R/f'jobs/smoke_{i:02d}/receipt.json').read_text())['verified']
f=json.loads((R/'findings.json').read_text());assert f['grand_total_steps']==467808;assert len(list(csv.DictReader((R/'seed_decomposition.csv').open())))==66;assert len(list(csv.DictReader((R/'anchor_decomposition.csv').open())))==330
source=R.parents[2]/'experiments/safeot_dual/progress_feed.json';old=json.loads((R/'persistent_feed_before.json').read_text());new=json.loads(source.read_text());assert new['owner']==old['owner'];assert all(x in new['entries'] for x in old['entries']);assert sum(x.get('task_id')=='T-1591' for x in new['entries'])==1
assert max(json.loads((R/'precision_audit.json').read_text())['max_abs_episode_return_difference'])<2.1e-6
print('PASS: 30 formal + 2 smoke receipts, 38400 formal episodes, 467808 all evaluation steps, immutable checkpoints, 66 seed/channel and330 anchor/channel rows, persistent feed preservation.')
