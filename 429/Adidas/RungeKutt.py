#Cурков Никита
import numpy as np
Func=lambda x, y:-np.sqrt(3+y**2)/(np.sqrt(1-x**2)*y)
def rungeKutta(x0, y0, x, h):
    n = (int)((x - x0)/h) 
    y = y0
    for i in range(1, n + 1):
        k1 = h * Func(x0, y)
        k2 = h * Func(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * Func(x0 + 0.5 * h, y + 0.5 * k2)
        k4 = h * Func(x0 + h, y + k3)
        y = y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)
        x0 = x0 + h
    return y
epsilon=10**(-12)
x0 = 0
y = 1
x = 0.999
h = 0.001
hmin=0.00000001
if x>=1:
    print("Решений нет")
else:
    while abs(rungeKutta(x0, y, x, h)-rungeKutta(x0, y, x, h/2)) > epsilon:
        h = h / 2
        if h < hmin:
            break
        print ('y= ', rungeKutta(x0, y, x, h/2)," x= ",x)
    print ('y= ', rungeKutta(x0, y, x, h)," x= ",x)
