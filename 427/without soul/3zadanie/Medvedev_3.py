** Методы программирования. 3 задание **
** Медведев Павел. 427 группа**

from numpy import *

A = 8
B = 19
C = 2001 + 9 * 3; 
h = 1e-5

def y(x):
    return exp(C/x)
def d_y(x):
    return (y(x + h) - y(x - h)) / (2 * h)
#y = lambda x: exp(C / x)
#d_y = lambda x: (y(x + h) - y(x - h)) / (2 * h)


def function(x):
    try:
        if x < 0:
            x = -x
            return -sum([x ** (i / A) for i in range(A + 1)]) - (x * B) ** (1 / 5) + y(x)
        if x > 0:
            return sum([x ** (i / A) for i in range(A + 1)]) + (x * B) ** (1 / 5) + y(x)
    except ZeroDivisionError:
        return 0


def plus_x():
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


print("Корень: ", euler(plus_x()))
print("Проверка: ", function(euler(plus_x())))
print("Провека дифф-уравнения: ", d_y(euler(plus_x()))) 
