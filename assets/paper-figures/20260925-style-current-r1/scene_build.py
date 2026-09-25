"""Current SafeOT content in the user-selected earlier modular visual language.

S5 source rasters remain immutable. These scenes are semantic redraw candidates,
not a claim of pixel-faithful conversion or author/mentor acceptance.
"""
from pathlib import Path
import json, math, shutil, sys, subprocess

HERE=Path(__file__).resolve().parent
R=HERE.parent
S=5
TEAL='#126D69'; NAVY='#264C70'; INK='#263641'; GRAY='#64717C'
LIGHT='#BAC4CB'; TF='#F0F7F5'; GF='#F7F9FA'; ORANGE='#B86C2B'; RED='#B14747'

class Scene:
 def __init__(self,n):self.n=n;self.e=[];self.m=[];self.container=None;self.geometry={}
 def add(self,kind,id,**kw):
  o=dict(kind=kind,id=id,z=len(self.e)+1,**kw)
  if self.container:o['container']=self.container
  self.e.append(o);return o
 def box(self,id,x,y,w,h,fill='white',stroke=LIGHT,radius=3):
  if fill=='white':fill='#FFFFFF'
  return self.add('shape',id,box=[v*S for v in (x,y,w,h)],shape='round_rect' if radius else 'rect',radius=radius*S,fill=fill,stroke=stroke,stroke_width=.65*S)
 def text(self,id,t,x,y,w,h=10,size=8.1,bold=False,color=INK,align='center'):
  return self.add('text',id,box=[v*S for v in (x,y,w,h)],text=t,font_family='Liberation Sans',font_size=size*S,bold=bold,color=color,align=align,valign='middle',fit='strict',wrap=False)
 def eq(self,id,t,x,y,w,h=15,size=10.5,color=INK):self.m.append((id,t,[x,y,w,h],size,color[1:]))
 def path(self,id,pts,color=GRAY,width=.8,arrow=False,dash=False):
  out=[]
  for i,(a,b) in enumerate(zip(pts,pts[1:])):
   kw=dict(points=[[v*S for v in a],[v*S for v in b]],stroke=color,stroke_width=width*S)
   if arrow and i==len(pts)-2:kw.update(arrow=True,arrow_head={'length':min(3.3,math.dist(a,b)*.65)*S,'width':max(2.5,width*1.8)*S})
   if dash:kw['dash']=[2*S,1.8*S]
   out.append(self.add('line',id+'_'+str(i),**kw))
  self.geometry['path_'+id]=[e['id'] for e in out]
  return out
 def module(self,id,x,y,w,h,title,teal=False,title_size=9.1):
  self.container=None;self.box(id,x,y,w,h,TF if teal else '#FFFFFF',TEAL if teal else LIGHT)
  self.container=id
  if title:self.text(id+'_title',title,x+3,y+4,w-6,max(11,title_size*1.3),title_size,True,TEAL if teal else NAVY)
 def circle(self,id,x,y,r=2.6,color=GRAY,fill='#FFFFFF'):
  return self.add('shape',id,shape='ellipse',box=[(x-r)*S,(y-r)*S,2*r*S,2*r*S],fill=fill,stroke=color,stroke_width=.7*S)
 def graph(self,id,x,y,w,h,mode='observed',hard=False,overlay=False):
  # Same six-node support for every projected-flow motif. Offset gray/teal
  # arrows reveal two flows without silently doubling the graph's edges.
  start=len(self.e);p=[(x,y+h*.5),(x+w*.27,y),(x+w*.7,y),(x+w,y+h*.5),(x+w*.27,y+h),(x+w*.7,y+h)]
  edges=[(0,1),(1,2),(2,3),(0,4),(4,5),(5,3),(1,5)]
  for j,(a,b) in enumerate(edges):
   ax,ay=p[a];bx,by=p[b];d=math.dist(p[a],p[b]);ux=(bx-ax)/d;uy=(by-ay)/d
   if hard and j==1:
    self.path(id+'_hard',[(ax+3,ay),(bx-3,by)],RED,.75,dash=True);cx=(ax+bx)/2;cy=(ay+by)/2
    self.path(id+'_x1',[(cx-2.3,cy-2.3),(cx+2.3,cy+2.3)],RED,1.2)
    self.path(id+'_x2',[(cx-2.3,cy+2.3),(cx+2.3,cy-2.3)],RED,1.2)
    continue
   styles=[(0,GRAY,.65)] if mode=='observed' else [(0,TEAL,1.55 if j in (3,4,5) else .65)]
   if overlay:styles=[(-1.4,'#A5AFB6',.65),(1.4,TEAL,1.65 if j in (3,4,5) else .7)]
   for z,(off,c,th) in enumerate(styles):
    self.path(f'{id}_e{j}_{z}',[(ax+ux*3.5-uy*off,ay+uy*3.5+ux*off),(bx-ux*3.5-uy*off,by-uy*3.5+ux*off)],c,th,True)
  for j,(a,b) in enumerate(p):self.circle(id+'_n'+str(j),a,b,color=TEAL if mode=='target' or overlay else GRAY,fill='#F1F7F6' if mode=='target' else '#FFFFFF')
  self.geometry[id]=[e['id'] for e in self.e[start:]]
 def save(self):
  self.container=None
  if self.n==1:
   for e in self.e:
    if e['id'] in ('penalty','constraints'):e.update(stroke=NAVY,stroke_width=.9*S)
    if e['id']=='safeot':e['stroke_width']=1.0*S
  # Only graph-local geometric joins are intentionally intersecting. Text and
  # unrelated connectors are not exempted from collision checks.
  for ids in self.geometry.values():
   for e in self.e:
    if e['id'] in ids:
     e.setdefault('allow_overlap_with',[]).extend(i for i in ids if i!=e['id'])
     e['overlap_reason']='Schematic graph: node/edge junction and crossing within this named graph only; no text objects included.'
  for e in self.e:
   if e['kind']=='text':
    x,y,w,h=e['box']; candidates=[]
    for b in self.e:
     if b['kind']=='shape' and b['z']<e['z'] and b.get('shape')!='ellipse':
      xx,yy,ww,hh=b['box']
      if xx<=x and yy<=y and x+w<=xx+ww and y+h<=yy+hh:candidates.append((ww*hh,b['id']))
    if candidates:e['container']=min(candidates)[1]
  # A connector may cross the boundary of its explicitly declared parent box.
  for e in self.e:
   if e['kind']=='line' and 'container' in e:
    e.setdefault('allow_overlap_with',[]).append(e.pop('container'))
    e['overlap_reason']='Connector in its named module background; graph joins separately declared.'
  if self.n==2:
   byid={e['id']:e for e in self.e}
   byid['sum_sign']['container']='sum'
   for a,b in [('gae_bypass_0','rollout'),('observed_feedback_0','rollout'),('attrsep1_0','attributes'),('attrsep2_0','attributes'),('price_to_sum_1','update'),('gae_drop_0','update'),('observed_feedback_2','update'),('observed_feedback_3','update')]:
    byid[a].setdefault('allow_overlap_with',[]).append(b)
    byid[a]['overlap_reason']='Named external port connector crosses its module background, or attribute table separator meets its own frame.'
  d=HERE/f'conversion/figure{self.n}/redrawn';d.mkdir(parents=True,exist_ok=True)
  shutil.copy2(HERE/f'conversion/figure{self.n}/pages/page_001/source.png',d/'source.png')
  scene={'version':1,'title':f'SafeOT Figure {self.n}','slide_width_inches':5.5,'slides':[{'id':f'figure{self.n}','width':1980,'height':1188,'background':'#FFFFFF','reviewed':True,'notes':'Current SafeOT. Semantic redraw of the S5 candidate in the author-requested modular style; print canvas adapted to 5.5 by 3.3 inches. Source raster retained separately. Not yet accepted by cold reading.','elements':self.e}]}
  (d/'scene.json').write_text(json.dumps(scene,indent=2));(d/'equations.json').write_text(json.dumps(self.m,indent=2))
  (d/'appearance-targets.json').write_text(json.dumps({'mode':'redesign','notes':'User explicitly chose earlier visual language with current content. This is a design record, not a runtime color-verification plan. Actual export gets isolated target-color checks separately.','roles':{'views':NAVY,'solve':TEAL,'feedback':ORANGE,'standard':GRAY,'exclusion':RED}},indent=2))
  print(d)

