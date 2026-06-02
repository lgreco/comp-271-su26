# A dynamic array whose initial capacity and growth factor are both configurable.
#
# The previous version (dynamic_array_improved.py) hardcoded RESIZE_BY = 2 as a
# class constant, committing every object to doubling. That is a reasonable default,
# but it removes the caller's ability to tune the trade-off.
#
# The trade-off, from class discussion:
#   - A large growth factor (2x, 4x) means resizing happens rarely, so the copy
#     loop runs infrequently -- but after each resize, many slots sit empty.
#   - A small growth factor (10%, 20%) wastes little memory -- but triggers the
#     copy loop far more often as the array grows.
#   - Neither extreme is universally correct. It depends on the application: how
#     often will the array grow? How much memory is available?
#
# The solution: lift both values out of the class body and into __init__ parameters
# with defaults. Callers who do not care get the same behavior as before. Callers
# who do care can pass their own values. One class, many policies.
#
# NOTE: this version contains a deliberate, instructive bug. See resize() below.

class DynamicArray:

    # These are fallback values used when the caller does not pass arguments.
    # Naming them DEFAULT_... makes clear that they are not fixed policy -- they
    # are the chef's choice when no preference is expressed.
    # Defining them here means there is one place to change each default, not one
    # per constructor call. This is the same named-constant discipline applied to
    # the magic-number problem from the earlier fixed-size version.
    DEFAULT_RESIZE_BY = 2
    DEFAULT_CAPACITY = 4

    # Both parameters are optional. If the caller passes nothing, the object
    # behaves exactly like the previous class: capacity 4, doubles on resize.
    # If the caller wants a different starting size or a different growth policy,
    # they can say so:
    #
    #   DynamicArray()              -- default capacity 4, doubles on resize
    #   DynamicArray(capacity=1, resize_by=4)  -- starts tiny, grows aggressively
    #   DynamicArray(capacity=2, resize_by=1.5) -- starts small, grows by 50%
    #
    # This flexibility is the whole point of the "more improved" version.
    def __init__(self, capacity = DEFAULT_CAPACITY, resize_by = DEFAULT_RESIZE_BY):
        self.zip_codes = list()
        self.capacity = capacity
        # resize_by is stored as an instance variable, not a class constant.
        # The previous version used RESIZE_BY = 2 at the class level, shared by
        # all objects. Here, each object carries its own growth policy, so two
        # DynamicArray objects can have different resize_by values at the same time.
        self.resize_by = resize_by
        for i in range(self.capacity):
            self.zip_codes.append(-1)
        # size counts how many real zip codes have been added.
        # It starts at 0 because no slots are filled yet.
        self.size = 0

    # Unlike dynamic_array_improved.py, which looped over range(self.size) and
    # hid the -1 sentinel slots, this version loops over range(self.capacity) so
    # every slot is visible -- filled and empty alike. This makes it easy to see
    # the full underlying array during demos: how many slots exist in total, not
    # just how many are currently occupied. A production __str__ would hide the
    # sentinels; here the transparency is intentional.
    def __str__(self):
        output = "["
        for i in range(self.capacity):
            output = output + str(self.zip_codes[i])
            # Add a comma after every element except the last.
            if i < self.capacity - 1:
                output = output + ", "
        output = output + "]"
        return output

    # Creates a larger storage list and copies all existing values into it.
    # Three steps: (1) compute the new capacity, (2) allocate a temporary list
    # of that size pre-filled with -1, (3) copy the current contents in, then
    # replace the old list with the new one.
    #
    # This method works correctly when resize_by is a whole number. But try
    # creating an object like DynamicArray(4, 0.1) and adding a fifth element --
    # something goes wrong. Your job: reproduce the error, read the error message
    # carefully, trace it back to the line in this method that causes it, and
    # explain in plain English why that line fails for this particular input.
    # Then propose a fix, and justify your choice.
    def resize(self):
        temp = list()
        temp_capacity = self.resize_by * self.capacity
        for i in range(temp_capacity):
            temp.append(-1)
        for i in range(self.capacity):
            temp[i] = self.zip_codes[i]
        self.zip_codes = temp
        self.capacity = temp_capacity

    # Adds a new zip code to the next open slot.
    # self.size serves as the index of that slot -- since slots fill in order
    # (0, then 1, then 2, ...), size always points to the first open one.
    # If the array is full, resize() makes room before the value is placed.
    def add(self, zip_code):
        if self.size >= self.capacity:
            self.resize()
        self.zip_codes[self.size] = zip_code
        self.size = self.size + 1
