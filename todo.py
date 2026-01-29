from __future__ import annotations
import json

class TodoManager:
    """
    You are building an in-memory task manager.

    Each task has:
        id (int, auto-increment starting at 1)
        title (str)
        created_at (float or int timestamp, passed in)
        due_at (float/int timestamp or None)
        done (bool)
        tags (set of strings internally, but returned as a sorted list)
    
    Level 1

    add(title, now, due_at=None, tags=None) -> int
        tags is None or an iterable of strings
        returns the created task id

    get(task_id) -> dict | None
        returns a dict with keys: id,title,created_at,due_at,done,tags
        tags must be a sorted list

    delete(task_id) -> bool

    Level 2

    complete(task_id) -> bool
        returns True if task existed (even if already done), else False
    
    list(status="all") -> list[dict]
        status is "all", "open", "done"

    Level 3

    list(status="all", tag=None, overdue_only=False, now=None) -> list[dict]
        if tag is provided, return only tasks that have that tag
        if overdue_only=True, include only tasks where:
            due_at is not None
            now is provided
            due_at < now
            and task is not done

    Sorting for list(...):
        open tasks first (done=False), then done tasks
        within each group: sort by due_at ascending where None is treated as “infinite” (i.e., comes last)
        tie-breaker: created_at ascending
        final tie-breaker: id ascending

    Level 4

    dump() -> str returns a JSON string
    load(json_str) -> None replaces all state
    """
    def __init__(self):
        raise NotImplementedError

    def add(self, title, now, due_at=None, tags=None) -> int:
        raise NotImplementedError

    def get(self, task_id):
        raise NotImplementedError

    def delete(self, task_id) -> bool:
        raise NotImplementedError

    def complete(self, task_id) -> bool:
        raise NotImplementedError

    def list(self, status="all", tag=None, overdue_only=False, now=None):
        raise NotImplementedError

    def dump(self) -> str:
        raise NotImplementedError

    def load(self, json_str) -> None:
        raise NotImplementedError
