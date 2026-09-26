# NIPSStyle 3Stage R1 handoff

This is an independent Figure 2 candidate following the Opus review. The old five equal-height columns are replaced by three Algorithm-1 stages: (1) build the constrained rollout graph, (2) project the observed flow and derive safety prices, and (3) update the actor on the priced advantage. The target flow is boxed as “target only · never executed”; the only thick cross-stage arrow is the orange price route. The dashed orange bottom rail carries observed-cost feedback, and the thin gray rail carries the next rollout.

The five displayed equations are attached to the visual objects that they explain: budget constraint, entropic projection objective, price fusion, normalized priced advantage, and beta feedback. Kernel/Sinkhorn/capacity internals are omitted. This branch does not modify Figure 1 or the manuscript.
