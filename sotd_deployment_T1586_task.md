# T-1586 - Frozen deployment kernel audit

Status: review
Owner: deployaudit
Agent: deployaudit
Created: 2026-09-16 04:06:10
Updated: 2026-09-16 04:06:10

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Audit same frozen policy under exact deterministic versus sampled deployment kernels.
- Non-Goals: Retraining,mode cherry-picking,officialdetchanges,oldresults/PDF/DERIVATION edits.
- Dependencies:24joint_transport_auditfinalactors/exactoldepisodeseeds andsnapshot evaluator.
- Expected Deliverables:24old100reproductions,14976pairednewepisodes,fullmode/perpolicyuncertainty,algebra/kernelcontract,dashboardexport.
- Definition of Done: Allfrozenhashes/oldmetrics/RNGpairing/unchangedparameters verified;all24modecomparisons andboundariesreported.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/deployment_policy_audit/v1`
- Files likely to touch: Independentv1snapshot/protocol/policyhashes/seeds/controller/evaltraces/analysis/export.
- Files explicitly out of scope: Source24checkpoints,oldresults,officialevalcode,PDF/DERIVATION.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Frozenpolicy/sampletransformaudit;24old100detreproductionsPASSwithin1e-6.
- [x] Stage 2:24pairedjobs312seedsx2modes=14976episodes,all48phasejobs exit0.
- [x] Stage 3: Fullrisk/pairedCIanalysis,algebra/kernelcontract anddashboardexport;0trainingsteps/hours.

## Stage Log
- 2026-09-16 04:12:28 48phasejobs exit0:24old100det reproduced+14976newpairedmodeepisodes. SpecialK3samplexcost6.9876CIcrosses7;anyviolation.532. Samplejoint improves1/drops17/ties6,rawrewardlower24/24. No training,0traininghours;modegapverified,lastupdate/noisestillunresolved.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Frozen24policy deploymentmode audit complete,14976newpairedepisodes andconditionalkernelcontract;officialdetunchanged
- Tests: analyze.py;24reproductions1e-6;14976RNG/parameter/hashtracechecks;48exit0;sampleequivalence;algebra;manualworkflowcheck
- Completed-at: 2026-09-16 04:12:28
