from sympy import nsolve, cos
from sympy.abc import x

print(nsolve(cos(x) - x, x, 2))