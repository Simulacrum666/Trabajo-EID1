import matplotlib.pyplot as plt
import sympy as sp
#V1.3

expresion=(input("Ingrese una funcion (X como incognita): "))   

while True:
    try:
        x_valor = int(input("Ingrese el valor de X: "))
        break
    except ValueError:
        print("Valor no válido, ingrese nuevamente")

f = sp.sympify(expresion)
x = sp.symbols('x')
y_valor = (f.subs(x, x_valor).evalf())

print(f"La función es: {f}")
print(f"La coordenada en x es: {x}", f"La coordenada en y es: {y_valor}")
print(f"El par ordenado es: ({x_valor},{y_valor})")

x_vals = [i/10 for i in range(-50, 50)] 
y_vals = [f.subs(x, val).evalf() for val in x_vals]


calcular_dominio = sp.calculus.util.continuous_domain(f, x, sp.S.Reals) 
calcular_recorrido = (min(y_vals), max(y_vals))

interseccion_x = sp.solve(f, x)
interseccion_y = f.subs(x, 0)

print(f"El dominio de la función es: {calcular_dominio}")
print(f"El recorrido de la función es: {calcular_recorrido}")

print(f"La intersección en el eje X es: {interseccion_x}")
print(f"La intersección en el eje Y es: {interseccion_y}")

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