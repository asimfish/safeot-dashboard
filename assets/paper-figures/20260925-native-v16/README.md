# V16 native method figures

Figure 1 is the teaser and Figure 2 is the method framework. Both preserve the approved V14 three-column/two-band compositions while enforcing final print dimensions and a 7 pt minimum. Treat these as review candidates; keep the V14 raster fallback until the writing owner accepts the vector versions.

Use `\includegraphics[width=\textwidth]{Figure1.pdf}` and similarly for Figure 2 in a 5.5 in text block. Do not downscale them. Suggested placement: Figure 1 on page 2; Figure 2 at the top of page 3 or 4. The source contains no float barriers or manuscript changes.

Captions carry the conditional price limits, graph-versus-execution distinction, graph/episode budget units and schematic feedback caveat. Caption equation labels match the R21 method source; the writing owner must preserve or resolve these labels on integration.

To edit/rebuild a single figure: `pdflatex -halt-on-error Figure1.tex`. Reapply metadata stripping to the resulting PDF before submission. The distributed PDFs and SVGs are already anonymous. Do not replace them with an unstripped compilation.

The native SVGs have outlined glyphs; the editable text/formulas live in the TikZ files. The dimensions and full font report are supplied alongside 300 dpi color and grayscale previews. These are diagrams, not measured data plots.
