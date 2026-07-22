# Week 10 Assignment: Data Structures With No Data Structure

## This Week in Class

### July 21 -- Designing a Queue Backed by Files

We opened with a detour into technical interviews: how companies like Google increasingly expect fluency with AI tools rather than memorized syntax, and how interviewers deliberately ask vague, evolving questions ("build a queue using files only," then "no, make it cloud-based") to see how a candidate reasons from an imperfect starting point rather than to get a finished solution out of them.

That became the shape of the class problem: build a queue -- first in, first out -- using only files, no lists or arrays anywhere. We first visualized a queue's possible states: empty, partially full, and full to capacity, then mapped those onto a file. An empty queue is a file of 0 bytes. With Alexander's suggestion of "just a blank file," we then had to define a length unit for a non-empty queue -- counting bytes, counting lines, or counting whole serialized-object blocks (a passenger record with a first name, last name, reservation code, and flight date, wrapped in opening and closing tags the way XML or JSON would) were all on the table. We settled on counting lines, one queue item per line, for our simplified string-based version.

We then reasoned through the two core operations. Adding an item is straightforward: create the file if the queue is empty, otherwise append to the end. Removing the first item is harder, since a file has no way to delete a single line directly. With Temeeka's help, we arrived at a strategy: read through the file line by line, hold onto the first line separately, write every remaining line into a temporary file, then swap the temporary file in as the queue file.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on instance methods and `self`, the mechanism behind the
  `FileQueue` class this session's design became.

---

### July 22 -- Magic Values, Constants, and Finishing enqueue/dequeue

We continued building the file-backed queue, starting from a constructor with a hard-coded file name and capacity -- magic values, literals with no explanation for where they came from. We replaced them with named constants (`DEFAULT_FILE_NAME`, `DEFAULT_CAPACITY`), letting the constructor accept a user-specified file name and capacity while falling back to those defaults when neither is given. We noted that by convention, uppercase names signal "this is a constant," but Python cannot actually stop a program from reassigning one -- that enforcement relies on programmer discipline, not the language. To make the point concrete, we used JShell and a compiled Java program to show that Java's `final` modifier truly blocks reassignment at compile time; Python has no equivalent, so we "rely on the we are all adults here principle."

With the file created in the constructor, we wrote `is_full()` by comparing size to capacity, then `enqueue()`, which opens the file in append mode and writes the payload followed by a newline, incrementing size on success -- simplified to return directly from the fullness check rather than through an intermediate variable. `dequeue()` was more involved: read the first line as the front of the queue, copy every remaining line into a temporary file, close both files, and swap the temporary file in as the new queue file, since a plain text file has no way to remove just its first line directly. We closed by discussing where to draw the line on magic values: mode strings like `"w"`, `"r"`, and `"a"` are technically string literals too, but since they are documented in Python's own reference, treating them as an acceptable exception is a matter of style rather than a hard rule.

**Further reading:**

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  background on instance methods and `self`, relevant to every method
  built this week.

---

## Overview

This week's queue design -- read the front line, copy the rest to a temp file, swap the temp file in -- is the same idea a *file-backed stack* [`stackq.py`](./stackq.py) already uses, except a stack has to find its top at the *other* end of the file, since last in, first out means the newest item is whichever line was written most recently.

Two tasks this week, both continuing the "no lists, no arrays, the file itself is the container" theme from class.

---

## Part 1: A Front-Loaded Stack

[`stackq.py`](./stackq.py) currently implements `FileStack` with the top of the stack living at the file's *last* line: `push()` appends, and `pop()` has to read one line ahead of the line it is about to commit, because a sequential reader has no way to know a line is last until it tries to read the next one and finds nothing there. `peek()` pays the same cost, scanning to the end for the same reason.

Your job is to flip which end of the file holds the top of the stack: rewrite `push()`, `pop()`, and `peek()` so the top of the stack is the file's *first* line instead.

Implement:

    def push(self, item: str) -> bool:
    def pop(self) -> str | None:
    def peek(self) -> str | None:

**Contract:**

* `push()` still returns `False` immediately, without writing anything, when the stack is already at capacity.
* Otherwise `push()` makes `item` the new first line of the file, shifting every line already there down by one position underneath it.
* `pop()` returns `None` immediately, without touching the file, when the stack is empty; otherwise it removes and returns the first line, shifting everything after it up by one position.
* `peek()` returns the exact same value `pop()` would remove, without removing it.
* `size()`, `is_empty()`, `is_full()`, `__bool__()`, and `__len__()` are unchanged -- they only count lines, and the stack has exactly as many lines no matter which end holds the top.

