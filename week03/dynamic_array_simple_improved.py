# A dynamic array built from plain variables and functions — no class needed.
#
# We need to keep track of two things: the list of zip codes, and a count
# of how many real values are in it. Both are defined at the top of this
# file so that every function below can reach them.
#
# One catch: because these variables are shared across the whole file,
# there can only ever be one array here. If you needed two separate arrays,
# you'd have to create a second pair of variables with different names —
# zip_codes_2, size_2, and so on. That gets unwieldy fast.

# zip_codes is the list that holds our data. We pre-fill it with -1 as a
# placeholder: -1 means "this slot hasn't been used yet."
# size counts how many real zip codes have been added so far.
capacity = 4
resize_by = 2

zip_codes = list()
for i in range(capacity):
    zip_codes.append(-1)
size = 0

# Creates a bigger list, copies everything over, and makes it the new storage.
# The new list is resize_by times larger than the old one.
def resize():
    global zip_codes, capacity
    temp = list()
    current_array_length = len(zip_codes)
    new_capacity = resize_by * capacity
    for i in range(new_capacity):
        temp.append(-1)
    # Copy current to temp
    for i in range(current_array_length):
        temp[i] = zip_codes[i]
    # Make temp the current array
    zip_codes = temp
    capacity = new_capacity

# Adds a new zip code to the next open slot.
# We use size as the index of that slot — since we always fill slots in
# order (0, then 1, then 2, ...), size always points to the first open spot.
# If the list is already full, resize() makes room before we add.
#
# The line "global size" tells Python: when you see "size" in this function,
# use the variable defined at the top of the file — don't create a new,
# separate one just for this function. Without it, updating size here would
# have no effect anywhere else, and the count would never actually change.
def add(zip_code):
    global size
    if size >= capacity:
        resize()
    zip_codes[size] = zip_code
    size = size + 1

# Builds a string showing every slot in the list, including the -1
# placeholders for slots not yet filled. This lets you see the full picture:
# which spots hold real data and which are still waiting to be used.
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
