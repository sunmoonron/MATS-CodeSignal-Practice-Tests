import unittest
import json
from url_shortener import URLShortener, encode_base62

class TestBase62(unittest.TestCase):
    def test_encode_base62_examples(self):
        self.assertEqual(encode_base62(1), "1")
        self.assertEqual(encode_base62(2), "2")
        self.assertEqual(encode_base62(10), "a")
        self.assertEqual(encode_base62(61), "Z")
        self.assertEqual(encode_base62(62), "10")
        self.assertEqual(encode_base62(63), "11")

class TestShortenerLevel1(unittest.TestCase):
    def test_shorten_expand_idempotent(self):
        s = URLShortener(domain="https://sho.rt/")
        c1 = s.shorten("https://example.com/a")
        self.assertEqual(c1, "1")
        self.assertEqual(s.expand(c1), "https://example.com/a")

        c1b = s.shorten("https://example.com/a")
        self.assertEqual(c1b, c1)

        c2 = s.shorten("https://example.com/b")
        self.assertEqual(c2, "2")
        self.assertNotEqual(c2, c1)
        self.assertEqual(s.expand(c2), "https://example.com/b")

        self.assertIsNone(s.expand("nope"))

    def test_short_url(self):
        s = URLShortener(domain="https://sho.rt/")
        code = s.shorten("https://example.com/a")
        self.assertEqual(s.short_url(code), "https://sho.rt/1")

class TestShortenerLevel2(unittest.TestCase):
    def test_custom_alias(self):
        s = URLShortener()
        code = s.shorten("https://example.com/alpha", alias="myAlias_1")
        self.assertEqual(code, "myAlias_1")
        self.assertEqual(s.expand("myAlias_1"), "https://example.com/alpha")

    def test_alias_validation(self):
        s = URLShortener()
        with self.assertRaises(ValueError):
            s.shorten("https://example.com/x", alias="ab")  # too short
        with self.assertRaises(ValueError):
            s.shorten("https://example.com/x", alias="bad space")

    def test_alias_conflict(self):
        s = URLShortener()
        s.shorten("https://example.com/a", alias="sameone")
        with self.assertRaises(ValueError):
            s.shorten("https://example.com/b", alias="sameone")

    def test_long_url_already_shortened_alias_mismatch(self):
        s = URLShortener()
        s.shorten("https://example.com/a")  # gets "1"
        with self.assertRaises(ValueError):
            s.shorten("https://example.com/a", alias="custom123")

class TestShortenerLevel3(unittest.TestCase):
    def test_click_tracking(self):
        s = URLShortener()
        code = s.shorten("https://example.com/a")
        self.assertEqual(s.clicks(code), 0)
        self.assertTrue(s.record_click(code))
        self.assertTrue(s.record_click(code))
        self.assertEqual(s.clicks(code), 2)

        self.assertFalse(s.record_click("missing"))
        self.assertEqual(s.clicks("missing"), 0)

class TestShortenerLevel4(unittest.TestCase):
    def test_dump_load(self):
        s = URLShortener(domain="https://sho.rt/")
        a = s.shorten("https://example.com/a")
        b = s.shorten("https://example.com/b", alias="bee")
        s.record_click(a)
        s.record_click(a)
        s.record_click("missing")

        dumped = s.dump()
        obj = json.loads(dumped)
        self.assertIn("domain", obj)
        self.assertIn("counter", obj)

        t = URLShortener()
        t.shorten("https://junk.example")  # ensure load replaces
        t.load(dumped)

        self.assertEqual(t.expand(a), "https://example.com/a")
        self.assertEqual(t.expand(b), "https://example.com/b")
        self.assertEqual(t.clicks(a), 2)
        self.assertEqual(t.short_url("bee"), "https://sho.rt/bee")

if __name__ == "__main__":
    unittest.main()