def figure1():
 f=Scene(1)
 f.module('penalty',3,3,87,166,'Penalty view')
 f.text('penalty_sub','Costs in the objective',6,22,81,20,8.1)
 # Generic edge-cost channels rather than unsupported spill/fire/robot icons.
 for j,k in enumerate(('1','2','K')):
  y=47+j*23
  f.box('cost'+k,10,y,29,19,GF,LIGHT)
  f.eq('C'+k,rf'C_{{{k}}}',13,y+2,23,15)
  f.eq('weight'+k,rf'\lambda_{{{k}}}',44,y+2,24,15)
  f.path('costweight'+k,[(40,y+9.5),(44,y+9.5)],GRAY,.65,True)
  f.path('weightmerge'+k,[(69,y+9.5),(78,y+9.5)],NAVY,.65)
 f.path('weightbus',[(78,56.5),(78,122),(49,122),(49,128)],NAVY,.65,True)
 f.geometry['cost_merge']=[e['id'] for e in f.e if e['id'].startswith(('weightmerge','weightbus'))]
 f.eq('objective',r'A_r-\sum_k\lambda_k A_{c_k}',7,130,79,27,10.5)
 f.container=None
 f.module('safeot',96,3,207,166,'SafeOT',True,11)
 f.text('one_flow','One flow, all budgets',100,21,199,11,8.6,True,TEAL)
 f.eq('budget',r'\langle C_k,F\rangle\leq b_k\quad\forall k',151,34,99,17,10.5,TEAL)
 f.graph('flow',110,57,179,28,hard=True,overlay=True)
 f.path('observed_key',[(108,98),(120,98)],'#A5AFB6',.7,True)
 f.text('observed_label','observed',122,93,38,10,8.1,color=GRAY)
 f.path('target_key',[(164,98),(176,98)],TEAL,1.6,True)
 f.text('target_label','target',178,93,27,10,8.1,color=TEAL)
 f.text('hard_label','hard edge excluded',216,92,80,11,8.1,color=RED)
 f.text('projection_label','Entropic projection',100,106,98,11,8.3,True,TEAL)
 f.eq('raw_price',r'\lambda_k^*',196,102,22,19,11,TEAL)
 f.text('pre_violation','can price before violation',197,120,102,11,8.1,True,TEAL)
 f.path('raw_filter',[(219,112),(224,112)],TEAL,.8,True)
 f.text('filter_label','clip + EMA',225,106,50,11,8.1,color=TEAL)
 f.path('filter_bar',[(278,112),(300,112),(300,137),(276,137)],TEAL,.8,True)
 f.eq('price_sum',r'\lambda_k=\bar\lambda_k^*+\beta_k',185,130,90,19,11,TEAL)
 f.text('feedback_label','observed-cost feedback',100,121,95,10,8.1,color=ORANGE)
 f.eq('feedback_cost',r'\bar J_k-B_k',113,132,58,16,10.5,ORANGE)
 f.path('feedback_to_price',[(173,140),(183,140)],ORANGE,.8,True)
 f.path('price_actor',[(231,150),(141,150),(141,152)],TEAL,.8,True)
 f.text('priced_adv_label','priced advantage',104,152,74,11,8.1)
 f.path('priced_actor',[(181,157),(195,157)],GRAY,.8,True)
 f.text('ppo','PPO/TRPO',197,152,47,11,8.1,True)
 f.path('actor_policy',[(246,157),(254,157)],GRAY,.8,True)
 f.eq('pi_next',r'\pi_{t+1}',257,149,39,18,10.5)
 # The side panels are two readings of the same rule, not training stages.
 f.container=None
 f.path('objective_view',[(96,141),(90,141)],TEAL,.8,True)
 f.module('constraints',309,3,84,166,'Constraint view')
 f.text('constraints_sub','Budgets bound\nflow costs',312,22,78,20,8.1)
 f.box('feasible',329,63,48,61,'#EDF3F7',None,0)
 f.path('axisx',[(327,125),(385,125)],NAVY,.7,True)
 f.path('axisy',[(329,128),(329,53)],NAVY,.7,True)
 f.path('boundx',[(377,63),(377,125)],NAVY,.65,dash=True)
 f.path('boundy',[(329,63),(377,63)],NAVY,.65,dash=True)
 f.text('slack','slack',345,48,28,10,8.1,color=GRAY)
 f.text('binding','binding',344,100,33,10,8.1,color=TEAL)
 f.circle('optimal',377,91,2.1,TEAL,TEAL)
 f.eq('Fstar',r'F^*',369,72,21,17,10.5,TEAL)
 f.eq('b1',r'b_1',369,126,21,16,10.5)
 f.eq('b2',r'b_2',309,55,21,16,10.5)
 f.eq('active_dual',r'\lambda_1^*>0,\quad\lambda_2^*=0',313,145,77,19,10.5,TEAL)
 f.geometry['feasible_geometry']=[e['id'] for e in f.e if e['id'].startswith(('axisx','axisy','boundx','boundy')) or e['id'] in ('feasible','optimal')]
 f.container=None
 f.path('constraint_view_link',[(309,141),(303,141)],TEAL,.8,True)
 # Discrete settings/limits band, deliberately without a performance axis.
 f.text('rule_title','One price rule',3,174,390,12,9.3,True,TEAL)
 f.path('exact_bracket',[(10,199),(10,196),(149,196),(149,199)],LIGHT,.65)
 f.path('limit_bracket',[(245,199),(245,196),(388,196),(388,199)],LIGHT,.65)
 f.text('exact_label','exact settings',43,184,72,10,8.1,color=GRAY)
 f.text('limit_label','conditional limits',272,184,85,10,8.1,color=GRAY)
 f.box('ours_band',162,196,72,39,TF,TEAL)
 for id,t,x in [('fixed','Fixed penalty',4),('lag','Lagrangian',83),('ours','SafeOT',162),('lp','LP',241),('active','Active-set',320)]:
  f.text('setting_'+id,t,x,198,72,11,8.4,True,TEAL if id=='ours' else INK)
 f.eq('fixed_c',r'c=0',4,211,72,12,10)
 f.eq('fixed_beta',r'\beta_k\ \text{fixed}',4,223,72,12,10)
 f.eq('lag_c',r'c=0',83,211,72,12,10)
 f.eq('lag_beta',r'\beta_k\ \text{adaptive}',83,223,72,12,10)
 f.eq('finite',r'\text{finite }\varepsilon',162,215,72,17,10.5,TEAL)
 f.eq('lp_limit',r'\varepsilon\to0',241,215,72,17,10.5)
 f.eq('active_limit',r'\varepsilon\to\infty',320,210,72,14,10.5)
 f.text('saturated','saturated clip',320,224,72,10,8.1)
 return f

