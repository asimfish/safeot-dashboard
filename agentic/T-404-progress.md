# T-404 - 发布PsiBot三组恢复结果与原始证据

Status: done
Owner: codex-psibot-recovery-panel
Agent: codex-psibot-recovery-panel
Created: 2026-09-13 16:46:25
Updated: 2026-09-13 16:46:25

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: 发布PsiBot恢复三条件真实终态与逐轮四图，保留旧中断独立。
- Non-Goals: 不混分母、不重跑模型、不把相对接口准备写成执行。
- Dependencies: T378闭集readout与rgb_relative恢复导出。
- Expected Deliverables: 三条件矩阵/播放器/成本wall/四图联动、可核源记录。
- Definition of Done: 数字/拒绝原因/原片哈希一致，默认无媒体请求，移动端核验，root gate发布。

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_psibot_results_panel_20260913/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: 三条件readout/拒绝计数/原片逐源核验。
- [x] Stage 2: 47轮导出联动、三宽度/零首载/播放切换验收。
- [ ] Stage 3: root gate后发布。

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: 发布PsiBot恢复三组各0/1、47轮四图与三条成本wall/原片，旧中断独立
- Tests: CONTENT_CHECK/MEDIA_CHECK/EVIDENCE_COPY_CHECK/BROWSER_CHECK全部通过；node --check
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-13 16:51:09
- Completed-at-ns: 1789289469003285202
