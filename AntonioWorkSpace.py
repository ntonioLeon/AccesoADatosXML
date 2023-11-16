import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import os
import Validador
import Utiles

file_path = ".\\datos.xml"


def prettify(elem, level=0):
    indent = "    "  # 4 espacios por nivel
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for subelem in elem:
            prettify(subelem, level + 1)
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def obtener_ultimo_id_alquiler(root):
    alquileres = root.find('Alquileres')
    ultimos_alquileres = alquileres.findall('Alquiler[@idAlquiler]')

    if ultimos_alquileres:
        ultimo_id = max(int(alquiler.get('idAlquiler')) for alquiler in ultimos_alquileres)
        return ultimo_id + 1
    else:
        return 1


def conseguir_precio_por_id(root, id_vehiculo):
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.find("Vehiculo")
        if vehiculo is not None:
            for attr in vehiculo.attrib:
                attr_name = attr
                attr_value = vehiculo.attrib[attr_name]
                if attr_value == id_vehiculo:
                    return vehiculo[3].text
    return 0


def esta_finalizado(alquiler, id_alquiler):
    if alquiler[4].text is None and alquiler[6].text is None:
        return False
    else:
        return True


def cargar_arbol_xml():
    if not os.path.exists(file_path):
        root = ET.Element('Renting')
        vehiculos = ET.SubElement(root, 'Vehiculos')
        alquileres = ET.SubElement(root, 'Alquileres')
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    else:
        tree = ET.parse(file_path)
        root = tree.getroot()
        vehiculos = root.find('Vehiculos')
        alquileres = root.find('Alquileres')

        if vehiculos is None:
            vehiculos = ET.SubElement(root, 'Vehiculos')
        if alquileres is None:
            alquileres = ET.SubElement(root, 'Alquileres')
        tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    prettify(root)


# Alta
def crear_alquiler(root):
    done = False
    print("Creacion de alquileres")
    while not done:
        id_del_vehiculo = Validador.validar_id()
        if id_del_vehiculo is not None:
            dni_del_cliente = Validador.validar_dni()
        if id_del_vehiculo is not None and dni_del_cliente is not None:
            print("Fecha de inicio:")
            fecha_del_ini = Validador.validar_fecha()
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None:
            print("Fecha de fin:")
            fecha_del_fin = Validador.validar_fecha()
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None:
            km_del_ini = Validador.validar_kilometraje()
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None and km_del_ini is not None:

            alquileres = root.find("Alquileres")
            if alquileres is None:
                print("Fallo al encontrar Alquileres")
                alquileres = ET.SubElement(root, "Alquileres")

            alquiler = ET.SubElement(alquileres, "Alquiler",
                                     idAlquiler=str(obtener_ultimo_id_alquiler(root)))
            id_vehiculo = ET.SubElement(alquiler, "idVehiculo")
            id_vehiculo.text = id_del_vehiculo
            dni_cliente = ET.SubElement(alquiler, "dniCliente")
            dni_cliente.text = dni_del_cliente
            fecha_ini_alq = ET.SubElement(alquiler, "FechaIniAlq")
            fecha_ini_alq.text = str(fecha_del_ini)  # Antes era datetime
            fecha_fin_alq = ET.SubElement(alquiler, "FechaFinAlq")
            fecha_fin_alq.text = str(fecha_del_fin)  # Antes era datetime
            fecha_devo = ET.SubElement(alquiler, "FechaDevolucion")
            km_ini = ET.SubElement(alquiler, "KmInicial")
            km_ini.text = str(km_del_ini)
            km_fin = ET.SubElement(alquiler, "KmGinal")
            precio_final = ET.SubElement(alquiler, "PrecioFinal")
            precio = int(str((fecha_del_fin - fecha_del_ini).days)) * float(
                str(conseguir_precio_por_id(root, id_del_vehiculo)))
            precio_final.text = str(precio) + "€"

            prettify(root)
            ElementTree(root).write(file_path)

            if not Utiles.si_no("Desea dar de alta otro alquiler?"):
                done = True
        else:
            done = True


# Mostrar
def mostrar_arbol(root):
    file = open(file_path, "r")
    lista = file.read()
    file.close()
    print(lista)


def mostrar_todos_alquileres(root):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for alquileres in root:
        for alquiler in alquileres:
            if "Alquiler" == alquiler.tag:
                for attr in alquiler.attrib:
                    print("ID del alquiler: ", attr)
                for i in alquiler:
                    print(i.tag, ": ", i.text)
                print()


def mostrar_por_dni(root):
    esta = False
    dni = Validador.validar_dni()
    for alquileres in root:
        for alquiler in alquileres:
            if "Alquiler" == alquiler.tag:
                if dni == alquiler[1].text:
                    esta = True
                    for attr in alquiler.attrib:
                        print("ID del alquiler: ", attr)
                    for i in alquiler:
                        print(i.tag, ": ", i.text)
                    print()

    if not esta:
        print("El DNI introducido no se correspondia con el de nadie que hubiese realizado un alquiler")


