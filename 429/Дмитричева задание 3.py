import matplotlib.pyplot as plt
import numpy as np
import sys

sys.setrecursionlimit(10 ** 6)

fun = lambda x, y: (-1) * (np.sqrt(3 + y * y) / ((np.sqrt(1 - x * x)) * y))

yilist = []
xilist = []

xk = 0.9
i = 0
h = 0.01
yii = 0


def runge(x0, y0):
    global i
    k1 = fun(x0, y0)
    k2 = fun((x0 + h / 2), y0 + (k1 * h) / 2)
    k3 = fun((x0 + h / 2), y0 + (h * k2) / 2)
    k4 = fun(x0 + h, y0 + (h * k3))
    dely = (h * (k1 + 2 * k2 + 2 * k3 + k4)) / 6
    yi = y0 + dely
    yilist.append(yi)
    y0 = yi
    x0 += h
    xilist.append(x0)
    i += 1
    global yii
    yii = y0
    if x0 < xk:
        runge(x0, y0)
    return round(yii * 1e12) / 1e12


print('xk, yk: ',xk,',', runge(0, 1))
print(i)
plt.plot(xilist, yilist)
plt.grid()
plt.show()
