#AHORA VAMOS A AGREGARLE SQLITE PARA PODER GUARDAR LOS DATOS EN UN .DB

import sqlite3
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# VENTANA PRINCIPAL
app = tb.Window(themename="darkly")
app.title("Agenda de Contactos")
app.geometry("1200x800")

#CONEXIÓN A LA DB
conexion = sqlite3.connect("contactos.db")
cursor = conexion.cursor()

#TABLAS

cursor.execute("""
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    direccion TEXT,
    cumpleanos TEXT,
    categoria TEXT,
    telefono TEXT,
    email TEXT
)                
""")
conexion.commit()


#FUNCIONCILLAS

def mostrar_home():
   
    print("Volviendo a HOME (tabla principal)")

def cargar_contactos():
    tabla.delete(*tabla.get_children())

    cursor.execute("SELECT nombre, direccion, cumpleanos, categoria, telefono, email FROM contactos")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)

def agregar_contacto():

    popup = tb.Toplevel(app)  
    popup.title("Agregar contacto")
    popup.geometry("400x600")

    nombre_var = tk.StringVar()
    direccion_var = tk.StringVar()
    cumpleanos_var = tk.StringVar()
    categoria_var = tk.StringVar()
    telefono_var = tk.StringVar()
    email_var = tk.StringVar()

    tb.Label(popup, text="Nombre:").pack(pady=5)
    tb.Entry(popup, textvariable=nombre_var).pack(pady=5)

    tb.Label(popup, text="Dirección:").pack(pady=5)
    tb.Entry(popup, textvariable=direccion_var).pack(pady=5)

    tb.Label(popup, text="Cumpleaños:").pack(pady=5)
    tb.Entry(popup, textvariable=cumpleanos_var).pack(pady=5)

    tb.Label(popup, text="Categoría:").pack(pady=5)
    tb.Combobox(popup, textvariable=categoria_var, values=["Familia", "Trabajo", "Amigos"]).pack(pady=5)

    tb.Label(popup, text="Teléfono:").pack(pady=5)
    tb.Entry(popup, textvariable=telefono_var).pack(pady=5)

    tb.Label(popup, text="Email:").pack(pady=5)
    tb.Entry(popup, textvariable=email_var).pack(pady=5)    

    def guardar_contacto():
        cursor.execute("""
        INSERT INTO contactos (nombre, direccion, cumpleanos, categoria, telefono, email)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre_var.get(), direccion_var.get(), cumpleanos_var.get(), categoria_var.get(), telefono_var.get(), email_var.get()))
        conexion.commit()

        cargar_contactos()
        popup.destroy()

    tb.Button(popup, text="Guardar", bootstyle=SUCCESS, command=guardar_contacto).pack(pady=10)

def gestionar_contactos():
    popup = tb.Toplevel(app)
    popup.title("Gestionar contactos")
    popup.geometry("900x400")

    # TABLA DEL POPUP
    columns = ("ID", "Nombre", "Dirección", "Cumpleaños", "Categoría", "Teléfono", "Email", "Editar", "Eliminar")
    tabla_gestion = tb.Treeview(popup, columns=columns, show="headings")
    tabla_gestion.pack(fill=BOTH, expand=True)

    for col in columns:
        tabla_gestion.heading(col, text=col, anchor="center")
        tabla_gestion.column(col, width=100, anchor="center")

    # CARGAR DATOS
    cursor.execute("SELECT id, nombre, direccion, cumpleanos, categoria, telefono, email FROM contactos")
    for fila in cursor.fetchall():
        tabla_gestion.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], "Editar", "Eliminar"))

    #DECTECTAR CLIC
    def click_tabla(event):
        item_id = tabla_gestion.identify_row(event.y)
        col_id = tabla_gestion.identify_column(event.x)

        if item_id:
            valores = tabla_gestion.item(item_id, "values")
            contacto_id = valores[0]

            if col_id == "#8":  
                editar_contacto(contacto_id, valores, tabla_gestion, item_id)

            elif col_id == "#9": 
                from tkinter import messagebox
                if messagebox.askyesno("Confirmar", f"¿Eliminar contacto {valores[1]}?"):
                    cursor.execute("DELETE FROM contactos WHERE id=?", (contacto_id,))
                    conexion.commit()
                    cargar_contactos()
                    tabla_gestion.delete(item_id)

    tabla_gestion.bind("<Button-1>", click_tabla)


def eliminar_contacto():
    popup = tb.Toplevel(app)
    tabla_gestion = tb.Treeview(popup, columns=columns, show="headings")
    seleccionado = tabla_gestion.selection()
    if seleccionado:
        valores = tabla_gestion.item(seleccionado, "values")
        contacto_id = valores[0]

        from tkinter import messagebox
        if messagebox.askyesno("Confirmar", f"¿Eliminar contacto {valores[1]}?"):
            cursor.execute("DELETE FROM contactos WHERE id=?", (contacto_id,))
            conexion.commit()
            cargar_contactos()
            tabla_gestion.delete(seleccionado)

def editar_contacto(contacto_id, valores, tabla_gestion, item_id):
    edit_popup = tb.Toplevel(app)
    edit_popup.title("Editar contacto")
    edit_popup.geometry("400x600")

    nombre_var = tk.StringVar(value=valores[1])
    direccion_var = tk.StringVar(value=valores[2])
    cumpleanos_var = tk.StringVar(value=valores[3])
    categoria_var = tk.StringVar(value=valores[4])
    telefono_var = tk.StringVar(value=valores[5])  
    email_var = tk.StringVar(value=valores[6])

    tb.Label(edit_popup, text="Nombre: ").pack(pady=5)
    tb.Entry(edit_popup, textvariable=nombre_var).pack(pady=5)

    tb.Label(edit_popup, text="Dirección: ").pack(pady=5)
    tb.Entry(edit_popup, textvariable=direccion_var).pack(pady=5)

    tb.Label(edit_popup, text="Cumpleaños: ").pack(pady=5)
    tb.Entry(edit_popup, textvariable=cumpleanos_var).pack(pady=5)

    tb.Label(edit_popup, text="Categoría: ").pack(pady=5)
    tb.Combobox(edit_popup, textvariable=categoria_var, values=["Familia","Trabajo", "Amigos"]).pack(pady=5)

    tb.Label(edit_popup, text="Teléfono: ").pack(pady=5)
    tb.Entry(edit_popup, textvariable=telefono_var).pack(pady=5)

    tb.Label(edit_popup, text="Email: ").pack(pady=5)
    tb.Entry(edit_popup, textvariable=email_var).pack(pady=5)

    def guardar_cambios():
        cursor.execute("""
        UPDATE contactos
        SET nombre=?, direccion=?, cumpleanos=?, categoria=?, telefono=?, email=?
        WHERE id=?            
        """, (nombre_var.get(), direccion_var.get(), cumpleanos_var.get(), categoria_var.get(), telefono_var.get(), email_var.get(), contacto_id))
        conexion.commit()
        cargar_contactos()
        edit_popup.destroy()

        tabla_gestion.item(item_id, values=(contacto_id, nombre_var.get(), direccion_var.get(), cumpleanos_var.get(), categoria_var.get(), telefono_var.get(), email_var.get(), "Editar", "Eliminar"))

    tb.Button(edit_popup, text="Guardar cambios", bootstyle=INFO, command=guardar_cambios).pack(pady=10)


def gestionar_categorias():
 
    popup = tb.Toplevel(app)
    popup.title("Gestionar categorías")
    popup.geometry("400x300")

    tb.Label(popup, text="Lista de categorías").pack(pady=5)
    tb.Label(popup, text="Categoría:").pack(pady=5)
    tb.Combobox(popup, values=["Familia", "Trabajo", "Amigos"]).pack(pady=5)

    tb.Button(popup, text="Agregar categoría", bootstyle=SUCCESS).pack(pady=5)
    tb.Button(popup, text="Editar categoría", bootstyle=INFO).pack(pady=5)
    tb.Button(popup, text="Eliminar categoría", bootstyle=DANGER).pack(pady=5)


#MENÚ SUPERIOR

menu_frame = tb.Frame(app)
menu_frame.pack(fill=X, pady=10)

btn_home = tb.Button(menu_frame, text="HOME", bootstyle=PRIMARY, command=mostrar_home)
btn_home.pack(side=LEFT, padx=5)

btn_agregar = tb.Button(menu_frame, text="Agregar contacto", bootstyle=SUCCESS, command=agregar_contacto)
btn_agregar.pack(side=LEFT, padx=5)

btn_gestionar = tb.Button(menu_frame, text="Gestionar contactos", bootstyle=INFO, command=gestionar_contactos)
btn_gestionar.pack(side=LEFT, padx=5)

btn_categorias = tb.Button(menu_frame, text="Gestionar categorías", bootstyle=WARNING, command=gestionar_categorias)
btn_categorias.pack(side=LEFT, padx=5)


#TABLA PRINCIPAL DE LA VISTA PRINCIPAL

columns = ("Nombre", "Dirección", "Cumpleaños", "Categoría", "Teléfonos", "Emails")
tabla = tb.Treeview(app, columns=columns, show="headings")
tabla.pack(fill=BOTH, expand=True)

for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, width=120, anchor=CENTER)


cargar_contactos()
app.mainloop()
