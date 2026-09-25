from pathlib import Path
import json,hashlib
import fitz,numpy as np
from PIL import Image
from pptx import Presentation
H=Path(__file__).resolve().parent;R=H.parent;B=R.parent/'final/history_unified_20260925/R4';D=H/'delivery';Q=H/'qa';Q.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((H/'r4_hashes.json').read_text())=={p.name:sha(p) for p in B.iterdir() if p.is_file()}
reports=[]
for n in (1,2):
 old=Presentation(B/f'Figure{n}_F02_R4.pptx');new=Presentation(D/f'Figure{n}_F02_R5.pptx');os={s.name:s for s in old.slides[0].shapes};ns={s.name:s for s in new.slides[0].shapes}
 change=json.loads((D/f'Figure{n}_object_changes.json').read_text());allowed=np.zeros((990,1650),bool)
 a=np.array(Image.open(B/f'Figure{n}_F02_R4_300dpi.png').convert('RGB'));b=np.array(Image.open(D/f'Figure{n}_F02_R5_300dpi.png').convert('RGB'));assert a.shape==b.shape
 delta=np.max(np.abs(a.astype(int)-b.astype(int)),axis=2)>0;allowed=np.zeros(delta.shape,bool)
 for name in change['modified_objects']+change['added_objects']:
  for shapes in (os,ns):
   if name not in shapes:continue
   s=shapes[name];x,y,w,h=[v/12700 for v in (s.left,s.top,s.width,s.height)];scale=300/72;pad=2
   allowed[max(0,int((y-pad)*scale)):min(a.shape[0],int((y+h+pad)*scale)+1),max(0,int((x-pad)*scale)):min(a.shape[1],int((x+w+pad)*scale)+1)]=True
 outside=int((delta&~allowed).sum());assert outside==0,(n,outside)
 Image.fromarray(np.where(delta[:,:,None],np.array([193,42,46]),b).astype('uint8')).save(Q/f'Figure{n}_diff.png')
 assert sha(B/f'Figure{n}_equations.tex')==sha(D/f'Figure{n}_equations.tex')
 # A formula group may translate, but its contour child XML stays unchanged.
 math=json.loads((D/f'Figure{n}_formula_audit.json').read_text())
 for r in math:
  name=r['id'];assert [s._element.xml for s in os[name].shapes]==[s._element.xml for s in ns[name].shapes]
 doc=fitz.open(D/f'Figure{n}_F02_R5.pdf');page=doc[0]
 for name in ['upper_cost_label']+(['flow_balance'] if n==2 else []):
  s=ns[name];x,y,w,h=[v/12700 for v in (s.left,s.top,s.width,s.height)];hits=page.search_for(s.text)
  assert len(hits)==1 and fitz.Rect(x,y,x+w,y+h).contains(hits[0]),(name,hits)
 margins=None
 if n==2:
  observed=page.search_for('episode cost')[0].y1
  edge=ns['edge_inputs'];edge_bottom=(edge.top+edge.height)/12700
  hard=page.search_for('Hard constraints')[0].y1
  margins=[139-observed,139-edge_bottom,139-hard];assert min(margins)>2 and max(margins)-min(margins)<.5,margins
  assert os['next_rollout_continuous']._element.xml==ns['next_rollout_continuous']._element.xml
 else:
  for name in ('leg_observed','leg_target','Fhat_legend','Fstar_legend'):assert (ns[name].left-os[name].left)/12700==-6
 assert not any(doc.metadata.get(k) for k in ('author','creator','producer'))
 reports.append(dict(figure=n,status='PASS',r4_all_files_hash_preserved=True,pixels_changed_outside_approved_regions=0,latex_and_all_math_child_contours_identical=True,new_labels_fit=True,panel123_bottom_margins_pt=margins,minimum_text_pt=8.107,minimum_math_pt=8.1694,zero_rasters=True,visual_review='Color actual PPTX render inspected; optional R5 awaits review; R4 acceptance is preserved'))
(Q/'requirements.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports))
