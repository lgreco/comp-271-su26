# COMP 271 -- Last Assignment: SimpleHash

This is the final assignment of the course. It picks up exactly where week 11 left off: an array of linked lists, a hash function that locates a slot in one step, and a resize policy that keeps the table from degrading into a handful of very long chains. It also asks you to step back and reflect honestly on your semester.

---

## Overview

Build a class called `SimpleHash` -- a hash table implemented as an array of linked lists, the same structure the week 11 classes (`2026-07-28-COMP271.md`, `2026-07-29-COMP271.md`) built by hand with the hotel-room metaphor.

- The object has an underlying array. Each array slot can hold the head of a singly linked list of nodes.
- A node's data payload is a string -- a person's name.
- The array location for a name is given by a hash function, using Python's built-in `hash(string)`.
- If the underlying array position is empty, the new node is placed there directly.
- If the position is already occupied, the *existing* linked list is attached after the new node, and the new node becomes the new head of that slot -- insert-at-head, not insert-at-end.
- The object keeps track of how many nodes it holds in total, and how many elements of the underlying array are in use (occupied slots, not total nodes -- a single occupied slot can hold many nodes once chains form).
- When the fraction of occupied array elements exceeds a threshold (default `0.7`, i.e. 70%), the underlying array doubles in size and every stored name is redistributed into the new array.

The stub file [`simple_hash_assignment.py`](./simple_hash_assignment.py) contains the `Node` class (complete -- do not modify it) and the `SimpleHash` class, with every method marked `pass`. Implement:

```python
def _hash(self, name: str) -> int:
def add(self, name: str) -> None:
def exists(self, name: str) -> bool:
def __str__(self) -> str:
def _resize(self) -> None:
```

`get_node_count()`, `get_slots_used()`, and `get_capacity()` are already implemented -- simple accessors, the same pattern as `get_size()`/`get_capacity()` from week 3.

---

## A Short Tutorial: `hash()` and Why We Call `abs()` on It

This course has used `hash()` once before, in passing, during the week 11 classes -- but never as something you call yourself inside a method you write. Here is what you need to know to use it correctly.

Every Python object that can be a dictionary key or a set member has a `hash()` value -- an integer Python computes from the object's contents:

```python
>>> hash("Frodo")
-2013951167291596860
>>> hash("Sam")
5566293414931350648
```

A few things about this that are easy to miss the first time:

- **The exact integer is not something you should predict or hardcode.** Unlike the ASCII-based hash functions from week 11's class (first-letter-of-last-name, or the sum/product functions in `hash_strings.py`), Python's string hash is randomized per process for security reasons -- the same string can hash to a *different* integer the next time you run the program. That's fine for this assignment: you never compare a hash value across two different runs, only within a single running program, against the same `self._capacity` each time.
- **The result can be negative.** Notice `hash("Frodo")` above came back negative. If you take `%` of a negative number directly, Python's modulo still returns a non-negative result (unlike some other languages), but relying on that without thinking about it is the kind of thing worth verifying yourself rather than assuming. The safer, more explicit habit -- and the one used in the week 11 class discussion of why `abs()` shows up before hashing -- is to call `abs()` on the hash value first:

```python
def _hash(self, name: str) -> int:
    return abs(hash(name)) % self._capacity
```

- **Why not just use the first letter, like `HotelAlphabetical.py` did in week 11?** A hash based on one letter can only ever produce 26 distinct values, no matter how big the underlying array grows -- exactly the "wasted rooms" problem from the hotel metaphor. `hash()` spreads strings across the full range of a Python integer, so `% self._capacity` distributes names much more evenly across whatever size the array currently is.

That is the entire new vocabulary this assignment needs. Everything else -- linked-list traversal, insert-at-head, checking a load factor, doubling and redistributing -- is a direct continuation of work already done in weeks 3 (`resize()`), 6 (`Trainline`), and 11 (chaining).

---

## Part 1: `_hash`

Implement `_hash(self, name: str) -> int` using the tutorial above: `abs(hash(name)) % self._capacity`.

**One return statement**, at the very end.

---

## Part 2: `add`

Implement `add(self, name: str) -> None`.

**Contract:**

- Compute the target slot with `self._hash(name)`.
- If `self._underlying[index]` is empty (`None`), place a brand-new `Node` there directly, and increment `self._slots_used` by one -- a previously-empty slot just became occupied.
- If `self._underlying[index]` already holds a chain, do **not** walk to the end of it looking for a place to append. Create a new `Node` whose `next` is the chain's *current* head, and put that new `Node` at `self._underlying[index]` -- it becomes the new head. This is $\mathcal O(1)$ regardless of how long the existing chain is, which is exactly why the week 11 class settled on insert-at-head over insert-at-end.
- Either way, increment `self._node_count` by exactly one -- this tracks total names stored, independent of how many slots are occupied.
- After the insertion, check whether `self._slots_used / self._capacity` has exceeded `self._load_factor`. If it has, call `self._resize()` before the method returns.

This method has no return value.

---

## Part 3: `exists`

Implement `exists(self, name: str) -> bool`.

**Contract:**

