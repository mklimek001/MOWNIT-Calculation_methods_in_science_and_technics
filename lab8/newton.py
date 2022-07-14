import math
import numpy as np

def func(x):
    return (x-1) * math.e ** (-15*x) + x ** 10


def func_der(x):
    return 10 * x ** 9 + math.e ** (-15*x) * ((15 * (1 - x))*math.log10(math.e)+1)


def find_0(start, stop, ro):
    point = start
    prev_point = stop
    i_counter = 0
    #print(start, ";", stop, ";", ro, end=" ; ")
    #print("ro = ", ro)


    #print("x_error")
    while math.fabs(point - prev_point) > ro:
        i_counter += 1
        new_point = point - (func(point)/func_der(point))
        prev_point = point
        point = new_point
        #print("    ", i_counter, " ---> ", point)

    #print("Znalezione miejsce zerowe w ", i_counter, " krokach: ", point)
    #print(" ")

    i_counter_x = i_counter
    point_x = point
    #print(i_counter, ";", point, end=" ; ")
    point = start
    i_counter = 0

    #print("y_error")
    while math.fabs(func(point)) > ro:
        i_counter += 1
        new_point = point - (func(point) / func_der(point))
        point = new_point
        #print("    ", i_counter, " ---> ", point)

    #print("Znalezione miejsce zerowe w ", i_counter, " krokach: ", point)
    #print(i_counter, ";", point)
    return [i_counter_x, point_x, i_counter, point]


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
