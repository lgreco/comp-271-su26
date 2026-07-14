from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

# Week 9 -- Circular Stack and Queue, Built on a Shared Superclass
#
# Same split as week08's BoundedCollection/Stack/Queue, but the backing
# list is never shifted. Two indices, _front and _back, chase each other
# around the list using modulo arithmetic instead of moving data, which
# is what gets push/pop and enqueue/dequeue down to O(1) -- week08's
# array-shifting versions were O(n) for at least one of the two
# operations. See week09/2026-07-13-COMP271.md and
# week09/2026-07-14-COMP271.md for the class discussion this follows.


class CircularBuffer(Generic[T]):
    """
    A fixed-capacity collection backed by a plain Python list, wrapped
    into a circle: index _capacity - 1 is adjacent to index 0. Not an
    abstract base class -- just the bookkeeping CircularStack and
    CircularQueue have in common.

    _back always names the entrance: the slot the next inserted item
    will occupy. Every push/enqueue writes at self._back and then
    advances self._back one step forward (mod capacity). Where the two
    subclasses differ is the exit -- CircularQueue reads from the other
    end (_front) for FIFO order, CircularStack reads back from the
    entrance side (_back) for LIFO order -- so peek() and _remove_*()
    are not shared here the way they were in week08; each subclass
    defines its own.
    """

    def __init__(self, capacity: int) -> None:
        """Create an empty circular buffer that holds at most capacity
        items. _front and _back start at the same slot -- on an empty
        buffer there is no distance between "the next slot to fill" and
        "the next slot to drain" yet.
        """
        self._capacity: int = capacity
        self._items: list[T | None] = [None] * capacity
        self._front: int = 0
        self._back: int = 0
        self._size: int = 0

    def __str__(self) -> str:
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
        return self._size == self._capacity

    def _insert(self, item: T) -> bool:
        # Shared entrance for both push and enqueue: write at _back,
        # then step _back forward one slot. The modulo is what turns
        # "one past the last index" back into 0 instead of running off
        # the end of the list -- the wraparound rule from class.
        added = not self.is_full()

        if added:
            self._items[self._back] = item
            self._back = (self._back + 1) % self._capacity
            self._size += 1

        return added


class CircularQueue(CircularBuffer[T]):
    """
    First in, first out. enqueue() writes at the entrance (_back);
    dequeue() drains from the exit (_front), the opposite end, which is
    what makes this FIFO.
    """

    def enqueue(self, item: T) -> bool:
        return self._insert(item)

    def dequeue(self) -> T | None:
        # Unlike week08, where _remove() lived once on BoundedCollection
        # and both Stack.pop and Queue.dequeue called it unchanged, this
        # method is not shared with CircularStack.pop. In week08 both
        # subclasses agreed to always exit at index 0, so one _remove()
        # covered both. Here the two subclasses drain from opposite
        # ends of the buffer -- FIFO reads and advances _front, LIFO
        # reads and retreats _back -- so there is no single index a
        # shared method could hardcode; each subclass has to name its
        # own pointer and its own direction of travel.
        result = None

        if not self.is_empty():
            result = self._items[self._front]
            self._items[self._front] = None
            # Same wraparound rule as _insert, just walking the other
            # pointer forward.
            self._front = (self._front + 1) % self._capacity
            self._size -= 1

        return result

    def peek(self) -> T | None:
        return None if self.is_empty() else self._items[self._front]


class CircularStack(CircularBuffer[T]):
    """
    Last in, first out. push() writes at the entrance (_back), same as
    CircularQueue.enqueue(). pop() also drains from _back -- the item
    most recently written is one step behind the entrance -- which is
    what makes this LIFO instead of FIFO. _front is inherited but never
    moves; a stack only ever operates from one end.

    Popping walks _back backwards, so the wraparound rule runs in
    reverse: stepping from slot 0 back to slot -1 must land on
    _capacity - 1, not a negative index. Python's % already does this
    for negative operands (-1 % capacity == capacity - 1), which is the
    same periodic-boundary behavior as list[-1] returning the last
    element.
    """

    def push(self, item: T) -> bool:
        return self._insert(item)

    def pop(self) -> T | None:
        # Kept local to CircularStack for the same reason
        # CircularQueue.dequeue is kept local to CircularQueue: there is
        # no single removal method both subclasses could share. Beyond
        # reading a different pointer (_back here vs _front there), the
        # arithmetic itself runs opposite ways -- dequeue steps _front
        # forward (+1) after reading, while pop must step _back
        # backward (-1) before reading, since the top of the stack is
        # the slot just behind the entrance, not the entrance itself.
        # Folding both directions into one method would need a
        # step-direction flag and an if-before-or-after-read branch,
        # which is more machinery than just writing the two methods
        # separately.
        result = None

        if not self.is_empty():
            self._back = (self._back - 1) % self._capacity
            result = self._items[self._back]
            self._items[self._back] = None
            self._size -= 1

        return result

    def peek(self) -> T | None:
        if self.is_empty():
            return None
        top_index = (self._back - 1) % self._capacity
        return self._items[top_index]


def main() -> None:
    stack: CircularStack[str] = CircularStack(3)
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
    print(stack.push("E"))  # expected: True -- back has wrapped around
    print(stack.peek())  # expected: E
    print(stack.pop())  # expected: E
    print(stack.pop())  # expected: A
    print(stack.pop())  # expected: None -- stack is empty
    print(stack.is_empty())  # expected: True
    print(bool(stack))  # expected: False

    queue: CircularQueue[str] = CircularQueue(3)
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
    print(queue.enqueue("E"))  # expected: True -- back has wrapped around
    print(queue.peek())  # expected: C
    print(queue.dequeue())  # expected: C
    print(queue.dequeue())  # expected: E
    print(queue.dequeue())  # expected: None -- queue is empty
    print(queue.is_empty())  # expected: True
    print(bool(queue))  # expected: False


if __name__ == "__main__":
    main()
