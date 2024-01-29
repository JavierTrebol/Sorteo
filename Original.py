import tkinter as tk
from tkinter import messagebox
import json

# Función para cargar los datos desde el archivo
def cargar_datos():
    datos = []
    with open("resultados_eurojackpot.txt", "r") as archivo:
        for linea in archivo:
            try:
                resultado = json.loads(linea)
                datos.append(resultado)
            except ValueError:
                continue
    return datos

# Función para buscar resultados en base a los criterios seleccionados
def buscar_resultados():
    año = entry_año.get()
    mes = entry_mes.get()

    # Cargar los datos desde el archivo
    datos = cargar_datos()

    # Realizar la búsqueda de resultados
    resultados_encontrados = []

    for resultado in datos:
        fecha_resultado = resultado["fecha"]
        año_resultado, mes_resultado, _ = fecha_resultado.split("-")

        if año and año != año_resultado:
            continue

        if mes and mes != mes_resultado:
            continue

        resultados_encontrados.append(resultado)

    # Borrar los datos anteriores en el archivo
    with open("resultados_encontrados.txt", "w") as archivo:
        archivo.write("")

    # Guardar los resultados encontrados en un archivo de texto
    with open("resultados_encontrados.txt", "a") as archivo:
        for resultado in resultados_encontrados:
            fecha = resultado["fecha"]
            numeros_euro = resultado["numeros_principales"]
            numeros_sol = resultado["euro_numeros"]
            archivo.write(f"Euro: {numeros_euro}, Sol: {numeros_sol}\n")

    # Mostrar los resultados en el cuadro de texto
    txt_resultados.delete("1.0", tk.END)
    if resultados_encontrados:
        for resultado in resultados_encontrados:
            fecha = resultado["fecha"]
            euro = resultado["numeros_principales"]
            sol = resultado["euro_numeros"]
            txt_resultados.insert(tk.END, f" {fecha}, {euro}, Soles: {sol}\n")
    else:
        txt_resultados.insert(tk.END, "No se encontraron resultados.")

# Función para crear las estadísticas de números y soles
def crear_estadisticas():
    estadisticas_euro = {}
    estadisticas_sol = {}

    # Leer el archivo con los resultados encontrados
    with open("resultados_encontrados.txt", "r") as archivo:
        lineas = archivo.readlines()

        for linea in lineas:
            linea = linea.strip()

            if linea.startswith("Euro:"):
                numeros_euro, numeros_sol = linea.split(", Sol:")
                numeros_euro = [int(num.strip()) for num in numeros_euro.split("[")[1].rstrip("]").split(",")]
                numeros_sol = [int(num.strip()) for num in numeros_sol.split("[")[1].rstrip("]").split(",")]

                for numero in numeros_euro:
                    if numero >= 1 and numero <= 50:
                        if numero in estadisticas_euro:
                            estadisticas_euro[numero] += 1
                        else:
                            estadisticas_euro[numero] = 1

                for numero in numeros_sol:
                    if numero >= 1 and numero <= 12:
                        if numero in estadisticas_sol:
                            estadisticas_sol[numero] += 1
                        else:
                            estadisticas_sol[numero] = 1

# Borrar los datos anteriores en el archivo
    with open("estadisticas.txt", "w") as archivo:
        archivo.write("")

    # Guardar las estadísticas en un archivo de texto
    with open("estadisticas.txt", "w") as archivo:
        # Escribir las estadísticas de los números Euro
        archivo.write("Estadísticas de los números Euro:\n")
        for numero in range(1, 51):
            apariciones = estadisticas_euro.get(numero, 0)
            archivo.write(f"{apariciones}\t{numero}\n")

        # Escribir las estadísticas de los números Sol
        archivo.write("\nEstadísticas de los números Sol:\n")
        for numero in range(1, 13):
            apariciones = estadisticas_sol.get(numero, 0)
            archivo.write(f"{apariciones}\t{numero}\n")

    return estadisticas_euro, estadisticas_sol

