import os,time,json,subprocess,datetime
from pathlib import Path
R=Path(__file__).resolve().parent;(R/'watcher.pid').write_text(str(os.getpid()))
while not (R/'exit_code').exists():
 (R/'watcher_heartbeat.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),waiting='controller gated smoke/development/mechanism')));time.sleep(15)
code=int((R/'exit_code').read_text())
if code==0:
 with (R/'analysis.log').open('w') as f:code=subprocess.call(['python3','-u',str(R/'analyze.py')],stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
(R/'watcher_exit_code').write_text(str(code));(R/'final_receipt.json').write_text(json.dumps(dict(exit_code=code,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='analysis_verified_publication_pending' if code==0 else 'failure_preserved')))
