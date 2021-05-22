import numpy as np
import sys
sys.setrecursionlimit(10**6)

def func(x,y):
    return -np.sqrt(3+y**2,dtype=complex)/(y*np.sqrt(1-x**2,dtype=complex))
y = 5
h=0.01
x=0

def kringe(x,y):
    if h*(func(x+h,y+h*func(x+h/2,y+h*func(x+h/2,y+h*func(x,y))))+2*func(x+h/2,y+h*func(x+h/2,y+h*func(x,y)))+2*func(x+h/2,y+h*func(x,y))+func(x,y))/6 > 10**(-12):
        return x,y
    else:
        return kringe(x+h,y+h*(func(x+h,y+h*func(x+h/2,y+h*func(x+h/2,y+h*func(x,y))))+2*func(x+h/2,y+h*func(x+h/2,y+h*func(x,y)))+2*func(x+h/2,y+h*func(x,y))+func(x,y))/6)
        
print(kringe(x,y))
