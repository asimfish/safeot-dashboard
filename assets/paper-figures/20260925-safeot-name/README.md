# SafeOT: current Figures1–5

This package supersedes the previously delivered names; it retains the R3 method layouts and R31 admitted data. Publication labels are **SafeOT**, **SafeOT (unclipped)**, and **SafeOT + PID feedback**. Historical raw arm IDs remain source identifiers. No data points, intervals or pairings changed.

- Figure1: R3 teaser, 5.5×2.9in, 32 labels including ticks.
- Figure2: R3 method, 5.5×2.3in, real newtx math.
- Figure3: admitted R31 forest and all-task curves, 5.5×4.1in; legends, direction/count text and ratio axis renamed.
- Figure4: admitted 19-run realization snapshot, 2.65×3.10in; image already name-free and pixel-identical after rebuilding. Caption identifies SafeOT. The separate 30-run refresh is not a naming change and is not silently substituted.
- Figure5: admitted local-budget data, 2.65×3.15in; ratio axes identify SafeOT and panels(b,c) explicitly identify SafeOT (unclipped). Sample counts remain in captions. The PID-feedback variant has a canonical mapping for plots where it is actually present; no new arm was inserted here.

All5 PDFs are native vector with embedded fonts and cleared metadata. Minimum actual font:7.1731pt for Figures1–2,7.2pt for Figures3–5.300dpi RGB/grayscale and color-vision previews accompany each PDF; outlined SVGs preserve vector editing. Figures1–2 also have editable TeX.

Rebuild: unzip editable_sources.zip, then run `python3 build_all.py`. Requires Python with Matplotlib,NumPy,Pillow,PyMuPDF, plus a TeX installation with TikZ/newtx. Numeric source snapshots are included. Verify public names and source invariance using rename_verification.json; every check passes. Data-figure provenance remains the admitted R31 snapshot, not a newly pooled estimator.

Independent R3 cold-reader acceptance and manuscript promotion remain with the writing owner and mentor. No manuscript source was edited.
