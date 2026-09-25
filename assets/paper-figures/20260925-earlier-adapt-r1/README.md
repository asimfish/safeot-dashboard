# SafeOT-Dual Figures 1–2

Run in an isolated environment:

```sh
python -m pip install -r requirements.txt
python build_pair.py
python build_editable.py
python make_accessibility.py
```

All coordinates are printer points. Figure 1 is 5.5 × 3.139 in and Figure 2 is 5.5 × 3.014 in. Use exactly the 5.5 in width; scaling down reduces the 7 pt minimum. Fonts are Liberation Serif and STIXGeneral (the latter ships with Matplotlib). Install these fonts for editable PowerPoint/SVG rendering on a new computer. The PDF embeds both fonts and the primary SVG contains vector outlines, so these exports do not require font installation. `_editable.svg` retains text.

The PowerPoint contains native editable shapes and text, with no raster images or theme shadows. The Python source and scene JSON provide a second editable representation. Small typography differences between PowerPoint renderers remain possible; the vector PDF is the publication reference.

The two Figure 1 curves are explicitly schematic. They do not encode experimental results. Figure 2 shows aggregate soft budgets, excluded hard edges, joint dual prices, realized-cost feedback and a priced policy update. The target flow is not directly executed. Limits in Figure 1 require the assumptions in the manuscript.

Author, creator and related metadata are cleared from final PDF/SVG and PowerPoint exports. Captions are in `captions.json`. Accessibility previews are diagnostic simulations; labels, stage order, dashed excluded edges and numeric symbols provide redundant encoding.
