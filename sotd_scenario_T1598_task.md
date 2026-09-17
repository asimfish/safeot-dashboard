# T-1598 - Scenario generalization audit and gated N100 DT comparison

Status: review
Owner: scenario-generalization
Agent: scenario-generalization
Created: 2026-09-17 22:24:58
Updated: 2026-09-17 22:24:58

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Audit ST/DT installations and fresh-scene generalization; conditionally compare N100 DT.
- Non-Goals: No old model edits, no margin/radius/PPO mask search, no restart of old window.
- Dependencies: Frozen T1595 integration adapter/worker/checkpoints.
- Expected Deliverables: Seedwise audit, 24-object scenario bank, gated replay/smoke/six-run receipts.
- Definition of Done: Diagnostic and conditional experiment evidence with actual counters, report and publication status.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/scenario_generalization/v1`
- Additional publication scope: `experiments/safeot_dual/progress_feed.json` incremental entry and `diagnostic_runs/scenario_generalization/v1/publish` isolated dashboard worktree; preserve all owners/entries.
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [ ] Stage 1:
- [ ] Stage 2:
- [ ] Stage 3:

## Stage Log
- 2026-09-17 23:05:37 T1598 six N100 jobs exit0; both task means improve reward and any-event vsN20 but5/6 policies eventful: HOLD. Added zero-step exact final-actor installation attribution with scenario max gaps and eval excess; preparing persistent dashboard publication before separate margin task.
- 2026-09-17 22:31:34 Mentor collision supplement audited: runtime already corrected before first N100 launch to env*1e7+seed*1e4+cycle*100; sourcefreeze match,12000 extras unique,15 runpair intersections0, no original/diagnostic overlap,15 saved tapes exact. No running source changed or restart. Both N20 two-cycle exact replays and N100 smokes exit0; development4 live PIDs182712/182717/182715/182718,2 queued; controller173936.
- 2026-09-17 22:29:56 Live verified PID173936 controller/PID173937 N100 K2 smoke; original full240step exploration batch, PPO proposal and100scene tape exist, worker CPU~97%, RSS~653MB. Nine accepted strict-original-safe candidates have fresh anyevent .00390625–.19140625. Added per-channel scenario CSV and output hashes. Six development jobs not yet launched; detached controller gates them automatically. Dashboard update pending, no published claim.
- 2026-09-17 22:28:59 T1598 diagnostic complete: all12 ST/DT final actors exact last effective update; ST pathwise installs1 vs DT44. 24 frozen objects: 73728 fresh+5760 replay model transitions, zero real steps; 9 accepted DT middles strict original20-safe/fresh256-eventful. N100 admitted; frozen controller starts single480step N100 smoke then exact N20 replay, secondsmoke and gated six development. No old watcher restarted.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Completed T1598 scenario diagnosis and six verified N100 jobs; both task mean reward/risk improve but5/6 policies eventful, HOLD. Exact final-actor attribution and source-backed export prepared; remote publication pending network fetch.
- Tests: preflight.py; training_gate.json PASS; all6 receipt exit0; collector transaction assertions; final_attribution.py; seed_namespace_audit.json PASS; agentctl check --mode manual
- Completed-at: 2026-09-17 23:06:13
