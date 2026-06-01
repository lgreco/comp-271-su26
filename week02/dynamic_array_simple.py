# This file is the answer to the end-of-class challenge from dynamic_array.py:
#   "How would you do the same thing WITHOUT a class?"
#
# Compare the two files side by side. Every concept from the class version
# reappears here — but the class kept everything neatly packaged together,
# while here we must manage the pieces ourselves.
#
# The class version had:
#   self.zip_codes  →  one list per object, owned by that object
#   self.size       →  one counter per object, owned by that object
#
# Without a class we use module-level variables instead. There is only one
# copy of each, shared by all code in this file. That's fine for a single
# "array" — but the moment we needed two independent arrays, we'd have a
# problem: there is no way to have two separate zip_codes lists without
# inventing a second pair of variable names.  Classes solve this by design:
# each object carries its own state.

# Both variables together represent the dynamic array.
# In dynamic_array.py they lived inside __init__ as self.zip_codes and
# self.size. Here they live at module scope because there is no object to
# attach them to.
zip_codes = list()
for i in range(4):
    zip_codes.append(-1)
size = 0

# Equivalent to DynamicArray.add(self, zip_code) in dynamic_array.py.
# The logic is identical — use size as the index of the next open slot,
# then increment size.
#
# The key difference: we need "global size" to tell Python we want to
# modify the module-level variable, not create a local one.  In the class
# version self.size implicitly referred to the object's own attribute —
# no special keyword required.  The global keyword is a warning sign that
# reveals shared mutable state; classes eliminate it by scoping state to
# the object.
def add(zip_code):
    global size
    if size < 4:
        zip_codes[size] = zip_code
        size = size + 1
    else:
        print("Sorry, no room")

# Equivalent to DynamicArray.__str__(self) in dynamic_array.py.
# Named to_string() instead of __str__ because __str__ is a special
# method Python calls automatically on print() — it only makes sense
# attached to a class.  Without a class, we give the function a plain
# name and call it explicitly.
#
# Spot the difference in the loop range:
#   class version:  range(self.size)      — shows only filled slots
#   this version:   range(len(zip_codes)) — shows all four slots, including
#                   the -1 placeholders for empty ones
# Neither is wrong; they make different choices about what "display" means.
# The class version hides the internal -1 sentinel from the caller;
# this version exposes it, letting you see the underlying storage layout.
def to_string():
    if size == 0:
        output = "nothing to show"
    else:
        output = "["
        for i in range(len(zip_codes)):
            output = output + str(zip_codes[i])
            if i < len(zip_codes) - 1:
                output = output + ", "
        output = output + "]"
    return output

if __name__ == "__main__":
    print(to_string())
    add(12345)
    print(to_string())
    add(23456)
    print(to_string())
    add(34567)
    print(to_string())
    add(45678)
    print(to_string())
    add(56789)
