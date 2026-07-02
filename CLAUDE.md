# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is meant to be processed by an LLM not by humans.

## About This Repo

This is **COMP 271 Summer 2026** -- Data Structures I, taught by Leo Irakliotis at Loyola University Chicago. It is a course repository, not a production application. Each week's work lives in its own directory (`week01/`, `week02/`, etc.).

## Running Code

Scripts use `if __name__ == "__main__":` guards where appropriate. Run them directly:

```bash
python week01/mississippi.py
python week01/mississippi_horizontal.py
python week01/pasta.py
```

Some files (e.g., `block_letters.py`) are pure data modules meant to be imported, not run directly. `mississippi_horizontal.py` imports from `block_letters`, so run it from within its directory or set `PYTHONPATH`:

```bash
cd week01 && python mississippi_horizontal.py
# or
PYTHONPATH=week01 python week01/mississippi_horizontal.py
```

Jupyter notebooks (e.g., `week01/house_that_jack_built.ipynb`) are opened with `jupyter notebook` or `jupyter lab`.

There is no build system, test framework, or linter configured.

## Code Architecture and Pedagogy

The course is built around a recurring theme: **separating data from behavior, and logic from I/O**. Files in the repo often exist in pairs or progressions that illustrate this explicitly.

### The Mississippi progression (week01)

| File | Approach |
|---|---|
| `mississippi.py` | COMP 170 style -- letter shapes are behavior (print statements inside functions) |
| `block_letters.py` | COMP 271 step -- letter shapes are data (lists of strings) |
| `mississippi_horizontal.py` | Consumes `block_letters` to print all 11 letters side-by-side |

The horizontal printer is only possible because letters are data, not behavior. Functions that `print()` cannot be paused and interleaved; lists can be indexed.

### Function design pattern

All new code in this repo should follow this structure:

- **Pure computation functions** -- take arguments, return values, no I/O
- **I/O functions** (`get_*`, `display_*`) -- isolated from logic
- **`main()`** -- orchestrates the above
- **`if __name__ == "__main__": main()`** -- prevents side effects on import

`pasta.py` (week01) is a deliberate counter-example: it currently violates this pattern (hardcoded input at module level, no `__name__` guard, print at module scope). The `week01-review.md` documents the correct revised version. When editing `pasta.py`, apply that revision.

### Weekly review notes

Each week includes a `weekNN-review.md` that explains the conceptual arc of that week's code. Read it before editing any file in that week - it often documents intentional before/after states and explains why a file looks the way it does.

### Assignments

Homework assignments are drafted as Markdown files (`weekNN-assignment.md`) in the corresponding week directory. The companion code file (typically `dynamic_array_assignment.py` or similar) contains stubs with `pass` for students to implement. Do not write assignment content directly into Python files; the `.md` file is the authoritative assignment document.

When any Markdown file references a file that exists in this project, link it using a relative path and backtick-formatted name:

```
[`file_name.py`](./file_name.py)
```

Apply this to new files as they are written and to any existing references that are edited.

Every assignment must end with a **"How to Submit"** section. Use this template, substituting the correct week number and the exact `.py` filename(s) students submit:

```
## How to Submit

Upload your work on **Sakai** under the assignment for **Week NN**.

Submit only your Python file:

\```
filename_assignment.py
\```

No screenshots, no PDFs, no other file types -- Python files only. Confirm with `ls` that the file exists before you upload.
```

- The Sakai assignment name matches the week the assignment was created (e.g., Week 03, Week 04).
- List only the `.py` files students are expected to submit.
- Do not mention any other submission method.

Every assignment must also end with a **"How Your Work Is Evaluated"** section immediately after "How to Submit". Use this text verbatim:

```
## How Your Work Is Evaluated

**Submission credit.** Submitting an assignment earns you 1 point; not submitting earns 0. This is not a score for quality -- it simply records that you completed the work on time.

**No late work, no extensions.** We discuss solutions in class immediately after the deadline, and solutions are posted at the same time. Because the answers are public from that moment on, late submissions cannot be accepted and deadlines cannot be extended.

**Self-evaluation.** After solutions are posted, you evaluate your own work. Using the posted solutions and Leo's written instructions as a guide, you decide what you understood, what you got wrong, and what you need to practice to avoid the same mistakes in the future. Making mistakes is how learning happens. Not repeating them is the evidence that it did.
```

