import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import os
import Validador
import Utiles

file_path = ".\\datos.xml"


def prettify(elem, level=0):
    """
    funcion que reescribe el xml para que no este en una linea y tenga una estructura valida.
    @:param elem, el elemento que va a ser reestructurado.
    """
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


def esta_dispinible(root, id_vehiculo):
    """
    funcion que comprueba si un alquiler esta finalizado o no.
    :param root: que se recorrera
    :param id_vehiculo: El que se va a comprobar
    :return: trye si esta disponible false si no
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")  # Nos situamos en vehiculo en el arbol.
        if vehiculo is not None:  # si hay vehiculos
            for vehi in vehiculo:
                for attr in vehi.attrib:  # Recorremos los atributos de los vehiculos.
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:  # si coincide con el parametro es decir lo encontramos.
                        if vehi[4].text == "Disponible":
                            return True
                        else:
                            return False


def obtener_ultimo_id_alquiler(root):
    """
    funcion que recorre los alquileres para saber cual es el siguiente id valido.
    @:param root, que sera recorrido en busca de alquileres.
    @:return 1 si no hay alquileres, el ultimo id + 1 si hay alquileres.
    """
    alquileres = root.find('Alquileres')  # Encuentra los alquileres.
    ultimos_alquileres = alquileres.findall('Alquiler[@idAlquiler]')  # lista con los ids de los alquileres.

    if ultimos_alquileres:  # Si hay ids de alquiler
        ultimo_id = max(
            int(alquiler.get('idAlquiler')) for alquiler in ultimos_alquileres)  # Recorremos la lista de ids.
        return ultimo_id + 1  # devolvemos el ultimo + 1.
    else:
        return 1  # Si no hay ids el id sera 1.


def obtener_matricula_por_id(root, id_vehiculo):
    """
    Funcion que devuelve una matricula a partir de un id
    :param root: que se recorre
    :param id_vehiculo: que se busca
    :return: la matricula
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is None:
        return
    lista_vehiculo = vehiculos.findall("Vehiculo")
    if lista_vehiculo is not None:
        for vehiculo in lista_vehiculo:
            if vehiculo.attrib["idVehiculo"] == id_vehiculo:
                return vehiculo[0].text


