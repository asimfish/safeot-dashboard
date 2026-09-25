# F02 R4 — terminology and cold-read consistency repairs

This is the updated R4 requested in the 20:20Z supplement. It supersedes the terminology-only R4 in this directory. That complete earlier delivery is preserved byte-for-byte in sibling `R4_text_only_2036Z/`; R3 and all other branches are unchanged. The manuscript owner selects/promotes the final figures after cold review.

## Preview and deliverables

- Figure1_F02_R4_300dpi.png; Figure2_F02_R4_300dpi.png: actual LibreOffice renders of the editable PPTX.
- Same stems: .pptx, .svg, .pdf, _grayscale.png, _deuteranopia.png, _protanopia.png.
- Figure1/2_equations.tex, formula_audit.json, font_editability_report.json, object_changes.json and editability_probe.json.
- F02_R4_sources.zip, requirements.json, checks.json, PROCESS_NOTES.md; native editing and export scripts.

## Numbered supplement changes

1. Every F/price star is now LaTeX `\star`: six formula groups, 7 star glyph occurrences. Same pdflatex/newtx typesetting at1:1, native vector outlines, no raster math or font shrinking.
2. Both hexagon target examples emphasize ONLY the lower teal route. Figure1 removes its three upper teal parallel arrows; the light-gray observed upper arrows remain. Figure2's target routing stays unchanged.
3. Figure1's SafeOT header moves up2pt, and “One flow, all budgets” up2.5pt. Graph/math positions stay fixed. Actual header-to-math ink gap is3.865pt,2.5pt greater than before.
4. Figure1's callout is “Prices before violations”.
5. Figure2's observed-cost feedback route and beta-to-sum arrow are dashed at1.1pt; the graph-price route stays solid at0.8pt. The short beta arrow extends left3pt, preserving its endpoint, so a dash is visible before its arrowhead in grayscale. Its native formula remains unchanged.
6. Figure2 panel2 arrow shafts encode observed flow with a schematic3:1 upper/lower split (1.8/0.6pt); “Width ∝ flow mass” supplies the key. The panel4 before-graph uses the same widths because it represents the same observed flow. Node positions, arrow endpoints and heads stay fixed. These are schematic encodings, not experimental data.

## Terminology retained from the 20:05Z request

Figure1 uses “hard constraint: excluded edge”, with Fixed penalty and Lagrangian unchanged. Figure2 uses Soft constraints, Hard constraints and safety prices. No visible filter/filtered label occurs; clip + EMA stays. Alpha, unhatted reward/cost advantages, the priced-advantage tilde, episode/per-step budgets and the outer next-rollout loop stay unchanged.

## Validation and editability

Both pages remain5.5×3.3in. Minimum exported label font8.107pt; minimum math including scripts8.169pt. All formulas fit at scale1. Zero raster objects in PPTX/PDF. Native objects outside the approved changes are XML-identical to the archived terminology-only R4; actual300dpi pixel differences outside the approved object regions are zero. Native formula-group move and child-label edit probes passed. Color and grayscale actual PPTX renders inspected; CVD previews supplied. Anonymous PDF/SVG exports checked.

Formulas are editable grouped vector contours with LaTeX source, not semantic OfficeMath. LibreOffice export is verified; PowerPoint rendering is not independently verified. This revision awaits the mentor's final cold read and does not claim acceptance. No manuscript or data changes.