def mostrar_por_matricula(root):
    esta = False
    esta_alq = False
    id_vehiculo = -1
    mat = input("Introduzca la matricula por la que desea buscar un alquiler: ")
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.find("Vehiculo")
        if vehiculo is not None:
            for vehiculo in vehiculos:
                if vehiculo[0].text == mat:
                    esta = True
                    id_vehiculo = vehiculo.get('idVehiculo')
    if esta:
        for alquileres in root:
            for alquiler in alquileres:
                if "Alquiler" == alquiler.tag:
                    if alquiler[0].text == id_vehiculo:
                        esta_alq = True
                    for attr in alquiler.attrib:
                        print("ID del alquiler: ", attr)
                    for i in alquiler:
                        print(i.tag, ": ", i.text)
                    print()
        if not esta_alq:
            print("La matricula introducida con se corresponde con la de ningun alquiler")
    else:
        print("La matricula introducida con se corresponde con la de ningun vehiculo")


# Finalizar
def calcular_recargo(alquiler, fecha_devo):
    fecha = alquiler[3].text
    print(type(fecha))
    fecha = str(fecha)
    fecha_aux = fecha.split("-")
    fecha_formateada = datetime.date(int(fecha_aux[0]), int(fecha_aux[1]), int(fecha_aux[2]))
    print(type(fecha_formateada))
    if fecha_formateada < fecha_devo:
        return True
    else:
        return False


def finalizar(root, alquiler, id_alquiler):
    print("Introduzca la fecha de devolucion del vehiculo")
    fecha_devo = Validador.validar_fecha()
    if fecha_devo is not None:
        km_fin = Validador.validar_kilometraje()
    if fecha_devo is not None and km_fin is not None:
        alquiler[4].text = str(fecha_devo)
        alquiler[6].text = km_fin
        recargo = ET.SubElement(alquiler, "Recargo")
        if calcular_recargo(alquiler, fecha_devo):
            recargo.text = "50€"
        else:
            recargo.text = "Sin recargo"
        prettify(root)
        ElementTree(root).write(file_path)
        print("Alquiler finalizado")
    else:
        print("Volviendo al menu de finalizacion.")


def finalizar_alquiler(root):
    done = False
    esta = False
    alquileres = root.find("Alquileres")
    if alquileres is not None and len(alquileres) > 0:
        while not done:
            print("Devolucion del vehiculo.")
            id_alquiler = Validador.validar_id()
            alquiler = alquileres.findall("Alquiler")
            if alquiler is not None and len(alquiler) > 0:
                for i in alquiler:
                    if id_alquiler == i.attrib["idAlquiler"]:
                        esta = True
                        if not esta_finalizado(i, id_alquiler):
                            finalizar(root, i, id_alquiler)
                        else:
                            print("El alquiler que desea finalizar ya fue finalizado anteriormente.")
                if not esta:
                    print("El id introducido no coincide con el de ningun alquiler")
            else:
                print("No hay alquileres en el sistema")
            if not Utiles.si_no("Quiere tratar de finalizar otro alquiler?"):
                done = True
    else:
        print("No hay alquileres en el sistema")


def modif_alq_sin_fin(root, alquiler):
    elec = "-1"
    while elec != "0":
        print("1. Id Vehiculo\n2. DNI cliente\n3. Fecha de inicio\n4. Fecha de fin\n5. Kilometraje inicial\n0. Salir")
        elec = input("Elija el campo que desea modificar (1/2/3/4/5/0):\n")
        if elec == "1":
            print("Nueva id de vehiculo")
            id_vehiculo = Validador.validar_id()
            if id_vehiculo is not None:
                if Utiles.si_no("Seguro que desea cambiar el id del vehiculo por " + id_vehiculo + "?"):
                    alquiler[0].text = id_vehiculo
                    print("Modificacion del id del vehiculo realizada.")
        elif elec == "2":
            print("Nuevo dni cliente")
            dni_cliente = Validador.validar_dni()
            if dni_cliente is not None:
                if Utiles.si_no("Seguro que desea cambiar el dni del cliente por " + dni_cliente + "?"):
                    alquiler[1].text = dni_cliente
        elif elec == "3":
            print("Nueva fecha de inicio")
            fecha_ini = Validador.validar_fecha()
            if fecha_ini is not None and Utiles.si_no("Seguro que desea cambiar la fecha de inicio por " + str(fecha_ini) + "?"):
                alquiler[2].text = str(fecha_ini)
        elif elec == "4":
            print("Nueva fecha de fin")
            fecha_fin = Validador.validar_fecha()
            if fecha_fin is not None and Utiles.si_no("Seguro que desea cambiar la fecha de fin por " + str(fecha_fin) + "?"):
                alquiler[3].text = str(fecha_fin)
        elif elec == "5":
            print("Nuevo kilometraje inicial")
            km_ini = Validador.validar_kilometraje()
            if km_ini is not None and Utiles.si_no("Seguro que desea cambiar el kilometraje inicial por " + km_ini + "?"):
                alquiler[5].text = str(km_ini)
        elif elec == "0":
            print("Finalizando modificacion")
        prettify(root)
        ElementTree(root).write(file_path)


