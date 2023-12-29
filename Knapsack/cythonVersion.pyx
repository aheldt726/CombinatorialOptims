from time import perf_counter
import sys
import random

def knapsack(int max_weight, int num, weights, values) -> int:
    """
    Solves a basic knapsack problem using dynamic programming and Cython.

    Time Complexity: O(nW), where W = max_weight

    Args:
        max_weight (int): The maximum weight the knapsack can hold.
        num (int): The total number of items.
        weights (list[int]): An integer list containing the weight of each item in order.
        values (list[int]): An integer list containing the value of each item in order.

    Returns:
        int: The maximum value of items the knapsack can hold.
    """
    cdef list dp = [0 for i in range(max_weight + 1)]
    cdef int index, weight

    for index in range(1, num + 1):
        for weight in range(max_weight, 0, -1):
            if weights[index - 1] <= weight:
                dp[weight] = max(dp[weight], dp[weight - weights[index - 1]] + values[index - 1])

    return dp[max_weight]


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
