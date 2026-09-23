# SafeOT-Dual — Figures 1–2, 2026-09-23

Figure 1 presents one shared price rule across its constrained and penalty-like regimes. Figure 2 shows the current on-policy algorithm: graph pricing, clipping/filtering, realized-cost feedback, and normalized priced-advantage PPO/TRPO. The obsolete flow-ratio update has been removed. The diagrams make no measured-performance or deployment-safety claim.

## Files

- `SafeOT_Dual_Figures_editable.pptx`: both figures, native editable shapes/text, physical width 5.5 inches. Figure 1 has a small bottom margin to match Figure 2's canvas; objects retain their original sizes.
- `Figure1_SafeOT_Dual.*`, `Figure2_SafeOT_Dual.*`: separate PPTX, tight vector PDF, editable SVG and actual PPT render PNG.
- `SafeOT_Dual_Figures_vector.pdf`: two-page vector export of the combined PPT.
- `ICLR2027_figure_placement.pdf`: two-page actual-size figure-and-caption sample in the unmodified official ICLR2027 style. This is not the full manuscript or a manuscript page-limit certificate.
- `captions.tex`, `claim-audit.md`, `iclr-format-check.md`: captions, scientific scope and formatting evidence.
- `Figure*_generated_draft.png`: image-generated drafts, retained separately from the refined native figures.
- `SafeOT_Dual_source_bundle.zip`: deliverables plus portable resolved scenes, source images, prompts, appearance/typography/editability checks and pinned tool versions.

## Editing and rendering

Figure 1 contains 222 native leaf objects in 57 groups; Figure 2 contains 240 native leaf objects in 70 groups. Neither final figure contains raster artwork. Select a logical component as a group; enter or ungroup it to edit individual labels and symbols. Group-move and label-edit probes passed, with surrounding objects unchanged.

Equations use grouped, styled PowerPoint text and line objects. They are editable but are **not Office equation/OMML objects**. External arrows have fixed endpoints and require manual adjustment after moving components.

Install **Liberation Serif** and **DejaVu Sans** to reproduce the tested layout. Fonts are not embedded in the PPT. Actual exports were checked through LibreOffice/PDFium, with no font substitution detected; Microsoft PowerPoint and WPS GUI rendering have not been tested. Ordinary text is at least 7.11 pt (Figure 1) and 7.06 pt (Figure 2) at 5.5-inch width; mathematical scripts are smaller, down to approximately 3.3 pt. Review the vector PDF at final print size before submission.

## Rebuilding the figures

Use SuperImg2PPT 0.3.15, commit `bf00a08c87f18f5079d976949212db10a6cee7d9`. From the unpacked bundle, for either `figure1` or `figure2`:

```bash
super-img2ppt build source/figure1/scene.resolved.json --appearance-mode redesign --appearance-plan source/figure1/appearance-plan.json --out rebuilt-figure1
```

The scene references relative assets bundled alongside it. Preserve those paths. The original authoring workspace and rejected iterations are retained locally; this public bundle contains the selected deliverables and supporting audits.

## Provenance and limits

SuperTeaser 3.2.21 scientific and visual contracts guided the image-generation drafts. The built-in image service did not expose its model version, so no GPT-image-2.5 claim is made. Editable reconstruction used the requested GPT-6 Astra max workers and SuperImg2PPT. Color, type size and routing were deliberately refined after reconstruction; the result is not claimed to be a pixel-identical copy. Figure 1 has two noisy source text-color regions without stable source-core measurements; the selected final target colors passed independent checks and the unresolved source audit is retained.

The recovered experiment snapshot does not establish the graph solver's advantage over the cost-triggered switch. No new experiment was run for these figures. Writing, complete-manuscript typography, bibliography and formal review pipelines remain separate tasks; listing those tools does not mean those audits have been completed.
