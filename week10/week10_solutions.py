from __future__ import annotations

import os      # check whether head/tail/registry files exist, remove and
               # replace files during node removal, unregistration, and clear()
import random  # pick the letters that make up each random intermediate filename
import string  # supply the upper- and lower-case letter pool random.choice() draws from

# Week 10 Solutions -- A Front-Loaded Stack and a Doubly Linked List With
# No Node Class, Only Files
#
# See ../../comp-271-su26/week10/week10-assignment.md for the full writeup.
#
# Part 1 rewrites push(), pop(), and peek() from
# ../../comp-271-su26/week10/stack_as_file.py so the top of the stack
# lives at the file's *first* line instead of its last. is_empty(),
# __bool__(), is_full(), size(), __len__(), and __init__() are carried
# over unchanged, exactly as the assignment's contract says they should
# be -- they only count lines, and the stack has exactly as many lines
# no matter which end holds the top.
#
# Part 2 is filell.py's FileLinkedList. There is no stub for it in the
# student-facing repo -- the assignment describes the file format and
# the contract in prose, not in code -- so everything below is new.
#
# Both parts keep leaning on ../../comp-271-su26/week10/queue_as_file.py
# for comparison: peek() below is line-for-line what FileQueue.peek()
# already does (the stack's new front end behaves exactly like a
# queue's front), and pop() below is line-for-line what
# FileQueue.dequeue() already does (removing the front line and
# shifting everything else up is the same operation either way).


# ---------------------------------------------------------------------------
# Part 1 -- FileStack, top of stack moved from the file's last line to
# its first.
# ---------------------------------------------------------------------------

_STACK_DEFAULT_FILENAME = "stackq_data.txt"
_STACK_DEFAULT_CAPACITY = 4
_STACK_TEMP_FILE_SUFFIX = ".tmp"


