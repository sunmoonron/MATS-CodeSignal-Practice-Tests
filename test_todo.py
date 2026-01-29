import unittest
import json
from todo import TodoManager

class TestTodoManagerLevel1(unittest.TestCase):
    def test_add_get_delete(self):
        t = TodoManager()
        a = t.add("write", now=10.0)
        b = t.add("study", now=11.0, due_at=20.0, tags=["school", "math"])
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)

        self.assertEqual(t.get(999), None)

        task_b = t.get(b)
        self.assertEqual(task_b["id"], 2)
        self.assertEqual(task_b["title"], "study")
        self.assertEqual(task_b["created_at"], 11.0)
        self.assertEqual(task_b["due_at"], 20.0)
        self.assertEqual(task_b["done"], False)
        self.assertEqual(task_b["tags"], ["math", "school"])  # sorted

        self.assertTrue(t.delete(a))
        self.assertFalse(t.delete(a))
        self.assertIsNone(t.get(a))

class TestTodoManagerLevel2(unittest.TestCase):
    def test_complete_and_status_list(self):
        t = TodoManager()
        a = t.add("a", now=1.0)
        b = t.add("b", now=2.0)
        self.assertTrue(t.complete(a))
        self.assertTrue(t.complete(a))  # idempotent
        self.assertFalse(t.complete(999))

        open_tasks = t.list(status="open")
        done_tasks = t.list(status="done")
        all_tasks = t.list(status="all")

        self.assertEqual([x["id"] for x in open_tasks], [b])
        self.assertEqual([x["id"] for x in done_tasks], [a])
        self.assertEqual([x["id"] for x in all_tasks], [b, a])  # open first

class TestTodoManagerSorting(unittest.TestCase):
    def test_sorting_rules(self):
        t = TodoManager()
        # open tasks
        a = t.add("no due", now=1.0)                 # due None
        b = t.add("due later", now=2.0, due_at=50.0)
        c = t.add("due sooner", now=3.0, due_at=10.0)
        d = t.add("same due", now=0.5, due_at=10.0)  # earlier created_at than c
        e = t.add("done due", now=4.0, due_at=1.0)
        t.complete(e)

        ids = [x["id"] for x in t.list()]
        # open tasks first: due 10 (d then c), due 50 (b), due None (a), then done tasks (e)
        self.assertEqual(ids, [d, c, b, a, e])

class TestTodoManagerLevel3(unittest.TestCase):
    def test_tag_filter(self):
        t = TodoManager()
        a = t.add("a", now=1.0, tags=["x"])
        b = t.add("b", now=2.0, tags=["y"])
        c = t.add("c", now=3.0, tags=["x", "y"])
        ids = [x["id"] for x in t.list(tag="x")]
        self.assertEqual(ids, [a, c])

    def test_overdue_filter(self):
        t = TodoManager()
        a = t.add("due past", now=1.0, due_at=5.0)
        b = t.add("due future", now=2.0, due_at=50.0)
        c = t.add("no due", now=3.0)
        d = t.add("overdue but done", now=4.0, due_at=4.5)
        t.complete(d)

        overdue = [x["id"] for x in t.list(overdue_only=True, now=10.0)]
        self.assertEqual(overdue, [a])

class TestTodoManagerLevel4(unittest.TestCase):
    def test_dump_load_roundtrip(self):
        t = TodoManager()
        a = t.add("a", now=1.0, due_at=10.0, tags=["x"])
        b = t.add("b", now=2.0)
        t.complete(a)

        s = t.dump()
        # must be JSON string
        obj = json.loads(s)
        self.assertIsInstance(obj, dict)

        u = TodoManager()
        u.add("junk", now=0.0)
        u.load(s)

        self.assertEqual(u.get(a)["done"], True)
        self.assertEqual(u.get(a)["tags"], ["x"])
        self.assertEqual([x["id"] for x in u.list()], [b, a])

if __name__ == "__main__":
    unittest.main()
