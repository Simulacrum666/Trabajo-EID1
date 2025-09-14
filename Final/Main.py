#Trabajo realizado por
#Agustin Flores
#Isidora Mellado
#Franchesca Marcial
#Antonio Lara

from interfaz import configurar_tema, crear_interfaz_grafica



def main():
    configurar_tema()
    ventana = crear_interfaz_grafica()
    ventana.mainloop()

if __name__ == "__main__":
    main()