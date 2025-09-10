import matplotlib.pyplot as plt
import sympy as sp
#V1.2
expresion=(input("Ingrese una funcion (X como incognita): "))
x=int(input("Ingrese el valor de X: "))

f = sp.sympify(expresion)
x = sp.symbols('x')

print(f)
print(x)

x_vals = [i/10 for i in range(-10, 50)] 
y_vals = [f.subs(x, val).evalf() for val in x_vals]

print(f.subs(x, x))




plt.figure(figsize=(10, 10))
plt.plot(x_vals, y_vals, label=f'${sp.latex(f)}$', linewidth=2)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('Gráfica Funcion')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()