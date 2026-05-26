# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is meant to be processed by an LLM not by humans.

## About This Repo

This is **COMP 271 Summer 2026** — Data Structures I, taught by Leo Irakliotis at Loyola University Chicago. It is a course repository, not a production application. Each week's work lives in its own directory (`week01/`, `week02/`, etc.).

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
| `mississippi.py` | COMP 170 style — letter shapes are behavior (print statements inside functions) |
| `block_letters.py` | COMP 271 step — letter shapes are data (lists of strings) |
| `mississippi_horizontal.py` | Consumes `block_letters` to print all 11 letters side-by-side |

The horizontal printer is only possible because letters are data, not behavior. Functions that `print()` cannot be paused and interleaved; lists can be indexed.

### Function design pattern

All new code in this repo should follow this structure:

- **Pure computation functions** — take arguments, return values, no I/O
- **I/O functions** (`get_*`, `display_*`) — isolated from logic
- **`main()`** — orchestrates the above
- **`if __name__ == "__main__": main()`** — prevents side effects on import

`pasta.py` (week01) is a deliberate counter-example: it currently violates this pattern (hardcoded input at module level, no `__name__` guard, print at module scope). The `week01-review.md` documents the correct revised version. When editing `pasta.py`, apply that revision.

### Weekly review notes

Each week includes a `weekNN-review.md` that explains the conceptual arc of that week's code. Read it before editing any file in that week — it often documents intentional before/after states and explains why a file looks the way it does.
