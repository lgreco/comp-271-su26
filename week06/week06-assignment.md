# Week 6 Assignment: Implementing the Data Structure Contract on a Linked Train Line

## This Week in Class

### June 22 -- Traversal and the Cost of Not Knowing the End

We picked up the linked train line we started sketching, reviewing the two
building blocks: [`Station.py`](./Station.py), whose objects each carry a
name and a pointer to the next station, and [`Trainline.py`](./Trainline.py),
whose `add` method attaches new stations at the end.

The session's main question was: how do we add a station when we don't know
where the line ends? We found the answer by traversal -- start a cursor at
`_head` and hop forward one `get_next()` call at a time until `has_next()`
returns `False`. That final station is the tail; calling `set_next` on it
attaches the newcomer. The cost is real: adding the nth station requires n
hops, so the time grows with the size of the line -- linear time, O(n).

We introduced Big O notation as a vocabulary for this kind of reasoning:
constant time O(1), linear O(n), quadratic O(n^2), and the practically
unsolvable exponential and factorial families, illustrated with
rice-on-a-chessboard and museum-heist examples.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods and `self` work, which is the mechanism behind
  every cursor traversal you write here.

---

### June 23 -- Tail Pointer, Big Theta, and the Data Structure Contract

We eliminated the O(n) cost of `add` by keeping a second pointer, `_tail`,
directly to the last station. With `_tail` always current, attaching a new
station costs exactly two assignments regardless of line length: one
`set_next` call and one update to `_tail`. That is O(1), constant time.

We also noticed a simplification: both branches of the old `if`/`else` in
`add` ended by setting `self._tail = new_item`, so that line could move
outside the conditional entirely. Eliminating redundancy means one fewer place
to update if the logic ever changes.

We formalized the difference between big O (an upper bound) and big Theta
(a tight, two-sided bound), and previewed the next step: implementing the
full data structure contract on our linked line.

**Further reading:**

