import math

# Dynamic array -- accessor methods assignment.
#
# The class below is complete except for five methods marked with pass.
# Your task: implement those methods according to the spec in their comments.
# Do not modify any other method.
# Run this file to check your work against the expected output shown below.

class DynamicArray:

    # Class-level constants: shared by every instance, not stored per object.
    # The underscore signals "internal detail -- not part of the public interface."
    _DEFAULT_RESIZE_BY: float = 2
    _DEFAULT_CAPACITY: int = 4

    def __init__(self, capacity: int = _DEFAULT_CAPACITY, resize_by: float = _DEFAULT_RESIZE_BY) -> None:
        self._underlying: list[int] = list()
        self._capacity: int = capacity
        self._resize_by: float = resize_by
        # Pre-fill every slot with -1 as a sentinel value that marks "nothing stored here."
        # This keeps _underlying at a fixed length equal to _capacity at all times.
        for i in range(self._capacity):
            self._underlying.append(-1)
        # _size tracks stored values; _capacity tracks total slots (including sentinel slots).
        # They start equal to 0 and _DEFAULT_CAPACITY and diverge as elements are added.
        self._size: int = 0

    def __str__(self) -> str:
        if self._size == 0:
            return "nothing to show"
        output = "["
        # Loop up to _size, not _capacity -- sentinel slots are internal and never displayed.
        for i in range(self._size):
            output = output + str(self._underlying[i])
            if i < self._size - 1:
                output = output + ", "
        output = output + "]"
        return output

    def resize(self) -> None:
        # math.ceil guarantees the new capacity is always larger than the old one.
        # int() would round down: int(3 * 1.1) == 3, so the array would never grow.
        temp_capacity = math.ceil(self._resize_by * self._capacity)
        temp = list()
        for i in range(temp_capacity):
            temp.append(-1)
        # Copy only the old _capacity elements -- temp already has sentinels beyond that.
        for i in range(self._capacity):
            temp[i] = self._underlying[i]
        self._underlying = temp
        self._capacity = temp_capacity

    def add(self, value: int) -> None:
        # Resize before writing; after resize there is guaranteed room at index _size.
        if self._size >= self._capacity:
            self.resize()
        # _size is always the index of the next empty slot.
        self._underlying[self._size] = value
        self._size = self._size + 1

    def __len__(self) -> int:
        # Return the number of values stored in this array.
        # Enables: len(da) and truthiness checks like "if da:"
        return self.get_size()

    def get_size(self) -> int:
        # Return the number of values stored in this array.
        # Same value as __len__; explicit name for readers unfamiliar with dunder methods.
        return self._size

    def get_capacity(self) -> int:
        # Return the total number of slots in the underlying array,
        # including empty sentinel slots. This is the hotel room count, not the guest count.
        return self._capacity

    def get(self, index: int):
        # Return the value at position index.
        # Valid positions are 0 through _size - 1 (filled slots only).
        # Return -1 for any index outside that range -- including negative indices.
        # Caution: Python lists accept negative indices natively; you must check for them
        # explicitly, or get(-1) will silently return the last element instead of -1.
        if index >= 0 and index < self._size:
          return self._underlying[index]
        else:
          return None

    def index_of(self, value: int) -> int:
        # Return the position of the first occurrence of value.
        # Search only filled slots: positions 0 through _size - 1.
        # Do not search sentinel slots -- they all hold -1 and would give false matches.
        # Return -1 if value is not found.
        index = -1
        i = 0
        while i < self._size and index < 0:
            if self._underlying[i] == value:
                index = i
            i = i + 1
        return index

    def contains(self, value: int) -> bool:
        """Return true if value is present in the underlying array
        and false otherwise"""
        return self.index_of(value) > -1 
