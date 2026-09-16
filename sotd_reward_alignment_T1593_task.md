# T-1593 - Reward objective alignment inner outer factorial

Status: review
Owner: reward-alignment
Agent: reward-alignment
Created: 2026-09-16 21:35:44
Updated: 2026-09-16 21:35:44

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Fixed2x2 inner joint reward and outer risk-feasible reward factorial, with shapedPPO retained; separate objective and metric contributions.
- Non-Goals: No CF/ridge/feature/radius/seed search; no budget/risk/officialdet/globaltrainer/oldresults/PDF changes.
- Dependencies: FrozenT1592 snapshot/timeLOO and originalT1591 12anchor bank; original source/checkpoints read-only.
- Expected Deliverables: Frozen protocol; math/raw-step/risk/SS gates;16smoke,48development,12mechanism with76 receipts; factorial/seed/channel/failure diagnostics and source-backed dashboard.
- Definition of Done: Allbounded jobs audited;12SS exact25cycle/312eval replays; scientific gate/HOLD or promising documented; review then immutable publication/feed/hash verification.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/reward_objective_alignment/v1`, `experiments/safeot_dual/progress_feed.json` (publication-stage incremental entry only; preserve owner/all existing entries).
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Protocol/source freeze and numerical/SS/raw reward gates.
- [x] Stage 2: Detached16smoke→48development→12mechanism, allnegative results retained.
- [x] Stage 3: Factorial effects, safety-failure attribution bounds, synthesis and durable publication.

## Stage Log
- 2026-09-16 22:07:46 T1593 closed scientificHOLD; immutable0990b7a and durablefeed0a9735c published. HTTP200 reportSHA02b5b915... matches local; first14 T1593, all37 priorentries/owner retained, T1591/T1592 retained. Producer dashboard_push.py:651 reads persistent source. No follow-on experiments.
- 2026-09-16 22:02:43 All76jobs exit0;12SS exactfullreplay;864528 actualsteps. HOLD_OBJECTIVE_RECIPE:24outer pairs identical; rawinner improves bankdetreward but worsens rawoptimism in12/12seed summaries, and nofixedconfig passesbothenvs.16finalunsafe jobs have checkpoint-matched4screen missed events. Publication scope narrowly expanded to durablefeed.
- 2026-09-16 21:47:51 T1593 gates and16smoke PASS; controller4151444 running fixed48development then12mechanism, final watcher detached. Raw/shaped gate144steps separately charged; 42/14/23 prior signs and new383 seed block verified. No PPO shaping/risk changes.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 diagnostic_runs/reward_objective_alignment/v1/gate.py` (already PASS; do not rerun paid gate)
  - `python3 diagnostic_runs/reward_objective_alignment/v1/verify.py smoke` (controller completed PASS)
  - `python3 diagnostic_runs/reward_objective_alignment/v1/verify.py development` (controller automatically checks once)
  - `python3 diagnostic_runs/reward_objective_alignment/v1/verify_final.py`
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1593 fixed inner/outer reward2x2 complete:76exit0,12SS exactreplays,864528steps; HOLD_OBJECTIVE_RECIPE. Immutable evidence 0990b7a4e8ae72deaeb777df96a8843f0c975ea5 and persistent-source feed 0a9735c377f27a2a50c329b95ecd17f0bc4765f4 published after review; HTTP200/first14/report SHA match verified.
- Tests: gate.py;verify.py smoke/development;verify_final.py;outer_replay_audit.py;accounting.py;agentctl check --mode manual
- Completed-at: 2026-09-16 22:04:48

- Artifacts: diagnostic_runs/reward_objective_alignment/v1/report.md, findings.json, results.csv, factorial_seed_effects.csv, mechanism_seed_pairs.csv, mechanism_risk_seed_pairs.csv, safety_failures.json, final_verification.json, run_accounting.json, publication_receipt.json; all76 job data/checkpoints retained.
- Risks: 3 training seeds are exploratory; four-episode screens missed final events in16 jobs (outer duplicates included). No zero-risk or OT/SOTA/native/VLA claim; old HOLD records unchanged.
- Follow-ups: None automatically scheduled. Fixed recipe closed HOLD_OBJECTIVE_RECIPE; mentor decides any next scientifically distinct task.
