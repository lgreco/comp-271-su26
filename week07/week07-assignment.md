# Week 7 Assignment: Middle Nodes, Direction, and Loops in a Doubly Linked List

## This Week in Class

### June 29 -- From TrainLine to a Generic Node

We opened by revisiting the `TrainLine` assignment -- `add`, `contains`, `indexOf`, `indexOfAll`, `returnCount`, and `remove` -- and used it as a bridge to a more general data structure. One observation worth carrying forward: `contains` and `indexOf` share redundant logic; `contains` could simply call `indexOf` and check whether the result is meaningful. We will lean on that same delegation idea below.

Before moving on, we looked at what happens if the caller passes a plain string instead of a `Station` object. Using `isinstance(new_item, str)`, we can detect that case and construct a `Station` from the string. In Java this would be method overloading -- two `add` signatures; Python handles it with an `if` check instead. Type annotations (`: str`, `: Station`, `: T`) are hints, not contracts -- Python runs the code regardless of whether the argument matches the declared type.

We then introduced `Node` as the building block of a doubly linked list. Using `TypeVar` and `Generic` from Python's `typing` module (plus `from __future__ import annotations`), we defined a type parameter `T` so a node's payload can be any object -- a string, an integer, a `Station` -- without changing the class. Each node carries three fields: `payload`, `next`, and `previous`, both links defaulting to `None`.

A doubly linked list lets us traverse in either direction: forward by following `next` pointers, backward by following `previous` pointers. The head node's `previous` is `None`; the tail's `next` is `None`. We can still model a one-directional structure (like the southbound Red Line) by simply leaving the `previous` pointers at `None` -- a doubly linked node used in only one direction. We closed by previewing stacks, queues, and how to detect discontinuities in a bidirectional list -- the discontinuity idea is exactly what Part 5 below asks you to build.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods and `self` work, the mechanism behind every
  `Node` and `DoubleLinkedList` method you will write this week.

