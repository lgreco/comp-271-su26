# Week 5 Assignment: Composing an App Class on Top of Dynamic Array

## This Week in Class

### June 15 -- Completing `count` and `index_of_all`, and Contracts

We opened by revisiting the dynamic array object built over the past few
weeks -- an object that wraps a fixed-size array and resizes itself as items
are added. The week 4 assignment asked us to add two methods: `count` (how
many times a given value appears) and `index_of_all` (a list of every index
position where it appears).

Several of us had written `count` by building `index_of_all` first and then
returning its length. That's exactly the point: once `index_of_all` exists,
`count` collapses to `return len(self.index_of_all(value))`. We also traced
the from-scratch version: start a counter at zero, loop `for i in
range(self.size)` (a `for` loop because we must check every position -- no
early exit), and increment whenever `self.underlying[i]` matches the target.
The lesson: when adding a new method, always check whether existing methods
can do part of the work. Redundant loops mean multiple maintenance points.

We introduced the idea of a *contract*: a formal agreement that every data
structure we build will expose at least `contains`, `index_of`, `remove`,
`index_of_all`, and `count`. We developed the car analogy together -- a
driver needs an accelerator, brakes, and a steering wheel, not knowledge of
the engine internals. In Python a contract is an *abstract base class*; in
Java it's called an *interface*. A class that signs the contract must
implement every method in it -- partial compliance isn't accepted. See
[`our_first_contract.py`](./our_first_contract.py) for the contract itself
and [`silly_data_structure.py`](./silly_data_structure.py) for a class that
signs it in letter but not in spirit.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers class definition syntax, instance methods, and the role of `self`.

---

### June 16 -- Docstrings, Magic Values, String Immutability, and ABCs as Contracts

We returned to the dynamic array and looked at ways to make the code more
professional. We added a docstring -- a documentation comment placed right
after a method header that explains what the method does, its inputs, and
what it returns -- distinguishing it from ordinary inline comments. The
solution file is [`dynamic_array_solution.py`](./dynamic_array_solution.py).

