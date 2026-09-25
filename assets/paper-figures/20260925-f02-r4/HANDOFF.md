# F02 R4: terminology only

R4 was made from exact copies of the final R3 PPTXs, not from the separate attached-PDF branch. Only four native text nodes changed:

- Figure1: “hard event: excluded edge” → “hard constraint: excluded edge”. “Fixed penalty” and “Lagrangian” are unchanged.
- Figure2: “Soft budgets” → “Soft constraints”; “Hard exclusions” → “Hard constraints”; “budget duals” → “safety prices”.
- No visible “filter” or “filtered” occurs in either R3 figure. The internal object ID `filter_chain` is unchanged, and its visible “clip + EMA” equation is unchanged.

All other PPTX ZIP entries are byte-identical to R3. Within slide1.xml, reverting these four strings reproduces canonical R3 XML exactly. Positions, dimensions, fonts, styling, formulas, groups, native editability and connectors are unchanged. Actual LibreOffice 300dpi renders differ only within the four existing text boxes: zero changed pixels elsewhere. Each replacement fits its original box. Both figures remain5.5×3.3in; exported labels>=8.107pt and unchanged formula scripts>=8.169pt. Zero raster objects.

Deliverables: Figure1/2_F02_R4.pptx, .svg, .pdf, _300dpi.png; grayscale and CVD previews; unchanged LaTeX and formula audits; text-only object-change reports, checks and source ZIP. Export uses the same LibreOffice → anonymous PDF/SVG/PNG pipeline as R3. Formulas are editable vector outlines, not OfficeMath; PowerPoint rendering is unverified.

R3 and the author’s separate attached-PDF/current-architecture branch remain unchanged. R4 awaits cold review; manuscript source stays with the owner.
