# Week 4 Assignment: Searching a Dynamic Array

## This Week in Class

### June 8 -- Reviewing Week 3, Searching, and Structured Programming

We opened by reviewing the week 3 assignment: `__len__`, `get_size`, `get_capacity`,
and `get`. Two themes came up repeatedly.

First, getter methods (accessors) give outside code controlled access to private
data. Reading `da._size` directly from outside the class violates the object's
boundary -- the leading underscore is a promise that internal variables are the
object's own business. Accessor methods (`get_size()`, `get_capacity()`) are the
right way in.

Second, we implemented `index_of` two ways -- a `for` loop and a `while` loop --
and compared them. The `for`-loop version has a subtle bug: when the value is not
found, it returns the last loop index rather than -1. The `while` loop is
preferred for searches because its condition can encode both "not yet found" and
"not yet exhausted all positions," making the termination logic explicit.

We also named Dijkstra's single-entry / single-exit principle: a method should
have one `return` statement, not several. Multiple `return` statements scattered
through a method are harder to trace. Express the termination condition in the
loop header instead.

**Further reading:**

* [A First Look at Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes) --
  covers class definition syntax, instance methods, and the role of `self`.

---

### June 9 -- Dunder Methods, Bounds Checking, and Delegation

We introduced **dunder methods**: methods whose names begin and end with two
underscores, such as `__str__` and `__len__`. Python wires these names to
built-in behavior automatically. We demonstrated `__str__` by temporarily
removing it: `print()` fell back to a cryptic memory-address string. Restoring
it made the object display its contents meaningfully.

The `get(index)` method raised a Python trap: Python lists accept negative indices
natively (-1 means the last element). Without an explicit check for `index < 0`,
`get(-1)` silently returns the last stored value instead of `None`, violating the
stated contract. The fix is a bounds check: `if index >= 0 and index < self._size`.

We then refactored `contains(value)`. An earlier version duplicated the search
loop from `index_of`. We reduced it to one line: call `index_of()` and return
`True` if the result is >= 0. The lesson: **eliminate redundancy by delegating to
methods that already do the work.** Duplicated loops mean double the maintenance
burden whenever the logic changes.

**Further reading:**

* [Class and Instance Variables](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) --
  distinguishes variables shared across all instances from variables unique to each one.
* [Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables) --
  explains single- and double-underscore conventions and name mangling.

---

### June 10 -- Removing Elements, Generalizing, and Encapsulation

We designed `remove(index)` together before writing a single line of code.
Removal must preserve contiguity: no gaps can appear in the filled region.
The algorithm shifts every element after the removed one one position to the
left, then clears the last occupied slot to `None`. Clearing that slot is
critical -- without it, the last element would be duplicated and could reappear
if new elements were added later.

We also generalized the array: `_underlying` now stores any value, not just
integers. Naming an internal container `_zip_codes` was a mistake from earlier
in the course -- it tied the implementation to one domain. `_underlying` removes
that constraint. The type annotation on `_underlying` changed from `list[int]`
to `list` to reflect this.

**Further reading:**

* [More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists) --
  documents the list operations the underlying array relies on (append, indexing, length).
* [Objects and classes](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html) --
  Chapter 11 of Lubanovic; covers how Python classes work from the ground up.

---

## Overview

The file [`dynamic_array_assignment.py`](./dynamic_array_assignment.py) contains
the `DynamicArray` class from class, complete except for two methods marked with
`pass`. Your task is to implement those two methods. Do not modify any other part
of the file.

---

## Part 1: Generalizing the Array -- Any Value, Not Just `int`

Earlier versions of `DynamicArray` carried `int` type hints throughout:
`list[int]`, `value: int`. That made sense when the only use case was storing
zip codes. But the class is general-purpose: it should hold strings, floats,
objects, or any mix.

The assignment file removes those `int` restrictions. The underlying list is
now typed as `list`, and the `value` parameters in `index_of` and `contains`
carry no type annotation.

The file also adds this import at the very top:

```python
from __future__ import annotations
```

This import changes how Python handles type annotations. Normally, Python
evaluates each annotation at the moment it is read -- `list[int]` is computed
immediately when the class is defined. With `from __future__ import annotations`,
every annotation is stored as a plain string and evaluated only if something
explicitly asks for it (such as a type-checking tool). This has two benefits:

- **Forward references work.** A method that returns an instance of its own
  class (e.g., `def copy(self) -> DynamicArray:`) would otherwise fail at
  definition time because the class is not yet fully defined. With the import,
  the annotation is just the string `"DynamicArray"` -- no problem.
- **Newer-style hints work in older Python.** `list[int]` as a type hint is
  valid only in Python 3.9 and later. With the import, it is a string on 3.7
  and 3.8 as well, so the code runs without error across more versions.

You do not need to add anything for this part -- the import and the updated type
annotations are already in place. Read the file and make sure you understand
what changed.

**Further reading:**

* [Type hints (typing module)](https://docs.python.org/3/library/typing.html) --
  the reference for Python's `typing` module; covers generic aliases (`list[int]`,
  `tuple[str, ...]`) and how annotations interact with runtime behavior.