def conseguir_precio_por_id(root, id_vehiculo):
    """
    funcion que a partir de un id devuelve el precio del vehiculo.
    @:param root que sera recorrida y id del vehiculo que queremos encontrar.
    @:return el precio del vehiculo, como los id se validan no puede no encontrar un precio.
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")  # Nos situamos en vehiculo en el arbol.
        if vehiculo is not None:  # si hay vehiculos
            for vehi in vehiculo:
                for attr in vehi.attrib:  # Recorremos los atributos de los vehiculos.
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:  # si coincide con el parametro es decir lo encontramos.
                        return vehi[3].text  # devolvemos el precio.


def cambiarDisponibilidad(root, id_vehiculo, estado):
    """
    funcion que re escribre el estado de los coches una vez son alquilados
    @:param root se recorre, id_vehiculo identifica, estado marca la accion a realizar
    """
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.findall("Vehiculo")
        if vehiculo is not None:
            for vehi in vehiculo:
                for attr in vehi.attrib:
                    attr_name = attr
                    attr_value = vehi.attrib[attr_name]
                    if attr_value == id_vehiculo:
                        if str(estado) == "Alquilado":  # Me encantaria saber por que si no casteo el estado falla...
                            vehi[4].text = "Alquilado"
                        elif str(estado) == "Disponible":
                            vehi[4].text = "Disponible"


def esta_finalizado(alquiler, id_alquiler):
    """
    funcion que comprueba que un alquiler esta finalizado por medio de comprobar los campos que solo se rellenan en la finalizacion
    @:param alquiler el alquiler que se comprueba.
    """
    if alquiler[4].text is None and alquiler[6].text is None:
        return False
    else:
        return True


def cargar_arbol_xml():
    """
    funcion que crea el arbol si no exsite con 'Renting'. 'Vehiculos' y 'Alquileres'
    """
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
    """
    funcion que pide campos, si todos son validos procede a situarse en alquileres y crear los correspondientes subelementos.
    @:param root, para ser recorrido y trabajado
    """
    done = False
    print("Creacion de alquileres")
    while not done:  # Bucle que servira para realizar mas de un alquiler
        id_del_vehiculo = Validador.validar_id(root,
                                               "1")  # En estas lineas nos apoyaremos en los funcions de Validador para conseguir campos correctos
        if not esta_dispinible(root, id_del_vehiculo):
            print("El vehiculo no esta disponible para ser alquilado")
            id_del_vehiculo = None
        if id_del_vehiculo is not None:
            dni_del_cliente = Validador.validar_dni()
        if id_del_vehiculo is not None and dni_del_cliente is not None:
            print("Fecha de inicio:")
            fecha_del_ini = Validador.validar_fecha()
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None:
            print("Fecha de fin:")
            fecha_del_fin = Validador.validar_fecha(fecha_del_ini)
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None:
            km_del_ini = Validador.validar_kilometraje()
        if id_del_vehiculo is not None and dni_del_cliente is not None and fecha_del_ini is not None and fecha_del_fin is not None and km_del_ini is not None:
            # Si todos los campos estan correctos procedemos a crear el subelemento

            alquileres = root.find("Alquileres")  # Nos situamos en alquileres
            if alquileres is None:  # Si no exsie los creamos
                print("Fallo al encontrar Alquileres")
                alquileres = ET.SubElement(root, "Alquileres")

            alquiler = ET.SubElement(alquileres, "Alquiler",  # Creamos el alquiler con el id como atributo
                                     idAlquiler=str(obtener_ultimo_id_alquiler(
                                         root)))  # Obtenemos el id por medio delfuncion que recorre los alquileres

            # Vamos creando los subelementos uno a uno y confiriendoles valores.
            id_vehiculo = ET.SubElement(alquiler, "idVehiculo", {'Matricula': obtener_matricula_por_id(root,
                                                                                                       id_del_vehiculo)})  # En el caso de idVheiculo le pondremos como atributo la matricula
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
            km_fin = ET.SubElement(alquiler, "KmFinal")
            precio_final = ET.SubElement(alquiler, "PrecioFinal")
            '''Linea que calcula el precio*dias por medio de restar fechas, pasarlas a dias, convertirlas a string porque 
            castear de date a int explota y concluye multiplicando los dias por el precio/dia del vehiculo.'''
            precio = int(str((fecha_del_fin - fecha_del_ini).days)) * float(
                conseguir_precio_por_id(root, id_del_vehiculo))
            precio_final.text = str(precio)
            cambiarDisponibilidad(root, id_del_vehiculo, "Alquilado")  # Cambiamos el estado del vehuiculo

            prettify(root)  # Re hacemos la estructura del xml
            ElementTree(root).write(file_path)  # Escribimos el archivo

            if not Utiles.si_no(
                    "Desea dar de alta otro alquiler?"):  # Preguntamos si quiere hacer otro y en caso de que no salimos
                done = True
        else:  # Si se falla en los campos te saca del menu.
            done = True


# Mostrar
def mostrar_todos_alquileres(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres
    @:param root
    """
    for alquileres in root:
        for alquiler in alquileres:
            if "Alquiler" == alquiler.tag:
                for attr in alquiler.attrib:
                    print("ID del alquiler: ", alquiler.attrib[attr])
                for i in alquiler:
                    print(i.tag, ": ", i.text)
                print()


