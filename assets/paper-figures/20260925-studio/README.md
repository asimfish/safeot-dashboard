# SafeOT-Dual — two design pairs, 2026-09-25

A / V12: central engine with in-place mechanisms; sans-serif labels.
B / V13: central synthesis spine and graph/policy bands; serif headings.
B is the proposed visual direction for comparison, not an author-approved final.

These are generated raster candidates, not native editable PowerPoint slides.
The PDF previews embed the original PNGs at 5.5 inches wide (no image edits).
Older editable decks remain in the dashboard history. The canonical manuscript
and all V00–V11 artifacts have not been replaced by these candidates.

Figure 1 caption draft:
SafeOT-Dual constructs graph dual prices from joint cost information and combines
their clipped/filtered values with accumulated cost feedback. The resulting shared
prices modulate one common policy-update interface. At zero graph-price cap,
fixed-penalty and adaptive Lagrangian cases are exact parameter settings. The
constraint-side LP-derived and active-set prices describe graph-price limits under
the manuscript assumptions, not a general policy-feasibility or CPO equivalence.

Figure 2 caption draft:
Rollouts provide empirical transition statistics, reward advantages and per-edge
cost information for a joint graph pricing problem with per-step budgets b_k=B_k/L,
discounted balance and a KL reference. The solver alternates Newton steps in node
potentials u with coordinate bisection in lambda. Clipped/filtered graph prices
combine with projected feedback from mean episodic costs relative to B_k. GAE
independently supplies reward and cost advantages. The actor subtracts the sum of
price-weighted cost advantages, divides by 1+sum(lambda), and applies PPO/TRPO.
The updated policy generates the next rollout. Only prices enter the actor from
the graph solve; transported flows or flow ratios are not actor inputs.

Reading limits:
- All matrices, small plots and graph states are schematic, not measured results.
- Hard-support exclusions apply to the graph; they do not certify policy safety.
- Figure1 is a conceptual overview; compound boxes omit internal ports.
- A2 retains a crossing of independent colored wires without a drawn underpass.
- B2 has an implicit clip/filter handoff and a small border hairline at price entry.
- Exact text font sizes cannot be audited from generated raster images. The PDF
  preview checks physical scale, not ICLR template or submission compliance.

Process archive:
All 12 generated images, all prompts, semantic reviews and skill provenance are
included in SafeOT_Studio_process.zip. Attempts 1 and 2 are retained process
references with known issues, not recommended final figures. The image provider
does not expose a model identifier; no GPT-image-2.5 model claim is made.

Design guidance used: SuperTeaser 3.2.21 and Figure Studio Pro 3.2.15f, for visible
mechanism internals, dominant reading paths and separate semantic/visual review.
This is an author-requested continuation, not a certification that every gated
stage of both tools has been run.

Refs: T-1635
