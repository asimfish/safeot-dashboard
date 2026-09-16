import copy
import numpy as np,torch

def metrics(old,new,states):
 with torch.no_grad():
  m0,l0=old(states);m1,l1=new(states);s0=l0.exp();s1=l1.exp();kl=torch.distributions.kl_divergence(torch.distributions.Normal(m0,s0),torch.distributions.Normal(m1,s1)).sum(-1).mean();w2=((m0-m1)**2+(s0-s1)**2).sum(-1).mean();shift=(m0-m1).abs().mean()
 return dict(KL=float(kl),W2_squared=float(w2),action_displacement=float(shift),variance_term=float(((s0-s1)**2).sum(-1).mean()))
def interpolate(old,new,alpha):
 a=copy.deepcopy(old);a.load_state_dict({k:(1-alpha)*v+alpha*new.state_dict()[k] for k,v in old.state_dict().items()});return a

def same(a,b):
 if isinstance(a,np.ndarray):return np.array_equal(a,b)
 if torch.is_tensor(a):return torch.equal(a,b)
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,(list,tuple)):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def install(agent,shadow,candidate,alpha,accepted,old_actor,old_optimizer):
 if accepted and alpha>0:
  agent.actor.load_state_dict(candidate.state_dict())
  if alpha==1:agent.actor_optimizer.load_state_dict(shadow.actor_optimizer.state_dict());rule='shadow_momenta'
  else:
   fresh=copy.deepcopy(old_optimizer);fresh['state']={};agent.actor_optimizer.load_state_dict(fresh);rule='reset_momenta'
 else:
  agent.actor.load_state_dict(old_actor);agent.actor_optimizer.load_state_dict(old_optimizer);rule='old_actor_and_momenta'
  assert same(agent.actor.state_dict(),old_actor) and same(agent.actor_optimizer.state_dict(),old_optimizer)
 for name in ['reward_critic','cost_critic']:getattr(agent,name).load_state_dict(getattr(shadow,name).state_dict())
 agent.critic_optimizer.load_state_dict(shadow.critic_optimizer.state_dict());return rule

def deltas(before,after):
 return {k:float((v-before[k]).norm()) for k,v in after.items()}
