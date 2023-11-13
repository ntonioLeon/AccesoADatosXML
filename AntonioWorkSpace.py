# from xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import os
import Validador

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


def obtener_ultimo_id_Alquiler():
    tree = ET.parse(file_path)
    root = tree.getroot()

    alquileres = root.find('Alquileres')
    ultimos_alquileres = alquileres.findall('alquiler[@idAlquiler]')

    if ultimos_alquileres:
        ultimo_id = max(int(alquiler.get('idAlquiler')) for alquiler in ultimos_alquileres)
        return ultimo_id + 1
    else:
        return 1


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


def crear_alquiler():
    tree = ET.parse(file_path)
    root = tree.getroot()

    idVehiculo = Validador.validar_id()
    if idVehiculo != None:
        dniCliente = Validador.validar_dni()
    if idVehiculo != None and dniCliente != None:
        print("Fecha de inicio:")
        fechaIni = Validador.validar_fecha()
    if idVehiculo != None and dniCliente != None and fechaIni != None:
        print("Fecha de fin:")
        fechaFin = Validador.validar_fecha()
    if idVehiculo != None and dniCliente != None and fechaIni != None and fechaFin != None:
        kmIni = Validador.validar_kilometraje()
    if idVehiculo != None and dniCliente != None and fechaIni != None and fechaFin != None and kmIni != None:
        try:
            alquileres = root.find("Alquileres")
        except:
            print("Fallo al encontrar Alquileres")

        alquiler = ET.SubElement(alquileres, "Alquiler",
                                 idAlquiler=str(obtener_ultimo_id_Alquiler()))  # Este ID es un place holder hasta encontrar/hacer un metodo que asigne IDs

        id_vehiculo = ET.SubElement(alquiler, "idVehiculo")
        id_vehiculo.text = idVehiculo
        dni_cliente = ET.SubElement(alquiler, "dniCliente")
        dni_cliente.text = dniCliente
        fecha_ini_alq = ET.SubElement(alquiler, "FechaIniAlq")
        fecha_ini_alq.text = str(fechaIni) #Antes era datetime
        fecha_fin_alq = ET.SubElement(alquiler, "FechaFinAlq")
        fecha_fin_alq.text = str(fechaFin) #Antes era datetime
        km_ini = ET.SubElement(alquiler, "KmInicial")
        km_ini.text = kmIni

        prettify(root)
        tree.write(file_path)

cargar_arbol_xml()
tree = ET.parse(file_path)
root = tree.getroot()
