# T-330 · FR3 front-view replacement and current campaign evidence

The current FR3 overhead camera obscures the approach region. This change places the original same-instant overhead/front PNGs near the top of the report and prepares an independent four-view replacement rig. The third channel keeps its neutral ID while its camera pose and corresponding extrinsics change; other cameras, the prompt, action contract, budget and evaluator stay fixed. This is a prepared configuration with 28 CPU serialization cases passing; no new camera runtime or model success is claimed.

The current 20x7 campaign remains on its original camera rig. Verified overnight additions are FR3 minus_F success, minus_H failure, rgb_only failure; PsiBot minus_S failure and minus_J success. Counts are now FR3 7/140, PsiBot 3/140. Every condition remains n=1 or uncompleted. Current results are now 14 visible condition rows, including 40 actual input images and 40 lazy inline videos, with per-success cost, per-episode timing, tokens and attempt counts. Earlier detailed explanations remain available below the table.

All 20 new videos preserve 640x480, 15 fps and exact original frame counts; faststart is verified. Input posters match the original files. No evaluator-only geometry is passed to the model. Unknown usage is not priced at zero. Raw collection timing and closed-loop timing have distinct definitions.

Transport recovery: the FR3 forwarding port vanished after the overnight SSH disconnect. Both platform tunnels now reconnect independently. A later attempt stopped before new model requests because the 5.9 TB dataset volume was full. Both task trees were copied to a private system-disk spool and all 6,607 files matched by hash. Original data remains intact. Private bind mounts preserve execution paths, and the source/controller/physics/camera contracts stay unchanged. Both collectors have since returned real model responses. The root cause of the initial jump-host disconnection remains unproven; the reconnection change is a mitigation.

Review notes: new row data attributes were given a campaign-specific prefix so the existing historical episode selector does not intercept video clicks. The older front-results section now contains its horizontal overflow so it cannot scale the whole mobile page down.

Validation: zero-model CPU payload audit (28 cases); seven preserved-completion resume tests; request/cost guard checks including carried request and spend counts; complete source hashes checked before/after storage migration; media metadata/hash checks; desktop/mobile and 42 actual playback checks; git diff --check and agentctl manual check. Runtime camera validation and the 20x7 campaign remain incomplete.

Refs: T-330