class FileStack:
    """
    Same public behavior as the original FileStack -- still last in,
    first out, still fixed-capacity, still no list/array anywhere --
    but a different mechanism underneath. The original kept the top
    of the stack at the file's *last* line, which meant pop() and
    peek() both had to scan to the end (a sequential reader cannot
    tell a line is last until the next readline() comes back empty).
    This version keeps the top at the file's *first* line instead,
    which flips which operation pays that cost:

    - peek() and pop() get *easier*. The top is always line 1, so
      peek() only ever reads one line, and pop()'s "shift everything
      after the removed line up by one position" is exactly
      FileQueue.dequeue()'s "copy every line after the first into a
      new file" -- no more reading one line ahead to find the end.
    - push() gets *harder*. A file can only ever be written to at its
      current end -- there is no way to insert at the front of a file
      directly. Getting item to the front means building a brand-new
      file that starts with item and then copying every line already
      on the stack after it, one at a time. The old version's "read
      one line ahead" trick did not disappear; it moved. push() now
      needs to know where the *old* file's last line was in order to
      finish copying it, which is exactly the shape of the old pop()'s
      problem, just aimed at a different method.

    push() and pop() still use the same "build a second file, then
    swap self._filename and self._temp_filename" idiom as before --
    two files ever exist on disk; which one is "the stack" alternates
    between them instead of either name ever being renamed.
    """

    def __init__(
        self,
        filename: str = _STACK_DEFAULT_FILENAME,
        capacity: int = _STACK_DEFAULT_CAPACITY,
    ) -> None:
        """Create an empty stack backed by filename, up to capacity items."""
        self._filename = filename
        self._temp_filename = f"{filename}{_STACK_TEMP_FILE_SUFFIX}"
        self._capacity = capacity

        # "w" creates the file if it does not exist yet and truncates
        # it to empty if it does, so the stack always starts empty.
        file = open(self._filename, "w")
        file.close()  # nothing to write here -- opening in "w" mode already did the job

    def is_empty(self) -> bool:
        """True if the stack currently holds no items.

        Unchanged from the original: size() re-reads the file rather
        than checking a stored count, so is_empty() is only ever as
        correct as the file on disk right now.
        """
        return self.size() == 0

    def __bool__(self) -> bool:
        """Defines what if stack: / while stack: mean for this class.
        Unchanged from the original.
        """
        return not self.is_empty()

    def is_full(self) -> bool:
        """True if the stack already holds self._capacity items.
        Unchanged from the original.
        """
        return self.size() == self._capacity

    def size(self) -> int:
        """Count the items currently on the stack.

        Unchanged from the original: counts lines by reading them off
        one at a time and discarding each as soon as it is counted --
        count is a scalar, never a list of the lines themselves. Which
        end holds the top of the stack has no bearing on how many
        lines the file has, so this method did not need to change at
        all when push/pop/peek did.
        """
        count = 0

        file = open(self._filename, "r")
        line = file.readline()
        while line:
            count += 1
            line = file.readline()
        file.close()

        return count

    def __len__(self) -> int:
        """Lets len(stack) work the same way it does for a list or a
        str. Unchanged from the original.
        """
        return self.size()

    def peek(self) -> str | None:
        """Return the top item without removing it, or None if empty.

        The top of the stack is now the *first* line, so this reads
        exactly one line and stops -- there is no reason to read
        further just to look at the top. This is line-for-line the
        same method as FileQueue.peek() in queue_as_file.py: once the
        top of a stack and the front of a queue are both "whatever is
        on line 1," the code that reads them is identical, even though
        a stack and a queue mean something different by "the item you
        would remove next."
        """
        result = None

        file = open(self._filename, "r")
        line = file.readline()
        file.close()
        if line:
            # An empty file's readline() returns "" (falsy), which is
            # indistinguishable here from "the top item happens to be
            # an empty string" -- for this simple stack, both cases
            # are treated as no line to return. rstrip("\n") strips
            # the trailing newline push() wrote, so peek() returns the
            # item itself, not the raw line.
            result = line.rstrip("\n")

        return result

    def push(self, item: str) -> bool:
        """Add item to the top of the stack; return False if full.

        Decides up front whether the item can be added at all, before
        touching either file -- a full stack must reject the item
        without writing anything, exactly as before.

        Making item the new *first* line means every line already in
        the stack has to move down by one position underneath it, and
        a file can only be appended to, never inserted into. So this
        builds destination by writing item first, then copying every
        line source already has, in the same order they already
        appear -- the line that used to be first is still first among
        the *copied* lines, it is just no longer the first line in the
        file overall. destination then becomes the new stack file via
        the same name-swap pop() and peek()'s callers rely on.
        """
        added = not self.is_full()

        if added:
            source = open(self._filename, "r")
            destination = open(self._temp_filename, "w")

            # item goes first, before a single line of the old file
            # has been copied -- this is the "insert at the front"
            # push() now has to do that the old, top-at-the-end
            # version never needed.
            destination.write(f"{item}\n")

            line = source.readline()
            while line:
                destination.write(line)
                line = source.readline()

            destination.close()
            source.close()

            # The temp file becomes the stack file: swap the two
            # names rather than renaming anything on disk, the same
            # idiom the old push()'s sibling methods already used.
            self._filename, self._temp_filename = self._temp_filename, self._filename

        return added

    def pop(self) -> str | None:
        """Remove and return the top item, or None if the stack is empty.

        The top is now the *first* line, so this is line-for-line the
        same method as FileQueue.dequeue() in queue_as_file.py: set
        the first line aside as the result, copy every remaining line
        into a second file, and swap that file in. The old version's
        "read one line behind the reader" trick -- needed because the
        last line only reveals itself once readline() comes back
        empty -- is gone. It did not vanish; it moved into push()
        above, which now has to solve the mirror-image problem of
        knowing where the *old* file's content ends so it can be
        copied after item.
        """
        result = None

        if not self.is_empty():
            source = open(self._filename, "r")
            # rstrip("\n") strips the trailing newline push() wrote,
            # so result is the item itself, not the raw line.
            result = source.readline().rstrip("\n")

            # Every line after the first is copied across in order --
            # self._temp_filename ends up holding exactly the lines
            # that should remain on the stack, still top-first.
            destination = open(self._temp_filename, "w")
            line = source.readline()
            while line:
                destination.write(line)
                line = source.readline()
            destination.close()
            source.close()

            self._filename, self._temp_filename = self._temp_filename, self._filename

        return result


