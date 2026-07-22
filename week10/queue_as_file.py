from __future__ import annotations

# A fixed-capacity FIFO queue with no backing list, array, or other
# in-memory container -- the file itself IS the queue. Each line is
# one queued item, oldest at the top of the file, newest at the
# bottom. Every method reads or writes the file one line at a time
# with a scalar loop variable; nothing ever holds more than one line
# in memory at once.

_DEFAULT_FILENAME = "fileq_data.txt"
_DEFAULT_CAPACITY = 4
_TEMP_FILE_SUFFIX = ".tmp"


class FileQueue:
    """
    The queue file is created (empty) the moment a FileQueue is
    instantiated, so every other method can assume it already exists.

    enqueue() appends a line to the queue file. dequeue() reads the
    file sequentially: the first line is set aside as the return
    value, every remaining line is copied to a second file one at a
    time, and that second file then becomes the queue file -- self._
    filename and self._temp_filename simply swap names, so the old
    queue file becomes next dequeue's temp file in turn. Two files
    ever exist on disk; which one is "the queue" alternates between
    them instead of being renamed.
    """

    def __init__(self, filename: str = _DEFAULT_FILENAME, capacity: int = _DEFAULT_CAPACITY) -> None:
        """Create an empty queue backed by filename, up to capacity items."""
        self._filename = filename
        self._temp_filename = f"{filename}{_TEMP_FILE_SUFFIX}"
        self._capacity = capacity

        # "w" creates the file if it does not exist yet and truncates
        # it to empty if it does, so the queue always starts empty.
        file = open(self._filename, "w")
        file.close()  # nothing to write here -- opening in "w" mode already did the job

    def is_empty(self) -> bool:
        """True if the queue currently holds no items.

        size() re-reads the file rather than checking a stored count,
        so is_empty() is only ever as correct as the file on disk
        right now -- there is no cached state to fall out of sync
        with it.
        """
        return self.size() == 0

    def __bool__(self) -> bool:
        """Defines what if queue: / while queue: mean for this class.

        Without __bool__, Python would fall back to True for any
        object that isn't None -- an empty queue would test truthy,
        which is the opposite of what a caller expects.
        """
        return not self.is_empty()

    def is_full(self) -> bool:
        """True if the queue already holds self._capacity items.

        capacity is a scalar bound, not a container size -- nothing
        here counts past self._capacity, it only compares against it.
        """
        return self.size() == self._capacity

    def size(self) -> int:
        """Count the items currently in the queue.

        Counts lines by reading them off one at a time and discarding
        each as soon as it is counted -- count is a scalar, never a
        list of the lines themselves.

        In class we tracked size with a self._size variable, incremented
        with += 1 on enqueue and decremented with -= 1 on dequeue -- a
        running count kept in memory. Here there is no self._size at
        all: size() recomputes the count from scratch every time by
        counting lines in the file, so the file on disk is the only
        source of truth and there is no cached count that could ever
        drift out of sync with it.
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
        """Lets len(queue) work the same way it does for a list or a
        str -- delegates to size() so there is exactly one place that
        knows how to count the queue.
        """
        return self.size()

    def peek(self) -> str | None:
        """Return the front item without removing it, or None if empty.

        Reads only the first line and stops -- the front of the queue
        is always line 1, so there is no reason to read past it just
        to look at it.
        """
        result = None

        file = open(self._filename, "r")
        line = file.readline()
        file.close()
        if line:
            # An empty file's readline() returns "" (falsy), which is
            # indistinguishable here from "the front item happens to
            # be an empty string" -- for this simple queue, both cases
            # are treated as no line to return. rstrip("\n") strips
            # the trailing newline enqueue() wrote, so peek() returns
            # the item itself, not the raw line.
            result = line.rstrip("\n")

        return result

    def enqueue(self, item: str) -> bool:
        """Add item to the back of the queue; return False if full.

        Decides up front whether the item can be added at all, before
        touching the file -- a full queue must reject the item
        without writing anything.
        """
        added = not self.is_full()

        if added:
            # "a" (append) seeks to the end of the file before every
            # write, so this call can never overwrite an item already
            # sitting in the queue -- it only ever adds one line after
            # the current last line.
            file = open(self._filename, "a")
            file.write(f"{item}\n")
            file.close()

        return added

    def dequeue(self) -> str | None:
        """Remove and return the front item, or None if the queue is empty.

        Reads the file sequentially: the first line is set aside as
        the result, every remaining line is copied to a second file,
        and that second file becomes the queue file in turn.
        """
        result = None

        if not self.is_empty():
            source = open(self._filename, "r")
            # rstrip("\n") strips the trailing newline enqueue() wrote,
            # so result is the item itself, not the raw line.
            result = source.readline().rstrip("\n")

            # Every line after the first is copied across one at a
            # time, in order -- self._temp_filename ends up holding
            # exactly the lines that should remain in the queue.
            destination = open(self._temp_filename, "w")
            line = source.readline()
            while line:
                destination.write(line)
                line = source.readline()
            destination.close()
            source.close()

            # The temp file becomes the queue file: swap the two
            # names rather than renaming anything on disk. The old
            # queue file is still sitting there, ready to be reused
            # as the temp file on the next dequeue.
            self._filename, self._temp_filename = self._temp_filename, self._filename

        return result


def main() -> None:
    queue = FileQueue("fileq_demo.txt", capacity=3)
    print(queue.is_empty())  # expected: True
    print(bool(queue))  # expected: False

    print(queue.enqueue("A"))  # expected: True
    print(queue.enqueue("B"))  # expected: True
    print(queue.enqueue("C"))  # expected: True
    print(queue.is_full())  # expected: True
    print(queue.enqueue("D"))  # expected: False -- queue is at capacity

    print(queue.peek())  # expected: A
    print(queue.size())  # expected: 3
    print(len(queue))  # expected: 3

    print(queue.dequeue())  # expected: A
    print(queue.dequeue())  # expected: B
    print(queue.dequeue())  # expected: C
    print(queue.dequeue())  # expected: None -- queue is empty
    print(queue.is_empty())  # expected: True
    print(bool(queue))  # expected: False


if __name__ == "__main__":
    main()
