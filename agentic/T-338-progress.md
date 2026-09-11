# T-338 - 发布各输入条件成功率及逐条对应视频

Status: done
Owner: codex-astra-input-panel
Agent: codex-astra-input-panel
Created: 2026-09-11 14:04:49
Updated: 2026-09-11 14:04:49

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Publish input-condition success counts and directly accessible raw videos.
- Non-Goals: No GPU/API experiments or unrelated dashboard edits.
- Dependencies: Terminal phase2 and E4 evaluations plus independent artifact verification.
- Expected Deliverables: Two interface-specific comparison tables, eight visible video cards, source provenance.
- Definition of Done: Source hashes, desktop/mobile playback pass; independent review and live Pages publication.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_input_panel_20260911/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Verify terminal result sources and copy original videos.
- [x] Stage 2: Implement comparisons and preserve historical evidence.
- [x] Stage 3: Validate 1440/390/320 layouts and all eight videos; prepare reviewed publication.

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Prepared two input-success comparison tables and eight visible raw videos, preserving prior failure evidence and separating WORLD and wrist-relative interfaces.
- Tests: BROWSER_CHECK.json: 1440/390/320 layouts and eight video playback PASS; SOURCE_CHECK.json: five original SHA256 matches PASS; ffmpeg decode PASS; git diff --check PASS
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-11 14:49:46
- Completed-at-ns: 1789109386496291359
