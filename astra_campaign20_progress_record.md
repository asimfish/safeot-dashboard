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