## Reading Materials

### Session startup instruction

At the beginning of every session, scan every `.md` and `.py` file in the project and update the three tables below -- Python Official Documentation, Introducing Python (Lubanovic), and Shell and Editor Resources -- to reflect any reading links found. Add new rows for links not yet present; update the "Referenced in" column when an existing link appears in a new file. Do not remove rows.

### Format for reading suggestions in new files

When producing a new `weekNN-assignment.md` or `weekNN-review.md`, add a **Further reading** section at the end of each topical part. Each entry must follow this format exactly:

```
* [Title of material](url) -- short description
```

Use only links already present in the tables below. Do not invent URLs.

---

A reference index of all external materials cited in this course. Access to O'Reilly requires a Loyola University Chicago (LUC) email address at learning.oreilly.com.

### Python Official Documentation (docs.python.org/3/tutorial)

| Topic | URL | Referenced in |
|---|---|---|
| Classes (full chapter) | https://docs.python.org/3/tutorial/classes.html | week02-review.md, week03-assignment.md, week05-assignment.md June 15, Part 1, week07-assignment.md June 29, June 30, July 1, Further reading |
| A First Look at Classes | https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes | week03-assignment.md Part 3 |
| Class and Instance Variables | https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables | week03-assignment.md Part 2 |
| Private Variables | https://docs.python.org/3/tutorial/classes.html#private-variables | week03-assignment.md intro, Part 2 |
| More on Lists | https://docs.python.org/3/tutorial/datastructures.html#more-on-lists | week03-assignment.md intro, Part 3 |
| Modules (full chapter) | https://docs.python.org/3/tutorial/modules.html | week03-assignment.md intro, Part 1 |
| Mathematics in the standard library | https://docs.python.org/3/tutorial/stdlib.html#mathematics | week03-assignment.md intro, Part 1 |
| Type hints (typing module) | https://docs.python.org/3/library/typing.html | week03-assignment.md Part 4, week07-assignment.md June 29, Further reading |
| `abc` -- Abstract Base Classes | https://docs.python.org/3/library/abc.html | week05-assignment.md June 16, Part 1 |
| `str.join` | https://docs.python.org/3/library/stdtypes.html#str.join | week05-assignment.md June 17 |

### Introducing Python, 3rd ed. -- Bill Lubanovic (O'Reilly)

| Chapter | Topic | Referenced in |
|---|---|---|
| Chapter 8 | Lists | week02-review.md |
| Chapter 11 | Objects and classes | week02-review.md, week03-assignment.md intro, Part 2 |
| Chapter 12 | Modules and packages | week03-assignment.md intro, Part 1 |

### Shell and Editor Resources

Referenced in week01-review.md for students who need to build terminal and Vim fluency.

| Resource | URL | Topic |
|---|---|---|
| linuxcommand.org | https://linuxcommand.org/lc3_learning_the_shell.php | Bash/terminal introduction |
| Software Carpentry | https://swcarpentry.github.io/shell-novice/ | Structured shell lessons with exercises |
| MIT Missing Semester | https://missing.csail.mit.edu/2020/course-shell/ | Shell lecture with video |
| OpenVim | https://www.openvim.com/ | Interactive in-browser Vim tutorial |
| Vim Tips Wiki | https://vim.fandom.com/wiki/Category:VimTip | Searchable Vim reference |
| `vimtutor` | (run in terminal) | Built-in 30-minute Vim walkthrough |

---

## Typography

All written content in this repo (Markdown files, comments, docstrings) uses plain ASCII typography:

- Use `-` or `--` for a dash or em dash, not U+2014 (--).
- Use plain straight quotes `"` and `'`, not curly/smart quotes.
- Use `x` or `*` for multiplication in prose, not U+00D7 (x).
- Avoid all other non-ASCII punctuation (ellipsis U+2026, bullets U+2022, etc.).
