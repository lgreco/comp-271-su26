# This file is the user of the dynamic_array class —
# it doesn't know (or need to know) how the class works on the inside.
# We just import the blueprint, build an object from it, and use it.
#
# Notice how simple this side is: one import, one line to create
# the object. All the bookkeeping (the list, the counter, the
# "sorry, no room" check) lives over in dynamic_array.py, out of our way.
#
# End-of-class challenge (resume Monday):
#   If there were no class to import, what would this file look like?
#   You'd have to create the list yourself, keep track of how full
#   it is yourself, and check before every add — right here,
#   every single time.

from dynamic_array import DynamicArray

# Build one object from the dynamic_array blueprint.
# From this point on, test_object is our "box" —
# it carries its own list and its own size counter inside.
test_object = DynamicArray()
