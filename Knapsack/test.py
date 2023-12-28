import random
import sys
from time import perf_counter

import simpleRecursion
import memoizationWithWrapper
import dynamicProgramming
import cythonVersion

sys.setrecursionlimit(10000)

W = 250
n = 50
wt = []
val = []
for x in range(50):
    wt.append(random.randint(1, 100))
    val.append(random.randint(1, 100))

start = perf_counter()
result = simpleRecursion.knapsack(W, n, wt, val)
end = perf_counter()

print(result)
print(f'Time elapsed: {end - start} seconds')

start = perf_counter()
result = memoizationWithWrapper.knapsack(W, n, wt, val)
end = perf_counter()

print(result)
print(f'Time elapsed: {end - start} seconds')

start = perf_counter()
result = dynamicProgramming.knapsack(W, n, wt, val)
end = perf_counter()

print(result)
print(f'Time elapsed: {end - start} seconds')

start = perf_counter()
result = cythonVersion.knapsack(W, n, wt, val)
end = perf_counter()

print(result)
print(f'Time elapsed: {end - start} seconds')