def stack_demo() -> None:
    """Reproduces main() from the original stack_as_file.py verbatim.

    The assignment's Verification section for Part 1 is explicit that
    every printed value here must be unchanged from before the
    rewrite -- the stack's public behavior did not change, only its
    internal mechanism did. Confirming *that* the mechanism changed
    (that "A" really does land on the first line of stackq_demo.txt
    after the first push) is a manual step, done by opening the file
    in a text editor, not something this demo prints.
    """
    stack = FileStack("stackq_demo.txt", capacity=3)
    print(stack.is_empty())  # expected: True
    print(bool(stack))  # expected: False

    print(stack.push("A"))  # expected: True
    print(stack.push("B"))  # expected: True
    print(stack.push("C"))  # expected: True
    print(stack.is_full())  # expected: True
    print(stack.push("D"))  # expected: False -- stack is at capacity

    print(stack.peek())  # expected: C
    print(stack.size())  # expected: 3
    print(len(stack))  # expected: 3

    print(stack.pop())  # expected: C
    print(stack.pop())  # expected: B
    print(stack.pop())  # expected: A
    print(stack.pop())  # expected: None -- stack is empty
    print(stack.is_empty())  # expected: True
    print(bool(stack))  # expected: False


# ---------------------------------------------------------------------------
# Part 2 -- FileLinkedList: a doubly linked list with no Node class and
# no list/array/dict anywhere. Every node -- including the head and the
# tail -- is a plain text file. This class carries *zero* instance
# state beyond nothing at all: unlike FileStack above, there is no
# self._filename, because the filenames here (head.txt, tail.txt, the
# registry) never change from one call to the next. The list's entire
# state -- how many nodes, what they hold, how they link -- lives on
# disk and nowhere else, which is exactly what makes __init__() able to
# pick up a list a previous process left behind without doing anything
# special to "reconstruct" it: every method already reads its answer
# fresh from the files every time, so there is nothing in memory that
# could be out of date on the very first call.
# ---------------------------------------------------------------------------

_HEAD_FILENAME = "head.txt"
_TAIL_FILENAME = "tail.txt"
_REGISTRY_FILENAME = "filell_registry.txt"
_RANDOM_NAME_CHARACTERS = string.ascii_letters  # upper- and lower-case letters only
_RANDOM_NAME_LENGTH = 8
_RANDOM_NAME_SUFFIX = ".txt"
_NODE_SEPARATOR = " -> "
# A note about the following two constants: usually we do not need
# constants for the empty string. The use of these constants here
# is purely for improved code readability.
_NO_NEXT = _NO_PREV = ""


