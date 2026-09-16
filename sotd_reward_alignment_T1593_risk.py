import numpy as np

def risk(samples,B,reward_key="shaped",raw_samples=None):
 c=np.asarray(samples)[:,1:];B=np.asarray(B);ex=np.maximum(c/B-1,0).mean(0)
 assert reward_key in ['shaped','raw'];shaped=float(np.asarray(samples)[:,0].mean());raw=float(np.asarray(raw_samples)[:,0].mean()) if raw_samples is not None else None
 assert reward_key=='shaped' or raw is not None
 return dict(reward_key=reward_key,actual_score=shaped if reward_key=='shaped' else raw,raw_reward=raw,mean_cost=c.mean(0).tolist(),event_probability=(c>B).mean(0).tolist(),excess=ex.tolist(),mean_feasible=bool(np.all(c.mean(0)<=B)),event_free=bool(not (c>B).any()),risk_pair=(float(ex.max()),float(ex.sum())),shaped_reward=float(np.asarray(samples)[:,0].mean()))
def choose(samples,B,mode,eligible=None,reward_key="shaped",raw_samples=None):
 eligible=list(range(3)) if eligible is None else eligible
 rs=[risk(x,B,reward_key,None if raw_samples is None else raw_samples[i]) for i,x in enumerate(samples)];sel=[np.mean(x,0) for x in samples]
 if mode=='mean':
  feasible=[i for i in eligible if np.all(sel[i][1:]<=B)]
  if feasible:return max(feasible,key=lambda i:(rs[i]["actual_score"],i)),False,rs
  return min(eligible,key=lambda i:(np.maximum(sel[i][1:]/B-1,0).sum(),-rs[i]["actual_score"])),True,rs
 feasible=[i for i in eligible if rs[i]['event_free']]
 if feasible:return max(feasible,key=lambda i:(rs[i]['actual_score'],i)),False,rs
 return min(eligible,key=lambda i:(*rs[i]['risk_pair'],-rs[i]['actual_score'],-i)),True,rs

def accept(old,new,B,mode,reward_key="shaped",raw_old=None,raw_new=None):
 o,n=risk(old,B,reward_key,raw_old),risk(new,B,reward_key,raw_new);vo=np.mean(old,0);va=np.mean(new,0)
 if mode=='mean':
  oldex=np.maximum(vo[1:]/B-1,0).sum();newex=np.maximum(va[1:]/B-1,0).sum();recovery=oldex>0
  yes=bool(newex<oldex-1e-8 if recovery else np.all(va[1:]<=B) and n['actual_score']>=o['actual_score'])
 else:
  recovery=not o['event_free'];yes=n['risk_pair']<o['risk_pair'] if recovery else n['event_free'] and n['actual_score']>=o['actual_score']
 return bool(yes),bool(recovery),o,n
