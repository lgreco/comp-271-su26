from __future__ import annotations

# A fixed-capacity LIFO stack with no backing list, array, or other
# in-memory container -- the file itself IS the stack. Each line is
# one stacked item, oldest at the top of the file, newest (the top of
# the stack) at the bottom. Every method reads or writes the file one
# line at a time with a scalar loop variable; nothing ever holds more
# than one line in memory at once.

_DEFAULT_FILENAME = "stackq_data.txt"
_DEFAULT_CAPACITY = 4
_TEMP_FILE_SUFFIX = ".tmp"


class FileStack:
    """
    The stack file is created (empty) the moment a FileStack is
    instantiated, so every other method can assume it already exists.

    push() appends a line to the stack file -- the same "add to the
    end" operation FileQueue's enqueue() uses, since the newest item
    belongs at the bottom of the file either way. pop() is where a
    stack and a queue diverge: the item to remove is the *last* line,
    not the first, and a sequential reader has no way to know a line
    is last until it tries to read the next one and finds nothing
    there. pop() therefore reads one line ahead of the line it is
    about to commit to the temp file -- once readline() comes back
    empty, whatever line is still being held is the last line, and
    that is the one popped rather than copied over. The temp file
    then becomes the stack file -- self._filename and
    self._temp_filename simply swap names, so the old stack file
    becomes next pop's temp file in turn. Two files ever exist on
    disk; which one is "the stack" alternates between them instead of
    being renamed.
    """

    def __init__(self, filename: str = _DEFAULT_FILENAME, capacity: int = _DEFAULT_CAPACITY) -> None:
        """Create an empty stack backed by filename, up to capacity items."""
        self._filename = filename
        self._temp_filename = f"{filename}{_TEMP_FILE_SUFFIX}"
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

        In class we tracked size with a self._size variable, incremented
        with += 1 on push and decremented with -= 1 on pop -- a running
        count kept in memory. Here there is no self._size at all:
        size() recomputes the count from scratch every time by counting
        lines in the file, so the file on disk is the only source of
        truth and there is no cached count that could ever drift out
        of sync with it.
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

        The top of the stack is the *last* line, which a sequential
        reader can only find by reading every line and keeping the
        most recent one -- result is overwritten on every iteration,
        so whatever it holds when the loop ends is the last line seen.
        """
        result = None

        file = open(self._filename, "r")
        line = file.readline()
        while line:
            result = line.rstrip("\n")
            line = file.readline()
        file.close()

        return result

    def push(self, item: str) -> bool:
        """Add item to the top of the stack; return False if full.

        Decides up front whether the item can be added at all, before
        touching the file -- a full stack must reject the item
        without writing anything.
        """
        added = not self.is_full()

        if added:
            # "a" (append) seeks to the end of the file before every
            # write, so this call can never overwrite an item already
            # on the stack -- it only ever adds one line after the
            # current last line, which is exactly where the new top
            # of the stack belongs.
            file = open(self._filename, "a")
            file.write(f"{item}\n")
            file.close()

        return added

    def pop(self) -> str | None:
        """Remove and return the top item, or None if the stack is empty.

        Reads the file sequentially, one line behind the reader: each
        line is held in current while the next line is fetched, and
        only written to the temp file once it is confirmed there is a
        following line. When readline() finally returns empty, current
        is holding the last line in the file -- the top of the stack --
        so it becomes the result instead of being copied over.
        """
        result = None

        if not self.is_empty():
            source = open(self._filename, "r")
            destination = open(self._temp_filename, "w")

            current = source.readline()
            line = source.readline()
            while line:
                destination.write(current)
                current = line
                line = source.readline()
            # current was never written to destination -- it is the
            # last line in the file, i.e. the top of the stack.
            result = current.rstrip("\n")

            destination.close()
            source.close()

            # The temp file becomes the stack file: swap the two
            # names rather than renaming anything on disk. The old
            # stack file is still sitting there, ready to be reused
            # as the temp file on the next pop.
            self._filename, self._temp_filename = self._temp_filename, self._filename

        return result


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
