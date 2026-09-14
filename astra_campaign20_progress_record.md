# T-330 panel progress record — 2026-09-15

## Delivered change

Seven historical FR3 input conditions are visible together near the top, with 28 actual input images and 14 inline videos. Each video carries an episode-matched poster and explicit success/failure/interruption label. Video URLs use the existing lazy loader contract so switching clips preserves the source and releases the previous download.

Rows include success count / valid attempts, known standard-equivalent cost per success (including failure/interruption spending), input/output token counts, wall collection time per attempt, and attempt count. Historical totals are 14 attempts / 13 valid; these are separate from the new 280-episode campaign. No small-sample improvement claim is made.

## Runtime snapshot

FR3 and PsiBot mainskill zero-model physics/input/recording checks passed after offline recovery of missing ffprobe. Original exceptions remain preserved. FR3 three scripted commands had <0.1 mm position error; all four recordings have 107 frames at 15 fps. PsiBot checks native 36-joint recordings, 120 Hz control, reset pairing and relative EEF execution; actual images were reviewed. Initial wrist view does not show the bottle. Formal collection supervisors are running, but no new valid model episode is claimed in this snapshot. SSH to 30109 is restored; no FR3/PsiBot collector has been deployed there yet.

## Validation

- Browser: 7 rows, 28 actual images, 14 inline videos; no startup MP4 request; desktop and mobile have no document overflow; visible input images load; no JavaScript exception.
- Two different inline videos loaded and advanced playback at 640×480; starting the second released the first. Local preview check does not measure every viewer's public network speed.
- Metrics recomputed from the existing public strict_9403 and strict_9404 evaluation JSON files. Mean duration divides by attempts, cost by successes; unknown use is marked as a lower bound.
- git diff --check passes. No model credentials or remote identity contents are included.

## Remaining work

Complete fair FR3/PsiBot 20×7 collection; publish verified new episodes as available. At least four-subtask long-horizon collection remains pending. Arm q/dq remain bundled in these seven conditions; splitting them is a later experiment.

## 2026-09-15 bounded overload recovery

Both collectors previously stopped after explicit `server_is_overloaded` events. FR3's latest interrupted epoch completed two model decisions before its third request failed. PsiBot's latest epoch failed on the first request. The earlier ~75-second `ChunkedEncodingError` does not establish a 60-second read-idle timeout as its cause. The actual PsiBot entry imports `api_client.py`; the previous timeout patch targeted an unused client file. This release corrects that entry and the FR3 supervisor's seven-episode-only loop.

Only explicit overload before any output can now retry, with identical serialized input and paused physics. Limits are two extra POSTs per decision (30/60-second waits), forty per platform campaign, also counted against the existing global request cap. Partial output, broken stream, authentication and quota errors do not retry. Unknown overload usage remains separate and makes cost a lower bound. Earlier epochs were archived intact. Physics, observations, schemas, controller and evaluation source hashes remain unchanged; original gate receipts were retained with an explicit transport-only compatibility receipt.

- 12 injected-event tests pass; they include the actual old/new client paths, identical retry payloads, retry exhaustion, cutoff/cancellation, and non-retryable errors. No live model requests were used for these checks.
- Both durable supervisors started on mainskill. Their initial runtime check remains pending; test success alone is not evidence that provider overload is resolved.
- Cumulative accounting now includes archived interrupted epochs, deduplicated by request start time, seed, condition and decision. The public JSON records known tokens/cost, unknown usage and partial executed decisions; those are not complete episodes or a success rate.
- Full 140-episode FR3 queue is connected. Both platforms retain the current $12 known-cost soft stop. Finishing all 280 episodes and the subsequent four-subtask tasks remains outstanding.

Frozen source manifests: FR3 `2a00f7a960aba7c874dd407160ae84d895c8f96f46e3ce690f0d68b337baecc2`; PsiBot `d0cb4ae4d2ea5fe5fa6c7cc742066501d60c6d8dd8963a28c51f9b50170892d9`.

## First verified campaign episode — 2026-09-15

FR3 seed 10000, rich inputs, is a verified valid failure: success 0/1 in this condition, campaign progress 1/140. Both model requests completed normally (32.22 / 47.70 seconds); there was no overload retry. At simulation time 5.25 seconds the right finger / bottle PhysX contact separation reached −0.00234794 m, exceeding the frozen 0.002 m penetration tolerance. The bottle was not lifted or placed/released. The recorder has 79 frames per camera at 15 fps and passes all closed-artifact checks. This establishes the stop trigger, not a general cause or comparison between input conditions.

The episode consumed 9037 input / 2349 output tokens, $0.20782 known standard-equivalent cost, and 688.85 wall seconds including initialization. Three motion segments were emitted across two model requests; the final requested descent was interrupted after 1.25 seconds. Cost per success is undefined with zero successes. Four original input images and four web videos are displayed together; total video size was reduced from 3,792,032 to 507,594 bytes, preserving 640×480, 79 frames and 15 fps. Public result and media receipts accompany the assets. The runtime summary now counts verified valid episode receipts, not raw supervisor termination totals.

FR3 continued automatically into minus_S for the same seed. PsiBot has completed two real model calls (about 98 and 90 seconds) and remains in its first episode. It has no verified complete sample at this snapshot. Browser checks now include all four new clips and two historical clips; all play and release the prior resource. The two 20×7 campaigns remain incomplete; long-horizon collection remains next.

## PsiBot first valid success and comparable timing — 2026-09-15

