import numpy as np
import matplotlib.pyplot as plt

import math


def func(x):
    return 30 + (x**2)/1.5 - 30*math.cos(1.5*x)

def funcDer(x):
    return 4*x/3 + 45 * math.sin(1.5*x)

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
    y1 = []
    diff = (end-start)/(node_num-1)
    curr_point = start

    for i in range(node_num):
        x.append(curr_point)
        y.append(func(curr_point))
        y1.append(funcDer(curr_point))
        curr_point += diff

    plotInter(x, y, y1, False)


def chbNodes(node_num, start=0.0, end=1.0):
    nodes = generateChbNodes(node_num)
    x = []
    y = []
    y1 = []

    length = end - start
    scale = length/2

    for node in nodes:
        curr_point = (node+1)*scale + start
        x.append(curr_point)
        y.append(func(curr_point))
        y1.append(funcDer(curr_point))

    plotInter(x, y, y1, True)


def hTabMake(xTab, yTab, y1Tab):
    size = len(xTab)*2
    cTab = [[0] * size for _ in range(size)]
    xTabExt = [0] * size

    for i in range(len(xTab)):
        xTabExt[i*2] = xTab[i]
        xTabExt[i*2 + 1] = xTab[i]

    for i in range(len(xTab)):
        cTab[i*2][0] = yTab[i]
        cTab[i*2 + 1][0] = yTab[i]
        cTab[i*2 + 1][1] = y1Tab[i]
        if i >= 1:
            cTab[i*2][1] = (cTab[i*2][0] - cTab[i*2-1][0])/(xTabExt[i*2] - xTabExt[i*2-1])

    for j in range(2, size):
        for i in range(j, size):
            cTab[i][j] = (cTab[i][j-1] - cTab[i-1][j-1])/(xTabExt[i] - xTabExt[i-j])

    return cTab


def hermit(xTab, cTab, xPoint):
        n = len(xTab)
        size = 2*n
        xTabExt = [0] * size
        ySum = 0

        for i in range(n):
            xTabExt[i * 2] = xTab[i]
            xTabExt[i * 2 + 1] = xTab[i]


        for i in range(size):
            curr = cTab[i][i]
            for j in range(i):
                curr *= (xPoint - xTabExt[j])
            ySum += curr

        return ySum

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

def plotInter(xTab, yTab, y1Tab, isChb = False):
    xplt = np.linspace(-4*math.pi, 4*math.pi, 1000)
    yplt = np.array([], float)
    yintplt_lag = np.array([], float)
    yintplt_hermit = np.array([], float)
    coef = hTabMake(xTab, yTab, y1Tab)

    maxdiff_lag = 0
    quaddiff_lag = 0

    maxdiff_hermit = 0
    quaddiff_hermit = 0

    for x in xplt:
        yplt = np.append(yplt, func(x))
        yintplt_lag = np.append(yintplt_lag, lagrange(xTab, yTab, x))
        yintplt_hermit = np.append(yintplt_hermit, hermit(xTab, coef, x))

        currdiff_lag = math.fabs(func(x) - lagrange(xTab, yTab, x))
        maxdiff_lag = max(maxdiff_lag, currdiff_lag)
        quaddiff_lag += currdiff_lag**2

        currdiff_hermit = math.fabs(func(x) - hermit(xTab, coef, x))
        maxdiff_hermit = max(maxdiff_hermit, currdiff_hermit)
        quaddiff_hermit += currdiff_hermit**2

    print("Lagrange - dokładność mierzona metodą pierwszą: ", maxdiff_lag)
    print("Lagrange - dokładność mierzona metodą drugą: ", quaddiff_lag/1000)
    print(" ")
    print("Hermit - dokładność mierzona metodą pierwszą: ", maxdiff_hermit)
    print("Hermit - dokładność mierzona metodą drugą: ", quaddiff_hermit/1000)
    print(" - - - - - - - - - - ")
    print(" ")

    plt.plot(xTab, yTab, 'ro',  xplt, yplt, 'r--', xplt, yintplt_hermit, 'g-', xplt, yintplt_lag, 'y--')
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



