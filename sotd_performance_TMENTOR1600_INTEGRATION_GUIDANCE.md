# Finish the actual pathwise learner

The verified `closed_loop.py` adapter is useful and should be retained. Stop developing substitute training loops or optimizer-only smoke scripts. The old invalid 9→32→2 learner and all failed attempts remain archived. Create a versioned integration from the frozen T1593 transaction worker; implementation belongs to the executor.

## 1. Reuse the working transaction

Copy frozen T1593 `worker.py`, `core.py`, `risk.py`, actor/environment snapshot and dependencies into an isolated integration directory, with explicit absolute paths derived from `Path(__file__).resolve().parent`. Check one import before launching any matrix. Copy the already-verified adapter there and rerun the immutable mentor checker against that directory if the adapter changes or a new path is used.

Keep the same agent construction, real 240-step exploration batch, full PPO shadow, critic/optimizer state installation, three candidate slots, 144-step deterministic selection, 96-step independent acceptance, dual update and final evaluation. Add mean/tail and sample/det switches only to the middle candidate builder. KL is the sole active geometry in this factorial. Any unused W2 diagnostic solve can be removed without changing the selected candidate, but record the removal and preserve the original PPO RNG stream and actor/optimizer transaction. Do not silently add the separate common-eligibility intervention to these four arms.

## 2. Replace the middle candidate objective callback

At each update build the original full 5060-parameter actor in double precision, base parameter vector, and named functional parameter mapping. Generate and store one independent optimization batch with N=20 initial positions, twelve environment disturbances and action noises per trajectory. Use the frozen environment's exact reset/noise distributions. Reserve distinct deterministic RNG namespaces for model optimization, exploration, selection, acceptance and evaluation, and assert no seed intersections.

For each candidate parameter vector theta, call the verified adapter to **reroll the complete trajectories using theta-dependent states**. The returned quantities define:

```text
R_i(theta) = sum_t raw_rewards[i,t]
C_ik(theta) = sum_t costs[i,t,k]
objective(theta) = mean_i R_i(theta) - mean_i R_i(theta_old)
rho_k(theta) = mean_i C_ik(theta)            [M]
rho_k(theta) = max_i C_ik(theta)             [T, N20 CVaR0.95]
distance(theta) = old-state mean KL(old Gaussian || candidate Gaussian)
```

Do not detach states, cumulative budgets, actor outputs or objectives. Pure log-std columns may have zero deterministic objective derivatives; that is correct. The model batch is fixed for every query of the same local solve and refreshed next cycle, independently of final evaluation.

## 3. Separate direction construction from constraint rows

Build exactly K+1 original-style Fisher-preconditioned directions from `grad(objective)` and `grad(rho_k)` at theta_old, with the existing damped CG settings. Fix the tie-gradient convention for `max`. A zero direction is recorded as zero rather than replaced by an unrelated gradient.

For SLSQP, optimize coordinates z with theta=base+D@z. Mean arms impose K inequalities `mean_i C_ik(theta) <= B_k`. Tail arms impose **20×K inequalities** `C_ik(theta) <= B_k`; tile budgets in the same flattened order. The KL inequality and normalized slack recovery remain. The constraint Jacobian has all corresponding rows; the direction basis remains K+1. Do not accidentally use 20×K independent basis directions, a scalar maximum across channels, or a fixed penalty coefficient.

Cache values/Jacobians only for the same actual parameter vector and frozen model batch. Count unique forward model queries, reverse computations and actual model transitions. Reserve a query for float32 installation verification within the existing cap of 200 per cycle. Recheck the actual installed float32 actor against every declared model constraint and KL. Query exhaustion/failure returns an explicit no-op/failed-candidate record, not a fabricated successful solve. A restoration result with positive slack is marked restoration, never hard-feasible.

## 4. Validate the actual worker

Use eight one-cycle worker jobs: K2/K3 × SM/ST/DM/DT × seed180. Each is **480 actual training interactions**, not merely any arbitrary set of 40 episodes. Verify the 240/144/96 phase ledger, original proposal/checkpoint/momenta semantics, paired noise tapes and arm mapping, complete model-query accounting, finite values, original raw rewards/budgets, actual checkpoint reload equality and installed-candidate identity. One valid fixture must exercise a nonzero accepted installation and one rejected rollback; an algorithmic rejection in a particular arm is a recorded outcome, not a reason to swap its seed or fake an update.

Run the existing 24-job development matrix only after these gates pass. Gate decisions measure implementation integrity, not desirable rewards. Archive auxiliary optimizer-only smoke results under their true names. Correct the unsupported `checkpoint_reload=true` claim in an erratum rather than overwriting the original result.

The parallel common-KL eligibility test is independent and inexpensive; it can use idle capacity once its own control-replay/import/smoke checks pass. It must not delay completion of this real learner by spawning another substitute smoke implementation.
