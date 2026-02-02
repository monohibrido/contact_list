import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# VENTANA PRINCIPAL
app = tb.Window(themename="darkly")
app.title("Agenda de Contactos")
app.geometry("1200x800")



#FUNCIONCILLAS

def mostrar_home():
   
    print("Volviendo a HOME (tabla principal)")

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
        tabla.insert("", "end", values=(
            nombre_var.get(),
            direccion_var.get(),
            cumpleanos_var.get(),
            categoria_var.get(),
            telefono_var.get(),
            email_var.get(),
        ))
        popup.destroy()

    tb.Button(popup, text="Guardar", bootstyle=SUCCESS, command=guardar_contacto).pack(pady=10)

def gestionar_contactos():
    
    print("Mostrando tabla de gestión de contactos")

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


app.mainloop()
