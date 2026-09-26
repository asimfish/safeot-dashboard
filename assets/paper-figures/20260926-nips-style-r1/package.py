from pathlib import Path
import json, hashlib, zipfile
from PIL import Image, ImageOps
from pptx import Presentation
import fitz
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
RENDER=ROOT/'render_final3'
# Anonymous metadata on the editable sources.
for ppt in [ROOT/'Figure1_NIPSStyle_R1.pptx', ROOT/'Figure2_NIPSStyle_R1.pptx']:
    prs=Presentation(str(ppt)); cp=prs.core_properties
    cp.author=''; cp.last_modified_by=''; cp.company=''; cp.comments=''; cp.keywords=''; cp.subject='';
    prs.save(str(ppt))

records=[]
for n in [1,2]:
    stem=f'Figure{n}_NIPSStyle_R1'
    srcpdf=RENDER/(stem+'.pdf')
    # strip PDF metadata while retaining vector content
    rd=PdfReader(str(srcpdf)); wr=PdfWriter()
    for page in rd.pages: wr.add_page(page)
    wr.add_metadata({'/Title':f'Figure {n} SafeOT','/Author':'','/Creator':'','/Producer':'','/Subject':''})
    outpdf=ROOT/(stem+'.pdf')
    with outpdf.open('wb') as f: wr.write(f)
    # render from the cleaned PDF at 300 dpi
    doc=fitz.open(str(outpdf)); page=doc[0]
    pix=page.get_pixmap(matrix=fitz.Matrix(300/72,300/72), alpha=False)
    outpng=ROOT/(stem+'_300dpi.png'); pix.save(str(outpng))
    svg=page.get_svg_image(matrix=fitz.Matrix(1,1), text_as_path=1)
    (ROOT/(stem+'.svg')).write_text(svg, encoding='utf-8')
    im=Image.open(outpng).convert('RGB')
    ImageOps.grayscale(im).convert('RGB').save(ROOT/(stem+'_grayscale.png'))
    # Simple Brettel-style preview matrices; these are accessibility previews, not paper outputs.
    import numpy as np
    arr=np.asarray(im).astype(float)/255.0
    mats={
      'deuteranopia':np.array([[0.625,0.375,0.0],[0.70,0.30,0.0],[0.0,0.30,0.70]]),
      'protanopia':np.array([[0.567,0.433,0.0],[0.558,0.442,0.0],[0.0,0.242,0.758]]),
    }
    for label,m in mats.items():
      x=np.clip(arr@m.T,0,1); Image.fromarray((x*255).astype('uint8')).save(ROOT/(stem+f'_{label}.png'))
    records.append({'figure':n,'pptx':f'Figure{n}_NIPSStyle_R1.pptx','pdf':outpdf.name,'svg':(ROOT/(stem+'.svg')).name,'png':outpng.name,'size_pt':[float(page.rect.width),float(page.rect.height)],'sha256':hashlib.sha256(outpdf.read_bytes()).hexdigest()})

# Font scan of editable text runs. Outlined legacy glyph groups remain part of the faithful NIPS baseline.
font={}
for n in [1,2]:
 ppt=ROOT/f'Figure{n}_NIPSStyle_R1.pptx'; prs=Presentation(str(ppt)); vals=[]; authored=[]
 def rec(sh):
  if hasattr(sh,'shapes'):
   for x in sh.shapes: rec(x)
  elif hasattr(sh,'text_frame'):
   for p in sh.text_frame.paragraphs:
    for r in p.runs:
     if r.text.strip() and r.font.size:
      vals.append(float(r.font.size.pt))
      if sh.name.startswith('current_') or sh.name in {'middle_title','left_title','hard_title','title1','title2','title3','title4','title5','collect','one_matrix','iterations','iter_row','iter_col','iter_projected','repeat_label','weights','ppo_label','costname0','costname1','costname2','costname3','costvalues0','costvalues1','costvalues2','costvalues3'}: authored.append(float(r.font.size.pt))
 for s in prs.slides[0].shapes: rec(s)
 font[str(n)]={'all_text_runs_min_pt':min(vals) if vals else None,'authored_text_min_pt':min(authored) if authored else None,'all_text_runs_count':len(vals),'authored_text_count':len(authored),'outlined_legacy_math':True}
(ROOT/'font_report.json').write_text(json.dumps(font,indent=2,ensure_ascii=False))
(ROOT/'manifest.json').write_text(json.dumps({'branch':'NIPSStyle_R1','basis':'AttachedPDF_R1/faithful plus NIPS 2026 visual grammar','figures':records,'experiments_in_teaser':False,'paper_source_modified':False,'anonymous_exports':True},indent=2,ensure_ascii=False))
(ROOT/'HANDOFF.md').write_text('''# NIPSStyle_R1 handoff\n\nThis is a separate review candidate built from the preserved NIPS/AttachedPDF_R1 editable visual baseline. It keeps the vivid three-panel / five-stage grammar, whitespace, panel proportions, curves, matrices, and generated pictogram anchors, while replacing the stale narrative labels with current SafeOT terminology:\n\n- Figure 1: penalty view → SafeOT one-flow pricing → constraint view, with the one-price-rule spectrum. No experimental data are included.\n- Figure 2: rollout → flow inputs → soft/hard constraints → one flow projection → priced PPO/TRPO update.\n\nR3, R4, R5, R6, OriginalTemplate_R3/R4 and the original faithful PPT files are unchanged. This branch is a visual candidate only; it is not promoted into the manuscript. PPTX remains the editable source; the SVG/PDF are vector exports. Generated icon PNGs are retained beside the source.\n''',encoding='utf-8')
(ROOT/'PROCESS_NOTES.md').write_text('''# Process notes\n\n1. Restored the preserved NIPS visual grammar rather than iterating on the rejected R3/R4 layout.\n2. Kept the original panel geometry, vivid blue/green/red/orange hierarchy, curves, matrices, and bottom spectrum.\n3. Replaced stale method labels with SafeOT content and removed stale solver/importance-weight formula outlines from Figure 2.\n4. Inserted generated transparent pictograms as independent PPT picture objects in the card/anchor slots.\n5. Rendered through LibreOffice at 5.5-inch figure width; cleaned PDF metadata and generated vector SVG plus grayscale/CVD previews.\n\nOpen items for visual review: the NIPS baseline contains a few legacy outlined glyphs by design; this candidate is for side-by-side selection, not a claim of final manuscript compliance.\n''',encoding='utf-8')
# Zip the editable source and generated assets.
with zipfile.ZipFile(ROOT/'NIPSStyle_R1_sources.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in [ROOT/'Figure1_NIPSStyle_R1.pptx',ROOT/'Figure2_NIPSStyle_R1.pptx',ROOT/'build.py',ROOT/'package.py',ROOT/'font_report.json',ROOT/'manifest.json',ROOT/'HANDOFF.md',ROOT/'PROCESS_NOTES.md']+list(ROOT.glob('icon_*.png')):
        z.write(p,p.name)
print(json.dumps({'root':str(ROOT),'font':font,'records':records},ensure_ascii=False,indent=2))
