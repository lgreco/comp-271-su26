from __future__ import annotations

class FileQueue:

    def __init__(self):
        self._size = 0
        self._underlying_file = "my_very_precious_file_based_queue_file.txt"

    def enqueue(self, payload: str) -> bool:
        pass

    def dequeue(self) -> str | None:
        pass

    def is_full(self) -> bool:
        pass

    def __str__(self) -> str:
        pass

    def peek(self) -> str | None:
        pass

    def size(self) --> int:
        pass
