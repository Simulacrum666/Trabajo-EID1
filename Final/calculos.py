import sympy as sp
from utils import validar_entrada, disminuir_decimal

# Funcion para calcular el dominio
def calcular_dominio(funcion_text):
    try:
        x_sym = sp.symbols('x')
        f = validar_entrada(funcion_text)

        pasos = []
        # Paso 1: Denominador
        den = sp.together(f).as_numer_denom()
        if den != 1:
            raices_den = sp.solve(sp.Eq(den, 0), x_sym)
            if raices_den:
                pasos.append(f"Paso 1: Denominador = {sp.pretty(den)} → excluir {', '.join(sp.pretty(r) for r in raices_den)}")
            else:
                pasos.append(f"Paso 1: Denominador = {sp.pretty(den)} → no excluye valores")
        else:
            pasos.append("Paso 1: No hay denominador con x")


        # Paso 2: Raíces cuadradas
        raiz_detectada = False
        for nodo in sp.preorder_traversal(f):
            if getattr(nodo, "func", None) == sp.sqrt or (nodo.is_Pow and nodo.as_base_exp()[1] == sp.Rational(1, 2)):
                raiz_detectada = True
                base = nodo.args[0] if getattr(nodo, "func", None) == sp.sqrt else nodo.as_base_exp()[0]
                pasos.append(f"Paso 2: Raíz cuadrada {sp.pretty(nodo)} → condición {sp.pretty(base)} ≥ 0")
        if not raiz_detectada:
            pasos.append("Paso 2: No hay raíces cuadradas")


        # Paso 3: Resultado final
        try:
            dominio = sp.calculus.util.continuous_domain(f, x_sym, sp.S.Reals)
            pasos.append(f"Paso 3: Dominio final = {sp.pretty(dominio)}")
        except Exception as e:
            pasos.append(f"Paso 3: No se pudo calcular dominio automáticamente ({e})")

        return "\n".join(pasos)

    except Exception as e:
        return f"Error calculando dominio: {e}"
    

# Funcion para calcular el recorrido
def calcular_recorrido(funcion_text):
    try:
        x_sym = sp.symbols('x')
        f = validar_entrada(funcion_text)

        x_vals = [i/10.0 for i in range(-100, 101)]
        y_vals = []
        
        for val in x_vals:
            try:
                y_val = f.subs(x_sym, val).evalf()
                if y_val != sp.zoo and y_val != sp.oo and y_val != -sp.oo:
                    y_vals.append(float(sp.N(y_val)))
            except:
                continue

        if y_vals:
            y_min = min(y_vals)
            y_max = max(y_vals)
            return f"Recorrido aproximado: [{disminuir_decimal(y_min)}, {disminuir_decimal(y_max)}]"
        else:
            return "No se pudo determinar el recorrido"

    except Exception as e:
        return f"Error calculando recorrido: {e}"



