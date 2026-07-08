# Week 8 Assignment: Stacks and Queues, Built on a Shared Superclass

## This Week in Class

### July 6 and July 7 -- Reversal Review, and Removing the Tail and Head in O(1)

We revisited the doubly linked list reversal problem from Week 7, since a few of us found the logic tricky the first time around: a doubly linked list has "next" and "previous" pointers on every node, and reversing it means flipping both directions everywhere, not just swapping the head and tail labels. A cursor moves from head to tail, using each node's "next" pointer to find the following node and set that node's "previous" pointer back toward the cursor; a temporary reference to the previous node lets this happen in a single pass instead of two.

We then worked out two special-case removals from a fully connected doubly linked list, each in constant time. To remove the tail: capture the node before the tail, set its "next" pointer to `None`, and move the tail reference there. To remove the head: capture the node after the head, set its "previous" pointer to `None`, and move the head reference there. Both are $\mathcal O(1)$ -- three steps, regardless of how many nodes the list holds.

We closed by noting that once a list supports adding and removing from either end in constant time, two classic abstractions fall out of it almost for free: a queue (first in, first out) and a stack (last in, first out).

### July 8 -- Recursion, Stacks, and Queues

We opened by revisiting the factorial calculation: first the "naive" loop with an accumulator starting at 1, then the recursive version using $n! = n \times (n-1)!$ with $0! = 1$ as the base case. Pushing the recursive version to its limits -- computing factorials of increasingly large numbers -- eventually triggered a maximum recursion depth error, which became the bridge into why recursion depends on a stack.

A role-play with several students passing a factorial request down a chain, then passing answers back up, modeled how each recursive call is a pending "order" placed on a stack, resolved last-in-first-out starting from the base case. This connects to computer architecture: a dedicated stack register in the CPU tracks the next instruction to execute, which is why stacks underlie both recursion and iterative control flow. A second example -- traversing a map of locations to see whether a path exists -- showed stacks used for backtracking through unexplored choices.

From there we defined the core stack and queue operations: `push`/`pop` for stacks (last in, first out) and `enqueue`/`dequeue` for queues (first in, first out), plus `peek`, `size`, and `is_empty`. We worked through why a queue backed by a fixed-size array requires shifting all remaining elements after a removal -- an $\mathcal O(n)$ operation -- versus the constant-time push/pop or enqueue/dequeue possible with a linked list, where only the head or tail pointer moves.

Today's assignment builds on that comparison, but with a twist: instead of a linked list, we build `Stack` and `Queue` on top of a plain Python list of fixed capacity. Once that list is full, no more items can be pushed or enqueued -- the collection simply refuses, rather than growing to make room.

A stack supports `push` (add) and `pop` (remove) -- last in, first out. A queue supports `enqueue` (add) and `dequeue` (remove) -- first in, first out. Both also need a `peek` (look at what would be removed next, without removing it), an `is_empty` check, and a `size`. Once we write both classes side by side, the overlap is hard to miss: `is_empty`, `size`, and `peek` all come down to the same few lines of code, checking or indexing into an internal list. That overlap is exactly what a superclass is for.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods and `self` work, background for every method
  in this assignment.