def modif_alq_fin(root, alquiler):
    elec = "-1"
    while elec != "0":
        print("1. Id Vehiculo\n2. DNI cliente\n3. Fecha de inicio\n4. Fecha de fin\n5. Kilometraje inicial\n6. Kilometraje final\n7. Fecha de devolucion\n8. Recargo0. Salir")
        elec = input("Elija el campo que desea modificar (1/2/3/4/5/6/7/8/0):\n")
        if elec == "1":
            print("Nueva id de vehiculo")
            id_vehiculo = Validador.validar_id()
            if id_vehiculo is not None:
                if Utiles.si_no("Seguro que desea cambiar el id del vehiculo por " + id_vehiculo + "?"):
                    alquiler[0].text = id_vehiculo
                    print("Modificacion del id del vehiculo realizada.")
        elif elec == "2":
            print("Nuevo dni cliente")
            dni_cliente = Validador.validar_dni()
            if dni_cliente is not None:
                if Utiles.si_no("Seguro que desea cambiar el dni del cliente por " + dni_cliente + "?"):
                    alquiler[1].text = dni_cliente
        elif elec == "3":
            print("Nueva fecha de inicio")
            fecha_ini = Validador.validar_fecha()
            if fecha_ini is not None and Utiles.si_no("Seguro que desea cambiar la fecha de inicio por " + str(fecha_ini) + "?"):
                alquiler[2].text = str(fecha_ini)
        elif elec == "4":
            print("Nueva fecha de fin")
            fecha_fin = Validador.validar_fecha()
            if fecha_fin is not None and Utiles.si_no("Seguro que desea cambiar la fecha de fin por " + str(fecha_fin) + "?"):
                alquiler[3].text = str(fecha_fin)
        elif elec == "5":
            print("Nuevo kilometraje inicial")
            km_ini = Validador.validar_kilometraje()
            if km_ini is not None and Utiles.si_no("Seguro que desea cambiar el kilometraje inicial por " + km_ini + "?"):
                alquiler[5].text = km_ini
        elif elec == "6":
            print("Nuevo kilometraje final")
            km_fin = Validador.validar_kilometraje()
            if km_fin is not None and Utiles.si_no("Seguro que desea cambiar el kilometraje final por " + km_fin + "?"):
                alquiler[6].text = km_fin
        elif elec == "7":
            print("Nueva fecha de devolucion")
            fecha_devo = Validador.validar_fecha()
            if fecha_devo is not None and Utiles.si_no("Seguro que desea cambiar la fecha de devolucion por " + str(fecha_devo) + "?"):
                alquiler[4].text = str(fecha_devo)
        elif elec == "8":
            print("Nuevo recargo")
            recargo = Validador.validar_kilometraje()
            if recargo is not None and Utiles.si_no("Seguro que desea cambiar el recargo por " + recargo + "?"):
                alquiler[8].text = recargo+"€"
        elif elec == "0":
            print("Finalizando modificacion")
        prettify(root)
        ElementTree(root).write(file_path)


def modificar_alquiler(root):
    done = False
    esta = False
    alquileres = root.find("Alquileres")
    print(len(alquileres))
    print(type(alquileres))
    if alquileres is not None and len(alquileres) > 0:
        while not done:
            print("Modificacion de vehiculos")
            id_alquiler = Validador.validar_id()
            alquiler = alquileres.findall("Alquiler")
            if alquiler is not None and len(alquiler) > 0:
                for i in alquiler:
                    if id_alquiler == i.attrib["idAlquiler"]:
                        esta = True
                        if not esta_finalizado(i, id_alquiler):
                            modif_alq_sin_fin(root, i)
                            print("Modificacion realizada")
                        else:
                            modif_alq_fin(root, i)
                            print("Modificacion realizada")

            if not esta and alquiler is not None and len(alquiler) > 0:
                print("El id introducido no coincide con el de ningun alquiler")
            else:
                print("No hay alquileres en el sistema")

            if not Utiles.si_no("Quiere tratar de modifucar otro alquiler?"):
                done = True
    else:
        print("No hay alquileres en el sistema")


def menu_alquiler(root):
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
            crear_alquiler(root)
        elif choice == "2":
            menu_busqueda(root)
        elif choice == "3":
            modificar_alquiler(root)
        elif choice == "4":
            finalizar_alquiler(root)
        elif choice == "0":
            print("Saliendo del menu de alquileres")
        else:
            print("Opcion no valida.")


def menu_busqueda(root):
    choice = ""
    while choice != "0":
        print("\nMenu de Alquileres:")
        print("1. Mostrar todos los alquileres")
        print("2. Buscar todos los alquileres de una matricula")
        print("3. Buscar todos los alquileres de un cliente (DNI)")
        print("0. Volver al menu de alquileres")

        choice = input("Selecciona una opcion (1/2/3/0): ")
        if choice == "1":
            mostrar_todos_alquileres(root)
        elif choice == "2":
            mostrar_por_matricula(root)
        elif choice == "3":
            mostrar_por_dni(root)
        elif choice == "0":
            print("Saliendo del menu de busqueda.")
        else:
            print("Opcion no valida.")
