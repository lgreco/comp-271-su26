from __future__ import annotations

from typing import Generic, TypeVar

# Same type parameter idea as Node[T] in earlier weeks: a Stack[str] holds
# strings, a Stack[int] holds ints, and so on, without rewriting the class.
T = TypeVar("T")

# Week 8 Solutions -- Stacks and Queues, Built on a Shared Superclass
#
# See stack_queue_assignment.py for the stub version and week08-assignment.md
# for the full writeup. This file fills in every method that was left as
# `pass`.


class BoundedCollection(Generic[T]):
    """
    A fixed-capacity collection backed by a plain Python list. This is
    the superclass for Stack and Queue below -- it is NOT an abstract
    base class (it does not import anything from the abc module, and
    nothing stops you from instantiating it directly). It is just an
    ordinary class that happens to hold the behavior Stack and Queue
    have in common.
    """

    def __init__(self, capacity: int) -> None:
        """Create an empty collection that will hold at most capacity
        items. The backing list is preallocated to its full capacity
        up front, filled with None placeholders, instead of starting
        empty and growing with append(). Because of this, self._items
        never changes length after __init__ -- occupancy is tracked
        separately with self._size, and len(self._items) is always
        self._capacity.
        """
        self._capacity: int = capacity
        self._items: list[T | None] = [None] * capacity
        self._size: int = 0

    def __str__(self) -> str:
        """Already implemented -- a debug view of the backing list, in
        the order items actually sit in memory (not "top-to-bottom" or
        "front-to-back"). Useful while testing Stack and Queue below.
        """
        return str(self._items)

    def is_empty(self) -> bool:
        return self._size == 0

    def __bool__(self) -> bool:
        return not self.is_empty()

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self.size()

    def is_full(self) -> bool:
        return self.size() == self._capacity

    def peek(self) -> T | None:
        # The upfront agreement behind this whole design: Stack and
        # Queue disagree about where an item goes IN (the entry point,
        # decided by the index _add is called with), but they agree to
        # share a single exit point -- the front of the list,
        # self._items[0] -- for both LIFO and FIFO. Once that exit
        # point is fixed, peek only ever has to look at index 0, no
        # matter which subclass is asking.
        result = None if self.is_empty() else self._items[0]
        return result

    def _add(self, item: T, index: int) -> bool:
        # Returns bool rather than the item itself because the caller
        # (Stack.push or Queue.enqueue) already has the item -- what it
        # doesn't have is knowledge of whether the collection was full.
        # The bool is the only new information _add can report back:
        # did the insert happen, or was it refused.
        # added is the return value itself, not just a flag guarding
        # the body below: whether the item gets added is exactly the
        # opposite of whether the collection is already full, so ask
        # is_full() once and read the answer straight into added
        # instead of re-deriving it with a separate condition.
        added = not self.is_full()

        if added:
            # The slot at self._size is already there (preallocated as
            # None in __init__), so "growing" here means claiming that
            # slot, not appending a new one -- last is the first open
            # slot, one past the last occupied index.
            last = self._size

            # From the 2026-07-13 class discussion: this loop must run
            # in reverse, from `last` down to `index`. A common bug is
            # shifting right with a left-to-right loop, which copies
            # self._items[index] into every following slot instead of
            # moving each value once -- every position ends up holding
            # the same duplicated value because the loop overwrites a
            # slot before it has copied that slot's original contents
            # onward. Running the loop backwards (highest index first)
            # guarantees each value is read out of a slot before that
            # slot is overwritten.
            for i in range(last, index, -1):
                self._items[i] = self._items[i - 1]

            self._items[index] = item
            self._size += 1

        return added

    def _remove(self) -> T | None:
        result = None

        if not self.is_empty():
            result = self._items[0]
            last = self._size - 1

            # Dequeuing/removal shifts left, so the loop runs forward,
            # from the left end toward the back. Unlike the
            # right-shift in _add, a forward loop is safe here:
            # self._items[i + 1] is always read before self._items[i]
            # is written, so nothing is lost.
            for i in range(0, last):
                self._items[i] = self._items[i + 1]

            self._items[last] = None  # clear the now-duplicated last slot
            self._size -= 1

        return result


class Stack(BoundedCollection[T]):
    """
    Last in, first out. push() adds to the top of the stack; pop()
    removes and returns the item most recently pushed.
    """

    def push(self, item: T) -> bool:
        # Insert at index 0: the new item becomes self._items[0], which
        # is exactly the slot _add shifts everything else out of the
        # way for -- and the only place a Stack does any shifting.
        return self._add(item, 0)

    def pop(self) -> T | None:
        # pop() never shifts on its own -- _remove already handles the
        # left-shift that closes the gap at index 0.
        return self._remove()


class Queue(BoundedCollection[T]):
    """
    First in, first out. enqueue() adds to the back of the queue;
    dequeue() removes and returns the item that has been waiting the
    longest.
    """

    def enqueue(self, item: T) -> bool:
        # Insert one past the last occupied slot: since index equals
        # size(), _add's shifting loop (range(last, index, -1)) never
        # runs -- the preallocated slot at self._items[self.size()] is
        # written directly.
        return self._add(item, self.size())

    def dequeue(self) -> T | None:
        # Same _remove as Stack.pop -- the front of the queue always
        # sits at index 0 because enqueue never disturbs it.
        return self._remove()


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
