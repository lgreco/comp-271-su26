# A dynamic array that grows as needed to hold any number of zip codes.
#
# The key improvement over a fixed-size version: no magic numbers.
# The initial capacity comes in as a parameter; the growth factor is a
# named constant. Each is defined exactly once and used everywhere —
# change it in one place and every loop, check, and calculation adjusts
# automatically.
#
# Think of a named value as load-bearing: it carries the meaning for every
# line that references it. A raw literal like 4 scattered across a dozen
# lines splits that load across a dozen places — miss one when you need to
# change the value, and you have a bug.

class DynamicArray:

    # RESIZE_BY is the growth factor: each time the array runs out of room,
    # its capacity is multiplied by this value. Naming it here means the
    # policy lives in exactly one place. Want to triple instead of double?
    # Change this line — resize() picks it up without any other edits.
    RESIZE_BY = 2

    # Python calls __init__ automatically when you create a new DynamicArray.
    # capacity is a parameter rather than a hardcoded number, so the caller
    # decides the starting size. Every loop and comparison below uses
    # self.capacity, so they all stay correct regardless of what was passed in —
    # no literals to hunt down and update if the default ever changes.
    def __init__(self, capacity):
        # Building the list slot-by-slot makes each step visible: create the
        # list, then fill it. -1 marks a slot as not yet used.
        # (The one-liner [-1] * self.capacity does the same thing in less code,
        # but hides the two-step process we want students to see clearly.)
        self.zip_codes = list()
        self.capacity = capacity
        for i in range(self.capacity):
            self.zip_codes.append(-1)
        # size counts how many real zip codes have been added.
        # It starts at 0 because no slots are filled yet.
        self.size = 0

    # Python calls __str__ automatically whenever you print() this object.
    # It builds a string showing only the filled slots — range(self.size),
    # not range(self.capacity), so unused placeholder slots stay hidden.
    def __str__(self):
        if self.size == 0:
            output = "nothing to show"
        else:
            output = "["
            for i in range(self.size):
                output = output + str(self.zip_codes[i])
                # Add a comma after every element except the last.
                # The last index is self.size - 1, so we stop one short.
                if i < self.size - 1:
                    output = output + ", "
            output = output + "]"
        return output

    # Creates a larger storage list and copies all existing values into it.
    # temp_capacity is computed from two named values — self.RESIZE_BY and
    # self.capacity — so this method never needs to be edited when either
    # of those changes. The load is on the names, not on this code.
    def resize(self):
        temp = list()
        temp_capacity = self.RESIZE_BY * self.capacity
        for i in range(temp_capacity):
            temp.append(-1)
        for i in range(self.capacity):
            temp[i] = self.zip_codes[i]
        self.zip_codes = temp
        self.capacity = temp_capacity

    # Adds a new zip code to the next open slot.
    # self.size serves as the index of that slot — since slots fill in order
    # (0, then 1, then 2, ...), size always points to the first open one.
    # If the array is full, resize() makes room before the value is placed.
    def add(self, zip_code):
        if self.size >= self.capacity:
            self.resize()
        self.zip_codes[self.size] = zip_code
        self.size = self.size + 1
