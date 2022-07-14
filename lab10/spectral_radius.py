from math import fabs
import numpy as np


def find_radius(num_of_vars):
    factors = [[0 for _ in range(num_of_vars)] for _ in range(num_of_vars)]
    reverse_diagonal = [[0 for _ in range(num_of_vars)] for _ in range(num_of_vars)]
    iteration_array = [[0 for _ in range(num_of_vars)] for _ in range(num_of_vars)]

    for i in range(num_of_vars):
        for j in range(num_of_vars):
            if i == j:
                factors[i][j] = 10
            else:
                factors[i][j] = 1/(fabs(i-j) + 4)

    for i in range(num_of_vars):
        reverse_diagonal[i][i] = -1/factors[i][i]
        factors[i][i] = 0

    for i in range(num_of_vars):
        for j in range(num_of_vars):
            curr_factor = 0
            for k in range(num_of_vars):
                curr_factor += reverse_diagonal[i][k]*factors[k][j]

            iteration_array[i][j] = curr_factor

    iteration_matrix = np.array(iteration_array)
    own_vals = np.linalg.eigvals(iteration_matrix)

    max_val = 0
    for val in own_vals:
        max_val = max(max_val, fabs(val))

    print("Iteration matrix radius : ", "{:.5f}".format(max_val))
    return max_val


n = int(input("Number of variables : "))
find_radius(n)
