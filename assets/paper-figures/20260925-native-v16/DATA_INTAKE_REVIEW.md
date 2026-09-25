# Resolution: preferred a41 source verified

The apparent forest/count mismatch is resolved for the preferred frozen version: the archived a41 manifest binds its estimates to the same 534-run A1 index and Bullet r4 cohort used by the new curve/count delivery. All four relevant producer source hashes still match. Figure 3 now preserves those original 31 estimates and intervals and joins the supplied counts and all-task curves. The later 686-row cross-suite refresh is not mixed into this version.

One follow-up remains: the separately sourced five-seed warm control has no delivered task-win count. Its original V point/CI is retained; its unavailable count/return is an em dash, not a zero. No count was recomputed by drawing. See preferred_a41_alignment.json in the delivery source directory.

---

Earlier intake finding (retained for provenance):

# Figure 3 intake review (06:16Z)

Detected w2_r22 draft exports while producer is still building. Do not publish until producer manifest/README validation is complete.

- New all-task aggregate uses 534 SafePO B25 runs from wave4 v0_partial frozen curve files; cross_suite_tidy current forest uses 686 SafePO rows, updated admission. These are different snapshots.
- Win-count file presently has SafePO CPO/CUP/FOCOPS/PCPO/PID-Lag/PPO-Lag/TRPO-Lag. Forest has TRPO-PID for SafePO too: its count is missing.
- Forest comparator PPO-PID (CPPO-PID) should be explicitly mapped to curve/wins PID-Lag per producer README. Keep that identity in caption/manifest.
- Need counts from the exact same cohort as forest ratios, or a newly consistent full producer forest+counts delivery. Drawing must not recalculate counts.
- All-task curve aggregation is valid as a separately disclosed curve snapshot if producer confirms coverage/normalization; return normalizer is each task maximum of seed-mean return across the four plotted methods and all training epochs, not the forest final-return denominator.
- Figure 3 forest and training curves must state different estimands/normalizers in caption.

Native F1/F2 are now 5.5 x 2.5/2.3 in and actual minimum PDF font 7.1731 pt. New shared style will preserve existing method identity: SafeOT-Dual blue, switch light blue; graph-only teal, realized-cost feedback orange. This honors the method-style contract while carrying the three diagram hues into data figures.
