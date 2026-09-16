"""Independent checks for the finite-data derivation note, zero environment use."""
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

R = Path(__file__).resolve().parent
ROOT = R.parents[1]

hashes = json.loads((R / "input_hashes.json").read_text())
for p, expected in hashes.items():
    assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == expected, p
s = json.loads((R / "summary.json").read_text())
rows = list(csv.DictReader((R / "learning_signal.csv").open()))
assert len(rows) == s["channel_batches"] == 1500
assert sum(x["firsthit_adv_zero"] == "True" for x in rows) == s["firsthit_adv_zero"] == 53
assert s["firsthit_adv_nonzero"] == 1447 and s["new_environment_steps"] == 0
assert s["original_event_flag_mismatches"] == s["episode_final_cost_mismatches"] == 0
for d in csv.DictReader((R / "sample_complexity.csv").open()):
    n, a, risk = int(d["minimum_zero_event_episodes"]), float(d["alpha_per_test"]), float(d["illustrative_risk_target"])
    u = binomtest(0, n, alternative="less").proportion_ci(1-a, method="exact").high
    assert abs(u-float(d["upper"])) < 1e-10 and u <= risk
    assert (1-risk)**n <= a < (1-risk)**(n-1)
    assert int(d["steps_for_25_validations"]) == n*12*25
rr = list(csv.DictReader((R / "mechanism_risk_proxy.csv").open()))
assert len(rr) == 168
for d in rr:
    v = {k:float(d[k]) for k in ("predicted_delta", "sample_delta", "det_delta", "proxy_minus_sample", "sample_minus_det", "proxy_minus_det")}
    assert abs(v["proxy_minus_sample"]+v["sample_minus_det"]-v["proxy_minus_det"]) < 1e-12
anyrows = [d for d in rr if d["channel"] == "any"]
assert len(anyrows) == 48
for k in ("proxy_minus_sample", "proxy_minus_det", "sample_minus_det"):
    expected = s["frozen_risk_proxy"]["mean_abs_"+k+"_any"]
    assert abs(np.mean([abs(float(d[k])) for d in anyrows])-expected) < 1e-12
# Event semantics test including exact boundary and persistent exceedance.
cost = np.array([[.5,.5,0.], [.5,.51,0.], [0.,0.,1.1]], dtype=np.float32)
cross = cost.cumsum(1) > np.float32(1)
first = cross & ~np.column_stack([np.zeros(len(cost), dtype=bool), cross[:, :-1]])
assert np.array_equal(first.sum(1), [0,1,1])
text = (R / "DERIVATION_REVIEW.md").read_text()
for heading in ("Target", "Status", "Invariant Object", "Assumptions", "Notation", "Derivation Strategy", "Derivation Map", "Main Derivation", "Remarks and Interpretation", "Boundaries and Non-Claims", "Open Risks"):
    assert "## "+heading in text
receipt = dict(status="PASS", input_files_verified=len(hashes), firsthit_event_identity=True,
               zero_event_cp_exact_crosscheck=True, minimum_sample_boundary=True,
               kernel_gap_identity=True, summary_recomputed=True, new_environment_steps=0,
               scope="Analysis correctness only; no learning or performance claim.")
(R / "verification.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps(receipt, indent=2))
