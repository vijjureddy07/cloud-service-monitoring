import unittest
from scripts.check_service import run_checks
from scripts.summarize_checks import summarize

GOOD = {'ok': True, 'status_code': 200, 'reason': 'healthy', 'latency_ms': 8.5}
BAD = {'ok': False, 'status_code': 503, 'reason': 'HTTP 503', 'latency_ms': 5.0}

class MonitoringTests(unittest.TestCase):
    def test_success_first_try(self):
        report = run_checks('http://demo', attempts=3, sleep=lambda _: None, probe_func=lambda _u, timeout: GOOD)
        self.assertEqual((report['outcome'], report['attempts']), ('UP', 1))

    def test_retry_then_recover(self):
        outcomes = iter([BAD, BAD, GOOD])
        report = run_checks('http://demo', attempts=3, sleep=lambda _: None, probe_func=lambda _u, timeout: next(outcomes))
        self.assertEqual((report['outcome'], report['attempts']), ('UP', 3))

    def test_failure_after_retries(self):
        report = run_checks('http://demo', attempts=2, sleep=lambda _: None, probe_func=lambda _u, timeout: BAD)
        self.assertEqual((report['outcome'], report['attempts']), ('DOWN', 2))

    def test_group_consecutive_failures_as_one_incident(self):
        items = [{'outcome': v} for v in ['UP', 'DOWN', 'DOWN', 'UP', 'DOWN']]
        self.assertEqual(summarize(items), {'checks': 5, 'up': 2, 'down': 3, 'availability_percent': 40.0, 'incidents': 2})

    def test_empty_log(self):
        self.assertIsNone(summarize([])['availability_percent'])

if __name__ == '__main__': unittest.main()
