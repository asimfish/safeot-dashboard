# Attached-PDF reconstruction and current SafeOT adaptation

The author explicitly requested Figures1–2 from the attached paper to be converted FIRST, then changed to current SafeOT. The attached figures differ from the previously used earlier originals. Source pixels are preserved under `source/`, with page and SHA256 provenance.

`faithful/` contains historical editable reconstructions: original layout/content/palette, 5.5in wide, original aspect ratios. Original small fonts are retained and are below the current print requirement. These are historical references, not current-science figures. They are not claimed pixel-identical: font substitutions and condensed math are disclosed in each editability report.

`adapted/` contains separate current SafeOT copies made from those PPTXs, retaining the three-column unification teaser and five-stage method grammar. Both are5.5×3.3in; actual PDF text>=8.192pt, math including subscripts>=8.169pt. Formula fit and metadata checks pass. Source trace/gradient diagnostics remain in the work directory, not the paper package.

Editable boundaries: labels, borders, matrices, graph nodes/edges, routes and schematic curves are native objects. Formula glyph contours are grouped editable vectors with LaTeX source, not semantic OfficeMath. Figure1 retains four tiny source pictograms; Figure2 retains two. PDF/SVG therefore contain small raster icons. Fonts are Liberation Serif/newtx. Actual PPTX rendering was checked through LibreOffice; native PowerPoint rendering is unverified. Module movement and a child-label edit were tested on separate copies.

Figure1 contains no experiment data. Current hard masks are graph constraints; a separate executor is needed for action-time exclusions. Cost-category icons are illustrative, not a statement about benchmark composition. Price-rule endpoints are exact settings or conditional limits, not external-algorithm recoveries. Use the accompanying caption notes.

All prior branches remain unchanged. The adapted pair is for author visual review; no new cold-reader acceptance is asserted, and the manuscript remains under the owner’s control.
