from __future__ import annotations

# A fixed-capacity LIFO stack with no backing list, array, or other
# in-memory container -- the file itself IS the stack. Every method
# reads or writes the file one line at a time with a scalar loop
# variable; nothing ever holds more than one line in memory at once.
#
# push() and pop() below are stubs: this file currently treats the
# BOTTOM of the file (its last line) as the top of the stack. Your
# assignment is to rewrite push(), pop(), and peek() so the top of the
# stack lives at the FIRST line of the file instead. size(), is_empty(),
# is_full(), __bool__(), and __len__() do not change -- they only count
# lines, and a stack has exactly as many lines regardless of which end
# holds the top.

_DEFAULT_FILENAME = "stackq_data.txt"
_DEFAULT_CAPACITY = 4


class FileStack:
    """
    The stack file is created (empty) the moment a FileStack is
    instantiated, so every other method can assume it already exists.

    Once push(), pop(), and peek() are rewritten, the top of the stack
    is the FIRST line of the file, and the oldest item on the stack
    sits at the last line.
    """

    def __init__(self, filename: str = _DEFAULT_FILENAME, capacity: int = _DEFAULT_CAPACITY) -> None:
        """Create an empty stack backed by filename, up to capacity items."""
        self._filename = filename
        self._temp_filename = f"{filename}.tmp"
        self._capacity = capacity

        # "w" creates the file if it does not exist yet and truncates
        # it to empty if it does, so the stack always starts empty.
        file = open(self._filename, "w")
        file.close()  # nothing to write here -- opening in "w" mode already did the job

    def is_empty(self) -> bool:
        """True if the stack currently holds no items.

        size() re-reads the file rather than checking a stored count,
        so is_empty() is only ever as correct as the file on disk
        right now -- there is no cached state to fall out of sync
        with it.
        """
        return self.size() == 0

    def __bool__(self) -> bool:
        """Defines what if stack: / while stack: mean for this class.

        Without __bool__, Python would fall back to True for any
        object that isn't None -- an empty stack would test truthy,
        which is the opposite of what a caller expects.
        """
        return not self.is_empty()

    def is_full(self) -> bool:
        """True if the stack already holds self._capacity items.

        capacity is a scalar bound, not a container size -- nothing
        here counts past self._capacity, it only compares against it.
        """
        return self.size() == self._capacity

    def size(self) -> int:
        """Count the items currently on the stack.

        Counts lines by reading them off one at a time and discarding
        each as soon as it is counted -- count is a scalar, never a
        list of the lines themselves.
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
        str -- delegates to size() so there is exactly one place that
        knows how to count the stack.
        """
        return self.size()

    def peek(self) -> str | None:
        """Return the top item without removing it, or None if empty.

        Rewrite this so it matches the new front-loaded top of stack.

        Contract:
        - Must return the exact same value pop() would remove, without
          removing it -- that invariant does not change just because
          the top moved to the other end of the file.
        - With the top now at the front of the file, peek() no longer
          needs to scan every line to find it.

        One return statement, at the very end.
        """
        pass

    def push(self, item: str) -> bool:
        """Add item to the top of the stack; return False if full.

        Rewrite this so item becomes the new FIRST line of the file,
        not the last.

        Contract:
        - Still returns False immediately, without touching the file,
          when the stack is already at capacity -- exactly as before.
        - Otherwise item becomes the new first line, and every line
          already in the file shifts down by one position underneath
          it.
        - A file can only ever be written to at its current end -- there
          is no way to insert at the front of a file directly. Getting
          item to the front therefore means building a new file that
          starts with item and then copying every existing line after
          it, one at a time, the same swap-the-filenames idiom pop()
          already uses below.

        One return statement, at the very end.
        """
        pass

    def pop(self) -> str | None:
        """Remove and return the top item, or None if the stack is empty.

        Rewrite this so the FIRST line of the file is removed and
        returned, not the last.

        Contract:
        - Returns None immediately, without touching the file, when the
          stack is already empty.
        - Otherwise the first line is the item to remove and return;
          every line after it shifts up by one position into a new
          temp file that then becomes the stack file, via the same
          name-swap idiom used elsewhere in this class.

        One return statement, at the very end.
        """
        pass


def main() -> None:
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


if __name__ == "__main__":
    main()