**Notice which half got harder and which got easier.** A file can only ever be written to at its current end -- there is no way to insert at the front of a file directly. Getting `item` to the front on `push()` means building a new file that starts with `item` and then copying every line already on the stack after it, one at a time -- the same "build a new file, then swap the two filenames" idiom `pop()` already uses in the current version, just run for a different reason. `pop()`, meanwhile, becomes the *easier* of the two: reading and discarding the first line, then copying everything that remains, is exactly the shape of `FileQueue.dequeue()` from class. The old version's "read one line ahead" trick, needed because the last line only reveals itself once `readline()` comes back empty, is not needed by either method anymore -- but it has to go *somewhere*, and it lands squarely in `push()` instead.

**Same public behavior, different mechanism.** This rewrite changes nothing about what `FileStack` does from the outside -- it is still last in, first out. `main()` in [`stackq.py`](./stackq.py) is untouched, and every expected value in its comments still holds. If your rewritten stack produces a single different value there, the rewrite broke the stack's contract, not just its internals.

**One return statement.** Each of the three methods above must have exactly one `return`, at the very end.

---

## Part 2: A Doubly Linked List, Built From Files Alone

Every linked list this course has built so far -- singly linked, doubly linked, circular -- has lived entirely in memory: `Node` objects holding references to other `Node` objects. This part asks the same question the file-backed stack and queue already asked, pointed at a doubly linked list instead: what does "a node" mean when the only thing available to hold state is a file, and there is no `Node` class, no list, no array anywhere in the solution?

Write this as a new file, [`filell.py`](./filell.py).

**The file format.** Every node -- including the head and the tail -- is a plain text file with exactly three lines:

```
payload
next_filename
prev_filename
```

`payload` is the node's data (a simple string is enough). `next_filename` and `prev_filename` are the *names* of the files holding the next and previous nodes -- a blank line means "no such neighbor." Every method that reads a node file reads exactly these three lines, in this order, every time.

**Two special files always exist: `head.txt` and `tail.txt`.** They are not pointers *to* the first and last node -- they *are* the first and last node's storage. Everything strictly between them, once the list has three or more nodes, lives in a randomly generated filename instead.

On instantiation, both files are created empty and the list's size is 0.

Once a single node is added (size == 1), that one node is simultaneously the head and the tail, so its data is written into *both* files:

```
head.txt                tail.txt
initial_payload          initial_payload
(empty line for next)   (empty line for next)
(empty line for prev)   (empty line for prev)
```

After a second node is added (size == 2), `head.txt` keeps the first payload but now points forward to `tail.txt`, and `tail.txt` holds the new payload, pointing back to `head.txt`:

```
head.txt              tail.txt
initial_payload        second_payload
tail.txt               (empty line for next)
(empty line for prev)  head.txt
```

After a third node is added (size == 3), the node that used to live directly in `tail.txt` moves out into a randomly named file, and `tail.txt` is overwritten with the newest payload:

```
head.txt                 random_file_name.txt      tail.txt
initial_payload           second_payload             third_payload
random_file_name.txt      tail.txt                   (empty line for next)
(empty line for prev)     head.txt                    random_file_name.txt
```

Work out for yourself why `head.txt` needed to hold a redundant copy of the first node's data at size 1, and why that redundancy is exactly what lets the second `add()` overwrite `tail.txt` without losing anything. The same question applies going the other direction: what has to happen to these files when `remove()` brings the list back down from size 2 to size 1, or from size 3 to size 2?

**Naming intermediate files.** A file name for an intermediate node is a random 8-character string of upper- and lower-case letters only. Because two different random names could in principle collide, maintain a separate file listing every node filename currently in use, and check a freshly generated name against it before using that name.

**No lists, arrays, or other in-memory containers anywhere in the file.** Every method reads or writes one line, or one file, at a time.

Implement:

    def __init__(self) -> None:
    def add(self, payload: str) -> None:
    def remove(self, payload: str) -> bool:
    def size(self) -> int:
    def is_full(self) -> bool:
    def is_empty(self) -> bool:
    def __str__(self) -> str:
    def filelist(self) -> str:
    def clear(self) -> None:

**Contract:**