We replaced "magic values" -- literal strings like brackets and separators
sprinkled directly in the code -- with named constants defined once near the
top of the class. That way, changing a delimiter style later requires
editing one line instead of hunting through the whole program. We noted an
exception: literal numbers that come directly from a mathematical formula
(like Einstein's `E = mc^2`) don't need to be parameterized.

We discussed why repeatedly concatenating strings in a loop is
memory-expensive: since strings are immutable, each concatenation creates an
entirely new string in memory rather than modifying the original. A live
demo, [`immutability_demo.py`](./immutability_demo.py), grew a string
exponentially (doubling each iteration) and crashed with a memory error well
before reaching outlandish sizes like 2^100.

We introduced **abstract base classes** as a way to write a contract
specifying which methods (`contains`, `index_of`, `index_of_all`, `count`,
`remove`) any data structure must implement, with exact names, arguments,
and return types. Python's `abc` module enforces this: a class that inherits
from an `ABC` and skips an `@abstractmethod` cannot even be instantiated --
Python raises `TypeError` immediately, rather than letting the gap surface
later as a confusing bug. We distinguished fulfilling the literal contract
from fulfilling its spirit -- a class can technically satisfy the contract
while doing something meaningless. Docstrings on the abstract methods
communicate that intended spirit.

**Further reading:**

* [`abc` -- Abstract Base Classes](https://docs.python.org/3/library/abc.html) --
  the reference for `ABC`, `@abstractmethod`, and how Python enforces a
  contract at instantiation time.

---

### June 17 -- String Immutability Revisited and Modeling a Linked Node

We opened with a second pass over the
[memory demonstration](./immutability_demo.py): repeatedly appending a
string to itself showed the memory address changing every time, proving
that Python strings are immutable -- an operation that looks like "growing"
a string actually creates a brand-new string object each time. We connected
this directly to our dynamic array's string-building logic in `__str__`,
which is fine at small scale but should ideally use
[`str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join) on
a list of items instead of repeated concatenation, since `join` builds only
one or two strings rather than one per item. `better_str()` in
[`dynamic_array_solution.py`](./dynamic_array_solution.py) is that improved
version, kept side by side with `__str__` so the two can be compared
directly.

We also started sketching a *node* -- the building block of every linked
structure -- using a CTA train station as the analogy:
[`station.py`](./station.py) bundles a `name` with a `next` reference to
another `Station`. We are not yet building or assigning linked-list work;
this is a preview of where the course goes after this week's assignment.

---

## Overview

This week we step back from extending `DynamicArray` itself and instead
*use* it as a building block inside a new class. The file
[`roster_assignment.py`](./roster_assignment.py) contains a `FellowshipRoster`
class that is complete except for three methods marked with `pass`. Your
task is to implement those three methods. Do not modify `add_member` or
`__str__`.

`FellowshipRoster` does not inherit from `DynamicArray` -- it does not
extend or override anything from it. Instead, its constructor creates a
`DynamicArray` and stores it in `self._members`:

```python
from dynamic_array_solution import DynamicArray

class FellowshipRoster:
    def __init__(self):
        self._members = DynamicArray()
```

This is **composition**: `FellowshipRoster` *has a* `DynamicArray`, rather
than *is a* `DynamicArray`. Every method you write should call a method on
`self._members` -- never reach into `self._members._underlying` or any
other private field directly. That boundary is exactly what `contains`,
`index_of`, `count`, and `remove` exist to protect: `FellowshipRoster`
should only ever need to know the array's public contract, never its
internal array-and-resizing mechanics.

---

## Part 1: Why Composition, and How the Contract Makes It Possible

This part has no code to write -- read and understand before moving on.

Recall the contract from June 15: any data structure we build exposes
`contains`, `index_of`, `index_of_all`, `count`, and `remove`. Look at
[`dynamic_array_solution.py`](./dynamic_array_solution.py): `DynamicArray`
already implements every one of those methods. It happens to already fulfill
[`our_first_contract.py`](./our_first_contract.py)'s `OurDataStructureContract`,
even though it was never written to inherit from it.

That is exactly why `FellowshipRoster` can be built through composition
instead of inheritance. `FellowshipRoster` does not need to know *how*
`DynamicArray` finds a value or shifts elements after a removal -- it only
needs to know that `contains(value)`, `count(value)`, `index_of(value)`, and
`remove(index)` exist and behave as documented. The same way a driver uses
an accelerator and a steering wheel without knowing how the engine works, a
class that *has* a `DynamicArray` only needs its public methods.

**Further reading:**

* [`abc` -- Abstract Base Classes](https://docs.python.org/3/library/abc.html) --
  see how `ABC` and `@abstractmethod` make a contract enforceable, rather
  than just a comment or a convention.
* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on how methods, `self`, and instance attributes work, which is
  what makes `self._members = DynamicArray()` meaningful.

---

## Part 2: `has_member`

Implement:

```python
def has_member(self, name) -> bool:
```

**Contract:**

- Return `True` if `name` appears anywhere on the roster, `False` otherwise.
- Delegate to exactly one `DynamicArray` method on `self._members`. Do not
  write a search loop in this method -- `DynamicArray` already has one.

---

## Part 3: `how_many`

Implement:

```python
def how_many(self, name) -> int:
```

**Contract:**

- Return the number of times `name` appears on the roster.
- If `name` does not appear, return `0`.
- Delegate to exactly one `DynamicArray` method on `self._members`.

---

## Part 4: `remove_member`

Implement:

```python
def remove_member(self, name):
```

**Contract:**

- Remove the first occurrence of `name` from the roster and return it.
- If `name` is not on the roster, return `-1`.
- This method needs two steps, not one: first find *where* `name` is, then
  remove it from that position. Both steps delegate to `DynamicArray`
  methods on `self._members` -- do not write a search loop or a shifting
  loop here.

---

## Verification

After implementing all three methods, run
[`use_roster.py`](./use_roster.py) and check your output against these
expected results:

```python
from roster_assignment import FellowshipRoster

fellowship = FellowshipRoster()
fellowship.add_member("Frodo")
fellowship.add_member("Sam")
fellowship.add_member("Sauron")
fellowship.add_member("Saruman")
fellowship.add_member("Sam")
fellowship.add_member("Donald")
fellowship.add_member("Donald")

print(fellowship.has_member("Sam"))     # expected: True
print(fellowship.how_many("Sam"))       # expected: 2
print(fellowship.has_member("Merry"))   # expected: False
print(fellowship.how_many("Merry"))     # expected: 0

print(fellowship.remove_member("Sauron"))  # expected: Sauron
print(fellowship.remove_member("Merry"))   # expected: -1
print(fellowship)  # expected: [ Frodo, Sam, Saruman, Sam, Donald, Donald ]
```

---

## Part 5: Reflection -- Comparing Your Week 4 Work with the Solutions

This part has no new code to write. Open your week 4 submission alongside
[`dynamic_array_solution.py`](./dynamic_array_solution.py) and compare what
you wrote for `index_of_all` and `count` with what the solution file
contains now. Write your answers as comments at the very bottom of
`roster_assignment.py`, beneath the existing code, so they are included when
you submit. A few sentences per question is enough.

**1. `index_of_all` -- single exit point**

The solution builds a `matches` list while scanning every filled slot with a
`for` loop, then returns `matches` once at the end. Did your week 4
implementation also use exactly one `return` statement? If you used a `for`
loop, did you scan every filled slot even after finding a match, or did you
try to stop early? Why does `index_of_all` need to keep scanning, unlike
`index_of`?

**2. `count` -- delegation versus a second loop**

The solution implements `count` as a single line: `return
len(self.index_of_all(value))`. Did you delegate to `index_of_all` the same
way, or did you write a second, independent search loop? If you wrote a
second loop, what would you have to change in two places if the definition
of "match" ever changed (for example, a case-insensitive comparison)?

**3. Sentinels -- `[]` versus `0` versus `-1`**

`index_of_all` returns `[]` when `value` is absent, and `count` returns `0`.
Neither uses `-1`, even though `index_of` and `remove` do. Why does an empty
list already serve as an unambiguous "not found" signal without needing a
sentinel? Why does `0` make sense as `count`'s "not found" value where `-1`
would not?

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 05**.

Submit only your Python file:

```
roster_assignment.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
