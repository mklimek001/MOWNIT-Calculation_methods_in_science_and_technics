import numpy as np
import matplotlib.pyplot as plt
import math

def func(x):
    return 30 + (x**2)/1.5 - 30*math.cos(1.5*x)


def stdNodes(node_num, start=0.0, end=1.0):
    x = []
    y = []
    diff = (end-start)/(node_num-1)
    curr_point = start

    for i in range(node_num):
        x.append(curr_point)
        y.append(func(curr_point))
        curr_point += diff

    not_a_knot = findSpline(x, y, True)
    natural = findSpline(x, y, False)
    plotSpline(x, y, not_a_knot, natural, False)


def generateChbNodes(n):
    nodes = []
    for i in range(n):
        k = i+1
        curr_node = -math.cos((2*k - 1)*math.pi/(2*n))
        nodes.append(curr_node)

    return nodes


def chbNodes(node_num, start=0.0, end=1.0):
    nodes = generateChbNodes(node_num)
    x = []
    y = []

    length = end - start
    scale = length/2

    for node in nodes:
        curr_point = (node+1)*scale + start
        x.append(curr_point)
        y.append(func(curr_point))

    not_a_knot = findSpline(x, y, True)
    natural = findSpline(x, y, False)
    plotSpline(x, y, not_a_knot, natural, True)


def findSpline(xTab, yTab, isNotaKnot = False):
    # ai x^2 + bi x + ci
    parts_num = len(xTab) - 1
    matrix_size = parts_num*3

    val_matrix = [0 for _ in range(matrix_size)]
    val_matrix[0] = yTab[0]

    for i in range(1, parts_num):
        val_matrix[2*i - 1] = yTab[i]
        val_matrix[2*i] = yTab[i]

    val_matrix[parts_num*2 - 1] = yTab[-1]

    var_matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    for j in range(3):
        var_matrix[0][j] = xTab[0] ** (2 - j)
        var_matrix[parts_num*2 - 1][-j-1] = xTab[-1] ** j

    for i in range(1, parts_num):
        for j in range(3):
            var_matrix[2*i - 1][j + 3*i - 3] = xTab[i] ** (2 - j)
            var_matrix[2*i][j + 3*i] = xTab[i] ** (2 - j)

    for i in range(0, parts_num-1):
        var_matrix[2 * parts_num + i][3 * i] = 2 * (xTab[i + 1])
        var_matrix[2 * parts_num + i][3 * i + 1] = 1
        var_matrix[2 * parts_num + i][3 * i + 3] = -2 * (xTab[i + 1])
        var_matrix[2 * parts_num + i][3 * i + 4] = -1

    #Not-a-Knot
    if isNotaKnot:
        var_matrix[- 1][0] = 1
        var_matrix[- 1][3] = -1

    #Natural spline
    if not isNotaKnot:
        var_matrix[- 1][0] = 2 * xTab[0]
        var_matrix[- 1][1] = 1

    '''
    #test matrix show
    for i in range(len(var_matrix)):
        print(var_matrix[i], "   [", val_matrix[i], "]")
    '''

    a = np.array(var_matrix)
    b = np.array(val_matrix)
    result = np.linalg.solve(a, b)
    return result


def plotSpline(xTB, yTB, splineNotaKnot, splineNatural, isChb = False):
    n = len(xTB)
    num_of_pieces = n - 1

    xp = np.array(xTB)
    yp = np.array(yTB)

    xplt = np.linspace(-4 * math.pi, 4 * math.pi, 1000)
    yplt = np.array([], float)
    xintplt = np.array([], float)
    yintplt_splain_not_a_knot = np.array([], float)
    yintplt_splain_natural = np.array([], float)

    maxdiff_knot = 0
    quaddiff_knot = 0
    maxdiff_natural = 0
    quaddiff_natural = 0

    for x in xplt:
        yplt = np.append(yplt, func(x))
        for i in range(num_of_pieces):
            if xTB[i] <= x < xTB[i + 1]:
                xintplt = np.append(xintplt, x)

                at_point = splineNotaKnot[3*i] * (x ** 2) + splineNotaKnot[3*i+1] * x + splineNotaKnot[3*i+2]
                yintplt_splain_not_a_knot = np.append(yintplt_splain_not_a_knot, at_point)

                currdiff_knot = math.fabs(at_point - func(x))
                maxdiff_knot = max(maxdiff_knot, currdiff_knot)
                quaddiff_knot += currdiff_knot ** 2

                at_point = splineNatural[3*i] * (x ** 2) + splineNatural[3*i + 1] * x + splineNatural[3*i + 2]
                yintplt_splain_natural = np.append(yintplt_splain_natural, at_point)

                currdiff_natural = math.fabs(at_point - func(x))
                maxdiff_natural = max(maxdiff_natural, currdiff_natural)
                quaddiff_natural += currdiff_natural ** 2

    print("NOT A KNOT    max       quad_sum         |      NATURAL    max       quad_sum")
    print(maxdiff_knot, "; ", quaddiff_knot/len(xintplt), "; ", maxdiff_natural, "; ", quaddiff_natural/len(xintplt))

    plt.plot(xp, yp, 'ro', xplt, yplt, 'r--', xintplt, yintplt_splain_not_a_knot, 'y-', xintplt, yintplt_splain_natural, 'c--')
    plt.xlabel('x')
    plt.ylabel('y')
    if isChb:
        plt.title("Interpolacja funkcji dla " + str(num_of_pieces) + " przedziałów rozłożonych według zer wielomianu Czebyszewa")
    else:
        plt.title("Interpolacja funkcji dla " + str(num_of_pieces) + " przedziałów rozłożonych równomiernie")



n = int(input("Liczba przedziałów : "))

plt.figure()
print("Węzły rozłożone równomiernie")
stdNodes(n+1, -4*math.pi, 4*math.pi)

plt.figure()
print("Węzły rozłożone według zer wielomianu Czebyszewa")
chbNodes(n+1, -4*math.pi, 4*math.pi)
plt.show()






