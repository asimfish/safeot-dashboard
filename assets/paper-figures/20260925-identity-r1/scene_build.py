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
  if self.n==2:
   for e in self.e:
    if e['id'] in ('inputs','budgets'):e.update(stroke=NAVY,stroke_width=.7*S)
    if e['id'] in ('rollout_title','update_title'):e['color']=GRAY
  for ids in self.geometry.values():
   for e in self.e:
    if e['id'] in ids:
     e.setdefault('allow_overlap_with',[]).extend(i for i in ids if i!=e['id']);e['overlap_reason']='Named schematic motif: native node/edge joins or pattern strokes, no unrelated text.'
  for e in self.e:
   if e['kind']=='line' and 'container' in e:
    e.setdefault('allow_overlap_with',[]).append(e.pop('container'));e['overlap_reason']='Connector intentionally meets its named module background.'
  byid={e['id']:e for e in self.e}
  for e in self.e:
   if e['kind']=='text':
    x,y,w,h=e['box'];candidates=[]
    for b in self.e:
     if b['kind']=='shape' and b['z']<e['z'] and b.get('shape')!='ellipse':
      xx,yy,ww,hh=b['box']
      if xx<=x and yy<=y and x+w<=xx+ww and y+h<=yy+hh:candidates.append((ww*hh,b['id']))
    if candidates:e['container']=min(candidates)[1]
  if self.n==1:
   byid['price_actor_0']['allow_overlap_with']=['safeot'];byid['price_actor_0']['overlap_reason']='The applied-price output crosses the central mechanism boundary to its actor consumer.'
  if self.n==2:
   byid['sum_sign']['container']='sum'
   for a,b in [('gae_bypass_0','rollout'),('observed_feedback_2','update'),('price_to_sum_1','update'),('gae_overpass_1','update')]+[(f'bound_mark{i}_0',f'bound_strip{i}') for i in range(3)]:
    byid[a].setdefault('allow_overlap_with',[]).append(b);byid[a]['overlap_reason']='This specific port crosses its module boundary, or this bound marker belongs inside its named strip.'
  d=HERE/f'conversion/figure{self.n}/redrawn';d.mkdir(parents=True,exist_ok=True)
  shutil.copy2(HERE/f'conversion/figure{self.n}/pages/page_001/source.png',d/'source.png')
  h=228 if self.n==1 else 237.6
  scene={'version':1,'title':f'SafeOT Figure {self.n}','slide_width_inches':5.5,'slides':[{'id':f'figure{self.n}','width':1980,'height':h*S,'background':'#FFFFFF','reviewed':True,'notes':'Semantic redrawing of the generated appearance candidate. Corrected notation and causal routes. Review candidate; no manuscript promotion.','elements':self.e}]}
  (d/'scene.json').write_text(json.dumps(scene,indent=2));(d/'equations.json').write_text(json.dumps(self.m,indent=2))
  (d/'appearance-plan.json').write_text(json.dumps({'version':1,'mode':'redesign','notes':'User asks to restore earlier visual specificity. White interiors; navy headings, teal graph projection/prices, orange observed feedback, gray standard RL; sparse red hard exclusions. Native geometry replaces generated erroneous labels and routes.','targets':[]},indent=2));print(d)

def network(f,id,x,y,w,h,target=False,overlay=False):
 start=len(f.e)
 p=[(0,.5),(.26,0),(.65,.06),(1,.5),(.23,1),(.55,.65),(.8,1)]
 p=[(x+a*w,y+b*h) for a,b in p]
 edges=[(0,1),(1,2),(2,3),(0,4),(4,5),(1,5),(5,3),(5,6),(6,3)]
 strong={0:1.6,3:1.0,4:1.0,5:1.6,6:1.25,7:1.25,8:1.25}
 for j,(a,b) in enumerate(edges):
  ax,ay=p[a];bx,by=p[b];d=math.dist(p[a],p[b]);ux=(bx-ax)/d;uy=(by-ay)/d
  if j==1:
   f.path(id+'_hard',[(ax+ux*3,ay+uy*3),(bx-ux*3,by-uy*3)],RED,.7,dash=True)
   cx=(ax+bx)/2;cy=(ay+by)/2
   for k,sgn in enumerate([1,-1]):f.path(id+'_cross'+str(k),[(cx-2.2,cy-sgn*2.2),(cx+2.2,cy+sgn*2.2)],RED,1)
   continue
  styles=[(0,GRAY,.7)]
  if overlay:styles=[(-1.15,'#A0A9B0',.65)]+([(1.15,TEAL,strong[j])] if j in strong else [])
  elif target:styles=[(0,TEAL,strong[j])] if j in strong else [(0,LIGHT,.55)]
  for z,(off,col,thick) in enumerate(styles):f.path(f'{id}_e{j}_{z}',[(ax+3*ux-off*uy,ay+3*uy+off*ux),(bx-3*ux-off*uy,by-3*uy+off*ux)],col,thick,True)
 for j,(a,b) in enumerate(p):f.circle(id+'_n'+str(j),a,b,3.0,TEAL if target or overlay else GRAY,'#E8F2F4' if target or overlay else '#F2F4F5')
 f.geometry[id]=[e['id'] for e in f.e[start:]]

