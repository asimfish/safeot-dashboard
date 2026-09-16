import json,hashlib,time,subprocess,concurrent.futures
from pathlib import Path
import requests
R=Path(__file__).resolve().parent;P=R/'publish';base='https://raw.githubusercontent.com/asimfish/safeot-dashboard/data/';names=['sotd_progress_feed.json','sotd_reward_alignment_T1593_report.md']
def fetch(n):
 u=base+n+'?t1593='+str(time.time_ns());q=requests.get(u,timeout=45);q.raise_for_status();return n,q,u
out={}
with concurrent.futures.ThreadPoolExecutor(2) as pool:
 for n,q,u in pool.map(fetch,names):
  x=dict(status=q.status_code,sha256=hashlib.sha256(q.content).hexdigest(),cache=q.headers.get('X-Cache'),url=u)
  if n=='sotd_progress_feed.json':
   d=q.json();old=json.loads((R/'feed_remote_before.json').read_text());x.update(T1593_in_first14=any(e.get('task_id')=='T-1593' for e in d['entries'][:14]),T1592_preserved=any(e.get('task_id')=='T-1592' for e in d['entries']),T1591_preserved=any(e.get('task_id')=='T-1591' for e in d['entries']),old_entries_preserved=all(e in d['entries'] for e in old['entries']),owner_preserved=d['owner']==old['owner'],entries=len(d['entries']));assert all(x[k] for k in ['T1593_in_first14','T1592_preserved','T1591_preserved','old_entries_preserved','owner_preserved'])
  else:x['matches_local']=q.content==(R/'report.md').read_bytes();assert x['matches_local']
  out[n]=x
h=requests.get('https://asimfish.github.io/safeot-dashboard/?t1593='+str(time.time_ns()),timeout=45);h.raise_for_status();out['homepage']=dict(status=h.status_code,reads_actual_feed='sotd_progress_feed.json' in h.text,first14='slice(0,14)' in h.text.replace(' ',''));assert out['homepage']['reads_actual_feed'] and out['homepage']['first14']
source=Path('experiments/safeot_dual/progress_feed.json');d=json.loads(source.read_text());out.update(evidence_commit=json.loads((R/'publication_pending.json').read_text())['evidence_commit'],feed_commit=subprocess.check_output(['git','-C',str(P),'rev-parse','HEAD'],text=True).strip(),source_contains_entry=any(x.get('task_id')=='T-1593' for x in d['entries']),persistent_source=str(source),persistent_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),producer='experiments/safeot_dual/dashboard_push.py:651-653 reads persistent source and dumps sotd_progress_feed.json',producer_source_sha256=hashlib.sha256(Path('experiments/safeot_dual/dashboard_push.py').read_bytes()).hexdigest(),status='verified');assert out['source_contains_entry'];(R/'publication_receipt.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
