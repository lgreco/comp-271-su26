def fact(n):
    if n == 0:
        return 1  # by definition, 0! = 1
    else:
        return n * fact(n-1)

print(fact(5))
print(fact(15))
print(fact(30))
print(fact(40))
print(fact(50))
print(fact(60))
print(fact(99))
print(fact(200))
print(fact(999))
