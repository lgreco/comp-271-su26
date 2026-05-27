# COMP 271 — Week 1 Review Notes

These notes cover the tools we set up this week and connect the programming ideas we discussed to code you have already seen — or will see again.

---

## 1. Terminal and `vim`

If any of the commands or editor mechanics from this week felt unfamiliar, the resources below are worth bookmarking. They are the same tools you used in COMP 170, but now you will use them more fluently and for longer programs.

**Terminal / Bash:**
- [Learning the Shell — linuxcommand.org](https://linuxcommand.org/lc3_learning_the_shell.php) — the clearest free introduction; start here if anything felt shaky
- [The Unix Shell — Software Carpentry](https://swcarpentry.github.io/shell-novice/) — structured lessons with exercises; skip the setup section if your environment is already working
- [The Missing Semester of Your CS Education: The Shell — MIT](https://missing.csail.mit.edu/2020/course-shell/) — a concise lecture with video; good for filling in gaps quickly

**Vim:**
- [OpenVim — interactive Vim tutorial in the browser](https://www.openvim.com/) — no installation; practice the motions without leaving your browser
- `vimtutor` — type this in your terminal for a built-in 30-minute walkthrough; it is available on every Unix system
- [Vim reference card — Vim Tips Wiki](https://vim.fandom.com/wiki/Category:VimTip) — searchable collection of tips and patterns

At the COMP 271 level, the goal is fluency: you should be able to open, edit, and close files without thinking about the editor. If you are still pausing to remember `:wq`, spend fifteen minutes with `vimtutor` this week.

---

## 2. Two Programs You Have Seen Before

In COMP 170, we ask students to write two programs that most introductory courses treat as finished exercises: *Hello, World* and *Mississippi*. You may also have encountered *The House that Jack Built*. In each case, the course arrived at a working solution and moved on.

That is the right choice for COMP 170 — the goal there is fluency with the basics. But COMP 271 asks a different question: *what does the same program look like once you know more?*

The answer reveals something important: **correctness is the floor, not the ceiling**. A program that produces the right output is necessary but not sufficient. As programs grow, the qualities that matter are readability, maintainability, and testability — and those require deliberate design choices.

---

### Hello, World

Here is the version you likely wrote in COMP 170:

```python
print("Hello, World!")
```

And here is a slightly more structured version — perhaps what you wrote by the end of week 1:

```python
def demo():
    print("Hello World")

demo()
```

Both are correct. The second one introduces a function, which is already one step of abstraction. But notice what `demo()` cannot do:

- It cannot return the greeting so another function can use it.
- It cannot take a name as input and greet that name.
- It cannot be tested without capturing stdout.

The function is defined, but it still mixes *producing a value* with *displaying it*. A version that separates those concerns would look like this:

```python
def greeting(name: str) -> str:
    return f"Hello, {name}!"

def main():
    print(greeting("World"))

if __name__ == "__main__":
    main()
```

Now `greeting` is a pure function: it takes a string, returns a string, and touches nothing outside itself. You can call it from a test, from a web handler, or from another function — without printing. `main` owns the I/O.

This is a small program, so the difference feels academic. On a 500-line program, the difference is the gap between code you can change safely and code you are afraid to touch.

---

### The House that Jack Built

The notebook `house_that_jack_built.ipynb` traces this program through five versions. The rhyme has a naturally cumulative structure — each stanza repeats everything before it and adds one phrase — and that structure makes it a useful vehicle for exploring progressively more powerful tools.

The five versions in brief:

| Version | Tool introduced | What it gains |
|---|---|---|
| 1 — Naive | `print()` only | Works. Simple to read. Cannot be extended without copy-paste. |
| 2 — Loop | `for` + `if` thresholds | Adding a stanza is a one-line change instead of a full block. |
| 3 — Recursion | Recursive function | Code structure mirrors the mathematical structure of the problem. |
| 4 — List | List of phrases + index arithmetic | Data lives in one place; the loops are generic and length-agnostic. |
| 5 — Functions | Pure functions, `main()`, `__name__` guard | Each function has one job; the logic is testable and reusable in isolation. |

The output is identical in all five versions. The progression is not about making the program *work*; it is about making it *easy to read, change, and reuse* as programs grow.

Read the notebook and pay attention to the commentary between versions. The key transitions are:
- **Version 1 → 2**: recognizing repetition and replacing it with a loop.
- **Version 3**: noticing that the problem's *structure* is recursive and writing code that reflects that.
- **Version 4**: the first time *data* and *logic* are separated. The phrases are no longer buried inside functions — they live in a list that the functions consume.
- **Version 5**: the organizational step. Pure functions, a single entry point, and the `__name__` guard are habits, not clever tricks. They cost almost nothing and pay off when you return to the code months later.

---

### Mississippi

The `mississippi.md` and `mississippi.py` files cover this problem in detail. The short version:

**COMP 170 endpoint:** One function per letter, each consisting entirely of `print()` calls. Then grouping functions (`ss()`, `pp()`, `ssi()`) that call the letter functions in sequence. The top-level call reads almost like a pronunciation guide:

```python
def mississippi():
    m(); i(); ssi(); ssi(); pp(); i()
```

This is clean and readable. But it has a hidden limitation: the letter shapes are *behavior*, not *data*. There is no way to ask what row 3 of the letter S looks like without running the function and reading the terminal.

**The COMP 271 step:** Store each letter as a list of strings — one string per row. Now a letter is data that a function can consume.

```python
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

def print_vertical(letter):
    for row in letter:
        print(row)
```

The output is identical. But now you can also write `print_horizontal` — something that was essentially impossible with the print-statement approach, because functions that print cannot be "paused" and interleaved with other output. When letter shapes are data, you can iterate over corresponding rows of multiple letters simultaneously.

The Mississippi progression is a concrete illustration of why **separating data from behavior** matters. `mississippi.md` develops this in full; read through to the horizontal printing section.

---

## 3. `pasta.py`: Separating I/O from Logic

Here is the current state of `pasta.py`:

```python
AMOUNT_PER_PERSON: float = 0.75  # cup
BASE_WATER: float = 1.5          # liters for one person
WATER_PER_GUEST: float = 0.5    # liters per additional person

def pasta_recipe(number_of_guests: int):
    amount_of_water: float = BASE_WATER + (number_of_guests - 1) * WATER_PER_GUEST
    amount_of_pasta: float = number_of_guests * AMOUNT_PER_PERSON
    return amount_of_water, amount_of_pasta

# Example usage
guests = 4
water_needed, pasta_needed = pasta_recipe(guests)
print(f"For {guests} guests, you will need {water_needed:.2f} liters of water and {pasta_needed:.2f} cups of pasta.")
```

`pasta_recipe` is already doing something right: it computes values and *returns* them rather than printing them directly. That is the most important step.

But the code around it has a problem. The last three lines — assigning `guests`, calling the function, and printing — are floating at module level with no structure around them. This creates two specific issues:

**1. The input is hardcoded.** `guests = 4` is not I/O; it is a constant pretending to be input. Anyone who wants to use this program for a different party size must edit the source file. Real input comes from the user at runtime, not from a literal in the code.

**2. There is no separation between the script runner and the display logic.** The `print` statement is at module level, tangled with the call to `pasta_recipe`. If you ever want to embed this logic in a web form, write the output to a file, or test the display format independently of the computation, you cannot — it is all one flat block.

**3. There is no `__name__` guard.** If another module imports `pasta_recipe` to use in a larger program, the print statement will fire immediately on import. That is almost never what you want.

### A revised version

```python
AMOUNT_PER_PERSON: float = 0.75  # cup
BASE_WATER: float = 1.5          # liters for one person
WATER_PER_GUEST: float = 0.5    # liters per additional person


def pasta_recipe(number_of_guests: int) -> tuple[float, float]:
    """Compute water (liters) and pasta (cups) for the given number of guests."""
    water = BASE_WATER + (number_of_guests - 1) * WATER_PER_GUEST
    pasta = number_of_guests * AMOUNT_PER_PERSON
    return water, pasta


def get_guests() -> int:
    """Read and return the number of guests from the user."""
    return int(input("How many guests? "))


def display_recipe(guests: int, water: float, pasta: float) -> None:
    """Print the recipe for the given inputs and computed quantities."""
    print(
        f"For {guests} guests, you will need "
        f"{water:.2f} liters of water and {pasta:.2f} cups of pasta."
    )


def main() -> None:
    guests = get_guests()
    water, pasta = pasta_recipe(guests)
    display_recipe(guests, water, pasta)


if __name__ == "__main__":
    main()
```

The structure now reflects three distinct concerns:

| Function | Concern | Can be tested by... |
|---|---|---|
| `pasta_recipe` | Logic — computes quantities | Calling it with known inputs and checking the return values |
| `get_guests` | Input — reads from the user | Mocking `input()` in a test |
| `display_recipe` | Output — formats and prints | Calling it with known inputs and checking stdout |
| `main` | Orchestration — wires the three together | Running the program end to end |

Notice what this structure buys you:

- You can test `pasta_recipe(6)` in isolation without triggering any I/O.
- You can change the display format (say, switch from metric to imperial) by editing only `display_recipe`.
- You can swap the input source (say, read from a command-line argument or a GUI field) by changing only `get_guests`.
- Importing this module in another file will not print anything.

The logic — the computation — did not change at all. What changed is the organization of everything around it.

---

## The Through-Line

Every example this week — Hello World, House that Jack Built, Mississippi, pasta.py — is a variation on the same theme:

> **Data and I/O are not logic. Keep them separate.**

In COMP 170, programs are short enough that everything in one flat block is fine. In COMP 271, programs will grow, and the habits you build now determine whether that growth is manageable or painful. Pure functions with clear inputs and outputs are the foundation of every other design principle we will study this semester.
