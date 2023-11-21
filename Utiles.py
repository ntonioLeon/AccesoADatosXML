import AntonioWorkSpace
import YuriWorkSpace


# Validadores
'''
funcion que sirve como comprobante para las preguntas al usuario.
@:param cadena que se printeara junto a la pregunta.
'''
def si_no(cadena):
    print(cadena)
    while True:
        elec = input("Pulse 1 para si, 2 para no ")
        if elec == "1":
            return True
        elif elec == '2':
            return False
        else:
            print("Introduzca una opcion valida.")


# Menus
'''
Menu basico llamado desde el main que te manda a los diferentes submenus de vehiculos y alquileres.
'''
def menu_basico():
    tree = YuriWorkSpace.cargar_arbol_xml()
    root = tree.getroot()
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
            AntonioWorkSpace.menu_alquiler(root)
        elif choice == "0":
            print("Saliendo del programa. Hasta luego!")
        else:
            print("Opción no valida.")