def figure2():
 f=Scene(2)
 f.module('rollout',3,3,68,139,'1  Rollout')
 f.eq('pi_t',r'\pi_t',23,24,27,17,11)
 # Time sequence, intentionally distinct from the clustered transition graph.
 for j in range(3):
  f.circle('state'+str(j),14+22*j,56,3.3)
  if j<2:f.path('transition'+str(j),[(18+22*j,56),(32+22*j,56)],GRAY,.8,True)
 f.text('gae_label','GAE',8,74,58,11,8.4,True)
 f.eq('gae',r'\hat A_r,\ \hat A_{c_k}',7,87,60,22,10.5)
 f.text('observed_label','episode cost',7,113,60,11,8.1,color=ORANGE)
 f.eq('observed_cost',r'\bar J_k',22,125,28,15,10.5,ORANGE)
 f.module('inputs',78,3,67,139,'2  Flow inputs')
 f.text('cluster_label','clustered states',81,25,61,11,8.1)
 f.graph('inputgraph',87,47,48,31)
 f.text('edge_label','edge attributes',81,88,61,11,8.1)
 # One attribute table with three distinct semantic columns; no numeric values.
 f.box('attributes',84,110,54,24,GF,LIGHT,0)
 f.path('attrsep1',[(102,110),(102,134)],LIGHT,.5)
 f.path('attrsep2',[(120,110),(120,134)],LIGHT,.5)
 f.eq('attributes_labels',r'\hat F\quad A\quad C_k',84,112,54,19,10.5)
 f.module('budgets',152,3,78,139,'3  Constraints')
 f.text('soft','soft budgets',156,24,70,11,8.4,True)
 f.eq('budget',r'\langle C_k,F\rangle\le b_k',156,38,70,21,10.5)
 f.eq('step_budget',r'b_k=B_k/L',156,61,70,19,10.5)
 f.text('hard_label','hard exclusions',156,86,70,11,8.1,color=RED)
 f.graph('hardgraph',162,101,58,21,hard=True)
 f.eq('hard_eq',r'F_H=0',165,127,51,13,10.5,RED)
 f.module('projection',237,3,156,139,'4  Entropic projection',True)
 f.eq('objective',r'\min_{F\ge0}\big[-\langle A,F\rangle+\varepsilon\mathrm{KL}(F\Vert\hat F)\big]',240,24,150,25,10.5,TEAL)
 f.text('st','s.t. flow balance + constraints',241,52,148,11,8.1)
 f.eq('before_label',r'\hat F',247,66,41,17,10.5)
 f.eq('after_label',r'F^*',342,66,41,17,10.5,TEAL)
 f.graph('before',247,91,48,26,hard=True)
 f.path('reroute',[(304,104),(327,104)],TEAL,1.1,True)
 f.graph('after',335,91,48,26,mode='target',hard=True)
 f.text('target_only','Target flow is not executed',241,126,148,11,8.1,True,TEAL)
 f.container=None
 for id,a,b in [('samples',(71,67),(78,67)),('inputs_constraints',(145,67),(152,67)),('constraints_solve',(230,67),(237,67))]:f.path(id,[a,b],GRAY,.8,True)
 # Only graph prices descend to the policy band. No target-flow execution arrow.
 f.text('budget_duals','budget duals',305,146,75,11,8.1,color=TEAL)
 f.eq('filter_chain',r'\bar\lambda_k^*\ \leftarrow\ \mathrm{clip}_c+\mathrm{EMA}\ \leftarrow\ \lambda_k^*',159,149,143,22,10.5,TEAL)
 f.path('duals_drop',[(317,142),(317,145),(306,145),(306,160),(302,160)],TEAL,.8,True)
 f.path('price_to_sum',[(160,161),(149,161),(149,200)],TEAL,.8,True)
 # GAE bypass stays above and outside the summation port.
 f.path('gae_bypass',[(61,101),(73,101),(73,149),(142,149),(142,174),(146,174)],GRAY,.65)
 # A four-point visual gap makes this a line overpass, never a junction.
 f.path('gae_overpass',[(152,174),(253,174)],GRAY,.65)
 f.path('gae_drop',[(253,174),(253,193)],GRAY,.65,True)
 f.geometry['gae_destination_elbow']=['gae_overpass_0','gae_drop_0']
 f.text('advantages','advantages',82,152,53,10,8.1,color=GRAY)
 f.path('observed_feedback',[(36,140),(36,157),(6,157),(6,208),(9,208)],ORANGE,.7,True)
 f.module('update',3,179,390,44,'',title_size=8.1)
 f.text('update_title','5  Priced policy update',10,182,128,11,8.5,True,INK,'left')
 f.eq('feedback_update',r'\beta_k\leftarrow[\beta_k+\eta(\bar J_k-B_k)]_+',9,199,127,18,10.5,ORANGE)
 f.path('beta_sum',[(137,208),(142,208)],ORANGE,.8,True)
 f.circle('sum',149,208,6,GRAY)
 f.text('sum_sign','+',143,202,12,12,10)
 f.path('sum_lambda',[(156,208),(160,208)],GRAY,.8,True)
 f.eq('lambda',r'\lambda_k',161,199,22,18,10.5,TEAL)
 f.path('lambda_adv',[(184,208),(191,208)],GRAY,.8,True)
 f.eq('priced_advantage',r'\widetilde A=\frac{\hat A_r-\sum_k\lambda_k\hat A_{c_k}}{1+\sum_k\lambda_k}',193,194,108,27,10.5)
 f.path('adv_ppo',[(302,208),(308,208)],GRAY,.8,True)
 f.text('ppo','PPO/TRPO',309,201,47,14,8.1,True)
 f.path('actor_next',[(357,208),(362,208)],GRAY,.8,True)
 f.eq('next_pi',r'\pi_{t+1}',362,199,29,19,10.5)
 f.container=None
 f.path('loop_start',[(381,223),(381,233),(231,233)],GRAY,.7)
 f.path('loop_end',[(161,233),(1,233),(1,63),(3,63)],GRAY,.7,True)
 f.text('loop_label','next rollout',164,226,64,10,8.1,color=GRAY)
 return f

if __name__=='__main__':
 for n in ([int(sys.argv[1])] if len(sys.argv)>1 else (1,2)):
  (figure1() if n==1 else figure2()).save()
