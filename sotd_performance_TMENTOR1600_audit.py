"""Read-only audit of frozen controls and two completed pilot branches.

No environment or learner imports; no new rollouts or fitting.
All output is restricted to this mentor task directory.
"""
import collections
import hashlib
import json
from pathlib import Path

import numpy as np
import torch

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
INPUTS = {}


def source(path):
    path = Path(path)
    INPUTS[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return path


def read(path):
    return json.loads(source(path).read_text())


def tensors(path):
    return torch.load(source(path), map_location="cpu", weights_only=False)


def same(a, b):
    return a.keys() == b.keys() and all(torch.equal(a[k], b[k]) for k in a)


def inspect_job(path):
    job, result, epochs = [read(path / name) for name in ("job.json", "result.json", "epochs.json")]
    assert job['metric'] == 'KL' and job['inner_reward'] == job['outer_reward'] == 'raw'
    assert result['effective_config']['actual_steps'] == 12000
    final = result['eval']['episodes']
    assert len(final) == 312
    budgets = np.asarray(result['cost_limits'])
    costs = np.asarray([e['costs'] for e in final])
    actions = tensors(path / 'actor.pt')
    installs = [e for e in epochs if e['effective_update']]
    last = installs[-1] if installs else None
    last_matches = last is not None and same(
        actions, tensors(path / f"cycle_{last['cycle']:03d}_after.pt")['actor'])
    phases = collections.Counter()
    for line in source(path / 'training_episodes.jsonl').read_text().splitlines():
        ep = json.loads(line)
        phase = ep['phase'].split('_')[0]
        phases[phase] += len(ep['trace'])
    assert sum(phases.values()) == 12000
    actual = dict(exploration_steps=phases['exploration'], selection_steps=phases['select'],
                  acceptance_steps=phases['accept'])
    reported = {k: result['effective_config'][k] for k in actual}
    rows = []
    for e in epochs:
        fi = e['fisher_info']
        risks = e['selection_risks']
        kl = [r['KL'] for r in e['regularizers']]
        assert len(risks) == 3 and len(kl) == 3
        # Exact same risk/reward ordering; only candidate eligibility changes.
        eligible = [i for i in e['eligible'] if i == 0 or kl[i] <= .01001]
        safe = [i for i in eligible if risks[i]['event_free']]
        alt = (max(safe, key=lambda i: (risks[i]['actual_score'], i)) if safe else
               min(eligible, key=lambda i: (*risks[i]['risk_pair'], -risks[i]['actual_score'], -i)))
        selected = e['candidate_sources'].index(e['source'])
        rows.append(dict(
            cycle=e['cycle'], source=e['source'], effective=e['effective_update'],
            installed_KL=e['actual_regularizer']['KL'], joint_surrogate_accepted=fi['accepted'],
            joint_surrogate_cost_feasible=bool(np.all(np.asarray(fi['actual_predicted_cost']) <= budgets + 1e-5)),
            joint_surrogate_reward_gain=fi['reward_gain'],
            joint_screen_mean_feasible=risks[1]['mean_feasible'],
            joint_screen_event_free=risks[1]['event_free'],
            ppo_screen_event_free=risks[2]['event_free'],
            solver_recovery=fi['recovery'], outer_recovery=e['recovery'],
            uniform_KL_mask_changes_selection=bool(alt != selected),
            uniform_KL_mask_slot=alt,
        ))
    return dict(
        job=path.name, path=str(path.relative_to(ROOT)), env=job['env'], seed=job['seed'],
        reward=result['eval']['reward_mean'], joint=result['eval']['joint_pass'],
        final_any_events=int((costs > budgets).any(1).sum()),
        final_channel_events=(costs > budgets).sum(0).tolist(),
        final_episodes=312, actual_steps=12000,
        actual_allocation=actual, reported_allocation=reported, allocation_metadata_matches=actual == reported,
        last_effective_cycle=last['cycle'] if last else None,
        last_effective_source=last['source'] if last else None,
        trailing_unchanged_cycles=len(epochs) - 1 - (last['cycle'] if last else -1),
        last_installed_actor_matches_final=last_matches,
        last_acceptance_event_free=last['acceptance_new_risk']['event_free'] if last else None,
        epochs=rows,
    )


def aggregate(jobs):
    rows = [e for j in jobs for e in j['epochs']]
    installed = [e for e in rows if e['effective']]
    ppo = [e for e in installed if e['source'] == 'full_PPO']
    joint = [e for e in installed if e['source'] == 'joint_KL']
    unsafe = [j for j in jobs if j['final_any_events']]
    return dict(
        jobs=len(jobs), cycles=len(rows), installations=len(installed),
        ppo_installs=len(ppo), ppo_installs_above_KL_radius=sum(e['installed_KL'] > .01001 for e in ppo),
        joint_installs=len(joint), joint_installs_above_KL_radius=sum(e['installed_KL'] > .01001 for e in joint),
        max_installed_KL=max(e['installed_KL'] for e in installed),
        joint_surrogate_accepted=sum(e['joint_surrogate_accepted'] for e in rows),
        joint_surrogate_cost_feasible=sum(e['joint_surrogate_cost_feasible'] for e in rows),
        joint_screen_mean_infeasible=sum(not e['joint_screen_mean_feasible'] for e in rows),
        joint_screen_with_event=sum(not e['joint_screen_event_free'] for e in rows),
        solver_recovery=sum(e['solver_recovery'] for e in rows),
        outer_recovery=sum(e['outer_recovery'] for e in rows),
        uniform_KL_mask_changes_selection=sum(e['uniform_KL_mask_changes_selection'] for e in rows),
        unsafe_final_jobs=len(unsafe),
        unsafe_final_matches_zero_event_acceptance=sum(
            j['last_installed_actor_matches_final'] and j['last_acceptance_event_free'] for j in unsafe),
        stale_allocation_metadata_jobs=sum(not j['allocation_metadata_matches'] for j in jobs),
        tasks={task: dict(mean_reward=float(np.mean([j['reward'] for j in jobs if j['env'] == task])),
                         mean_joint=float(np.mean([j['joint'] for j in jobs if j['env'] == task])))
               for task in ('DiagReachK2', 'DiagReachK3')},
    )


def main():
    all_jobs = []
    branches = {}
    for name, pattern in (
        ('reward_objective_alignment', 'development_*_KL_RR'),
        ('candidate_span', 'span_DiagReach*_KL'),
        ('interaction_allocation', 'alloc_attempt2_DiagReach*'),
    ):
        base = ROOT / 'diagnostic_runs' / name / 'v1'
        for f in ('worker.py', 'joint_solver.py', 'core.py', 'risk.py'):
            source(base / f)
        jobs = [inspect_job(p) for p in sorted((base / 'jobs').glob(pattern))]
        assert len(jobs) == 6
        branches[name] = dict(summary=aggregate(jobs), jobs=jobs)
        all_jobs += jobs
    report = dict(
        status='READ_ONLY_AUDIT_COMPLETE', new_environment_steps=0,
        scope='18 development runs, paired/reused seeds, 420 correlated cycles; descriptive evidence only',
        limits=['No causal claim that KL bypass causes violations.',
                'Four deterministic screen episodes do not estimate population feasibility precisely.',
                'Mask replays change selection only; alternative acceptance data and retraining are not available.',
                'Source files are current observed copies; their hashes do not retroactively prove launch-time immutability.'],
        summary=aggregate(all_jobs), branches=branches,
        input_sha256=INPUTS,
    )
    (OUT / 'audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({'summary': report['summary'], 'branches': {k: v['summary'] for k, v in branches.items()}}, indent=2))


if __name__ == '__main__':
    main()
