
def hash_sum(name):
    sum = 0
    for c in name:
        sum += ord(c)
    return sum

def hash_prod(name):
    prod = 1
    for c in name:
        prod *= ord(c)
    return prod
