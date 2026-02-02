############CUARTA VERSIÓN#################

#NORMALIZACIÓN DE DATOS EN LA BASE DE DATOS
#LOS DATOS SON GUARDADOS EN SQLITE EN UN ARCHIVO .DB

#EN LOS DATOS DEL CONTACTO SE AGREGÓ AHORA LA DIRECCIÓN
#VALIDACIÓN DE QUE EXISTA EL CONTACTO PARA PODER BUSCAR, EDITAR Y ELIMINAR.
#VALIDACIÓN DE QUE EDITAR DISTINGA EL VALOR DEL CONTACTO CON EL INGRESADO.

#CRUD MÁS SIMPLE
#AHORA EN EL AGREGAR CONTACTO SE PEDIRÁN TODOS LOS DATOS ENVÉS DE TENER TANTAS OPCIONES
#EN EL MENÚ DE LA APP PORQUE YA ERA DEMASIADO E IBA A LLEGAR AL 45654115

#TAMBIÉN CUANDO SE EDITA EL CONTACTO SE PIDEN TODOS LOS DATOS, NAA DE EDITAR POR SEPARADO.

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

def agregar_contacto():
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    nombre = input("Nombre: ")
    direccion = input("Dirección: ")
    cumpleanos = input("cumpleaños (dd/mm/): ")

    cursor.execute("SELECT id FROM contactos WHERE LOWER(nombre) = LOWER(?)", (nombre,))
    existe = cursor.fetchone()

    if existe:
        print(f"Ya existe un contacto con el nombre '{nombre}'. Usa un nombre distinto. ")
        conexion.close()
        return


    cursor.execute(
        "INSERT INTO contactos (nombre, direccion, cumpleanos) VALUES (?,?,?)",
        (nombre, direccion, cumpleanos if cumpleanos else None) 
    )
    contacto_id = cursor.lastrowid #ID DEL NUEVO CONTACTO

    while True:
        telefono = input("Teléfono (deja vacío si no hay): ")
        if not telefono:
            break
        else:
            cursor.execute("INSERT INTO telefonos (contacto_id, telefono) VALUES (?, ?)", (contacto_id, telefono)) 
            break

    while True:
        email = input("Email (deja vacío si no hay): ")
        if not email:
            break
        else:
            cursor.execute("INSERT INTO emails (contacto_id, email) VALUES (?, ?)", (contacto_id, email))
            break

    conexion.commit()
    conexion.close()
    print("Contacto agregado correctamente. ")



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

def editar_contacto(contacto_id):
    conexion = sqlite3.connect("agenda.db")
    cursor = conexion.cursor()

    print("Deja en blanco si no quieres cambiar ese dato. ")
    nuevo_nombre = input("Nuevo nombre: ")
    nueva_direccion = input("Nueva dirección: ")
    nuevo_cumpleanos = input("Nuevo cumpleaños (dd/mm/aaaa): ")

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

    print("\n---- Editar teléfono ----")
    while True:
        nuevo_telefono = input("Nuevo teléfono (deja vacío si no hay): ")
        if not nuevo_telefono:
            break
        else:
            cursor.execute("UPDATE telefonos SET telefono = ? WHERE contacto_id = ?", (nuevo_telefono, contacto_id))
            break

    
    print("\n---- Editar email ----")
    while True:
        nuevo_email = input("Nuevo email (deja vacío si no hay): ")
        if not nuevo_email:
            break
        else:
            cursor.execute("UPDATE emails SET email = ? WHERE contacto_id = ?", (nuevo_email, contacto_id))
            break

    conexion.commit()
    conexion.close()
    print("Contacto actualizado correctamente. ")





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
      "2.- Mostrar contactos \n"
      "3.- Editar contacto \n"
      "4.- Eliminar un contacto \n"
      "5.- Salir\n")

    respuesta = input("Elige una opción: ")

    if respuesta == "1":
        print("Escribe los datos del nuevo contacto:")
        agregar_contacto()
    
    elif respuesta == "2":
        mostrar_contactos()

    elif respuesta == "3":
        nombre = input("Nombre del contacto a editar: ")
        contacto_id = obtener_contacto_id(nombre)

        if contacto_id:
            editar_contacto(contacto_id)
        
        else:
            print("Contacto no encontrado. ")
      

    elif respuesta == "4":
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
    
    elif respuesta == "5":
        print("Saliendo de la agenda... chau")
        break

    else:
        print("Opción inválida, intenta de nuevo.")

