# T-359 - 重整输入信息矩阵与紧凑证据浏览

Status: done
Owner: codex-astra-input-matrix
Agent: codex-astra-input-matrix
Created: 2026-09-12 19:37:37
Updated: 2026-09-12 19:37:37

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: 用中文总输入表及独立协议矩阵解释每个条件提供什么；默认页面简洁。
- Non-Goals: 不变更实验或结果，不删证据，不混协议分母。
- Dependencies: root INPUT_INFORMATION_DISPLAY_FACTS.json。
- Expected Deliverables: 简洁总览、FR3/PsiBot矩阵、默认折叠结果与逐轮查看器、响应式截图。
- Definition of Done: 输入事实核对、默认零媒体/证据加载、移动端清晰、旧链接保留，root review后发布。

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_input_matrix_ui_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: 输入矩阵与默认折叠信息架构。
- [x] Stage 2: 320/390/1440截图与四查看器/旧链接/媒体按需验收。
- [ ] Stage 3: root gate后发布与线上核验。

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: 完成总输入定义/FR3和PsiBot独立矩阵、四个默认折叠证据入口及响应式简洁首页
- Tests: CONTENT_CHECK权威事实/原链接；BROWSER_CHECK四viewer及零首载；AFTER_DOM三宽度；node --check
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-12 19:46:11
- Completed-at-ns: 1789213571194865656
