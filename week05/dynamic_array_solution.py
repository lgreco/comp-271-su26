from __future__ import annotations
import math




# A dynamic array looks like a plain list to the outside world, but internally
# it manages its own growth. The key idea: it keeps a fixed-size underlying list
# (_underlying) and replaces it with a larger one whenever it fills up. Two
# invariants hold at all times:
#   1. _size <= _capacity
#   2. _underlying always has exactly _capacity slots (some filled, some sentinel)
class DynamicArray:

    # Class-level constants: shared by every instance, not stored per object.
    # Putting them here instead of inside __init__ means there is exactly one
    # copy in memory regardless of how many DynamicArray objects exist.
    # The underscore signals "internal detail -- not part of the public interface."
    _DEFAULT_RESIZE_BY: float = 2
    _DEFAULT_CAPACITY: int = 4

    def __init__(
        self, capacity: int = _DEFAULT_CAPACITY, resize_by: float = _DEFAULT_RESIZE_BY
    ) -> None:
        # Think of this array like a hotel.
        # _capacity = total rooms built (slots allocated in _underlying).
        # _size     = rooms currently occupied (values stored by the user).
        # A hotel with 4 rooms and 0 guests is not "empty" -- it still has 4 rooms.
        self._underlying: list = list()
        self._capacity: int = capacity
        self._resize_by: float = resize_by
        # Pre-fill every slot with None as a sentinel value that marks "nothing stored here."
        # This keeps _underlying at a fixed length equal to _capacity at all times,
        # which makes index-based writes like self._underlying[i] = value safe.
        # Without this, Python would raise IndexError on any assignment beyond the list end.
        for i in range(self._capacity):
            self._underlying.append(None)
        # _size starts at 0: zero guests checked in, even though the hotel has rooms.
        self._size: int = 0

    _EMPTY_MESSAGE = "nothing to show"
    _OPENING_DELIMITER = "[ "
    _CLOSING_DELIMITER = " ]"
    _SEPARATING_DELIMITER = ", "

    def __str__(self) -> str:
        """String representation for the object.

        Returns:
        --------
        str : a nicely formatted string with information about
              the object and its contents.
        """
        # Default value in case the object empty
        output = self._EMPTY_MESSAGE
        # If object is not empty, build an output string
        # Not a memory-safe operation!
        if self._size > 0:
            output = self._OPENING_DELIMITER
            for i in range(self._size):
                output = output + str(self._underlying[i])
                if i < self._size - 1:
                    output = output + self._SEPARATING_DELIMITER
            output = output + self._CLOSING_DELIMITER
        return output

    def _resize(self) -> None:
        # Compute the new capacity. math.ceil is required here, not int().
        # Example: if _capacity is 3 and _resize_by is 1.1, then 3 * 1.1 = 3.3.
        # int(3.3) == 3, so the array would never grow -- an infinite loop on the next add.
        # math.ceil(3.3) == 4, guaranteeing the new array is always strictly larger.
        temp_capacity = math.ceil(self._resize_by * self._capacity)
        # Allocate a fresh list pre-filled with sentinels, exactly like __init__ does.
        temp = list()
        for i in range(temp_capacity):
            temp.append(None)
        # Copy only the old _capacity elements (the filled ones plus their sentinels).
        # Slots from _capacity onward in temp are already None -- no need to touch them.
        for i in range(self._capacity):
            temp[i] = self._underlying[i]
        # Swap the old array out. The old _underlying is now unreferenced and will be
        # garbage-collected. From this point on, all operations use the larger array.
        self._underlying = temp
        self._capacity = temp_capacity

    # Why does doubling (_resize_by = 2) make add() fast on average?
    # If we grew by just 1 slot each time, adding N elements would require copying
    # 1 + 2 + 3 + ... + N = O(N^2) total work. Doubling means each element is copied
    # at most log2(N) times, giving O(N log N) total -- or O(1) amortized per add.
    def add(self, value) -> None:
        # Resize before writing so there is always a free slot at index _size.
        # After a resize, _underlying is larger but _size is unchanged.
        if self._size >= self._capacity:
            self._resize()
        # _size is always the index of the next empty slot.
        # Writing here and then incrementing keeps the invariant intact.
        self._underlying[self._size] = value
        self._size = self._size + 1

    def __len__(self) -> int:
        # Implementing __len__ lets Python's built-in len() work: len(da).
        # It also enables truthiness: "if da:" is True when the array is non-empty.
        return self.get_size()

    def get_size(self) -> int:
        # Explicit named accessor for readers unfamiliar with dunder methods.
        # Both get_size() and len() return the number of values the user has stored.
        return self._size

    def get_capacity(self) -> int:
        # Total slots in _underlying, including empty sentinel slots.
        # This is the hotel room count, not the guest count.
        # Users rarely need this; it is exposed mainly for testing and debugging.
        return self._capacity

    def get(self, index: int):
        # Return the value at position index, or None if index is out of range.
        # Valid range is 0 through _size - 1 (filled slots only; sentinel slots are off-limits).
        #
        # Python trap: Python lists accept negative indices natively (-1 means last element).
        # Without an explicit check for index < 0, get(-1) would silently return the last
        # stored value instead of None, violating the contract stated above.
        item_to_return = None
        if index >= 0 and index < self._size:
            item_to_return = self._underlying[index]
        return item_to_return

    def index_of(self, value) -> int:
        # Linear search: inspect each filled slot in order and return the first match.
        # Time complexity is O(n) in the worst case (value is last or absent).
        # Search only filled slots: positions 0 through _size - 1.
        # Sentinel slots all hold None; searching them would produce false matches.
        # Return -1 (not None) to signal "not found" because -1 is an unambiguous sentinel
        # for an index -- no valid index is ever negative.
        index = -1
        i = 0
        while i < self._size and index < 0:
            if self._underlying[i] == value:
                index = i
            i = i + 1
        return index

    def contains(self, value) -> bool:
        # Delegation: reuse index_of rather than re-implementing the search loop.
        # index_of returns -1 when value is absent, so any non-negative result means found.
        # This pattern -- one method as a thin wrapper around another -- avoids duplicating
        # logic and ensures both methods stay in sync if the search algorithm ever changes.
        return self.index_of(value) > -1

    def index_of_all(self, value) -> list[int]:
        # Return the index position of every occurrence of value in this array.
        #
        # Search only the filled slots -- positions 0 through _size - 1.
        # Sentinel slots (positions _size through _capacity - 1) must not be searched;
        # they all hold None and would produce false matches for any caller looking for None.
        #
        # Build and return a list of all matching indices. Examples:
        #   If the array holds ["Sam", "Frodo", "Sam", "Pippin"] and value is "Sam",
        #   return [0, 2].
        #   If value is not found anywhere, return [] -- an empty list, not None, not -1.
        #   An empty list is unambiguous: the caller checks "if result:" or "len(result) == 0"
        #   without needing to special-case a sentinel value.
        #
        # Unlike index_of, do not stop at the first match. Continue through every filled slot
        # so that all occurrences are collected.
        #
        # Your method must have exactly one return statement, at the very end.
        # Build a result list as you scan, then return it once. An empty list
        # is already the correct answer when value is not found -- no second return needed.
        pass

    def count(self, value) -> int:
        # Return the number of times value appears in this array.
        #
        # Search only the filled slots -- positions 0 through _size - 1.
        # If value does not appear, return 0.
        #
        # Hint: index_of_all already finds every occurrence. Consider delegating to it
        # rather than re-implementing the search. A method that does one thing well
        # is easier to maintain than two methods that each do the same search.
        #
        # Your method must have exactly one return statement, at the very end.
        pass

    def remove(self, index: int):
        # Remove the element at position index and return it.
        # To preserve contiguity (no gaps in the filled region), shift every element
        # after the removed one one position to the left.
        #
        # Before remove(1):  [A, B, C, D, None, None]   _size = 4
        # After remove(1):   [A, C, D, None, None, None] _size = 3
        #
        # The slot at the old _size - 1 position must be cleared to None after the shift.
        # Without that step, the last filled slot would be duplicated and remain visible
        # if _size were ever incremented again -- a subtle "object loitering" bug.
        #
        # Returns -1 (not None) when index is out of range, matching get() and index_of()
        # convention: -1 is the sentinel for "operation did not succeed."
        value_to_return = -1
        if index >= 0 and index < self._size:
            value_to_return = self._underlying[index]
            # Shift elements left to close the gap.
            # The loop reads from position i+1 and writes to position i.
            # It runs from the removed index up to (but not including) _size,
            # because _underlying[_size] is already a sentinel and should not be copied.
            for i in range(index, self._size - 1):
                self._underlying[i] = self._underlying[i + 1]
            # Clear the last occupied slot. After the shift it holds a duplicate of
            # what is now at _size - 2; leaving it in place would expose stale data.
            self._underlying[self._size - 1] = None
            self._size = self._size - 1
        return value_to_return
