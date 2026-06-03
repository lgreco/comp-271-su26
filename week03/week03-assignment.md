# Week 3 Assignment: DynamicArray Accessors

## Overview

The file `dynamic_array_assignment.py` contains a `DynamicArray` class that is
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
it automatically when you write `len(da)`. It should return the number of zip
codes stored -- that is, `_size`. Implementing `__len__` also makes the object
work with truthiness checks: `if da:` is `True` whenever `_size > 0`.

`get_size()` is a regular method that returns the same value. Why have both?
`__len__` integrates with Python's built-in `len()` function and the rest of
the language; `get_size()` is explicit and self-documenting. A reader who
has not memorized Python's dunder protocol immediately understands
`da.get_size()`. Both belong in the public interface.

### `get_size` vs `get_capacity`

`get_size()` returns `_size` -- the count of real zip codes stored.

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
---

## Your Tasks

Implement the five methods below, each currently marked `pass`:

1. `__len__` -- return the number of stored zip codes
2. `get_size` -- return the number of stored zip codes
3. `get_capacity` -- return the total number of slots in the underlying array
4. `get(index)` -- return the zip code at `index` if `0 <= index < _size`;
   return `-1` for any index outside that range
5. `index_of(zip_code)` -- return the index of the first occurrence of
   `zip_code` among positions `0` through `_size - 1`; return `-1` if not found

---

## Verification

The [assignment file](./dynamic_array_assignment.py contains simple test code to verify the correctness of your work. 
Each `print` statement in `__main__` has an `# expected:` comment. Your output
should match every expected value. Pay particular attention to:

- `get(-1)` -- a negative index is out of range and must return `-1`, even
  though Python lists accept negative indices natively. A naive implementation
  that skips the bounds check will pass the positive-index tests but fail here.
- `get_size()` vs `get_capacity()` -- after construction with default arguments
  and three `add()` calls, size is `3` and capacity is `4`. After a fifth add,
  size is `5` and capacity has doubled to `8`.
