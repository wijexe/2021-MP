from numpy import *
import matplotlib.pyplot as plt
from scipy.special import lambertw
h = 0.01; eps =10**-8; y = -2.4675-0j; x = 0
f = lambda x, y:  exp(y) / ((1 + exp(x))*y)
precise_answer = lambda x: - lambertw((x - log(1 + exp(x)) + 18) / exp(1)) - 1
coord_x = linspace(-100, 100, 100)
coord_y = precise_answer(coord_x)
plt.plot(coord_x, coord_y.real)
plt.grid(True)
plt.show()
def euler_default(y, x):
    while abs(y - precise_answer(x)) > eps:
        y_iter = y + h * f(x, y)
        x += h
        y = y_iter
    return y, x
euler_default(y, x)
y_predict = lambda x, x1, y: y + (x1- x)*f(x, y)
y_correct = lambda x, x1, y: y + (x1 - x) * ((f(x, y) + f(x1, y_predict(x, x1, y)))/2)
def euler_modified(y, x):
    n = 0
    while n < 1000:
        y_iter = y_correct(x, x+h, y)
        x += h
        y = y_iter
        n+=1
    return y, x
  euler_modified(y, x)
