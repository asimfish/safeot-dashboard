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
