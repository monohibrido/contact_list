############CUARTA VERSIÓN#################

#NORMALIZACIÓN DE DATOS EN LA BASE DE DATOS
#LOS DATOS SON GUARDADOS EN SQLITE EN UN ARCHIVO .DB

#EN LOS DATOS DEL CONTACTO SE AGREGÓ AHORA LA DIRECCIÓN
#VALIDACIÓN DE QUE EXISTA EL CONTACTO PARA PODER BUSCAR, EDITAR Y ELIMINAR.
#VALIDACIÓN DE QUE EDITAR DISTINGA EL VALOR DEL CONTACTO CON EL INGRESADO.

import sqlite3

def crear_tablas():
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()


#TABLA CONTACTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT,
            cumpleanos TEXT           
        )
    """)
#TABLA TELÉFONOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telefonos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contacto_id INTEGER NOT NULL,
            telefono TEXT NOT NULL,
            FOREIGN KEY(contacto_id) REFERENCES contactos(id)        
        )
    """)

#TABLA DE EMAILS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contacto_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY(contacto_id) REFERENCES contactos(id)
        )
    """)

    conexion.commit()
    conexion.close()

crear_tablas()
#FUNCIONCILLAS DE AGREGAR

def agregar_contacto(nombre, direccion, cumpleanos=None):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO contactos (nombre, direccion, cumpleanos) VALUES (?,?,?)",
        (nombre, direccion, cumpleanos)
    )
    conexion.commit()
    conexion.close()
    print("Contacto agregado correctamente. ")


def agregar_telefono(contacto_id, telefono):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO telefonos (contacto_id, telefono) VALUES (?, ?)",
        (contacto_id, telefono)
    )
    conexion.commit()
    conexion.close()
    print("Teléfono agregado correctamente. ")

def agregar_email(contacto_id, email):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO emails ( contacto_id, email) VALUES (?, ?)",
        (contacto_id, email)
    )
    conexion.commit()
    conexion.close()
    print("Email agregado correctamente. ")



##### FUNCIÓN PARA LA ASOCIACIÓN DE VALORES ENTRE TABLAS.

def obtener_contacto_id(nombre):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM contactos WHERE LOWER(nombre) = LOWER(?)", (nombre,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado[0] if resultado else None

#FUNCIONCILLAS DE MOSTRAR CONTACTOS

def mostrar_contactos():
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT c.id, c.nombre, c.direccion, c.cumpleanos, t.telefono, e.email
        FROM contactos c
        LEFT JOIN telefonos t ON c.id = t.contacto_id
        LEFT JOIN emails e ON c.id = e.contacto_id
        ORDER BY c.nombre ASC
    """)

    resultados = cursor.fetchall()
    conexion.close()

    contactos = {}
    for fila in resultados:
        contacto_id, nombre, direccion, cumpleanos, telefono, email = fila
        if contacto_id not in contactos:
            contactos[contacto_id] = {
                "nombre": nombre,
                "direccion": direccion,
                "cumpleanos": cumpleanos,
                "telefono": [],
                "email": []
            }
        if telefono:
            contactos[contacto_id]["telefono"].append(telefono)
        if email:
            contactos[contacto_id]["email"].append(email)

    for contacto in contactos.values():
        print(f"\nNombre: {contacto['nombre']}")
        print(f"Dirección: {contacto['direccion']}")
        print(f"Cumpleaños: {contacto['cumpleanos']}")
        print("Teléfonos: ", ", ".join(contacto["telefono"]) if contacto["telefono"] else "None")
        print("Emails: ", ", ".join(contacto["email"]) if contacto["email"] else "None")
        print("\n#########################################")


#EDITAR CONTACTOS

def editar_contacto(contacto_id, nuevo_nombre=None, nueva_direccion=None, nuevo_cumpleanos=None):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    campos = []
    valores= []

    if nuevo_nombre:
        campos.append("nombre = ?")
        valores.append(nuevo_nombre)
    if nueva_direccion:
        campos.append("direccion = ?")
        valores.append(nueva_direccion)
    if nuevo_cumpleanos:
        campos.append("cumpleanos = ?")
        valores.append(nuevo_cumpleanos)

    if campos:
        consulta = f"UPDATE contactos SET {', '.join(campos)} WHERE id = ?"
        valores.append(contacto_id)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Contacto actualizado correctamente. ")
    else:
        print("No se ingresaron los cambios. ")
    
    conexion.close()


#EDITAR LOS TELÉFONOS DE LOS CONTACTOS

