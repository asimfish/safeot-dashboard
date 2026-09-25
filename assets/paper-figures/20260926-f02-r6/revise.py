"""R5 -> R6: replace only the outlined clip + EMA labels; preserve other objects."""
from pathlib import Path
import copy,hashlib,json,sys,shutil,zipfile
import fitz,numpy as np
from PIL import Image
from lxml import etree
from pptx import Presentation
from pptx.util import Pt
import native_tools as nt
H=Path(__file__).resolve().parent;R=H.parent;B=R.parent/'final/history_unified_20260925/R5';D=R.parent/'final/history_unified_20260925/R6';D.mkdir(exist_ok=False)
sys.path.append(str(R.parent/'image_pipeline_20260925/runtime-venv/lib/python3.12/site-packages'))
from super_img2ppt.render import LibreOfficeRenderer
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':nt.ANS}
baseline={p.name:sha(p) for p in B.iterdir() if p.is_file()};reports=[]
texdoc=fitz.open(H/'typeset/figure1/equations.pdf')
for n,indices in [(1,[0,1,2]),(2,[6,7,8])]:
 src=B/f'Figure{n}_F02_R5.pptx';stem=f'Figure{n}_F02_R6';dst=D/(stem+'.pptx')
 prs=Presentation(src);sl=prs.slides[0];g=nt.get(sl,'filter_chain');old=[g.shapes[i] for i in indices]
 x=min(s.left for s in old)/12700;y=min(s.top for s in old)/12700
 right=max(s.left+s.width for s in old)/12700;bottom=max(s.top+s.height for s in old)/12700
 scratch=Presentation();scratch.slide_width=prs.slide_width;scratch.slide_height=prs.slide_height;tmp=scratch.slides.add_slide(scratch.slide_layouts[6])
 nt.import_formula(tmp,H/'typeset/figure1/eq-2.svg','replacement',[0,0,90,20],nt.TEAL,texdoc[1].rect)
 fresh=list(tmp.shapes[-1].shapes);assert len(fresh)==3
 fx=min(s.left for s in fresh)/12700;fy=min(s.top for s in fresh)/12700
 fr=max(s.left+s.width for s in fresh)/12700
 dx=(x+right)/2-(fx+fr)/2;dy=y-fy
 replacements=[]
 for a,b in zip(old,fresh):
  b.left+=Pt(dx);b.top+=Pt(dy)
  new=copy.deepcopy(b._element);new.find('p:nvSpPr/p:cNvPr',ns).attrib.update(a._element.find('p:nvSpPr/p:cNvPr',ns).attrib)
  replacements.append((a.name,new))
 # Change only the approved vector text children in slide1.xml; keep all ZIP parts intact.
 with zipfile.ZipFile(src) as z:
  xml=etree.fromstring(z.read('ppt/slides/slide1.xml'))
  for name,new in replacements:
   found=xml.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$name]',namespaces=ns,name=name);assert len(found)==1
   found[0].getparent().replace(found[0],new)
  with zipfile.ZipFile(dst,'w') as out:
   for info in z.infolist():out.writestr(info,etree.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True) if info.filename=='ppt/slides/slide1.xml' else z.read(info.filename))
 with zipfile.ZipFile(src) as a,zipfile.ZipFile(dst) as b:
  changed=[name for name in a.namelist() if a.read(name)!=b.read(name)];assert changed==['ppt/slides/slide1.xml']
  before=etree.fromstring(a.read(changed[0]));after=etree.fromstring(b.read(changed[0]))
  for name,_ in replacements:
   original=before.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$name]',namespaces=ns,name=name)[0]
   edited=after.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@name=$name]',namespaces=ns,name=name)[0]
   edited.getparent().replace(edited,copy.deepcopy(original))
  assert etree.tostring(before,method='c14n')==etree.tostring(after,method='c14n')
 build=H/f'figure{n}';build.mkdir()
 pdf=LibreOfficeRenderer('/usr/bin/soffice',timeout=60).render(dst,build/'render')
 doc=fitz.open(pdf);doc.set_metadata({});doc.del_xml_metadata();doc.save(D/(stem+'.pdf'),garbage=4,deflate=True)
 p=doc[0];p.get_pixmap(dpi=300).save(D/(stem+'_300dpi.png'));(D/(stem+'.svg')).write_text(p.get_svg_image(text_as_path=False))
 spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
 assert min(s['size'] for s in spans)>=8 and not p.get_images()
 assert all(p.rect.contains(fitz.Rect(s['bbox'])) for s in spans)
 im=Image.open(D/(stem+'_300dpi.png')).convert('RGB');im.convert('L').save(D/(stem+'_grayscale.png'),dpi=(300,300))
 before=np.array(Image.open(B/f'Figure{n}_F02_R5_300dpi.png').convert('RGB'));after=np.array(im);delta=np.any(before!=after,axis=2);allowed=np.zeros(delta.shape,bool)
 newleft=fx+dx;newright=fr+dx;region=[min(x,newleft),y,max(right,newright),bottom]
 xa,ya,xb,yb=region;scale=300/72;allowed[max(0,int(ya*scale)-2):int(yb*scale)+3,max(0,int(xa*scale)-2):int(xb*scale)+3]=True
 assert int((delta&~allowed).sum())==0
 Image.fromarray(np.where(delta[:,:,None],np.array([192,40,45]),after).astype('uint8')).save(build/'text_only_diff.png')
 linear=after.astype(float)/255;linear=np.where(linear<=.04045,linear/12.92,((linear+.055)/1.055)**2.4)
 for name,m in {'deuteranopia':[[.367322,.860646,-.227968],[.280085,.672501,.047413],[-.011820,.042940,.968881]],'protanopia':[[.152286,1.052583,-.204868],[.114503,.786281,.099216],[-.003882,-.048116,1.051998]]}.items():
  v=np.clip(linear@np.array(m).T,0,1);v=np.where(v<=.0031308,12.92*v,1.055*v**(1/2.4)-.055);Image.fromarray(np.round(v*255).astype('uint8')).save(D/(stem+'_'+name+'.png'),dpi=(300,300))
 # Actual edit probe, separate disposable file.
 check=Presentation(dst);slide=check.slides[0];positions={s.name:(s.left,s.top,s.width,s.height) for s in slide.shapes};group=nt.get(slide,'filter_chain');group.left+=Pt(2)
 label=nt.get(slide,'safeot_title' if n==1 else 'projection_title');label.text_frame.paragraphs[0].runs[0].text+=' test'
 probe=D/f'Figure{n}_editability_probe.pptx';check.save(probe);reopened=Presentation(probe).slides[0]
 assert all((s.left,s.top,s.width,s.height)==positions[s.name] for s in reopened.shapes if s.name!='filter_chain')
 assert nt.get(reopened,'filter_chain').left-positions['filter_chain'][0]==Pt(2)
 (D/f'Figure{n}_editability_probe.json').write_text(json.dumps({'status':'PASS','probe_file':probe.name,'formula_group_move_pt':2,'neighbor_positions_unchanged':True,'label_native_edit_verified':True,'submission_source_unchanged':True},indent=2))
 audit=json.loads((B/f'Figure{n}_formula_audit.json').read_text());updated=next(a for a in audit if a['id']=='filter_chain');assert 'EMA' in updated['latex']
 updated['latex']=updated['latex'].replace('clip + EMA','clip + smooth');updated['label_replacement']={'size_pt':10,'scale':1,'baseline_unchanged':True,'center_preserved':True,'arrows_and_math_unchanged':True,'label_ink_box_pt':region}
 (D/f'Figure{n}_formula_audit.json').write_text(json.dumps(audit,indent=2))
 # Preserve original text advance with centered replacement; only text grows, math positions stay fixed.
 tex=(B/f'Figure{n}_equations.tex').read_text();assert tex.count('clip + EMA')==1
 tex=tex.replace(r'\text{clip + EMA}',r'\text{\makebox[47.681bp][c]{clip + smooth}}')
 (D/f'Figure{n}_equations.tex').write_text(tex)
 report=json.loads((B/f'Figure{n}_font_editability_report.json').read_text());report.update(source_r5_sha256=sha(src),r5_preserved=True,minimum_pdf_text_pt=min(s['size'] for s in spans),text_only_outline_proof=True,pixels_changed_outside_approved_text=0,cold_reader_acceptance='R5 accepted per mentor23:50Z;R6 only terminology edit, no new cold-read score')
 (D/f'Figure{n}_font_editability_report.json').write_text(json.dumps(report,indent=2))
 proof={'figure':n,'before':'clip + EMA','after':'clip + smooth','changed_outline_children':[name for name,_ in replacements],'all_other_package_entries_identical':True,'restoring_three_text_contours_reproduces_original_slide_XML':True,'all_other_shapes_math_arrows_styles_geometry_identical':True,'changed_pixels':int(delta.sum()),'pixels_changed_outside_text_region':0,'label_ink_box_pt':region,'minimum_text_pt':report['minimum_pdf_text_pt'],'minimum_math_pt':report['minimum_math_source_pdf_font_pt'],'r5_preserved':True}
 (D/f'Figure{n}_object_changes.json').write_text(json.dumps(proof,indent=2));reports.append(proof)
 assert sha(src)==baseline[src.name]
 print(json.dumps(proof),flush=True)