def mostrar_por_dni(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres que correspondan a un dni
    @:param root
    """
    esta = False
    dni = Validador.validar_dni()
    for alquileres in root:
        for alquiler in alquileres:
            if "Alquiler" == alquiler.tag:
                if dni == alquiler[1].text:
                    esta = True
                    for attr in alquiler.attrib:
                        print("ID del alquiler: ", alquiler.attrib[attr])
                    for i in alquiler:
                        print(i.tag, ": ", i.text)
                    print()

    if not esta:
        print("El DNI introducido no se correspondia con el de nadie que hubiese realizado un alquiler")


def mostrar_por_matricula(root):
    """
    funcion que recorre el arbol desde la raiz y printea los alquileres que correspondan a una matricula
    @:param root
    """
    esta = False
    esta_alq = False
    id_vehiculo = -1
    mat = input("Introduzca la matricula por la que desea buscar un alquiler: ")
    '''vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.find("Vehiculo")
        if vehiculo is not None:
            for vehiculo in vehiculos:
                if vehiculo[0].text == mat:
                    esta = True
                    id_vehiculo = vehiculo.get('idVehiculo')
    if esta:'''
    for alquileres in root:
        for alquiler in alquileres:
            if "Alquiler" == alquiler.tag:
                print(alquiler[0].attrib["Matricula"])
                if alquiler[0].attrib["Matricula"] == mat:
                    esta_alq = True
                    for attr in alquiler.attrib:
                        print("ID del alquiler: ", alquiler.attrib[attr])
                    for i in alquiler:
                        if i.tag == "idVehiculo":
                            print("Matricula", ": ", i.attrib["Matricula"])
                        else:
                            print(i.tag, ": ", i.text)
                print()
    if not esta_alq:
        print("La matricula introducida con se corresponde con la de ningun alquiler")
    else:
        print("La matricula introducida con se corresponde con la de ningun vehiculo")


# Finalizar
def calcular_recargo(alquiler, fecha_devo):
    """
    funcion que comprueba si la fecha de devolucion sobrepasa la del final del alquiler
    @:param alquiler que se va a finalizar la fecha de devolucion
    @:return true si la fecha fin es menor que la de devolucion
    """
    fecha = alquiler[3].text  # Obtenemos la fecha final
    fecha = str(fecha)
    fecha_aux = fecha.split("-")  # Sacamos una lista con los datos
    fecha_formateada = datetime.date(int(fecha_aux[0]), int(fecha_aux[1]),
                                     int(fecha_aux[2]))  # Reconstruimos la fecha final
    if fecha_formateada < fecha_devo:  # Comprobamos cual es mayor
        return True
    else:
        return False


def finalizar(root, alquiler, id_alquiler):
    """
    funcion que finaliza los campos de un alquiler.
    @:param root que se escribira alquiler que se actualizara
    """
    print("Introduzca la fecha de devolucion del vehiculo")
    campos = str(alquiler[2].text).split("-")  # Obtenemos la fecha inicial
    fecha_ini = datetime.date(int(campos[0]), int(campos[1]), int(campos[2]))  # Reconstruimos la fecha inicial
    fecha_devo = Validador.validar_fecha(fecha_ini)  # pedimos la fecha de devolucion
    if fecha_devo is not None:  # comprobamos que los campos son validos
        km_fin = Validador.validar_kilometraje(alquiler[5].text)  # Pedimos kmfinal
    if fecha_devo is not None and km_fin is not None:  # Si los campos son correctos damos el alquiler por finalizado

        alquiler[4].text = str(fecha_devo)
        alquiler[6].text = km_fin  # Escribimos los campos
        recargo = ET.SubElement(alquiler, "Recargo")  # Creamos el campo recargo
        if calcular_recargo(alquiler, fecha_devo):  # Comprobamos si merece recargo o no y lo aplicamos si es necesario
            campos_fin = str(alquiler[3].text).split("-")
            fecha_fin = datetime.date(int(campos_fin[0]), int(campos_fin[1]), int(campos_fin[2]))
            precio = conseguir_precio_por_id(root, alquiler[0].text)
            recargo.text = str(int(str((fecha_devo - fecha_fin).days)) * (float(precio) + 30))
        else:
            recargo.text = "Sin recargo"
        cambiarDisponibilidad(root, alquiler[0].text, "Disponible")  # Cambiamos el estado del vehuiculo

        prettify(root)
        ElementTree(root).write(file_path)  # Re escribimos el xml
        print("Alquiler finalizado")
    else:
        print("Volviendo al menu de finalizacion.")


def finalizar_alquiler(root):
    """
    funcion que pide un id de alquiler y si no esta finalizado lo finaliza.
    @:param root que se recorrera
    """
    done = False
    esta = False
    alquileres = root.find("Alquileres")  # Encontramos los alquileres
    if alquileres is not None and len(alquileres) > 0:
        while not done:  # Para finalizar mas de uno si se quiere
            print("Devolucion del vehiculo.")
            id_alquiler = Validador.validar_id(root, "2")  # Se pide el id
            alquiler = alquileres.findall("Alquiler")
            if alquiler is not None and len(alquiler) > 0:  # consequimos una lista de alquileres
                for i in alquiler:  # Recorremos los alquileres
                    if id_alquiler == i.attrib["idAlquiler"]:  # Si el id se corresponde con el que buscamos
                        esta = True  # Marcamos true para que luego no salte lo de que no se encontro
                        if not esta_finalizado(i, id_alquiler):  # Comprobamos si ya esta finalizado
                            finalizar(root, i, id_alquiler)  # Si no lo esta lo mandamos finalizar.
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
    """
    funcion que modifica los campos de un alquiler si este no esta finalizado.
    @:param root que se reescribira y alquiler que se modificara
    """
    elec = ""
    while elec != "0":
        print(
            "1. Id Vehiculo\n2. DNI cliente\n3. Fecha de inicio\n4. Fecha de fin\n5. Kilometraje inicial\n0. Salir")  # Elecciones
        elec = input("Elija el campo que desea modificar (1/2/3/4/5/0):\n")
        if elec == "1":  # Echo de menos en swich.
            print("Nueva id de vehiculo")
            id_vehiculo = Validador.validar_id(root,
                                               "2")  # Pedimos el nuevo campo, comprobamos que es valido y lo sustituimos, es asi en todos.
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
            if fecha_ini is not None and Utiles.si_no(
                    "Seguro que desea cambiar la fecha de inicio por " + str(fecha_ini) + "?"):
                alquiler[2].text = str(fecha_ini)
        elif elec == "4":
            print("Nueva fecha de fin")
            fecha_fin = Validador.validar_fecha()
            if fecha_fin is not None and Utiles.si_no(
                    "Seguro que desea cambiar la fecha de fin por " + str(fecha_fin) + "?"):
                alquiler[3].text = str(fecha_fin)
        elif elec == "5":
            print("Nuevo kilometraje inicial")
            km_ini = Validador.validar_kilometraje()
            if km_ini is not None and Utiles.si_no(
                    "Seguro que desea cambiar el kilometraje inicial por " + km_ini + "?"):
                alquiler[5].text = str(km_ini)
        elif elec == "0":
            print("Finalizando modificacion")
        prettify(root)
        ElementTree(root).write(file_path)  # resescribimos el fichero


def modif_alq_fin(root, alquiler):
    """
    funcion que modifica los campos de un alquiler si este si esta finalizado. Es como el anterior pero con mas posibilidades.
    @:param root que se reescribira y alquiler que se modificara
    """
    elec = "-1"
    while elec != "0":
        print(
            "1. Id Vehiculo\n2. DNI cliente\n3. Fecha de inicio\n4. Fecha de fin\n5. Kilometraje inicial\n6. Kilometraje final\n7. Fecha de devolucion\n8. Recargo0. Salir")
        elec = input("Elija el campo que desea modificar (1/2/3/4/5/6/7/8/0):\n")
        if elec == "1":
            print("Nueva id de vehiculo")
            id_vehiculo = Validador.validar_id(root, "2")
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
            if fecha_ini is not None and Utiles.si_no(
                    "Seguro que desea cambiar la fecha de inicio por " + str(fecha_ini) + "?"):
                alquiler[2].text = str(fecha_ini)
        elif elec == "4":
            print("Nueva fecha de fin")
            fecha_fin = Validador.validar_fecha()
            if fecha_fin is not None and Utiles.si_no(
                    "Seguro que desea cambiar la fecha de fin por " + str(fecha_fin) + "?"):
                alquiler[3].text = str(fecha_fin)
        elif elec == "5":
            print("Nuevo kilometraje inicial")
            km_ini = Validador.validar_kilometraje()
            if km_ini is not None and Utiles.si_no(
                    "Seguro que desea cambiar el kilometraje inicial por " + km_ini + "?"):
                alquiler[5].text = km_ini
        elif elec == "6":
            print("Nuevo kilometraje final")
            km_fin = Validador.validar_kilometraje()
            if km_fin is not None and Utiles.si_no("Seguro que desea cambiar el kilometraje final por " + km_fin + "?"):
                alquiler[6].text = km_fin
        elif elec == "7":
            print("Nueva fecha de devolucion")
            fecha_devo = Validador.validar_fecha()
            if fecha_devo is not None and Utiles.si_no(
                    "Seguro que desea cambiar la fecha de devolucion por " + str(fecha_devo) + "?"):
                alquiler[4].text = str(fecha_devo)
        elif elec == "8":
            print("Nuevo recargo")
            recargo = Validador.validar_kilometraje()
            if recargo is not None and Utiles.si_no("Seguro que desea cambiar el recargo por " + recargo + "?"):
                alquiler[8].text = recargo
        elif elec == "0":
            print("Finalizando modificacion")
        prettify(root)
        ElementTree(root).write(file_path)  # resescribimos el fichero


def modificar_alquiler(root):
    """
    funcion que busca un alquiler y se manda a modificar.
    @:param root que se recorrera en busca del alquiler a modificar.
    """
    done = False
    esta = False
    alquileres = root.find("Alquileres")
    if alquileres is not None and len(alquileres) > 0:  # Si hay alquileres
        while not done:  # Bucle para modificar mas de uno si se quiere
            print("Modificacion de vehiculos")
            id_alquiler = Validador.validar_id(root, "2")  # Pelidmos id
            alquiler = alquileres.findall("Alquiler")
            if alquiler is not None and len(alquiler) > 0:  # Si hay alquiler
                for i in alquiler:
                    if id_alquiler == i.attrib["idAlquiler"]:  # Si coincide procede a comprobar si esta finalizado y mandarlo al modif correspondiente
                        esta = True
                        if not esta_finalizado(i, id_alquiler):
                            modif_alq_sin_fin(root, i)
                            print("Modificacion realizada")
                        else:
                            modif_alq_fin(root, i)
                            print("Modificacion realizada")

            if not esta and alquiler is not None and len(alquiler) > 0:
                print(
                    "El id introducido no coincide con el de ningun alquiler")  # Por si metemos un id que no encuentra
            else:
                print("No hay alquileres en el sistema")
            if not Utiles.si_no("Quiere tratar de modifucar otro alquiler?"):
                done = True
    else:
        print("No hay alquileres en el sistema")


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
            mostrar_todos_alquileres(root)
        elif choice == "2":
            mostrar_por_matricula(root)
        elif choice == "3":
            mostrar_por_dni(root)
        elif choice == "0":
            print("Saliendo del menu de busqueda.")
        else:
            print("Opcion no valida.")