class FileLinkedList:
    """
    Every node is a three-line file:

        payload
        next_filename
        prev_filename

    where a blank next_filename or prev_filename line means "no such
    neighbor." head.txt and tail.txt are not pointers *to* the first
    and last node -- they *are* the first and last node's storage, so
    they always exist and their filenames never change. Every node
    strictly between them lives in a randomly named file instead.

    The tricky part of this design, and the reason add() and remove()
    below are longer than push()/pop() in Part 1, is that head.txt and
    tail.txt are fixed storage *locations*, not nodes that can be
    freely relinked like an ordinary node can. When the node currently
    living in tail.txt needs to stop being the tail (because a new
    node was just added after it), its data has to physically move out
    to a new file -- tail.txt cannot just start pointing somewhere
    else the way an ordinary node's next_filename can, because
    "wherever tail.txt points" is not what makes something the tail;
    *being the file named tail.txt* is. The same is true in reverse
    when remove() deletes the head or the tail: a neighbor's data has
    to move *into* head.txt or tail.txt, because after the removal
    something still has to be living in that fixed file.

    At size 1, head.txt and tail.txt hold an identical copy of the one
    node that exists -- both, with no data anywhere else, since a list
    of one node is simultaneously its own head and its own tail. Every
    add() and remove() below either creates or dissolves that
    duplication as the list crosses the size-1/size-2 boundary in
    either direction.
    """

    def __init__(self) -> None:
        """Create head.txt, tail.txt, and the filename registry if they
        do not already exist -- and leave them alone if they do.

        There is no self._size, no self._head, nothing cached in this
        instance at all, so "reconstructing" a list left behind by an
        earlier process needs no special code here: the very first
        call to size() (or __str__(), or anything else) will walk
        whatever chain of files is already sitting on disk and report
        exactly what it finds. A brand-new FileLinkedList() picking up
        mid-list is just this class doing what it always does.
        """
        if not os.path.exists(_HEAD_FILENAME):
            # "w" creates an empty (0-byte) file -- the size-0 state
            # the file format description calls for.
            file = open(_HEAD_FILENAME, "w")
            file.close()

        if not os.path.exists(_TAIL_FILENAME):
            file = open(_TAIL_FILENAME, "w")
            file.close()

        if not os.path.exists(_REGISTRY_FILENAME):
            file = open(_REGISTRY_FILENAME, "w")
            file.close()

    # -- low-level node helpers -------------------------------------------
    #
    # Every other method builds on these two. A node's three fields
    # come back as a 3-item tuple, not a list -- this mirrors the
    # file's own fixed three-line format rather than standing in for
    # a growing, in-memory collection of nodes, which is the thing
    # the assignment actually rules out.

    def _read_node(self, filename: str) -> tuple[str, str, str] | None:
        """Read filename's three lines: payload, next_filename,
        prev_filename.

        Returns None when filename is completely empty (0 bytes) --
        the signal this class uses for "no node lives here," the
        state head.txt and tail.txt start in and the state both
        return to once the list empties back down to size 0. A node
        file that does hold data always has exactly three lines, even
        when the second or third is blank; a blank line means "no
        such neighbor," not "this file has fewer than three lines."
        """
        result = None

        file = open(filename, "r")
        payload_line = file.readline()
        if payload_line:
            next_line = file.readline()
            prev_line = file.readline()
            result = (
                payload_line.rstrip("\n"),
                next_line.rstrip("\n"),
                prev_line.rstrip("\n"),
            )
        file.close()

        return result

    def _write_node(
        self, filename: str, payload: str, next_filename: str, prev_filename: str
    ) -> None:
        """Write (or overwrite) filename as a three-line node file."""
        file = open(filename, "w")
        file.write(f"{payload}\n{next_filename}\n{prev_filename}\n")
        file.close()

    def _empty(self, filename: str) -> None:
        """Truncate filename to 0 bytes -- the same size-0 state
        __init__() creates head.txt and tail.txt in, and the state
        _read_node() reads back as "no node here."
        """
        file = open(filename, "w")
        file.close()

    # -- filename registry ---------------------------------------------
    #
    # Two different random 8-letter names could in principle collide,
    # so every name this class hands out is checked against, then
    # recorded in, a registry file -- one intermediate filename per
    # line. The registry is itself just another file with no way to
    # delete a single line directly, so unregistering a name uses the
    # same "copy everything except the one line to drop, then swap it
    # in" idiom FileStack.pop() and FileQueue.dequeue() already use.

    def _is_registered(self, filename: str) -> bool:
        found = False

        registry = open(_REGISTRY_FILENAME, "r")
        line = registry.readline()
        while line and not found:
            found = line.rstrip("\n") == filename
            line = registry.readline()
        registry.close()

        return found

    def _generate_unique_filename(self) -> str:
        """Produce a random 8-letter filename not already in the
        registry, register it, and return it.

        Collisions are checked against the registry rather than
        against the folder's actual file listing, because the
        registry is the one place this class already promises to
        record every intermediate node it has ever created -- checking
        it is one file read; scanning the whole folder would mean
        reaching outside the files this class owns.
        """
        candidate = ""
        in_use = True

        while in_use:
            letters = ""
            # _ signals the loop counter itself is unused -- only the
            # number of iterations matters here
            for _ in range(_RANDOM_NAME_LENGTH):
                letters += random.choice(_RANDOM_NAME_CHARACTERS)
            candidate = f"{letters}{_RANDOM_NAME_SUFFIX}"
            in_use = self._is_registered(candidate)

        registry = open(_REGISTRY_FILENAME, "a")
        registry.write(f"{candidate}\n")
        registry.close()

        return candidate

    def _unregister(self, filename: str) -> None:
        """Remove filename from the registry."""
        temp_filename = f"{_REGISTRY_FILENAME}{_RANDOM_NAME_SUFFIX}.tmp"

        source = open(_REGISTRY_FILENAME, "r")
        destination = open(temp_filename, "w")
        line = source.readline()
        while line:
            if line.rstrip("\n") != filename:
                destination.write(line)
            line = source.readline()
        destination.close()
        source.close()

        os.replace(temp_filename, _REGISTRY_FILENAME)

    # -- public interface -------------------------------------------------

    def size(self) -> int:
        """Count the nodes currently in the list.

        Walks the chain from head.txt to tail.txt one next_filename
        link at a time -- the same "recompute from what is actually on
        disk, never trust a cached number" approach FileStack.size()
        and FileQueue.size() already take in Part 1, extended from
        counting lines in one file to counting nodes across however
        many files the list currently spans.
        """
        result = 0

        node = self._read_node(_HEAD_FILENAME)
        if node is not None:
            result = 1
            # _read_node() always returns the tuple
            # (payload, next_filename, prev_filename), assigned above to
            # node. Unpacking it below pulls out all three items, but
            # only next_filename is needed here -- the other two are
            # discarded by assigning them to the dummy variable _.
            _, next_filename, _ = node
            while next_filename != _NO_NEXT:
                node = self._read_node(next_filename)
                _, next_filename, _ = node
                result += 1

        return result

    def is_empty(self) -> bool:
        """True if the list currently holds no nodes."""
        return self.size() == 0

    def is_full(self) -> bool:
        """Always False. Unlike the array-backed Stack/Queue from week
        8, a node here is just another file, and nothing caps how many
        files can exist.
        """
        return False

    def __str__(self) -> str:
        """Return the payloads from head to tail, as a single string
        joined by " -> " -- what the list actually *holds*, the
        abstraction filelist() deliberately does not expose.
        """
        result = ""

        node = self._read_node(_HEAD_FILENAME)
        if node is not None:
            payload, next_filename, _ = node
            result = payload
            while next_filename != _NO_NEXT:
                node = self._read_node(next_filename)
                payload, next_filename, _ = node
                result += f"{_NODE_SEPARATOR}{payload}"

        return result

    def filelist(self) -> str:
        """Return the filenames from head.txt to tail.txt, in
        traversal order, as a single string joined by " -> " -- which
        files exist and in what order, the *implementation*, as
        opposed to __str__()'s abstraction.
        """
        result = ""

        node = self._read_node(_HEAD_FILENAME)
        if node is not None:
            result = _HEAD_FILENAME
            _, next_filename, _ = node
            while next_filename != _NO_NEXT:
                result += f"{_NODE_SEPARATOR}{next_filename}"
                node = self._read_node(next_filename)
                _, next_filename, _ = node

        return result

    def add(self, payload: str) -> None:
        """Append payload as the new tail of the list.

        There is no self._size to branch on, so this reads tail.txt
        itself to decide which of three shapes the list is currently
        in:

        - tail.txt is empty (size 0): head.txt and tail.txt both
          become the same solo node, duplicated exactly as the file
          format description shows.
        - tail.txt's prev field is blank (size 1): there is exactly
          one node, living in both head.txt and tail.txt at once. It
          keeps living in head.txt -- which now needs to point forward
          to tail.txt for the first time -- and nothing moves to an
          intermediate file, because there was never a second file to
          move it out of.
        - tail.txt's prev field is a real filename (size 2+): the node
          currently in tail.txt is not the head, so it has to move out
          to its own new file to make room. Its payload and prev field
          travel with it unchanged; only its next field changes, from
          "" (it used to be last) to tail.txt (its new neighbor once
          the new node lands there). The node it used to call its
          predecessor also needs to be told its next neighbor's name
          changed.
        """
        old_tail = self._read_node(_TAIL_FILENAME)

        if old_tail is None:
            # size 0 -> 1.
            self._write_node(_HEAD_FILENAME, payload, _NO_NEXT, _NO_PREV)
            self._write_node(_TAIL_FILENAME, payload, _NO_NEXT, _NO_PREV)
        else:
            old_tail_payload, _, old_tail_prev = old_tail

            if old_tail_prev == _NO_PREV:
                # size 1 -> 2: the solo node keeps living in head.txt.
                self._write_node(_HEAD_FILENAME, old_tail_payload, _TAIL_FILENAME, _NO_PREV)
                new_prev = _HEAD_FILENAME
            else:
                # size N -> N+1, N >= 2: move the old tail's node out
                # to a new intermediate file.
                new_filename = self._generate_unique_filename()
                self._write_node(new_filename, old_tail_payload, _TAIL_FILENAME, old_tail_prev)

                # old_tail_prev is never _NO_PREV in this branch (that case
                # was handled above), so it is always a real file --
                # head.txt or another intermediate node -- and it used
                # to call tail.txt its next neighbor. Now it has to
                # call new_filename that instead.
                prev_payload, _, prev_prev = self._read_node(old_tail_prev)
                self._write_node(old_tail_prev, prev_payload, new_filename, prev_prev)
                new_prev = new_filename

            self._write_node(_TAIL_FILENAME, payload, _NO_NEXT, new_prev)

    def remove(self, payload: str) -> bool:
        """Search from head.txt toward tail.txt for the first node
        whose payload matches; remove it and return True, or return
        False (touching nothing) if no node matches.

        The search walks the chain exactly the way size() does. Once a
        match is found, the actual splicing is delegated to _unlink(),
        since which files need to change depends on whether the
        matched node is an ordinary node, the head, or the tail -- see
        _unlink()'s docstring for why those three cases differ.
        """
        removed = False

        match_filename = _HEAD_FILENAME
        node = self._read_node(match_filename)

        while node is not None and not removed:
            match_payload, match_next, match_prev = node

            if match_payload == payload:
                removed = True
            else:
                match_filename = match_next
                if match_filename == _NO_NEXT:
                    node = None
                else:
                    node = self._read_node(match_filename)

        if removed:
            self._unlink(match_filename, match_next, match_prev)

        return removed

    def _unlink(self, filename: str, next_filename: str, prev_filename: str) -> None:
        """Splice filename's node out of the chain.

        Three cases, matching the question the assignment's docstring
        asks directly -- what has to happen when the list shrinks from
        size 2 to 1, or from size 3 to 2 (and by extension, from any
        size N to N - 1):

        - filename is head.txt and it was the only node (next_filename
          is blank): the list drops to size 0. Both fixed files go
          back to the empty state __init__() starts them in.
        - filename is head.txt with a real next neighbor: the list
          drops from size N to N - 1 with the head disappearing, so
          the node after it has to become the new head -- see
          _remove_head().
        - filename is tail.txt: symmetric to the head case -- see
          _remove_tail().
        - filename is an ordinary intermediate node: no fixed file is
          involved at all. Its two neighbors are pointed directly at
          each other, and its file is deleted.
        """
        if filename == _HEAD_FILENAME and next_filename == _NO_NEXT:
            # size 1 -> 0: the one node lived in both fixed files;
            # both simply go back to empty. No intermediate file was
            # ever involved, so there is nothing to unregister.
            self._empty(_HEAD_FILENAME)
            self._empty(_TAIL_FILENAME)
        elif filename == _HEAD_FILENAME:
            self._remove_head(next_filename)
        elif filename == _TAIL_FILENAME:
            self._remove_tail(prev_filename)
        else:
            prev_payload, _, prev_prev = self._read_node(prev_filename)
            self._write_node(prev_filename, prev_payload, next_filename, prev_prev)

            next_payload, next_next, _ = self._read_node(next_filename)
            self._write_node(next_filename, next_payload, next_next, prev_filename)

            os.remove(filename)
            self._unregister(filename)

    def _remove_head(self, new_head_filename: str) -> None:
        """The node currently at new_head_filename becomes the new
        head.

        If new_head_filename is tail.txt, the list is dropping from
        size 2 to size 1: the node that used to be the tail becomes
        the new solo node, so it is written into *both* fixed files,
        mirroring exactly what add() does going the other direction
        when a size-1 list gains a second node. Otherwise
        new_head_filename names an ordinary intermediate file: its
        data moves into head.txt, that file is retired, and whatever
        came after it is told its predecessor is now head.txt.
        """
        payload, next_filename, _ = self._read_node(new_head_filename)

        if new_head_filename == _TAIL_FILENAME:
            self._write_node(_HEAD_FILENAME, payload, _NO_NEXT, _NO_PREV)
            self._write_node(_TAIL_FILENAME, payload, _NO_NEXT, _NO_PREV)
        else:
            self._write_node(_HEAD_FILENAME, payload, next_filename, _NO_PREV)

            next_payload, next_next, _ = self._read_node(next_filename)
            self._write_node(next_filename, next_payload, next_next, _HEAD_FILENAME)

            os.remove(new_head_filename)
            self._unregister(new_head_filename)

    def _remove_tail(self, new_tail_filename: str) -> None:
        """Mirror image of _remove_head(): the node currently at
        new_tail_filename becomes the new tail.
        """
        payload, _, prev_filename = self._read_node(new_tail_filename)

        if new_tail_filename == _HEAD_FILENAME:
            self._write_node(_HEAD_FILENAME, payload, _NO_NEXT, _NO_PREV)
            self._write_node(_TAIL_FILENAME, payload, _NO_NEXT, _NO_PREV)
        else:
            self._write_node(_TAIL_FILENAME, payload, _NO_NEXT, prev_filename)

            prev_payload, _, prev_prev = self._read_node(prev_filename)
            self._write_node(prev_filename, prev_payload, _TAIL_FILENAME, prev_prev)

            os.remove(new_tail_filename)
            self._unregister(new_tail_filename)

    def clear(self) -> None:
        """Delete every file this instance owns and put head.txt,
        tail.txt, and the registry back in the exact empty state
        __init__() creates them in.

        The registry is read once, up front, to learn every
        intermediate filename ever handed out -- deleting files while
        also trying to walk the chain those same files form would mean
        removing the map while still reading it.
        """
        registry = open(_REGISTRY_FILENAME, "r")
        line = registry.readline()
        while line:
            intermediate_filename = line.rstrip("\n")
            if os.path.exists(intermediate_filename):
                os.remove(intermediate_filename)
            line = registry.readline()
        registry.close()

        self._empty(_REGISTRY_FILENAME)
        self._empty(_HEAD_FILENAME)
        self._empty(_TAIL_FILENAME)


