# COMP 271 -- Course Review, Summer 2026

The course ran for eleven weeks, from a fixed-capacity array wrapped in a first class to a hash table built out of an array of linked lists. This document looks back at that arc, with particular attention to how the course built up its own recurring themes -- **arrays, linked structures, complexity analysis, and abstraction through contracts** -- and what, given eleven weeks, there simply wasn't time to cover.

---

## 1. Course Progression

### Weeks 1-2: From behavior to data, then from list to class

Week 1 was not about data structures at all -- it was about a single habit that shapes everything after it: **separating data from behavior, and logic from I/O**. The Mississippi progression (`mississippi.py` -> `block_letters.py` -> `mississippi_horizontal.py`) made the point concretely: as long as a letter's shape is baked into `print()` calls, you cannot pause mid-letter and interleave output with another letter. Once a letter is a list of strings, you can. `pasta.py` made the same point about a program's other seam -- input, computation, and display each belong in their own function, and only `main()` should call all three.

Week 2 turned this into the course's first real data structure question: what is a Python list actually doing when it grows? Class distinguished a true array (fixed size, single type, manual resizing) from Python's dynamic list, then wrote the first `DynamicArray` class -- a fixed-size list of four sentinel `-1` values, with `add_zip_code()` refusing a fifth insertion. This is also where object-oriented programming entered the course: a class as blueprint, an object as instance, `__init__` as initializer (not quite a constructor), and `self` as "this specific object."

### Week 3: Resizing, magic numbers, and encapsulation

Week 3 lifted the four-slot ceiling with `resize()`: allocate double the capacity, copy every element over, replace the old array. This is where the course named its first code smell, **magic numbers** -- any bare literal other than `-1`, `0`, or `+1` -- and replaced them with `DEFAULT_CAPACITY` and `DEFAULT_RESIZE_BY`. A live bug (`int(3 * 1.1)` flooring to `3`, so a 10% growth factor never actually grew the array) motivated `math.ceil()` over `int()` for rounding. The internal list was renamed from `_zip_codes` to `_underlying` -- the first lesson in **structural versus domain naming**, and in the leading-underscore convention Python uses for "please don't reach in here directly."

### Week 4: Dunder methods, bounds checking, and delegation

Week 4 introduced `__len__` and `__str__` as **dunder methods** Python wires to built-in behavior, and fixed a real trap: Python's native negative indexing meant `get(-1)` would silently return the last element unless the bounds check explicitly rejected `index < 0`. The class also learned **delegation** as a design habit -- `contains()` collapsed from its own search loop into a single call to `index_of()`, and later `count()` collapsed into `len(index_of_all(value))`. `remove()` closed the week, introducing the shift-left-then-clear pattern that keeps a dynamic array's filled region contiguous after a deletion.

### Week 5: Contracts, composition, and the first linked node

Week 5 named the idea that had been implicit since week 4: every data structure the course would build should expose the same handful of methods -- `contains`, `index_of`, `index_of_all`, `count`, `remove`. In Python that agreement is an **abstract base class**; `@abstractmethod` makes Python refuse to instantiate a class that skips one. `FellowshipRoster` then demonstrated **composition over inheritance** -- it *has a* `DynamicArray` rather than *is a* `DynamicArray`, and its own methods only ever call the array's public contract, never its internals. The week also covered string immutability (`str.join()` over repeated concatenation) and previewed the shape of everything to come: `station.py`, a small object whose field points to another object of the same class.

### Week 6: Linked traversal, tail pointers, and Big O

Week 6 built `TrainLine` on top of the station object, and immediately hit the cost of not knowing where a list ends: adding the $n$th station required $n$ hops -- $\mathcal O(n)$. Adding a second pointer, `_tail`, brought that down to $\mathcal O(1)$ regardless of length -- a small, explicit memory-for-speed trade the course would repeat all term. This is also where **Big O and Big Theta** were formalized as an upper bound versus a tight, two-sided bound, and where the full data-structure contract from week 5 was implemented on a genuinely linked structure for the first time, including `__iter__` via `yield`.

### Week 7: Generic nodes, doubly linked lists, and O(1) tricks

Week 7 generalized `Node` with `TypeVar`/`Generic` so a node's payload could be any type, then built a `DoubleLinkedList` with both `next` and `previous` pointers. The recurring pattern of the week was **turning an $\mathcal O(n)$ query into an $\mathcal O(1)$ read by maintaining extra state on every insert** -- a count field made finding the middle node possible in one step instead of a slow/fast-cursor race, the same way `_tail` had done for `add()` the week before. The assignment pushed this further: detecting a broken bidirectional link (`is_continuous`), detecting a cycle without traversal on a well-maintained list (`has_loop_unidirectional`, `has_loop_bidirectional`), and reversing a forward-only list in place by rewiring pointers rather than rebuilding.

### Week 8: Constant-time ends, recursion, and a shared superclass

Week 8 finished the doubly linked list's remaining constant-time operations -- removing the head or the tail in three pointer updates, regardless of size -- and used that as the bridge into **stacks and queues**. The week also introduced recursion properly: the loop-based factorial next to the recursive $n! = n \times (n-1)!$, a maximum-recursion-depth crash as the natural way to discover that recursive calls live on a stack, and a role-play modeling the call stack as pending requests resolved last-in-first-out. `BoundedCollection` then generalized `Stack` and `Queue` as **inheritance** (not composition, this time): both share `is_empty`, `size`, `peek`, and a single `_add`/`_remove` pair, differing only in which end of the array each operation targets.

### Week 9: Circular buffers and graphs

