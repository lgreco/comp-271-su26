# Week 6 Assignment: Search, Index, and Count on a Linked Train Line

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
full data structure contract -- `search`, `index_of`, and `count` -- on our
linked line.

---

## Assignment Overview

The stub file [`trainline_assignment.py`](./trainline_assignment.py) contains
a `Trainline` class with `__init__` and `add` already working. Your job is
to implement three missing methods: `search`, `index_of`, and `count`. All
three require traversal -- the same cursor pattern from class.

A fourth part asks you to transform `count` from O(n) to O(1) by adding one
field and one line, then write a short reflection explaining why the change
works.

All your code goes in [`trainline_assignment.py`](./trainline_assignment.py).
Do not modify [`Station.py`](./Station.py).

---

## Part 1: `search`

Implement:

```python
def search(self, target) -> bool:
```

**Contract:**

- Return `True` if any station on the line has the name `target`.
- Return `False` if no such station exists, including when the line is empty.
- Use a cursor that starts at `self._head` and advances via `get_next()`.
- Call `get_name()` to read a station's name. Do not reach into `_name`
  directly.

---

## Part 2: `index_of`

Implement:

```python
def index_of(self, target) -> int:
```

**Contract:**

- Return the 0-based position of the first station named `target`.
  Howard is at index 0, the station after Howard is at index 1, and so on.
- Return `-1` if no station has that name, including when the line is empty.
- Use a cursor and a counter that starts at 0 and increments with each hop.

---

## Part 3: `count` -- Linear Time

Implement:

```python
def count(self) -> int:
```

**Contract:**

- Return the total number of stations on the line.
- Return `0` if the line is empty.
- Use a cursor that starts at `self._head` and counts every station it visits.

---

## Part 4: `count` -- Constant Time

This part has two pieces: a code change and a written reflection.

**Code change.** The traversal in Part 3 is O(n) -- it visits every station
to count them, so doubling the line doubles the work. We can do better. Make
these three changes to [`trainline_assignment.py`](./trainline_assignment.py):

1. Add `self._size = 0` to `__init__`.
2. Add `self._size += 1` inside `add`, so every new station increments the
   counter.
3. Replace the body of `count` with `return self._size`.

After the change, `count` costs exactly one step no matter how long the
line is.

**Reflection.** At the bottom of
[`trainline_assignment.py`](./trainline_assignment.py), below all the code,
add a comment block with your answers to these two questions. Two or three
sentences each is enough.

```python
# Part 4 Reflection
#
# 1. Why is the traversal version of count O(n), and what makes
#    the _size version O(1)?
#
# 2. In class we made a similar trade for add: keeping _tail turned
#    an O(n) traversal into an O(1) pointer update. What do those two
#    changes have in common? What did we give up in each case?
```

---

## Verification

After implementing all three methods (with the Part 4 constant-time change
in place), run [`trainline_assignment.py`](./trainline_assignment.py) and
check your output against the expected values:

```
True
False
3
-1
5
```

---

## Further reading

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods and `self` work, which is the mechanism behind
  every cursor traversal you write here.

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
