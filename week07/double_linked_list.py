from __future__ import annotations

from typing import Generic, TypeVar

from Node import Node

# Same type parameter idea as Node[T]: a DoubleLinkedList[str] holds
# Node[str] objects, a DoubleLinkedList[int] holds Node[int] objects, and
# so on, without rewriting this class.
T = TypeVar("T")

# Week 7 Assignment -- O(1) Middle Nodes, Continuity, and Loops in a Doubly
# Linked List
#
# This file has 5 method stubs marked with pass. Your job is to implement
# each one. __init__, add, __str__, get_middle_slow_fast, and has_loop are
# already complete -- do not change them, except where a stub's docstring
# tells you that you need to extend __init__ or add with new bookkeeping.
#
# The stubs:
#   1. get_middle_node         -- the middle node, in O(1)
#   2. is_continuous            -- detect a broken link in a bidirectional list
#   3. has_loop_unidirectional  -- loop detection on a forward-only list, O(1)
#   4. has_loop_bidirectional   -- loop detection on a bidirectional ring, O(1)
#   5. reverse                  -- reverse a forward-only list, in O(n)
#
# main() below builds several deliberately unusual fixtures (a broken link,
# a forward-only loop, a bidirectional ring) by reaching into Node objects
# directly with set_next/set_prev. Ordinary code should never build a
# DoubleLinkedList that way; it is done here only so the stubs above have
# something interesting to detect.


