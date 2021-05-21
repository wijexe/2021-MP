import numpy as np

#y' = -((sqrt(3+y^2)/(sqrt(1-x^2)*y))

func = lambda x, y: (-1)*(np.sqrt(3+y*y)/((np.sqrt(1-x*x))*y))

eps = 10**(-12)
x0 = 0
y0 = 1
e = 0.001

xk = 0.9
# точка в которой будет найдено значение функции

def RungeKytta(x0, y0,xk, eps):
    xi = []
    yi = []
    h = 2*eps
    i = 0
    xi.append(x0)
    yi.append(y0)
    n = (int)((xk - x0)/h)
    for i in range(0, n):
        k1 = h*func(xi[i],yi[i])
        k2 = h*func(xi[i]+h/2, yi[i] +k1/2)
        k3 = h*func(xi[i]+h/2, yi[i] +k2/2)
        k4 = h*func(xi[i]+h, yi[i] +k3)
        i +=1
        y = yi[i-1] + (k1+2*k2+2*k3+k4)/6
        x = xi[i-1] + h
        yi.append(y)
        xi.append(x)
        print('x = ', x, 'y = ', "%.12f" % y)
    return yi

RungeKytta(x0, y0, xk, e)