def editar_telefono(contacto_id, nuevo_telefono=None):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    campos = []
    valores= []

    if nuevo_telefono:
        campos.append("telefono = ?")
        valores.append(nuevo_telefono)
    

    if campos:
        consulta = f"UPDATE telefonos SET {', '.join(campos)} WHERE contacto_id = ?"
        valores.append(contacto_id)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Teléfono actualizado correctamente. ")
    else:
        print("No se ingresaron los cambios. ")
    
    conexion.close()


#EDITAR LOS EMAILS DE LOS CONTACTOS...UFFF

def editar_email(contacto_id, nuevo_email=None):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    campos = []
    valores = []

    if nuevo_email:
        campos.append("email = ?")
        valores.append(nuevo_email)

    if campos:
        consulta = f"UPDATE emails SET {', '.join(campos)} WHERE contacto_id = ?"
        valores.append(contacto_id)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Email actualizado correctamente.")
    else:
        print("No se ingresaron los cambios.")

    conexion.close()

#ELIMINAR CONTACTO

def eliminar_contacto(contacto_id):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM telefonos WHERE contacto_id = ?", (contacto_id,))
    cursor.execute("DELETE FROM emails WHERE contacto_id = ?" , (contacto_id,))
    cursor.execute("DELETE FROM contactos WHERE id = ?", (contacto_id,))

    conexion.commit()
    conexion.close()
    print("Contacto y sus datos asociados eliminados correctamente.")

#MENÚ USUARIO

while True:
    print("---------------------------------------------------------")
    print("\n____________________AGENDA DE CONTACTOS____________________\n")
    print("1.- Agregar contacto \n"
      "2.- Agregar teléfono al contacto \n"
      "3.- Agregar mail al contacto \n"
      "4.- Mostrar contactos \n"
      "5.- Editar contacto \n"
      "6.- Editar teléfono de un contacto \n"
      "7.- Editar email de un contacto \n"
      "8.- Eliminar un contacto \n"
      "9.- Salir\n")

    respuesta = input("Elige una opción: ")

    if respuesta == "1":
        print("Escribe los datos del nuevo contacto:")
        nombre = input("Nombre: ")
        direccion = input("dirección: ")
        cumpleanos = input("Cumpleaños (dd/mm/aaaa, opcional): ")
        agregar_contacto(nombre, direccion, cumpleanos if cumpleanos else None)
        print("Se ha agregado el contacto exitosamente.")

    elif respuesta == "2":
        print("-----------------------------\n")
        nombre = input("Nombre del contacto al que quieres agregar teléfono: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            telefono = input("Teléfono: ")
            agregar_telefono(contacto_id, telefono)
        else:
            print("Ese contacto no existe. ")

    elif respuesta == "3":
        print("-----------------------------\n")
        nombre = input("Nombre del contacto al que quieres agregar email: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            email = input("Email: ")
            agregar_email(contacto_id, email)
        else:
            print("Ese contacto no existe")

    
    elif respuesta == "4":
        mostrar_contactos()

    elif respuesta == "5":
        nombre = input("Nombre del contacto a editar: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            print("Deja en blanco si no quieres cambiar ese dato. ")
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_direccion = input("Nueva dirección: ")
            nuevo_cumpleanos = input("Nuevo cumpleaños (dd/mm/aaaa): ")

            editar_contacto(
                contacto_id,
                nuevo_nombre if nuevo_nombre else None,
                nueva_direccion if nueva_direccion else None,
                nuevo_cumpleanos if nuevo_cumpleanos else None
            )
        
        else:
            print("Contacto no encontrado. ")
      
    elif respuesta == "6":
        
        nombre = input("Nombre del contacto a editar: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            print("Deja en blanco si no quieres cambiar ese dato. ")
            nuevo_telefono = input("Nuevo teléfono: ")

            editar_telefono(
                contacto_id,
                nuevo_telefono if nuevo_telefono else None
            )
        
        else:
            print("Contacto no encontrado. ")

    elif respuesta == "7":
        
        nombre = input("Nombre del contacto a editar: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            print("Deja en blanco si no quieres cambiar ese dato. ")
            nuevo_email = input("Nuevo email: ")

            editar_email(
                contacto_id,
                nuevo_email if nuevo_email else None
            )
        
        else:
            print("Contacto no encontrado. ")

    elif respuesta == "8":
        nombre = input("Nombre del contacto a eliminar: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            confirmacion = input(f"¿Seguro que quieres eliminar a {nombre}? (s/n): ")
            if confirmacion.lower() == "s":
                eliminar_contacto(contacto_id)
            else:
                print("operación cancelada. ")
        else:
            ("Ese contacto no existe. ")
    
    elif respuesta == "9":
        print("Saliendo de la agenda... chau")
        break

    else:
        print("Opción inválida, intenta de nuevo.")
