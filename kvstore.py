# kvstore.py
from __future__ import annotations


class KVStore:
    """
    Implement a class KVStore in kvstore.py.
    
    Level 1: Core operations
    
    set(key, value): stores any Python value
    get(key): returns the value, or None if missing
    delete(key): deletes key; returns True if it existed, else False
    keys(): returns sorted list of current keys
    
    Level 2: TTL expiration (no external libs)
    
    Add TTL support:
    set(key, value, ttl_seconds=None, now=None):
        if ttl_seconds is not None, key expires at now + ttl_seconds
        now is a float timestamp (tests will pass it; don’t call network/time APIs)
    get(key, now=None) & keys(now=None): treat expired keys as missing
    
    Level 3: Atomic “compare and set”
    
    Add:
    compare_and_set(key, expected, new_value, now=None):
        returns True and sets to new_value iff current value == expected and key isn’t expired
        if key missing/expired, treat value as None
    
    Level 4: Export/import
    
    Add:
    dump(now=None): returns a JSON string representing all non-expired keys (use json)
    load(json_str): replaces the store with the contents (no TTL on loaded values)
    """
    def __init__(self):
        # TODO
        raise NotImplementedError

    def set(self, key, value, ttl_seconds=None, now=None):
        # TODO
        raise NotImplementedError

    def get(self, key, now=None):
        # TODO
        raise NotImplementedError

    def delete(self, key):
        # TODO
        raise NotImplementedError

    def keys(self, now=None):
        # TODO
        raise NotImplementedError

    def compare_and_set(self, key, expected, new_value, now=None):
        # TODO
        raise NotImplementedError

    def dump(self, now=None):
        # TODO
        raise NotImplementedError

    def load(self, json_str):
        # TODO
        raise NotImplementedError
