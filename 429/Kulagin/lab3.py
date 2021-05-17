import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(10**6)

def func(x,y):
    return -np.sqrt(3+y**2,dtype=complex)/(y*np.sqrt(1-x**2,dtype=complex))
    
y = 5
h=0.01
x=0

def runge_cute(x,y):
    k1 = func(x,y)
    k2 = func(x+h/2,y+h*k1/2)
    k3 = func(x+h/2,y+h*k2/2)
    k4 = func(x+h,y+h*k3)
    dy = h*(k1+2*k2+2*k3+k4)/6
    if dy>10**(-12):
        return x,y
    else:
        return runge_cute(x+h, y+ dy)

print(runge_cute(x,y))
