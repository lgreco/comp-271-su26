from __future__ import annotations

from typing import Generic, TypeVar

# Same type parameter idea as Node[T] in earlier weeks: a Stack[str] holds
# strings, a Stack[int] holds ints, and so on, without rewriting the class.
T = TypeVar("T")

# Week 8 Assignment -- Stacks and Queues, Built on a Shared Superclass
#
# This file has three classes, each with method stubs marked pass:
#   1. BoundedCollection -- the superclass shared by Stack and Queue
#   2. Stack              -- push, pop
#   3. Queue               -- enqueue, dequeue
#
# BoundedCollection.__init__ is already complete -- do not change it.
# Everything else marked pass is yours to implement.


class BoundedCollection(Generic[T]):
    """
    A fixed-capacity collection backed by a plain Python list. This is
    the superclass for Stack and Queue below -- it is NOT an abstract
    base class (it does not import anything from the abc module, and
    nothing stops you from instantiating it directly). It is just an
    ordinary class that happens to hold the behavior Stack and Queue
    have in common.

    No list shortcuts: list.insert(index, value), list.pop(index) with
    an index, and list.remove(value) are off limits everywhere in this
    file, because they hide their own O(n) shifting inside C code. The
    only allowed ways to change len(self._items) are
    self._items.append(item) (grow by one, at the end) and
    self._items.pop() with NO argument (shrink by one, at the end).
    Both are O(1). Any other shifting -- moving existing items to open
    or close a gap -- must be a loop you write yourself, indexing into
    self._items directly.

    Because of how Stack.push and Queue.enqueue call _add() below, the
    item due to come out next is always at self._items[0], for both
    classes. peek() and _remove() can therefore hardcode index 0 --
    neither one needs a _PEEK_INDEX-style hook to know which end of
    the list matters.
    """

    def __init__(self, capacity: int) -> None:
        """Create an empty collection that will hold at most capacity
        items. Already implemented -- do not change.
        """
        self._capacity: int = capacity
        self._items: list[T] = []

    def __str__(self) -> str:
        """Already implemented -- a debug view of the backing list, in
        the order items actually sit in memory (not "top-to-bottom" or
        "front-to-back"). Useful while testing Stack and Queue below.
        """
        return str(self._items)

    def is_empty(self) -> bool:
        """Return True if this collection holds no items.

        One return statement, at the very end.
        """
        pass

    def __bool__(self) -> bool:
        """Return True if this collection holds at least one item, so
        that `if my_stack:` and `if my_queue:` read naturally -- the
        opposite sense of is_empty().

        One return statement, at the very end.
        """
        pass

    def size(self) -> int:
        """Return how many items this collection currently holds.

        One return statement, at the very end.
        """
        pass

    def __len__(self) -> int:
        """Return the same value as size(), so that `len(my_stack)` and
        `len(my_queue)` work.

        One return statement, at the very end.
        """
        pass

    def is_full(self) -> bool:
        """Return True if this collection already holds _capacity
        items -- the point past which _add must refuse to add another.

        One return statement, at the very end.
        """
        pass

    def peek(self) -> T | None:
        """Return self._items[0], without removing it. Return None if
        the collection is empty.

        Hardcode index 0 here -- see the class docstring for why that
        is always the correct index for both Stack and Queue.

        One return statement, at the very end.
        """
        pass

    def _add(self, item: T, index: int) -> bool:
        """Insert item at position index in the backing list, unless
        the collection is already full. Return True if the item was
        added, False if it was rejected because the collection was
        full.

        Handle this generally rather than special-casing index == 0
        and index == self.size():
        - Grow the list by one slot first: self._items.append(item)
          (the value appended does not matter yet -- it is a
          placeholder that becomes the last slot).
        - If index is less than the new last index, shift every item
          from the old last index down to index one position to the
          right, working backwards (highest index first) so nothing
          gets overwritten before it is moved.
        - Write item into self._items[index].

        No list.insert(...) -- write the shifting loop yourself.

        Not part of the public Stack/Queue vocabulary by itself --
        push() and enqueue() below both just call this.

        One return statement, at the very end.
        """
        pass

    def _remove(self) -> T | None:
        """Remove and return self._items[0]. Return None, and remove
        nothing, if the collection is empty.

        - Save self._items[0] to return later.
        - Shift every remaining item one position to the left, so the
          gap at index 0 closes: self._items[i] = self._items[i + 1]
          for each i from 0 up to (but not including) the last index.
        - Shrink the list by one slot: self._items.pop() with NO
          argument (this just drops the now-duplicated last slot; it
          does no shifting of its own).

        No list.pop(0) and no list.remove(...) -- write the shifting
        loop yourself.

        Not part of the public Stack/Queue vocabulary by itself --
        pop() and dequeue() below both just call this.

        One return statement, at the very end.
        """
        pass


class Stack(BoundedCollection[T]):
    """
    Last in, first out. push() adds to the top of the stack; pop()
    removes and returns the item most recently pushed.

    Contract:
    - push(item) inserts at index 0 (see _add), so the top of the
      stack is always self._items[0]. Returns True if the item was
      added, False if the stack was already full.
    - pop() returns the item removed, or None if the stack was empty.
    """

    def push(self, item: T) -> bool:
        pass

    def pop(self) -> T | None:
        pass


class Queue(BoundedCollection[T]):
    """
    First in, first out. enqueue() adds to the back of the queue;
    dequeue() removes and returns the item that has been waiting the
    longest.

    Contract:
    - enqueue(item) inserts at index self.size() -- one past the last
      occupied slot (see _add) -- so the front of the queue stays at
      self._items[0] until it is dequeued. Returns True if the item
      was added, False if the queue was already full.
    - dequeue() returns the item removed, or None if the queue was
      empty.
    """

    def enqueue(self, item: T) -> bool:
        pass

    def dequeue(self) -> T | None:
        pass


def main() -> None:
    stack: Stack[str] = Stack(3)
    print(stack.is_empty())  # expected: True
    print(bool(stack))  # expected: False

    print(stack.push("A"))  # expected: True
    print(stack.push("B"))  # expected: True
    print(stack.push("C"))  # expected: True
    print(stack.is_full())  # expected: True
    print(stack.push("D"))  # expected: False -- stack is at capacity

    print(stack.peek())  # expected: C
    print(stack.size())  # expected: 3
    print(len(stack))  # expected: 3

    print(stack.pop())  # expected: C
    print(stack.pop())  # expected: B
    print(stack.pop())  # expected: A
    print(stack.pop())  # expected: None -- stack is empty
    print(stack.is_empty())  # expected: True
    print(bool(stack))  # expected: False

    queue: Queue[str] = Queue(3)
    print(queue.is_empty())  # expected: True
    print(bool(queue))  # expected: False

    print(queue.enqueue("A"))  # expected: True
    print(queue.enqueue("B"))  # expected: True
    print(queue.enqueue("C"))  # expected: True
    print(queue.is_full())  # expected: True
    print(queue.enqueue("D"))  # expected: False -- queue is at capacity

    print(queue.peek())  # expected: A
    print(queue.size())  # expected: 3
    print(len(queue))  # expected: 3

    print(queue.dequeue())  # expected: A
    print(queue.dequeue())  # expected: B
    print(queue.dequeue())  # expected: C
    print(queue.dequeue())  # expected: None -- queue is empty
    print(queue.is_empty())  # expected: True
    print(bool(queue))  # expected: False


if __name__ == "__main__":
    main()
