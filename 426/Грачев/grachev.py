# -*- coding: utf-8 -*-
"""
Created on Fri May  7 18:20:17 2021

@author: Vadim
"""
import numpy as np

import math
A=6#Грачев
B=20
C=1998+7**3
func= lambda x: np.exp(A*x)+x**B+math.log(x**3,C)#функциональное программирование
#func=lambda x:4-2.7**x-2*x**2
a=0.001#начальное приближение
b=0.2
c=1
epsilon_1=10**(-12)#эпсилон для проверка
i=0
while(b-a>epsilon_1):
    c=(a+b)/2 #середиа отрезка
    if(func(b)*func(c)<0): #если график между правой границей и серединой отрезка пересечет границу, значит где то между ними есть корень
        print(a,"--",b)
        a=c# cдвигаем левую границу на половину отрезка
    else:
        b=c # 
    i+=1
print(func(a))