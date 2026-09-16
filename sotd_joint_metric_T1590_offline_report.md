# Offline numerical gates (zero environment interactions)

| Task | Seed | cW | KL_s1 replay | Accepted metric-scale solves /6 |
|---|---:|---:|---|---:|
| DiagReachK2 | 180 | 1.109611400 | exact actor and coordinates | 6 |
| DiagReachK2 | 186 | 1.970060763 | exact actor and coordinates | 6 |
| DiagReachK2 | 187 | 1.370475117 | exact actor and coordinates | 6 |
| DiagReachK3 | 180 | 1.407689946 | exact actor and coordinates | 6 |
| DiagReachK3 | 186 | 2.008800380 | exact actor and coordinates | 6 |
| DiagReachK3 | 187 | 1.658006021 | exact actor and coordinates | 6 |

Calibration is first KL.01 anchor only, never chosen using evaluation. All36 cases retained even if their reward surrogate differs; no scale selection at this gate. Isotropic fixture yields proportional metrics and identical solution; anisotropic fixture is a mathematical positive control only, not task performance evidence.
Two pretraining offline scripting exceptions are retained under offline_failure_1/2 with receipt and source; neither changed optimization mathematics or consumed environment interactions.
