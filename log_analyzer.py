from __future__ import annotations
from dataclasses import dataclass
import shlex
import math
from collections import Counter

@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    level: str
    fields: dict[str, str]

def parse_line(line: str) -> LogEntry:
    """
    Format (tokens parsed with shlex.split):
      <timestamp> <LEVEL> key=value key=value ...
    Values may be quoted, e.g. msg="hello world"

    Example:
      2026-01-27T12:00:00Z INFO action=login user=alice ip=1.2.3.4 latency_ms=123 msg="hi there"
    """
    raise NotImplementedError

class LogAnalyzer:
    """
    Level 1:
      - ingest(lines)
      - count_levels() -> dict[level] = count

    Level 2:
      - top_values(field, n=3) -> list[(value,count)] sorted by count desc then value asc
      - most_common(field) -> value or None

    Level 3:
      - latency_percentile(p) using nearest-rank method on latency_ms field (ints)
        * ignore lines missing latency_ms or non-int
        * p is 0..100 (0 -> min, 100 -> max)

    Level 4:
      - filter(level=None, field=None, value=None) -> list[LogEntry]
        (field/value match exact string)
    """
    def __init__(self):
        raise NotImplementedError

    def ingest(self, lines: list[str]) -> None:
        raise NotImplementedError

    def count_levels(self) -> dict[str, int]:
        raise NotImplementedError

    def top_values(self, field: str, n: int = 3) -> list[tuple[str, int]]:
        raise NotImplementedError

    def most_common(self, field: str) -> str | None:
        raise NotImplementedError

    def latency_percentile(self, p: float) -> int | None:
        raise NotImplementedError

    def filter(self, level: str | None = None, field: str | None = None, value: str | None = None) -> list[LogEntry]:
        raise NotImplementedError
