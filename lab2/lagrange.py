import numpy as np
import matplotlib.pyplot as plt
import math


def func(x):
    return 30 + (x**2)/1.5 - 30*math.cos(1.5*x)


def generateChbNodes(n):
    nodes = []
    for i in range(n):
        k = i+1
        curr_node = -math.cos((2*k - 1)*math.pi/(2*n))
        nodes.append(curr_node)

    return nodes


def stdNodes(node_num, start=0.0, end=1.0):
    x = []
    y = []
    diff = (end-start)/(node_num-1)
    curr_point = start

    for i in range(node_num):
        x.append(curr_point)
        y.append(func(curr_point))
        curr_point += diff

    plotInter(x, y, False)


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

    plotInter(x, y, True)


def lagrange(xTab, yTab, xPoint):
    deg = len(xTab)
    ySum = 0

    for i in range(deg):
        curr = 1
        for j in range(deg):
            if j != i:
                curr *= (xPoint - xTab[j])/(xTab[i] - xTab[j])
        ySum += yTab[i] * curr

    return ySum


def cTabMake(xTab, yTab):
    size = len(xTab)
    cTab = [[0] * size for _ in range(size)]

    for i in range(size):
        cTab[i][0] = yTab[i]

    for j in range(1, size):
        for i in range(size - j):
            cTab[i][j] = (cTab[i + 1][j - 1] - cTab[i][j - 1]) / (xTab[i + j] - xTab[i])

    return cTab


def newton(xTab, cTab, xPoint):
        n = len(xTab)
        ySum = 0

        for i in range(n):
            curr = cTab[0][i]
            for j in range(i):
                curr *= (xPoint - xTab[j])

            ySum += curr

        return ySum


def plotInter(xTab, yTab, isChb = False):
    #xplt = np.linspace(xTab[0], xTab[-1], 1000)
    xplt = np.linspace(-4*math.pi, 4*math.pi, 1000)
    yplt = np.array([], float)
    yintplt_lag = np.array([], float)
    yintplt_newt = np.array([], float)
    coef = cTabMake(xTab,yTab)

    maxdiff_lag = 0
    quaddiff_lag = 0

    maxdiff_newt = 0
    quaddiff_newt = 0

    for x in xplt:
        yplt = np.append(yplt, func(x))
        yintplt_lag = np.append(yintplt_lag, lagrange(xTab, yTab, x))
        yintplt_newt = np.append(yintplt_newt, newton(xTab, coef, x))

        currdiff_lag = math.fabs(func(x) - lagrange(xTab, yTab, x))
        maxdiff_lag = max(maxdiff_lag, currdiff_lag)
        quaddiff_lag += currdiff_lag**2

        currdiff_newt = math.fabs(func(x) - newton(xTab, coef, x))
        maxdiff_newt = max(maxdiff_newt, currdiff_newt)
        quaddiff_newt += currdiff_newt**2

    print("Lagrange - dokładność mierzona metodą pierwszą: ", maxdiff_lag)
    print("Lagrange - dokładność mierzona metodą drugą: ", quaddiff_lag/1000)
    print(" ")
    print("Newton - dokładność mierzona metodą pierwszą: ", maxdiff_newt)
    print("Newton - dokładność mierzona metodą drugą: ", quaddiff_newt/1000)
    print(" - - - - - - - - - - ")
    print(" ")

    plt.plot(xTab, yTab, 'ro',  xplt, yplt, 'r--', xplt, yintplt_lag, 'b-', xplt, yintplt_newt, 'y--')
    plt.xlabel('x')
    plt.ylabel('y')
    if isChb:
        plt.title("Interpolacja funkcji dla " + str(n) + " węzłów rozłożonych według zer wielomianu Czebyszewa")
    else:
        plt.title("Interpolacja funkcji dla " + str(n) + " węzłów rozłożonych równomiernie")



plt.figure()

n = int(input("Liczba węzłów : "))
print(" ")
print("Dokładność dla ", n, " węzłów")
print(" ")
print("Węzły rozłożone równomiernie")
stdNodes(n, -4*math.pi, 4*math.pi)

plt.figure()
print("Węzły rozłożone według zer wielomianu Czebyszewa")
chbNodes(n, -4*math.pi, 4*math.pi)

plt.show()
