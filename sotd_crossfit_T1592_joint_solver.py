import copy,time
import numpy as np
import torch
from reward_baseline import fit_predict
from scipy.optimize import minimize,nnls

def finite_targets(x,H=12):
 y=x.reshape(-1,H,*x.shape[1:]);return y.flip(1).cumsum(1).flip(1).reshape_as(x)
def centered(x,H=12):
 y=x.reshape(-1,H,*x.shape[1:]);N=len(y)
 assert N>1
 return ((y-y.mean(0))*N/(N-1)).reshape_as(x)
def solve_local(values,jac,K,B,radius=.01,geometry="original"):
 # values = reward gain, predicted raw costs, mean forward KL.
 B=np.asarray(B);z0=np.zeros(K);bounds=[(-.25,.25)]*K if geometry=="original" else [(None,None)]*K
 def con(z,slack=0):v=values(z);return np.r_[B*(1+slack)-v[1:-1],radius-v[-1]]
 def cj(z,slack=0):return -jac(z)[1:]
 res=minimize(lambda z:-values(z)[0],z0,jac=lambda z:-jac(z)[0],constraints=[dict(type='ineq',fun=con,jac=cj)],bounds=bounds,method='SLSQP',options=dict(maxiter=60,ftol=1e-7))
 recovery=False;slack=0.
 if not res.success or np.min(con(res.x)) < -1e-6:
  recovery=True
  def rc(x):return con(x[:-1],x[-1])
  def rj(x):return np.column_stack([cj(x[:-1]),np.r_[B,0.]])
  rr=minimize(lambda x:x[-1],np.r_[z0,max(0,float(np.max((values(z0)[1:-1]-B)/B)))+1e-5],jac=lambda x:np.r_[np.zeros(K),1.],constraints=[dict(type='ineq',fun=rc,jac=rj)],bounds=bounds+[(0,None)],method='SLSQP',options=dict(maxiter=60,ftol=1e-7))
  slack=max(0,float(rr.x[-1]));res=rr;z=rr.x[:-1]
 else:z=res.x
 valid=bool(res.success and np.isfinite(values(z)).all() and np.min(con(z,slack))>=-1e-5)
 if not valid:z=z0
 v=values(z);J=jac(z);active=np.r_[np.abs(B*(1+slack)-v[1:-1])<1e-4,abs(radius-v[-1])<1e-5]
 # Recovery KKT has additional slack variable and different objective: do not label reward prices.
 prices=None;kkt=None
 if valid and not recovery:
  cols=[J[1:][active].T];boundvec=[]
  for n,t in enumerate(z):
   if geometry=="original" and abs(abs(t)-.25)<1e-6:
    q=np.zeros(K);q[n]=np.sign(t);boundvec.append(q)
  A=cols[0]
  if boundvec:A=np.column_stack([A,np.array(boundvec).T])
  dual,err=nnls(A,J[0]) if A.shape[1] else (np.zeros(0),float(np.linalg.norm(J[0])))
  full=np.zeros(len(B)+1);full[active]=dual[:sum(active)];prices=full[:-1].tolist();kkt=float(err)
 return z,dict(accepted=valid,recovery=recovery,slack=slack,solver_success=bool(res.success),solver_message=str(res.message),iterations=int(res.nit),lambda_raw=prices,kkt_stationarity_subspace=kkt,predicted_cost=v[1:-1].tolist(),KL=float(v[-1]),reward_gain=float(v[0]),constraint_residual=float(np.maximum(v[1:-1]-B,0).max()),coordinates=z.tolist())