def plain_module(f,id,x,y,w,h,title,color=NAVY):
 f.container=None;f.box(id,x,y,w,h,'#FFFFFF',None,0);f.container=id
 f.path(id+'_header_rule',[(x,y+16),(x+w,y+16)],color,.7)
 f.text(id+'_title',title,x+2,y+1,w-4,13,9.3,True,color,align='left')

def figure1():
 f=Scene(1)
 plain_module(f,'penalty',4,4,82,153,'Penalty view')
 f.text('penalty_sub','Costs in the objective',5,24,81,12,8.1,color=GRAY,align='left')
 for j,k in enumerate(['1','2','K']):
  y=44+j*27;f.eq('cost_'+k,rf'C_{{{k}}}',4,y,19,16,10.5)
  begin=len(f.e);f.box('strip_'+k,25,y+1,27,14,'#F5F8FA',NAVY,1)
  if j==0:
   for v in [4,9]:f.path('pattern_'+k+str(v),[(27+i*2,y+v+math.sin(i*math.pi/2)*1.3) for i in range(12)],NAVY,.5)
  elif j==1:
   for i in range(5):f.path('pattern_'+k+str(i),[(27+i*4,y+12),(31+i*4,y+4)],NAVY,.5)
  else:
   for row in range(2):
    for col in range(6):f.circle('pattern_'+k+str(row)+str(col),28+4*col,y+5+5*row,.45,NAVY,NAVY)
  f.geometry['pattern'+k]=[e['id'] for e in f.e[begin:]]
  f.eq('weight_'+k,rf'\lambda_{{{k}}}',55,y-3,22,18,10.5,NAVY)
  f.path('costroute_'+k,[(54,y+12),(80,y+12)],NAVY,.65)
 f.path('costbus',[(80,56),(80,123),(45,123),(45,127)],NAVY,.65,True)
 f.geometry['cost_routes']=[e['id'] for e in f.e if e['id'].startswith(('costroute','costbus'))]
 f.eq('weighted_objective',r'A_r-\sum_k\lambda_k A_{c_k}',4,128,82,24,10.5)
 f.container=None;f.box('safeot',92,3,212,154,'#FFFFFF',TEAL,2);f.container='safeot'
 f.text('safeot_title','SafeOT',99,7,53,15,11,True,TEAL,'left')
 f.text('one_flow','One flow, all budgets',157,8,139,13,8.8,True,TEAL,'right')
 f.eq('budgets',r'\langle C_k,F\rangle\le b_k\quad\forall k',100,25,103,17,10.5)
 # Three aligned budget tabs, no real-valued or hazard-specific examples.
 for j,k in enumerate(['1','2','K']):
  f.box('budget_tab'+k,210+j*28,26,25,15,'#F2F7F7',LIGHT,1)
  f.eq('tab_b'+k,rf'b_{{{k}}}',211+j*28,26,23,15,10)
 network(f,'projection_graph',106,49,126,44,overlay=True)
 f.text('legend_states','state clusters',242,44,58,11,8.1,color=GRAY)
 f.path('observed_key',[(245,63),(254,63)],'#A0A9B0',.65,True)
 f.text('observed_text','observed',257,58,41,11,8.1,color=GRAY,align='left')
 f.path('target_key',[(245,78),(254,78)],TEAL,1.6,True)
 f.text('target_text','target',257,73,41,11,8.1,color=TEAL,align='left')
 f.path('excluded_key',[(245,92),(253,92)],RED,.65,dash=True)
 f.text('excluded_text','excluded',257,87,41,11,8.1,color=RED,align='left')
 f.text('projection','Entropic projection',98,100,94,12,8.4,True,TEAL,'left')
 f.path('projection_duals',[(178,107),(193,107)],TEAL,.75,True)
 f.eq('raw_duals',r'\lambda_k^*',194,95,23,21,10.5,TEAL)
 f.path('raw_filter',[(218,107),(226,107)],TEAL,.75,True)
 f.text('filter','clip + EMA',228,101,70,11,8.1,color=TEAL)
 f.text('before_violation','can price before violation',99,112,116,10,8.1,color=TEAL,align='left')
 f.text('feedback','observed-cost feedback',98,125,94,10,8.1,color=ORANGE,align='left')
 f.eq('cost_error',r'\bar J_k-B_k',111,135,55,18,10.5,ORANGE)
 f.path('feedback_price',[(167,144),(185,144)],ORANGE,.75,True)
 f.eq('price_rule',r'\lambda_k=\bar\lambda_k^*+\beta_k',190,127,106,23,11,TEAL)
 f.path('filter_to_price',[(292,112),(299,112),(299,138),(294,138)],TEAL,.7,True)
 # Actor remains a short semantic output; the detailed normalized formula is in Figure2.
 f.container=None
 f.text('actor_strip','priced advantage',103,162,78,11,8.1,color=GRAY)
 f.path('price_actor',[(222,151),(222,159),(144,159),(144,161)],TEAL,.65,True)
 f.path('adv_actor',[(183,167),(193,167)],GRAY,.7,True)
 f.text('actor','PPO/TRPO',196,162,51,11,8.1,True,GRAY)
 f.path('actor_next',[(249,167),(259,167)],GRAY,.7,True)
 f.eq('pi_next',r'\pi_{t+1}',264,158,31,18,10.5)
 # Price/view links are leaders, not causal pipeline arrows.
 plain_module(f,'constraints',310,4,82,153,'Constraint view')
 f.text('constraints_sub','Budgets bound\nflow costs',312,23,77,21,8.1,color=GRAY)
 f.box('feasible',329,62,48,61,'#EDF3F7',None,0)
 f.path('cost_axisx',[(327,123),(387,123)],GRAY,.7,True)
 f.path('cost_axisy',[(329,126),(329,60)],GRAY,.7,True)
 f.path('bound1',[(377,62),(377,123)],NAVY,.65,dash=True)
 f.path('bound2',[(329,62),(377,62)],NAVY,.65,dash=True)
 f.eq('axis_cost1',r'\langle C_1,F\rangle',339,126,53,17,10)
 f.eq('axis_cost2',r'\langle C_2,F\rangle',310,43,59,16,10)
 f.text('slack','slack',351,63,25,10,8.1,color=GRAY)
 f.text('binding','binding',340,108,33,10,8.1,color=TEAL)
 f.circle('Fstar_dot',377,88,2,TEAL,TEAL);f.eq('Fstar',r'F^*',366,70,24,18,10.5,TEAL)
 f.eq('b1',r'b_1',373,105,20,17,10);f.eq('b2',r'b_2',309,60,21,16,10)
 f.eq('duals_active',r'\lambda_1^*>0,\quad\lambda_2^*=0',312,141,79,17,10.5,TEAL)
 f.geometry['constraint_geometry']=[e['id'] for e in f.e if e['id'].startswith(('cost_axis','bound')) or e['id'] in ('feasible','Fstar_dot')]
 f.container=None;f.path('summary_rule',[(4,176),(392,176)],LIGHT,.65)
 f.text('one_rule','One price rule',4,176,78,12,8.8,True,NAVY,'left')
 f.text('exact_settings','exact settings',87,179,109,11,8.1,color=GRAY)
 f.path('exact_bracket',[(4,192),(4,190),(196,190),(196,192)],LIGHT,.5)
 f.path('limit_bracket',[(271,192),(271,190),(392,190),(392,192)],LIGHT,.5)
 f.text('conditional','conditional limits',281,179,108,11,8.1,color=GRAY)
 f.box('ours_band',207,193,58,21,'#EFF7F5',None,0)
 for name,title,x,w in [('fixed','Fixed penalty',4,79),('lag','Lagrangian',87,109),('ours','SafeOT',207,58),('lp','LP',271,47),('active','Active-set',322,70)]:
  f.text('setting_'+name,title,x,193,w,10,8.2,True,TEAL if name=='ours' else NAVY)
 f.eq('fixed_setting',r'c=0,\ \beta\ \text{fixed}',4,204,79,11,8.3)
 f.eq('lag_setting',r'c=0,\ \beta\ \text{adaptive}',87,204,109,11,8.3)
 f.eq('finite',r'\text{finite }\varepsilon',207,204,58,11,8.3,TEAL)
 f.eq('lp_limit',r'\varepsilon\to0',271,204,47,11,8.3)
 f.eq('active_limit',r'\varepsilon\to\infty',322,203,70,11,8.3)
 f.text('saturated_clip','saturated clip',322,215,70,11,8.1)
 return f

