# Week 3 Assignment: DynamicArray Accessors

## This Week in Class

### June 1 -- Dynamic Arrays: From Fixed Capacity to Automatic Resizing

We started from last week's zip-code store: a fixed-size list with a `capacity`
(total slots) and a `size` (filled slots). When the array was full, the old
version just printed "sorry." The first goal was to fix that.

Class discussion weighed several options -- hardcoding a bigger number, using a
variable, pre-allocating the theoretical maximum -- and settled on doubling the
array size each time it fills up. Doubling keeps arithmetic clean and avoids
fractional sizes; 50% or 3x growth would work equally well.

The `resize()` method has three steps:

1. Create a new array twice the current size, pre-filled with `-1`.
2. Copy every element from the old array into the new one.
3. Replace the current array with the new one and update `capacity`.

We also named a code smell: **magic numbers**. Any literal integer other than
`-1`, `0`, or `+1` appearing directly in code hides intent. Named variables
(`capacity = 4`, `resize_by = 2`) document the policy and make it easy to
change in exactly one place.

The session closed by beginning the transition from the procedural version --
which needed `global` declarations inside every function -- to a class-based
version. An object bundles data and behavior together:

- Data: the underlying list, `capacity`, `size`
- Behavior: `add()`, `resize()`, `__str__()`

The `DynamicArray` class uses `self` to access its own data from any method,
making `global` unnecessary. The growth factor becomes a class-level constant
`RESIZE_BY = 2`, and the initial capacity is passed into `__init__()` so the
caller controls the starting size.

**Further reading:**

