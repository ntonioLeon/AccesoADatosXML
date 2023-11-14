import AntonioWorkSpace
import YuriWorkSpace
#Validadores
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


#Menus
def menu_basico():
    choice = ""
    while choice != "0":
        print("\nMenu:")
        print("1. Menu de vehiculos")
        print("2. Menu de alquileres")
        print("0. Salir del programa")
        choice = input("Selecciona una opcion (1/2/0): ")
        #if choice == "1":
            #YuriWorkSpace.menu_vehiculo()
        if choice == "2":
            AntonioWorkSpace.menu_alquiler()
        elif choice == "0":
            print("Saliendo del programa. Hasta luego!")
        else:
            print("Opción no valida.")





