from __future__ import annotations


from our_first_contract import OurDataStructureContract
from Station import Station

# Week 6 Assignment -- Implement OurDataStructureContract on Trainline
#
# This file has 5 method stubs marked with pass. Your job is to implement
# each one. __init__ and add are already complete -- do not change them.
#
# Trainline inherits from OurDataStructureContract. Python raises TypeError
# at instantiation time if any abstract method is left unimplemented. That
# is the contract enforcement in action: partial compliance is rejected.
#
# Every method you write must use the cursor pattern from class:
#   cursor = self._head
#   while ... and cursor is not None:
#       ... cursor.get_name() ...
#       cursor = cursor.get_next()
# Never reach into _name or _next directly. Always call get_name() and
# get_next().


class Trainline(OurDataStructureContract):

    def __init__(self):
        self._head = None
        self._tail = None

    def add(self, new_item):
        if self._head is None:
            self._head = new_item
        else:
            self._tail.set_next(new_item)
        self._tail = new_item

    def contains(self, value) -> bool:
        """Return True if any station named value is on the line, False otherwise.

        Example:
            line: Howard -> Jarvis -> Morse
            contains("Morse")   -> True
            contains("Belmont") -> False
            contains("Howard")  -> True   (head is a valid match)
            on an empty line    -> False

        Your method must have exactly one return statement, at the very end.
        Use a bool variable (result = False) to accumulate the answer and
        build the while condition around it. Do not return inside the loop.
        """
        # We worked this in class, but you can do it again here. The pattern is:
        #   result = False
        #   cursor = self._head
        #   while not result and cursor is not None:
        #       if cursor.get_name() == value:
        #           result = True
        #       cursor = cursor.get_next()
        #   return result
        pass

    def index_of(self, value) -> int:
        """Return the 0-based position of the first station named value, or -1.

        Howard is at index 0, the station after Howard is at index 1, and so
        on. Keep a counter alongside the cursor; increment it with each hop
        regardless of whether the current station matches.

        Example:
            line: Howard -> Jarvis -> Morse -> Loyola -> Granville
            index_of("Loyola")   ->  3
            index_of("Howard")   ->  0
            index_of("Belmont")  -> -1
            on an empty line     -> -1

        Return -1, not None. -1 is an unambiguous sentinel: no valid index is
        negative, so -1 cannot be confused with a real position.

        Your method must have exactly one return statement, at the very end.
        Initialize result = -1 and build the while condition around it so the
        loop stops as soon as a match is found.
        """
        pass

    def index_of_all(self, value) -> list:
        """Return a list of every index where a station named value appears.

        Return [] (empty list) if value is absent or the line is empty.
        Unlike index_of, do not stop early: scan every station because the
        same name could appear more than once.

        Example:
            line: Howard -> Jarvis -> Morse -> Loyola -> Granville
            index_of_all("Morse")   ->  [2]
            index_of_all("Belmont") ->  []

        Return [] rather than None. An empty list is already an unambiguous
        "not found" signal -- a caller can check `if result` or `len(result)`
        without a special None check, and [] has the same type as a real result.

        Your method must have exactly one return statement, at the very end.
        Start with matches = [] and grow it with matches.append(position) inside
        the loop. There is no early exit condition in the while test -- the loop
        runs until the cursor reaches None.

        This may be an overkill as we do not expect duplicate station names in a
        realistic train line. Nevertheless, it is a good exercise in list building.
        And then, there is CTA's Blue Line with two "Western" stations, and two
        "Harlem" stations.
        """
        pass

    def count(self, value) -> int:
        """Return the number of stations named value.

        Delegate entirely to index_of_all: return len(self.index_of_all(value)).
        Do not write a traversal loop here. index_of_all already does the work;
        a second independent loop means two places to update if the match logic
        ever changes.

        Example:
            line: Howard -> Jarvis -> Morse -> Loyola -> Granville
            count("Morse")   ->  1
            count("Belmont") ->  0

        Your method must have exactly one return statement, at the very end.
        The entire body is one line: return len(self.index_of_all(value)).
        """
        pass

    def remove(self, index: int):
        """Remove and return the station at position index, or -1 if out of range.

        index is 0-based. Howard is at index 0. Return -1 (not None) when:
            - the line is empty
            - index is negative
            - index >= the number of stations on the line

        The algorithm has three cases:
          1. index < 0 or line is empty: result stays -1, nothing changes.
          2. index == 0 (removing the head)
          3. index > 0 (removing a station in the middle or at the tail):


        Example:
            line: Howard -> Jarvis -> Morse -> Loyola -> Granville
            remove(2)  ->  returns the Morse Station (prints "Morse")
            line is now: Howard -> Jarvis -> Loyola -> Granville
            remove(99) ->  -1
            remove(-1) ->  -1

        Your method must have exactly one return statement, at the very end.
        Start with result = -1 and only assign a Station object to it when a
        valid station is found and successfully removed.
        """
        pass


def main():
    line = Trainline()
    line.add(Station("Howard"))
    line.add(Station("Jarvis"))
    line.add(Station("Morse"))
    line.add(Station("Loyola"))
    line.add(Station("Granville"))

    print(line.contains("Morse"))  # expected: True
    print(line.contains("Belmont"))  # expected: False
    print(line.index_of("Loyola"))  # expected: 3
    print(line.index_of("Belmont"))  # expected: -1
    print(line.index_of_all("Morse"))  # expected: [2]
    print(line.index_of_all("Belmont"))  # expected: []
    print(line.count("Morse"))  # expected: 1
    print(line.count("Belmont"))  # expected: 0
    print(line.remove(2))  # expected: Morse
    print(line.remove(99))  # expected: -1


if __name__ == "__main__":
    main()
