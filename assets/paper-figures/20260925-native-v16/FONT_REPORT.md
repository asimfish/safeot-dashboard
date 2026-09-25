# Native method figures — print audit

| Figure | Width × height | Minimum actual PDF font | Module titles | English words | Embedded raster images |
|---|---|---|---|---|---|
| 1: teaser | 5.5 × 2.5 in | 7.1731 pt | 8.767 pt | 45 / 45 | 0 |
| 2: framework | 5.5 × 2.3 in | 7.1731 pt | 8.767 pt | 37 / 60 | 0 |

PDF points are 1/72 inch. All visible text spans, including math scripts and superscripts, were inspected with PyMuPDF. Ordinary TeX points were set slightly larger to clear the PDF-point floor. All fonts are embedded Type 1, from TeX Gyre Termes / NewTX; no Type 3 or unembedded font is used. Full span-size and font inventories are supplied in the JSON reports.

PNG print previews are 1650 × 750 px and 1650 × 690 px with 300 dpi metadata. SVG files contain native vector paths, including outlined text; edit wording in the accompanying TikZ source rather than attempting text editing of outlines. These exports do not contain embedded raster art. The TeX sources are independently editable and compilable with newtxtext, newtxmath, TikZ and standalone.

Visual checks: module borders and text do not collide; graph arrowheads are visible; the hard edge is distinguished by a red dashed cross; the GAE bypass and policy loop are separate; the only graph-to-policy signal is the filtered price. Print-scale and grayscale previews were inspected. No claim of author approval is implied.

Words count English labels, abbreviations and named text operators, including clip-filter, const, KL and PPO/TRPO. Mathematical variables and equation/reference numbers are excluded; hyphenated compounds count as one word. The exact counted-token ledger is in each JSON report.

Author, Creator, Producer, timestamps, document Info and XMP are cleared from the PDF. SVG contains no metadata element, personal account or external link. PNGs contain resolution metadata only.
