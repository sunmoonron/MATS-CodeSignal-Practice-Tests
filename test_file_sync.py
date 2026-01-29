import unittest
from pathlib import Path
import tempfile

from file_sync import diff_dirs, sync_dirs

def write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

class TestFileSync(unittest.TestCase):
    def test_diff_and_sync(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            src = Path(a)
            dst = Path(b)

            # src files
            write(src / "a.txt", "AAA")
            write(src / "sub" / "b.txt", "BBB")
            write(src / "sub" / "c.txt", "CCC")

            # dst has stale + extra
            write(dst / "a.txt", "OLD")
            write(dst / "extra.txt", "XXX")

            d = diff_dirs(src, dst)
            self.assertEqual(d.added, {"sub/b.txt", "sub/c.txt"})
            self.assertEqual(d.modified, {"a.txt"})
            self.assertEqual(d.deleted, {"extra.txt"})

            applied = sync_dirs(src, dst, delete_extra=False)
            self.assertEqual(applied.added, d.added)
            self.assertEqual(applied.modified, d.modified)
            # not deleted because delete_extra=False
            self.assertEqual(applied.deleted, set())

            self.assertEqual((dst / "a.txt").read_text(encoding="utf-8"), "AAA")
            self.assertEqual((dst / "sub" / "b.txt").read_text(encoding="utf-8"), "BBB")
            self.assertTrue((dst / "extra.txt").exists())

            applied2 = sync_dirs(src, dst, delete_extra=True)
            self.assertEqual(applied2.deleted, {"extra.txt"})
            self.assertFalse((dst / "extra.txt").exists())

    def test_empty_src_delete_extra(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            src = Path(a)
            dst = Path(b)
            (dst / "x.txt").write_text("x", encoding="utf-8")

            applied = sync_dirs(src, dst, delete_extra=True)
            self.assertEqual(applied.added, set())
            self.assertEqual(applied.modified, set())
            self.assertEqual(applied.deleted, {"x.txt"})
            self.assertFalse((dst / "x.txt").exists())

if __name__ == "__main__":
    unittest.main()
