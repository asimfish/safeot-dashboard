# E-normalization findings (T1577)

## Active path and units

Instantiated SafeFlowV2 runner: SAGraphBuilder.capacity_alloc=global_cost, composition_tau=None; GammaFlowSinkhorn hard solver, cost_projection_interval=10. Graph C is arithmetic mean measured transition cost per edge; Fhat is transition counts/T (mass1), not discounted episode flow. mu0 is normalized episode-start count plus1% uniform smoothing. Fstar total mass1.00000024. Solver uses discounted balance outflow-gamma*inflow=(1-gamma)*mu0, gamma=.99. Terminal done marks starts for mu0; the graph does not provide finite-horizon terminal sink subtraction or explicit absorbing terminal self-loop. Edges are PCA/binned state-action pairs, can merge time/budget and virtual edges. RHS passed is original episode thresholds[6,6]. No cost_fn placeholder substitution here.

The active solver called global cost projection5 times; all changes0 on the observed graph, despite mean episode costs[9.585259,11.290753]. Graph functional[.798772,.940896] is per-step average. Direct excessive-cost fixture triggers projection12->6, so operator is enabled, not dead code. Fhat balance L1=.165019 against actual solver RHS. This is a measured empirical residual for this constructed dataset, not actor realizability residual for trained policies.

## Identities and counterexamples

For fixed H, Z=sum(t=0..H-1) gamma^t; f_t=gamma^t/Z. Use C_t=Z gamma^-t c_t: sum f_t C_t=sum c_t. Finite balance requires e0/Z - gamma^H eH/Z; using (1-gamma)e0 alone omits terminal flux. Here Z=11.3615128284 and max error of correct identity/balance<1.4e-17.

For infinite absorbing occupancy, transient f_t=(1-gamma)gamma^t, terminal self-loop mass gamma^H, terminal cost0. Transient coefficient c_t/[(1-gamma)gamma^t] restores undiscounted episode cost. This is a different occupancy normalization and requires actual absorbing support; it is not the current empirical Fhat.

Constant c=1: true12 versus normalized1. Terminal unit cost: naive H*normalized=.9456539 versus true1. First-step unit cost:1.0561974 versus true1. Thus blindly b/H is timing biased. Variable horizons2/12 with costs1/2: correct equally weighted episode mean13 versus pooled transition mean1.85714; per-episode Z or equivalent weighted construction is needed.

Time-indexed reference LP with early/late unit-cost paths: exact costs permit high-reward path probability1, reward2; b/H distorts allocation to .491626/.508374 and reward1.491626 despite identical true path costs1. Balance residual<7e-18. Reference only; it does not test neural actor training or existing Sinkhorn consistency.

## Gate and route

Supported: active legacy cost/RHS units are incompatible with intended undiscounted episode cost in these diagnostics. Uncertain: this causes observed policy failures or correcting it improves learning. Legacy cost+balance gate FAIL. Time-indexed reference algebra/LP PASS, not the full actor-compatible solver gate. A/B training NOT STARTED. Route DEEPEN: design time-indexed transition support with explicit terminal convention and matched discounted sampling, then verify solver balances; changing only RHS cannot restore missing time information. Must separate that architecture change from unit-only causal attribution.

No independent review, statistical power, superiority, native/VLA or full SuperResearch gate passed. Attempt1 missing next_actions keyword retained as engineering failure; attempt2 exit0. No repeated training or budget/target changes.
