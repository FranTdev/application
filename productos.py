from tkinter import ttk
from tkinter import *
import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, windows):
        self.wind = windows
        self.wind.title('PRODUCTOS')

        # CREATING a Frame Container
        frame = LabelFrame(self.wind, text = 'REGISTRAR NUEVO PRODUCTO')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) # Como se posiciona el elemento

        #Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0 )
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text = 'Precio').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #Button Add Product
        ttk.Button(frame, text = 'Guardar Producto', command= self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        #OUTPUT Messages
        self.message = Label(frame, text = '', fg = 'DarkOrchid4')#fg -> color 
        self.message.grid(row=4, column=0, columnspan=2, sticky= W + E)

        #Table
        self.tree = ttk.Treeview(frame, height = 10, columns = 2)
        self.tree.grid(row = 5, column=0, columnspan=2)
        self.tree.heading('#0', text = 'Nombre', anchor=CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
        #BUTTONS
        ttk.Button(frame, text='ELIMINAR', command=self.delete_product).grid(row=6,column=0,sticky= W + E)
        ttk.Button(frame, text='EDITAR', command= self.edit_product).grid(row=6,column=1, sticky=W + E)


        #Filling the Rows
        self.get_products()
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        #Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #QUERY DATA
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        #Filling Data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
    
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES (NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Producto {self.name.get()} añadido correctamente'
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Nombre y Precios son requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona lo que vas a modificar'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = f'El producto {name} ha sido eliminado satifactoriamente'
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona lo que vas a modificar'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price  = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'EDITAR'

        #OLD NAME
        Label(self.edit_wind, text='NOMBRE ANTERIOR: ').grid(row=0,column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name), state='readonly').grid(row=0,column=2)
        
        #New NAME
        Label(self.edit_wind, text = 'NUEVO NOMBRE: ').grid(row=1,column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)

        #OLD PRICE
        Label(self.edit_wind, text='PRECIO ANTERIOR: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        
        #NEW PRICE
        Label(self.edit_wind, text = 'NUEVO PRECIO: ').grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3,column=2)

        #BUTTON
        Button(self.edit_wind, text='Aceptar', command= lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4,column=2,sticky= W + E)

    def edit_records(self, new_name, name, new_price, old_price):

        if new_name == '' and new_price == '':
            self.message['text'] = f'Por favor llena las casillas'
            return
        if new_name == '':
            new_name = name
        #Se asegura de que el precio que le demos tenga siempre un valor
        if new_price == '':
            new_price = old_price
        elif not new_price.isdigit():
            self.message['text'] = f'El precio debe ser un numero'
            return
        
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name,new_price,name,old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = f'El producto {name} ha sido actualizado.'
        self.get_products()


def app_producto():
    window = Tk()
    application = Product(window)
    window.mainloop()
