from __future__ import annotations


class Node:
    """A single linked-list node. Complete -- do not modify."""

    def __init__(self, payload: str, next: Node | None = None) -> None:
        self._payload = payload
        self._next = next

    def get_payload(self) -> str:
        return self._payload

    def get_next(self) -> Node | None:
        return self._next

    def set_next(self, next: Node | None) -> None:
        self._next = next


class SimpleHash:
    """
    A hash table with separate chaining: an underlying array where every
    occupied slot holds the head of a singly linked list of Nodes. Each
    Node's payload is a person's name (a string).

    __init__ is complete. Every other method is a stub marked `pass`.
    Implement them in the order they appear below -- later methods build on
    the ones before them, the same way this course's dynamic array and
    linked-list assignments built one method on top of another.
    """

    DEFAULT_CAPACITY = 8
    DEFAULT_LOAD_FACTOR = 0.7
    RESIZE_BY = 2

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self._capacity = capacity
        self._underlying: list[Node | None] = [None] * capacity
        self._node_count = 0
        self._slots_used = 0
        self._load_factor = SimpleHash.DEFAULT_LOAD_FACTOR

    def _hash(self, name: str) -> int:
        """
        Return an index into self._underlying for the given name.

        Contract:
        - Use Python's built-in hash(name).
        - hash() can return a negative integer -- wrap it with abs() before
          taking the modulo, or two names that hash to negative numbers of
          the same magnitude could be sent to different-looking indices
          than you expect.
        - Reduce the (non-negative) hash to a valid index with `% self._capacity`.

        One return statement, at the very end.
        """
        pass

    def add(self, name: str) -> None:
        """
        Insert name into the hash table.

        Contract:
        - Compute the target slot with self._hash(name).
        - If self._underlying[index] is empty (None), this is a new slot:
          place a new Node there directly, and increment self._slots_used.
        - If self._underlying[index] already holds a chain, do not walk to
          the end of it. Create a new Node whose `next` is the *existing*
          head of that chain, and place the new Node at self._underlying[index]
          -- the new node becomes the new head. (This is the same
          insert-at-head idea from the week 11 class discussion: appending
          to the end of a chain means walking it first, which insert-at-head
          avoids entirely.)
        - Either way, increment self._node_count by exactly one.
        - After inserting, check whether self._slots_used / self._capacity
          has exceeded self._load_factor. If it has, call self._resize()
          before returning.

        No return value -- this method returns None.
        """
        pass

    def exists(self, name: str) -> bool:
        """
        Return True if name is already stored in the table, False otherwise.

        Contract:
        - Compute the target slot with self._hash(name).
        - Walk the linked list at that slot with a cursor, comparing each
          node's payload against name.
        - Return False if the slot is empty, or the chain is exhausted
          without a match.

        One return statement, at the very end. Use a boolean result variable
        and a while loop, the same pattern this course used for
        Trainline.contains() in week 6.
        """
        pass

    def __str__(self) -> str:
        """
        Return a string showing every occupied slot and the names chained
        there, in slot order.

        Contract:
        - Skip empty slots entirely -- do not print anything for them.
        - For each occupied slot, print the slot's index and every name in
          its chain, head to tail.
        - Exact formatting is your choice, as long as it is readable and
          shows both the slot index and every name in that slot's chain.

        One return statement, at the very end. Build the result with a list
        of pieces and str.join(), the way dynamic_array_solution.py's
        better_str() did in week 5 -- not repeated string concatenation
        inside the loop.
        """
        pass

    def _resize(self) -> None:
        """
        Double the underlying array's capacity and redistribute every
        stored name into the new array.

        Contract:
        - Create a new underlying array of size self._capacity * SimpleHash.RESIZE_BY,
          filled with None.
        - Walk every slot of the *old* array. For every node in every
          chain, re-hash its payload against the *new* capacity (the same
          name can land in a different slot once capacity changes) and
          insert it into the new array using the same insert-at-head rule
          add() uses.
        - Update self._capacity to the new size, and self._underlying to
          the new array.
        - Recompute self._slots_used to match how many slots are actually
          occupied in the new array -- it is not necessarily the same
          count as before, since two names that used to occupy two
          different slots in the old array could land in the same slot
          in the new one, or vice versa.
        - self._node_count does not change -- resizing moves nodes, it does
          not add or remove any.

        No return value -- this method returns None. Do not call add() to
        perform the reinsertion (add() checks the load factor and could
        trigger a second resize mid-resize); build the reinsertion directly
        against self._underlying's new array.
        """
        pass

    def get_node_count(self) -> int:
        return self._node_count

    def get_slots_used(self) -> int:
        return self._slots_used

    def get_capacity(self) -> int:
        return self._capacity


def main() -> None:
    table = SimpleHash(capacity=4)

    names = ["Frodo", "Sam", "Merry", "Pippin", "Gandalf", "Aragorn"]
    for name in names:
        table.add(name)

    print(table)
    print(table.exists("Frodo"))     # expected: True
    print(table.exists("Sauron"))    # expected: False
    print(table.get_node_count())    # expected: 6
    print(table.get_capacity())      # expected: 8 or 16, depending on how many
                                      # resizes the load factor threshold triggered


if __name__ == "__main__":
    main()
