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


def xesToPower(xTab, pow):
    xessum = 0
    for x in xTab:
        xessum += x**pow

    return xessum


# m = stopień wielomianu + 1
# n = liczba punktów
def aporoximate(xTab, yTab, m):
    freeParts = [0 for _ in range(m)]
    n = len(xTab)

    for i in range(m):
        for j in range(n):
            freeParts[i] += (xTab[j] ** i) * yTab[j]

    values = [[0 for _ in range(m)] for _ in range(m)]

    for i in range(m):
        for j in range(m):
            values[i][j] = xesToPower(xTab, i+j)

    #test matrixes print
    #for i in range(m):
    #    print(values[i], "   [", freeParts[i], "]")

    a = np.array(values)
    b = np.array(freeParts)
    result = np.linalg.solve(a, b)
    return result


# m = stopień wielomianu
# n = liczba punktów
def plotSpline(n, m, chb = False):
    m += 1
    xTab = [0 for _ in range(n)]
    yTab = [0 for _ in range(n)]
    diff = 8 * math.pi/(n-1)

    for i in range(n):
        xTab[i] = -4*math.pi + i*diff
        yTab[i] = func(xTab[i])

    if chb:
        scale = 4 * math.pi
        chbUnscaled = generateChbNodes(n)
        for i in range(n):
            xTab[i] = (chbUnscaled[i]+1)*scale - scale
            yTab[i] = func(xTab[i])

    print(xTab)
    print(yTab)

    result = aporoximate(xTab, yTab, m)
    #print(result)

    xplt = np.linspace(-4 * math.pi, 4 * math.pi, 1000)
    yplt = np.array([], float)
    yaproxplt = np.array([], float)

    maxdiff = 0
    quaddiff = 0

    for x in xplt:
        yplt = np.append(yplt, func(x))

        aproxval = 0
        for i in range(m):
            aproxval += result[i] * x ** i

        yaproxplt = np.append(yaproxplt, aproxval)

        currdiff = math.fabs(aproxval - func(x))
        maxdiff = max(maxdiff, currdiff)
        quaddiff += currdiff ** 2

    print(" ")
    print("Aproksymacja wielomianowa dla ", n," punktów - wielomian stopnia ", m-1)
    print("Maksymalna różnica : ", maxdiff)
    print("Uśredniony kwadrat błędu : ", quaddiff)

    plt.figure()
    plt.plot(xTab, yTab, 'ro', xplt, yplt, 'r--', xplt, yaproxplt, 'c-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Aproksymacja wielomianowa dla " + str(n) + " punktów - wielomian stopnia " + str(m-1))
    plt.show()


n = int(input("Liczba punktów : "))
m = int(input("Stopień wielomianu : "))


plotSpline(n, m)
