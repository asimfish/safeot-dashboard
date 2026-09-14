import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from resume_receipts import load_completed


class ResumeReceipts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ep = self.root / 'recovery/epoch/episode'
        self.ep.mkdir(parents=True)
        self.result = {'seed': 10000, 'condition': 'rich', 'success': True,
                       'attempt_validity': 'valid_attempt', 'unknown_usage_requests': 0}
        self.verification = {'passed': True, 'checks': {'control_120hz': True, 'four_decoded_videos': True}}
        self.budget = {'seeds': [10000, 10001], 'conditions': ['rich', 'minus_S']}
        self.refresh()

    def refresh(self):
        for name, value in [('evaluation.json', self.result), ('artifact_verification.json', self.verification)]:
            (self.ep / name).write_text(json.dumps(value))
        self.item = {'relative_path': 'recovery/epoch/episode', 'sha256': {
            name: hashlib.sha256((self.ep / name).read_bytes()).hexdigest()
            for name in ('evaluation.json', 'artifact_verification.json')}}
        self.budget['resume_completed_episodes'] = [self.item]

    def test_resume_skips_success_but_retains_remaining_order(self):
        results, checks, done = load_completed(self.root, self.budget)
        self.assertEqual(done, {(10000, 'rich')})
        queue = [(s, c) for s in self.budget['seeds'] for c in self.budget['conditions'] if (s, c) not in done]
        self.assertEqual(queue, [(10000, 'minus_S'), (10001, 'rich'), (10001, 'minus_S')])
        self.assertTrue(results[0]['success'] and checks[0]['passed'])

    def test_valid_failure_also_skipped(self):
        self.result['success'] = False
        self.refresh()
        self.assertEqual(load_completed(self.root, self.budget)[2], {(10000, 'rich')})

    def test_interrupted_or_unknown_rejected(self):
        for changes in [{'attempt_validity': 'interrupted'}, {'unknown_usage_requests': 1}]:
            old = copy.deepcopy(self.result)
            self.result.update(changes)
            self.refresh()
            with self.assertRaises(AssertionError):
                load_completed(self.root, self.budget)
            self.result = old

    def test_changed_or_bad_verification_rejected(self):
        (self.ep / 'evaluation.json').write_text('{}')
        with self.assertRaises(AssertionError):
            load_completed(self.root, self.budget)
        self.verification['passed'] = False
        self.refresh()
        with self.assertRaises(AssertionError):
            load_completed(self.root, self.budget)

    def test_duplicate_and_outside_cohort_rejected(self):
        self.budget['resume_completed_episodes'] *= 2
        with self.assertRaises(AssertionError):
            load_completed(self.root, self.budget)
        self.refresh()
        self.budget['seeds'] = [10001]
        with self.assertRaises(AssertionError):
            load_completed(self.root, self.budget)

    def test_path_escape_rejected(self):
        self.item['relative_path'] = '../outside'
        with self.assertRaises(AssertionError):
            load_completed(self.root, self.budget)

    def test_fresh_epoch(self):
        self.budget.pop('resume_completed_episodes')
        self.assertEqual(load_completed(self.root, self.budget), ([], [], set()))


if __name__ == '__main__':
    unittest.main()
