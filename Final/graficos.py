import sympy as sp
import matplotlib.pyplot as plt
from utils import validar_entrada, disminuir_decimal

def graficar_funcion(funcion_text, x_val_text=""):
    try:
        x_sym = sp.symbols('x')
        f = validar_entrada(funcion_text)

        # Crear valores para x manualmente (sin numpy)
        x_vals = [i/10.0 for i in range(-100, 101)] # De -10 a 10 con paso 0.1

        # Calcular valores para y
        y_vals = []
        
        for val in x_vals:
            try:
                y_val = f.subs(x_sym, val).evalf()
                # manejar zoo/inf
                if y_val == sp.zoo or y_val == sp.oo or y_val == -sp.oo:
                    y_vals.append(float('nan'))
                else:
                    y_vals.append(float(sp.N(y_val)))
            except:
                y_vals.append(float('nan')) # Valor no definido

        # Crear la gráfica
        plt.figure(figsize=(10, 7))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'f(x) = {funcion_text}')
        plt.axhline(0, color='black', linewidth=1, alpha=0.8, label='Eje X')
        plt.axvline(0, color='black', linewidth=1, alpha=0.8, label='Eje Y')
        
        try:
            # Intersección eje Y
            inter_y = f.subs(x_sym, 0).evalf()
            if inter_y != sp.zoo and inter_y != sp.oo and inter_y != -sp.oo:
                y_val = float(inter_y)
                plt.plot(0, y_val, 'ro', markersize=10, 
                        label=f'Intersección eje Y: (0, {disminuir_decimal(y_val)})')
        except:
            pass

        try:
            # Intersecciones eje X
            num, den = sp.together(f).as_numer_denom()
            soluciones = sp.solve(sp.Eq(num, 0), x_sym)
            x_intersections = []
            
            for sol in soluciones[:3]: # máximo 3 para no saturar
                try:
                    sol_val = float(sp.N(sol).evalf())
                    if abs(sp.im(sp.N(sol))) < 1e-8:
                        plt.plot(sol_val, 0, 'go', markersize=10)
                        x_intersections.append(sol_val)
                except:
                    continue
            if x_intersections:
                # Solo una etiqueta para todas las intersecciones X
                plt.plot([], [], 'go', markersize=10, 
                        label=f'Intersecciones eje X: {len(x_intersections)} punto(s)')
        except:
            pass
        


        # 4. PUNTO EVALUADO (si existe)
        if x_val_text.strip():
            try:
                x_eval = float(x_val_text)
                y_eval = f.subs(x_sym, x_eval).evalf()
                if y_eval != sp.zoo and y_eval != sp.oo and y_eval != -sp.oo:
                    plt.plot(x_eval, float(y_eval), 'mo', markersize=12, 
                            label=f'Punto evaluado: ({disminuir_decimal(x_eval)}, {disminuir_decimal(float(y_eval))})')
            except:
                pass
        
        plt.title(f'Análisis de la función f(x) = {funcion_text}', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Variable independiente (x)', fontsize=13)
        plt.ylabel('Variable dependiente f(x)', fontsize=13)
        plt.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
        plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
        plt.xlim(-10, 10)
        plt.ylim(-15, 15)
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        raise Exception(f"No se pudo graficar la función: {e}")