---

## Part 2: `index_of_all`

`index_of(value)` returns the index of the **first** occurrence of `value`.
That is not always enough. If the array holds `["Sam", "Frodo", "Sam", "Pippin"]`,
a caller may want to know that `"Sam"` appears at positions 0 **and** 2 -- not
just the first one.

Implement:

```python
def index_of_all(self, value) -> list[int]:
```

**Contract:**

- Search only the filled slots -- positions `0` through `_size - 1`.
- Return a `list[int]` containing the index of every element that equals `value`,
  in order from lowest index to highest.
- If `value` does not appear, return `[]` -- an empty list, not `None`, not `-1`.

**Why an empty list instead of a sentinel?**

`index_of` returns `-1` as a sentinel because its return type is `int` and there
is no valid index that is negative. `index_of_all` returns a `list`, and a list
already has a natural way to signal "nothing found": it is empty. The caller
checks `if result:` (empty list is falsy) or `len(result) == 0` -- no special
sentinel needed.

**Do not stop at the first match.** Unlike `index_of`, this method must continue
through every filled slot so that all occurrences are collected.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. This is the single-entry / single-exit principle from class.
Use a result list that grows as you scan the array, then return it once when the
loop is done. An empty result list is already the correct answer for the
not-found case -- no second `return` is needed.

---

## Part 3: `count`

Implement:

```python
def count(self, value) -> int:
```

**Contract:**

- Return the number of times `value` appears in the filled slots.
- If `value` does not appear, return `0`.

**Hint -- delegate, don't duplicate.** `index_of_all` already finds every
occurrence. The number of occurrences is the length of that list. A one-line
implementation that calls `index_of_all` and returns its length is correct,
concise, and easy to maintain. If the search algorithm ever changes, only
`index_of_all` needs to be updated.

This is the same delegation principle we used when refactoring `contains`:
one method does the work; the other is a thin wrapper that interprets the result.

**One return statement.** Your method must have exactly one `return` statement,
at the very end. Whether you delegate to `index_of_all` or write the count loop
directly, compute the result first and return it once.

---

## Verification

After implementing both methods, run [`dynamic_array_assignment.py`](./dynamic_array_assignment.py)
and check your output against these expected results. You can also use
[`implement_da.py`](./implement_da.py) as a starting point for your own manual tests.

Use an array that contains repeated values to exercise both methods:

```python
da = DynamicArray()
da.add("Sam")
da.add("Frodo")
da.add("Sam")
da.add("Pippin")
da.add("Sam")

print(da.index_of_all("Sam"))   # expected: [0, 2, 4]
print(da.index_of_all("Frodo")) # expected: [1]
print(da.index_of_all("Merry")) # expected: []

print(da.count("Sam"))          # expected: 3
print(da.count("Frodo"))        # expected: 1
print(da.count("Merry"))        # expected: 0
```

Pay particular attention to the not-found cases. `index_of_all("Merry")` must
return `[]`, not `None`. `count("Merry")` must return `0`, not `-1`.

---

## Part 4: Reflection -- Comparing Your Week 3 Work with the Solutions

This part has no new code to write. Open your week 3 submission alongside
[`dynamic_array_assignment.py`](./dynamic_array_assignment.py) and compare what
you wrote with what the solutions contain. Write your answers as comments at the
very bottom of `dynamic_array_assignment.py`, beneath the existing code, so they
are included when you submit. A few sentences per question is enough.

**1. `__len__` and `get_size` -- delegation**

The solution implements `__len__` as a single call to `get_size()`, and
`get_size()` is the only method that reads `self._size` directly. Did your
implementation do the same, or did both methods independently read `self._size`?
If yours duplicated the access, what is the cost of that duplication -- what
would you have to change in two places if `_size` were ever renamed?

**2. `get` -- the negative index trap and a changed sentinel**

The solution guards against negative indices with `if index >= 0 and index < self._size`.
Did your implementation include the `index >= 0` check? If not, what would
`get(-1)` have returned on a non-empty array, and why is that result wrong?

Also notice that the solution returns `None` for an out-of-range index, while
the week 3 assignment asked for `-1`. The reason: we generalized the array to
hold any type of value, not just integers. A method that stores strings cannot
use `-1` as a "not found" signal -- `-1` is not a string, and returning it would
cause a type error for the caller. `None` is the type-neutral sentinel. Did your
week 3 implementation use `-1` or `None`? Does that choice still make sense now
that the array is no longer limited to integers?

**3. `index_of` -- loop choice and a single exit point**

The solution uses a while loop with two conditions encoded directly in the header:
`while i < self._size and index < 0`. This expresses both termination conditions
-- "exhausted all slots" and "already found a match" -- without a `break` or an
early `return`. Did you use a `for` or a `while` loop? If you used a `for` loop,
how did you stop early when you found a match, and how did you handle the
not-found case? Does the solution have exactly one `return` statement? Does yours?

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 04**.

Submit only your Python file:

```
dynamic_array_assignment.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
