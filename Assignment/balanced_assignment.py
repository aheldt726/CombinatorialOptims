from math import inf


def hungarian_fibonacci(arr):
    """
    Uses the Hungarian algorithm with Fibonacci heaps to calculate the minimum assignment cost
    :param arr: 2D array of floats or integers where the ith row and jth column represent the ith agent working on the
    jth task
    :return: List of integers where the ith index represents the ith worker's task except the last value
    which is the total assignment cost.  If the array at index i is -1, it means the ith worker is unassigned
    """

    n_jobs = len(arr)
    n_workers = len(arr[0])
    if n_jobs > n_workers:
        raise Exception("Balanced algorithm has received unbalanced problem")
    jobs = [-1] * (n_workers + 1)  # job assignment list
    j_pots = [0] * n_workers  # Johnson Potentials
    ans_cur = 0
    answers = []

    for job_cur in range(n_jobs):
        worker_cur = n_workers
        jobs[worker_cur] = job_cur
        dist = [inf]*(n_workers+1)  # List of Johnson reduced distances
        dist[n_workers] = 0
        visited = [False] * (n_workers+1)
        previous = [-1] * (n_workers+1)
        while jobs[worker_cur] != -1:
            min_dist = inf
            visited[worker_cur] = True
            worker_next = -1
            for w in range(n_workers):
                if not visited[w]:
                    edge = arr[jobs[worker_cur]][w] - j_pots[w]
                    if worker_cur != n_workers:
                        edge = edge - (arr[jobs[worker_cur]][worker_cur] - j_pots[worker_cur])
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
            j_pots[w] += dist[w]
        ans_cur += j_pots[worker_cur]
        while worker_cur != n_workers:
            w = previous[worker_cur]
            jobs[worker_cur] = jobs[w]
            worker_cur = w
        answers.append(ans_cur)
    jobs[-1] = answers[-1]
    return jobs


def hungarian(arr):
    """
    Uses the Hungarian algorithm without Fibonacci heaps to calculate the minimum cost assignment
    :param arr: 2D array of floats or integers where the ith row and jth column represent the ith agent working on the
    jth task
    :return: List of integers where the ith index represents the ith worker's task except the last value
    which is the total assignment cost.  If the array at index i is -1, it means the ith worker is unassigned
    """
    n_jobs = len(arr)
    n_workers = len(arr[0])
    if n_jobs > n_workers:
        raise Exception("Balanced algorithm has received unbalanced problem")
    jobs = [-1] * (n_workers + 1)  # job assignment list
    pots = [0] * n_jobs  # Potentials
    pott = [0] * (n_workers+1)
    answers = []
    for job_cur in range(n_jobs):
        worker_cur = n_workers
        jobs[worker_cur] = job_cur
        min_cost = [inf]*(n_workers+1)  # minimum reduced cost from edges in Z to worker w
        previous = [-1]*(n_workers+1)  # previous worker
        in_Z = [False]*(n_workers+1)  # list of workers in subset Z
        while jobs[worker_cur] != -1:
            in_Z[worker_cur] = True
            j = jobs[worker_cur]
            delta = inf
            worker_next = 0
            for w in range(n_workers):
                if not in_Z[w]:
                    if arr[j][w] - pots[j] - pott[w] < min_cost[w]:
                        min_cost[w] = arr[j][w] - pots[j] - pott[w]
                        previous[w] = worker_cur
                    if min_cost[w] < delta:
                        delta = min_cost[w]
                        worker_next = w
            for w in range(n_workers+1):
                if in_Z[w]:
                    pots[jobs[w]] += delta
                    pott[w] -= delta
                else:
                    min_cost[w] -= delta
            worker_cur = worker_next
        while worker_cur != n_workers:
            w = previous[worker_cur]
            jobs[worker_cur] = jobs[w]
            worker_cur = w
        answers.append(-pott[n_workers])
    jobs[-1] = answers[-1]
    return jobs


