# T-354 - 排查视频播放卡顿并补齐PsiBot历史录像选择器

Status: done
Owner: codex-astra-video-performance
Agent: codex-astra-video-performance
Created: 2026-09-12 16:38:59
Updated: 2026-09-12 16:38:59

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Diagnose playback stalls, eliminate eager hidden video loading, preserve original evidence and expose all10 valid PsiBot historical episodes.
- Non-Goals: No experiment reruns, interpolation/speed changes or score changes.
- Dependencies: Original MP4 assets, remote PsiBot evaluations/media and reviewed allowlist.
- Expected Deliverables: Click-to-load single-active video manager, labelled compressed previews, ten-episode history selector, benchmark/seek/source checks.
- Definition of Done: Same-throttle before/after evidence, startup0 MP4 requests, play/seek and source/privacy checks, parent review/gate and live publication.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_video_performance_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Reproduce contention and inspect codec/boxes/online Range support.
- [x] Stage 2: Implement deferred loading and preview/history support.
- [x] Stage 3: Verify throttled startup/playback, mobile seek, 10 histories and original hashes.

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Diagnosed eager hidden video contention; implemented versioned click-to-load single-active playback, labelled unchanged-time previews, all10 PsiBot historical original videos and allowlisted evaluation excerpts.
- Tests: Same1.6Mbps100ms baseline29requests20videos/no play15s vs fixed0/0.45s; mobile320390 all10 history and600kbps seek PASS;25 preview frames/fps/duration exact PASS;10 remote source hashes PASS;public allowlist/static links PASS;git diff --check PASS
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-12 16:58:57
- Completed-at-ns: 1789203537233137717
