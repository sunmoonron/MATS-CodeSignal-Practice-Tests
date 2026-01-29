# test_kvstore.py
import json
import unittest
from kvstore import KVStore

class TestKVStoreLevel1(unittest.TestCase):
    def test_set_get(self):
        s = KVStore()
        self.assertIsNone(s.get("a"))
        s.set("a", 123)
        self.assertEqual(s.get("a"), 123)
        s.set("a", 999)
        self.assertEqual(s.get("a"), 999)

    def test_delete(self):
        s = KVStore()
        self.assertFalse(s.delete("missing"))
        s.set("x", "y")
        self.assertTrue(s.delete("x"))
        self.assertIsNone(s.get("x"))
        self.assertFalse(s.delete("x"))



    def test_keys_sorted(self):
        s = KVStore()
        s.set("b", 1)
        s.set("a", 2)
        s.set("c", 3)
        self.assertEqual(s.keys(), ["a", "b", "c"])

class TestKVStoreLevel2TTL(unittest.TestCase):
    def test_ttl_expires(self):
        s = KVStore()
        s.set("a", "alive", ttl_seconds=10, now=100.0)
        self.assertEqual(s.get("a", now=109.999), "alive")
        self.assertIsNone(s.get("a", now=110.0))
        self.assertEqual(s.keys(now=110.0), [])

    def test_ttl_none_means_no_expiry(self):
        s = KVStore()
        s.set("a", 1, ttl_seconds=None, now=0.0)
        self.assertEqual(s.get("a", now=10_000.0), 1)

    def test_overwrite_resets_ttl(self):
        s = KVStore()
        s.set("a", 1, ttl_seconds=10, now=0.0)      # expires at 10
        s.set("a", 2, ttl_seconds=100, now=5.0)     # now expires at 105
        self.assertEqual(s.get("a", now=10.0), 2)
        self.assertEqual(s.get("a", now=104.999), 2)
        self.assertIsNone(s.get("a", now=105.0))

class TestKVStoreLevel3CAS(unittest.TestCase):
    def test_cas_basic(self):
        s = KVStore()

        self.assertTrue(s.compare_and_set("a", None, 1, now=0.0))
        self.assertEqual(s.get("a", now=0.0), 1)
        self.assertFalse(s.compare_and_set("a", None, 2, now=0.0))
        self.assertTrue(s.compare_and_set("a", 1, 2, now=0.0))
        self.assertEqual(s.get("a", now=0.0), 2)

    def test_cas_respects_ttl(self):
        s = KVStore()
        s.set("a", 1, ttl_seconds=10, now=0.0)
        self.assertTrue(s.compare_and_set("a", 1, 2, now=9.0))
        self.assertEqual(s.get("a", now=9.0), 2)
        self.assertIsNone(s.get("a", now=10.0))
        # expired behaves like missing (value None)
        self.assertTrue(s.compare_and_set("a", None, 5, now=10.0))
        self.assertEqual(s.get("a", now=10.0), 5)

class TestKVStoreLevel4DumpLoad(unittest.TestCase):
    def test_dump_load_roundtrip(self):
        s = KVStore()
        s.set("a", 1, ttl_seconds=None, now=0.0)
        s.set("b", {"x": [1, 2, 3]}, ttl_seconds=None, now=0.0)
        dumped = s.dump(now=100.0)
        # must be valid JSON
        obj = json.loads(dumped)
        self.assertEqual(set(obj.keys()), {"a", "b"})

        t = KVStore()
        t.set("z", 999, ttl_seconds=None, now=0.0)
        t.load(dumped)
        self.assertEqual(t.get("a"), 1)
        self.assertEqual(t.get("b"), {"x": [1, 2, 3]})
        self.assertEqual(t.keys(), ["a", "b"])

    def test_dump_excludes_expired(self):
        s = KVStore()
        s.set("a", "keep", ttl_seconds=None, now=0.0)
        s.set("b", "expire", ttl_seconds=10, now=0.0)
        dumped = s.dump(now=10.0)
        obj = json.loads(dumped)
        self.assertEqual(set(obj.keys()), {"a"})

if __name__ == "__main__":
    unittest.main()
