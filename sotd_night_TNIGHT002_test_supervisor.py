"""Offline checks: no API writes and no experiment runs."""
import unittest
from supervisor import decide, clean, external_steering


class Scheduling(unittest.TestCase):
    def test_running_agent_is_never_dispatched(self):
        self.assertEqual(decide(10, 100, {'is_running': 1}, {}, True, 0), 'stream')

    def test_done_sse_without_idle_does_not_override_running(self):
        self.assertEqual(decide(10, 100, {'is_running': 1, 'done': False}, {}, True, 0), 'stream')

    def test_queue_is_preserved(self):
        self.assertEqual(decide(10, 100, {}, {'items': [{'id': 'user'}]}, True, 0), 'respect_queue')

    def test_deadline_has_priority(self):
        self.assertEqual(decide(100, 100, {}, {}, True, 0), 'deadline')

    def test_no_dispatch_before_protocol_ready(self):
        self.assertEqual(decide(10, 100, {}, {}, False, 0), 'preparing')

    def test_uncertain_post_is_not_replayed(self):
        self.assertEqual(decide(10, 100, {}, {}, True, 0, True), 'uncertain_delivery')

    def test_cooldown(self):
        self.assertEqual(decide(10, 100, {}, {}, True, 20), 'cooldown')

    def test_idle_dispatch(self):
        self.assertEqual(decide(10, 100, {}, {}, True, 0), 'dispatch')

    def test_redaction(self):
        self.assertNotIn('ct-secret', clean('Authorization: Bearer ct-secret'))

    def test_new_user_steering_pauses_automatic_dispatch(self):
        self.assertTrue(external_steering({'type': 'human', 'text': 'stop'}, 'my-campaign'))
        self.assertFalse(external_steering({'type': 'human', 'text': '[campaign=my-campaign; round=1]'}, 'my-campaign'))
        self.assertFalse(external_steering({'type': 'tool_result', 'text': 'stop'}, 'my-campaign'))


if __name__ == '__main__':
    unittest.main()
