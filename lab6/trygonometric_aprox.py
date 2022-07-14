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


# m = stopień wielomianu
# n = liczba punktów
def aproximateTryg(xTab, yTab, m):
    n = len(xTab)
    a0 = sum(yTab)/n
    factors = [[0,0] for _ in range(m)]

    for j in range(1, m+1):
        curr_a = 0
        curr_b = 0
        for i in range(n):
            curr_a += yTab[i] * math.cos(j * (xTab[i] - 4*math.pi)/4)
            curr_b += yTab[i] * math.sin(j * (xTab[i] - 4*math.pi)/4)

        curr_a *= (2/n)
        curr_b *= (2/n)
        factors[j-1][0] = curr_a
        factors[j-1][1] = curr_b

    #print(a0)
    #print(factors)

    return factors


# m = stopień wielomianu
# n = liczba punktów
def plotSpline(n, m, chb = False):
    #m += 1
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

    a0 = sum(yTab)/n
    factors = aproximateTryg(xTab, yTab, m)

    xplt = np.linspace(-4 * math.pi, 4 * math.pi, 1000)
    yplt = np.array([], float)
    yaproxplt = np.array([], float)

    maxdiff = 0
    quaddiff = 0

    for x in xplt:
        yplt = np.append(yplt, func(x))

        aproxval = a0
        for j in range(m):
            aproxval += factors[j][0] * math.cos((j+1) * (x - 4 * math.pi)/4)
            aproxval += factors[j][1] * math.sin((j+1) * (x - 4 * math.pi)/4)

        yaproxplt = np.append(yaproxplt, aproxval)

        currdiff = math.fabs(aproxval - func(x))
        maxdiff = max(maxdiff, currdiff)
        quaddiff += currdiff ** 2

    #print("punkty: ", n, "  stopień:", m, "    błąd: ", round(maxdiff*100)/100)

    print(" ")
    print("Aproksymacja wielomianowa dla ", n," punktów - wielomian stopnia ", m)
    print("Maksymalna różnica : ", maxdiff)
    print("Uśredniony kwadrat błędu : ", quaddiff)

    plt.figure()
    plt.plot(xTab, yTab, 'ro', xplt, yplt, 'r--', xplt, yaproxplt, 'c-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Aproksymacja trygonometryczna dla " + str(n) + " punktów - wielomian stopnia " + str(m))
    plt.show()
 

n = int(input("Liczba punktów : "))
m = int(input("Stopień wielomianu : "))

plotSpline(n, m)
