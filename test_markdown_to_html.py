import unittest
from textwrap import dedent
from markdown_to_html import markdown_to_html

class TestMarkdownLevel1HeadingsParagraphs(unittest.TestCase):
    def test_heading_and_paragraph(self):
        md = dedent("""\
        # Title

        Hello world.
        """)
        expected = dedent("""\
        <h1>Title</h1>
        <p>Hello world.</p>
        """).strip()
        self.assertEqual(markdown_to_html(md).strip(), expected)

class TestMarkdownInline(unittest.TestCase):
    def test_inline_formatting(self):
        md = "Hello **bold** and *ital* and `x<y` and [link](https://a.b)\n"
        out = markdown_to_html(md).strip()
        self.assertIn("<strong>bold</strong>", out)
        self.assertIn("<em>ital</em>", out)
        self.assertIn("<code>x&lt;y</code>", out)
        self.assertIn('<a href="https://a.b">link</a>', out)

class TestMarkdownLists(unittest.TestCase):
    def test_unordered_list(self):
        md = dedent("""\
        - a
        - b
        - **c**
        """)
        expected = dedent("""\
        <ul>
        <li>a</li>
        <li>b</li>
        <li><strong>c</strong></li>
        </ul>
        """).strip()
        self.assertEqual(markdown_to_html(md).strip(), expected)

    def test_list_then_paragraph(self):
        md = dedent("""\
        - a
        - b

        after list
        """)
        out = markdown_to_html(md).strip().splitlines()
        self.assertEqual(out[0], "<ul>")
        self.assertEqual(out[-1], "<p>after list</p>")

class TestMarkdownEscaping(unittest.TestCase):
    def test_escape_html_in_text(self):
        md = "2 < 3 & 5 > 4\n"
        expected = "<p>2 &lt; 3 &amp; 5 &gt; 4</p>"
        self.assertEqual(markdown_to_html(md).strip(), expected)

if __name__ == "__main__":
    unittest.main()
