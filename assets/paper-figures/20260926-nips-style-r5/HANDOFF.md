# NIPSStyle R5 handoff

Figure 2 is a layout-only continuation of the NIPSStyle R4 editable baseline. The fifth column now separates the graph price, observed-cost feedback, normalized priced advantage, and PPO/TRPO update into non-overlapping cards. Column 4 shows only the observed-to-target flow, the projection caption, and the safety-price output; solver-kernel internals and stale capacity-composition equations were removed.

The displayed equations are the method-level equations: `F-hat -> F-star`, soft/hard constraints, `lambda_k = bar-lambda_k-star + beta_k`, the beta residual update, and the normalized priced advantage. Detailed solver derivation remains in the paper. Figure 1 is unchanged from NIPSStyle R4. The PPTX remains editable; PDF/SVG are vector exports.
