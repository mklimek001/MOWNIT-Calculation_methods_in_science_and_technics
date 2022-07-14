import math


def f(x, y, z):
    return x*x - 4*y*y + z*z*z - 1


def g(x, y, z):
    return 2*x*x + 4*y*y - 3*z


def h(x, y, z):
    return x*x - 2*y + z*z - 1


def system_matrix(x, y, z):
    return [[x*x, -4*y*y, z*z*z],
            [2*x*x, 4*y*y, -3*z],
            [x*x, -2*y, z*z]]


def jacobian(x, y, z):
    result = [[0 for _ in range(3)] for _ in range(3)]
    result[0][0] = 2*x
    result[0][1] = -8*y
    result[0][2] = 3*z*z
    result[1][0] = 4*x
    result[1][1] = 8*y
    result[1][2] = -3
    result[2][0] = 2*x
    result[2][1] = -2
    result[2][2] = 2*z
    return result


def test_y(curr_sol, ro):
    x = curr_sol[0]
    y = curr_sol[1]
    z = curr_sol[2]
    return max(math.fabs(f(x, y, z)), math.fabs(g(x, y, z)), math.fabs(h(x, y, z))) < ro


def test_x(prev_sol, curr_sol, ro):
    return max(math.fabs(prev_sol[i] - curr_sol[i]) for i in range(3)) < ro


def cramer(factors, r):
    w = (factors[0][0]*factors[1][1]*factors[2][2] + factors[0][1]*factors[1][2]*factors[2][0] + factors[0][2]*factors[1][0]*factors[2][1]) - (factors[0][2] * factors[1][1] * factors[2][0] + factors[0][1] * factors[1][0] * factors[2][2] + factors[0][0] * factors[1][2] * factors[2][1])
    wx = (r[0]*factors[1][1]*factors[2][2] + factors[0][1]*factors[1][2]*r[2] + factors[0][2]*r[1]*factors[2][1]) - (factors[0][2] * factors[1][1] * r[2] + factors[0][1] * r[1] * factors[2][2] + r[0] * factors[1][2] * factors[2][1])
    wy = (factors[0][0]*r[1]*factors[2][2] + r[0]*factors[1][2]*factors[2][0] + factors[0][2]*factors[1][0]*r[2]) - (factors[0][2] * r[1] * factors[2][0] + r[0] * factors[1][0] * factors[2][2] + factors[0][0] * factors[1][2] * r[2])
    wz = (factors[0][0]*factors[1][1]*r[2] + factors[0][1]*r[1]*factors[2][0] + r[0]*factors[1][0]*factors[2][1]) - (r[0] * factors[1][1] * factors[2][0] + factors[0][1] * factors[1][0] * r[2] + factors[0][0] * r[1] * factors[2][1])
    rx = wx/w
    ry = wy/w
    rz = wz/w
    result = [rx, ry, rz]
    return result


def newton(start_vector, ro):
    prev_sol = [math.inf, math.inf, math.inf]
    curr_sol = [start_vector[i] for i in range(3)]

    print("Wektor początkowy: ", start_vector)

    print("Kryterium X, ro = ", ro)
    x_cntr = 0
    while not(test_x(prev_sol, curr_sol, ro)):
        x = curr_sol[0]
        y = curr_sol[1]
        z = curr_sol[2]
        x_cntr += 1
        result = [f(x, y, z), g(x, y, z), h(x, y, z)]
        curr_chngs = cramer(jacobian(x, y, z), result)
        for i in range(3):
            prev_sol[i] = curr_sol[i]
            curr_sol[i] -= curr_chngs[i]
        #print(prev_sol, curr_chngs, curr_sol)

    for i in range(len(curr_sol)):
        elem = curr_sol[i]
        curr_sol[i] = round(100*elem)/100

    print("Rozwiązanie : ", curr_sol, " znalezione w ", x_cntr, " krokach")

    prev_sol = [math.inf, math.inf, math.inf]
    curr_sol = [start_vector[i] for i in range(3)]

    print("Kryterium = Y, ro = ", ro)
    y_cntr = 0
    while not(test_y(curr_sol, ro)):
        x = curr_sol[0]
        y = curr_sol[1]
        z = curr_sol[2]
        y_cntr += 1
        result = [f(x, y, z), g(x, y, z), h(x, y, z)]
        curr_chngs = cramer(jacobian(x, y, z), result)
        for i in range(3):
            prev_sol[i] = curr_sol[i]
            curr_sol[i] -= curr_chngs[i]
        #print(prev_sol, curr_chngs, curr_sol)

    for i in range(len(curr_sol)):
        elem = curr_sol[i]
        curr_sol[i] = round(100*elem)/100

    print("Rozwiązanie : ", curr_sol, " znalezione w ", y_cntr, " krokach")


for i in [100, 10, 1, 0.1]:
    newton([-100, -100, 100], i)