* [Type hints (`typing` module)](https://docs.python.org/3/library/typing.html) --
  the reference for `TypeVar` and `Generic`, used to make `Node` hold any
  payload type.

---

### June 30 -- Building `DoubleLinkedList` and Finding the Middle Node

With `Node` established, we began building a `DoubleLinkedList` class. The constructor takes no arguments and initializes three fields: `_head` (`None`), `_tail` (`None`), and a node count (`0`).

We explored finding the middle node of a linked list. The naive approach counts all nodes (one full traversal), divides by floor(n/2), then traverses again to reach that position -- two passes. A more elegant one-pass method uses two cursors: a slow cursor moves one node at a time while a fast cursor skips every other node. Using a staircase analogy, we worked out that when the fast cursor reaches the tail, the slow cursor is at the middle. We also reinforced why maintaining a node count field is practical: rather than counting on demand, we update it by +1 on insertion (and -1 on deletion, once `remove` exists) -- so the middle is always reachable in floor(count/2) steps from the head, with no traversal needed just to learn how many nodes there are.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on `self`, instance methods, and how a class like
  `DoubleLinkedList` organizes state and behavior together.

---

## Overview

The stub file [`double_linked_list_assignment.py`](./double_linked_list_assignment.py) contains a `DoubleLinkedList` class. `__init__`, `add`, `get_count`, `close_loop`, and `has_loop` are already complete. Your job is to implement seven methods: two that find the middle node, two that inspect whether a list's links go only one way, and three that detect broken or looping pointers.

Do not modify [`Node.py`](./Node.py).

---

## Part 1: `get_middle_by_count`

`add` already maintains `self._count`, updating it by +1 on every call. This part asks you to put that field to work: find the middle node without ever counting the list yourself.

Implement:

```python
def get_middle_by_count(self):
```

**Contract:**

- Return the payload stored at index `self._count // 2`, counting from the head.
- Return `None` if the list is empty.
- Do not traverse the list to learn its length -- `self._count` already holds it. The only traversal allowed is the walk from the head to the middle index.

**Why this method needs only one traversal.**

Without a stored count, finding the middle takes two passes: one to count the nodes, one to walk to the middle. Because `_count` is already updated on every `add`, the counting pass disappears -- the division becomes a single field lookup, and the only traversal left is the `count // 2` hops to reach the middle itself. This is the payoff from the June 30 session for keeping `_count` current.

**One return statement.** Your method must have exactly one `return` statement, at the very end. Initialize `result = None` and only walk the cursor and assign `result` when `self._head is not None`.

---

## Part 2: `get_middle_two_cursor`

This part asks for the same result as Part 1, reached a completely different way: without reading `self._count` at all.

Implement:

```python
def get_middle_two_cursor(self):
```

**Contract:**

- Start a slow cursor and a fast cursor both at `self._head`.
- On each iteration, advance the slow cursor one node and the fast cursor two nodes.
- Stop as soon as the fast cursor cannot advance two more nodes. The slow cursor is then on the middle node -- return its payload.
- Return `None` if the list is empty.
- `get_middle_by_count` and `get_middle_two_cursor` must return the same payload for the same list -- they describe the same node by two different routes.

**Why this is the "staircase" method from class.**

The fast cursor covers two nodes for every one the slow cursor covers, so by the time fast runs out of nodes, slow has covered half the distance -- one pass, with no separate counting step and no dependence on a maintained `_count` field. This is the technique to reach for whenever the size of a structure is not already tracked.

**One return statement.** Your method must have exactly one `return` statement, at the very end. Initialize `result = None` and only move the cursors and assign `result` when `self._head is not None`.

---

## Part 3: `which_direction`

A `DoubleLinkedList` built through `add` links every node in both directions. But nothing stops someone from building one by chaining `Node` objects with only `set_next` calls (a forward-only chain) or only `set_prev` calls (a backward-only chain) -- see `_build_one_directional` in `double_linked_list_assignment.py`, used by `main()` to build exactly these fixtures.

Implement:

```python
def which_direction(self) -> int:
```

**Contract:**

- Return `1` if every node's `_prev` is unusable (the list only works by following `_next`).
- Return `-1` if every node's `_next` is unusable (the list only works by following `_prev`).
- Return `0` if the list is fully bidirectional, and `0` for an empty list.
- Use `self._count`: walk forward from `self._head` counting how many nodes you reach, and walk backward from `self._tail` counting how many nodes you reach. Whichever direction reaches all `self._count` nodes -- and the other does not -- tells you the answer.

**Why `self._count` is needed here.**

A forward-only chain has no working `_prev` pointers, so you cannot discover its length by walking backward from the tail -- you would stop after one node. A backward-only chain has the same problem in reverse. `self._count`, set directly by whatever built the list, is what lets you tell "this direction reached every node" apart from "this direction gave up immediately."

**One return statement.** Your method must have exactly one `return` statement, at the very end. Initialize `result = 0` and only change it inside an `if self._head is not None:` block.

---

## Part 4: `is_unidirectional`

**Contract:**

- Return `True` if the list's links only go one way (forward-only or backward-only).
- Return `False` if the list is fully bidirectional, and `False` for an empty list.
- Delegate entirely to `which_direction`: the entire body is one line, `return self.which_direction() != 0`.

**Why delegation, not a second traversal.**

`which_direction` already walks the list in both directions and knows the answer. Writing a second traversal here would duplicate that logic -- exactly the redundancy we called out in `contains` calling `indexOf` on June 29, and the same principle behind `count` delegating to `index_of_all` in week 6.

**One return statement.** Your method must have exactly one `return` statement, at the very end. It is also the only statement.

---

## Part 5: `has_discontinuity`

This is the discontinuity check previewed at the end of the June 29 session. It is different from `is_unidirectional`: a one-directional chain is missing the same pointer on every node, on purpose. A discontinuity is a single broken node in what is otherwise meant to be a normal, fully-linked chain -- the kind of bug that shows up if a pointer update is missed during an insert or remove.

Implement:

```python
def has_discontinuity(self) -> bool:
```

**Contract:**

- Walk the list from `self._head` using `get_next()`.
- For every node that is not `self._head`, its `get_prev()` must not be `None`.
- For every node that is not `self._tail`, its `get_next()` must not be `None`.
- Return `True` the moment either check fails anywhere in the list.
- Return `False` if the whole list is checked with no failures, and `False` for an empty list.

**Why this check is local, not count-based.**

Unlike Part 3, this method is not comparing two full traversals -- it is looking for one bad node among otherwise-good ones. A single node with a missing pointer would not change how far a traversal reaches (you can still walk past it using the other direction's good link), so the count-comparison trick from `which_direction` would not catch it. You have to inspect each node's own pointers directly.

**One return statement.** Your method must have exactly one `return` statement, at the very end. Initialize `result = False` and build the while condition around it (`while cursor is not None and not result`) so the loop stops as soon as a broken node is found.

---

## Part 6: `has_infinite_loop`

A doubly linked list can be wired so that it never terminates: the head's `_prev` points somewhere instead of `None`, and the tail's `_next` points somewhere instead of `None`, so the whole structure forms one continuous ring.

Implement:

```python
def has_infinite_loop(self) -> bool:
```

**Contract:**

- Return `True` if the list is fully circular: no node has a `_prev` of `None` and no node has a `_next` of `None`.
- Return `False` for a normal, properly-terminated list.
- Return `False` for an empty list.

**A warning, not a hint.**

A loop like this has no `None` anywhere to stop at. A traversal that keeps calling `get_next()` (or `get_prev()`) until it finds `None` will never finish on a list like this -- it is not slow, it simply does not end. Whatever approach you take, make sure it is guaranteed to terminate before you run it.

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Part 7: `has_loop_instant`

`has_loop` is already implemented for you, above `has_loop_instant` in the stub file. Read it before writing this part. It is the tortoise-and-hare technique from Parts 1-2, applied to cycle detection instead of middle-finding: a slow cursor and a fast cursor, using only `_next`, so it works even on a one-directional chain. If the chain loops back on itself, the fast cursor eventually laps the slow one; if the chain terminates normally, the fast cursor runs out of nodes first.

`has_loop` costs a traversal every time it is called. This part asks for the same answer in O(1) -- the same idea as `_count`, which is updated the moment a node is added rather than counted on demand whenever someone asks.

Implement:

```python
def has_loop_instant(self) -> bool:
```

**Contract:**

- Return the same answer `has_loop` would return, for any list.
- Do this with no traversal at all.

**What you need to add.**

`close_loop`, already provided, links the tail's `_next` back to the head and sets `self._has_loop = True` -- but nothing in `__init__` initializes that field. Add `self._has_loop = False` to `__init__`. If you skip this step, calling `has_loop_instant` on a list that was never looped will raise `AttributeError` -- that crash is telling you the field is missing, not that your logic is wrong.

**One return statement.** Your method must have exactly one `return` statement, at the very end. The entire body is one line: `return self._has_loop`.

---

## Verification

After implementing all seven methods, run [`double_linked_list_assignment.py`](./double_linked_list_assignment.py) from the `week07` directory:

```
python3 double_linked_list_assignment.py
```

Check your output against the expected values:

```
Morse
Morse
Morse
Morse
None
None
0
1
-1
False
True
True
False
True
False
True
False
True
False
True
```

The first six lines test `get_middle_by_count` and `get_middle_two_cursor` on a 5-station list, a 4-station list, and an empty list -- both methods must agree on every line. The next six test `which_direction` and `is_unidirectional` on a normal list plus the forward-only and backward-only fixtures built by `_build_one_directional`. The next two test `has_discontinuity` on a normal list and one with a deliberately broken `_prev`. The next two test `has_infinite_loop` on a normal list and a fully wrapped one. The last four test `has_loop` and `has_loop_instant` on a normal list and a looped one.

Edge cases to verify manually:

- All seven methods return their "empty" value (`None`, `0`, `False`, as appropriate) on a freshly constructed `DoubleLinkedList()` with nothing added.
- A single-node list is bidirectional (`which_direction` returns `0`), has no discontinuity, has no infinite loop, and has no cycle.
- Calling `has_loop_instant()` before adding the `self._has_loop = False` line to `__init__` raises `AttributeError` on a list that was never looped -- try it, see the crash, then add the line.

---

## Part 8: Reflection -- Pointer Maintenance, Then and Now

This part has no new code. Open your week 6 submission ([`../week06/trainline_assignment.py`](../week06/trainline_assignment.py)) alongside `double_linked_list_assignment.py`. Write your answers as a comment block at the very bottom of `double_linked_list_assignment.py`, below all the code, so the reflection is included when you submit.

```python
# Part 8 Reflection
#
# 1. Your remove() in trainline_assignment.py updated only one pointer per
#    station (_next), because Station is singly linked. DoubleLinkedList.add
#    updates two pointers for the same reason in reverse: new_node.set_prev(...)
#    and self._tail.set_next(...). Why does a doubly linked structure always
#    need this pair of updates, where a singly linked one only needed the
#    one? What would happen to which_direction's answer for a list where add
#    forgot the set_prev call, every single time?
#
# 2. is_unidirectional delegates entirely to which_direction, the same way
#    count() in week 6 delegated to index_of_all(). Find the method in your
#    week 6 submission that does NOT delegate -- one that could have reused
#    an existing method's traversal but instead wrote its own loop. Which
#    method was it, and what existing method could it have called instead?
#
# 3. has_discontinuity and has_loop_instant both guard against a problem by
#    checking something before trusting it -- has_discontinuity checks each
#    node's pointers directly rather than trusting a stored count, while
#    has_loop_instant depends entirely on a stored field (_has_loop) instead
#    of checking anything directly. What has to go right elsewhere in the
#    class for has_loop_instant's shortcut to stay trustworthy over time --
#    and what is the equivalent risk for self._count, which get_middle_by_count
#    and which_direction both trust without double-checking?
```

---

## Further reading

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods, `self`, and class state work, the foundation
  of every method you implemented this week.

* [Type hints (`typing` module)](https://docs.python.org/3/library/typing.html) --
  the reference for `TypeVar` and `Generic`, used by the `Node` class this
  assignment builds on.

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 07**.

Submit only your Python file:

```
double_linked_list_assignment.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
