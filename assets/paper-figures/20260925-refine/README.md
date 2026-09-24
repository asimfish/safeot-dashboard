# V14 — Viewpoint and small-type refinement of accepted V13

Figure1 now distinguishes two roles of the same price construction:
- Penalty view: prices weight costs in the policy objective. With zero graph-price
  cap, fixed prices and adaptive Lagrangian feedback are exact parameter settings.
- Constraint view: budgets bound costs on the graph surrogate. LP-derived and
  active-set prices are conditional graph-price limits under the paper assumptions.
The shared graph-price construction, cost feedback and one policy update remain
central. These are two interpretations, not two unrelated executable algorithms.

The left panel is pale slate blue, the right panel warm ivory, and the central
method teal. Headings keep their previous scale. Shorter labels make room for
clearer small type. The feedback card and GAE inset received a final local edit.

Figure2 preserves graph/policy bands and clarifies clip-to-filter handoff, the
weighted cost sum, mean episode cost minus budget, and accumulator output. Dense
cost-cell time subscripts are removed; remaining cells are schematic.

## Caption drafts

Figure1. One price rule, two views. Joint graph costs and budgets produce dual
prices, which are clipped and filtered, then combined with accumulated episodic
cost feedback. The same prices modulate a common GAE-based policy update. The
penalty side shows exact zero-graph-price-cap settings; the constraint side shows
graph-price limits under the manuscript assumptions. Lowercase b denotes graph
per-step budgets, not episodic budgets B. The rectangular region depicts budget
inequalities, not the complete attainable cost set or a policy-safety guarantee.

Figure2. The on-policy SafeOT-Dual framework. Rollouts provide empirical graph
statistics, GAE advantages and mean episodic costs. Graph pricing uses per-step
budgets b_k=B_k/L, discounted balance and a KL reference. Newton steps in node
potentials alternate with coordinate bisection in multipliers. Only conditioned
prices cross to the actor, combining with projected feedback on J-bar_k-B_k.
GAE independently supplies reward and cost advantages. The policy update subtracts
the sum of weighted cost advantages, normalizes by 1+sum(lambda), and applies
PPO/TRPO. The resulting policy generates the next rollout. Graph feasibility does
not imply final-policy feasibility; a separate off-policy executor is not shown.

## Files and scope

Figure1.png and Figure2.png are original generated images without pixel edits.
Figures_raster_preview.pdf embeds them at 5.5 inches wide. V13_V14_same_width.pdf
places accepted V13 and refined V14 at the same physical width for each figure.
Print at 100% to assess size; these are raster previews, not vector PDFs.
Exact font sizes and embedding cannot be certified from raster text. Secondary
axes, subscripts and the edge legend still require inspection at print scale.

All five generation attempts, prompts, reviews and skill provenance are preserved
in V14_process.zip. Figure2 attempts 1 and 2 retain known feedback-port problems
and are process references only. No model identifier is exposed by the built-in
image provider. No native editable PPT is claimed. The canonical paper is unchanged.
All V00–V13 files and version records are preserved in the dashboard.

Refs: T-1640
