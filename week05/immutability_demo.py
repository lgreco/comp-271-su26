import sys  # for getsizeof()

#hi

# Strings are immutable: "base = base + base" never mutates the existing
# string object, it builds a brand new one and rebinds the name to it. The
# id() column below proves this -- it changes on every iteration.
base = "hello "

# Running total of every object size ever allocated for `base`, not just the
# current one. Because the old strings are unreachable once rebound, this is
# really tracking garbage Python had to create (and could collect) along the
# way -- the cost of immutability when you grow data by repeated concatenation.
total_mem = sys.getsizeof(base)

# Doubling the string each loop reaches multi-gigabyte sizes fast; this caps
# the loop so the demo can't run away and exhaust memory.
safety = 30
count_to_safety = 0

ID_HEADER = "Object ID"
LEN_HEADER = "Length"
OBJ_SIZE_HEADER = "Object size (MB)"
TOTAL_SIZE = "Memory used (GB)"
MB = 1024*1024
GB = MB*1024

# Column widths are named here so the header and the data rows always line
# up -- change one value instead of hunting down matching numbers.
ID_WIDTH = 16
LEN_WIDTH = 14
OBJ_SIZE_WIDTH = 15
TOTAL_SIZE_WIDTH = 15

print(f"{ID_HEADER:>{ID_WIDTH}}\t{LEN_HEADER:>{LEN_WIDTH}}\t{OBJ_SIZE_HEADER:>{OBJ_SIZE_WIDTH}}\t{TOTAL_SIZE:>{TOTAL_SIZE_WIDTH}}")
while count_to_safety < safety:
    # id(base) is the object's identity, not its value -- watch it change
    # every time `base` is rebound to a new string below.
    print(f"{hex(id(base)):>{ID_WIDTH}}\t{len(base):{LEN_WIDTH},d}\t{(sys.getsizeof(base)/MB):{OBJ_SIZE_WIDTH},.4f}\t{(total_mem)/GB:{TOTAL_SIZE_WIDTH},.4f}")
    # This is not appending to `base` -- it allocates a new string twice the
    # length and points `base` at it. The old string becomes garbage.
    base = base + base
    total_mem += sys.getsizeof(base)
    count_to_safety += 1