#funcion para leer las estadisticas y mostrarlas ordenadas
def mostrar_estadisticas():
    datos_euro = []
    datos_sol = []

    # Leer el archivo de texto y obtener los datos
    with open("estadisticas.txt", "r") as archivo:
        lineas = archivo.readlines()

        datos_euro = []
        datos_sol = []

        for linea in lineas:
            if linea.strip() and not linea.startswith("Estadísticas de"):  # Saltar líneas en blanco y encabezados
                apariciones, numero = linea.strip().split("\t")
                if linea.startswith("Estadísticas de los números Euro"):
                    datos_euro.append((int(apariciones), int(numero)))
                elif linea.startswith("Estadísticas de los números Sol"):
                    datos_sol.append((int(apariciones), int(numero)))

    # Ordenar los datos de los números Euro por el número de apariciones
    datos_euro_ordenados = sorted(datos_euro, key=lambda x: x[0], reverse=True)

    # Generar una cadena ordenada para los números Euro
    estadisticas_euro_str = " vgmxfg"
    for apariciones, numero in datos_euro_ordenados:
        estadisticas_euro_str += f"Número: {numero} - Apariciones: {apariciones}\n"

    txt_estadisticas_euro.insert(tk.END, estadisticas_euro_str)

    # Ordenar los datos de los números Sol por el número de apariciones
    datos_sol_ordenados = sorted(datos_sol, key=lambda x: x[0], reverse=True)

    # Generar una cadena ordenada para los números Sol
    estadisticas_sol_str = "no hay datos"
    for apariciones, numero in datos_sol_ordenados:
        estadisticas_sol_str += f"Número: {numero} - Apariciones: {apariciones}\n"

    txt_estadisticas_sol.insert(tk.END, estadisticas_sol_str)

    return  datos_euro, datos_sol
    

def estadisticas():
    crear_estadisticas()
    mostrar_estadisticas()
  
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Eurojackpot App")
ventana.geometry("800x1200")

# Crear etiquetas y campos de entrada para el año y mes de búsqueda
lbl_año = tk.Label(ventana, text="Año: (XXXX)")
lbl_año.pack()

entry_año = tk.Entry(ventana)
entry_año.pack()

lbl_mes = tk.Label(ventana, text="Mes: (XX)")
lbl_mes.pack()

entry_mes = tk.Entry(ventana)
entry_mes.pack()

# Crear botón de búsqueda
btn_buscar = tk.Button(ventana, text="<<<      Buscar      >>>", command=buscar_resultados)
btn_buscar.pack()

# Crear etiqueta para las estadísticas de los números Euro
lbl_resultados_euro = tk.Label(ventana, text="Resultados solicitados:")
lbl_resultados_euro.pack()

# Crear cuadro de texto para mostrar los resultados
txt_resultados = tk.Text(ventana, height=30)
txt_resultados.pack()

# Crear botón de búsqueda Y LLAMADA A LA FUNCION CREAR ESTADISTICAS
btn_buscar = tk.Button(ventana, text="<<<      Estadisticas      >>>", command=estadisticas)
btn_buscar.pack()

# Crear etiqueta para las estadísticas de los números Euro
lbl_estadisticas_euro = tk.Label(ventana, text="Estadísticas de los números Euro:")
lbl_estadisticas_euro.pack()

# Crear cuadro de texto para mostrar las estadísticas de los números Euro
txt_estadisticas_euro = tk.Text(ventana, height=15)
txt_estadisticas_euro.pack()

# Crear etiqueta para las estadísticas del número Sol
lbl_estadisticas_sol = tk.Label(ventana, text="Estadísticas del número Sol:")
lbl_estadisticas_sol.pack()

# Crear cuadro de texto para mostrar las estadísticas del número Sol
txt_estadisticas_sol = tk.Text(ventana, height=15)
txt_estadisticas_sol.pack()


ventana.mainloop()