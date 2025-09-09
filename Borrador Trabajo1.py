import matplotlib.pyplot as plt
import sympy as sm
from sympy import solve, symbols
from sympy.abc import x

#A=input(str("Ingrese una funcion (X como incognita): "))

#B=input(str("Ingrese el valor de X: "))
x=symbols('x')
#print(B)

C=solve(2*x)
print(C)


#grafica def
#x = ([1, 2, 3, 4, 5])
#y = ([1, 0, 2, -3, 10])

#plt.plot(x, y)
#plt.show()