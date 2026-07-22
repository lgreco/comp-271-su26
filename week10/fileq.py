from __future__ import annotations

_DEFAULT_FILENAME: str = 'q_file.txt'
_DEFAULT_CAPACITY: int = 4
_TEMP_FILE = "broccoli_cheesecake_with_ketchup_icecream.txt"
_WRITE_MODE = "w"
_NEWLINE = "\n"

class FileQueue:

    def __init__(self, filename: str = _DEFAULT_FILENAME, capacity: int = _DEFAULT_CAPACITY):
        self._size = 0
        self._underlying_file: str = filename
        self._capacity: int = capacity
        # Create the actual file
        file = open(self._filename, self._WRITE_MODE)
        file.close()

    def enqueue(self, payload: str) -> bool:
        success: bool = not self.is_full()
        if success:
            file = open(self._filename, "a")
            file.write(payload+self._NEWLINE)
            file.close()
            self._size += 1
        return success


    def dequeue(self) -> str | None:
        front = None
        if self._size > 0:
            # open the file
            source = open(self._filename, "r")
            front = source.readline().rstrip("\n")
            line = source.readline()
            destination = open(_TEMP_FILE, "w")
            while line: # while next line from file not empty
                destination.write(line)
                line = source.readline()
            destination.close()
            source.close()
            self._filename, self._TEMP_FILE = self._TEMP_FILE, self._filename
        self._size -= 1
        # os.remove(temp file)
        return front

            # graph the first line (the "front")
            # copy the rest to a temp file
            # make the temp file the queue file
        return front

    def is_full(self) -> bool:
        return self._size == self._capacity

    def __str__(self) -> str:
        pass

    def peek(self) -> str | None:
        pass

    def size(self) --> int:
        pass
