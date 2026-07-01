from __future__ import annotations

from Node import Node

# Week 7 Assignment -- Middle Nodes, Direction, and Loops in a Doubly
# Linked List
#
# This file has 7 method stubs marked with pass. Your job is to implement
# each one. __init__, add, get_count, close_loop, and has_loop are already
# complete -- do not change them.
#
# The stubs fall into three groups:
#   1. get_middle_by_count, get_middle_two_cursor -- find the middle node
#      two different ways.
#   2. which_direction, is_unidirectional -- inspect whether a list's
#      links only go one way.
#   3. has_discontinuity, has_infinite_loop, has_loop_instant -- detect
#      broken or looping pointers.
#
# main() below builds several deliberately unusual fixtures (a one-
# directional chain, a chain with a broken link, a chain that loops back
# on itself) by reaching into Node objects directly with set_next/
# set_prev. Ordinary code should never build a DoubleLinkedList that way;
# it is done here only so the stubs below have something interesting to
# detect.


class DoubleLinkedList:

    def __init__(self):
        # An empty list has no head, no tail, and a count of zero.
        self._head = None
        self._tail = None
        self._count = 0

    def add(self, payload):
        new_node = Node(payload)
        if self._head is None:
            # The list is empty. The new node becomes both head and tail.
            self._head = new_node
            self._tail = new_node
        else:
            # Link the new node in both directions: it points back at the
            # current tail, and the current tail points forward at it.
            new_node.set_prev(self._tail)
            self._tail.set_next(new_node)
            self._tail = new_node
        self._count += 1

    def get_count(self) -> int:
        return self._count

    def close_loop(self) -> None:
        """Link the tail's next pointer back to the head, turning this
        chain into a cycle. Used to build fixtures for has_loop and
        has_loop_instant; not part of normal list-building.
        """
        if self._tail is not None:
            self._tail.set_next(self._head)
            self._has_loop = True

    def has_loop(self) -> bool:
        """Already implemented -- read this before writing has_loop_instant.

        Classic tortoise-and-hare cycle detection, using only next
        pointers (this works even on a one-directional chain where prev
        is never set). A slow cursor advances one node per step; a fast
        cursor advances two. If the chain loops back on itself, the fast
        cursor eventually laps the slow cursor and they land on the same
        node. If the chain terminates normally, the fast cursor reaches a
        node with no next before that ever happens.
        """
        result = False
        if self._head is not None:
            slow = self._head
            fast = self._head
            while (
                fast.get_next() is not None
                and fast.get_next().get_next() is not None
                and not result
            ):
                slow = slow.get_next()
                fast = fast.get_next().get_next()
                result = slow is fast
        return result

    def get_middle_by_count(self):
        """Return the payload of the middle node, using the stored count.

        self._count is already maintained by add (incremented on every
        call), so no traversal is needed to learn how many nodes are in
        the list. The middle index is self._count // 2 -- walk that many
        hops forward from self._head and return the payload found there.

        Example:
            list: Howard <-> Jarvis <-> Morse <-> Loyola <-> Granville
            count = 5, so the target index is 5 // 2 = 2
            get_middle_by_count() -> "Morse"

            list: Howard <-> Jarvis <-> Morse <-> Loyola
            count = 4, so the target index is 4 // 2 = 2 (the "upper" middle)
            get_middle_by_count() -> "Morse"

            on an empty list -> None

        Why this method needs only one traversal.
        Without a stored count, finding the middle takes two passes: one
        to count the nodes, one to walk to the middle. Because _count is
        already updated on every add, the counting pass is gone -- the
        division becomes a single field lookup, and the only traversal
        left is the count // 2 hops to reach the middle itself.

        Your method must have exactly one return statement, at the very
        end. Initialize result = None. Only walk the cursor and assign
        result when self._head is not None -- an empty list has no
        middle to find.
        """
        pass

    def get_middle_two_cursor(self):
        """Return the payload of the middle node using two cursors -- one
        slow, one fast -- without reading self._count at all.

        Start both cursors at self._head. On each iteration, advance the
        slow cursor one node (get_next()) and the fast cursor two nodes
        (get_next().get_next()). Stop as soon as the fast cursor cannot
        advance two more nodes -- that is, fast is None or fast.get_next()
        is None. When the loop ends, the slow cursor is on the middle node.

        Example (same lists as get_middle_by_count -- both methods must
        agree on every list):
            list: Howard <-> Jarvis <-> Morse <-> Loyola <-> Granville
            get_middle_two_cursor() -> "Morse"

            list: Howard <-> Jarvis <-> Morse <-> Loyola
            get_middle_two_cursor() -> "Morse"

            on an empty list -> None

        Why this is the "staircase" method from class.
        The fast cursor covers two nodes for every one the slow cursor
        covers, so by the time fast runs out of nodes, slow has covered
        half the distance -- one pass, with no separate counting step and
        no dependence on a maintained _count field.

        Your method must have exactly one return statement, at the very
        end. Initialize result = None. Only move the cursors and assign
        result when self._head is not None.
        """
        pass

    def which_direction(self) -> int:
        """Return 1 if this list's links only go forward (every _prev is
        None), -1 if they only go backward (every _next is None), or 0
        if the list is fully bidirectional (or empty).

        A normal list built through add() links every node in both
        directions. But a DoubleLinkedList can also be built by chaining
        Node objects with only set_next calls (a one-directional, forward
        -only chain) or only set_prev calls (a one-directional, backward
        -only chain) -- see _build_one_directional in main() below.

        Because a forward-only chain has no working prev pointers, you
        cannot discover its full length by walking backward from the
        tail. Likewise a backward-only chain has no working next
        pointers, so you cannot discover its full length by walking
        forward from the head. self._count -- set directly by whatever
        built the fixture -- is what lets you tell "this direction reached
        every node" apart from "this direction gave up after one node."

        Algorithm:
            1. Starting at self._head, follow get_next() as far as
               possible, counting nodes reached (forward_reach).
            2. Starting at self._tail, follow get_prev() as far as
               possible, counting nodes reached (backward_reach).
            3. If forward_reach == self._count and backward_reach does
               not, this list is forward-only: return 1.
            4. If backward_reach == self._count and forward_reach does
               not, this list is backward-only: return -1.
            5. Otherwise (both reach every node, or the list is empty),
               return 0.

        Example:
            Howard <-> Jarvis <-> Morse (built with add)   -> 0
            Howard --> Jarvis --> Morse (next pointers only) -> 1
            Howard <-- Jarvis <-- Morse (prev pointers only) -> -1
            an empty list                                    -> 0

        Your method must have exactly one return statement, at the very
        end. Initialize result = 0 and only change it inside the
        if self._head is not None: block.
        """
        pass

    def is_unidirectional(self) -> bool:
        """Return True if this list's links only go one way -- forward
        only or backward only -- and False if it is fully bidirectional
        (or empty).

        Delegate entirely to which_direction: a list is one-directional
        exactly when which_direction() is not 0. Do not write a second
        traversal here -- which_direction already did the work, the same
        way count() delegated to index_of_all() in week 6 instead of
        scanning the list a second time.

        Example:
            Howard <-> Jarvis <-> Morse (built with add)     -> False
            Howard --> Jarvis --> Morse (next pointers only) -> True
            Howard <-- Jarvis <-- Morse (prev pointers only) -> True
            an empty list                                     -> False

        Your method must have exactly one return statement, at the very
        end. The entire body is one line:
        return self.which_direction() != 0.
        """
        pass

    def has_discontinuity(self) -> bool:
        """Return True if some node in the middle of this list is missing
        a pointer that a properly linked node should have -- for example,
        one node's _prev is None even though it is not the head.

        This is different from is_unidirectional: a one-directional chain
        is missing the same pointer on every node, on purpose. A
        discontinuity is a broken node in what is otherwise meant to be a
        normal, fully-linked chain -- the kind of bug that shows up if a
        pointer update is missed during an insert or remove.

        Walk the list from self._head using get_next(). For every node
        that is not self._head, its get_prev() must not be None. For
        every node that is not self._tail, its get_next() must not be
        None. If either check fails anywhere, the list has a
        discontinuity.

        Example:
            Howard <-> Jarvis <-> Morse, fully linked        -> False
            the same list, with Jarvis.set_prev(None) called -> True
            an empty list                                    -> False

        Your method must have exactly one return statement, at the very
        end. Initialize result = False and build the while condition
        around it (while cursor is not None and not result) so the loop
        stops as soon as a broken node is found.
        """
        pass

    def has_infinite_loop(self) -> bool:
        """Return True if this doubly linked list forms one continuous
        loop -- with no true starting or ending point -- rather than
        terminating with None at both ends.

        Contract:
            - Return True if the list is fully circular: there is no node
              whose _prev is None and no node whose _next is None.
            - Return False for a normal, properly-terminated list.
            - Return False for an empty list.

        Example:
            Howard <-> Jarvis <-> Morse, normally terminated  -> False
            the same three nodes, with Morse linked forward to
            Howard and Howard linked backward to Morse         -> True
            an empty list                                      -> False

        Be careful: a loop of the kind this method checks for has no None
        anywhere to stop at. A traversal that keeps calling get_next() (or
        get_prev()) until it finds None will never finish on a list like
        this. Whatever approach you take, make sure it is guaranteed to
        terminate.

        Your method must have exactly one return statement, at the very
        end.
        """
        pass

    def has_loop_instant(self) -> bool:
        """Return the same answer as has_loop, but in O(1) -- no
        traversal at all.

        has_loop above walks the chain with two cursors every time it is
        called; the cost grows with the length of the loop. Instead,
        track whether a loop exists at the moment it is created -- the
        same idea as _count, which is updated the moment a node is added
        rather than counted on demand.

        Two steps:
            1. Add one more field to __init__: self._has_loop = False.
               (Look at close_loop above -- it already assumes this field
               exists and sets it to True when it links the tail back to
               the head. Without the line you add to __init__, calling
               has_loop_instant on a list that was never looped will
               crash with an AttributeError -- that crash is telling you
               the field is missing.)
            2. Make this method a single field lookup: return
               self._has_loop.

        Your method must have exactly one return statement, at the very
        end. The entire body is one line: return self._has_loop.
        """
        pass


