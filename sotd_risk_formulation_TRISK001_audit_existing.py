"""Recompute existing evidence only; never instantiate an environment or learner."""
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import beta, binomtest

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT / "diagnostic_runs/reward_objective_alignment/v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name, rows):
    with (OUT / name).open("w") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def frozen_risk_proxy(manifest):
    """Re-use existing fresh bank and stored action likelihood ratios, no fitting."""
    rows = []
    for path in sorted((SOURCE / "jobs").glob("mechanism_*")):
        j = json.loads((path / "job.json").read_text())
        b = np.array([6, 6] if j["env"] == "DiagReachK2" else [7, 6.5, 12.5], dtype=np.float32)

        def load_events(label):
            p = path / (label+".npz")
            manifest[str(p.relative_to(ROOT))] = sha(p)
            with np.load(p) as z:
                cost = z["values"][:, :, 3:].astype(np.float32)
                cross = np.cumsum(cost, axis=1, dtype=np.float32) > b
                assert np.array_equal(cross[:, -1], z["totals"][:, 3:] > b)
            # Each channel and the union are separate probability objects.
            cross = np.concatenate([cross, cross.any(2, keepdims=True)], axis=2)
            hit = cross & ~np.concatenate([np.zeros_like(cross[:, :1]), cross[:, :-1]], axis=1)
            assert np.array_equal(hit.sum(1), cross[:, -1])
            return hit.astype(float), cross[:, -1].astype(float)

        hits, old_s = load_events("sample_old")
        _, old_d = load_events("det_old")
        ret = hits[:, ::-1].cumsum(1)[:, ::-1]
        adv = (ret-ret.mean(0))*64/63
        for target in ("shaped", "raw"):
            for metric in ("KL", "W2"):
                label = target+metric
                _, new_s = load_events("sample_"+label)
                _, new_d = load_events("det_"+label)
                pp = path / (label+"_contributions.npz")
                manifest[str(pp.relative_to(ROOT))] = sha(pp)
                with np.load(pp) as z:
                    ratio = z["ratio"]
                assert ratio.shape == (64, 12)
                predicted_delta = ((ratio-1)[:, :, None]*adv).sum(1).mean(0)
                for k in range(len(b)+1):
                    sample_delta = float((new_s-old_s)[:, k].mean())
                    det_delta = float((new_d-old_d)[:, k].mean())
                    prediction = float(old_s[:, k].mean()+predicted_delta[k])
                    rows.append(dict(env=j["env"], seed=j["seed"], anchor=j["anchor"],
                                     target=target, metric=metric,
                                     channel=str(k) if k < len(b) else "any",
                                     old_sample_risk=float(old_s[:, k].mean()),
                                     old_det_risk=float(old_d[:, k].mean()),
                                     predicted_sample_risk=prediction,
                                     measured_sample_risk=float(new_s[:, k].mean()),
                                     measured_det_risk=float(new_d[:, k].mean()),
                                     predicted_delta=float(predicted_delta[k]),
                                     sample_delta=sample_delta, det_delta=det_delta,
                                     proxy_minus_sample=float(predicted_delta[k]-sample_delta),
                                     sample_minus_det=sample_delta-det_delta,
                                     proxy_minus_det=float(predicted_delta[k]-det_delta),
                                     outside_probability_range=not (0 <= prediction <= 1)))
    assert len(rows) == 168
    write_csv("mechanism_risk_proxy.csv", rows)
    anyrows = [x for x in rows if x["channel"] == "any"]
    return dict(candidate_pairs=len(anyrows), channel_and_any_rows=len(rows),
                outside_probability_range=sum(x["outside_probability_range"] for x in rows),
                any_risk_decrease_predicted_det_increase=sum(x["predicted_delta"] < 0 < x["det_delta"] for x in anyrows),
                mean_abs_proxy_minus_sample_any=float(np.mean([abs(x["proxy_minus_sample"]) for x in anyrows])),
                mean_abs_proxy_minus_det_any=float(np.mean([abs(x["proxy_minus_det"]) for x in anyrows])),
                mean_abs_sample_minus_det_any=float(np.mean([abs(x["sample_minus_det"]) for x in anyrows])),
                inference="Posthoc frozen-bank diagnostic, no trained first-hit treatment, no probability clipping, no independence claim.")


