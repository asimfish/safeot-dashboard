# F02 R3 handoff

## Delivery and status

Direct revisions of the R2 editable PPTX copies, 5.5 × 3.3 inches. Figure 1 R2 was accepted in the mentor's two independent reads (4/4/4/4 each). That acceptance is not assigned to either R3 file: both revised renders await the mentor's review, and only the manuscript owner promotes figures.

- Figure 1: `Figure1_F02_R3.pptx`, `.svg`, `.pdf`, and `_300dpi.png`.
- Figure 2: `Figure2_F02_R3.pptx`, `.svg`, `.pdf`, and `_300dpi.png`.
- Each figure also has grayscale, deuteranopia and protanopia previews, a font/editability report, a formula audit, and an object-change record.
- `F02_R3_sources.zip` contains both editable figures, LaTeX equations, revision/export scripts and verification records.

## Response to the five requested changes

1. Figure 2 feedback uses alpha: beta_k ← [beta_k + alpha (Jbar_k − B_k)]_+.
2. Figure 2 rollout and priced update use A_r and A_{c_k}, without hats; the priced advantage retains its tilde. The three changed equation groups were generated with pdflatex/newtx at scale 1 and imported as native vector contours.
3. The return route is one open native freeform path with six vertices, from pi_{t+1} around the right, bottom and left exterior to pi_t. The orange observed-cost route instead enters the feedback update through an inner gap. The return label has 6.6 pt of lower margin; the nearest outer-left and inner-cost vertical segments are separated by 109.8 pt. The white-backed advantages label is above its connector and is not struck through.
4. Figure 1 now includes a gray '(schematic)' under each side-panel subtitle. All formerly sub-8 pt labels were increased to 8.1 pt without moving the accepted composition.
5. Optional long flow legend skipped to preserve the accepted central layout. At a readable size its actual newtx width is 222.429 pt, while the existing key has only 101 pt; adding it would displace the budget formula and graph. The existing symbolic key remains. Measurement is in `legend_measurement.json`.

## Verification and limitations

- Actual LibreOffice PPTX export, then vector PDF/SVG and 300 dpi PNG. Color and grayscale print previews reviewed.
- Minimum exported text: 8.107 pt. Minimum mathematical font, including subscripts/superscripts in the source PDF at 1:1: 8.169 pt. Formula contours in the final PDF do not carry font metadata, so their sizes are checked against the source PDF and import scale.
- No raster objects in either PPTX or PDF. Formula groups remain editable vector shapes; they are not semantic OfficeMath. Exact LaTeX is supplied. PowerPoint's renderer has not been independently tested.
- Text/formula bounds, required notation, one-path geometry and source-preservation checks pass. PDF/SVG metadata have been cleared. Source R2 PPTX hashes are unchanged.
- A disposable native-edit probe moved one formula group and edited a title without moving neighboring objects.
- No experiment values or manuscript files changed. The separate earlier-style/current-content branch and all prior R2 files remain available for comparison.

## Owner action

Use the two `_300dpi.png` files for the next cold read. If accepted, integrate the corresponding PDF. The drawing agent has not replaced manuscript figures or assigned new cold-reader scores.
