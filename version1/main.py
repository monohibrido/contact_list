############     PRIMERA VERSIÓN      #################
#LOS DATOS SON GUARDADOS EN LA RAM

class Contacto:
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"{self.nombre} - {self.telefono} - {self.email}"


class Libreta:
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, contacto):
        self.contactos.append(contacto)

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



libreta = Libreta()

while True:
    print("\n---------AGENDA DE CONTACTOS-------------")
    print("1.- Agregar contacto \n"
      "2.- Ver contactos \n"
      "3.- Buscar contacto \n"
      "4.- Eliminar contacto \n"
      "5.- Salir")

    respuesta = input("Elige una opción: ")

    if respuesta == "1":
        print("Escribe los datos del nuevo contacto:")
        nombre = input("Nombre: ")
        telefono = input("telefono: ")
        email = input("Email: ")
          
        nuevo = Contacto(nombre, telefono, email)
        libreta.agregar_contacto(nuevo)
        print("Se ha agregado el contacto exitosamente.")

    elif respuesta == "2":
        libreta.mostrar_contactos()

    elif respuesta == "3":
        nombre = input("Nombre a buscar: ")
        resultado = libreta.buscar_contacto(nombre)

        if resultado:
            print("Encontrado: ", resultado)
        else:
            print("no encontrado.")
    
    elif respuesta == "4":
        nombre = input("Nombre a eliminar: ")
        if libreta.eliminar_contacto(nombre):
            print("Contacto eliminado.")
        else:
            print("No encontrado.")
    
    elif respuesta == "5":
        print("Saliendo de la agenda... chau")
        break

    else:
        print("Opción inválida, intenta de nuevo.")


