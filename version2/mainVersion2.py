############   SEGUNDA VERSIÓN    #################
#LOS DATOS SON GUARDADOS EN UN ARCHIVO JSON


import json

class Contacto:
    def __init__(self, nombre, telefono, email, cumpleanos=None):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.cumpleanos = cumpleanos

    def __str__(self):
        return f"{self.nombre} - {self.telefono} - {self.email} - {self.cumpleanos}"


class Libreta:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, contacto):
        self.contactos.append(contacto)
        self.contactos.sort(key=lambda c: c.nombre.lower())

    def mostrar_contactos(self):
        if not self.contactos:
            print("No hay contactos guardados")
        else:
            for c in self.contactos:
                print(c)

    def buscar_contacto(self, nombre):
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                return c
        return None

    def eliminar_contacto(self, nombre):
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                self.contactos.remove(c)
                return True
        return False
    
    def editar_contacto(self, nombre, nuevo_nombre=None, nuevo_telefono=None, nuevo_email=None, nuevo_cumpleanos=None):
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                if nuevo_nombre:
                    c.nombre = nuevo_nombre
                if nuevo_telefono:
                    c.telefono = nuevo_telefono
                if nuevo_email:
                    c.email = nuevo_email
                if nuevo_cumpleanos:
                    c.cumpleanos = nuevo_cumpleanos
                return True
            self.contactos.sort(key=lambda c: c.nombre.lower())
        return False

def guardar_contactos(libreta, archivo="contactos.json"):
    datos = []
    for c in libreta.contactos:
        datos.append({
            "nombre": c.nombre,
            "telefono": c.telefono,
            "email": c.email,
            "cumpleanos": c.cumpleanos
        })
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_contactos(libreta, archivo="contactos.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            for d in datos:
                libreta.agregar_contacto(Contacto(d["nombre"], d["telefono"], d["email"], d["cumpleanos"]))
    except FileNotFoundError:
        pass 


libreta = Libreta()
cargar_contactos(libreta)

while True:
    print("---------------------------------------------------------")
    print("\n---------AGENDA DE CONTACTOS-------------\n")
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
        nuevo = Contacto(nombre, telefono, email, cumpleanos if cumpleanos else None)
        libreta.agregar_contacto(nuevo)
        guardar_contactos(libreta)
        print("Se ha agregado el contacto exitosamente.")

    elif respuesta == "2":
        print("-----------------------------\n")
        libreta.mostrar_contactos()

    elif respuesta == "3":
        nombre = input("Nombre a buscar: ")
        resultado = libreta.buscar_contacto(nombre)
        if resultado:
            print("-----------------------\n")
            print("Encontrado: ", resultado)
        else:
            print("no encontrado.")
            print("-----------------------\n")        
    
    elif respuesta == "4":
        nombre = input("Nombre a eliminar: ")
        if libreta.eliminar_contacto(nombre):
            guardar_contactos(libreta)
            print("Contacto eliminado.")
        else:
            print("No encontrado.")

    elif respuesta == "5":
        nombre = input("Nombre del contacto a editar: ")
        contacto = libreta.buscar_contacto(nombre)
        if contacto:
            print("Deja en blanco si no quieres cambiar ese dato.")
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_telefono = input("Nuevo teléfono: ")
            nuevo_email = input("Nuevo email: ")
            nuevo_cumpleanos = input("Nuevo cumpleaños (dd/mm/aaaa): ")

            
            libreta.editar_contacto(
                nombre,
                nuevo_nombre if nuevo_nombre else None,
                nuevo_telefono if nuevo_telefono else None,
                nuevo_email if nuevo_email else None,
                nuevo_cumpleanos if nuevo_cumpleanos else None
            )
            guardar_contactos(libreta)
            print("Contacto actualizado correctamente.")
        else:
            print("Contacto no encontrado.")

    
    elif respuesta == "6":
        
        guardar_contactos(libreta)
        print("Saliendo de la agenda... chau")
        break

    else:
        print("Opción inválida, intenta de nuevo.")