# Funcion para calcular la interseccion con los ejes
def calcular_ejes(funcion_text):
    try:
        x_sym = sp.symbols('x')
        f = validar_entrada(funcion_text)

        explicacion = ""
        # --- Intersección con eje Y ---
        explicacion += "1) Intersección con eje Y:\n"
        explicacion += "   Se evalúa f(0):\n"
        try:
            inter_y = f.subs(x_sym, 0)
            # intentar evaluar numéricamente
            try:
                inter_y_eval = inter_y.evalf()
            except Exception:
                inter_y_eval = None

            if inter_y_eval is None:
                explicacion += f"   f(0) = {sp.pretty(inter_y)} → No se pudo evaluar numéricamente\n\n"
                eje_y = "No definida"
            else:
                # manejar infinito/zoo
                if inter_y_eval == sp.zoo or inter_y_eval == sp.oo or inter_y_eval == -sp.oo:
                    explicacion += "   Al evaluar, la función tiende a infinito (no definida en x=0).\n\n"
                    eje_y = "No definida"
                else:
                    explicacion += f"   f(0) = {sp.pretty(inter_y)} → Punto: (0, {disminuir_decimal(inter_y_eval)})\n\n"
                    eje_y = f"(0, {disminuir_decimal(inter_y_eval)})"
        except Exception:
            explicacion += "   f(0) indefinido → No hay intersección con eje Y\n\n"
            eje_y = "No definida"

        # --- Intersección con eje X ---
        explicacion += "2) Intersecciones con eje X:\n"
        explicacion += "   Se resuelve f(x) = 0:\n"
        try:
            # descomponer f = num/den
            num, den = sp.together(f).as_numer_denom()
            explicacion += f"   Reescribimos como fracción: numerador = {sp.pretty(num)}, denominador = {sp.pretty(den)}\n"
            # obtener raíces reales del denominador para excluir
            soluciones = []
            try:
                soluciones = sp.solve(sp.Eq(num, 0), x_sym)
            except Exception:
                soluciones = sp.solve(sp.Eq(f, 0), x_sym)

            excluded = []
            if den != 1:
                try:
                    den_roots = sp.solve(sp.Eq(den, 0), x_sym)
                    excluded = [r for r in den_roots if abs(float(sp.im(sp.N(r)))) < 1e-12]
                    if excluded:
                        explicacion += f"   Raíces reales del denominador (se excluyen): {', '.join(sp.pretty(r) for r in excluded)}\n"
                except Exception:
                    pass
            # filtrar soluciones reales y válidas
            soluciones_validas = []
            for s in soluciones:
                try:
                    sN = sp.N(s)
                    if abs(float(sp.im(sN))) > 1e-8:
                        continue # no real
                except Exception:
                    continue
                # excluir si hace den = 0
                if den != 1:
                    try:
                        if abs(float(sp.N(den.subs(x_sym, s)))) < 1e-8:
                            continue
                    except Exception:
                        continue
                soluciones_validas.append(s)

            if not soluciones_validas:
                explicacion += "   No se encontraron soluciones reales válidas (o estaban excluidas por el dominio).\n"
                eje_x_str = "No se intersecta con el eje X"
            else:
                explicacion += "   Soluciones reales válidas: " + ", ".join(sp.pretty(s) for s in soluciones_validas) + "\n"
                eje_x_str = ", ".join(f"({disminuir_decimal(sp.N(s))}, 0)" for s in soluciones_validas)

        except Exception as e:
            explicacion += f"   Error resolviendo: {e}\n"
            eje_x_str = "Error"

        return explicacion + f"\nResultado: Eje Y: {eje_y}    |    Eje X: {eje_x_str}"

    except Exception as e:
        return f"Error calculando intersecciones: {e}"

def calcular_punto(funcion_text, x_val_text):
    try:
        x_sym = sp.symbols('x')
        f = validar_entrada(funcion_text)

        pasos = []
        pasos.append(f"Paso 1: Valor ingresado: x = {x_val_text}")

        # Evaluar
        try:
            x_val = float(x_val_text)
        except:
            return "Error: el valor de x no es numérico"

        try:
            y_val = f.subs(x_sym, x_val)
            y_eval = y_val.evalf()
            
            # manejar infinito/zoo
            if y_eval == sp.zoo or y_eval == sp.oo or y_eval == -sp.oo:
                pasos.append("Paso 3: La función no está definida en este valor (tiende a infinito).")
                texto = "\n".join(pasos)
                return texto + f"\n\nResultado: No existe el punto para x = {disminuir_decimal(x_val)}"

            pasos.append(f"Paso 2: Sustituimos: f({disminuir_decimal(x_val)}) = {sp.pretty(y_val)}")
            texto = "\n".join(pasos)
            return texto + f"\n\nPaso 3: Punto ({disminuir_decimal(x_val)}, {disminuir_decimal(y_eval)})"

        except Exception:
            pasos.append("Paso 3: La función no se puede evaluar en este valor.")
            texto = "\n".join(pasos)
            return texto + f"\n\nResultado: No existe el punto para x = {disminuir_decimal(x_val)}"

    except Exception as e:
        return f"Error calculando punto: {e}"