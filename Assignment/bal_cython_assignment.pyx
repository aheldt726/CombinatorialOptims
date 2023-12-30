# cython: boundscheck=False
from cpython cimport array
import array


cdef extern from "math.h":
        float INFINITY
def hungarian_fibonacci(list arr):
    """
    Uses the Hungarian algorithm with Fibonacci heaps to calculate the minimum assignment cost
    :param arr: 2D array of floats or integers where the ith row and jth column represent the ith agent working on the
    jth task
    :return: List of integers where the ith index represents the ith worker's task except the last value
    which is the total assignment cost.  If the array at index i is -1, it means the ith worker is unassigned
    """

    cdef int n_jobs = len(arr)
    cdef int n_workers = len(arr[0])
    #cdef double[:,:] arr = arr_a
    if n_jobs > n_workers:
        raise Exception("Balanced algorithm has received unbalanced problem")
    cdef array.array jobs_a = array.array('i',  [-1] * (n_workers + 1))
    cdef int[:] jobs = jobs_a
    cdef array.array j_pots_a = array.array('d', [0]*n_workers)
    cdef double[:] j_pots = j_pots_a
    cdef double ans_cur = 0
    cdef array.array answers_a = array.array('d', [0]*n_workers)
    cdef double[:] answers = answers_a
    cdef int answers_ind = 0
    cdef int worker_cur
    cdef array.array dist_a = array.array('d', [INFINITY] * (n_workers + 1))
    cdef double[:] dist_template = dist_a
    cdef array.array visited_a = array.array('i', [0] * (n_workers + 1))
    cdef int[:] visited_template = visited_a
    cdef array.array previous_a = array.array('i', [-1] * (n_workers + 1))
    cdef int[:] previous_template = previous_a
    cdef float min_dist
    cdef int worker_next
    cdef int w
    cdef array.array output_a = array.array('d', [0]*(n_workers+1))
    cdef double[:] output = output_a
    cdef double edge


    for job_cur in range(n_jobs):
        worker_cur = n_workers
        jobs[worker_cur] = job_cur
        dist = dist_template.copy()  # List of Johnson reduced distances
        dist[n_workers] = 0.0
        visited = visited_template.copy()
        previous = previous_template.copy()
        while jobs[worker_cur] != -1:
            min_dist = INFINITY
            visited[worker_cur] = 1
            worker_next = -1
            for w in range(n_workers):
                if visited[w] == 0:
                    edge = arr[jobs[worker_cur]][w] - j_pots[w]
                    if worker_cur != n_workers:
                        edge = edge - ((arr[jobs[worker_cur]][worker_cur]) - j_pots[worker_cur])
                        if edge < 0:
                            raise Exception("Fatal issue: edge is negative")
                    if dist[worker_cur] + edge < dist[w]:
                        dist[w] = dist[worker_cur] + edge
                        previous[w] = worker_cur
                    if dist[w] < min_dist:
                        min_dist = dist[w]
                        worker_next = w
            worker_cur = worker_next
        for w in range(n_workers):
            if dist[worker_cur] < dist[w]:
                dist[w] = dist[worker_cur]
            j_pots[w] += dist[w] #rn dist[w] is being screwy
        ans_cur += j_pots[worker_cur]
        while worker_cur != n_workers:
            w = previous[worker_cur]
            jobs[worker_cur] = jobs[w]
            worker_cur = w
        answers[answers_ind] = ans_cur
        answers_ind += 1
    for i in range(n_workers):
        output[i] = jobs[i]
    output[n_workers] = answers[-1]
    return list(output)


def hungarian(list arr):
    """
    Uses the Hungarian algorithm without Fibonacci heaps to calculate the minimum cost assignment
    :param arr: 2D array of floats or integers where the ith row and jth column represent the ith agent working on the
    jth task
    :return: List of integers where the ith index represents the ith worker's task except the last value
    which is the total assignment cost.  If the array at index i is -1, it means the ith worker is unassigned
    """
    cdef int n_jobs = len(arr)
    cdef int n_workers = len(arr[0])
    #cdef double[:,:] arr = arr
    if n_jobs > n_workers:
        raise Exception("Balanced algorithm has received unbalanced problem")
    cdef array.array jobs_a = array.array('i',  [-1] * (n_workers + 1))
    cdef int[:] jobs = jobs_a
    cdef array.array pots_a = array.array('d', [0]*n_jobs)
    cdef double[:] pots = pots_a
    cdef array.array pott_a = array.array('d', [0]*(n_workers+1))
    cdef double[:] pott = pott_a
    cdef array.array answers_a = array.array('d', [0] * n_workers)
    cdef double[:] answers = answers_a
    cdef int answers_ind = 0
    cdef int worker_cur
    cdef array.array min_cost_a = array.array('d', [INFINITY] * (n_workers + 1))
    cdef double[:] min_cost_template = min_cost_a
    cdef array.array previous_a = array.array('i', [-1] * (n_workers + 1))
    cdef int[:] previous_template = previous_a
    cdef array.array in_Z_a = array.array('i', [0] * (n_workers + 1))
    cdef int[:] in_Z_template = in_Z_a
    cdef int j
    cdef int worker_next
    cdef int w
    cdef array.array output_a = array.array('d', [0]*(n_workers+1))
    cdef double[:] output = output_a
    for job_cur in range(n_jobs):
        worker_cur = n_workers
        jobs[worker_cur] = job_cur

        min_cost = min_cost_template.copy() # minimum reduced cost from edges in Z to worker w

        previous = previous_template.copy()  # previous worker

        in_Z = in_Z_template.copy()  # list of workers in subset Z
        while jobs[worker_cur] != -1:
            in_Z[worker_cur] = 1
            j = jobs[worker_cur]
            delta = INFINITY
            worker_next = 0
            for w in range(n_workers):
                if in_Z[w] == 0:
                    if arr[j][w] - pots[j] - pott[w] < min_cost[w]:
                        min_cost[w] = arr[j][w] - pots[j] - pott[w]
                        previous[w] = worker_cur
                    if min_cost[w] < delta:
                        delta = min_cost[w]
                        worker_next = w
            for w in range(n_workers+1):
                if in_Z[w] == 1:
                    pots[jobs[w]] += delta
                    pott[w] -= delta
                else:
                    min_cost[w] -= delta
            worker_cur = worker_next
        while worker_cur != n_workers:
            w = previous[worker_cur]
            jobs[worker_cur] = jobs[w]
            worker_cur = w
        answers[answers_ind] = -pott[n_workers]
        answers_ind += 1
    for i in range(n_workers):
        output[i] = jobs[i]
    output[n_workers] = answers[-1]
    return list(output)