PsiBot rich seed 10000 passed physical success and all recording checks: stable lift of 6.6348 cm, last-second minimum lift 6.6345 cm, last-window speed below 0.000174 m/s, last-window tilt below 0.565 degrees, no geometric hard abort. Eleven normal model calls completed with no overload retries; the eighth-call prefix had not achieved the lift threshold. This is a within-trajectory observation about additional decisions, not an independently randomized budget comparison. Rich is now 1/1 valid success; 19 paired seeds remain in that condition. FR3's place-and-release task differs from PsiBot's grasp-and-lift task and is not pooled.

The episode used 83416 input / 32403 output tokens and $2.45431 known standard-equivalent cost. Including earlier interrupted rich attempts, observed unit-success cost is at least $2.69546, with five unknown-usage requests. Four original input posters and four web videos are exposed inline; all 568 frames, 15 fps and 640×480 are retained. The original 18.34 MB video total is compressed to 2.068 MB; no task evidence is generated or replaced.

A timestamp audit found an accounting difference: FR3's raw clock includes process startup; PsiBot's starts inside the episode after the persistent simulator is initialized. The report now additionally shows first-observation-to-evaluation completion: FR3 169.054 s plus 519.795 s before first observation; PsiBot 1782.612 s plus 10.454 s before first observation, excluding its one-time process startup. Raw totals remain visible. PsiBot's median output interval is 172.484 s over ten intervals. This profile used existing request timestamps, not additional paid calls or a performance intervention.

The report explicitly names the fixed six-dimensional hand semantics, limits, wrist-frame directions and mimic couplings shared by all seven PsiBot conditions. Textual self-memory, categorical execution status and remaining-request counts also remain shared; history ablation removes previous image/action records. No policy, control, physics, seed or evaluation source was changed. Both supervisors continue into minus_S.

Validation: all eight current clips and two historical clips play through the lazy loader; original image SHA checks and MP4 faststart checks; desktop/mobile no page overflow; exact native recording receipts; git diff --check; agentctl manual check. The full two 20×7 campaigns and four-subtask follow-up remain incomplete.


## FR3 same-seed success without S — 2026-09-15

FR3 seed 10000 minus_S is a verified valid success (1/1): it lifted 6.18 cm, placed within 2.68 cm of target, released and remained stable for one second. All recording checks passed. It used 15 requests, 100515 input / 28641 output tokens, $2.43720, no unknown use. This group's current unit-success cost is $2.43720. Raw collection was 2187.145 s; first-observation-to-terminal 1661.720 s, preparation 525.424 s. Median output interval was 95.905 s over fourteen intervals.

The paired rich episode failed on request two; both conditions retain the same 30-request cap. The minus_S tenth-request prefix had lifted but not placed/released, and completion required fifteen requests. This supports feasibility without S for one initial state, not superiority from removing S. Exact initial physics, J, K and camera order match. First RGB images have small measured differences: mean absolute channel error 0.041–0.057 on a 0–255 scale; the source of rendering differences is unconfirmed. The public paired receipt preserves this limitation. Common textual memory and other shared inputs remain.

Four new FR3 inline clips retain 662 frames, 15 fps and 640×480, compressed from 28.51 MB to 3.277 MB. The existing rich failure is adjacent. PsiBot videos total 2.068 MB. There are now 2/140 completed FR3 attempts and 1/140 PsiBot attempts; both collectors continue. Timing profiling identified initialization accounting differences; no runtime speedup is claimed. No collector source, policy or physics changed in this reporting update.


## SSH interruption, bounded resume, and third FR3 condition — 2026-09-15 05:04 CST

The first PsiBot rich success remains verified. In minus_S, the proxy-carrying SSH connection exited at 04:44:39 CST; the in-flight model request later failed with a read timeout. The initial SSH outage cause remains unproven; this is a transport mitigation, not evidence that upstream errors are solved. The original three executed minus_S decisions and fourth unknown-usage request were archived intact. They do not count as a completed robot failure.

An independent loopback-only SSH reverse tunnel now has systemd reconnection. It retains pinned host verification and the same existing local proxy; model identity is still passed in memory to the collector. No model POST is automatically replayed by tunnel reconnection. The full queue resumes from the missing seed/condition and validates immutable completion receipts; both valid successes and valid failures are skipped. Source changes affect queue setup only; policy, schema, physics, controller and evaluation remain frozen. Seven focused resume tests pass locally and on mainskill. The first deployment check exposed an actual PsiBot receipt schema difference and stopped before collection; the helper was corrected to require all native verification checks, then revalidated against the real rich artifact.

Previous active-epoch known spend of $3.09588 and one unknown-usage request are retained; the remaining known-cost soft stop is $8.90412, keeping the original $12 total. The request allowance drops from 2800 to 2785 and the overload-retry counter is retained. All older archived epochs remain included in cost accounting. The new source-freeze digest is ff826b777c3f60cdef82c1e1a94062a0310f7218e6bc936761d6f9653799f52d. Resume and proxy services are running; at this checkpoint resumed inference is not yet verified.

FR3 minus_J seed 10000 is another valid failure, 0/1: right finger/bottle penetration 2.069 mm exceeds 2 mm at simulation 5.1 s. Two calls completed, using 8750 input / 2194 output tokens, $0.19720; wall time 489.795 s, closed loop 151.239 s, pre-observation 338.556 s. Four 77-frame videos are exposed inline (0.345 MB combined). New verified totals are FR3 3/140 (one success) and PsiBot 1/140 (one success). Runtime accounting now resolves completed episodes inside preserved archives. This is 4/280 valid attempts; 276 remain. The long-horizon phase is still pending.

Delivery checks: 16 new-cohort clips plus two historical clips loaded and advanced playback; previous resources were released. All 16 original poster SHA checks and MP4 faststart checks pass. Historical seven rows, 28 inputs and 14 videos remain; desktop/mobile layout and zero startup MP4 download pass. Seven queue-resume regression tests pass.
