from tkinter import ttk
from tkinter import *
import sqlite3
import datetime
import pandas as pd

def run_query(query, parameters = ()): #EJECUTA LOS COMANDOS EN SQLite
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result
def productosDB():  #ES USADA PARA ENLISTAR LOS PRODUCTOS EN EL TOGGLE
    query = 'SELECT name FROM product'
    a = run_query(query)
    lista = [] 
    for x in a:
            
            lista.append(x)

    lista = ', '.join(str(tupla[0]) for tupla in lista)
    lista = lista.split(', ')    
    return lista   
def obtener_opcion(opcion_seleccionada): # RETORNA EL VALOR DE LA OPCION SELECCIONADA POR EL USUARIO
        
        #SI ES UNA DE ESTAS OPCIONES VA A RETORNAR UN VALOR ESPECIFICO
        if opcion_seleccionada == 'Motel':
             return 20000
        elif opcion_seleccionada == 'Otro':
             return 0
        
        #TAMBIEN SE PUEDE HACER LA CONDICION CON MANEJO DE ERRORES
        query = f"SELECT price FROM product WHERE name = '{opcion_seleccionada}'"
        a = run_query(query).fetchall()
        a = ', '.join(str(tupla[0]) for tupla in a)
        a = a.split(', ')
        a = str(a[0])
        print(str(opcion_seleccionada) + ": " + a)
        return a

def fecha_pc():
     fecha_actual = datetime.datetime.now()
     fecha = fecha_actual.date()
     return str(fecha)

def comprobar_db(): #Se debe comprobar que la fecha coincida con alguna linea de ingresos -> si no : crear fila con fecha y columnas en 0
    print(fecha_pc())
    query = f"SELECT Fecha FROM ingresos WHERE Fecha = '{fecha_pc()}';"
    l = str(run_query(query).fetchall())
    print(l)
    if l == "[]":
        dato = (fecha_pc(),0,0,0,0,0,"-",0)
        query = 'INSERT INTO ingresos (Fecha, entrada, entradatienda, salida, salidatienda, otro, nota, total) VALUES (?,?,?,?,?,?,?,?)'
        run_query(query,dato)
    elif len(l) > 0:
        print("Ya se creo la fila")
        return
    return

def procesar_datos(opcion, precio):
    fecha = fecha_pc()
    comprobar_db()
    if opcion == "Otro":
         #OTRO
         query = f"SELECT otro FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET otro = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadido a otro : {nuevo_valor}")
    
    elif opcion == "Motel":
         query = f"SELECT entrada FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET entrada = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadida a entrada: {nuevo_valor}")
    else:
         #ENTRADA TIENDA
         datos = (fecha,opcion, precio)
         print(datos)
         query = f"INSERT INTO registro_productos (Fecha, nombre, precio) VALUES (?,?,?)"
         print(query)
         #BASE DE DATOS GRANDE
         query = f"SELECT entradatienda FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET entradatienda = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadida a entrada tienda: {nuevo_valor}")
    
def procesar_salida(opcion, precio):
    print(opcion)
    print(precio)

    fecha = fecha_pc()
    comprobar_db() 
    if opcion == "Otro":
         if precio > 0:
             precio = precio * -1
         #OTRO
         query = f"SELECT otro FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET otro = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadido a otro : {nuevo_valor}")
    elif opcion == "Motel":
         if precio > 0:
             precio = precio * -1
         query = f"SELECT salida FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET salida = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadida a salida: {nuevo_valor}")
    else:
         if precio > 0:
             precio = precio * -1
         query = f"SELECT salidatienda FROM ingresos WHERE Fecha = '{fecha_pc()}'"
         resultados = run_query(query)
         anterior_valor = [resultado[0] for resultado in resultados] 
         print(anterior_valor[0])
         nuevo_valor = int(anterior_valor[0]) + precio
         print(nuevo_valor)
         queryu = f"UPDATE ingresos SET salidatienda = {nuevo_valor} WHERE Fecha = '{fecha}';" #Completar
         run_query(queryu)
         actualizar_total()
         return print(f"Añadida a salida tienda: {nuevo_valor}")
    
def actualizar_total():
     query_view = f"SELECT entrada, entradatienda, salida, salidatienda, otro FROM ingresos WHERE Fecha = '{fecha_pc()}'"
     sq = run_query(query_view) 
     a = ', '.join(str(tupla) for tupla in sq)
     a = eval(a)
     total = sum(a)
     enviar_total = f"UPDATE ingresos SET total = {total} WHERE Fecha = '{fecha_pc()}'"
     run_query(enviar_total)
     print(total)

def enviar_excel():
    print("Hola")
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('database.db')

    # Consulta SQL para seleccionar los datos de la primera tabla
    query1 = "SELECT * FROM ingresos"

    # Leer los datos de la primera tabla en un DataFrame de pandas
    df1 = pd.read_sql_query(query1, conn)

    # Consulta SQL para seleccionar los datos de la segunda tabla
    query2 = "SELECT * FROM registro_productos"

    # Leer los datos de la segunda tabla en un DataFrame de pandas
    df2 = pd.read_sql_query(query2, conn)

    # Cerrar la conexión a la base de datos SQLite
    conn.close()

    # Exportar el primer DataFrame a un archivo de Excel
    df1.to_excel('inventario.xlsx', index=False)

    # Exportar el segundo DataFrame a otro archivo de Excel
    df2.to_excel('venta.xlsx', index=False)
    print("Enviado correctamente")
    return 

    