def main():
    rows, manifest = [], {}
    final_mismatches = 0
    jobs = []
    for path in sorted((SOURCE / "jobs").glob("development_*")):
        job = json.loads((path / "job.json").read_text())
        # SR==SS and RR==RS full-trajectory equalities were established by T1593.
        # This is an explicit restriction, not a claim of independent trajectories.
        if job["combo"] not in ("SS", "RS"):
            continue
        jobs.append(path.name)
        tracepath = path / "training_episodes.jsonl"
        jobpath = path / "job.json"
        manifest[str(tracepath.relative_to(ROOT))] = sha(tracepath)
        manifest[str(jobpath.relative_to(ROOT))] = sha(jobpath)
        budgets = np.array([6, 6] if job["env"] == "DiagReachK2" else [7, 6.5, 12.5], dtype=np.float32)
        epochs = {}
        for line in tracepath.open():
            ep = json.loads(line)
            if ep["phase"] == "exploration":
                epochs.setdefault(ep["cycle"], []).append(ep)
        assert sorted(epochs) == list(range(25))
        for cycle, eps in sorted(epochs.items()):
            assert len(eps) == 20
            c = np.array([[t["cost"] for t in ep["trace"]] for ep in eps], dtype=np.float32)
            assert c.shape == (20, 12, len(budgets)) and np.all(c >= 0)
            cum = np.cumsum(c, axis=1, dtype=np.float32)
            event = cum > budgets
            hit = event & ~np.concatenate([np.zeros_like(event[:, :1]), event[:, :-1]], axis=1)
            assert np.array_equal(hit.sum(1), event[:, -1])
            flags = np.array([ep["violation"] for ep in eps], dtype=bool)
            final_mismatches += int(not np.array_equal(flags, event[:, -1]))
            assert np.array_equal(cum[:, -1], np.array([ep["costs"] for ep in eps], dtype=np.float32))
            # Match target precision in the existing finite_targets/time_loo path.
            f = np.cumsum(hit[:, ::-1].astype(np.float32), axis=1, dtype=np.float32)[:, ::-1]
            ca_return = np.cumsum(c[:, ::-1], axis=1, dtype=np.float32)[:, ::-1]
            fa = (f - f.mean(0)) * 20 / 19
            ca = (ca_return - ca_return.mean(0)) * 20 / 19
            for k in range(len(budgets)):
                n = int(event[:, -1, k].sum())
                rows.append(dict(job=path.name, env=job["env"], metric=job["metric"], combo=job["combo"],
                                 seed=job["seed"], cycle=cycle, channel=k, episodes=20, events=n,
                                 zero_event=n == 0, all_event=n == 20,
                                 firsthit_adv_zero=bool(np.all(fa[:, :, k] == 0)),
                                 continuous_adv_zero=bool(np.all(ca[:, :, k] == 0)),
                                 firsthit_adv_std=float(fa[:, :, k].std()),
                                 continuous_adv_std=float(ca[:, :, k].std())))
    assert len(jobs) == 24 and len(rows) == 1500 and final_mismatches == 0
    write_csv("learning_signal.csv", rows)
    power = []
    for tests in (1, 25, 75):
        alpha = .05 / tests
        for risk in (.01, .05):
            n = math.ceil(math.log(alpha) / math.log1p(-risk))
            upper = float(beta.ppf(1-alpha, 1, n))
            exact = binomtest(0, n, alternative="less").proportion_ci(1-alpha, method="exact").high
            assert abs(upper-exact) < 1e-10 and upper <= risk
            assert 1-alpha**(1/(n-1)) > risk
            power.append(dict(family_tests=tests, alpha_per_test=alpha, illustrative_risk_target=risk,
                              minimum_zero_event_episodes=n, upper=upper,
                              steps_per_validation=12*n, steps_for_25_validations=25*12*n))
    write_csv("sample_complexity.csv", power)
    frozen = frozen_risk_proxy(manifest)
    zero = sum(x["firsthit_adv_zero"] for x in rows)
    summary = dict(status="VERIFIED_DESCRIPTIVE_AUDIT", source="T1593", selected_jobs=jobs,
                   selected_jobs_count=len(jobs), cycles=600, channel_batches=len(rows),
                   firsthit_adv_zero=zero, firsthit_adv_nonzero=len(rows)-zero,
                   zero_event_channel_batches=sum(x["zero_event"] for x in rows),
                   all_event_channel_batches=sum(x["all_event"] for x in rows),
                   continuous_adv_zero=sum(x["continuous_adv_zero"] for x in rows),
                   original_event_flag_mismatches=final_mismatches,
                   episode_final_cost_mismatches=0,
                   new_environment_steps=0, new_training_steps=0,
                   cp_zero_of_four_upper=float(beta.ppf(.95, 1, 4)),
                   cp_zero_of_312_upper=float(beta.ppf(.95, 1, 312)),
                   frozen_risk_proxy=frozen,
                   limits=["Training data come from stochastic policies, not deterministic deployment.",
                           "Outer exact duplicates excluded; cross-job shared trajectories remain correlated.",
                           "Nonzero advantage does not guarantee a useful or nonzero aggregate policy gradient.",
                           "Existing final evaluation remains retrospective evidence, not a new selection set.",
                           "Illustrative 1%/5% risk levels are not a change to the user safety requirement."])
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
    manifest["diagnostic_runs/reward_objective_alignment/v1/report.md"] = sha(SOURCE / "report.md")
    (OUT / "input_hashes.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("selected_jobs", "limits")}, indent=2))


if __name__ == "__main__":
    main()
