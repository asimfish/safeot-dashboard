# Astra experiment explanation update

Refs: T-311

Added four questions covering actual E3 model inputs and outputs, Astra/controller responsibilities, proposed RGB information ablations and long-horizon evidence limits. These are documentation additions; no new experiments or score changes.

Verified against actual E3 prompts, public state, action schemas and the model client, campaign, simulator observation and servo execution code on 2026-09-10. Retained all 50 existing anchors and 42 media references; checked all fragment targets and unique IDs. Chrome checks passed at 1440, 390 and 320 pixels with no page overflow, working keyboard disclosures, no runtime exceptions and the existing $27.87 E3 estimate. Desktop and mobile screenshots inspected. Diff whitespace check passed.

RGB-only and long-horizon proposals remain unrun. Existing simulation uses paused physics during model inference and a robot-state-aware generic IK controller.
