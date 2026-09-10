# T-322: E4 first completed attempts

Publishes two independent completed attempts: strict RGB single-object seed 9401 and full-input two-object seed 9401. Both failed; the strict RGB record retains its TLS-interrupted final request, while the long record preserves a previously completed brown-bottle subtask without relabelling the failed whole chain as success.

- Complete measured wall-clock: 308.223763 s and 517.124159 s. Long policy-collection segment: 444.621860 s.
- Parsed-return interval: 78.116522 s and 58.527968 s, derived from the first and last valid-return timestamps. This differs from requests divided by a collection window.
- Executed action chunks: 0 and 7, including the partially executed safety-aborted final chunk. Throughput uses the entire measured wall-clock denominator.
- Known Standard API equivalents: $0.45930 plus one unknown-usage request; $0.83042 with no unknown usage. Budget reservations are not billed cost.
- Four-camera frame synchronization verified: 17 and 394 frames per camera. The long recording covers simulation clocks 1.100–27.375, a 26.275-second span; it is not a 27.375-second span.
- Training-format export and training dataset acceptance remain pending. Control-state and video recordings are distinct from policy decision observations.
- The public strict evaluation omits verbose provider attribution and internal request directories; the compact episode manifest records both original-source and published-file SHA-256 values.
- Runtime status is a dated 2026-09-10 23:09 snapshot; future queued work has no fabricated results.

## Verification

E4 equations and source hashes passed. All 64 existing anchor IDs and 26 video/source elements preserved. E3 64-row/312-request/$27.866166 accounting is unchanged. Chromium 1440/390/320 px passed: no horizontal overflow, two E4 rows, existing E3 costs, native disclosure keyboard action, and actual long-video playback. Workflow T-322 holds publication evidence.