class DoubleLinkedList(Generic[T]):
    """
    A list of Node objects that can be wired three different ways,
    chosen at construction time by directionality: fully bidirectional
    (every node's _next and _prev both set), forward-only (only _next
    is ever set), or backward-only (only _prev is ever set). add() and
    __str__ both branch on directionality so the same class can build
    and display all three shapes correctly.
    """

    # The three ways a DoubleLinkedList can be wired. Stored in
    # self.directionality, then read by add() (to decide which pointers
    # a new node gets) and __str__ (to decide which arrow template to
    # print). Defined here, before __init__, because __init__'s default
    # argument below needs them to already exist when this class body
    # runs.
    _BIDIRECTIONAL = 0
    _FORWARD_ONLY = 1
    _BACKWARD_ONLY = -1

    def __init__(self, directionality: int = _BIDIRECTIONAL) -> None:
        # An empty list has no head, no tail, and no nodes yet.
        self._head: Node[T] | None = None
        self._tail: Node[T] | None = None
        self.count_of_nodes: int = 0
        # Fixed for the life of this list -- add() reads it on every
        # call, but nothing here ever reassigns it after construction.
        self.directionality: int = directionality

    def add(self, payload: T) -> None:
        """Append a new node holding payload to the end of the list,
        linking it according to self.directionality, and bump
        count_of_nodes by one.
        """
        new_node: Node[T] = Node(payload)
        if self._head is None:
            # The list is empty. The new node becomes both head and tail.
            self._head = new_node
            self._tail = new_node
        else:
            # Which pointers get linked depends on directionality: a
            # bidirectional list links both, a forward-only list links
            # only _next, a backward-only list links only _prev. A
            # pointer that is skipped here is never set by anyone else
            # later -- it stays None for the life of the node.
            if self.directionality != self._FORWARD_ONLY:
                new_node.set_prev(self._tail)
            if self.directionality != self._BACKWARD_ONLY:
                self._tail.set_next(new_node)
            # Whichever pointers got linked above, the newest node is
            # always the new tail.
            self._tail = new_node
        self.count_of_nodes += 1

    # String pieces used to assemble __str__'s three display formats: the
    # arrow "caps" at the open end of a list, and the separator printed
    # between two adjacent payloads. Used nowhere but __str__ below.
    _EMPTY = "EMPTY"
    _CAP_LEFT = "<-- "
    _CAP_RIGHT = " -->"
    _LINK_BOTH = " <---> "
    _LINK_NEXT = " --> "
    _LINK_PREV = " <-- "

    def __str__(self) -> str:
        """Return a printable view of the list: EMPTY if there are no
        nodes, otherwise every payload in head-to-tail order, wrapped
        in the arrow template that matches this list's directionality.
        """
        if self._head is None:
            return self._EMPTY

        payloads: list[str] = []
        if self.directionality == self._BACKWARD_ONLY:
            # No _next pointers exist in this mode, so the only way to
            # reach every node is to start at the tail and follow _prev
            # back toward the head.
            cursor: Node[T] | None = self._tail
            while cursor is not None:
                payloads.append(str(cursor.get_payload()))
                cursor = cursor.get_prev()
            # The walk above collects payloads tail-to-head; reverse so
            # the printed string still reads head-to-tail, left to right.
            payloads.reverse()
        else:
            # Bidirectional and forward-only lists both have working
            # _next pointers, so a normal forward walk from the head
            # already visits the nodes in head-to-tail order.
            cursor = self._head
            while cursor is not None:
                payloads.append(str(cursor.get_payload()))
                cursor = cursor.get_next()

        # Wrap the collected payloads in whichever arrow template
        # matches this list's directionality.
        if self.directionality == self._BIDIRECTIONAL:
            result = self._CAP_LEFT + self._LINK_BOTH.join(payloads) + self._CAP_RIGHT
        elif self.directionality == self._FORWARD_ONLY:
            result = self._LINK_NEXT.join(payloads) + self._CAP_RIGHT
        else:
            result = self._CAP_LEFT + self._LINK_PREV.join(payloads)
        return result

    def get_middle_slow_fast(self) -> T | None:
        """Already implemented -- read this before writing get_middle_node.

        The slow/fast ("tortoise and hare") technique from the June 30
        session: a slow cursor advances one node at a time while a fast
        cursor advances two. By the time the fast cursor cannot advance
        two more nodes, the slow cursor is standing on the middle node.
        This finds the middle correctly on any list, without reading
        count_of_nodes at all -- but it is O(n): every call re-walks the
        list from the head.
        """
        result: T | None = None
        if self._head is not None:
            slow: Node[T] = self._head
            fast: Node[T] = self._head
            # Stop the instant fast cannot take two more hops. Checking
            # get_next() before calling .get_next() on its result is
            # what keeps this from ever calling a method on None.
            while (
                fast.get_next() is not None
                and fast.get_next().get_next() is not None
            ):
                slow = slow.get_next()
                fast = fast.get_next().get_next()
            result = slow.get_payload()
        return result

    def has_loop(self) -> bool:
        """Already implemented -- read this before writing
        has_loop_unidirectional and has_loop_bidirectional.

        Classic slow/fast cycle detection, using only _next pointers
        (this works even on a forward-only list where _prev is never
        set, and even on a fully wrapped bidirectional ring, since a
        ring is still a cycle when followed through _next). A slow
        cursor advances one node per step; a fast cursor advances two.
        If the chain loops back on itself, the fast cursor eventually
        laps the slow cursor and they land on the same node. If the
        chain terminates normally, the fast cursor reaches a node with
        no _next before that ever happens. Correct on any list -- but
        O(n), and the cost is paid on every single call.
        """
        result: bool = False
        if self._head is not None:
            slow: Node[T] = self._head
            fast: Node[T] = self._head
            while (
                fast.get_next() is not None
                and fast.get_next().get_next() is not None
                and not result
            ):
                slow = slow.get_next()
                fast = fast.get_next().get_next()
                # `is`, not `==`: this asks whether the two cursors have
                # landed on the exact same Node object, not on two
                # different nodes that happen to hold equal payloads.
                result = slow is fast
        return result

    def get_middle_node(self) -> T | None:
        """Return the payload stored in the middle node of this list --
        the same node get_middle_slow_fast finds -- but in O(1).

        O(1) here means exactly that: no traversal, no cursor, no loop
        of any kind inside this method when it is called. Whatever
        answer this method returns has to already exist somewhere by
        the time it's asked for.

        Contract:
        - Return None if the list is empty.
        - Otherwise, return the same payload get_middle_slow_fast(self)
          would return for the same list.
        - The body of this method must not walk the list.

        You will likely need to add at least one more field to
        __init__, and keep it updated inside add() every time a node
        is appended -- the same idea behind count_of_nodes itself.
        Think about how the identity of the middle node changes, if at
        all, each time a single new node is appended to the end.

        One return statement, at the very end.
        """
        pass

    def is_continuous(self) -> bool:
        """Return True if this bidirectional list (directionality ==
        _BIDIRECTIONAL) is fully and correctly linked in both
        directions, and False if a break has crept in anywhere.

        This is different from asking whether a list is unidirectional
        by design: a forward-only or backward-only list is missing the
        same pointer on every node, on purpose. A discontinuity is a
        single broken link in a list that is supposed to be fully
        bidirectional -- the kind of bug that shows up if a pointer
        update is missed during an insert or remove.

        Contract:
        - Assume this is only ever called on a bidirectional list.
        - Return True for an empty list and for a single-node list.
        - Walk the list and check each node's pointers against what a
          properly linked node in that position should have.

        One return statement, at the very end.
        """
        pass

    def has_loop_unidirectional(self) -> bool:
        """Return the same answer has_loop would return for this
        forward-only (directionality == _FORWARD_ONLY) list, but in
        O(1) -- no cursor race, no traversal at all.

        Contract:
        - Return False for a normal, properly terminated forward-only
          list.
        - Return False for an empty list.
        - Return True if the list loops back on itself.

        Think about what a properly maintained self._tail should look
        like at the moment this method is called, and what it would
        mean if it did not look that way.

        One return statement, at the very end.
        """
        pass

    def has_loop_bidirectional(self) -> bool:
        """Return True if this bidirectional list has been wired into
        a closed ring -- no node's _next or _prev pointer is ever None
        -- rather than terminating normally at both ends. Answer in
        O(1): no cursor race, no traversal at all.

        A bidirectional list gives you twice the information a
        forward-only list does at each node. Think about what that
        buys you at the two ends of the list specifically.

        Contract:
        - Return False for a normal, properly terminated bidirectional
          list.
        - Return False for an empty list.
        - Return True if the list is a closed ring.

        One return statement, at the very end.
        """
        pass

    def reverse(self) -> None:
        """Reverse this forward-only (directionality == _FORWARD_ONLY)
        list in place, so that traversing it from the new head to the
        new tail visits every node in the opposite order.

        It is tempting to think this is as simple as swapping
        self._head and self._tail. It is not: swapping the two fields
        changes which node you call the head, but every node's _next
        pointer still points the same physical way it did before, so
        walking from the "new" head with get_next() dead-ends
        immediately. The links themselves have to be rebuilt, one node
        at a time.

        Contract:
        - Must run in O(n).
        - directionality stays _FORWARD_ONLY when you are done.
        - An empty list or a single-node list is already its own
          reverse -- handle those without crashing.

        One return statement, at the very end.
        """
        pass


