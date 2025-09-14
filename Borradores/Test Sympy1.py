import sympy as sp
#update 1.1
# Definir símbolos
x, y = sp.symbols('x y')

# Crear función
f = x**2 + 2*y

# Evaluar
print(f.subs({x: 5, y: 2}))
