def fact(n: int) -> int:
    # Pure computation, single return statement: the conditional
    # expression picks the base case (0! = 1) or the recursive case
    # (n * (n-1)!) without branching into separate return paths.
    return 1 if n == 0 else n * fact(n - 1)


def main():
    # fact(999) sits close to Python's default recursion limit (1000),
    # so this is also a demo of how recursion trades stack frames for
    # the neat, linear-recursive definition above.
    for n in (5, 15, 30, 40, 50, 60, 99, 200, 999):
        print(f"{n}! = {fact(n):,d}\n")


if __name__ == "__main__":
    main()
