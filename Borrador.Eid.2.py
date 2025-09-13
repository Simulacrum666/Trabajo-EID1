import customtkinter as ctk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
import re

# Funcion para configurar el tema
def configurar_tema():
    """Configura el tema visual de la aplicación"""
    ctk.set_appearance_mode("black")
    ctk.set_default_color_theme("blue")

def validar_entrada(expr_text):
    try:
        # Reemplazos comunes para entrada más limpia
        expr_text = expr_text.replace("^", "**")   # Usar ^ como potencia
        expr_text = expr_text.replace(" ", "")     # Quitar espacios

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
        return str(valor)  # Si no es numérico (ej: infinito, símbolos)

# Funcion para calcular el dominio
def calcular_dominio():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = validar_entrada(expr_text)

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
            dominio = sp.S.Reals

        resultado_dom.configure(text="\n".join(pasos), anchor="w", justify="left")

    except Exception as e:
        resultado_dom.configure(text=f"Error calculando dominio: {e}")

# Funcion para calcular el recorrido
def calcular_recorrido():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = validar_entrada(expr_text)

        pasos = []
        pasos.append("Paso 1: Para calcular el recorrido, buscamos todos los posibles valores que puede tomar f(x).")

        try:
            rango = sp.calculus.util.function_range(f, x_sym, sp.S.Reals)
            pasos.append(f"Paso 2: Resultado: {sp.pretty(rango)}")
            texto = "\n".join(pasos)
            resultado_rec.configure(text=texto, anchor="w", justify="left")
        except Exception:
            resultado_rec.configure(text="No se pudo calcular el recorrido automáticamente.", anchor="w", justify="left")

    except Exception as e:
        resultado_rec.configure(text=f"Error: {e}")

# Funcion para calcular la interseccion con los ejes
def calcular_ejes():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = validar_entrada(expr_text)

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

            # resolver num = 0 (evitar soluciones espurias)
            soluciones = []
            try:
                soluciones = sp.solve(sp.Eq(num, 0), x_sym)
            except Exception:
                soluciones = sp.solve(sp.Eq(f, 0), x_sym)

            # obtener raíces reales del denominador para excluir
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
                        continue  # no real
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

        resultado_text = explicacion + f"\nResultado: Eje Y: {eje_y}    |    Eje X: {eje_x_str}"
        resultado_ejes.configure(text=resultado_text, anchor="w", justify="left")

    except Exception as e:
        resultado_ejes.configure(text=f"Error calculando intersecciones: {e}")

def calcular_punto():
    try:
        expr_text = funcion.get()
        x_val_text = x.get()
        x_sym = sp.symbols('x')
        f = validar_entrada(expr_text)

        pasos = []
        pasos.append(f"Paso 1: Valor ingresado: x = {x_val_text}")

        try:
            x_val = float(x_val_text)
        except:
            resultado_punto.configure(text="Error: el valor de x no es numérico")
            return

        # Evaluar
        try:
            y_val = f.subs(x_sym, x_val)
            y_eval = y_val.evalf()

            # manejar infinito/zoo
            if y_eval == sp.zoo or y_eval == sp.oo or y_eval == -sp.oo:
                pasos.append("Paso 3: La función no está definida en este valor (tiende a infinito).")
                texto = "\n".join(pasos)
                texto += f"\n\nResultado: No existe el punto para x = {disminuir_decimal(x_val)}"
                resultado_punto.configure(text=texto, anchor="w", justify="left")
                return

            pasos.append(f"Paso 2: Sustituimos: f({disminuir_decimal(x_val)}) = {sp.pretty(y_val)}")
            texto = "\n".join(pasos)
            texto += f"\n\nPaso 3: Punto ({disminuir_decimal(x_val)}, {disminuir_decimal(y_eval)})"
            resultado_punto.configure(text=texto, anchor="w", justify="left")

        except Exception:
            pasos.append("Paso 3: La función no se puede evaluar en este valor.")
            texto = "\n".join(pasos)
            texto += f"\n\nResultado: No existe el punto para x = {disminuir_decimal(x_val)}"
            resultado_punto.configure(text=texto, anchor="w", justify="left")

    except Exception as e:
        resultado_punto.configure(text=f"Error calculando punto: {e}")