def figure2():
 f=Scene(2)
 f.module('rollout',4,4,68,143,'1  Rollout',False,9)
 f.eq('pi_t',r'\pi_t',23,24,29,17,10.5)
 for i in range(3):
  x=14+22*i;f.circle('trajectory'+str(i),x,51,3.3,GRAY,'#F2F4F5')
  if i<2:f.path('time'+str(i),[(x+4,51),(x+17,51)],GRAY,.7,True)
  f.path('action'+str(i),[(x,56),(x,68)],GRAY,.7,True)
 f.text('trajectory_label','state / action\nsamples',7,73,61,20,8.1,color=GRAY)
 f.text('gae_label','GAE',8,95,60,11,8.1,True)
 f.eq('gae',r'A_r,\ A_{c_k}',9,108,61,20,10.5)
 f.text('cost_label','observed\nepisode cost',7,126,61,20,8.1,color=ORANGE)
 # Cost math output sits in the inner routing gap, distinct from the GAE port.
 f.container=None;f.eq('observed_cost',r'\bar J_k',11,147,23,17,10.5,ORANGE)
 f.module('inputs',78,4,68,143,'2  Flow inputs',False,9)
 # Samples -> state clustering, then a graph; not a second rollout trajectory.
 begin=len(f.e)
 for i,(a,b) in enumerate([(85,39),(90,44),(84,52),(90,59),(85,67),(92,74)]):f.circle('sample'+str(i),a,b,1.3,GRAY,'#DDE5EB')
 pts=[(103,54),(116,36),(135,47),(131,77),(109,79)]
 for i,(a,b) in enumerate([(0,1),(1,2),(0,3),(0,4),(2,3),(4,3)]):
  aa=pts[a];bb=pts[b];d=math.dist(aa,bb);ux=(bb[0]-aa[0])/d;uy=(bb[1]-aa[1])/d
  f.path('clusteredge'+str(i),[(aa[0]+3*ux,aa[1]+3*uy),(bb[0]-3*ux,bb[1]-3*uy)],NAVY,.6,True)
 for i,(a,b) in enumerate(pts):f.circle('cluster'+str(i),a,b,3,NAVY,'#DCE9F2')
 f.path('cluster_transform',[(91,51),(97,54)],GRAY,.6,True)
 f.geometry['clustering']=[e['id'] for e in f.e[begin:]]
 f.text('clusters_label','clustered states',81,87,62,11,8.1,color=GRAY)
 f.box('attributes',84,103,56,38,'#F7F9FA',LIGHT,1)
 f.text('attributes_title','edge attributes',85,105,54,11,8.1)
 f.eq('attribute_names',r'\hat F\quad A\quad C_k',85,118,54,20,10.5)
 f.module('budgets',152,4,76,143,'3  Constraints',False,9)
 f.text('soft_label','soft budgets',156,26,68,11,8.1,True)
 f.eq('budget_rule',r'\langle C_k,F\rangle\le b_k',155,38,70,20,10.5)
 # Parallel cost-bound strips visually encode multiple channels without numeric data.
 for i in range(3):
  f.box('bound_strip'+str(i),161,65+i*7,57,4,'#EAF1F4',LIGHT,0)
  f.path('bound_mark'+str(i),[(200,65+i*7),(200,69+i*7)],NAVY,.55)
 f.eq('step_budget',r'b_k=B_k/L',157,88,67,18,10.5)
 f.text('hard_label','hard exclusion',156,110,68,11,8.1,color=RED)
 f.circle('hard_from',161,134,3,GRAY);f.circle('hard_to',188,134,3,GRAY)
 f.path('hard_edge',[(165,134),(184,134)],RED,.7,dash=True)
 f.path('hard_x1',[(172,131),(178,137)],RED,1);f.path('hard_x2',[(172,137),(178,131)],RED,1)
 f.eq('hard_eq',r'F_H=0',192,125,34,17,10.5,RED)
 f.geometry['hardmotif']=[e['id'] for e in f.e if e['id'].startswith(('hard_from','hard_to','hard_edge','hard_x'))]
 f.module('projection',234,4,158,143,'4  Entropic projection',True,9)
 f.eq('projection_objective',r'\min_{F\ge0}[-\langle A,F\rangle+\varepsilon\mathrm{KL}(F\Vert\hat F)]',237,25,152,25,10.5,TEAL)
 f.text('constraints_line','s.t. flow balance + budgets',238,54,150,11,8.1)
 f.eq('Fhat',r'\hat F',245,71,41,17,10.5)
 f.eq('Ftarget',r'F^*',342,71,41,17,10.5,TEAL)
 network(f,'before',244,94,54,26)
 f.path('projection_operation',[(304,108),(322,108)],TEAL,1.2,True)
 network(f,'after',328,94,54,26,target=True)
 f.text('target_only','Target flow is not executed',238,131,150,11,8.1,True,TEAL)
 f.container=None
 for name,a,b in [('rollout_graph',(72,68),(78,68)),('graph_budget',(146,68),(152,68)),('budget_projection',(228,68),(234,68))]:f.path(name,[a,b],GRAY,.7,True)
 # Prices descend on a separate rail. GAE will enter the advantage formula directly.
 f.eq('filter_chain',r'\bar\lambda_k^*\leftarrow\mathrm{clip}_c+\mathrm{EMA}\leftarrow\lambda_k^*',154,151,142,21,10.5,TEAL)
 f.text('price_label','budget duals',305,153,77,11,8.1,color=TEAL)
 f.path('solved_prices',[(314,147),(314,150),(302,150),(302,161),(297,161)],TEAL,.75,True)
 f.module('update',4,180,388,42,'',False)
 f.text('update_title','5  Priced policy update',10,182,127,11,8.5,True,NAVY,'left')
 f.eq('beta_update',r'\beta_k\leftarrow[\beta_k+\alpha(\bar J_k-B_k)]_+',8,198,126,18,10.5,ORANGE)
 f.path('beta_sum',[(135,207),(142,207)],ORANGE,.7,True)
 f.circle('sum',149,207,6,GRAY);f.text('sum_sign','+',143,201,12,12,10)
 f.path('sum_lambda',[(156,207),(162,207)],GRAY,.7,True)
 f.eq('lambda',r'\lambda_k',162,199,22,17,10.5,TEAL)
 f.path('lambda_adv',[(184,207),(191,207)],GRAY,.7,True)
 f.eq('advantage',r'\widetilde A=\frac{A_r-\sum_k\lambda_k A_{c_k}}{1+\sum_k\lambda_k}',193,192,109,29,10.5)
 f.path('adv_ppo',[(303,207),(307,207)],GRAY,.7,True)
 f.text('ppo','PPO/TRPO',308,200,48,14,8.1,True)
 f.path('ppo_next',[(357,207),(362,207)],GRAY,.7,True)
 f.eq('pi_next',r'\pi_{t+1}',363,198,28,18,10.5)
 f.container=None
 f.path('observed_feedback',[(22,163),(22,171),(116,171),(116,198)],ORANGE,.75,True)
 f.path('price_to_sum',[(154,163),(149,163),(149,200)],TEAL,.75,True)
 f.path('gae_bypass',[(69,119),(75,119),(75,149),(144,149),(144,175),(146,175)],GRAY,.65)
 f.path('gae_overpass',[(152,175),(248,175),(248,191)],GRAY,.65,True)
 f.text('advantages','advantages',78,149,57,11,8.1,color=GRAY)
 f.text('next_label','next rollout',164,224,70,10,8.1,color=GRAY)
 # Native export adds a single continuous exterior freeform path, never a segmented loop.
 return f

if __name__=='__main__':
 for n in ([int(sys.argv[1])] if len(sys.argv)>1 else (1,2)):(figure1() if n==1 else figure2()).save()
