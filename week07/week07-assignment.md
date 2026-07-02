# Week 7 Assignment: $\mathcal O(1)$ Middle Nodes, Continuity, and Loops in a Doubly Linked List

## This Week in Class

### June 29 -- From TrainLine to a Generic Node

We opened by revisiting the `TrainLine` assignment -- `add`, `contains`, `indexOf`, `indexOfAll`, `returnCount`, and `remove` -- and used it as a bridge to a more general data structure. One observation worth carrying forward: `contains` and `indexOf` share redundant logic; `contains` could simply call `indexOf` and check whether the result is meaningful.

Before moving on, we looked at what happens if the caller passes a plain string instead of a `Station` object. Using `isinstance(new_item, str)`, we can detect that case and construct a `Station` from the string. In Java this would be method overloading -- two `add` signatures; Python handles it with an `if` check instead. Type annotations (`: str`, `: Station`, `: T`) are hints, not contracts -- Python runs the code regardless of whether the argument matches the declared type.

We then introduced `Node` as the building block of a doubly linked list. Using `TypeVar` and `Generic` from Python's `typing` module (plus `from __future__ import annotations`), we defined a type parameter `T` so a node's payload can be any object -- a string, an integer, a `Station` -- without changing the class. Each node carries three fields: `payload`, `next`, and `previous`, both links defaulting to `None`.

A doubly linked list lets us traverse in either direction: forward by following `next` pointers, backward by following `previous` pointers. The head node's `previous` is `None`; the tail's `next` is `None`. We can still model a one-directional structure (like the southbound Red Line) by simply leaving the `previous` pointers at `None` -- a doubly linked node used in only one direction. We closed by previewing stacks and queues, and how to detect discontinuities in a bidirectional list -- the discontinuity idea is exactly what Part 2 below asks you to build.

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

We explored finding the middle node of a linked list. The naive approach counts all nodes (one full traversal), divides by $\lfloor n/2 \rfloor$, then traverses again to reach that position -- two passes. A more elegant one-pass method uses two cursors: a slow cursor moves one node at a time while a fast cursor skips every other node. Using a staircase analogy developed with Alexander and Jeleel, we worked out that when the fast cursor reaches the tail, the slow cursor is at the middle. We also reinforced why maintaining a node count field is practical: rather than counting on demand, we update it by $+1$ on insertion (and $-1$ on deletion, once `remove` exists) -- so the middle is always reachable in $\lfloor \text{count}/2 \rfloor$ steps from the head, with no traversal needed just to learn how many nodes there are.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on `self`, instance methods, and how a class like
  `DoubleLinkedList` organizes state and behavior together.

---

### July 1 -- Building `add`, and Bidirectionality as a Design Choice

We wrapped up the `Node` discussion by contrasting how Python and Java handle "any type of data." In Python, the type annotations we write are decorative -- the same intent could be captured in a comment and the code would behave identically. In Java, the equivalent notation is enforced by the compiler. Part of why we keep circling back to Java is that COMP 272, the next course in the sequence, is taught in Java.

We then wrote `add`. If the list is empty (`_head` is `None`), the new node becomes both head and tail. Otherwise, the new node is linked after the current tail and becomes the new tail. Either way, the node count is incremented -- a concrete example of trading space for time: maintaining a running count costs a few bytes of memory but avoids re-traversing the whole list every time we need to know its size.

Using escalators, undo/redo (Control-Z/Control-Y), and one-way cassette tapes as analogies, we distinguished unidirectional from bidirectional linked lists, and revised the constructor to accept a directionality parameter, so that setting a new node's `_previous` pointer happens only conditionally. Alexander asked whether a right-to-left unidirectional list would just swap head and tail -- Leo agreed that is the simpler way to *build* one that way. That is a different question from the one Part 5 below asks: given a forward-only list that already exists, how do you reverse it in place?

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods, `self`, and class state work, the
  foundation of every method you implement this week.

---

One more thing worth naming before you start: `double_linked_list.py` uses class attributes as named constants instead of bare literals, and they live in two different spots for a reason. `_BIDIRECTIONAL`, `_FORWARD_ONLY`, and `_BACKWARD_ONLY` sit at the very top of the class, above `__init__`, because `__init__`'s default argument (`directionality: int = _BIDIRECTIONAL`) is evaluated the moment the class body runs -- if those three were defined later in the file, that line would fail with a `NameError` before you ever created a list. 

The six string pieces used only by `__str__` (`_EMPTY`, `_CAP_LEFT`, `_CAP_RIGHT`, `_LINK_BOTH`, `_LINK_NEXT`, `_LINK_PREV`) have no such constraint, so they sit immediately above the one method that reads them. 

