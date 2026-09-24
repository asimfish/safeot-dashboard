# SafeOT-Dual — V11 visual mechanism revision (2026-09-25)

The author found V10 cluttered and formula-heavy. V11 replaces displayed objectives
and update equations with visible operations: encode joint costs, price one graph,
condition its prices, combine cost feedback, and update one policy. Full equations
remain in the manuscript and companion captions.

Figure1 connects penalty and constraint views to a single shared construction.
Cost-map tiles feed one graph; conditioned graph prices and feedback combine into
a shared price vector for the same policy update. The two upper leaders are
conceptual relationships, not separate algorithm branches. Zero-cap settings are
exact; conditional graph-price limits do not recover CPO.

Figure2 follows Observe → Construct shared prices → Update policy. The graph solve
and cost-feedback branch are inside one core. Clipping is shown as an analytic
response. GAE independently supplies reward and cost advantages. Prices weight
the cost advantages; reward minus weighted cost is normalized before PPO/TRPO.
The outer loop returns to rollout. A gap at the blue/teal line crossing means an
underpass, not a junction. Only prices pass from the graph to the actor.

Blue means policy/observation, teal means graph/shared prices, ochre means costs
and feedback. All motifs are schematic; no experimental measurements are depicted.
Three illustrated channels represent an arbitrary number of costs. The graph's
balance is discounted. Graph budgets are per-step B_k/L, feedback uses episodic B_k.
Hard graph exclusion and a finite hard-channel policy penalty do not certify
policy support or deployed-policy safety.

The two delivered figures contain 309 native leaf objects, no raster artwork.
PNG previews are actual LibreOffice renders of the PPTX. Labels, mathematical
symbols, nodes and connectors are editable; mathematical symbols are grouped
text/lines, not Office Math. Moving a group does not auto-reroute external arrows.
Use Liberation Sans and Liberation Serif when editing. Fonts are embedded in PDF,
not in the PPTX. PowerPoint/WPS rendering was not independently checked.

Geometry, native objects, actual-render text/fonts and the opaque white target-fill
checks pass. Duplicate-file group movement and label editing were verified. The
smallest ordinary label is about 6.24 pt at 5.5 inches / 6.11 pt at the checked paper
width; mathematical subscripts are smaller. The isolated paper preview retains
9 main / 57 total pages, with embedded fonts and zero overfull or unresolved
reference diagnostics. ICLR2027_figure_placement.pdf contains the two figure pages.
This checks figure placement, not all current venue submission requirements.

SuperTeaser's visual mechanism/composition guidance and built-in image generation
were used for proposals. Provider model ID was not exposed. SuperImg2PPT 0.3.15
was used for native semantic reconstruction, not pixel-faithful tracing. Generated
proposals are preserved as unadopted history; their price/GAE labels and connections
are corrected in the native version. No borrowed paper artwork is included.

V00–V10 and all dated assets are retained. V11 remains a comparison candidate on the
same frozen R2 method; canonical main.pdf and active writing revisions are unchanged.
