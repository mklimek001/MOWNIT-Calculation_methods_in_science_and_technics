from timeit import default_timer as timer
from math import fabs


def vector_comparison_norm(curr, prev):
    n = len(curr)
    diff_sum = 0
    for i in range(n):
        diff_sum += fabs(curr[i] - prev[i])

    return diff_sum


def vector_summary_norm(curr, factors, free_vals):
    n = len(curr)
    tmp_results = [0 for _ in range(n)]
    diff_sum = 0

    for i in range(n):
        for j in range(n):
            tmp_results[i] += factors[i][j]*curr[j]

    for i in range(n):
        diff_sum += fabs(tmp_results[i] - free_vals[i])

    return diff_sum


def find_sol(num_of_vars,  ro, comparison=True, close_vector=True):
    print(" ")
    print("Number of variables : ", num_of_vars, "  |   ro : ", ro, end="  |  ")
    if comparison:
        print("First criterium (results comparison)", end="  |  ")
    else:
        print("Second criterium (free values comparison)", end="  |  ")

    if close_vector:
        print("Vector close to solution")
    else:
        print("Vector far from solution")

    factors = [[0 for _ in range(num_of_vars)] for _ in range(num_of_vars)]

    for i in range(num_of_vars):
        for j in range(num_of_vars):
            if i == j:
                factors[i][j] = 10
            else:
                factors[i][j] = 1/(fabs(i-j) + 4)

    given_result = [1 for _ in range(num_of_vars)]
    free_vals = [0 for _ in range(num_of_vars)]

    for i in range(num_of_vars):
        curr_sum = 0
        for j in range(num_of_vars):
            curr_sum += factors[i][j] * given_result[j]
        free_vals[i] = curr_sum

    if close_vector:
        result = [5 for _ in range(num_of_vars)]
    else:
        result = [-1000 for _ in range(num_of_vars)]

    prevs = [0 for _ in range(num_of_vars)]

    iter_cntr = 0

    t_start = timer()

    if comparison:
        while vector_comparison_norm(result, prevs) > ro:
            iter_cntr += 1
            for i in range(num_of_vars):
                prevs[i] = result[i]
            for i in range(num_of_vars):
                inside_sum = 0
                for j in range(num_of_vars):
                    if i != j:
                        inside_sum += factors[i][j] * prevs[j]
                result[i] = (free_vals[i] - inside_sum) / factors[i][i]

    else:
        while vector_summary_norm(result, factors, free_vals) > ro:
            iter_cntr += 1
            for i in range(num_of_vars):
                prevs[i] = result[i]
            for i in range(num_of_vars):
                inside_sum = 0
                for j in range(num_of_vars):
                    if i != j:
                        inside_sum += factors[i][j] * prevs[j]
                result[i] = (free_vals[i] - inside_sum) / factors[i][i]

    max_diff = 0
    for i in range(num_of_vars):
        max_diff = max(max_diff, fabs(result[i] - given_result[i]))

    t_end = timer()
    print("Time in sec : ", t_end - t_start)
    print("Num of iterations : ", iter_cntr)
    print("Maximum difference : ", max_diff)
    #print(result)


n = int(input("Number of variables : "))
ro = float(input("Difference : "))

find_sol(n, ro, True, True)
find_sol(n, ro, True, False)
find_sol(n, ro, False, True)
find_sol(n, ro, False, False)

