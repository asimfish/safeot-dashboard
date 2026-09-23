# T-1584 · Paper figure panel update

The owner requested that the revised figures be made available on the existing dashboard after local HTML previews failed to load sibling image paths.

This update adds a paper-figure page, visible links on both dashboard navigation menus and a compact homepage preview. It hosts the existing Figure1 unified v01, Figure2 framework v03 and two-page PDF at versioned same-origin URLs. Original image/PDF bytes are unchanged; checksums are in `assets/paper-figures/20260916/manifest.json`.

The figure page identifies the files as PNG design revisions. Editable conversion, manuscript typography and ICLR page compliance are not claimed. Existing experimental data, collection scripts and the data branch are outside this update.

Validation: original artifact hash parity, two loaded image elements, navigation/download targets, desktop/mobile page layout, existing JavaScript preservation and publication verification are recorded in the SafeTransport T-1584 task record.


## T-1599 · 2026-09-18 editable delivery

Continued the user-requested figure conversion using image-to-editable-ppt. Added combined/individual PPTX, actual PPT-export previews, vector PDF/SVG, LaTeX/font source bundle and an exact 396pt-width inspection sheet. Original generated PNGs remain the default view; the page can switch to the editable export. Existing collectors and experimental data are untouched.

Both page builds, records and deck finalization passed; the exported vector PDF has zero raster images. Source-matched small labels remain 3–6pt at paper width, disclosed on the page. Formula SVG objects are editable as separate objects with retained LaTeX, not native Office equations. No full-manuscript ICLR compliance claim is made.

Checksums of all new assets are in assets/paper-figures/20260918-editable/manifest.json.


## T-FIG-20260923 · 2026-09-23 SafeOT-Dual price framework

Updated Figure 1 to show one shared price rule and its qualified endpoint regimes. Figure 2 now transfers graph-solved prices into the on-policy update, with a separate GAE branch and episode-cost feedback. The retired flow-ratio update is removed. Teal/charcoal, line weights and ordinary label sizes are consistent. The page defaults to actual editable-PPT exports and keeps the image-generated drafts and September18 page available for comparison.

Added independent and combined native PPTX, vector PDF/SVG, source scenes and audits, captions, editing notes and an actual-size placement proof compiled with the unmodified ICLR2027 style. The native figures contain 222 and 240 leaf objects with no raster artwork. The combined deck preserves individual physical font sizes. Ordinary labels are at least 7.11/7.06pt at 5.5in; smaller mathematical scripts are documented. Equations use editable grouped parts, not OMML. Fonts are not embedded and PowerPoint/WPS GUI appearance is unverified.

Validation: selected SuperImg2PPT builds pass; representative group movement/label edits pass; combined PDF text/fonts match independent exports; official-template proof has no overflow; ZIP/source paths and delivery checksums verified. Browser/download publication checks are recorded in the parent SafeTransport task. No experiment files, collection code or root manuscripts changed; full-paper page-limit/citation compliance and graph-solver efficacy are not claimed.

Assets and hashes: `assets/paper-figures/20260923-pricing/manifest.json`.

Portable source-package follow-up: the combined-deck reconstruction script now locates deliveries from the extracted ZIP root. The extracted package was exercised: native combination preserved all figure text/font sizes and contained no raster images. Scene checks pass for both extracted individual sources.
