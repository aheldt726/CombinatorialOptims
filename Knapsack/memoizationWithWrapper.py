from time import perf_counter
from functools import wraps
import sys
import random


def memoization(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


@memoization
def knapsack(max_weight: int, num: int, weights: list[int], values: list[int]) -> int:
    """
    Solves a basic knapsack problem using simple recursion and memoization.

    Time Complexity:
        Worst Case: O(2^n)
        Best Case: O(nW), where W = max_weight

    Args:
        max_weight (int): The maximum weight the knapsack can hold.
        num (int): The total number of items.
        weights (list[int]): An integer list containing the weight of each item in order.
        values (list[int]): An integer list containing the value of each item in order.

    Returns:
        int: The maximum value of items the knapsack can hold.
    """

    if num == 0 or max_weight == 0:
        return 0

    if weights[num - 1] > max_weight:
        return knapsack(max_weight, num - 1, weights, values)

    return max(values[num - 1] + knapsack(max_weight - weights[num - 1], num - 1, weights, values),
               knapsack(max_weight, num - 1, weights, values))


if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    W = 250
    n = 50
    wt = []
    val = []
    for x in range(50):
        wt.append(random.randint(1, 100))
        val.append(random.randint(1, 100))

    start = perf_counter()
    result = knapsack(W, n, wt, val)
    end = perf_counter()

    print(result)
    print(f'Time elapsed: {end - start} seconds')
