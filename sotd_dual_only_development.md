# Dual-only transfer: completed gated development

## Previous version closed
Thirty finite-mixture confirmation jobs completed. Joint K2 old/finite/PPOLag=.690/.582/.812; K3=.862/.148/.882. No more finite path-importance expansion. The prototype changed graph/LP/entropy/reward aggregation/weights and may reselect initial/noise paths; this is not a falsification of original SafeOT theory.

## Gradient gate and units
Actual PPOLagrangian _update gradient agrees with independent clipped reward-PPO at applied lambda0 (max8.94e-8), and manual applied lambda[.7,1.3] (max3.58e-7). Same proposals/logprob/returns, terminal cost GAE[1,2] retained. No importance weights, SafeFlow scaffold or capacity penalties in dual-only. Dynamic LP dual is nonnegative shaped episode reward per raw cost. Apply lambda/std(raw reward GAE) because buffer normalizes reward but not cost GAE; raw, applied and divisor logged. It remains a discounted GAE policy surrogate, not a proven undiscounted dual gradient. Infeasible LP keeps explicitly stale previous raw lambda (initial.001), with failure status; never asserts fallback safety.

## Development results (seed1,2400 steps,100raw episodes each)
K2 dual-only:joint1,reward8.05503,cost[4.26944,3.92320],violations[0,0]. PPOLag:joint1,reward8.20214,cost[3.97082,5.20195]. Finite:joint0,reward9.43010,cost[7.84654,5.15822].
K3 dual-only:joint1,reward8.17461,cost[4.94137,3.96820,7.90610],violations[0,0,0]. PPOLag:joint1,reward8.14010,cost[4.89324,3.95667,7.84424]. Finite:joint.12,reward9.50091,cost[7.15016,6.27425,12.36972].
All6 exit0; exact step/optimizer/checkpoint/source checks in acceptance.json. First2 jobs ran concurrently, then at most4 one-thread CPU workers. No impact on external queues. Result improves finite joint but loses its unsafe reward; no strict joint+reward improvement over PPOLag. Precommitted promotion criterion FAIL, seeds170-174 not launched. Small K3 reward difference at tied joint is not statistical superiority.

## Selection-bias diagnostic
Historical flow_epochs has weights but not corresponding training states/actions/noise. Cannot recover initial-state/noise/terminal-cost correlations or empirical feasible fraction from those marginal logs. No substitute eval-to-training correlation was fabricated.
Fresh100-path fixed-action diagnostics saved all paths. Identical actions, fixed initial state, different exogenous noise: feasible fraction1, mean shaped episode reward8.145409, LP-selected8.337542. Weight/noise-sum correlations x=.24584,y=.13906. Initial-state-varying case saved separately, correlations/terminal costs in bias.json. This is retrospective selection optimism, not action-policy improvement; environment dynamics used only for this diagnostic. LP selected distribution is not guaranteed realizable.

## Routing and time
Stop expansion: dual-only has not cleared strict development joint+reward gate. Next reported hypothesis is dual signal availability/normalization stability using existing logged raw/applied lambda and reward-GAE scale; no new parameter sweep authorized or started. Receipt time is union across concurrent successful processes, worker-hours separately. Prior contiguous night remains7.583698h; prior separate prototype adds.180203h; current final_summary adds only successful development worker union. Still no claim of8h continuous effective execution.

No independent review/power/SOTA claim. Snapshot hashes predate jobs; prototype instrumentation hash audit, if subsequently added, is retrospective. PDF unchanged.
