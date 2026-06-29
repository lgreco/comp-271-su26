from __future__ import annotations
from typing import TypeVar, Generic

# Create a type variable that can be anything. 
# Says who. Says I.

T = TypeVar('T')



class Node(Generic[T]):

    def __init__(self, payload: T):
        self._payload: T = payload
        self._next: Node | None = None
        self._prev: Node | None = None

    def __str__(self) -> str:
        return "a string"

    # Write set/get for _next and _prev
    # Write a get for _payload

    def get_payload(self) -> T:
        return self._payload