Either way, naming these values -- and marking them private with a leading underscore, since nothing outside this class should depend on them -- turns a comparison like `self.directionality != self._FORWARD_ONLY` into a readable decision instead of a bare `1` you would have to remember the meaning of. 

`__str__` itself is built out of the same three-way branch on `self.directionality` that you will write several more times this week: it picks which pointer is safe to follow (only `_prev` works on a backward-only list, so it walks from `_tail` and reverses the collected payloads before printing), then picks which arrow template to wrap those payloads in, and assembles the final string with a single `str.join` rather than concatenating piece by piece in a loop.

---

## Overview

The stub file [`double_linked_list.py`](./double_linked_list.py) contains a `DoubleLinkedList` class built on [`Node.py`](./Node.py). `__init__`, `add`, `__str__`, `get_middle_slow_fast`, and `has_loop` are already complete. Your job is to implement five methods: one that finds the middle node in $O(1)$, one that checks whether a bidirectional list is fully and correctly linked, two that detect loops in $O(1)$, and one that reverses a forward-only list.

`__init__` sets up four fields:

* `_head` and `_tail` -- the ends of the list, `None` when empty.
* `count_of_nodes` -- how many nodes have been added, maintained by `add`.
* `directionality` -- `0` for a fully bidirectional list, `1` for a list that only links `_next` (forward-only), `-1` for a list that only links `_prev` (backward-only). `add` uses this field to decide which pointers to set on every insertion.

Do not modify [`Node.py`](./Node.py).

**A note on type hints.** The type hints throughout `double_linked_list.py` -- including `DoubleLinkedList(Generic[T])` and the `TypeVar` it shares with `Node[T]` -- are more extensive than earlier weeks' code. They are there to demonstrate the concept, not because this assignment requires you to write or maintain them. Type hints are not part of what is graded this week; focus on getting the five methods correct.

---

## Part 1: `get_middle_node`

`get_middle_slow_fast`, already implemented above `get_middle_node` in the stub file, is the slow/fast cursor technique from the June 30 session:

```python
def get_middle_slow_fast(self):
    result = None
    if self._head is not None:
        slow = self._head
        fast = self._head
        while (
            fast.get_next() is not None
            and fast.get_next().get_next() is not None
        ):
            slow = slow.get_next()
            fast = fast.get_next().get_next()
        result = slow.get_payload()
    return result
```

It is correct on any list and needs nothing but `_head` and `_next` to work -- but it is $O(n)$: every call walks the list again from the beginning, racing a fast cursor against a slow one.

**Contract for `get_middle_node`:**

- Return the same payload `get_middle_slow_fast` would return, for any list.
- Return `None` if the list is empty.
- Run in $O(1)$: no traversal, no cursor, no loop of any kind inside the method body when it is called.

**Why this has to change more than just this one method.**

There is no way to answer "which node is in the middle" in constant time by inspecting the list at query time -- some structure has to already know the answer before `get_middle_node` is ever called. That means the real work happens elsewhere: you will need to add at least one more field to `__init__`, and keep it current inside `add` every time a node is appended, the same way `count_of_nodes` is already kept current. Think about how the identity of the middle node changes, if at all, each time a single node is appended to the end of the list. `get_middle_node` itself should end up being nothing more than reading that field.

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Part 2: `is_continuous`

Consider a bidirectional list, fully and correctly linked in both directions:

```
<-- A <---> B <---> C <---> D <---> E <---> F -->
```

Now suppose something goes wrong -- a pointer update is missed during an insert, or corrupted some other way -- and the list becomes:

```
<-- A <---> B <---> C --> D <---> E <---> F -->
```

The bidirectionality between `C` and `D` has broken: `D`'s `_prev` now points to `None`, even though `D` is not the head. Every `_next` pointer in the list is still intact, so a simple forward traversal from `A` would never notice anything wrong -- it would print `A B C D E F` exactly as before. The damage is only visible if you also check `_prev`.

This is a different problem from asking whether a list is unidirectional by design (`directionality` of `1` or `-1`): a forward-only or backward-only list is missing the same pointer on *every* node, on purpose. A discontinuity is a break in a list that is supposed to be fully bidirectional.

**Contract:**

- Implement `is_continuous(self) -> bool`, meant to be called only on a bidirectional list.
- Return `True` if every node's `_next` and `_prev` are consistent with a properly linked bidirectional list.
- Return `True` for an empty list and for a single-node list.
- Return `False` the moment a broken link is found anywhere.

How would you walk the list and check each node's pointers against what a properly linked node in that position should have?

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Part 3: `has_loop_unidirectional`

