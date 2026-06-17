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
        """Create an empty dynamic array.

        Parameters:
        -----------
        capacity : int
            Number of slots to allocate up front in the underlying list.
            Defaults to _DEFAULT_CAPACITY.
        resize_by : float
            Growth factor applied to capacity whenever the array fills up.
            Defaults to _DEFAULT_RESIZE_BY.
        """
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

    def better_str(self) -> str:
        """A demonstration of a more efficient way to produce a string
        representation of the object. This is, ideally, the code we 
        should use in __str__ above. I keep it separate here to juxtapose
        the problematic code with cummulative strings (that eat up memory)
        and this more efficient approach.
        """
        output = self._EMPTY_MESSAGE
        if self._size > 0:
            items = list()
            for i in range(self._size):
                items.append(self._underlying[i])
            output = "".join(items)
        return output

    def _resize(self) -> None:
        """Grow the underlying list when it has no free slots left.

        Allocates a new list of size resize_by * capacity (rounded up),
        copies every existing slot into it, and replaces _underlying and
        _capacity. Leading underscore: callers never invoke this directly --
        add() calls it automatically when needed.
        """
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
        """Append value as the new last element, resizing first if full.

        Parameters:
        -----------
        value : any
            The item to store. No type restriction -- the array is general
            purpose.
        """
        # Resize before writing so there is always a free slot at index _size.
        # After a resize, _underlying is larger but _size is unchanged.
        if self._size >= self._capacity:
            self._resize()
        # _size is always the index of the next empty slot.
        # Writing here and then incrementing keeps the invariant intact.
        self._underlying[self._size] = value
        self._size = self._size + 1

    def __len__(self) -> int:
        """Return the number of values stored, so len(da) works.

        Returns:
        --------
        int : same value as get_size().
        """
        # Implementing __len__ lets Python's built-in len() work: len(da).
        # It also enables truthiness: "if da:" is True when the array is non-empty.
        return self.get_size()

    def get_size(self) -> int:
        """Return how many values the caller has actually stored.

        Returns:
        --------
        int : the number of filled slots (the "guests checked in").
        """
        # Explicit named accessor for readers unfamiliar with dunder methods.
        # Both get_size() and len() return the number of values the user has stored.
        return self._size

    def get_capacity(self) -> int:
        """Return the total number of slots currently allocated.

        Returns:
        --------
        int : filled slots plus empty sentinel slots (the "hotel room count").
        """
        # Total slots in _underlying, including empty sentinel slots.
        # This is the hotel room count, not the guest count.
        # Users rarely need this; it is exposed mainly for testing and debugging.
        return self._capacity

    def get(self, index: int):
        """Return the value stored at index, or None if index is out of range.

        Parameters:
        -----------
        index : int
            Position to read. Valid range is 0 through get_size() - 1.

        Returns:
        --------
        any : the stored value, or None if index is negative or >= get_size().
        """
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
        """Return the index of the first occurrence of value.

        Parameters:
        -----------
        value : any
            The item to search for among the filled slots.

        Returns:
        --------
        int : index of the first match, or -1 if value is not present.
        """
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
        """Return whether value is present anywhere in the filled slots.

        Parameters:
        -----------
        value : any
            The item to search for.

        Returns:
        --------
        bool : True if value appears at least once, False otherwise.
        """
        # Delegation: reuse index_of rather than re-implementing the search loop.
        # index_of returns -1 when value is absent, so any non-negative result means found.
        # This pattern -- one method as a thin wrapper around another -- avoids duplicating
        # logic and ensures both methods stay in sync if the search algorithm ever changes.
        return self.index_of(value) > -1

    def index_of_all(self, value) -> list[int]:
        """Return the index of every occurrence of value, in order.

        Parameters:
        -----------
        value : any
            The item to search for among the filled slots.

        Returns:
        --------
        list[int] : indices of every match, lowest to highest, or [] if
                     value does not appear anywhere.
        """
        # Search only the filled slots -- positions 0 through _size - 1.
        # Sentinel slots (positions _size through _capacity - 1) must not be searched;
        # they all hold None and would produce false matches for any caller looking for None.
        #
        # Unlike index_of, do not stop at the first match. Continue through every filled slot
        # so that all occurrences are collected.
        #
        # Single-entry / single-exit: build the result list while scanning,
        # then return it once at the very end. An empty list is already the
        # correct answer when value is not found -- no second return needed.
        matches = list()
        for i in range(self._size):
            if self._underlying[i] == value:
                matches.append(i)
        return matches

    def count(self, value) -> int:
        """Return how many times value appears among the filled slots.

        Parameters:
        -----------
        value : any
            The item to search for.

        Returns:
        --------
        int : number of occurrences, or 0 if value does not appear.
        """
        # Delegation: index_of_all already finds every occurrence, so the
        # count is just the length of that list. Reusing it instead of
        # re-implementing the search keeps both methods in sync if the
        # search algorithm ever changes.
        return len(self.index_of_all(value))

    def remove(self, index: int):
        """Remove and return the element at index, shifting later elements left.

        Parameters:
        -----------
        index : int
            Position to remove. Valid range is 0 through get_size() - 1.

        Returns:
        --------
        any : the removed value, or -1 if index is out of range.
        """
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
