# T-320: actual decision example and episode accounting

- Source: E3 FR3 seed 9301 xhigh decision 00. Published original four RGB PNGs, public state, prompt, execute_motion schema and model candidate. Image/prompt hashes match the original request manifest; `io_9301_d00_provenance.json` preserves these checks.
- `e3_episode_costs_20260910.json` joins the 64 E3 evaluation records to previously audited token usage. 312 requests, 300 parsed candidate returns, 312 decision-observation sets, 12 unknown-usage requests, $27.866166 known API Standard equivalent at 2026-09-10 prices. No actual billing claim.
- Every episode wall-clock duration is null because complete start/end timestamps were not recorded. Output intervals are reconstructed between candidate return events from request start plus measured latency. Video frame rate and physics control rate are separate from decision-observation sampling.
- Success amortization divides all known same-condition attempt costs by independently evaluated successes; PsiBot includes invalid infrastructure costs separately from its valid success-rate denominator.
- E4 task cards are a dated status snapshot. T-318/T-319 are independent deployments waiting for their execution gates; no unobserved model result is claimed.

## Verification

- Static integrity: all 55 previous anchor IDs and 26 video/source references preserved; all new local links exist; raw source SHA-256 checks pass; numerical sums and example displacements verified.
- Chromium at 1440, 390 and 320 px: no horizontal overflow, four full-resolution inputs loaded, native details keyboard operation passed, filtering yields 64 total / 30 successful / 30 valid failed / 4 infrastructure-invalid records, custom price/reset/invalid-input behavior passed, no runtime exceptions.
- JavaScript syntax and git diff whitespace checks passed.
- Workflow task T-320 records evidence and publication follow-up. GPU experiment results and training-format export are outside this dashboard phase.
