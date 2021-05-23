from numpy import *
import matplotlib.pyplot as plt
from scipy.special import lambertw

h = 0.01; eps =10**-8; y = -2.4675-0j; x = 0

f = lambda x, y:  exp(y) / ((1 + exp(x))*y)

precise_answer = lambda x: - lambertw((x - log(1 + exp(x)) + 18) / exp(1)) - 1

crd_x = linspace(-100, 100, 100)
crd_y = precise_answer(crd_x)
plt.plot(crd_x, crd_y.real)
plt.grid(True)
plt.show()

def euler_def(y, x):
    while abs(y - precise_answer(x)) > eps:
        y_1 = y + h * f(x, y)
        x += h
        y = y_1
    return y, x
  
euler_def(y, x)
  
y_pre = lambda x, x1, y: y + (x1- x)*f(x, y)
y_cor = lambda x, x1, y: y + (x1 - x) * ((f(x, y) + f(x1, y_pre(x, x1, y)))/2)

def euler_modif(y, x):
    n = 0
    while n < 1000:
        y_1 = y_cor(x, x+h, y)
        x += h
        y = y_1
        n+=1
    return y, x

euler_modif(y, x)
