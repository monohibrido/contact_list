############TERCERA VERSIÓN#################
#LOS DATOS SON GUARDADOS EN SQLITE EN UN ARCHIVO .DB

#VALIDACIÓN DE QUE EXISTA EL CONTACTO PARA PODER BUSCAR, EDITAR Y ELIMINAR.
#VALIDACIÓN DE QUE EDITAR DISTINGA EL VALOR DEL CONTACTO CON EL INGRESADO.

import sqlite3

def crear_tabla():
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        cumpleanos TEXT
        )   
    """)
    conexion.commit()
    conexion.close()


def agregar_contacto(nombre, telefono, email, cumpleanos=None):
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO contactos (nombre, telefono, email, cumpleanos) VALUES (?,?,?,?)",
                   (nombre, telefono, email, cumpleanos))
    conexion.commit()
    conexion.close()

def mostrar_contacto():
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, telefono, email, cumpleanos FROM contactos ORDER BY nombre ASC")
    contactos = cursor.fetchall()
    conexion.close()

    if not contactos:
        print("No existen contactos guardados.")
    else:
        for c in contactos:
            print(f"Nombre: {c[0]} || teléfono: {c[1]} || email: {c[2]} || f. nacimiento: {c[3] if c[3] else 'None'}")

def buscar_contacto(nombre):
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, telefono, email, cumpleanos FROM contactos WHERE nombre = ?", (nombre,))
    contacto = cursor.fetchone()
    conexion.close()

    if contacto:
        print(f"Encontrado:\n Nombre: {contacto[0]} || teléfono: {contacto[1]} || email: {contacto[2]} || f. nacimiento: {contacto[3]}")
    else:
        print("No encontrado.")

def editar_contacto(nombre, nuevo_nombre=None, nuevo_telefono=None, nuevo_email=None, nuevo_cumpleanos=None):
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()

    actualizado = False

    if nuevo_nombre:
        cursor.execute("UPDATE contactos SET nombre = ? WHERE LOWER(nombre) = LOWER(?)", (nuevo_nombre, nombre))
        actualizado = True
    if nuevo_telefono:
        cursor.execute("UPDATE contactos SET telefono = ? WHERE LOWER(nombre) = LOWER(?)", (nuevo_telefono, nombre))
        actualizado = True
    if nuevo_email:
        cursor.execute("UPDATE contactos SET email = ? WHERE LOWER(nombre) = LOWER(?)", (nuevo_email, nombre))
        actualizado = True
    if nuevo_cumpleanos:
        cursor.execute("UPDATE contactos SET cumpleanos = ? WHERE LOWER(nombre) = LOWER(?)", (nuevo_cumpleanos, nombre))
        actualizado = True

    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()

    return filas_afectadas > 0 and actualizado

    

def eliminar_contacto(nombre):
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM contactos WHERE LOWER(nombre) = LOWER(?)", (nombre,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0

def existe_contacto(nombre):
    conexion = sqlite3.connect("contactos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM contactos WHERE LOWER(nombre) = LOWER(?)", (nombre,))
    contacto = cursor.fetchone()
    conexion.close()
    return contacto is not None


crear_tabla()

#############################################################################################


while True:
    print("---------------------------------------------------------")
    print("\n____________________AGENDA DE CONTACTOS____________________\n")
    print("1.- Agregar contacto \n"
      "2.- Ver contactos \n"
      "3.- Buscar contacto \n"
      "4.- Eliminar contacto \n"
      "5.- Editar contacto \n"
      "6.- Salir\n")

    respuesta = input("Elige una opción: ")

    if respuesta == "1":
        print("Escribe los datos del nuevo contacto:")
        nombre = input("Nombre: ")
        telefono = input("telefono: ")
        email = input("Email: ")
        cumpleanos = input("Cumpleaños (dd/mm/aaaa, opcional): ")
        agregar_contacto(nombre, telefono, email, cumpleanos if cumpleanos else None)
        print("Se ha agregado el contacto exitosamente.")

    elif respuesta == "2":
        print("-----------------------------\n")
        mostrar_contacto()

    elif respuesta == "3":
        nombre = input("Nombre a buscar: ")
        buscar_contacto(nombre)
        print("-----------------------\n")        
    
    elif respuesta == "4":
        nombre = input("Nombre a eliminar: ")
        if eliminar_contacto(nombre): 
            print("Contacto eliminado.") 
        
        else: print("Ese contacto no existe.")
      
      

    elif respuesta == "5":
        nombre = input("Nombre del contacto a editar: ")

        
        if not existe_contacto(nombre):
            print("Ese contacto no existe.")
        else:
            print("Deja en blanco si no quieres cambiar ese dato.")
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_telefono = input("Nuevo teléfono: ")
            nuevo_email = input("Nuevo email: ")
            nuevo_cumpleanos = input("Nuevo cumpleaños (dd/mm/aaaa): ")

            resultado = editar_contacto(
                nombre,
                nuevo_nombre if nuevo_nombre else None,
                nuevo_telefono if nuevo_telefono else None,
                nuevo_email if nuevo_email else None,
                nuevo_cumpleanos if nuevo_cumpleanos else None
            )

            if resultado:
                print("Contacto actualizado correctamente.")
            else:
                print("No se pudo actualizar el contacto.")



    
    elif respuesta == "6":
        print("Saliendo de la agenda... chau")
        break

    else:
        print("Opción inválida, intenta de nuevo.")


