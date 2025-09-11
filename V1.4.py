import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import sympy as sp
import matplotlib.pyplot as plt
# V1.4

#Funcion para configurar el tema
def configurar_tema():
    """Configura el tema visual de la aplicación"""
    ctk.set_appearance_mode("black")
    ctk.set_default_color_theme("blue")

#Funcion para calcular el dominio
def calcular_dominio():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = sp.sympify(expr_text)
        dominio = sp.calculus.util.continuous_domain(f, x_sym, sp.S.Reals)
        resultado_dom.configure(text=f"Dominio: {sp.pretty(dominio)}")

        #este es la funcion
        print(expr_text)
    except Exception as e:
        resultado_dom.configure(text=f"Error calculando dominio: {e}")

#Funcion para calcular el recorrido
def calcular_recorrido():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = sp.sympify(expr_text)
        # El recorrido es la imagen de f(x) para x en el dominio real
        # Usamos function_range para obtener el rango
        recorrido = sp.calculus.util.function_range(f, x_sym, sp.S.Reals)
        resultado_rec.configure(text=f"Recorrido: {sp.pretty(recorrido)}")
    except Exception as e:
        resultado_rec.configure(text=f"Error calculando recorrido: {e}")

#Funcion para calcular la interseccion con los ejes
"agregar 'no se intersecta con el eje _' para resultados vacios'"
"resultados con fracciones pasarlo a decimal"
def calcular_ejes():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = sp.sympify(expr_text)
        # Intersección con eje Y: f(0)
        inter_y = f.subs(x_sym, 0)
        # Intersección con eje X: soluciones de f=0
        inter_x = sp.solve(f, x_sym)
        resultado_ejes.configure(text=f"Eje Y: (0, {inter_y}), Eje X: {inter_x}")
    except Exception as e:
        resultado_ejes.configure(text=f"Error calculando intersecciones: {e}")



def GraficaPLT():
    try:
        expr_text = funcion.get()
        x_sym = sp.symbols('x')
        f = sp.sympify(expr_text)
        
        # Crear valores para x manualmente (sin numpy)
        x_vals = [i/10.0 for i in range(-100, 101)]  # De -10 a 10 con paso 0.1
        
        # Calcular valores para y
        y_vals = []
        for val in x_vals:
            try:
                y_val = f.subs(x_sym, val).evalf()
                y_vals.append(y_val)
            except:
                y_vals.append(float('nan'))  # Valor no definido
        
        # Crear la gráfica
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label=f'${sp.latex(f)}$', linewidth=2)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.title('Gráfica de la Función')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo graficar la función: {e}")

#Funcion para crear la interfaz grafica
def crear_interfaz_grafica():
    """Crea y configura la interfaz gráfica principal"""
    global ventana, funcion, x, resultado_ejes, resultado_dom, resultado_rec
    
    # Configurar ventana
    ventana = ctk.CTk()
    ventana.title("Funciones")
    ventana.geometry("700x450")

    # Entrada de funcion
    etiqueta_funcion = ctk.CTkLabel(ventana, text="Ingresar función:")
    etiqueta_funcion.grid(row=0, column=0, padx=(100, 50), pady=(50, 50), sticky="w")
    funcion = ctk.CTkEntry(ventana, placeholder_text="Ej: 2x -3")
    funcion.grid(row=0, column=0, padx=(100, 50), pady=(50, 0), sticky="ew")

    # Entrada de x
    etiqueta_x = ctk.CTkLabel(ventana, text="Ingresar valor de x:")
    etiqueta_x.grid(row=2, column=0, padx=(100, 50), pady=(0, 50), sticky="w")
    x = ctk.CTkEntry(ventana, placeholder_text="Ej: 2")
    x.grid(row=2, column=0, padx=(100, 50), pady=(50, 50), sticky="ew")

    # Botón y resultado para dominio
    boton_dom = ctk.CTkButton(ventana, text="Calcular dominio", command=calcular_dominio)
    boton_dom.grid(row=0, column=1, padx=(100, 50), pady=(0, 50), sticky="ew")
    resultado_dom = ctk.CTkLabel(ventana, text="Dominio: ---")
    resultado_dom.grid(row=0, column=1, padx=(100, 50), pady=(50, 20), sticky="w")

    # Botón y resultado para recorrido
    boton_rec = ctk.CTkButton(ventana, text="Calcular recorrido", command=calcular_recorrido)
    boton_rec.grid(row=1, column=1, padx=(100, 50), pady=(10, 50), sticky="ew")
    resultado_rec = ctk.CTkLabel(ventana, text="Recorrido: ---")
    resultado_rec.grid(row=1, column=1, padx=(100, 50), pady=(50, 20), sticky="w")

    # Botón y resultado para intersecciones
    boton_ejes = ctk.CTkButton(ventana, text="Calcular intersecciones", command=calcular_ejes)
    boton_ejes.grid(row=2, column=1, padx=(100, 50), pady=(10,50), sticky="ew")
    resultado_ejes = ctk.CTkLabel(ventana, text="Intersecciones: ---")
    resultado_ejes.grid(row=2, column=1, padx=(100, 50), pady=(50, 20), sticky="w")

    boton_Grafico = ctk.CTkButton(ventana, text="Mostrar Grafico", command=GraficaPLT)
    boton_Grafico.grid(row=3, column=1, padx=(100, 50), pady=(10,50), sticky="ew")




#main
def main():
    """Función principal que inicia la aplicación"""
    configurar_tema()
    crear_interfaz_grafica()
    ventana.mainloop()

if __name__ == "__main__":
    main()
