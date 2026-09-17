# SafeTransport editable figures

The combined PPTX has two slides; individual Figure1/2 PPTX files are also provided. Text, graph nodes, edges, capacity matrix cells, boxes and lines are native editable objects. Mathematical expressions are separate SVG objects with retained LaTeX under source/pages; they are not native Office equations.

The PDF, SVG and PNG previews were exported from the actual combined PPTX with LibreOffice. The PDF is vector content with no raster image objects. Original generated PNGs are preserved separately on the dashboard.

## Print-size limitation

The conversion keeps the current source composition and text scale. At the manuscript text width of 396 pt / 5.5 in, many native labels are about 3–6 pt. The 7 pt threshold used in the report is an internal readability target, not an asserted official ICLR minimum. Paper_width_check_396pt.pdf places each figure at the exact target width on a letter page. These files have not replaced the manuscript or passed a full ICLR page-count/font audit.

## Source

The source bundle contains per-page manifests, formula SVG/TeX files and reconstruction scripts. The manifests use relative formula asset paths. Rendering/building uses the image-to-editable-ppt skill runtime. Source normalization, structural validation and actual page rendering passed. Configured external OCR timed out; local ink measurements and source reading were used.

Install the included Liberation Sans regular/bold fonts before editing on a machine where they are absent. They are bundled unmodified with their SIL Open Font License to reduce font substitution and layout changes.
