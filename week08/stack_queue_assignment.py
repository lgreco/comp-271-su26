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

    Subclasses are expected to set the class attribute _PEEK_INDEX to
    the list index that peek() and _remove() should act on. A Stack
    and a Queue disagree about which end of the list matters for
    removal, but agree on almost everything else -- that disagreement
    is the only thing _PEEK_INDEX needs to capture.
    """

    # Overridden by Stack and Queue below. Left as None here so that a
    # BoundedCollection used directly (rather than through a subclass)
    # fails loudly the moment peek/_add/_remove try to use it, instead
    # of silently guessing an end.
    _PEEK_INDEX: int | None = None

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
        """Return the item that the next _remove() call would remove,
        without removing it. Return None if the collection is empty.

        Use self._PEEK_INDEX -- do not hardcode 0 or -1 here. The
        whole point of this method living on the superclass is that it
        works for both Stack and Queue, whichever _PEEK_INDEX they set.

        One return statement, at the very end.
        """
        pass

    def _add(self, item: T) -> bool:
        """Append item to the end of the backing list, unless the
        collection is already full. Return True if the item was added,
        False if it was rejected because the collection was full.

        Not part of the public Stack/Queue vocabulary by itself --
        push() and enqueue() below both just call this.

        One return statement, at the very end.
        """
        pass

    def _remove(self) -> T | None:
        """Remove and return the item at self._PEEK_INDEX. Return None,
        and remove nothing, if the collection is empty.

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
    - Set _PEEK_INDEX so that peek/pop act on the top of the stack --
      the end of the backing list that push() adds to.
    - push(item) returns True if the item was added, False if the
      stack was already full.
    - pop() returns the item removed, or None if the stack was empty.
    """

    _PEEK_INDEX: int = None  # replace None with the correct index

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
    - Set _PEEK_INDEX so that peek/dequeue act on the front of the
      queue -- the opposite end from the one enqueue() adds to.
    - enqueue(item) returns True if the item was added, False if the
      queue was already full.
    - dequeue() returns the item removed, or None if the queue was
      empty.
    """

    _PEEK_INDEX: int = None  # replace None with the correct index

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
