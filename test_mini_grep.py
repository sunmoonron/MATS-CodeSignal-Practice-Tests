import unittest
import tempfile
from pathlib import Path
import io

from mini_grep import main, run

class TestMiniGrepBasic(unittest.TestCase):
    def test_substring_matches(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("Hello\nworld\nHELLO\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run("Hello", str(p), ignore_case=False, regex=False, count=False, line_numbers=False, stdout=out, stderr=err)
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "Hello\n")

    def test_ignore_case(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("Hello\nworld\nHELLO\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run("hello", str(p), ignore_case=True, regex=False, count=False, line_numbers=False, stdout=out, stderr=err)
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "Hello\nHELLO\n")

    def test_no_matches_exit_1(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("abc\ndef\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run("zzz", str(p), ignore_case=False, regex=False, count=False, line_numbers=False, stdout=out, stderr=err)
            self.assertEqual(code, 1)
            self.assertEqual(out.getvalue(), "")

class TestMiniGrepOptions(unittest.TestCase):
    def test_count(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("a\nax\nb\nax\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run("ax", str(p), ignore_case=False, regex=False, count=True, line_numbers=False, stdout=out, stderr=err)
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue().strip(), "2")

    def test_line_numbers(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("one\ntwo\nthree\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run("t", str(p), ignore_case=False, regex=False, count=False, line_numbers=True, stdout=out, stderr=err)
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "2:two\n3:three\n")

    def test_regex(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "f.txt"
            p.write_text("cat\ncot\ncut\n", encoding="utf-8")

            out = io.StringIO()
            err = io.StringIO()
            code = run(r"c.t", str(p), ignore_case=False, regex=True, count=False, line_numbers=False, stdout=out, stderr=err)
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "cat\ncot\ncut\n")

if __name__ == "__main__":
    unittest.main()