* `__init__()` -- if `head.txt` and `tail.txt` do not already exist in the current folder, create both empty and start the list at size 0, exactly as described above. If they *do* already exist (a previous run of the program left them behind), reconstruct the list's size by walking the chain from `head.txt` to `tail.txt` instead of resetting it -- the list's state lives entirely on disk, so a fresh Python process should be able to pick up exactly where the last one left off.
* `add()` always appends after the current tail -- there is no "insert at a position" operation in this part of the assignment.
* `remove(payload)` searches from `head.txt` toward `tail.txt` for the first node whose payload matches, removes it, and returns `True`; returns `False` without changing anything if no node matches.
* `is_full()` always returns `False`. This structure has no fixed capacity -- unlike the array-backed `Stack`/`Queue` from week 8, a node here is just another file, and nothing here caps how many files can exist.
* `filelist()` returns the filenames from `head.txt` to `tail.txt`, in traversal order, as a single string -- this exposes the *implementation* (which files exist and in what order).
* `__str__()` returns the *payloads* from head to tail, in traversal order, as a single string -- this exposes the *abstraction* (what the list actually holds), the same separation `filelist()` vs. `__str__()` draws for every other collection built this course.
* `clear()` removes every underlying file -- `head.txt`, `tail.txt`, the filename registry, and every intermediate node file -- then recreates `head.txt` and `tail.txt` empty, so the list is left in the exact same state a brand-new instantiation would produce.

**One return statement.** `remove()`, `size()`, `is_full()`, `is_empty()`, `__str__()`, and `filelist()` must each have exactly one `return`, at the very end.

---

## Part 3: Reflection -- Comparing Your Week 9 Work with the Solutions

This part has no new code to write. Open your week 9 submission alongside [`../week09/week09_solutions.py`](../week09/week09_solutions.py) and compare what you wrote with what the solutions contain. Write your answers as comments at the very bottom of [`stackq.py`](./stackq.py), beneath `main()`, so they are included when you submit. A few sentences per question is enough.

```python
# Part 3 Reflection
#
# 1. The solution's better_reachability introduces exactly one new piece
#    of state beyond naive_reachability -- a single boolean, path_exists,
#    starting False and flipped to True the moment target is visited --
#    and folds it into the while loop's own condition (`while
#    len(explore_next) > 0 and not path_exists:`) instead of using a
#    break statement. Did your better_reachability stop the loop the
#    same way, through the while condition, or did you reach for
#    break to exit early? If you used break, what would it take to
#    rewrite your version so the while condition alone decides when to
#    stop?
#
# 2. The solution only appends a vertex's neighbors to explore_next
#    when that vertex was NOT the target (the else branch after
#    `if vertex_to_explore == target:`). What was the consequence, in
#    your own version, of queuing neighbors unconditionally even after
#    the target had already been found -- did it change the final
#    answer, or only how much unnecessary work the loop did before
#    stopping?
#
# 3. naive_reachability and better_reachability return target in visited
#    and path_exists respectively -- two different variables answering
#    the identical question, "was the target ever visited?" Did your
#    solution compute that answer the same way naive_reachability does
#    (checking membership in visited at the very end), or did you track
#    it incrementally the way path_exists does? What tradeoff, if any,
#    do you see between the two approaches?
```

---

## Verification

**Part 1.** Run [`stackq.py`](./stackq.py) directly:

```
python3 stackq.py
```

Every printed value must match the expected comments already in `main()` -- `True`, `False`, `True`, `True`, `True`, `True`, `False`, `C`, `3`, `3`, `C`, `B`, `A`, `None`, `True`, `False` -- unchanged from before your rewrite. Then confirm the mechanism actually changed: after `stack.push("A")`, open `stackq_demo.txt` in a text editor (or `cat` it) and check that `A` is on the *first* line, not the last.

**Part 2.** A short smoke test for `filell.py`:

```python
from filell import FileLinkedList

fll = FileLinkedList()
print(fll.is_empty())          # expected: True
print(fll.size())               # expected: 0

fll.add("first")
print(fll.size())               # expected: 1
print(fll.__str__())            # expected: first

fll.add("second")
fll.add("third")
print(fll.size())               # expected: 3
print(fll.__str__())            # expected: first -> second -> third (or your chosen separator)
print(fll.filelist())           # expected: head.txt -> <random>.txt -> tail.txt

print(fll.remove("second"))     # expected: True
print(fll.size())                # expected: 2
print(fll.remove("second"))     # expected: False -- already removed

fll.clear()
print(fll.is_empty())            # expected: True
print(fll.size())                 # expected: 0
```

Then, separately, confirm recovery: run a script that creates a `FileLinkedList`, adds two or three items, and exits *without* calling `clear()`. Start a fresh Python process in the same folder, instantiate a new `FileLinkedList()`, and confirm `size()` reports the same count the previous process left behind, without you having called `add()` again.

---

## Further reading

* [The Python Tutorial -- Classes](https://docs.python.org/3/tutorial/classes.html) --
  covers how instance methods and `self` work, background for both
  `FileStack` in [`stackq.py`](./stackq.py) and `FileLinkedList` in
  [`filell.py`](./filell.py).

---

## How to Submit

Upload your work on **Sakai** under the assignment for **Week 10**.

Submit only your Python files:

```
stackq.py
filell.py
```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that both files exist before you upload.

---

## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
