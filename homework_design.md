# Homework Design -- Operational Prompt

Use this document as a step-by-step guide when creating a new weekly assignment.
Follow the steps in order. Do not skip the reading phase.

---

## Step 1 -- Read Before Writing

Run these reads before touching any file.

1. `ls weekNN/` -- inventory what already exists in the target week directory.
2. Read the companion `.py` file (usually `dynamic_array_assignment.py` or similar).
   Understand what the class does, which methods are already complete, and what
   state the code is in. This is the file students will submit.
3. Read every date-stamped session note (`YYYY-MM-DD-COMP271.md`) in the week
   directory. These are the primary source for what was covered in class, what
   design decisions were made, what student questions surfaced, and what is
   coming next. The assignment must reflect the class arc, not invent one.
4. Read the most recent existing `weekNN-assignment.md` (usually the prior week)
   for format and tone reference.
5. Re-read `CLAUDE.md`. The assignment format rules, reading link tables, and
   submission template are all there and override defaults.

---

## Step 2 -- Update the Python File

Make these changes to the companion `.py` before writing the assignment markdown.

- **Import.** Add `from __future__ import annotations` at the top if the file
  uses type hints. This enables forward references and newer-style generics
  (`list[int]`) across Python versions.
- **Type hints.** Update annotations to match the current design. If the class
  was generalized (e.g., from `list[int]` to `list`), propagate that change to
  all affected method signatures and instance variable annotations.
- **Stubs.** Add one stub per new method, each containing:
  - The correct signature with type hints.
  - `pass` as the only body statement.
  - Comments that explain: what the method must do, which slots to scan (filled
    only: `0` through `_size - 1`, never sentinel slots), concrete examples with
    expected return values, why the return type was chosen over alternatives
    (e.g., "return `[]`, not `None`, because..."), and any explicit constraints
    (see single-return rule below).
- **Update the file-level comment** at the top to reflect how many stubs are
  present and what the assignment asks for.

### Single-Return Rule

Every new method stub must carry this constraint in its comments:

> Your method must have exactly one return statement, at the very end.

Add the same constraint as a bold paragraph in the corresponding Part of the
assignment markdown. The rationale (Dijkstra's single-entry / single-exit
principle, discussed in the June 8 session) should be stated or referenced.

---

## Step 3 -- Write the Assignment Markdown

File name: `weekNN-assignment.md` in the week directory.

### Section order

1. **Title** -- `# Week N Assignment: [descriptive phrase]`
2. **This Week in Class** -- one `###` subsection per class session. Summarize:
   what was built, what design decisions were made, what student questions
   surfaced, what principle or pattern was named. End each subsection with a
   **Further reading** block. Use only links already in the tables in `CLAUDE.md`;
   never invent a URL.
3. **Overview** -- one short paragraph. Point to the `.py` file using a relative
   backtick link. State the task in one sentence.
4. **One Part per coding task.** See structure below.
5. **Verification** -- concrete expected output for every new method. Cover the
   happy path and at least one edge case (not-found, empty array, repeated
   values). Provide the test code and the expected output as comments. Call out
   traps explicitly (e.g., "not-found must return `[]`, not `None`").
6. **Reflection part** (see Step 4).
7. **How to Submit** -- copy verbatim from the `CLAUDE.md` template. Substitute
   the correct week number and the exact `.py` filename(s) students submit.
8. **How Your Work Is Evaluated** -- copy verbatim from `CLAUDE.md`. Do not alter
   a word.

### Structure of each Part section

```
## Part N: [method name or theme]

[One paragraph: why this method is needed, how it relates to existing methods.]

Implement:

    def method_name(self, ...) -> return_type:

**Contract:**

- [bullet: what to scan]
- [bullet: what to return when found]
- [bullet: what to return when not found, and why that choice]

**[Design rationale heading]**

[Paragraph explaining WHY the return type / sentinel / algorithm was chosen.
Connect to a decision made in class or to a principle already named.]

**One return statement.** Your method must have exactly one `return` statement,
at the very end. [One sentence connecting to the Dijkstra principle or to the
while-loop pattern from class.]
```

### Delegation

When a new method can be implemented by calling an existing one, say so
explicitly and explain why delegation is better than duplicating the loop.
Connect it to the `contains` -> `index_of` refactor from the June 9 session as
a concrete precedent.

---

## Step 4 -- Add a Reflection Exercise

Add a **Part N: Reflection** section after Verification. This part asks students
to compare their prior week's submission with the solutions in the current `.py`.

Structure:

- State that no new code is required.
- Tell students to open their prior submission alongside the current `.py`.
- Tell students to write their answers as comments at the bottom of the `.py`
  file so the reflection is included in their submission.
- Ask 3-4 questions, each targeting a specific, observable difference:
  - A delegation pattern they may have duplicated instead.
  - A guard or edge case they may have missed (e.g., the negative-index trap).
  - A sentinel value that changed and why (e.g., `-1` -> `None` when the array
    was generalized to non-integer types).
  - A loop-structure or single-exit difference.

Questions should be specific enough that a student can answer "yes/no, and here
is why" rather than writing vague generalities.

---

## Step 5 -- Cross-Check Before Saving

- Every link in **Further reading** must exist in the `CLAUDE.md` tables.
- Every file reference in the markdown uses a relative backtick link:
  [`filename.py`](./filename.py).
- The stub comments in the `.py` and the Part description in the `.md` say the
  same thing about each method's contract and constraints.
- "How to Submit" names the correct week number and the exact filename(s).
- "How Your Work Is Evaluated" is verbatim from `CLAUDE.md`.
- Typography: straight quotes, ASCII dashes (-- not --), no curly quotes, no
  Unicode bullets or ellipses.
