import xml.etree.ElementTree as ET
import os

file_path = ".\\datos.xml"


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
    return tree


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


def obtener_ultimo_id():
    tree = ET.parse(file_path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')
    ultimos_vehiculos = vehiculos.findall('Vehiculo[@idVehiculo]')

    if ultimos_vehiculos:
        ultimo_id = max(int(vehiculo.get('idVehiculo')) for vehiculo in ultimos_vehiculos)
        return ultimo_id + 1
    else:
        return 1


def crear_vehiculo(vehiculo):
    tree = ET.parse(file_path)
    root = tree.getroot()

    id = obtener_ultimo_id()

    coche = ET.Element('Vehiculo', {'idVehiculo': str(id)})

    for key, value in vehiculo.items():
        if key != 'idVehiculo':
            sub_element = ET.Element(key)
            sub_element.text = str(value)
            coche.append(sub_element)

    vehiculos = root.find('Vehiculos')
    vehiculos.append(coche)

    prettify(root)

    tree.write(file_path)


def mostrar_todos():
    tree = ET.parse(file_path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')

    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo'):
            print("\nID de VehÃ­culo:", vehiculo.get('idVehiculo'))
            for element in vehiculo:
                print(f"{element.tag}: {element.text}")


'''
vehicle_data = {
    'Matricula': 'ABC665',
    'MarcaModelo': 'Honda Civic',
    'AnnoFabricacion': '2006',
    'TarifaDia': '250.00',
    'Estado': 'Disponible'
}
cargar_arbol_xml()
crear_vehiculo(vehicle_data)
mostrar_todos()
'''