* [Introducing Python, 3rd ed., Chapter 11 -- Inheritance](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html#c11_h_inheritance) --
  Lubanovic's chapter section on inheritance, background for the
  superclass/subclass relationship this assignment builds.

---

## A Short Detour: What Inheritance Is

Before Part 1, a small example unrelated to stacks and queues.

```python
class Vehicle:
    def __init__(self, wheels: int) -> None:
        self.wheels = wheels

    def describe(self) -> str:
        return f"a vehicle with {self.wheels} wheels"


class Car(Vehicle):
    def __init__(self) -> None:
        super().__init__(4)  # Car does not repeat what Vehicle already knows


my_car = Car()
print(my_car.describe())  # "a vehicle with 4 wheels" -- Car never wrote describe() itself
```

`Car(Vehicle)` means "a `Car` is a `Vehicle`, plus whatever `Car` adds or changes." `Car` never defines `describe` -- it inherits it from `Vehicle` automatically, because every `Car` object is also a `Vehicle` object underneath. `super().__init__(4)` calls `Vehicle`'s constructor, so `Car` does not have to repeat the line that stores `self.wheels`.

This is a different tool from the `abc` module (Abstract Base Classes) some of you have seen: `abc` exists to *forbid* a class from being instantiated directly, forcing every subclass to fill in specific methods before it will run. Plain inheritance, the kind used above and in this assignment, does not forbid anything -- `Vehicle()` on its own is perfectly legal Python, it just is not a very interesting object by itself. `BoundedCollection` in this assignment works the same way: nothing stops you from writing `BoundedCollection(5)`, but it only becomes a useful stack or queue once `Stack` or `Queue` adds the piece that makes it one.

---

## Overview

The stub file [`stack_queue_assignment.py`](./stack_queue_assignment.py) contains three classes:

* `BoundedCollection` -- the shared superclass. `__init__` is already complete. Everything else is a stub.
* `Stack(BoundedCollection)` -- last in, first out. `push` and `pop` are stubs.
* `Queue(BoundedCollection)` -- first in, first out. `enqueue` and `dequeue` are stubs.

Every one of these collections is backed by a single Python list, `self._items`, and a fixed `self._capacity` set once at construction and never changed. Do not let `self._items` grow past `self._capacity` -- that is the entire meaning of "fixed capacity" here.

**No list shortcuts for insertion or removal.** `list.insert(index, value)`, `list.pop(index)` (with an index other than none), and `list.remove(value)` all do their own shifting internally, in C, hiding the exact cost this assignment is about. None of those three may appear anywhere in your solution. The only list operations you may use to change the *length* of `self._items` are:

* `self._items.append(item)` -- grow the list by one slot at the end.
* `self._items.pop()` -- called with **no argument** -- shrink the list by one slot at the end.

Both of those are $\mathcal O(1)$ and involve no shifting on their own. Any actual shifting -- moving existing elements one slot to make room, or one slot to close a gap -- must be a loop you write yourself, reading and writing `self._items[i]` by index.

---

## Part 1: `BoundedCollection`

`BoundedCollection` is not an abstract base class -- it does not use the `abc` module, and nothing stops you from creating a `BoundedCollection` directly. It is an ordinary class that holds everything a `Stack` and a `Queue` have in common, so that neither subclass has to repeat it.

Implement:

* `is_empty(self) -> bool` -- `True` if `self._items` holds nothing.
* `__bool__(self) -> bool` -- the opposite sense of `is_empty`, so `if my_stack:` reads naturally.
* `size(self) -> int` -- how many items are currently stored.
* `__len__(self) -> int` -- same value as `size`, so `len(my_stack)` works.
* `is_full(self) -> bool` -- `True` once `size()` reaches `self._capacity`.
* `peek(self) -> T | None` -- the item at `self._items[0]`, without removing it; `None` if empty.
* `_add(self, item: T, index: int) -> bool` -- insert `item` at position `index`, unless the collection is already full; return whether it was added.
* `_remove(self) -> T | None` -- remove and return `self._items[0]`; `None` if empty.

Unlike earlier drafts of this assignment, `peek` and `_remove` do **not** need to know which end of `self._items` a `Stack` and a `Queue` disagree about -- because of how `_add` is used in Part 2 and Part 3, the item due to come out next always ends up at index `0`, for both classes. Hardcode `0` in `peek` and `_remove`.

The disagreement between a stack and a queue lives entirely in `_add`'s `index` argument:

* Inserting at `index == 0` means: first grow the list by one slot (`append`), then shift every existing item one position to the right (working from the back of the list toward `index`, so you never overwrite a value before you have moved it), then write `item` into `self._items[0]`.
* Inserting at `index == self.size()` (the first open slot, one past the last occupied one) means there is nothing to shift -- `self._items.append(item)` already puts it exactly there.

Write `_add` generally enough to handle both cases (and, if you want the extra practice, any `index` in between) rather than special-casing `index == 0` and `index == self.size()` as two unrelated code paths.

**One return statement per method.** Every method above must have exactly one `return`, at the very end.

---

## Part 2: `Stack`

A stack is last in, first out: whatever was pushed most recently is the first thing to come back out.

* `push(self, item: T) -> bool` -- add `item` to the top of the stack by calling `self._add(item, 0)`. Return `True` if it was added, `False` if the stack was already full. Do not duplicate `_add`'s logic here -- call it.
* `pop(self) -> T | None` -- remove and return the item at the top of the stack by calling `self._remove()`. Return `None` if the stack is empty. Do not duplicate `_remove`'s logic here -- call it.

Because `push` always inserts at index `0`, the most recently pushed item is always at `self._items[0]` -- which is exactly what `peek` and `_remove` already look at. `push` is the only place where a stack does any shifting; `pop` never has to shift, since removing index `0` and closing the gap is `_remove`'s job, and `_remove` uses the same $\mathcal O(1)$ tail-`pop()` trick as `_add` to shrink the list.

If you find yourself writing `self._items.append(...)`, `self._items.insert(...)`, or `self._items.pop(some_index)` directly inside `Stack`, stop -- that logic already exists on `BoundedCollection`. `push` and `pop` should be thin wrappers.

---

## Part 3: `Queue`

A queue is first in, first out: whatever was enqueued longest ago is the first thing to come back out.

* `enqueue(self, item: T) -> bool` -- add `item` to the back of the queue by calling `self._add(item, self.size())`. Return `True` if it was added, `False` if the queue was already full. Call `_add` -- do not duplicate it.
* `dequeue(self) -> T | None` -- remove and return the item at the front of the queue by calling `self._remove()`. Return `None` if the queue is empty. Call `_remove` -- do not duplicate it.

Because `enqueue` always inserts one past the last occupied slot, the item that has been waiting longest stays at `self._items[0]` until it is dequeued -- again, exactly what `peek` and `_remove` look at. `enqueue` never has to shift anything; `dequeue`, via `_remove`, does the shifting that closes the gap left at the front.

Notice that `enqueue` and `push` end up calling the exact same `_add` -- the only thing that ever distinguished a stack from a queue was the `index` passed in: `0` for a stack, `self.size()` for a queue. `pop` and `dequeue` call the exact same `_remove`, with no argument at all, because after `Stack.push` and `Queue.enqueue` are wired up this way, the next item to come out is always at index `0` no matter which one you built.

---

## Verification

After implementing all methods, run [`stack_queue_assignment.py`](./stack_queue_assignment.py) from the `week08` directory:

```
python3 stack_queue_assignment.py
```

Check your output against the expected values:

```
True
False
True
True
True
True
False
C
3
3
C
B
A
None
True
False
True
False
True
True
True
True
False
A
3
3
A
B
C
None
True
False
```

The first block exercises `Stack(3)`: `is_empty`/`bool` on an empty stack, three successful pushes, `is_full`, a rejected fourth push, `peek`/`size`/`len`, three pops in LIFO order, a pop on an empty stack, and `is_empty`/`bool` again. The second block repeats the same sequence for `Queue(3)`, except dequeues come back in FIFO order.

Edge cases to verify manually:

* `peek()`, `pop()`, and `dequeue()` all return `None` on a freshly constructed, empty `Stack` or `Queue` -- they must not raise an exception or crash on an empty backing list.
* `push`/`enqueue` on a full collection returns `False` and leaves `size()` unchanged -- the rejected item is not silently added anyway.
* A `Stack` and a `Queue` of the same capacity, given the same three items in the same order, must return items in the *opposite* order from each other when drained completely.

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 08**.

Submit only your Python file:

```
stack_queue_assignment.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