def _build_one_directional(names: list, use_next: bool) -> DoubleLinkedList:
    """Build a DoubleLinkedList whose nodes are chained in only one
    direction -- only set_next calls if use_next is True, only set_prev
    calls otherwise. This bypasses add() on purpose: add() always links
    both directions, so it cannot produce the fixtures which_direction
    and is_unidirectional are meant to detect.
    """
    nodes = [Node(name) for name in names]
    for i in range(len(nodes) - 1):
        if use_next:
            nodes[i].set_next(nodes[i + 1])
        else:
            nodes[i + 1].set_prev(nodes[i])
    fixture = DoubleLinkedList()
    fixture._head = nodes[0]
    fixture._tail = nodes[-1]
    fixture._count = len(nodes)
    return fixture


def main():
    stations = ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]

    odd = DoubleLinkedList()
    for name in stations:
        odd.add(name)

    even = DoubleLinkedList()
    for name in stations[:4]:
        even.add(name)

    empty = DoubleLinkedList()

    print(odd.get_middle_by_count())  # expected: Morse
    print(odd.get_middle_two_cursor())  # expected: Morse
    print(even.get_middle_by_count())  # expected: Morse
    print(even.get_middle_two_cursor())  # expected: Morse
    print(empty.get_middle_by_count())  # expected: None
    print(empty.get_middle_two_cursor())  # expected: None

    forward_only = _build_one_directional(stations[:3], use_next=True)
    backward_only = _build_one_directional(stations[:3], use_next=False)

    print(odd.which_direction())  # expected: 0
    print(forward_only.which_direction())  # expected: 1
    print(backward_only.which_direction())  # expected: -1
    print(odd.is_unidirectional())  # expected: False
    print(forward_only.is_unidirectional())  # expected: True
    print(backward_only.is_unidirectional())  # expected: True

    broken = DoubleLinkedList()
    for name in stations[:3]:
        broken.add(name)
    # Break the link on purpose: Jarvis (the middle node) loses its prev
    # pointer, simulating pointer corruption, to test has_discontinuity.
    broken._head.get_next().set_prev(None)

    print(odd.has_discontinuity())  # expected: False
    print(broken.has_discontinuity())  # expected: True

    circular = DoubleLinkedList()
    for name in stations[:3]:
        circular.add(name)
    # Wrap the ends together so the list has no true head or tail
    # terminus, to test has_infinite_loop.
    circular._tail.set_next(circular._head)
    circular._head.set_prev(circular._tail)

    print(odd.has_infinite_loop())  # expected: False
    print(circular.has_infinite_loop())  # expected: True

    looped = DoubleLinkedList()
    for name in stations[:3]:
        looped.add(name)
    looped.close_loop()

    print(odd.has_loop())  # expected: False
    print(looped.has_loop())  # expected: True
    print(odd.has_loop_instant())  # expected: False
    print(looped.has_loop_instant())  # expected: True


if __name__ == "__main__":
    main()
