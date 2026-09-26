from pathlib import Path
import io, json, zipfile, shutil, hashlib
from PIL import Image
from pptx import Presentation
from pptx.util import Pt
from lxml import etree
HERE=Path(__file__).resolve().parent
R=HERE.parent
SRC=R.parent/'final/history_unified_20260925/OriginalTemplate_R3'
OUT=R.parent/'final/history_unified_20260925/OriginalTemplate_R4'
AS=HERE/'assets'; AS.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=False)
SHEET=Path('/home/batchcom/.whalent-agent/profiles/acct-63aacf96110c0e9595f3/agents/nv5bvsjuit04a7lpcn1am0z15/codex/generated_images/01a08cfe-d675-7f50-a638-3f819c5db330/exec-0784bff2-ae38-4c2a-8378-ad5c296a0640.png')
shutil.copy2(SHEET,AS/'generated_icon_sheet.png')
im=Image.open(SHEET).convert('RGBA')
# alpha components from the generated horizontal sheet: trajectory, graph, gauge, projection, policy
boxes={'trajectory':(20,140,430,610),'graph':(480,120,890,610),'gauge':(900,120,1270,550),'projection':(1250,120,1710,610),'policy':(1680,100,2160,650)}
for name,b in boxes.items():
 crop=im.crop(b); bb=crop.getchannel('A').getbbox()
 if bb: crop=crop.crop((max(0,bb[0]-12),max(0,bb[1]-12),min(crop.width,bb[2]+12),min(crop.height,bb[3]+12)))
 crop.save(AS/f'{name}.png')
# fit a generated crop in a transparent canvas with the target aspect; preserve alpha

def fit_asset(name,w_pt,h_pt):
 src=Image.open(AS/f'{name}.png').convert('RGBA'); pad=12
 aspect=w_pt/h_pt
 sw,sh=src.size
 if sw/sh>aspect:
  hh=max(1,int(sw/aspect)); y=max(0,(sh-hh)//2);src=src.crop((0,y,sw,min(sh,y+hh)))
 else:
  ww=max(1,int(sh*aspect)); x=max(0,(sw-ww)//2);src=src.crop((x,0,min(sw,x+ww),sh))
 canvas=Image.new('RGBA',(max(8,int(w_pt*8)),max(8,int(h_pt*8))),(0,0,0,0))
 src.thumbnail(canvas.size,resample=Image.Resampling.LANCZOS)
 x=(canvas.width-src.width)//2;y=(canvas.height-src.height)//2;canvas.alpha_composite(src,(x,y))
 out=AS/f'{name}_{int(round(w_pt*10))}x{int(round(h_pt*10))}.png';canvas.save(out);return out

def all_shapes(sl):
 out=[]
 def rec(s):
  out.append(s)
  if hasattr(s,'shapes'):
   for x in s.shapes: rec(x)
 for s in sl.shapes: rec(s)
 return out

def find(sl,name): return next(x for x in all_shapes(sl) if x.name==name)
def remove_group_child(group,name):
 for s in list(group.shapes):
  if s.name==name:
   s._element.getparent().remove(s._element);return s
 raise KeyError(name)

def add_pic(sl,name,path,x,y,w,h):
 p=sl.shapes.add_picture(str(path),Pt(x),Pt(y),Pt(w),Pt(h));p.name=name;return p
# replacement plan; target boxes are the original individual icon bounds
plan={1:[('icon_cost_icon0','trajectory','gen_icon_trajectory',118.0,67.72,11.0,9.35),('icon_cost_icon1','graph','gen_icon_graph',119.95,85.40,7.09,9.24),('icon_cost_icon2','gauge','gen_icon_gauge',118.22,105.94,10.78,8.91),('icon_cost_icon3','projection','gen_icon_projection',119.33,123.40,8.05,10.86)],2:[('icon_environment','trajectory','gen_icon_rollout',9.0,83.0,13.0,13.0),('icon_agent','policy','gen_icon_policy',34.0,81.12,11.0,14.41)]}
for n in (1,2):
 src=SRC/f'Figure{n}_OriginalTemplate_R3.pptx';dst=OUT/f'Figure{n}_OriginalTemplate_R4.pptx'
 prs=Presentation(src);sl=prs.slides[0]
 parent_names={1:'module_safeot',2:'module_stage1'}
 parent=find(sl,parent_names[n])
 specs=plan[n]
 for old,asset,new,x,y,w,h in specs:
  remove_group_child(parent,old)
  fp=fit_asset(asset,w,h)
  add_pic(sl,new,fp,x,y,w,h)
 prs.save(dst)
 # Restore the vivid semantic accents only. Neutral ink/borders stay unchanged.
 replacements={'607891':'285AA0','3F746B':'18785B','A57957':'BA651F'}
 tmp=dst.with_suffix('.tmp')
 with zipfile.ZipFile(dst) as zin,zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zout:
  for info in zin.infolist():
   data=zin.read(info.filename)
   if info.filename.endswith('.xml'):
    text=data.decode('utf-8')
    for a,b in replacements.items(): text=text.replace(a,b)
    data=text.encode('utf-8')
   zout.writestr(info,data)
 tmp.replace(dst)
 # source and generated asset records
 (OUT/f'Figure{n}_generated_icons.json').write_text(json.dumps({'source_sheet':'assets/generated_icon_sheet.png','generated_assets':[{'name':new,'asset':f'assets/{asset}.png','bbox_pt':[x,y,w,h],'raster_by_request':True} for old,asset,new,x,y,w,h in specs],'semantic_palette_restored':replacements,'source_r3_sha256':hashlib.sha256(src.read_bytes()).hexdigest()},indent=2))
# copy source notes and provide explicit imagegen provenance
(HERE/'IMAGEGEN_PROMPT.txt').write_text('''Generated with the built-in imagegen route. Prompt: five separate pictograms for a top-tier machine-learning paper on transparent background; editorial vector-like line illustrations; thin charcoal outlines; flat vivid teal, cobalt blue and orange; no words, letters, numbers, formulas, labels, watermark, gradients or shadows. Tiles: rollout trajectory; clustered transition graph; constraint gauge and crossed edge; observed-to-target flow projection; policy update actor chip.\n\nThe sheet was cropped into independent PNG assets; the final PPT keeps each asset as a separate movable picture object. The surrounding scientific graph, equations and labels remain editable native PPT objects.\n''')
(HERE/'APPEARANCE_PLAN.json').write_text(json.dumps({'base':'OriginalTemplate_R3','direction':'restore vivid original accents while keeping neutral borders and pale focal fills','accent_colors':{'blue':'285AA0','teal':'18785B','orange':'BA651F'},'generated_icons':'transparent PNG crops from imagegen sheet; no PPT primitive reconstruction','raster_boundary':'only six generated pictograms are raster assets; all text, arrows, graphs and equations remain native/outlined objects'},indent=2))
(HERE/'PROCESS_NOTES.md').write_text('''Started from immutable OriginalTemplate_R3. Restored the original vivid blue/teal/warm accent colors without changing layout or equations. Replaced four Figure1 decorative cost icons and two Figure2 rollout/agent icons with transparent imagegen pictograms. The pictograms are inserted as independent movable PPT picture objects; no icon is rebuilt from PPT primitives. Core graph motifs and all scientific text remain unchanged.\n''')
print('built',OUT)
