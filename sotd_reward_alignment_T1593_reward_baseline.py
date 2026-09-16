import numpy as np,torch,time

def features(states,K):
 s=np.asarray(states,dtype=np.float64).reshape(-1,12,np.asarray(states).shape[-1]);x=np.concatenate([s[:,:,:2],s[:,:,4:5],s[:,:,6:6+K]],-1);t=np.broadcast_to(np.arange(12)[None,:],x.shape[:2]);cols=[np.ones_like(t,dtype=np.float64)];names=['intercept']
 for i in range(1,12):cols.append((t==i).astype(np.float64));names.append('time_'+str(i))
 for i in range(x.shape[-1]):cols.append(x[:,:,i]);names.append('x_'+str(i))
 for i in range(x.shape[-1]):
  for j in range(i,x.shape[-1]):cols.append(x[:,:,i]*x[:,:,j]);names.append(f'x_{i}*x_{j}')
 for k in range(K):cols.append(np.maximum(x[:,:,2]-x[:,:,3+k],0));names.append(f'positive_time_minus_budget_{k}')
 return np.stack(cols,-1),names

def fit_predict(states,returns,K):
 start=time.perf_counter();F,names=features(states,K);Y=np.asarray(returns,dtype=np.float64).reshape(-1,12);N=len(Y);assert N==20 and len(F)==20;pred=np.zeros_like(Y);folds=[]
 for i in range(N):
  idx=np.delete(np.arange(N),i);X=F[idx].reshape(-1,F.shape[-1]);y=Y[idx].reshape(-1);mu=X[:,1:].mean(0);std=np.maximum(X[:,1:].std(0),1e-6);Z=X.copy();Z[:,1:]=(Z[:,1:]-mu)/std;pen=.01*np.eye(Z.shape[1]);pen[0,0]=0;w=np.linalg.solve(Z.T@Z/len(Z)+pen,Z.T@y/len(Z));T=F[i].copy();T[:,1:]=(T[:,1:]-mu)/std;pred[i]=T@w;folds.append(dict(heldout_episode=i,fit_episodes=idx,feature_mean=mu,feature_std=std,coef=w))
 assert np.isfinite(pred).all();adv=Y-pred
 return torch.from_numpy(adv.reshape(-1)).detach(),dict(feature_names=names,features=F,targets=Y,prediction=pred,advantage=adv,folds=folds,ridge=.01,seconds=time.perf_counter()-start,OOF_residual_MSE=float(np.mean(adv**2)),baseline_frozen=True,action_features=False)
