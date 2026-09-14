"""Accept only immutable, verified prior episodes when restarting an epoch."""
import hashlib
import json
from pathlib import Path


def load_completed(root, budget):
    root = Path(root).resolve()
    results, verifications, completed = [], [], set()
    allowed = {(s, c) for s in budget['seeds'] for c in budget['conditions']}
    for item in budget.get('resume_completed_episodes', []):
        ep = (root / item['relative_path']).resolve()
        assert ep.is_relative_to(root / 'recovery'), 'Resume outside preserved recovery'
        paths = {name: ep / name for name in ('evaluation.json', 'artifact_verification.json')}
        for name, path in paths.items():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'][name], 'Changed resume receipt'
        result = json.loads(paths['evaluation.json'].read_text())
        verification = json.loads(paths['artifact_verification.json'].read_text())
        key = (result['seed'], result['condition'])
        assert key in allowed and key not in completed, 'Duplicate or out-of-cohort resume'
        assert result['attempt_validity'] == 'valid_attempt', 'Interrupted episode cannot be skipped'
        assert result['unknown_usage_requests'] == 0, 'Unknown usage cannot be valid completion'
        assert verification.get('passed') is True and verification.get('checks') and all(v is True for v in verification['checks'].values()), 'Unverified resume'
        # Valid successes and valid failures are both retained; outcomes never select retries.
        result['artifact_sync_verified'] = True
        results.append(result)
        verifications.append({'episode': str(ep), 'passed': True, 'receipt': str(paths['artifact_verification.json'])})
        completed.add(key)
    return results, verifications, completed
