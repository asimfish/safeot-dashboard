import copy
import numpy as np,torch

def targets(values):
 x=torch.as_tensor(values,dtype=torch.float32)
 return x.flip(1).cumsum(1).flip(1)

def contribution(ratio,target):
 t=torch.as_tensor(target,dtype=torch.float32);n=len(t);cen=(t-t.mean(0))*n/(n-1)
 return ((np.asarray(ratio)-1)[...,None]*cen.double().numpy()).sum(1)

def lr(actor,old,states,actions):
 a=copy.deepcopy(actor).double();o=copy.deepcopy(old).double()
 with torch.no_grad():
  s=torch.as_tensor(states,dtype=torch.double);u=torch.as_tensor(actions,dtype=torch.double);delta=a.log_prob(s,u)-o.log_prob(s,u)
 return delta.exp().numpy()

class RecordingRNG:
 def __init__(self,rng):self.rng=rng;self.noises=[]
 def normal(self,*a,**k):
  v=self.rng.normal(*a,**k);self.noises.append(v.astype(np.float32));return v

def load_actor(runner,env,ck):
 a=runner.build_ppolag_agent(env,dict(total_steps=6000,steps_per_epoch=240)).actor;a.load_state_dict(ck['actor']);a.eval();return a

def bootstrap(ratios,target,totals,train_gain,metric,n_boot,seed):
 # Resample complete paired episode indices, including repeats; recenter LOO each draw.
 rng=np.random.default_rng(seed);n=len(target);draws=rng.integers(0,n,(n_boot,n));out=[]
 for idx in draws:
  hold=contribution(ratios[idx],target[idx]).mean(0);sam=(totals['sample_'+metric][idx]-totals['sample_old'][idx]).mean(0);det=(totals['det_'+metric][idx]-totals['det_old'][idx]).mean(0);mo=(totals['sample_'+metric+'_mean'][idx]-totals['sample_old'][idx]).mean(0);so=(totals['sample_'+metric+'_std'][idx]-totals['sample_old'][idx]).mean(0)
  out.append(np.stack([hold,sam,det,train_gain-hold,hold-sam,sam-det,mo,so,sam-mo-so]))
 return np.array(out),draws
