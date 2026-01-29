import unittest
import json
from booking import BookingSystem

class TestBookingLevel1(unittest.TestCase):
    def test_create_and_book(self):
        b = BookingSystem()
        self.assertTrue(b.create_event("show", 2))
        self.assertFalse(b.create_event("show", 5))  # already exists

        self.assertEqual(b.book("missing", "a"), "NO_EVENT")
        self.assertEqual(b.book("show", "alice"), "CONFIRMED")
        self.assertEqual(b.book("show", "bob"), "CONFIRMED")
        self.assertEqual(b.book("show", "cara"), "WAITLIST")

        self.assertEqual(b.book("show", "alice"), "ALREADY_BOOKED")
        self.assertEqual(b.status("show", "alice"), "CONFIRMED")
        self.assertEqual(b.status("show", "cara"), "WAITLIST")
        self.assertIsNone(b.status("show", "nobody"))
        self.assertIsNone(b.status("missing", "alice"))

class TestBookingLevel2(unittest.TestCase):
    def test_cancel_promotes_waitlist(self):
        b = BookingSystem()
        b.create_event("talk", 1)
        self.assertEqual(b.book("talk", "a"), "CONFIRMED")
        self.assertEqual(b.book("talk", "b"), "WAITLIST")
        self.assertEqual(b.book("talk", "c"), "WAITLIST")

        # cancel waitlisted: just removed
        self.assertTrue(b.cancel("talk", "b"))
        self.assertIsNone(b.status("talk", "b"))
        self.assertEqual(b.status("talk", "a"), "CONFIRMED")
        self.assertEqual(b.status("talk", "c"), "WAITLIST")

        # cancel confirmed: promote earliest waitlisted (c)
        self.assertTrue(b.cancel("talk", "a"))
        self.assertEqual(b.status("talk", "c"), "CONFIRMED")

    def test_cancel_missing_cases(self):
        b = BookingSystem()
        self.assertFalse(b.cancel("nope", "x"))
        b.create_event("x", 0)
        self.assertFalse(b.cancel("x", "nobody"))

class TestBookingLevel3(unittest.TestCase):
    def test_confirmed_waitlisted_availability(self):
        b = BookingSystem()
        b.create_event("game", 2)
        b.book("game", "a")
        b.book("game", "b")
        b.book("game", "c")
        b.book("game", "d")

        self.assertEqual(b.confirmed("game"), ["a", "b"])
        self.assertEqual(b.waitlisted("game"), ["c", "d"])
        self.assertEqual(b.availability("game"), 0)
        self.assertIsNone(b.availability("missing"))
        self.assertEqual(b.confirmed("missing"), [])
        self.assertEqual(b.waitlisted("missing"), [])

        # cancel confirmed promotes c
        b.cancel("game", "a")
        self.assertEqual(b.confirmed("game"), ["b", "c"])
        self.assertEqual(b.waitlisted("game"), ["d"])
        self.assertEqual(b.status("game", "c"), "CONFIRMED")

class TestBookingLevel4(unittest.TestCase):
    def test_dump_load_roundtrip(self):
        b = BookingSystem()
        b.create_event("e1", 1)
        b.create_event("e2", 2)
        b.book("e1", "a")
        b.book("e1", "b")  # waitlist
        b.book("e2", "x")
        b.book("e2", "y")
        b.book("e2", "z")  # waitlist

        s = b.dump()
        obj = json.loads(s)
        self.assertIsInstance(obj, dict)

        c = BookingSystem()
        c.create_event("junk", 99)
        c.load(s)

        self.assertEqual(c.confirmed("e1"), ["a"])
        self.assertEqual(c.waitlisted("e1"), ["b"])
        self.assertEqual(c.confirmed("e2"), ["x", "y"])
        self.assertEqual(c.waitlisted("e2"), ["z"])

if __name__ == "__main__":
    unittest.main()
