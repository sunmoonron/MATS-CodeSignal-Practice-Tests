from __future__ import annotations
import json
import re

_BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(n: int) -> str:
    """
    Convert a positive integer to base62 using _BASE62_ALPHABET.
    Spec:
      - n must be >= 1
      - encode_base62(1) == "1"
      - encode_base62(10) == "a"
      - encode_base62(62) == "10"
    """
    raise NotImplementedError

class URLShortener:
    """
    In-memory URL shortener.

    Level 1:
      - shorten(long_url) -> code (base62 counter starting at 1)
      - expand(code) -> long_url or None
      - shortening same long_url twice returns same code

    Level 2:
      - shorten(long_url, alias="custom") -> "custom"
      - alias must match: [A-Za-z0-9_-]{3,32}
      - if alias already used for a DIFFERENT long_url: raise ValueError
      - if long_url already has a code and alias is different: raise ValueError

    Level 3:
      - record_click(code) increments click count (returns True if exists else False)
      - clicks(code) returns click count (0 if unknown)

    Level 4:
      - dump() -> JSON string capturing mappings, clicks, counter, domain
      - load(json_str) replaces all state
    """
    ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]{3,32}$")

    def __init__(self, domain: str = "https://sho.rt/"):
        raise NotImplementedError

    def shorten(self, long_url: str, alias: str | None = None) -> str:
        raise NotImplementedError

    def expand(self, code: str) -> str | None:
        raise NotImplementedError

    def short_url(self, code: str) -> str:
        """Return full short URL like 'https://sho.rt/<code>'."""
        raise NotImplementedError

    def record_click(self, code: str) -> bool:
        raise NotImplementedError

    def clicks(self, code: str) -> int:
        raise NotImplementedError

    def dump(self) -> str:
        raise NotImplementedError

    def load(self, json_str: str) -> None:
        raise NotImplementedError