* [Classes](https://docs.python.org/3/tutorial/classes.html) -- the full
  chapter; read the introduction and the sections on class definition and
  instance objects.
* [More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
  -- documents the list operations the underlying array relies on (append,
  indexing, length).
* [Objects and classes](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html)
  -- Chapter 11 of Lubanovic; covers how Python classes work from the ground up.

---

### June 2-3 -- Resize Strategies, Debugging, and Encapsulation

**Resize strategies.** We examined the cost trade-off more carefully: adding
one extra slot minimizes wasted memory but triggers a copy on every single add.
Doubling wastes up to half the allocated space but copies rarely. We explored
percentage-based resizing (e.g., 10%) with a ceiling function to guarantee at
least one new slot -- balancing both concerns.

The class was updated to accept optional `capacity` and `resize_by` arguments
with class-level defaults (`DEFAULT_CAPACITY = 4`, `DEFAULT_RESIZE_BY = 2`).
Testing with `resize_by=0.1` produced a crash, left as a diagnostic exercise
for the following class.

**Debugging.** The bug was traced with help from Alexander, Temeeka, and Dutch:
multiplying an integer capacity by a float resize factor produces a float.
Python's `int()` floors the result, so `int(3 * 1.1)` is `3` -- the array
never actually grew. The fix is `math.ceil()`, which rounds up and guarantees
at least one new slot every time.

Two import styles are valid:

```python
import math            # call as: math.ceil(x)
from math import ceil  # call as: ceil(x)
```

Both are correct. The first keeps the module name visible at every call site;
the second is shorter but hides the origin. Prefer the first when you reference
the module only occasionally.

**Naming and encapsulation.** We renamed the internal container from `zip_codes`
to `_underlying`, making the class generic enough to hold any values. Single-
underscore prefixes on `_underlying`, `_capacity`, `_size`, and `_resize_by`
signal "do not access this directly." Python does not enforce this -- it relies
on professional courtesy rather than language rules. Double underscores add name
mangling (Python rewrites `__name` to `_ClassName__name` at compile time) for
extra friction, but still do not create true privacy.

The analogy: a car's dashboard is the public interface; the engine internals are
meant to be left alone. The weekend assignment asks you to write methods that
safely expose the object's size and capacity without violating that boundary.

**Further reading:**

* [Mathematics in the standard library](https://docs.python.org/3/tutorial/stdlib.html#mathematics)
  -- a short overview of `math`, `random`, and related modules.
* [Modules](https://docs.python.org/3/tutorial/modules.html) -- the full chapter
  on import forms, the standard library, and `from ... import` style.
* [Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables)
  -- explains single- and double-underscore conventions and name mangling in
  detail.
* [Modules and packages](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch12.html)
  -- Chapter 12 of Lubanovic; covers the module system and import patterns.

---

## Overview

The file [`dynamic_array_assignment.py`](./dynamic_array_assignment.py) contains a `DynamicArray` class that is
complete except for five methods marked with `pass`. Your task is to implement
those five methods. Do not modify any other part of the file.

---

## Part 1: Importing a Module

The `resize()` method computes the new capacity with this line:

```python
temp_capacity = math.ceil(self._resize_by * self._capacity)
```

`math.ceil()` rounds a number up to the next integer. Use of
`int()`, may be problematic because it rounds values down. This causes a bug:
`int(3 * 1.1)` evaluates to `3`, so an array with capacity 3 and a 10% growth
factor would never actually grow. `math.ceil` ensures the new capacity is
always at least one slot larger than the current one.

To use `math.ceil`, you must import Python's `math` module. There are two ways:

```python
import math
# call as: math.ceil(x)
```

```python
from math import ceil
# call as: ceil(x)
```

Both are correct. The first form keeps the module name visible at every call
site -- anyone reading `math.ceil(x)` knows immediately where `ceil` comes
from. The second is shorter but hides the origin. Prefer the first when
working with a module you reference only occasionally; the second is reasonable
when you use the function heavily and the source is obvious from context. The
assignment file uses the first form.

**Further reading:**
* [Modules](https://docs.python.org/3/tutorial/modules.html) --
the full chapter on the module system, import forms, and the standard library.
* [Mathematics in the standard library](https://docs.python.org/3/tutorial/stdlib.html#mathematics) --
a short overview of `math`, `random`, and related modules.
* [Modules and Packages](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch12.html) from Bill Lubanovic's book.

---

## Part 2: Protected Variables

The instance variables in this class use a single-underscore prefix:
`_underlying`, `_size`, `_capacity`, `_resize_by`. In Python, a leading `_`
is a convention, not a language rule. It signals: "this is an internal
detail -- interact with the object through its methods, not by reaching in
directly." Python does not enforce this; code outside the class can still read
and write `da._size`. The underscore is a gentlemen's agreement.

A double-underscore prefix (`__name`) does something different. Python rewrites
the name to `_ClassName__name` at compile time -- a transformation called
*name mangling*. This makes accidental override in subclasses harder but does
not create true privacy: you can still access the variable from outside the
class if you know the mangled name (e.g., `da._DynamicArray__size`). Python
has no private variables in the C++ or Java sense; it relies on convention and
programmer discipline instead.

The single underscore is the idiomatic choice for data-structure internals. Use
double underscore only when you specifically need to guard against subclass
name collisions -- a narrower situation.

The name `_underlying` is also a deliberate choice. An earlier version of this
class called the list `_zip_codes`, which tied the implementation to a single
domain. Naming an internal container after the data it happens to hold right now
is a mistake: a class called `DynamicArray` that stores its data in `_zip_codes`
cannot be reused for temperatures, student IDs, or scores without renaming
things throughout the code. `_underlying` removes that constraint -- it says
"this is the technical infrastructure" without implying anything about the
values stored. The rule generalizes: implementation internals should use
*structural* names (describing the variable's role in the implementation), not
*domain* names (describing the data's meaning). Domain meaning belongs to the
caller.

**Further reading:**

* [Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables) --
explains the single- and double-underscore conventions and name mangling.

* [Class and Instance Variables](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) --
distinguishes variables shared across all instances from variables unique to each one.

* [Objects](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html) from Bill Lubanovic's book.
---

## Part 3: Accessor Methods

### `__len__` and `get_size`

`__len__` is one of Python's *dunder* (double-underscore) methods. Python calls
it automatically when you write `len(da)`. It should return the number of values
stored -- that is, `_size`. Implementing `__len__` also makes the object
work with truthiness checks: `if da:` is `True` whenever `_size > 0`.

`get_size()` is a regular method that returns the same value. Why have both?
`__len__` integrates with Python's built-in `len()` function and the rest of
the language; `get_size()` is explicit and self-documenting. A reader who
has not memorized Python's dunder protocol immediately understands
`da.get_size()`. Both belong in the public interface.

### `get_size` vs `get_capacity`

`get_size()` returns `_size` -- the count of values stored.

`get_capacity()` returns `_capacity` -- the total number of slots in the
underlying array, including the empty sentinel slots.

These are the hotel analogy from class: size is the guest count; capacity is
the room count. They are equal only when the array is full. `len()` by
convention always means "how many items are in this collection" -- implementing
`__len__` to return capacity would be wrong, because capacity is not the same
as length.

**Further reading:**

* [A First Look at Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes) --
covers class definition syntax, instance methods, and the role of `self`.
* [More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists) --
documents the list methods used by the underlying array in this class.

* [Objects](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html) from Bill Lubanovic's book.
---

## Part 4: Type Hints

Python is a *dynamically typed* language: a variable can hold any type of value,
and Python does not check types when code runs. Type hints (also called type
annotations) are optional labels that say what type of data a variable,
parameter, or return value holds. Python ignores them at runtime, but they serve
two purposes:

- **Documentation.** `def get(self, index: int) -> int:` tells a reader
  immediately what the method accepts and what it returns, without reading the
  body or a comment.
- **Tool support.** Editors and static analyzers (such as `mypy`) read
  annotations and flag type mismatches before the code runs -- catching errors
  earlier than a test run would.

The syntax comes in three forms:

```python
def get(self, index: int) -> int:   # parameter and return type
def __str__(self) -> str:           # return type only
self._size: int = 0                 # instance variable
```

The arrow (`->`) annotates what a method returns. Methods that modify state but
return nothing are annotated `-> None`. In this class, all stored values are
integers, so the underlying list is `list[int]`, all counts and indices are
`int`, and the resize factor is `float`.

Type hints do not replace comments or tests. They describe expected types;
comments explain non-obvious decisions; tests verify that the code produces the
right answers. All three layers belong in well-written code.

**Further reading:**

* [Type hints (typing module)](https://docs.python.org/3/library/typing.html) --
  the reference for Python's `typing` module; covers the built-in types, generic
  aliases (`list[int]`, `tuple[str, ...]`), and `Optional`.

---

## Your Tasks

Implement the five methods below, each currently marked `pass`:

1. `__len__` -- return the number of stored values
2. `get_size` -- return the number of stored values
3. `get_capacity` -- return the total number of slots in the underlying array
4. `get(index)` -- return the value at `index` if `0 <= index < _size`;
   return `-1` for any index outside that range
5. `index_of(value)` -- return the index of the first occurrence of
   `value` among positions `0` through `_size - 1`; return `-1` if not found

---

## Verification

The [`dynamic_array_assignment.py`](./dynamic_array_assignment.py) contains simple test code to verify the correctness of your work.
Each `print` statement in `__main__` has an `# expected:` comment. Your output
should match every expected value. Pay particular attention to:

- `get(-1)` -- a negative index is out of range and must return `-1`, even
  though Python lists accept negative indices natively. A naive implementation
  that skips the bounds check will pass the positive-index tests but fail here.
- `get_size()` vs `get_capacity()` -- after construction with default arguments
  and three `add()` calls, size is `3` and capacity is `4`. After a fifth add,
  size is `5` and capacity has doubled to `8`.

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 03**.

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
