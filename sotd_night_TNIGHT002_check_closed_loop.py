"""Independent acceptance of an executor-owned batched closed-loop adapter.

No learner is implemented here. This checks the actual frozen environment and
finite differences of full episodic objectives, not a dummy neural-network loss.
"""
import argparse
import copy
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
import torch

REPO = Path(__file__).resolve().parents[2]
SNAPSHOT = REPO / 'diagnostic_runs/reward_objective_alignment/v1/snapshot'
sys.path.insert(0, str(SNAPSHOT))
from experiments.run_synthetic_multi_constraint import build_ppolag_agent, make_synthetic_multi_constraint_env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adapter', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    torch.set_num_threads(1)
    spec = importlib.util.spec_from_file_location('audited_oracle_adapter', args.adapter.resolve())
    module = importlib.util.module_from_spec(spec)
    # Adapter contract: pure import plus rollout(actor, params, config, init_pos,
    # env_noise, action_noise, kernel). No training or file mutation on import.
    sys.path.insert(0, str(args.adapter.resolve().parent))
    spec.loader.exec_module(module)
    counts = {'actual_environment_steps': 0, 'model_forward_calls': 0, 'model_transitions': 0}
    report = {'status': 'RUNNING', 'counts': counts, 'checks': [], 'errors': [],
              'adapter_sha256': hashlib.sha256(args.adapter.read_bytes()).hexdigest(),
              'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.out.parent.mkdir(parents=True, exist_ok=True)

    def save():
        tmp = args.out.with_suffix('.tmp')
        tmp.write_text(json.dumps(report, indent=2))
        tmp.replace(args.out)

    def ensure(ok, label):
        if not bool(ok):
            raise AssertionError(label)

    class RecordingRNG:
        def __init__(self, rng):
            self.rng, self.values = rng, []

        def normal(self, *a, **kw):
            v = self.rng.normal(*a, **kw)
            self.values.append(v.astype(np.float32))
            return v

    save()
    try:
        for env_idx, name in enumerate(['DiagReachK2', 'DiagReachK3']):
            torch.manual_seed(180)
            template = make_synthetic_multi_constraint_env(name, 180, budget_shaping_coef=5)
            actor = build_ppolag_agent(template, {'device': 'cpu', 'total_steps': 240, 'steps_per_epoch': 240}).actor.double()
            config = asdict(template.config)
            config['cost_limits'] = list(template.cost_limits)
            params = dict(actor.named_parameters())
            ensure(sum(p.numel() for p in params.values()) == 5060, 'frozen actor architecture changed')
            for kernel in ['sample', 'det']:
                initial, noises, zetas, refs = [], [], [], []
                for ep in range(8):
                    env = make_synthetic_multi_constraint_env(name, 8100000 + 100 * env_idx + ep, budget_shaping_coef=0)
                    obs = env.reset()
                    initial.append(np.array(env._pos, copy=True))
                    rec = RecordingRNG(env.rng)
                    env.rng = rec
                    z = np.random.default_rng(8200000 + 100 * env_idx + ep).standard_normal((12, 2))
                    zetas.append(z)
                    rows = {k: [] for k in ['states', 'proposal', 'executed', 'raw_rewards', 'costs', 'cumulative_costs']}
                    for t in range(12):
                        with torch.no_grad():
                            mu, ls = actor(torch.tensor(obs, dtype=torch.double))
                            proposal = mu + ls.exp() * torch.tensor(z[t], dtype=torch.double) if kernel == 'sample' else mu
                        rows['states'].append(np.array(obs, copy=True))
                        obs, reward, cost, done, info = env.step(proposal.numpy())
                        counts['actual_environment_steps'] += 1
                        rows['proposal'].append(proposal.numpy().copy())
                        rows['executed'].append(info['executed_action'].copy())
                        rows['raw_rewards'].append(reward)
                        rows['costs'].append(cost.copy())
                        rows['cumulative_costs'].append(info['cost_episode_cumulative'].copy())
                        ensure(done == (t == 11), 'horizon mismatch')
                    ensure(len(rec.values) == 12, 'environment noise recording mismatch')
                    noises.append(np.array(rec.values)); refs.append(rows)
                    env.close()
                init = torch.tensor(np.array(initial), dtype=torch.double)
                noise = torch.tensor(np.array(noises), dtype=torch.double)
                z = torch.tensor(np.array(zetas), dtype=torch.double)

                def query(pdict):
                    counts['model_forward_calls'] += 1
                    counts['model_transitions'] += 8 * 12
                    out = module.rollout(actor, pdict, config, init, noise, z, kernel)
                    ensure(isinstance(out, dict), 'rollout must return a dict')
                    for key in refs[0]:
                        ensure(key in out and torch.is_tensor(out[key]), 'missing tensor ' + key)
                        ensure(tuple(out[key].shape) == np.array([r[key] for r in refs]).shape, 'shape mismatch ' + key)
                        ensure(torch.isfinite(out[key]).all(), 'nonfinite ' + key)
                    return out

                out = query(params)
                errors = {}
                for key in refs[0]:
                    expected = torch.tensor(np.array([r[key] for r in refs]), dtype=torch.double)
                    atol = 1e-4 if key == 'raw_rewards' else 2e-5
                    errors[key] = float((out[key].detach() - expected).abs().max())
                    ensure(torch.allclose(out[key], expected, atol=atol, rtol=2e-6), 'closed-loop original environment mismatch ' + key)
                vals = torch.cat([out['raw_rewards'].sum(1).mean().reshape(1), out['costs'].sum(1).mean(0)])
                ensure(vals.requires_grad, 'episodic objectives detached')
                grads = []
                for v in vals:
                    gs = torch.autograd.grad(v, tuple(params.values()), retain_graph=True, allow_unused=True)
                    grads.append([torch.zeros_like(p) if g is None else g for p, g in zip(params.values(), gs)])
                flat_grad = torch.stack([torch.cat([g.flatten() for g in gs]) for gs in grads])
                ensure(float(flat_grad[0].norm()) > 1e-8, 'episodic reward actor gradient zero')
                ensure(any('backbone' in n and float(g.norm()) > 1e-8 for (n, _), g in zip(params.items(), grads[0])), 'reward does not reach backbone')
                if kernel == 'det':
                    ensure(all(float(g.norm()) < 1e-10 for (n, _), g in zip(params.items(), grads[0]) if 'log_std_head' in n), 'det reward depends directly on pure std head')
                fd_records = []
                for direction_idx in range(2):
                    gen = torch.Generator().manual_seed(8300000 + env_idx * 10 + direction_idx)
                    ds = [torch.randn(p.shape, dtype=p.dtype, generator=gen) for p in params.values()]
                    if direction_idx == 1:
                        ds = [d if 'backbone' in n else torch.zeros_like(d) for (n, _), d in zip(params.items(), ds)]
                    norm = torch.sqrt(sum((d*d).sum() for d in ds)); ds = [d/norm for d in ds]
                    analytic = flat_grad @ torch.cat([d.flatten() for d in ds])
                    passes = []
                    for h in [1e-4, 1e-5, 1e-6]:
                        vv = []
                        for sign in [1, -1]:
                            pd = {n: p.detach() + sign*h*d for (n, p), d in zip(params.items(), ds)}
                            y = query(pd)
                            vv.append(torch.cat([y['raw_rewards'].sum(1).mean().reshape(1), y['costs'].sum(1).mean(0)]).detach())
                        fd = (vv[0]-vv[1])/(2*h)
                        ok = (analytic-fd).abs() <= 1e-6 + 1e-3*torch.maximum(analytic.abs(), fd.abs())
                        passes.append(ok)
                        fd_records.append({'direction': direction_idx, 'h': h, 'analytic': analytic.detach().tolist(), 'finite_difference': fd.tolist(), 'pass_per_objective': ok.tolist()})
                    ensure((torch.stack(passes).sum(0) >= 2).all(), 'episodic full-actor finite difference failed')
                # Exercise a real copy of the original actor: this is a graph/unit check, not training evidence.
                changed = copy.deepcopy(actor)
                with torch.no_grad():
                    for p, g in zip(changed.parameters(), grads[0]):
                        p.add_(g, alpha=1e-5 / max(float(flat_grad[0].norm()), 1.))
                ensure(any(not torch.equal(p, q) for p, q in zip(actor.parameters(), changed.parameters())), 'actor parameter installation unchanged')
                report['checks'].append({'env': name, 'kernel': kernel, 'episodes': 8, 'errors': errors,
                                         'objective_gradient_norms': flat_grad.norm(dim=1).tolist(), 'finite_difference': fd_records,
                                         'actual_actor_copy_changed': True})
                save()
            template.close()
        ensure(counts['actual_environment_steps'] == 384, 'actual environment call count mismatch')
        report['status'] = 'PASS_CLOSED_LOOP_AND_EPISODIC_GRADIENT'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
        raise
    finally:
        save()


if __name__ == '__main__':
    main()
