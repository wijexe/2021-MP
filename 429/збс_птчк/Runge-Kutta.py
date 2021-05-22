import numpy as np
import matplotlib.pyplot as plt

# sqrt(3 + y**2)dx + sqrt(1 - x**2)ydy = 0
# |x| < 1

f = lambda x, y: -np.sqrt(3 + y*y) / (y * np.sqrt(1 - x*x))

def getDots(Yo, h):
    X = np.linspace(-1+5*h, 1-5*h, int(1/h))
    Y = [Yo]
    for i in range(len(X)):
        K1 = f(X[i], Y[i])
        K2 = f(X[i] + h/2, Y[i] + h*K1/2)
        K3 = f(X[i] + h/2, Y[i] + h*K2/2)
        K4 = f(X[i] + h, Y[i] + h*K3)
        y_next = Y[i] + 1/6 * h * (K1 + 2*K2 + 2*K3 + K4)
        if(y_next == 0):
            print('y_next = 0')
            del X[i]
        else:
            Y.append(y_next)
    del Y[-1]
    return X, Y

# Solved by Wolframalpha:
def math_solution(Yo, x):
    y1 = np.sqrt((np.arcsin(x) - Yo)**2 - 3)
    y2 = -1 * y1
    return y1, y2


# Xo = -1
h = 1e-3
# Yo = float(input())
Yo = [3, 5, 7, 9]
for y0 in Yo:
    X, Y1 = getDots(y0, h)
    Y2 = []
    for y in Y1:
        Y2.append(-y)
    plt.plot(X, Y1, 'green')
    # plt.plot(X, Y2, 'green')


for y0 in Yo:
    Y1 = []
    Y2 = []
    for x in X:
        y1, y2 = math_solution(y0, x)
        Y1.append(y1)
        Y2.append(y2)

    plt.plot(X, Y1, 'orange')
    # plt.plot(X, Y2, 'orange')
plt.grid()
plt.show()
