import matplotlib.pyplot as plt
import sympy as sp
#update 1.1
expresion=(input("Ingrese una funcion (X como incognita): "))

f = sp.sympify(expresion)

print(f)

x_val=int(input("Ingrese el valor de X: "))

x=sp.symbols('x')

print(x_val)

print(f.subs(x, x_val))




#grafica def
#x = ([1, 2, 3, 4, 5])
#y = ([1, 0, 2, -3, 10])

#plt.plot(x, y)
#plt.show()