def GraficaPLT():
    try:
        expr_text = funcion.get()
        x_val_text = x.get()
        x_sym = sp.symbols('x')
        f = validar_entrada(expr_text)

        # Crear valores para x manualmente (sin numpy)
        x_vals = [i/10.0 for i in range(-100, 101)]  # De -10 a 10 con paso 0.1

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
                y_vals.append(float('nan'))  # Valor no definido

        # Crear la gráfica
        plt.figure(figsize=(10, 7))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'f(x) = {expr_text}')
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
            
            for sol in soluciones[:3]:  # máximo 3 para no saturar
                try:
                    sol_val = float(sp.N(sol).evalf())
                    if abs(sp.im(sp.N(sol))) < 1e-8:  # solo reales
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
        plt.title(f'Análisis de la función f(x) = {expr_text}', 
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
        messagebox.showerror("Error", f"No se pudo graficar la función: {e}")

# Funcion para crear la interfaz grafica
def crear_interfaz_grafica():
    """Crea y configura la interfaz gráfica principal"""
    global ventana, funcion, x, resultado_ejes, resultado_dom, resultado_rec, resultado_punto

    # Configurar ventana
    ventana = ctk.CTk()
    ventana.title("Funciones")
    ventana.geometry("950x650")

    # Configurar grid principal: 2 columnas
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=3)

    # Dar peso a las filas para que crezcan
    for i in range(5):
        ventana.grid_rowconfigure(i, weight=1)

    # Entrada de funcion
    frame1 = ctk.CTkFrame(ventana, height=300)
    frame1.grid(row=1, column=0, padx=(40,10), pady=(10,10), sticky="nsew")
    etiqueta_funcion = ctk.CTkLabel(frame1, text="Ingresar función:")
    etiqueta_funcion.pack(anchor="w", pady=5)
    funcion = ctk.CTkEntry(frame1, placeholder_text="Ej: 2x -3", width=300)
    funcion.pack(anchor="w", pady=5, fill="x")

    # Entrada de x
    frame2 = ctk.CTkFrame(ventana, height=300)
    frame2.grid(row=3, column=0, padx=(40,10), pady=(10,10), sticky="nsew")
    etiqueta_x = ctk.CTkLabel(frame2, text="Ingresar valor de x:")
    etiqueta_x.pack(anchor="w", pady=5)
    x = ctk.CTkEntry(frame2, placeholder_text="Ej: 2", width=300)
    x.pack(anchor="w", pady=5, fill="x")

    # Botón y resultado para dominio
    frame3 = ctk.CTkFrame(ventana, height=120)
    frame3.grid(row=0, column=1, padx=(10, 50), pady=10, sticky="ew")
    boton_dom = ctk.CTkButton(frame3, text="Calcular dominio", command=calcular_dominio)
    boton_dom.pack(anchor="w", pady=5, fill="x")
    resultado_dom = ctk.CTkLabel(frame3, text="Dominio: ---", anchor="w", justify="left", wraplength=700)
    resultado_dom.pack(anchor="w", pady=5, fill="x")

    # Botón y resultado para recorrido
    frame4 = ctk.CTkFrame(ventana, height=120)
    frame4.grid(row=1, column=1, padx=(10, 50), pady=10, sticky="ew")
    boton_rec = ctk.CTkButton(frame4, text="Calcular recorrido", command=calcular_recorrido)
    boton_rec.pack(anchor="w", pady=5, fill="x")
    resultado_rec = ctk.CTkLabel(frame4, text="Recorrido: ---", anchor="w", justify="left", wraplength=700)
    resultado_rec.pack(anchor="w", pady=5, fill="x")

    # Botón y resultado para intersecciones
    frame5 = ctk.CTkFrame(ventana, height=120)
    frame5.grid(row=2, column=1, padx=(10, 50), pady=10, sticky="ew")
    boton_ejes = ctk.CTkButton(frame5, text="Calcular intersecciones", command=calcular_ejes)
    boton_ejes.pack(anchor="w", pady=5, fill="x")
    resultado_ejes = ctk.CTkLabel(frame5, text="Intersecciones: ---", anchor="w", justify="left", wraplength=700)
    resultado_ejes.pack(anchor="w", pady=5, fill="x")

    # Botón y resultado para punto dado x
    frame6 = ctk.CTkFrame(ventana, height=120)
    frame6.grid(row=3, column=1, padx=(10, 50), pady=10, sticky="ew")
    boton_punto = ctk.CTkButton(frame6, text="Calcular punto", command=calcular_punto)
    boton_punto.pack(anchor="w", pady=5, fill="x")
    resultado_punto = ctk.CTkLabel(frame6, text="Punto: ---", anchor="w", justify="left", wraplength=700)
    resultado_punto.pack(anchor="w", pady=5, fill="x")

    # Boton para grafico
    frame7 = ctk.CTkFrame(ventana, height=100)
    frame7.grid(row=4, column=1, padx=(10, 50), pady=10, sticky="ew")
    boton_Grafico = ctk.CTkButton(frame7, text="Mostrar Gráfico", command=GraficaPLT)
    boton_Grafico.pack(anchor="w", pady=5, fill="x")

# main
def main():
    """Función principal que inicia la aplicación"""
    configurar_tema()
    crear_interfaz_grafica()
    ventana.mainloop()

if __name__ == "__main__":
    main()
