from Station import Station


class Trainline:

    def __init__(self):
        self._head = None
        self._tail = None

    def add(self, new_item):
        if self._head is None:
            self._head = new_item
        else:
            self._tail.set_next(new_item)
        self._tail = new_item

    def search(self, target) -> bool:
        """Return True if a station named target exists on the line, False otherwise."""
        pass

    def index_of(self, target) -> int:
        """Return the 0-based position of the first station named target, or -1 if not found."""
        pass

    def count(self) -> int:
        """Return the number of stations on the line."""
        pass


def main():
    line = Trainline()
    line.add(Station("Howard"))
    line.add(Station("Jarvis"))
    line.add(Station("Morse"))
    line.add(Station("Loyola"))
    line.add(Station("Granville"))

    print(line.search("Morse"))       # expected: True
    print(line.search("Belmont"))     # expected: False
    print(line.index_of("Loyola"))    # expected: 3
    print(line.index_of("Belmont"))   # expected: -1
    print(line.count())               # expected: 5


if __name__ == "__main__":
    main()
