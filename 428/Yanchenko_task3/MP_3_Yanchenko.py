import numpy as np
import matplotlib.pyplot as plt
def plot_def(a=-0.9,b=19.1,h=0.01,y0=1):
    if a<=-1:
        return "ERROR"
    else:
        k=1
        if y0<0:
            k=-1
        C1=np.arctan(y0*y0)+a-np.log(a+1)
        X=np.linspace(a,b,int((b-a)/h)+1)
        Y=k*np.sqrt(np.tan(C1-X+np.log(X+1)))
        plt.plot(X,Y)
plot_def()