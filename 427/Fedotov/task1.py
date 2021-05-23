from numpy import *
import matplotlib.pyplot as plt
x = [1, 5, 10 , 100]
A = 21
for i in x:
    y = log(abs((exp(cos(i)**A)*tan(i*i))/(A*i/9+i**(3/2))))/log(2*i)
    print (y)
    
import matplotlib.pyplot as pl
x = [(i)for i in range (2, 24, 2)]
y = [3.52, 9.39, 15.77, 23.47, 31.63, 39.6, 47.96, 59.25, 68.76, 78.90, 87.87]
k = float(y[5]/x[5])
pl.figure(figsize=(15,4))
pl.subplot(1, 2, 1)
pl.title("Зависимость I от U")
pl.xlabel('U (В)')
pl.ylabel('I (А)')
pl.errorbar(x, y, xerr=0, yerr=1)
pl.grid()
def func(x, k):
    return k*x
pl.subplot(1, 2, 2)
x = linspace(1, 24, 50)
y = func(x, k)
pl.title("Общий вид графика")
pl.xlabel('x')
pl.ylabel('y')
pl.plot(x, y)
pl.grid()
pl.show()
