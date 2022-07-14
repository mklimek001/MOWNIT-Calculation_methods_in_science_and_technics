import math
import numpy as np


def func(x):
    return (x-1) * math.e ** (-15*x) + x ** 10


def find_0(start, stop, ro):
    #print("ro = ", ro)
    first_point = (start, func(start))
    second_point = (stop, func(stop))
    i_counter = 0

    #print("x_error")
    while math.fabs(first_point[0] - second_point[0]) > ro:
        i_counter += 1
        #print("    ", i_counter, " ---> ", first_point, second_point)

        '''
        if (first_point[1]*second_point[1]) > 0:
            print("Błąd w działaniu programu w ", i_counter, " kroku ! ")
            break
        '''

        new_x = (second_point[1] * first_point[0] - first_point[1] * second_point[0])/(second_point[1] - first_point[1])
        first_point = second_point
        second_point = (new_x, func(new_x))

    #print("Znalezione miejsce zerowe w ", i_counter, " krokach: ", second_point[0])
    #print(i_counter, ";", second_point[0], end=" ; ")

    i_counter_x = i_counter
    point_x = second_point[0]
    first_point = (start, func(start))
    second_point = (stop, func(stop))
    i_counter = 0

    #print("y_error")
    while math.fabs(second_point[1]) > ro and first_point[1] != second_point[1]:
        i_counter += 1
        #print("    ", i_counter, " ---> ", first_point, second_point)

        new_x = (second_point[1] * first_point[0] - first_point[1] * second_point[0]) / (
                    second_point[1] - first_point[1])
        first_point = second_point
        second_point = (new_x, func(new_x))

    #print("Znalezione miejsce zerowe w ", i_counter, " krokach: ", second_point[0])
    #print(i_counter, ";", second_point[0], end=" ; ")
    point_y = second_point[0]
    return [i_counter_x, point_x, i_counter , point_y]


ivals = np.arange(-1, 0.8, 0.1)
jvals = np.arange(0.8, -1, -0.1)
istepsx_result = [[[0] for _ in ivals] for _ in jvals]
pointx_result = [[[0] for _ in ivals] for _ in jvals]
istepsy_result = [[[0] for _ in ivals] for _ in jvals]
pointy_result = [[[0] for _ in ivals] for _ in jvals]

for e in [-1, -3, -6, -9]:
    print("e = ", e)
    for i in range(ivals.size):
        for j in range(jvals.size):
            result = find_0(round(10*ivals[i])/10, round(10*jvals[j])/10, 10**e)
            istepsx_result[i][j] = result[0]
            pointx_result[i][j] = result[1]
            istepsy_result[i][j] = result[2]
            pointy_result[i][j] = result[3]

    print("")
    print("steps in x diff")
    print(" ;", end="")
    for i in range(ivals.size):
        print(round(10*jvals[i])/10, end=" ; ")
    print("")
    for i in range(ivals.size):
        print(round(10*ivals[i])/10, end=" ; ")
        for j in range(jvals.size):
            print(istepsx_result[i][j], end=" ; ")
        print(" ")

    print("")
    print("zeros in x diff")
    print(" ;", end="")
    for i in range(ivals.size):
        print(round(10 * jvals[i]) / 10, end=" ; ")
    print("")
    for i in range(ivals.size):
        print(round(10*ivals[i])/10, end=" ; ")
        for j in range(jvals.size):
            print(pointx_result[i][j], end=" ; ")
        print(" ")

    print("")
    print("steps in y diff")
    print(" ;", end="")
    for i in range(ivals.size):
        print(round(10*jvals[i])/10, end=" ; ")
    print("")
    for i in range(ivals.size):
        print(round(10*ivals[i])/10, end=" ; ")
        for j in range(jvals.size):
            print(istepsy_result[i][j], end=" ; ")
        print(" ")

    print("")
    print("zeros in y diff")
    print(" ;", end="")
    for i in range(ivals.size):
        print(round(10*jvals[i])/10, end=" ; ")
    print("")
    for i in range(ivals.size):
        print(round(10*ivals[i])/10, end=" ; ")
        for j in range(jvals.size):
            print(pointy_result[i][j], end=" ; ")
        print(" ")
    print("")
