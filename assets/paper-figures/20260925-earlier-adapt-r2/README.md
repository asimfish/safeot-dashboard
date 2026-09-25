# SafeOT-Dual figures — modular current-method revision

Run in an isolated environment:

```sh
python -m pip install -r requirements.txt
python build_pair.py
python build_editable.py
python make_accessibility.py
```

Figure 1 is 5.5 × 3.583 in; Figure 2 is 5.5 × 3.014 in. Use at 5.5 in width so all scripts and labels remain at least 7 pt. Liberation Serif is Times-compatible; STIXGeneral provides mathematical brackets. Install both for native PowerPoint or text SVG rendering. PDF embeds the fonts; the primary SVG outlines its glyphs. `_editable.svg` and the PowerPoint retain editable text; all diagram geometry and data curves remain native shapes.

`figure3c_alltask_aggregate.csv` is the unchanged 600-row producer snapshot. The figure selects the 300 SafeOT-Dual/TRPO-Lag cost/B medians, without smoothing. Bullet uses a labelled log y axis; its peak is fully visible. The shading is descriptive median-curve excess, not the reported V statistic. `primary_V_summaries.json` preserves the separate headline estimates, intervals and denominators. See `ESTIMANDS.md` before interpreting comparisons or replacing data.

The two top-left curves are labelled schematic. The Lagrangian sketch integrates previously observed excess using projected ascent, so the feedback price does not increase before violation. Joint flow graphs and geometry are conceptual. No experimental reward or cost values are modified. Native PPT uses explicit styling without shadows. PDF is the publication reference because font substitution can change PowerPoint spacing.

Exports remove identity metadata. Source rebuilds require no external service or manuscript content. CVD previews are diagnostic simulations, with line patterns and textual labels providing redundant encoding.
