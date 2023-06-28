from tkinter import ttk
from tkinter import *
import sqlite3
import productos
import funcionesp

class Menu:
    db_name = 'database.db'
    opciones = funcionesp.productosDB() #Debo  traer estas variables de un programa externo que extraiga los nombre de la base de datos

    def __init__(self, window):
        #FUNCIONEs
        def devuelta():
            a = billete.get() - (costo.get() * cantidad.get())
            r = IntVar(value = a)
            Entry(framed, textvariable=r, state='readonly').grid(row=2,column=2) 
        def modificar_costo(NULL):
            nuevo_costo  = funcionesp.obtener_opcion(opcion_seleccionada.get())
            costo.set(int(nuevo_costo))

        #VARs
        billete = IntVar()
        cantidad = IntVar(value=1)
        opcion_seleccionada = StringVar()
        opcion_seleccionada.set("Otro")
        opcion_salida = StringVar()
        opcion_salida.set("Otro")
        costo = IntVar()
        costo.set(0)
        gasto = IntVar()
        gasto.set(0)
        
        #WINDOW
        self.window = window
        self.window.title('Menu') 

        #FRAMEs
        frame = LabelFrame(self.window, text='INGRESAR DINERO')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 10, sticky=W + E)
        frame_gastos = LabelFrame(self.window, text='RETIRAR DINERO')
        frame_gastos.grid(row = 1, column= 0, columnspan = 3, pady = 20,sticky=W+E)
        framed = LabelFrame(self.window, text = 'CALCULADORA DE DEVUELTAS')
        framed.grid(row=2, column=0, columnspan= 3, padx = 15, sticky= W + E)

        #Funcionalidad del Toggle    
        OptionMenu(frame, opcion_seleccionada, 'Otro', 'Motel' ,*self.opciones, command=modificar_costo).grid(row=1, column=2)
        OptionMenu(frame_gastos, opcion_salida, 'Motel', 'Tienda', 'Otro').grid(row=1, column=3)

        #LABELs
        Label(frame, text='PRODUCTO').grid(row=1, column=1)
        Label(frame, text='ENTRADA').grid(row=2, column=1)
        Label(frame_gastos, text='SALIDA: ').grid(row=1, column=1)
        Label(framed, text='BILLETE').grid(row=1,column=1)
        Label(framed, text='DEVUELTA').grid(row=2,column=1)

        #ENTRADAs
        Entry(frame, textvariable=cantidad, state='normal').grid(row=3 ,column=3) # LA CANTIDAD DE PRODUCTOS DEL MISMO TIPO
        Entry(frame,textvariable = costo, state='normal').grid(row=2, column=2) # <---- IMPORTANTE! VARIABLE COSTO DEBE CAMBIAR
        Entry(frame_gastos, textvariable= gasto, state='normal').grid(row=1, column=2)
        Entry(framed, textvariable=billete, state='normal').grid(row=1,column=2)

        #BOTONEs
        ttk.Button(frame, text='ACEPTAR', command=lambda: funcionesp.procesar_datos(opcion_seleccionada.get(), costo.get())).grid(row=1,column=3)
        ttk.Button(frame_gastos, text='Aceptar',command= lambda: funcionesp.procesar_salida(opcion_salida.get(), gasto.get())).grid(row=2, column=3)
        ttk.Button(framed, text='CALCULAR', command = devuelta).grid(row=3,column=2)
        ttk.Button(window, text='PRODUCTOS', command=productos.app_producto).grid(row=3, column=0,sticky=W+E)
        ttk.Button(window, text='ENVIAR A EXCEL', command=funcionesp.enviar_excel).grid(row=3,column=2, sticky=W+E)
        
if __name__ == '__main__':
    window = Tk()
    application = Menu(window)
    funcionesp.comprobar_db()
    window.mainloop()