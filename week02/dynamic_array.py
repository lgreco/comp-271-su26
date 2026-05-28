# A class is a blueprint. This blueprint describes a simple container
# for zip codes — think of it as a small box that holds up to 4 of them.
# Once we build an object from this blueprint, each object gets its own
# box and its own count of how full the box is.
#
# The key idea: the class keeps the list and the counter together,
# so any code that uses this class never has to juggle them separately.
#
# End-of-class challenge (resume Monday):
#   How would you do the same thing WITHOUT a class —
#   just plain Python, no blueprints, no objects?
#   What would you need to keep track of, and how would you do it?

class DynamicArray:

    # __init__ is the constructor — Python calls it automatically
    # the moment you create a new object from this class.
    # Think of it as "set up a fresh, empty box."
    def __init__(self):
        # We deliberately avoid the one-liner self.zip_codes = [-1] * 4
        # to show each step clearly: create an empty list, then
        # add four placeholder values (-1 means "slot not yet used").
        self.zip_codes = list()
        for i in range(4):
            self.zip_codes.append(-1)
        # size tracks how many real zip codes we've added so far.
        # It starts at 0 because the box is empty.
        self.size = 0

    # __str__ is what Python calls when you print() this object.
    # It builds one string showing all four slots,
    # including the empty ones (shown as -1).
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

    # add() puts a new zip code into the next open slot.
    # self.size doubles as the index of that open slot —
    # because we always fill slots in order: 0, then 1, then 2, then 3.
    # If the box is already full (size has reached 4), we say so and stop.
    def add(self, zip_code):
        if self.size < 4:
            self.zip_codes[self.size] = zip_code
            self.size = self.size + 1
        else:
            print("Sorry, no room")
