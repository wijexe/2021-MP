import numpy as np

A = 9
B = 5
C = 2001 + 5 * 3; 
h = 0.00001

y = lambda x: np.exp(C / x)
dy = lambda x: (y(x + h) - y(x - h)) / (2 * h)


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
    while abs(dy(x)) > 10**-4: x+=1
    return x


def Eiler(x0):
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


print("Корень: ", euler(start_x()))
print("Проверка: ", func(Eiler(start_x())))
print("Проверка дифф: ", dy(Eiler(start_x()))) 
