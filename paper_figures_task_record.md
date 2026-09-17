# T-1584 · Paper figure panel update

The owner requested that the revised figures be made available on the existing dashboard after local HTML previews failed to load sibling image paths.

This update adds a paper-figure page, visible links on both dashboard navigation menus and a compact homepage preview. It hosts the existing Figure1 unified v01, Figure2 framework v03 and two-page PDF at versioned same-origin URLs. Original image/PDF bytes are unchanged; checksums are in `assets/paper-figures/20260916/manifest.json`.

The figure page identifies the files as PNG design revisions. Editable conversion, manuscript typography and ICLR page compliance are not claimed. Existing experimental data, collection scripts and the data branch are outside this update.

Validation: original artifact hash parity, two loaded image elements, navigation/download targets, desktop/mobile page layout, existing JavaScript preservation and publication verification are recorded in the SafeTransport T-1584 task record.


## T-1599 · 2026-09-18 editable delivery

Continued the user-requested figure conversion using image-to-editable-ppt. Added combined/individual PPTX, actual PPT-export previews, vector PDF/SVG, LaTeX/font source bundle and an exact 396pt-width inspection sheet. Original generated PNGs remain the default view; the page can switch to the editable export. Existing collectors and experimental data are untouched.

Both page builds, records and deck finalization passed; the exported vector PDF has zero raster images. Source-matched small labels remain 3–6pt at paper width, disclosed on the page. Formula SVG objects are editable as separate objects with retained LaTeX, not native Office equations. No full-manuscript ICLR compliance claim is made.

Checksums of all new assets are in assets/paper-figures/20260918-editable/manifest.json.
