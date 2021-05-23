from numpy import *
import math
import scipy.signal as ss
import matplotlib.pyplot as plt

f = lambda x,a: log(abs(((np.exp((np.cos(x))**a))*np.tan(x**2))/((a*x)/9+x**1.5)))/np.log(2*x)

x=[1,5,10,100]
k=[]
for i in range (4):
    g=f(x[i],5)
    k.append(g)
print(k)

a=19
x=np.linspace(1,100,200)
y=f(x,a)
plt.figure(figsize=(15,5))
plt.plot(x,y)
plt.grid(True)
x=[1,5,10,100]
y=[]
y=k
plt.errorbar(x, y, xerr=2, yerr=0.08)
plt.grid()
plt.show()