* [`abc` -- Abstract Base Classes](https://docs.python.org/3/library/abc.html) --
  the reference for `ABC`, `@abstractmethod`, and how Python enforces a
  contract at instantiation time.

---

### June 24 -- `contains`, `__iter__`, and the Cursor Pattern

We wrote a `contains` method that searches the train line for a named station
and returns a boolean. Because our object is not a list, tuple, or string, a
`for` loop raises "object is not iterable." Instead, we used a cursor starting
at `self._head` and a `while` loop with two exit conditions: stop when the
cursor reaches `None` (end of line) or when the result becomes `True` (station
found). We hit an infinite loop mid-demo -- with student help, we spotted that
`cursor.get_next()` was being called but never assigned back to `cursor`.

Once we fixed the bug, we added `__iter__` using the same cursor pattern and
the `yield` keyword. Unlike `return`, which exits the method immediately,
`yield` passes the current value out and resumes on the next call. With
`__iter__` defined, `for x in red_line_southbound:` worked as expected.

We closed with a style preference: a `while` loop expresses the search intent
directly ("keep going until found or exhausted") without the hidden break that
a `for` loop requires. The assignment asks you to apply that same cursor
pattern to the four remaining contract methods.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on how `self`, instance methods, and special methods like
  `__iter__` work.

---

## Assignment Overview

The stub file [`trainline_assignment.py`](./trainline_assignment.py) contains
a `Trainline` class that inherits from `OurDataStructureContract` (defined in
[`../week05/our_first_contract.py`](../week05/our_first_contract.py)). The
`__init__` and `add` methods are already complete. Your job is to implement
the five abstract methods that the contract requires: `contains`, `index_of`,
`index_of_all`, `count`, and `remove`.

Python will raise `TypeError` if you try to create a `Trainline` object while
any abstract method is still unimplemented. That is the contract enforcement
in action.

All your code goes in [`trainline_assignment.py`](./trainline_assignment.py).
Do not modify [`Station.py`](./Station.py).

---

## Part 1: `contains`

`contains` is the method we built together in class on June 24. Implement it
here from memory, using the cursor pattern.

Implement:

```python
def contains(self, value) -> bool:
```

**Contract:**

- Return `True` if any station on the line has the name `value`.
- Return `False` if no such station exists, including when the line is empty.
- Start a cursor at `self._head`. Call `cursor.get_name()` to read a name;
  call `cursor.get_next()` to advance. Never reach into `_name` or `_next`
  directly.

**Why a while loop, not a for loop.**

A linked list is not a Python sequence -- it has no length, no indexing, and
no built-in iteration (until we add `__iter__`). The only way to move through
it is with `get_next()` calls managed by a `while` loop. The exit conditions
in the while test express the algorithm directly: stop when found or when the
end is reached.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. Initialize `result = False`, build the while condition around
it (`while not result and cursor is not None`), and return `result` after the
loop.

---

## Part 2: `index_of`

`index_of` extends the search idea from `contains` by also tracking position.

Implement:

```python
def index_of(self, value) -> int:
```

**Contract:**

- Return the 0-based position of the first station named `value`. Howard is
  at index 0, the station after Howard is at index 1, and so on.
- Return `-1` if no station has that name, including when the line is empty.
- Use a cursor and a counter that starts at `0` and increments with each hop,
  regardless of whether the current station is a match.

**Why -1 as the sentinel.**

`-1` is unambiguous: no valid index is negative. Using `None` would work
technically but forces callers to write a type-specific check (`if result is
None`). With `-1`, a caller can check `if result < 0` or compare directly to
a threshold, and the return type is always `int`.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. Initialize `result = -1` and build the while condition around
it so the loop exits as soon as a match is found.

---

## Part 3: `index_of_all`

`index_of_all` collects every position where `value` appears, not just the
first one.

Implement:

```python
def index_of_all(self, value) -> list:
```

**Contract:**

- Return a list of every index where a station named `value` appears.
- Return `[]` (empty list) if `value` is absent or the line is empty.
- Scan every station -- do not stop early. The same name could appear more
  than once on a line under construction.

**Why no early exit.**

`index_of` can stop the moment it finds one match, because the goal is the
first position. `index_of_all` must keep scanning to the end because it must
collect every position. A `while cursor is not None` condition with no match
check in the test expresses this directly.

**Why [] rather than None.**

An empty list already signals "not found" unambiguously. It has the same
type as a non-empty result, so a caller can always call `len()` or iterate
over it without a special `None` check.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. Start with `matches = []` and use `matches.append(position)`
inside the loop.

---

## Part 4: `count`

`count` returns the number of stations named `value`. It can be implemented
without a traversal loop of its own.

Implement:

```python
def count(self, value) -> int:
```

**Contract:**

- Return the number of stations named `value` on the line.
- Return `0` if `value` is absent or the line is empty.
- Delegate to `index_of_all`: the entire body is one line,
  `return len(self.index_of_all(value))`.

**Why delegation, not a second loop.**

`index_of_all` already traverses the line and collects every matching
position. Writing a second independent traversal in `count` duplicates that
logic -- if the definition of "match" ever changes (say, to case-insensitive
comparison), you would have to update two places instead of one. We saw the
same principle in the week 5 class on June 15: `count` built on `index_of_all`
rather than repeating its loop.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. It is also the only statement.

---

## Part 5: `remove`

`remove` is the most structurally complex method: it must update the chain of
pointers, not just read them.

Implement:

```python
def remove(self, index: int):
```

**Contract:**

- Remove and return the station at 0-based position `index`.
- Return `-1` (not `None`) if the line is empty, if `index` is negative, or
  if `index` is greater than or equal to the number of stations.
- Removing the head (`index == 0`) requires updating `self._head` to the
  station that was after it. If the line becomes empty, also set
  `self._tail = None`.
- Removing any other station requires traversing to the station just before
  `index`, then calling `set_next` on it to skip over the target. If the
  removed station was the tail, update `self._tail` to the station before it.

**Why pointer surgery, not shifting.**

In a dynamic array, `remove` shifts every element after the gap one position
to the left. In a linked list, removal is purely a pointer update: redirect
one `_next` field and the target station is no longer reachable from the head.
No elements move. The tradeoff is that reaching the station before `index`
still requires traversal -- it is O(n) -- but the removal itself is O(1).

**One return statement.** Your method must have exactly one `return` statement,
at the very end. Initialize `result = -1`. Only assign a `Station` object to
`result` when a valid station is found and its surrounding pointers have been
updated. Return `result` after all cases are handled.

---

## Verification

After implementing all five methods, run
[`trainline_assignment.py`](./trainline_assignment.py) from the `week06`
directory:

```
python3 trainline_assignment.py
```

Check your output against the expected values:

```
True
False
3
-1
[2]
[]
1
0
Morse
-1
```

The last two lines test `remove`. After `remove(2)` removes Morse (index 2),
the line becomes Howard -> Jarvis -> Loyola -> Granville. `remove(99)` on
that four-station line returns `-1` because index 99 is out of range.

Edge cases to verify manually:

- `contains` and `index_of` on an empty `Trainline()` return `False` and `-1`.
- `remove(0)` on a one-station line leaves `_head` and `_tail` both `None`.
- `remove` on an empty line returns `-1` without crashing.

---

## Part 6: Reflection -- Your Week 5 Work vs. the Posted Solution

This part has no new code. Open your week 5 submission (`roster_assignment.py`)
alongside [`../week05/week05-solutions.py`](../week05/week05-solutions.py).
Write your answers as a comment block at the very bottom of
[`trainline_assignment.py`](./trainline_assignment.py), below all the code,
so the reflection is included when you submit.

```python
# Part 6 Reflection
#
# 1. has_member and how_many in the solution are each a single line that
#    delegates to one DynamicArray method -- contains and count respectively.
#    Did you implement them the same way, or did you write a search loop
#    inside either method? If you wrote a loop, name the DynamicArray method
#    that already did that work.
#
# 2. remove_member in the solution has exactly two statements and one return:
#
#       position = self._members.index_of(name)
#       result = self._members.remove(position)
#
#    When name is absent, index_of returns -1, and remove(-1) returns -1 on
#    its own because of the `index >= 0` guard inside DynamicArray.remove.
#    Did your remove_member add an explicit `if position == -1` check before
#    calling remove? If so, which guard is now redundant -- yours or
#    DynamicArray's?
#
# 3. The solution's remove_member has exactly one return statement. If your
#    version had two (an early return for the not-found case and one at the
#    end), explain in one sentence how the sentinel chaining from question 2
#    makes the early return unnecessary.
#
# 4. The solution's index_of_all (in dynamic_array_solution.py) scans every
#    filled slot with a single-exit for loop and returns the matches list
#    once at the end. Did your week 5 index_of_all also scan every slot, or
#    did you add an early exit after the first match? What result would
#    index_of_all("Sam") produce on a roster containing two Sams if the
#    loop stopped at the first match?
```

---

## Further reading

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods, `self`, and special methods like `__iter__` work,
  which is the foundation of every method you implement here.

* [`abc` -- Abstract Base Classes](https://docs.python.org/3/library/abc.html) --
  explains how `ABC` and `@abstractmethod` make a contract enforceable at
  instantiation time rather than only at the call site.

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 06**.

Submit only your Python file:

```
trainline_assignment.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
