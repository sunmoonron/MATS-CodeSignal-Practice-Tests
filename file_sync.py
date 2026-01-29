from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import shutil
import os

@dataclass(frozen=True)
class Diff:
    added: set[str]      # present in src, missing in dst
    modified: set[str]   # present in both, content differs
    deleted: set[str]    # present in dst, missing in src

def file_hash(path: Path) -> str:
    """Return hex sha256 of file bytes."""
    raise NotImplementedError

def list_files(root: Path) -> set[str]:
    """
    Return relative file paths (posix-style) for all files under root.
    Example: {"a.txt", "sub/b.txt"}
    """
    raise NotImplementedError

def diff_dirs(src: str | Path, dst: str | Path) -> Diff:
    """Compute added/modified/deleted comparing src -> dst."""
    raise NotImplementedError

def sync_dirs(src: str | Path, dst: str | Path, *, delete_extra: bool = False) -> Diff:
    """
    Copy added/modified files from src into dst, creating directories as needed.
    If delete_extra=True, delete files in dst that aren't in src.
    Return the Diff that was applied.
    """
    raise NotImplementedError
