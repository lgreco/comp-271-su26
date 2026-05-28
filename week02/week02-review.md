# COMP 271 — Week 2 Review Notes

These notes cover the class session of May 27, 2026, in which we examined what Python lists actually are under the hood and wrote our first class. The material connects to two chapters in *Introducing Python* (3rd ed.) by Bill Lubanovic: Chapter 8 for lists, and Chapter 11 for objects and classes. Both are available free at [O'Reilly Learning](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/) using your LUC email address. The [Python tutorial's chapter on classes](https://docs.python.org/3/tutorial/classes.html) is a useful second reference for the OOP material.

---

## 1. Arrays and Python Lists: What Is Actually Going On

In most programming languages, an **array** is a fixed block of memory. Every element must be the same type, and the block has a fixed size decided at creation time. If you need room for more elements, you allocate a new block, copy everything over, and discard the old one. In Java, this work is visible and manual — you can see it in the code. Python hides it entirely.

When you used lists in COMP 170, you were using Python's *mutable sequence* type — a structure that grows automatically when you call `append()`. Python is doing the allocation and copying behind the scenes. The list grows, your program runs, and you never had to think about it.

COMP 271 asks you to start thinking about it. Not because Python's convenience is wrong, but because this course is about understanding the choices underneath. Once you know what a fixed-size array is and what it costs to resize one, you are in a position to design your own data structures — and to reason about the trade-offs you are making.

The key distinction in one sentence: a true array has a fixed size and a single element type; a Python list is a dynamic structure that manages its own memory and accepts elements of any type. Lubanovic covers Python lists in Chapter 8. If indexing, slicing, or `append` feel uncertain, read through that chapter before continuing here.

---

## 2. Classes and Objects: Blueprint and Instance

**Object-oriented programming** organizes a program around things rather than steps. Instead of writing a sequence of instructions that manipulate data directly, you define the data and its associated behavior together — and then create as many copies of that bundle as you need.

The vocabulary is specific:

- A **class** is a blueprint. It defines what attributes an object will have and what methods it can perform. The class itself holds no data; it is just the definition.
- An **object** is one specific thing built from that blueprint. Creating an object from a class is called **instantiation**.

A concrete analogy: the blueprint for a house describes the number of rooms, the placement of walls, and the location of doors. The blueprint is not a house — you cannot live in it. But from one blueprint, a contractor can build twenty houses. Each house is a separate physical thing with its own occupants, its own wear on the floors, and its own history. The blueprint is the class; each house is an object.

In Python, you define a class with the `class` keyword:

```python
class DynamicArray:
    pass
```

`pass` is Python's placeholder for an empty block. Python requires that a `class` body contain at least one statement; `pass` satisfies that requirement without doing anything. Once you add `__init__` or any other method, `pass` is removed.

This definition introduces the name `DynamicArray` but creates nothing yet. To build an actual object, you call the class by name:

```python
a = DynamicArray()
b = DynamicArray()
```

Now `a` and `b` are two separate `DynamicArray` objects. They share the same class definition, but they are independent: modifying `a` does not affect `b`. This is the point. If you need to track ten different arrays, you do not write ten separate sets of variables — you instantiate ten objects.

Lubanovic introduces this model at the opening of Chapter 11. He describes an object as a data structure containing both variables (called *attributes*) and code (called *methods*) — a data structure with behavior built in.

---

## 3. `__init__` and `self`: Giving an Object Its Starting State

When Python creates a new object, it immediately calls a special method named `__init__`. This is the **initializer**: it runs once per object, right after the object is created, and its job is to set up the object's initial state.

Here is what `__init__` looks like for the class we built in class:

```python
class DynamicArray:
    def __init__(self):
        self.data = [-1, -1, -1, -1]
        self.size = 0
```

Two things to examine carefully.

**`self`** appears as the first parameter of every method in a class. When you write `a = DynamicArray()`, Python creates a new object and passes it in as `self` automatically. `self` is the name for "this specific object" inside its own method definitions. Writing `self.data` means "the attribute named `data` that belongs to this object." Without `self`, there would be no way to distinguish `a.data` from `b.data` — they would both try to write to the same place.

**`self.data` and `self.size`** are **attributes** — variables that live inside the object and travel with it. `self.data` starts as a list of four `-1` values. We use `-1` as a **sentinel**: a placeholder that signals "this slot is not yet occupied." `self.size` starts at zero and will track how many real values have been placed into the array.

One precision worth holding onto, from Lubanovic's Chapter 11: `__init__` is technically not a constructor. Python already created the object before `__init__` runs — the `__new__` method handles that, invisibly. Think of `__init__` as the *initializer*: the step that gives a freshly created object its starting values. Most of the time this distinction does not matter, but understanding it prevents confusion later when Python's object model comes up again.

---

## 4. `DynamicArray`: A Class in Practice

With `__init__` in place, we added two more methods to complete the class:

```python
class DynamicArray:
    def __init__(self):
        self.data = [-1, -1, -1, -1]
        self.size = 0

    def add_zip_code(self, value):
        if self.size < 4:
            self.data[self.size] = value
            self.size += 1

    def __str__(self):
        return str(self.data[:self.size])
```

### `add_zip_code`

This method inserts a new value. The guard `if self.size < 4` checks whether there is still room. If there is, the value goes into `self.data[self.size]` — the first unfilled slot — and `self.size` is incremented.

Notice that `self.size` does double duty: it is both the *count* of stored elements and the *index* of the next available position. This is not a coincidence — it is a direct consequence of zero-based indexing. If two elements have been stored, they occupy indices 0 and 1. Index 2 is the next open slot. `size` is 2. These are the same number.

When all four slots are full, `self.size` reaches 4, the guard `self.size < 4` is false, and the method does nothing. The fifth call is silently rejected.

### `__str__`

`__str__` is another special method. Python calls it whenever you pass the object to `print()`. Without it, `print(a)` would display something like `<__main__.DynamicArray object at 0x10f2a3b40>` — the object's type and memory address, which is correct but not useful. With `__str__`, we decide exactly what the user sees.

The slice `self.data[:self.size]` extracts only the occupied portion of the internal list, hiding the sentinel values from the output. If two zip codes have been stored, `self.data[:2]` returns just those two.

### Testing the class

We ran this interactively to confirm the behavior:

```python
a = DynamicArray()
a.add_zip_code(60611)
a.add_zip_code(60614)
a.add_zip_code(60647)
a.add_zip_code(60660)
a.add_zip_code(60601)   # no room — silently ignored
print(a)                 # [60611, 60614, 60647, 60660]
```

### The open question

The class is deliberately limited to four slots. The natural next question — posed as the weekend reflection — is what it takes to lift that constraint. Given a list of four elements, can you write plain Python (no `def`, no class) to produce a new list of eight elements, with the original four preserved in the first four positions and `-1` filling the rest? This is the first step toward making `DynamicArray` actually dynamic.

---

---
### Exercise 1 — Tracing `add_zip_code` by Hand

Consider this code:

```python
a = DynamicArray()
a.add_zip_code(60611)
a.add_zip_code(60614)
print(a)
```

Questions:
1. Before running: trace through `__init__` and the two `add_zip_code` calls step by step. What are the values of `self.data` and `self.size` after each call? What will `print(a)` display?
2. After running: was your prediction correct? If it was not, identify the specific step where your mental model diverged.
3. What would happen if you inserted `a.add_zip_code(99999)` between the two existing calls? Would `print(a)` change?

---
### Exercise 2 — `self.size` as an Index

Read the `add_zip_code` method carefully:

```python
def add_zip_code(self, value):
    if self.size < 4:
        self.data[self.size] = value
        self.size += 1
```

Questions:
1. After three calls to `add_zip_code`, what is the value of `self.size`? What index in `self.data` does that number represent?
2. Suppose you swapped the last two lines — incrementing `self.size` before placing `value` into `self.data`. What would go wrong? Trace through one call to show the effect.
3. Why does `self.data[:self.size]` in `__str__` correctly show only the occupied slots?

---
### Exercise 3 — A Deliberate Error: Removing `__str__`

Run the following code with the complete `DynamicArray` class, then modify the class by commenting out the `__str__` method and run it again.

```python
a = DynamicArray()
a.add_zip_code(60611)
a.add_zip_code(60614)
print(a)
```

Questions:
1. What does `print(a)` display when `__str__` is present?
2. What does `print(a)` display when `__str__` is removed? Copy the exact output.
3. The second output is not an error — Python still ran without raising an exception. What does the output tell you about how Python handles objects that have no `__str__` defined? What information is in that default output?

---
### Exercise 4 — The Weekend Reflection: Doubling an Array

Without using `def`, `class`, or `append`, write Python code that takes this list:

```python
data = [60611, 60614, 60647, 60660]
```

and produces a new list of eight elements. The first four positions should hold the original values in their original order; positions four through seven should hold `-1`.

Questions:
1. Write the code. How many lines does it require?
2. Does your approach generalize? If `data` had eight elements and you needed to double to sixteen, what would you need to change?
3. Now imagine `add_zip_code` could call this doubling operation automatically whenever the array is full. What would that mean for the current `if self.size < 4` guard — what should replace it?

---

## Quick Reference Card

```
### Python — Class Definition

class ClassName:
    def __init__(self):          # initializer; runs once when object is created
        self.attribute = value   # attribute: a variable that belongs to this object

    def method_name(self, param): # additional method
        ...

    def __str__(self):           # called by print(); must return a string
        return "..."

# Instantiate an object
obj = ClassName()

# Access an attribute from outside the class
obj.attribute

# Call a method from outside the class
obj.method_name(argument)

### Python — Lists (review)

data = [10, 20, 30]   # create a list with square brackets
data[0]               # access element at index 0 (zero-based)
data[-1]              # last element
data[1:3]             # slice: elements at indices 1 and 2
data[:n]              # first n elements
len(data)             # number of elements
data.append(x)        # add x to the end (grows the list)

### Sentinel Pattern

EMPTY = -1
data = [EMPTY, EMPTY, EMPTY, EMPTY]   # all slots initialized to sentinel
# A slot is "occupied" when its value is not EMPTY
```