def filell_demo() -> None:
    """Runs the smoke test from the assignment's Verification section
    for Part 2, then a same-process stand-in for the "kill the process,
    start a new one" recovery check.

    A true recovery test needs a second python3 process, but nothing
    about FileLinkedList depends on anything living in a Python object
    -- every method reads the answer fresh from disk on every call --
    so a second instance created in the *same* process without ever
    calling clear() on the first one demonstrates the identical thing a
    second process would: __init__() never resets files it finds
    already sitting on disk.
    """
    fll = FileLinkedList()
    print(fll.is_empty())  # expected: True
    print(fll.size())  # expected: 0

    fll.add("first")
    print(fll.size())  # expected: 1
    print(fll.__str__())  # expected: first

    fll.add("second")
    fll.add("third")
    print(fll.size())  # expected: 3
    print(fll.__str__())  # expected: first -> second -> third
    print(fll.filelist())  # expected: head.txt -> <random 8-letter file>.txt -> tail.txt

    print(fll.remove("second"))  # expected: True
    print(fll.size())  # expected: 2
    print(fll.remove("second"))  # expected: False -- already removed

    # Recovery check: a second instance, still in this same process,
    # sees the two nodes the first instance left on disk without
    # fll_recovered.add() ever being called.
    fll_recovered = FileLinkedList()
    print(fll_recovered.size())  # expected: 2
    print(fll_recovered.__str__())  # expected: first -> third

    fll.clear()
    print(fll.is_empty())  # expected: True
    print(fll.size())  # expected: 0


def main() -> None:
    print("=== Part 1: FileStack, top of stack moved to the first line ===")
    stack_demo()

    print()
    print("=== Part 2: FileLinkedList, every node -- including head and tail -- is a file ===")
    filell_demo()


if __name__ == "__main__":
    main()
