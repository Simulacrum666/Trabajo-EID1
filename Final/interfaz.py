import customtkinter as ctk
from tkinter import messagebox
from calculos import calcular_dominio, calcular_recorrido, calcular_ejes, calcular_punto
from graficos import graficar_funcion

def configurar_tema():
    """Configura el tema visual de la aplicación"""
    ctk.set_appearance_mode("black")
    ctk.set_default_color_theme("blue")

def crear_interfaz_grafica():
    """Crea y configura la interfaz gráfica principal"""
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

    # Entrada de función (FRAME IZQUIERDO)
    frame1 = ctk.CTkFrame(ventana)
    frame1.grid(row=1, column=0, padx=(40,10), pady=(10,10), sticky="nsew")
    
    etiqueta_funcion = ctk.CTkLabel(frame1, text="Ingresar función:")
    etiqueta_funcion.pack(anchor="w", pady=5)
    funcion_entry = ctk.CTkEntry(frame1, placeholder_text="Ej: 2x -3", width=250)
    funcion_entry.pack(anchor="w", pady=5, fill="x", padx=10)

    # Entrada de x (FRAME IZQUIERDO)
    frame2 = ctk.CTkFrame(ventana)
    frame2.grid(row=3, column=0, padx=(40,10), pady=(10,10), sticky="nsew")
    
    etiqueta_x = ctk.CTkLabel(frame2, text="Ingresar valor de x:")
    etiqueta_x.pack(anchor="w", pady=5)
    x_entry = ctk.CTkEntry(frame2, placeholder_text="Ej: 2", width=250)
    x_entry.pack(anchor="w", pady=5, fill="x", padx=10)

    # Botones y resultados (FRAMES DERECHOS)
    def ejecutar_calculo_dominio():
        resultado = calcular_dominio(funcion_entry.get())
        resultado_dom.configure(text=resultado)

    def ejecutar_calculo_recorrido():
        resultado = calcular_recorrido(funcion_entry.get())
        resultado_rec.configure(text=resultado)

    def ejecutar_calculo_ejes():
        resultado = calcular_ejes(funcion_entry.get())
        resultado_ejes.configure(text=resultado)

    def ejecutar_calculo_punto():
        resultado = calcular_punto(funcion_entry.get(), x_entry.get())
        resultado_punto.configure(text=resultado)

    def ejecutar_grafico():
        try:
            graficar_funcion(funcion_entry.get(), x_entry.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Dominio (FRAME DERECHO)
    frame3 = ctk.CTkFrame(ventana)
    frame3.grid(row=0, column=1, padx=(10, 50), pady=10, sticky="ew")
    
    boton_dom = ctk.CTkButton(frame3, text="Calcular dominio", command=ejecutar_calculo_dominio)
    boton_dom.pack(anchor="w", pady=5, fill="x", padx=10)
    resultado_dom = ctk.CTkLabel(frame3, text="Dominio: ---", anchor="w", justify="left")
    resultado_dom.pack(anchor="w", pady=5, fill="x", padx=10)

    # Recorrido (FRAME DERECHO)
    frame4 = ctk.CTkFrame(ventana)
    frame4.grid(row=1, column=1, padx=(10, 50), pady=10, sticky="ew")
    
    boton_rec = ctk.CTkButton(frame4, text="Calcular recorrido", command=ejecutar_calculo_recorrido)
    boton_rec.pack(anchor="w", pady=5, fill="x", padx=10)
    resultado_rec = ctk.CTkLabel(frame4, text="Recorrido: ---", anchor="w", justify="left")
    resultado_rec.pack(anchor="w", pady=5, fill="x", padx=10)

    # Intersecciones (FRAME DERECHO)
    frame5 = ctk.CTkFrame(ventana)
    frame5.grid(row=2, column=1, padx=(10, 50), pady=10, sticky="ew")
    
    boton_ejes = ctk.CTkButton(frame5, text="Calcular intersecciones", command=ejecutar_calculo_ejes)
    boton_ejes.pack(anchor="w", pady=5, fill="x", padx=10)
    resultado_ejes = ctk.CTkLabel(frame5, text="Intersecciones: ---", anchor="w", justify="left")
    resultado_ejes.pack(anchor="w", pady=5, fill="x", padx=10)

    # Punto (FRAME DERECHO)
    frame6 = ctk.CTkFrame(ventana)
    frame6.grid(row=3, column=1, padx=(10, 50), pady=10, sticky="ew")
    
    boton_punto = ctk.CTkButton(frame6, text="Calcular punto", command=ejecutar_calculo_punto)
    boton_punto.pack(anchor="w", pady=5, fill="x", padx=10)
    resultado_punto = ctk.CTkLabel(frame6, text="Punto: ---", anchor="w", justify="left")
    resultado_punto.pack(anchor="w", pady=5, fill="x", padx=10)

    # Gráfico (FRAME DERECHO)
    frame7 = ctk.CTkFrame(ventana)
    frame7.grid(row=4, column=1, padx=(10, 50), pady=10, sticky="ew")
    
    boton_grafico = ctk.CTkButton(frame7, text="Mostrar Gráfico", command=ejecutar_grafico)
    boton_grafico.pack(anchor="w", pady=5, fill="x", padx=10)

    return ventana