`has_loop`, already implemented in the stub file, is the same slow/fast cursor technique applied to cycle detection instead of middle-finding: a slow cursor and a fast cursor, using only `_next`. If the chain loops back on itself, the fast cursor eventually laps the slow one; if the chain terminates normally, the fast cursor runs out of nodes first. It is correct on a forward-only list, but it costs $O(n)$ every time it is called.

**Contract for `has_loop_unidirectional`:**

- Return the same answer `has_loop` would return, for a forward-only (`directionality == 1`) list.
- Return `False` for a normal, properly terminated forward-only list.
- Return `False` for an empty list.
- Run in $O(1)$: no cursor race, no traversal at all.

Think about what a properly maintained `_tail` should look like at the moment this method is called, and what it would mean if it did not look that way.

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Part 4: `has_loop_bidirectional`

A bidirectional list can also be wired so that it never terminates: instead of the head's `_prev` and the tail's `_next` being `None`, they are wired to each other, so the whole structure forms one continuous ring with no true starting or ending point. `has_loop` from Part 3 still correctly reports `True` on a list like this, since a ring is still a cycle when followed through `_next` alone -- but a bidirectional list hands you twice the information a forward-only list does at every node. Can you use the second pointer to answer without a cursor race at all?

**Contract:**

- Implement `has_loop_bidirectional(self) -> bool`, meant to be called only on a bidirectional list.
- Return `False` for a normal, properly terminated bidirectional list.
- Return `False` for an empty list.
- Return `True` if the list has been wired into a closed ring.
- Run in $O(1)$: no cursor race, no traversal at all.

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Part 5: `reverse`

Given a forward-only (`directionality == 1`) list, reverse it in place, so that traversing it from the new head to the new tail visits every node in the opposite order.

Recall Alexander's question from the July 1 session: if you want a list that reads right-to-left instead of left-to-right, the simplest approach is to build it that way from the start, using `_prev` instead of `_next`. `reverse` is a different problem: the list already exists, built entirely out of `_next` pointers, and you have to turn it around without rebuilding it from scratch.

It is tempting to think this is as simple as swapping `self._head` and `self._tail`. It is not. Swapping the two fields changes which node you *call* the head, but every node's `_next` pointer still points the same physical way it did before -- walking from the "new" head with `get_next()` would dead-end immediately, one hop in. The links themselves have to be rebuilt, one node at a time.

**Contract:**

- Implement `reverse(self) -> None`.
- After `reverse` runs, printing the list shows the payloads in the opposite order.
- `directionality` stays `1` (forward-only) when you are done.
- Must run in $O(n)$.
- An empty list or a single-node list is already its own reverse -- handle those without crashing.

**One return statement.** Your method must have exactly one `return` statement, at the very end.

---

## Verification

After implementing all five methods, run [`double_linked_list.py`](./double_linked_list.py) from the `week07` directory:

```
python3 double_linked_list.py
```

Check your output against the expected values:

```
<-- Howard <---> Jarvis <---> Morse <---> Loyola <---> Granville -->
Howard --> Jarvis --> Morse -->
<-- Howard <-- Jarvis <-- Morse
EMPTY
Morse
Morse
True
False
False
True
False
True
False
True
Howard --> Jarvis --> Morse -->
Morse --> Jarvis --> Howard -->
```

The first four lines test `__str__` (already implemented) on a bidirectional list, a forward-only list, a backward-only list, and an empty list. The next two test `get_middle_slow_fast` and `get_middle_node` on the same 5-station bidirectional list -- both must agree. The next two test `is_continuous` on a normal list and one with a deliberately broken `_prev`. The next four test `has_loop` and `has_loop_unidirectional` on a normal forward-only list and a looped one. The next two test `has_loop_bidirectional` on a normal bidirectional list and a fully wrapped ring. The last two show a forward-only list before and after `reverse`.

Edge cases to verify manually:

- `get_middle_node`, `is_continuous`, `has_loop_unidirectional`, and `has_loop_bidirectional` all return their "empty" value (`None`, `True`, `False`, `False`, respectively) on a freshly constructed `DoubleLinkedList()` with nothing added.
- A single-node bidirectional list has no discontinuity and no loop.
- Calling `reverse()` on an empty list or a single-node forward-only list does not crash, and leaves the list printing exactly as it did before.

---

## Further reading

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods, `self`, and class state work, the
  foundation of every method you implemented this week.

* [Type hints (`typing` module)](https://docs.python.org/3/library/typing.html) --
  the reference for `TypeVar` and `Generic`, used by the `Node` class this
  assignment builds on.

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 07**.

Submit only your Python file:

```
double_linked_list.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
