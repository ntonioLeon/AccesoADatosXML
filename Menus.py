import GestorAlquileres
import YuriWorkSpace


# Menus
def menu_basico():
    """
    sMenu basico llamado desde el main que te manda a los diferentes submenus de vehiculos y alquileres.
    """
    root = YuriWorkSpace.cargar_arbol_xml()
    choice = ""
    while choice != "0":
        print("\nMenu:")
        print("1. Menu de vehiculos")
        print("2. Menu de alquileres")
        print("0. Salir del programa")
        choice = input("Selecciona una opcion (1/2/0): ")
        # if choice == "1":
        # YuriWorkSpace.menu_vehiculo()
        if choice == "2":
            menu_alquiler(root)
        elif choice == "0":
            print("Saliendo del programa. Hasta luego!")
        else:
            print("Opción no valida.")


# Menus Alquileres
def menu_alquiler(root):
    """
    funcion que actua como un menu y dispara los funcions
    @:param root que se manda por los funcions
    """
    choice = ""
    while choice != "0":
        print("\nMenu de Alquileres:")
        print("1. Crear un alquiler")
        print("2. Buscar un alquiler")
        print("3. Modificar un alquiler")
        print("4. Finalizar un alquiler")
        print("0. Volver al menu principal")

        choice = input("Selecciona una opcion (1/2/3/4/0): ")

        if choice == "1":
            GestorAlquileres.crear_alquiler(root)
        elif choice == "2":
            menu_busqueda(root)
        elif choice == "3":
            GestorAlquileres.modificar_alquiler(root)
        elif choice == "4":
            GestorAlquileres.finalizar_alquiler(root)
        elif choice == "0":
            print("Saliendo del menu de alquileres")
        else:
            print("Opcion no valida.")


def menu_busqueda(root):
    """
    Menu con los tres tipo de busqueda
    @:param root que se manda por los funcions
    """
    choice = ""
    while choice != "0":
        print("\nMenu de Alquileres:")
        print("1. Mostrar todos los alquileres")
        print("2. Buscar todos los alquileres de una matricula")
        print("3. Buscar todos los alquileres de un cliente (DNI)")
        print("0. Volver al menu de alquileres")

        choice = input("Selecciona una opcion (1/2/3/0): ")
        if choice == "1":
            GestorAlquileres.mostrar_todos_alquileres(root)
        elif choice == "2":
            GestorAlquileres.mostrar_por_matricula(root)
        elif choice == "3":
            GestorAlquileres.mostrar_por_dni(root)
        elif choice == "0":
            print("Saliendo del menu de busqueda.")
        else:
            print("Opcion no valida.")
