import sys  # for getsizeof()

base = "hello "
total_mem = sys.getsizeof(base)
safety = 30
count_to_safety = 0
ID_HEADER = "Object ID"
LEN_HEADER = "Length"; LEN_LEN=15
OBJ_SIZE_HEADER = "Object size (MB)"
TOTAL_SIZE = "Memory used (GB)"
MB = 1024*1024
GB = MB*1024

print(f"{ID_HEADER:>15}\t{LEN_HEADER:>15}\t{OBJ_SIZE_HEADER:>15}\t{TOTAL_SIZE:>15}")
while count_to_safety < safety:
    print(f"{hex(id(base)):>15}\t{len(base):15,d}\t{(sys.getsizeof(base)/MB):15.9,f}\t{total_mem:,d}")
    base = base + base
    total_mem += sys.getsizeof(base)
    count_to_safety += 1
