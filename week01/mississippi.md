# The Mississippi Problem

> The Python source code for this document is in [mississippi.py](mississippi.py).

## The Problem

Print the word MISSISSIPPI in block letters, where each letter occupies a 10×10
grid of characters. The block character is `*`; empty space is filled with
blanks so every row is exactly 10 characters wide.

## The Introductory Approach: One Function per Letter

The natural first solution in an introductory course is to write one function
per letter, each consisting entirely of `print()` calls:

```python
def m():
    print("*        *")
    print("**      **")
    print("* *    * *")
    print("*  *  *  *")
    print("*   **   *")
    print("*        *")
    print("*        *")
    print("*        *")
    print("*        *")
    print("*        *")

def i():
    print("**********")
    print("**********")
    print("    **    ")
    print("    **    ")
    ...
```

This is a fine starting point. The functions are short, readable, and require
no knowledge beyond the most basic building blocks of a program: a function
definition and a print statement.

To spell out the full word we make one call per letter — eleven in total:

```python
m(); i(); s(); s(); i(); s(); s(); i(); p(); p(); i()
```

> **A note on semicolons.** Python allows multiple statements on a single line,
> separated by semicolons. This document uses that syntax in a few places
> because it keeps short call sequences compact and easy to read at a glance —
> `m(); i(); s()...` scans almost like a pronunciation guide for the word.
> In real code, however, this style is discouraged. The standard Python
> convention (and the rule enforced by virtually every style guide and linter)
> is **one statement per line**. Multiple statements crammed onto one line make
> code harder to read, harder to debug, and harder to step through in a
> debugger. Use the semicolon form only when it genuinely aids clarity in a
> narrow, self-contained context — and even then, think twice.

## Reducing Redundancy by Grouping

MISSISSIPPI contains repeated consecutive subsequences. Rather than writing
those calls out every time, we can name the patterns:

```python
def ss():   # S appears twice in a row
    s(); s()

def pp():   # P appears twice in a row
    p(); p()

def ssi():  # SSI appears twice in a row
    ss(); i()
```

Now the top-level function mirrors the syllable structure of the word:

```python
def mississippi():
    m(); i(); ssi(); ssi(); pp(); i()
```

Six calls instead of eleven. Each repeated pattern is written — and
maintained — in exactly one place.

### Is fewer always better?

Reducing the number of calls is *usually* a good thing, but it is worth being
precise about why. The real goal is not a lower call count for its own sake;
it is **eliminating duplication**. When the same sequence appears in two
places, a future change (fixing a bug, tweaking the shape of S) must be made
in two places, and it is easy to update one and forget the other. Naming the
pattern and calling it once removes that risk entirely.

That said, abstraction has a cost: a reader now needs to know what `ssi()`
means before they can follow `mississippi()`. For a sequence as short and
obvious as SSI the trade-off is clearly worth it. For a contrived grouping
with no natural meaning it might not be. The guiding question is always:
*does this name make the code clearer, or does it just make it shorter?*

## Where the Course Usually Stops

Most introductory courses introduce the problem, arrive at the grouped
solution, and move on. That is understandable — there is a lot of ground to
cover. But the problem is worth revisiting, because the solution above has a
significant hidden limitation that only becomes apparent when you try to do
something slightly different.

## Taking Another Look: Parameterizing Letters as Data

The functions above **mix data and behavior**: the shape of each letter is
baked into a series of print statements. There is no way to ask "what does
row 3 of the letter S look like?" without running the function and reading the
terminal output.

A better representation stores each letter as a **list of strings** — one
string per row. Here are all four letters needed for MISSISSIPPI:

```python
m = [
    "*        *",
    "**      **",
    "* *    * *",
    "*  *  *  *",
    "*   **   *",
    "*        *",
    "*        *",
    "*        *",
    "*        *",
    "*        *",
]

i = [
    "**********",
    "**********",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "    **    ",
    "**********",
    "**********",
]

s = [
    " ******** ",
    "**      **",
    "**        ",
    "**        ",
    " ******** ",
    "        **",
    "        **",
    "**      **",
    " ******** ",
    "          ",
]

p = [
    "**********",
    "**      **",
    "**      **",
    "**      **",
    "**********",
    "**        ",
    "**        ",
    "**        ",
    "**        ",
    "**        ",
]
```

Now a letter is just data. A separate function can decide what to do with
it — print it, measure it, compare it, or combine it with other letters.
This separation of *what a letter looks like* from *what we do with it* is
a foundational idea in software design.

### Printing vertically with lists

With the list representation, printing a letter vertically is a simple loop
over its rows:

```python
def print_vertical(letter):
    for row in letter:
        print(row)
```

To print MISSISSIPPI vertically, we call `print_vertical` for each letter in
the word:

```python
for letter in [m, i, s, s, i, s, s, i, p, p, i]:
    print_vertical(letter)
```

The output is identical to the print-statement version — but now the letter
shapes live in data rather than buried inside function bodies.

## Printing Horizontally

With the print-statement approach, printing MISSISSIPPI horizontally — all
eleven letters side by side on the same 10 lines — is essentially impossible.
The functions produce output immediately and irrevocably; there is no way to
"pause" halfway through printing one letter and move to the next.

With letters stored as lists of strings, horizontal printing becomes possible.
Think about what the output needs to look like:

```
Row 0:  [row 0 of M]  [row 0 of I]  [row 0 of S]  ...  [row 0 of I]
Row 1:  [row 1 of M]  [row 1 of I]  [row 1 of S]  ...  [row 1 of I]
...
Row 9:  [row 9 of M]  [row 9 of I]  [row 9 of S]  ...  [row 9 of I]
```

How would you write a function `print_horizontal(letters)` that produces this
output? What should the outer loop iterate over? What should the inner loop
iterate over? How do you combine the pieces of each row into a single line
before printing it?