- Compute the target slot with `self._hash(name)`.
- Walk the chain at that slot with a cursor, the same cursor pattern `Trainline.contains()` used in week 6: start `result = False`, loop `while not result and cursor is not None`, and set `result = True` the moment a payload matches.
- Return `False` if the slot is empty or the chain is exhausted without a match.

**One return statement**, at the very end.

---

## Part 4: `__str__`

Implement `__str__(self) -> str`.

**Contract:**

- Skip empty slots entirely.
- For every occupied slot, show the slot's index and every name chained there, in head-to-tail order.
- Build the result with a list of string pieces and `str.join()` rather than repeated concatenation inside a loop -- the same reasoning from week 5's `immutability_demo.py`: every `+=` on a string allocates an entirely new string, and `join()` avoids paying that cost once per name.

**One return statement**, at the very end.

---

## Part 5: `_resize`

Implement `_resize(self) -> None`.

**Contract:**

- Create a new underlying array of size `self._capacity * SimpleHash.RESIZE_BY` (double the current capacity), filled with `None`.
- Walk every slot of the **old** array. For every node in every chain, re-hash its payload against the **new** capacity -- a name that hashed to slot 2 in an 8-slot array will very likely hash to a different slot once the array is 16 slots -- and insert it into the new array using the same insert-at-head rule `add()` uses.
- Update `self._capacity` and `self._underlying` to the new size and array.
- Recompute `self._slots_used` to match how many slots are actually occupied in the *new* array. This is not guaranteed to equal the old count: two names that used to land in two different slots could now collide in the same new slot, or two names that used to collide could now land apart.
- `self._node_count` does not change. Resizing moves every node to a (possibly different) slot in a bigger array; it does not add or remove any name.

**Why not just call `add()` for each node during the reinsertion?** `add()` checks the load factor after every insertion and could trigger a second resize in the middle of the first one, which would be both wasteful and hard to reason about. Build the reinsertion loop directly against the new array instead.

This method has no return value.

---

## Verification

After implementing all five methods, run [`simple_hash_assignment.py`](./simple_hash_assignment.py):

```
python3 simple_hash_assignment.py
```

`main()` inserts six names into a `SimpleHash(capacity=4)` and checks:

```python
print(table.exists("Frodo"))     # expected: True
print(table.exists("Sauron"))    # expected: False
print(table.get_node_count())    # expected: 6
```

Because Python's `hash()` is randomized per run, you will not get the exact same slot assignments as a classmate, and `print(table)` will not have one universally "correct" output to compare against -- but the following must always hold, no matter how the six names happen to land:

- `table.get_node_count()` is `6` after all six `add()` calls, regardless of how many resizes happened along the way.
- `table.get_capacity()` is always a power of two times the original `4` -- `4`, `8`, `16`, and so on -- since `_resize()` only ever doubles.
- `table.exists(name)` is `True` for every name you added, and `False` for a name you never added.
- Every name printed by `__str__()` appears in exactly one slot -- never zero, never two.

Edge cases to verify manually:

- Calling `exists()` on a name whose hashed slot has never been occupied returns `False` without crashing (the empty-slot case).
- Adding two names that happen to hash to the same slot in a small-capacity table produces a chain of length 2 at that slot, and both names still `exists()` as `True`.
- Adding enough names to cross the 70% load-factor threshold roughly doubles `get_capacity()`'s return value, and every name added before the resize still returns `True` from `exists()` afterward.

---

## Part 6: A Reflection on Your Semester

Step back from the code and reflect honestly on your semester in COMP 271. This is not a summary of what we covered -- it's an honest self-assessment, and it asks you to propose your own final grade with a justification.

**Write a plain text file**, `reflection.txt` (not a `.py` file -- this is prose, not code), addressing all of the following:

- **Attendance.** How many classes did you attend this term, as best you can recall? Was your attendance a help or a hindrance to how well you learned the material?
- **Participation.** Did you ask questions, work through problems out loud, help classmates, or otherwise engage during class? Or did you mostly observe?
- **Code quality.** Looking back at the posted solutions across the term, how closely did your own submissions match them in approach and correctness? Where did you consistently struggle, and where did you consistently do well?
- **Your proposed final grade.** Based on the three points above, propose the letter grade you believe you earned this semester, and justify it in your own words.

Keep in mind the grading floor set by attendance, and be honest with yourself about where you fall:

- **5 to 9 absences** preclude an **A**, unless those absences are excused by the university police.
- **10 or more absences** preclude a **passing grade**, regardless of code quality or participation.

**Requirements:**

- Maximum **300 words**. Being concise and specific is worth more than being long -- say what actually happened, not what sounds good.
- Submit as a plain `.txt` file, not a `.py`, `.docx`, or `.pdf` file.

---

## How to Submit

Upload your work on **Sakai** under the assignment for the **Final Assignment**, following the same rules as every prior assignment this term.

Submit these files:

```
simple_hash_assignment.py
reflection.txt
```

`simple_hash_assignment.py` must be a Python file -- no screenshots, no PDFs. `reflection.txt` must be a plain text file -- no `.docx`, no `.pdf`. Confirm with `ls` that both files exist before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
