from numpy import *

A = 5; B = 21; C = 2001 + 9 * 3; h = 1e-5
y = lambda x: exp(C / x)
d_y = lambda x: (y(x + h) - y(x - h)) / (2 * h)


def func(x):
    try:
        if x < 0:
            x = -x
            return -sum([x ** (i / A) for i in range(A + 1)]) - (x * B) ** (1 / 5) + y(x)
        if x > 0:
            return sum([x ** (i / A) for i in range(A + 1)]) + (x * B) ** (1 / 5) + y(x)
    except ZeroDivisionError:
        return 0


def start_x():
    x = 9
    while abs(d_y(x)) > 10**-4: x+=1
    return x


def euler(x0):
    eps = 10 ** -5; h = 0.01
    if func(x0) > func(x0 - h * func(x0)):
        while abs(func(x0)) > eps:
            x1 = x0 - h * func(x0)
            x0 = x1
    else:
        while abs(func(x0)) > eps:
            x1 = x0 + h * func(x0)
            x0 = x1
    return x0


print("root: ", euler(start_x()))
print("check: ", func(euler(start_x())))
print("DU check: ", d_y(euler(start_x())))