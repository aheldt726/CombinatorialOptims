import bal_cython_assignment
import balanced_assignment
from time import perf_counter

if __name__ == '__main__':
    problem1 = [[8,4,7],[5,2,3],[9,4,8]]
    problem2 = [[108,125,150], [150,135,175], [122,148,250]]
    problem3 = [[5,8,6,10,3], [7,5,7,4,1], [11,5,10,8,9], [6,6,7,2,4], [7,5,3,4,9]]
    problem4 = [[9,2,2,7,4,2], [6,2,3,6,1,8], [6,5,4,9,9,3], [3,8,9,9,3,7], [5,7,2,4,0,2], [3,1,0,3,4,5]]
    problems = [problem1, problem2, problem3, problem4]

    for x in range(len(problems)):
        start = perf_counter()
        result = balanced_assignment.hungarian_fibonacci(problems[x])
        stop = perf_counter()
        print(f"Python Hungarian Fibonacci Solution to Problem {x+1}: {result}")
        print(f"Time elapsed: {stop - start}")
        start = perf_counter()
        result2 = bal_cython_assignment.hungarian_fibonacci(problems[x])
        stop = perf_counter()
        print(f"Cython Hungarian Fibonacci Solution to Problem {x+1}: {result}")
        print(f"Time elapsed: {stop - start}")
        start = perf_counter()
        result = balanced_assignment.hungarian(problems[x])
        stop = perf_counter()
        print(f"Python Hungarian Solution to Problem {x+1}: {result}")
        print(f"Time elapsed: {stop - start}")
        start = perf_counter()
        result = bal_cython_assignment.hungarian(problems[x])
        stop = perf_counter()
        print(f"Cython Hungarian Solution to Problem {x+1}: {result}")
        print(f"Time elapsed: {stop - start}")