Week 9 closed the loop on why linked lists beat arrays for stacks and queues -- array-backed insertion or removal at the front costs $\mathcal O(n)$ in shifting, no matter how carefully the shifting loop is written -- then recovered array-level memory efficiency with **circular buffers**: front and back pointers that advance by $(\text{position} + 1) \bmod \text{capacity}$ instead of shifting data. The same modular idea reappeared immediately in a new subject, **graphs**: vertices, edges, the reachability question, and two representations of the same graph (adjacency list, adjacency matrix). The assignment asked students to stop a reachability search the moment the target is found, rather than only when there is nothing left to explore -- the same "smallest new piece of state, updated in exactly one place" idea that had powered week 7's constant-time middle-node lookup.

### Week 10: Data structures with no data structure

Week 10 asked what a queue, a stack, and a doubly linked list look like when the only thing available to hold state is a **file** -- no list, no array, no `Node` class anywhere in the solution. A file's inability to delete a single line directly forced a recurring idiom: read what you need, write everything else to a temporary file, then swap the temp file in. The file-backed doubly linked list pushed this furthest, using two fixed files (`head.txt`, `tail.txt`) as the list's true anchors and randomly named files for everything in between -- the same head/tail/pointer vocabulary from week 6 and 7, translated into a medium with no pointers at all.

### Week 11: Hashing

The final synchronous week introduced hashing through a hotel-room metaphor: assign a guest a room from a hash of their last name for $\mathcal O(1)$ lookup, then confront what happens when two guests hash to the same room. Probing (take the next open room) gave way to **chaining** -- a linked list hanging off every array slot, recognized as nothing more than an array of the linked lists the course had already built in week 6. The week closed by naming Python's `dict` as exactly this structure, previewing the **load factor** and resize-and-rehash policy the final assignment asks students to implement themselves.

### The recurring themes, end to end

| Theme | First introduced | Recurred |
|---|---|---|
| Arrays and fixed capacity | Week 2 (`DynamicArray`) | Weeks 3-4 (resize, remove), Week 8 (`BoundedCollection`), Week 9 (circular buffers), Week 11 (hash table's underlying array) |
| Linked structures (pointers over shifting) | Week 5 (`station.py` preview) | Week 6 (`TrainLine`), Week 7 (doubly linked list), Week 8 (O(1) head/tail removal), Week 10 (file-backed list), Week 11 (chaining) |
| Complexity analysis ($\mathcal O$, $\Theta$) | Week 6 | Weeks 7-9 (O(1) middle node, O(1) loop detection, circular buffers, reachability), Week 11 (load factor) |
| Abstraction and contracts | Week 5 (`abc`, composition) | Week 6 (contract on a linked list), Week 8 (inheritance via `BoundedCollection`) |

By week 6, no theme stood alone -- every new structure combined at least two, and the final hash table asks for all four at once: an underlying array (theme 1) of linked lists (theme 2), sized and resized by a load-factor threshold (theme 3), exposing the same handful of methods the course has asked every structure to expose since week 5 (theme 4).

---

## 2. What the Course Didn't Have Time For

Eleven weeks was enough to build real fluency with arrays, linked structures, stacks, queues, and hashing -- and to reason carefully about the cost of each. It was not enough to survey everything a second data-structures course usually touches. A few gaps worth naming, and pursuing on your own if you want to go further before COMP 272:

- **Sorting algorithms.** We talked about simple sorting in $\mathcal O(n^2)$  and $\mathcal O(nlog_2n) but we did not explore their mechanisms at depth
- **Trees.** Binary search trees, heaps, and tree traversal never appeared, even though the linked-node vocabulary built in weeks 6-7 (a payload plus one or more pointers to other nodes) is exactly the machinery a tree needs. This is very likely one of the first topics in COMP 272.
- **Named graph traversal algorithms.** Week 9 built reachability by hand, using a queue-like list under the hood -- but the terms *breadth-first search* and *depth-first search* were never used, and depth-first traversal (using a stack instead of a queue) was never built as its own exercise.
- **Recursion beyond factorial and mergesort.** Week 8 introduced recursion and the call stack, and we talked about mergesort implemented recursively, but the course never returned to recursion for a genuinely recursive data structure (a tree, or a recursive definition of a linked list itself).
- **Inheritance and polymorphism, in depth.** Week 8's `Vehicle`/`Car` example and `BoundedCollection` introduced plain inheritance, but polymorphism -- one method call behaving differently depending on the object's actual subclass -- was only touched, not built as its own exercise.
- **Systematic testing.** Every assignment this term included worked verification code with expected output in comments, but the course never introduced `assert` statements or Python's `unittest` module as tools students write themselves, the way COMP 170 did in its own week 8.
- **Recurrence relations and formal algorithm analysis.** Big O and Big Theta were introduced and used constantly, but always informally -- counting hops, counting shifts. Setting up and solving a recurrence (the way $T(n) = 2T(n/2) + n$ describes a divide-and-conquer algorithm's cost) never appeared. These topics are covered in COMP 363.
- **Open addressing beyond linear probing.** Week 11 named linear probing on the way to chaining, but did not build it, and never mentioned quadratic probing or double hashing as alternatives.

None of these are urgent -- arrays, linked structures, complexity reasoning, and contracts are the load-bearing skills, and everything above builds on top of them. But if you are looking for the highest-leverage next step before COMP 272 (which covers non-linear data structures in Java), trees and named graph-traversal algorithms are probably it: COMP 272 will assume you can read and write recursive, node-based structures fluently, and this term's linked-list work is the closest run-up you have had.
