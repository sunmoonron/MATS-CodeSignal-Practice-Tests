from __future__ import annotations
import re
import html

def render_inline(text: str) -> str:
    """
    Inline features (apply on already-escaped text except code spans):
      - `code` -> <code>code</code> (code contents should be HTML-escaped)
      - **bold** -> <strong>bold</strong>
      - *italic* -> <em>italic</em>
      - [text](url) -> <a href="url">text</a>

    Keep it simple; nesting doesn't need to be perfect.
    """
    raise NotImplementedError

def markdown_to_html(md: str) -> str:
    """
    Block features:
      - Headings: '# ' -> h1, '## ' -> h2 ... up to '###### '
      - Unordered lists: consecutive lines starting with '- ' become <ul><li>...</li>...</ul>
      - Paragraphs: consecutive non-empty lines become one <p> ... </p> (join with spaces)

    Output blocks separated by '\n' exactly as tests expect.
    """
    raise NotImplementedError