def update(agent,data,B,geometry="fisher",metric="KL",scale=1.,c_w=1.,estimator="time_loo"):
 assert metric in ["KL","W2"] and c_w>0
 radius=.01*scale
 start=time.time();H=12;N=len(data['states'])//H
 done=data['dones'].reshape(N,H);assert done[:,-1].bool().all() and not done[:,:-1].bool().any()
 rt=finite_targets(data['rewards']);ct=finite_targets(data['costs']);ar=centered(rt).double();ac=centered(ct).double();agent.audit_reward_baseline=dict(estimator=estimator,targets=rt.detach().cpu(),advantage=ar.detach().cpu())
 if estimator=='cf_state':
  ar,baseline=fit_predict(data['states'].cpu().numpy(),rt.cpu().numpy(),len(B));agent.audit_reward_baseline=baseline;agent.audit_reward_baseline['estimator']=estimator
 elif estimator!='time_loo':raise ValueError(estimator)
 Jhat=data['costs'].reshape(N,H,-1).sum(1).mean(0).double()
 actor=copy.deepcopy(agent.actor).double();named=list(actor.named_parameters());base=torch.cat([p.detach().flatten() for _,p in named]);states=data['states'].double();actions=data['actions'].double()
 with torch.no_grad():oldmu,oldls=actor(states);oldlp=actor.log_prob(states,actions)
 def evaltheta(theta,force_kl=False):
  params={};i=0
  for name,p in named:params[name]=theta[i:i+p.numel()].view_as(p);i+=p.numel()
  mu,ls=torch.func.functional_call(actor,params,(states,));dist=torch.distributions.Normal(mu,ls.exp());ratio=(dist.log_prob(actions).sum(-1)-oldlp).exp()
  gain=((ratio-1)*ar).sum()/N;cost=Jhat+((ratio-1)[:,None]*ac).sum(0)/N
  kl=(ls-oldls+((oldls.exp()**2+(oldmu-mu)**2)/(2*ls.exp()**2))-.5).sum(-1).mean()
  w2=((mu-oldmu)**2+(ls.exp()-oldls.exp())**2).sum(-1).mean()
  dist=kl if metric=="KL" or force_kl else w2/c_w
  return torch.cat([gain[None],cost,dist[None]])
 t=base.clone().requires_grad_();v=evaltheta(t,force_kl=True);grads=[]
 for k in range(1+len(B)):
  g=torch.autograd.grad(v[k],t,retain_graph=True)[0];grads.append(g/max(float(g.norm()),1e-12))
 cg=[]
 if geometry=='fisher':
  kg=torch.autograd.grad(v[-1],t,create_graph=True,retain_graph=True)[0]
  def hv(p):return torch.autograd.grad((kg*p).sum(),t,retain_graph=True)[0].detach()+.001*p
  natural=[]
  for g in grads:
   sol=torch.zeros_like(g);res=g.clone();direction=res.clone();rr=res@res;initial=float(rr.sqrt())
   for iteration in range(50):
    hp=hv(direction);alpha=rr/(direction@hp);sol+=alpha*direction;res-=alpha*hp;nr=res@res
    if float(nr.sqrt())<=1e-8*max(initial,1e-12):rr=nr;break
    direction=res+(nr/rr)*direction;rr=nr
   true=float((hv(sol)-g).norm());cg.append(dict(iterations=iteration+1,residual=true,relative_residual=true/max(initial,1e-12),damping=.001));natural.append(sol/max(float(sol.norm()),1e-12))
  grads=natural
 D=torch.stack(grads,1).detach();agent.audit_directions=D.cpu();cache={}
 def calc(z):
  key=tuple(z)
  if cache.get('key')!=key:
   zt=torch.tensor(z,dtype=torch.double,requires_grad=True);vals=evaltheta(base+D@zt);jac=torch.stack([torch.autograd.grad(x,zt,retain_graph=True)[0] for x in vals]);cache.update(key=key,v=vals.detach().numpy(),j=jac.detach().numpy())
  return cache['v'],cache['j']
 z,info=solve_local(lambda z:calc(z)[0],lambda z:calc(z)[1],D.shape[1],B,radius=radius,geometry=geometry)
 agent.audit_delta=(D@torch.tensor(z,dtype=torch.double)).detach().cpu()
 info["solver_distance"]=info.pop("KL")
 info.update(metric=metric,scale=scale,c_W=c_w,normalized_radius=radius,raw_radius=radius if metric=="KL" else radius*c_w,geometry=geometry,CG=cg,coordinate_touches=bool(geometry=="original" and any(abs(abs(x)-.25)<1e-6 for x in z)),cost_gradient_columns_retained=True)
 target=(base+D@torch.tensor(z,dtype=torch.double)).float();idx=0
 agent.actor_optimizer.zero_grad()
 for p in agent.actor.parameters():p.grad=(p.detach().flatten()-target[idx:idx+p.numel()]).view_as(p).clone();idx+=p.numel()
 if info['accepted']:agent.actor_optimizer.step()
 actual=torch.cat([p.detach().flatten() for p in agent.actor.parameters()]).double()
 checked=evaltheta(actual).detach().numpy()
 rawkl=float(evaltheta(actual,force_kl=True)[-1].detach())
 from core import metrics
 old_actor=copy.deepcopy(agent.actor)
 idx0=0
 with torch.no_grad():
  for pp in old_actor.parameters():pp.copy_(base[idx0:idx0+pp.numel()].float().view_as(pp));idx0+=pp.numel()
 both=metrics(old_actor.double(),copy.deepcopy(agent.actor).double(),states)
 valid_install=bool(np.isfinite(checked).all() and checked[-1]<=radius+1e-5)
 info.update(actual_raw_KL=rawkl,actual_raw_W2_squared=both['W2_squared'],actual_solver_distance=float(checked[-1]),normalized_distance_residual=float(checked[-1]-radius),distance_active=bool(abs(checked[-1]-radius)<1e-5),float32_candidate_valid=valid_install)
 if not valid_install:info['accepted']=False

 before=[];after=[]
 for i in range(4):
  rv=agent.reward_critic(data['states']).squeeze(-1);cv=agent.cost_critic(data['states']);loss=((rv-rt)**2).mean()+((cv-ct)**2).mean()
  if i==0:before=[float(((rv-rt)**2).mean()),float(((cv-ct)**2).mean())]
  agent.critic_optimizer.zero_grad();loss.backward();agent.critic_optimizer.step()
 with torch.no_grad():after=[float(((agent.reward_critic(data['states']).squeeze(-1)-rt)**2).mean()),float(((agent.cost_critic(data['states'])-ct)**2).mean())]
 info.update(Jhat=Jhat.tolist(),B=list(B),actual_KL=rawkl,actual_predicted_cost=checked[1:-1].tolist(),parameter_delta=float((actual-base).norm()),critic_MSE_before=before,critic_MSE_after=after,seconds=time.time()-start,extra_environment_steps=0,finite_reward_return_mean=float(rt.reshape(N,H)[:,0].mean()),finite_cost_return_mean=ct.reshape(N,H,-1)[:,0].mean(0).tolist(),discounted_GAE_used=False)
 info.update(reward_estimator=estimator,baseline_seconds=agent.audit_reward_baseline.get("seconds",0.),reward_advantage_std=float(ar.std()),reward_advantage_mean=float(ar.mean()),cost_advantage_std=ac.std(0).tolist())
 return info
