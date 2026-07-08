def naive_fact(n: int) -> int:
    # Pure computation: multiply 1 * 2 * ... * n iteratively.
    # "Naive" here just means iterative, as opposed to the recursive
    # version in recursive_factorial.py.
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product


def main():
    print(naive_fact(5))


if __name__ == "__main__":
    main()
