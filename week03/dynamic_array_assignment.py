import math

# Dynamic array -- accessor methods assignment.
#
# The class below is complete except for five methods marked with pass.
# Your task: implement those methods according to the spec in their comments.
# Do not modify any other method.
# Run this file to check your work against the expected output shown below.

class DynamicArray:

    _DEFAULT_RESIZE_BY: float = 2
    _DEFAULT_CAPACITY: int = 4

    def __init__(self, capacity: int = _DEFAULT_CAPACITY, resize_by: float = _DEFAULT_RESIZE_BY) -> None:
        self._underlying: list[int] = list()
        self._capacity: int = capacity
        self._resize_by: float = resize_by
        for i in range(self._capacity):
            self._underlying.append(-1)
        self._size: int = 0

    def __str__(self) -> str:
        if self._size == 0:
            return "nothing to show"
        output = "["
        for i in range(self._size):
            output = output + str(self._underlying[i])
            if i < self._size - 1:
                output = output + ", "
        output = output + "]"
        return output

    def resize(self) -> None:
        temp_capacity = math.ceil(self._resize_by * self._capacity)
        temp = list()
        for i in range(temp_capacity):
            temp.append(-1)
        for i in range(self._capacity):
            temp[i] = self._underlying[i]
        self._underlying = temp
        self._capacity = temp_capacity

    def add(self, value: int) -> None:
        if self._size >= self._capacity:
            self.resize()
        self._underlying[self._size] = value
        self._size = self._size + 1

    def __len__(self) -> int:
        # Return the number of values stored in this array.
        # Enables: len(da)
        pass  # replace with your implementation

    def get_size(self) -> int:
        # Return the number of values stored in this array.
        pass  # replace with your implementation

    def get_capacity(self) -> int:
        # Return the total number of slots in the underlying array,
        # including empty sentinel slots.
        pass  # replace with your implementation

    def get(self, index: int) -> int:
        # Return the value at position index.
        # Valid positions are 0 through _size - 1 (filled slots only).
        # Return -1 for any index outside that range.
        pass  # replace with your implementation

    def index_of(self, value: int) -> int:
        # Return the position of the first occurrence of value.
        # Search only filled slots: positions 0 through _size - 1.
        # Return -1 if value is not found.
        pass  # replace with your implementation


if __name__ == "__main__":
    da = DynamicArray()
    da.add(10001)
    da.add(60626)
    da.add(90210)
    print(da)                    # expected: [10001, 60626, 90210]

    print()
    print("__len__ and size/capacity getters")
    print(len(da))               # expected: 3
    print(da.get_size())         # expected: 3
    print(da.get_capacity())     # expected: 4

    print()
    print("get() tests")
    print(da.get(0))             # expected: 10001
    print(da.get(1))             # expected: 60626
    print(da.get(2))             # expected: 90210
    print(da.get(-1))            # expected: -1  (below valid range)
    print(da.get(3))             # expected: -1  (at size, no data there)
    print(da.get(100))           # expected: -1  (well beyond size)

    print()
    print("index_of() tests")
    print(da.index_of(10001))    # expected: 0
    print(da.index_of(60626))    # expected: 1
    print(da.index_of(90210))    # expected: 2
    print(da.index_of(99999))    # expected: -1  (not in array)

    da.add(11111)
    da.add(22222)
    print()
    print("after 2 more adds (triggers resize)")
    print(da)                    # expected: [10001, 60626, 90210, 11111, 22222]
    print(len(da))               # expected: 5
    print(da.get_capacity())     # expected: 8