def main() -> None:
    stations: list[str] = ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]

    # A normal bidirectional list -- directionality defaults to
    # _BIDIRECTIONAL, so add() links both _next and _prev on every node.
    bidirectional: DoubleLinkedList[str] = DoubleLinkedList()
    for name in stations:
        bidirectional.add(name)
    print(bidirectional)
    # expected: <-- Howard <---> Jarvis <---> Morse <---> Loyola <---> Granville -->

    # A forward-only list: only _next pointers are ever set.
    forward_only: DoubleLinkedList[str] = DoubleLinkedList(DoubleLinkedList._FORWARD_ONLY)
    for name in stations[:3]:
        forward_only.add(name)
    print(forward_only)
    # expected: Howard --> Jarvis --> Morse -->

    # A backward-only list: only _prev pointers are ever set.
    backward_only: DoubleLinkedList[str] = DoubleLinkedList(DoubleLinkedList._BACKWARD_ONLY)
    for name in stations[:3]:
        backward_only.add(name)
    print(backward_only)
    # expected: <-- Howard <-- Jarvis <-- Morse

    empty: DoubleLinkedList[str] = DoubleLinkedList()
    print(empty)  # expected: EMPTY

    # get_middle_node must return the same payload as the already-working
    # O(n) reference implementation, for the same list.
    print(bidirectional.get_middle_slow_fast())  # expected: Morse
    print(bidirectional.get_middle_node())  # expected: Morse

    broken: DoubleLinkedList[str] = DoubleLinkedList()
    for name in stations[:3]:
        broken.add(name)
    # Break the link on purpose: Jarvis (the middle node) loses its prev
    # pointer, simulating pointer corruption, to test is_continuous.
    broken._head.get_next().set_prev(None)

    print(bidirectional.is_continuous())  # expected: True
    print(broken.is_continuous())  # expected: False

    looped_forward: DoubleLinkedList[str] = DoubleLinkedList(DoubleLinkedList._FORWARD_ONLY)
    for name in stations[:3]:
        looped_forward.add(name)
    # Wire the tail back into the chain, to test loop detection.
    looped_forward._tail.set_next(looped_forward._head)

    print(forward_only.has_loop())  # expected: False
    print(looped_forward.has_loop())  # expected: True
    print(forward_only.has_loop_unidirectional())  # expected: False
    print(looped_forward.has_loop_unidirectional())  # expected: True

    ring: DoubleLinkedList[str] = DoubleLinkedList()
    for name in stations[:3]:
        ring.add(name)
    # Wrap both ends together so the list has no true head or tail
    # terminus, to test has_loop_bidirectional.
    ring._tail.set_next(ring._head)
    ring._head.set_prev(ring._tail)

    print(bidirectional.has_loop_bidirectional())  # expected: False
    print(ring.has_loop_bidirectional())  # expected: True

    # reverse() should flip the print order without changing directionality.
    reversible: DoubleLinkedList[str] = DoubleLinkedList(DoubleLinkedList._FORWARD_ONLY)
    for name in stations[:3]:
        reversible.add(name)
    print(reversible)  # expected: Howard --> Jarvis --> Morse -->
    reversible.reverse()
    print(reversible)  # expected: Morse --> Jarvis --> Howard -->


if __name__ == "__main__":
    main()
