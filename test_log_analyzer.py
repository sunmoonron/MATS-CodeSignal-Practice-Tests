import unittest
from log_analyzer import parse_line, LogAnalyzer

SAMPLE = [
    '2026-01-27T12:00:00Z INFO action=login user=alice ip=1.1.1.1 latency_ms=120 msg="hello world"',
    '2026-01-27T12:00:01Z INFO action=login user=bob ip=2.2.2.2 latency_ms=200',
    '2026-01-27T12:00:02Z WARN action=rate_limit user=bob ip=2.2.2.2 latency_ms=50',
    '2026-01-27T12:00:03Z ERROR action=checkout user=alice ip=1.1.1.1 latency_ms=500',
    '2026-01-27T12:00:04Z INFO action=login user=alice ip=1.1.1.1 latency_ms=80',
    '2026-01-27T12:00:05Z INFO action=logout user=alice ip=1.1.1.1',
]

class TestParseLine(unittest.TestCase):
    def test_parse_basic(self):
        e = parse_line(SAMPLE[0])
        self.assertEqual(e.timestamp, "2026-01-27T12:00:00Z")
        self.assertEqual(e.level, "INFO")
        self.assertEqual(e.fields["action"], "login")
        self.assertEqual(e.fields["user"], "alice")
        self.assertEqual(e.fields["ip"], "1.1.1.1")
        self.assertEqual(e.fields["latency_ms"], "120")
        self.assertEqual(e.fields["msg"], "hello world")

class TestAnalyzerLevel1(unittest.TestCase):
    def test_count_levels(self):
        a = LogAnalyzer()
        a.ingest(SAMPLE)
        counts = a.count_levels()
        self.assertEqual(counts["INFO"], 4)
        self.assertEqual(counts["WARN"], 1)
        self.assertEqual(counts["ERROR"], 1)

class TestAnalyzerLevel2(unittest.TestCase):
    def test_top_values(self):
        a = LogAnalyzer()
        a.ingest(SAMPLE)
        self.assertEqual(a.top_values("ip", n=2), [("1.1.1.1", 4), ("2.2.2.2", 2)])
        self.assertEqual(a.most_common("action"), "login")
        self.assertIsNone(a.most_common("missing_field"))

class TestAnalyzerLevel3(unittest.TestCase):
    def test_latency_percentile(self):
        a = LogAnalyzer()
        a.ingest(SAMPLE)
        # latencies present: 120,200,50,500,80 -> sorted: 50,80,120,200,500
        self.assertEqual(a.latency_percentile(0), 50)
        self.assertEqual(a.latency_percentile(50), 120)   # nearest-rank median-ish
        self.assertEqual(a.latency_percentile(100), 500)
        self.assertEqual(a.latency_percentile(95), 500)

class TestAnalyzerLevel4(unittest.TestCase):
    def test_filter(self):
        a = LogAnalyzer()
        a.ingest(SAMPLE)
        errs = a.filter(level="ERROR")
        self.assertEqual(len(errs), 1)
        self.assertEqual(errs[0].fields["action"], "checkout")

        bob_logins = a.filter(field="user", value="bob")
        self.assertEqual(len(bob_logins), 2)

        warn_rate = a.filter(level="WARN", field="action", value="rate_limit")
        self.assertEqual(len(warn_rate), 1)

if __name__ == "__main__":
    unittest.main()