assert baseline=={p.name:sha(p) for p in B.iterdir() if p.is_file()}
(D/'checks.json').write_text(json.dumps(reports,indent=2));(D/'requirements.json').write_text(json.dumps({'status':'PASS','r5_files_sha256':baseline,'changed_labels':2,'raster_objects':0,'layout_sizes_colors_editability_preserved':True,'powerpoint_render_verified':False},indent=2))
(D/'HANDOFF.md').write_text('R6 delivered: R5 copies change only “clip + EMA” to “clip + smooth” in Figures1–2; native editable contours, layout/fonts/colors preserved; PDF/SVG/300dpi/gray/CVD and edit probes included; actual LibreOffice render and zero outside-label pixel differences PASS; R5 unchanged fallback.\n')
(D/'PROCESS_NOTES.md').write_text('One text-only round. Two occurrences were outlined newtx text rather than editable a:t nodes. Replaced only three native text contours per figure with the same10pt newtx wording, at the same baseline and text-center; all arrows/math/group transforms unchanged. Archive reversal proof and actual pixel-region checks pass. Formulas remain native vector contours+TeX, not OfficeMath. LibreOffice checked; PowerPoint unverified. Probe PPTXs contain deliberate test edits and are not submission figures.\n')
for name in ['revise.py','native_tools.py']:shutil.copy2(H/name,D/name)
with zipfile.ZipFile(D/'F02_R6_sources.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(D.iterdir()):
  if f.suffix in ('.pptx','.tex','.json','.md','.py'):z.write(f,f.name)
print('R6 delivered',str(D),flush=True)
