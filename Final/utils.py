import sympy as sp
import re

def validar_entrada(expr_text):
    try:
        # Reemplazos comunes para entrada más limpia
        expr_text = expr_text.replace("^", "**") # Usar ^ como potencia
        expr_text = expr_text.replace(" ", "") # Quitar espacios

        # Insertar * entre número y variable
        expr_text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_text)
        expr_text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr_text)
        expr_text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr_text)

        # Definir variable simbólica
        x_sym = sp.symbols('x')

        # Intentar parsear con sympy
        f = sp.sympify(expr_text, locals={"x": x_sym, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "log": sp.log}, evaluate=True)
        return f
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")

def disminuir_decimal(valor, decimales=3):
    try:
        num = float(valor)
        return str(round(num, decimales)).rstrip("0").rstrip(".")
    except:
        return str(valor) # Si no es numérico (ej: infinito, símbolos)