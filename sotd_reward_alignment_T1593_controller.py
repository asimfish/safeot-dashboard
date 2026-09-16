import os,sys,json,time,hashlib,subprocess,concurrent.futures,fcntl,traceback
from pathlib import Path
R=Path(__file__).resolve().parent;lock=(R/'lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);assert not (R/'manifest.json').exists();(R/'pid').write_text(str(os.getpid()))
env=dict(os.environ,OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1');mem=int([x for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable')][0].split()[1]);cpus=len(os.sched_getaffinity(0));lanes=3 if os.getloadavg()[0]<cpus-3 and mem>8*1024**2 else 1
m=dict(start=time.time(),pid=os.getpid(),status='running',phase='smoke',lanes=lanes,cpus=cpus,load=os.getloadavg(),mem_available_kb=mem,hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and p.suffix in ['.py','.md'] and 'offline_failure_1' not in p.parts});receipts=[]
def persist():(R/'manifest.json').write_text(json.dumps(m,indent=2));(R/'receipts.json').write_text(json.dumps(receipts,indent=2))
def run(j):
 tag=f"{j['phase']}_{j['env']}_s{j['seed']}_{j['arm']}";p=R/'jobs'/tag;p.mkdir(parents=True,exist_ok=False);(p/'job.json').write_text(json.dumps(j));cmd=[sys.executable,'-u',str(R/('mechanism.py' if j['phase']=='mechanism' else 'worker.py')),str(p/'job.json')];(p/'command.json').write_text(json.dumps(cmd));start=time.time()
 with (p/'stdout').open('w') as so,(p/'stderr').open('w') as se:
  proc=subprocess.Popen(cmd,stdout=so,stderr=se,env=env);(p/'pid').write_text(str(proc.pid));timeout=False
  try:proc.wait(timeout=2400)
  except subprocess.TimeoutExpired:proc.kill();proc.wait();timeout=True
 (p/'exit_code').write_text(str(proc.returncode));ok=False
 if proc.returncode==0 and j['phase']=='mechanism':
  d=json.loads((p/'result.json').read_text());ok=d['status']=='verified' and d['steps']==7680 and d['episodes']==640
 elif proc.returncode==0:
  d=json.loads((p/'result.json').read_text());ok=d['effective_config']['actual_steps']==j['steps'] and d['effective_config']['checkpoint_reload_equal'] and len(d['eval']['episodes'])==j['eval_episodes']
 rec=dict(job=tag,command=cmd,pid=proc.pid,start=start,end=time.time(),exit_code=proc.returncode,verified=ok,timeout=timeout,result_sha256=hashlib.sha256((p/'result.json').read_bytes()).hexdigest() if (p/'result.json').exists() else None);(p/'receipt.json').write_text(json.dumps(rec));return rec
def phase(name,seeds,steps,evals):
 m['phase']=name
 if name=='mechanism':
  bank=json.loads((R.parents[1]/'surrogate_gap_decomposition/v1/bank.json').read_text())['anchors'];jobs=[dict(phase=name,env=b['env'],seed=b['seed'],arm='anchor'+str(b['anchor']),anchor=b['anchor']) for b in bank if b['cycle'] in [6,18]]
 else:jobs=[dict(phase=name,env=e,seed=s,arm=metric+'_'+combo,metric=metric,combo=combo,inner_reward='shaped' if combo[0]=='S' else 'raw',outer_reward='shaped' if combo[1]=='S' else 'raw',estimator='time_loo',scale=1.,steps=steps,eval_episodes=evals) for e in ['DiagReachK2','DiagReachK3'] for s in seeds for metric in ['KL','W2'] for combo in ['SS','SR','RS','RR']]
 m[name+'_jobs']=jobs;persist()
 with concurrent.futures.ThreadPoolExecutor(lanes) as ex:
  fs={ex.submit(run,j) for j in jobs}
  while fs:
   done,fs=concurrent.futures.wait(fs,timeout=5,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in done:
    try:receipts.append(f.result())
    except Exception:receipts.append(dict(verified=False,error=traceback.format_exc()))
   persist();(R/'heartbeat.json').write_text(json.dumps(dict(time=time.time(),pid=os.getpid(),phase=name,remaining=len(fs),completed=len(receipts))))
 assert all(x['verified'] for x in receipts)
 if name=='mechanism':return
 with (R/(name+'_gate.log')).open('w') as log:r=subprocess.run([sys.executable,str(R/'verify.py'),name],stdout=log,stderr=subprocess.STDOUT,env=env)
 assert r.returncode==0,name+' verification failed'
code=1
try:
 assert all(json.loads((R/n).read_text())['status']=='PASS' for n in ['gate.json'])
 persist();phase('smoke',[180],960,6);phase('development',[180,186,187],12000,312);phase('mechanism',[],0,0);m['status']='complete';code=0
except Exception:m['status']='failed';(R/'failure.txt').write_text(traceback.format_exc())
finally:m['end']=time.time();persist();(R/'exit_code').write_text(str(code))
