from __future__ import annotations
from typing import TypeVar, Generic

# Create a type variable that can be anything.
# Says who. Says I.

T = TypeVar('T')


class Node(Generic[T]):
    """
    A doubly-linked node that holds a single value (its payload) and two
    optional references: one to the node ahead of it (_next) and one to
    the node behind it (_prev).

    Generic[T] means Node can hold any type -- Node[int], Node[str],
    Node[Station], etc. -- without rewriting this class.

    Typical use: build a doubly-linked list by chaining nodes together
    through their _next and _prev links.
    """

    def __init__(self, payload: T):
        """
        Create a new Node that stores the given payload.

        Both _next and _prev start as None because a freshly created node
        is not yet connected to anything.

        Parameters
        ----------
        payload : T
            The value this node will hold.
        """
        self._payload: T = payload
        self._next: Node | None = None
        self._prev: Node | None = None

    # ------------------------------------------------------------------
    # _next methods
    # ------------------------------------------------------------------

    def has_next(self) -> bool:
        """Return True if this node is linked to a successor, False otherwise."""
        return self._next is not None

    def get_next(self) -> Node | None:
        """Return the node that follows this one, or None if there is none."""
        return self._next

    def set_next(self, node: Node | None) -> None:
        """
        Point this node's _next reference at another node (or clear it).

        Parameters
        ----------
        node : Node | None
            The node to link as the successor, or None to unlink.
        """
        self._next = node

    # ------------------------------------------------------------------
    # _prev methods
    # ------------------------------------------------------------------

    def has_prev(self) -> bool:
        """Return True if this node is linked to a predecessor, False otherwise."""
        return self._prev is not None

    def get_prev(self) -> Node | None:
        """Return the node that precedes this one, or None if there is none."""
        return self._prev

    def set_prev(self, node: Node | None) -> None:
        """
        Point this node's _prev reference at another node (or clear it).

        Parameters
        ----------
        node : Node | None
            The node to link as the predecessor, or None to unlink.
        """
        self._prev = node

    # ------------------------------------------------------------------
    # payload accessor (read-only by design -- payloads do not change)
    # ------------------------------------------------------------------

    def get_payload(self) -> T:
        """Return the value stored in this node."""
        return self._payload

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Return a human-readable description of this node.

        Shows the payload and whether _prev and _next links exist, using
        arrows to hint at the chain: <-- [payload] --> or variations.

        Examples
        --------
        A standalone node holding 42:     [ 42 ]
        A node with a successor:          [ 42 ] -->
        A node with both links:        <-- [ 42 ] -->
        """
        left  = "<--" if self.has_prev() else "   "
        right = "-->" if self.has_next() else "   "
        return f"{left} [ {self._payload} ] {right}"
