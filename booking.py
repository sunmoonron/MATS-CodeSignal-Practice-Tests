from __future__ import annotations
import json

class BookingSystem:
    """
    You manage events with a fixed capacity and a waitlist.
    
    Level 1

    create_event(name, capacity) -> bool
        returns False if event already exists
    book(name, user) -> str
        returns:
        "NO_EVENT" if event doesn’t exist
        "ALREADY_BOOKED" if user already confirmed or waitlisted
        "CONFIRMED" if capacity available
        "WAITLIST" otherwise
    status(name, user) -> str | None
        returns "CONFIRMED", "WAITLIST", or None (including if no event)
    
    Level 2

    cancel(name, user) -> bool
        returns False if no event or user not booked
        if a confirmed user cancels and there’s a waitlist, promote the earliest waitlisted user to confirmed
    
    Level 3

    confirmed(name) -> list[str] in confirmation order
    waitlisted(name) -> list[str] in waitlist order
    availability(name) -> int | None
        remaining confirmed slots
        None if no event

    Level 4
    
    dump() -> str JSON string capturing events, capacities, and ordering
    load(json_str) -> None replace all state
    """
    def __init__(self):
        raise NotImplementedError

    def create_event(self, name, capacity) -> bool:
        raise NotImplementedError

    def book(self, name, user) -> str:
        raise NotImplementedError

    def status(self, name, user):
        raise NotImplementedError

    def cancel(self, name, user) -> bool:
        raise NotImplementedError

    def confirmed(self, name):
        raise NotImplementedError

    def waitlisted(self, name):
        raise NotImplementedError

    def availability(self, name):
        raise NotImplementedError

    def dump(self) -> str:
        raise NotImplementedError

    def load(self, json_str) -> None:
        raise NotImplementedError
