def naive_fact(n:int) -> int:
    product = 1
    for i in range(1, n+1):
        product *= i
    return product

print(naive_fact(5))
