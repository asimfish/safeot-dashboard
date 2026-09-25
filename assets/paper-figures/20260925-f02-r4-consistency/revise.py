"""Small native edits on archived text-only R4, following the 20:20Z brief."""
from pathlib import Path
import sys,json,ast,copy,hashlib
import fitz
from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.xmlchemy import OxmlElement
from lxml import etree
import native_tools as nt
HERE=Path(__file__).resolve().parent;R=HERE.parent
SOURCE=R.parent/'final/history_unified_20260925/R4_text_only_2036Z'
OUT=HERE/'build03';OUT.mkdir(exist_ok=False);nt.OUT=OUT
ANS=nt.ANS

def replace_text(sl,name,new):
 s=nt.get(sl,name);runs=[r for p in s.text_frame.paragraphs for r in p.runs];assert len(runs)==1
 runs[0].text=new

def dash(sl,name):
 s=nt.get(sl,name);ln=s._element.spPr.find('{'+ANS+'}ln')
 for x in list(ln):
  if x.tag.endswith(('prstDash','custDash')):ln.remove(x)
 d=OxmlElement('a:prstDash');d.set('val','dash');ln.insert(1,d)
 # Weight also distinguishes the 5pt-long beta-to-sum arrow in grayscale.
 ln.set('w',str(Pt(1.1)))
 if name=='beta_to_sum_0':
  s.left=Pt(121);s.width=Pt(8)
  ln.remove(d);custom=OxmlElement('a:custDash');part=OxmlElement('a:ds');part.set('d','150000');part.set('sp','150000');custom.append(part);ln.insert(1,custom)

def shaft(sl,name,width):
 """Preserve arrow endpoints and head; change only native polygon shaft width."""
 s=nt.get(sl,name);path=s._element.find('.//{'+ANS+'}path');pts=path.findall('.//{'+ANS+'}pt');assert len(pts)==7
 old=[(float(p.get('x')),float(p.get('y'))) for p in pts]
 scale=width/.7
 for a,b in ((0,6),(1,5)):
  mid=[(old[a][k]+old[b][k])/2 for k in (0,1)]
  for i in (a,b):
   for k,axis in enumerate(('x','y')):pts[i].set(axis,str(round(mid[k]+scale*(old[i][k]-mid[k]))))
 return dict(name=name,shaft_width_pt=width,arrow_head_unchanged=True,endpoints_unchanged=True)

def build(n):
 src=SOURCE/f'Figure{n}_F02_R4.pptx';prs=Presentation(src);sl=prs.slides[0]
 before={s.name:etree.tostring(s._element,method='c14n') for s in sl.shapes}
 audit=json.loads((SOURCE/f'Figure{n}_formula_audit.json').read_text());edge_audit=[]
 if n==1:
  # Header separation increases2.5pt without moving any graph or math position.
  nt.get(sl,'safeot_title').top-=Pt(2)
  nt.get(sl,'one_flow').top-=Pt(2.5)
  replace_text(sl,'pre_violation','Prices before violations')
  # Only the lower route is target flow; upper observed gray arrows stay.
  nt.delete(sl,names=tuple(f'unified_graph_edge_{i}_1.4' for i in (0,1,2)))
 else:
  for name in ('cost_route_0','cost_route_1','cost_route_2','beta_to_sum_0'):dash(sl,name)
  # Schematic, flow-balanced3:1 split; same observed-flow encoding in panel4.
  for prefix in ('inputs_graph','before'):
   for i in range(6):edge_audit.append(shaft(sl,f'{prefix}_edge_{i}',1.8 if i<3 else .6))
  replace_text(sl,'input_edges','Width ∝ flow mass')
 # Only formulas containing stars are replaced; all others remain original native groups.
 oldsource=R/'revision_r2/revise.py';tree=ast.parse(oldsource.read_text());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='equation_rows')
 env={'INK':nt.INK,'TEAL':nt.TEAL,'ORANGE':nt.ORANGE};exec(compile(ast.Module(body=[f],type_ignores=[]),str(oldsource),'exec'),env)
 sizes={row[0]:row for row in env['equation_rows'](n)}
 changed=set()
 for a in audit:
  if '*' in a['latex']:
   a['latex']=a['latex'].replace('^{*}',r'^{\star}');assert '*' not in a['latex'];changed.add(a['id'])
 rows=[(a['id'],a['latex'],a['allocated_box'],sizes[a['id']][3],sizes[a['id']][4]) for a in audit]
 d=nt.typeset(rows,n);pdf=fitz.open(d/'equations.pdf');svgs=sorted(d.glob('eq-*.svg'),key=lambda p:int(p.stem.split('-')[-1]))
 for i,(row,page,svg) in enumerate(zip(rows,pdf,svgs)):
  name,tex,b,size,color=row
  assert page.rect.width<=b[2]+.2 and page.rect.height<=b[3]+.2,(name,page.rect,b)
  if name in changed:
   old=nt.get(sl,name);idx=list(sl.shapes._spTree).index(old._element);nt.delete(sl,names=(name,))
   a=nt.import_formula(sl,svg,name,b,color,page.rect);a['latex']=tex;audit[i]=a
   sh=nt.get(sl,name);sl.shapes._spTree.remove(sh._element);sl.shapes._spTree.insert(idx,sh._element)
  audit[i]['minimum_latex_pdf_font_pt']=min(s['size'] for bl in page.get_text('dict')['blocks'] for l in bl.get('lines',[]) for s in l['spans'] if s['text'].strip())
  assert audit[i]['minimum_latex_pdf_font_pt']>=8
 target=d/f'Figure{n}_F02_R4.pptx';prs.save(target)
 after={s.name:etree.tostring(s._element,method='c14n') for s in sl.shapes}
 modified=[k for k in before if k in after and before[k]!=after[k]];removed=[k for k in before if k not in after];added=[k for k in after if k not in before]
 allowed=changed|({'safeot_title','one_flow','pre_violation'} if n==1 else {'input_edges','cost_route_0','cost_route_1','cost_route_2','beta_to_sum_0'}|{f'{p}_edge_{i}' for p in ('inputs_graph','before') for i in range(6)})
 assert set(modified)<=allowed,(modified,allowed);assert not added
 assert removed==([f'unified_graph_edge_{i}_1.4' for i in range(3)] if n==1 else [])
 report={'figure':n,'source':str(src.relative_to(R.parent)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'identical_native_objects':len([k for k in before if after.get(k)==before[k]]),'modified_objects':modified,'removed_objects':removed,'added_objects':added,'star_formulas_retypeset':sorted(changed),'all_other_native_objects_identical':True,'edge_width_encoding':edge_audit,'target_routing':'only lower route emphasized in teal in both figures','observed_widths_note':'Schematic3:1 route split, no empirical quantities or experimental results.'}
 (d/'formula_audit.json').write_text(json.dumps(audit,indent=2));(d/'object_changes.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
for n in (1,2):build(n)
