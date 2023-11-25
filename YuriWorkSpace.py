import xml.etree.ElementTree as ET
from datetime import datetime
import os
import random
import string
import Menus
import Validador


path = ".\\datos.xml"


def cargar_arbol_xml():
    if not os.path.exists(path):
        root = ET.Element('Renting')
        vehiculos = ET.SubElement(root, 'Vehiculos')
        alquileres = ET.SubElement(root, 'Alquileres')
        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    else:
        tree = ET.parse(path)
        root = tree.getroot()
        vehiculos = root.find('Vehiculos')
        alquileres = root.find('Alquileres')

        if vehiculos is None:
            vehiculos = ET.SubElement(root, 'Vehiculos')
        if alquileres is None:
            alquileres = ET.SubElement(root, 'Alquileres')
        tree.write(path, encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=False)
    prettify(root)
    return root


def prettify(elem, level=0):
    indent = "    "  # 4 espacios por nivel
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        for subelem in elem:
            prettify(subelem, level + 1)
            if not subelem.tail or not subelem.tail.strip():
                subelem.tail = i + indent
        if not elem[-1].tail or not elem[-1].tail.strip():
            elem[-1].tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def obtener_ultimo_id():
    tree = ET.parse(path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')
    ultimos_vehiculos = vehiculos.findall('Vehiculo[@idVehiculo]')

    if ultimos_vehiculos:
        ultimo_id = max(int(vehiculo.get('idVehiculo')) for vehiculo in ultimos_vehiculos)
        return ultimo_id + 1
    else:
        return 1


def crear_vehiculo(vehiculo, root):
    tree = ET.ElementTree(root)
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

    tree.write(path)


def mostrar_todos():
    tree = ET.parse(path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')

    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo'):
            print("\nID de Vehículo:", vehiculo.get('idVehiculo'))
            for element in vehiculo:
                print(f"{element.tag}: {element.text}")


def buscar_vehiculo(matricula):
    tree = ET.parse(path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')

    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo'):
            if vehiculo.find('Matricula').text == matricula:
                print("\nID de Vehículo:", vehiculo.get('idVehiculo'))
                for element in vehiculo:
                    print(
                        f"{element.tag}: {element.text}")  # f es como el printf en java es mas felxible para imprimir expresiones
                return True
    print(f"No se encontró ningún vehículo con la matrícula: {matricula}")
    return False


def obtener_id_por_matricula(matricula):
    tree = ET.parse(path)
    root = tree.getroot()

    vehiculos = root.find('Vehiculos')
    if vehiculos is not None:
        for vehiculo in vehiculos.findall('Vehiculo[Matricula="{0}"]'.format(matricula)):
            return vehiculo.get('idVehiculo')

    return None


def verificar_matricula(cadena):
    if len(cadena) == 6:
        letras = cadena[:3]
        numeros = cadena[3:]
        if letras.isalpha() and numeros.isdigit():
            return True
        else:
            return False
    else:
        return False


def matricula_en_uso(matricula, root):
    try:
        tree = ET.ElementTree(root)
        vehiculos = tree.find('.//Vehiculos')
        if vehiculos is not None:
            for vehiculo in vehiculos.findall('.//Vehiculo/Matricula'):
                if vehiculo.text == matricula:
                    return True
        return False
    except Exception as e:
        print(f"Error al verificar matrícula: {e}")
        return False


def entrada_teclado(campo):
    contador = 0
    while True:
        entrada = input("Introduce una  " + campo + ": ")
        if entrada.strip():
            return entrada
        else:
            print("Por favor, no ingresa una cadena vacía.")
            contador += 1
            if contador == 3:
                return None


def fails(fallos, modificacion):
    fallos += 1
    print(str(fallos) + "/3 fallos hasta salir del " + modificacion)
    return fallos


def isdecima(num):
    try:
        numero = int(num)
        if 50 <= numero <= 250:
            return str(numero) + ".00"
    except ValueError:
        try:
            numero = float(num)
            if 50 <= numero <= 250:
                return round(numero, 2)
        except ValueError:
            return None


def alta_datos(root):
    renuncia = False
    fallos = 0
    while not renuncia:
        print("ALTA NUEVO VEHICULO")
        exito = False

        while not exito:
            matricula = input("Introduzca una matricula valida, recuerde el formato valido de matricula es AAA000.")
            if matricula is not None and not matricula_en_uso(matricula, root) and verificar_matricula(matricula):
                print("**Matricula introducida con exito")
                exito = True
            elif matricula is None:
                print("Es una cadena vacia")
                fallos = fails(fallos, "Alta")
            elif not verificar_matricula(matricula):
                print("El formato de la matricula no es correcto")
                fallos = fails(fallos, "Alta")
            elif matricula_en_uso(matricula, root):
                print("La matricula ya esta en uso")
                fallos = fails(fallos, "Alta")

            if fallos == 3:
                print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                exito = True
                renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                marca = input("Introduzca una marca valida.").split()
                if marca is not None:
                    print("**Marca introducida con exito")
                    exito = True
                elif marca is None:
                    print("Es una cadena vacia.")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                modelo = input("Introduzca un modelo valido.").split()
                if modelo is not None:
                    print("**Modelo introducida con exito.")
                    exito = True
                elif modelo is None:
                    print("Es una cadena vacia.")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                anno = input(
                    "Introduzca una fecha de fabricacion valida. Recuerde nuestros modelos abarcan entre 1970 y 2023")
                if anno is not None:
                    if anno.isnumeric():
                        anno = int(anno)
                        if 1970 <= anno <= 2023:
                            print("**Fecha de fabricacion introducida con exito")
                            exito = True
                        else:
                            print("No ha introducido una fecha valida.")
                            fallos = fails(fallos, "Alta")
                    else:
                        print("No ha introducido una fecha.")
                        fallos = fails(fallos, "Alta")
                elif anno is None:
                    print("Es una cadena vacia")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                tarifa = input("Introduzca una tarifa. Recuerde nuestros modelos abarcan entre 50 y 250€ al dia")
                tarifa = isdecima(tarifa)
                if tarifa is not None:
                    print("**Tarifa introducida con exito")
                    exito = True
                else:
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("Ha alcanzado el máximo de intentos. Saliendo del proceso de alta.")
                    exito = True
                    renuncia = True

        if fallos < 3:
            retorno = False
            fallos = 0
            vehicle = {'Matricula': matricula, 'MarcaModelo': marca, 'AnnoFabricacion': anno, 'TarifaDia': tarifa,
                       'Estado': 'Disponible'}
            print(vehicle)
            if Validador.si_no("Desea agregar un nuevo vehiculo con estas caracteristicas?"):
                crear_vehiculo(vehicle, root)
                print("** Nuevo vehiculo agregado")
                retorno = True
            else:
                print("Alta cancelada")
                retorno = True
            if retorno:
                if Validador.si_no("Desea volver a agregar un nuevo vehiculo?"):
                    print("Volviendo al menu principal")
                    retono = False
                else:
                    print("Volviendo al menu principal")
                    renuncia = True


def eliminar_vehiculo(root, id_vehiculo):
    """

    :param root:
    :param id_vehiculo:
    :return:
    """
    try:
        vehiculo_a_eliminar = None

        # Buscar el vehículo con el ID dado
        for vehiculo in root.findall(".//Vehiculo"):
            if vehiculo.get("idVehiculo") == str(id_vehiculo):
                vehiculo_a_eliminar = vehiculo
                break

        if vehiculo_a_eliminar is not None:
            # Eliminar el vehículo del árbol
            root.find('.//Vehiculos').remove(vehiculo_a_eliminar)
            print(f"Vehículo con ID {id_vehiculo} eliminado correctamente.")
        else:
            print(f"Vehículo con ID {id_vehiculo} no encontrado.")

        prettify(root)

        # No es necesario crear un nuevo ElementTree, usa el mismo árbol
        tree = ET.ElementTree(root)
        tree.write(path)
    except Exception as e:
        print(f"Error al procesar el XML: {e}")


def modificar_vehiculo(root, matricula, datos):
    """
    Modifica un vehiculo exsistente en el XML

    :param root: Elemento raiz del arbol XML
    :param matricula: Matricula del vehiculo susceptible del cambio, no comprueba si existe
    :param datos: Diccionario con los nuevos datos del vehiculo, los modificados y los no modificados
    :return: None
    """
    try:
        for vehiculo in root.findall(".//Vehiculo[Matricula='" + matricula + "']"):
            for key, value in datos.items():
                # Verificar si el elemento ya existe
                elemento = vehiculo.find(key)
                if elemento is not None:
                    # Actualizar el valor existente
                    elemento.text = str(value)
                else:
                    # Crear un nuevo elemento si no existe
                    nuevo = ET.Element(key)
                    nuevo.text = str(value)
                    vehiculo.append(nuevo)

        prettify(root)
        tree = ET.ElementTree(root)
        tree.write(path)
        print(f"Vehículo con matrícula {matricula} modificado correctamente.")
    except Exception as e:
        print(f"Error al procesar el XML: {e}")


vehicle_data = {
    'Matricula': 'ABC123',
    'MarcaModelo': 'Esto es un test3',
    'AnnoFabricacion': '1979',
    'TarifaDia': '50.00',
    'Estado': 'Disponible'
}
vehicle_data2 = {
    'Matricula': 'ABC667',
    'MarcaModelo': 'Honda Civic',
    'AnnoFabricacion': '2004',
    'TarifaDia': '150.00',
    'Estado': 'Disponible'
}

root = cargar_arbol_xml()
tree = ET.ElementTree(root)
# alta_datos(root)
eliminar_vehiculo(root, obtener_id_por_matricula("SHN034"))
modificar_vehiculo(root, "ABC665", vehicle_data)
"""
if(vehi is not None):
    
    buscar_vehiculo(vehi['Matricula'])
    print(obtener_id_por_matricula(vehi['Matricula']))
"""
# mostrar_todos()
print("----------" * 20)

print("----------" * 20)
"""
def generar_coche(root):
    tree = ET.ElementTree(root)
    matricula = None
    marca = None
    fin = False
    while not fin:
        matricula = ''.join(random.choice(string.ascii_uppercase) for letras in range(3)) + ''.join(
            random.choice(string.digits) for numeros in range(3))
        if not matricula_en_uso(matricula, tree):
            fin = True

    aleatorio = random.randint(0, 10)
    if (aleatorio == 0):
        marca = "Mitsubishi"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Pajero"
        elif (modelo == 1):
            marca += " EVO Lancer 7"
        elif (modelo == 2):
            marca += " Eclipse"
        elif (modelo == 3):
            marca += " Outlander"
        elif (modelo == 4):
            marca += " ASX"
        elif (modelo == 5):
            marca += " EVO Lancer X"
    elif (aleatorio == 1):
        marca = "Toyota"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Prius"
        elif (modelo == 1):
            marca += " Corolla"
        elif (modelo == 2):
            marca += " AE86"
        elif (modelo == 3):
            marca += " LEVI"
        elif (modelo == 4):
            marca += " RAV4"
        elif (modelo == 5):
            marca += " Tacoma"
    elif (aleatorio == 2):
        marca = "Honda"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Civic"
        elif (modelo == 1):
            marca += " CR-V"
        elif (modelo == 2):
            marca += " Odyssey"
        elif (modelo == 3):
            marca += " Pilot"
        elif (modelo == 4):
            marca += " HR-V"
        elif (modelo == 5):
            marca += " Accord"
    elif (aleatorio == 3):
        marca = "Nissan"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Altima"
        elif (modelo == 1):
            marca += " Rogue"
        elif (modelo == 2):
            marca += " Sentra"
        elif (modelo == 3):
            marca += " Murano"
        elif (modelo == 4):
            marca += " Maxima"
        elif (modelo == 5):
            marca += " Armada"
    elif (aleatorio == 4):
        marca = "Subaru"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Outback"
        elif (modelo == 1):
            marca += " Impreza"
        elif (modelo == 2):
            marca += " WRX"
        elif (modelo == 3):
            marca += " Forester"
        elif (modelo == 4):
            marca += " BRZ"
        elif (modelo == 5):
            marca += " XV"
    elif (aleatorio == 5):
        marca = "Mazda"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " 3"
        elif (modelo == 1):
            marca += " 6"
        elif (modelo == 2):
            marca += " MX-5 Miata"
        elif (modelo == 3):
            marca += " RX-8"
        elif (modelo == 4):
            marca += " CX-30"
        elif (modelo == 5):
            marca += " CX-5"
    elif (aleatorio == 6):
        marca = "Suzuki"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Swift"
        elif (modelo == 1):
            marca += " Jimny"
        elif (modelo == 2):
            marca += " Vitara"
        elif (modelo == 3):
            marca += " Baleno"
        elif (modelo == 4):
            marca += " Ignis"
        elif (modelo == 5):
            marca += " S-Cross"
    elif (aleatorio == 7):
        marca = "Lexus"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " RX"
        elif (modelo == 1):
            marca += " EX"
        elif (modelo == 2):
            marca += " IS"
        elif (modelo == 3):
            marca += " NX"
        elif (modelo == 4):
            marca += " LX"
        elif (modelo == 5):
            marca += " LC"
    elif (aleatorio == 8):
        marca = "Acura"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " MDX"
        elif (modelo == 1):
            marca += " RDX"
        elif (modelo == 2):
            marca += " TLX"
        elif (modelo == 3):
            marca += " ILX"
        elif (modelo == 4):
            marca += " NSX"
        elif (modelo == 5):
            marca += " RSX"
    elif (aleatorio == 9):
        marca = "Infiniti"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " Q50"
        elif (modelo == 1):
            marca += " Q60"
        elif (modelo == 2):
            marca += " QX50"
        elif (modelo == 3):
            marca += " QX60"
        elif (modelo == 4):
            marca += " QX80"
        elif (modelo == 5):
            marca += " QX70"
    elif (aleatorio == 10):
        marca = "Isuzu"
        modelo = random.randint(0, 5)
        if (modelo == 0):
            marca += " D-MAX"
        elif (modelo == 1):
            marca += " MU-X"
        elif (modelo == 2):
            marca += " Trooper"
        elif (modelo == 3):
            marca += " Axiom"
        elif (modelo == 4):
            marca += " VehiCROSS"
        elif (modelo == 5):
            marca += " Gemini"
    anno = random.randint(1975, datetime.now().year)
    tarifa = round(random.uniform(50.00, 150.00), 2)
    return {'Matricula': matricula, 'MarcaModelo': marca, 'AnnoFabricacion': anno, 'TarifaDia': tarifa,
            'Estado': 'Disponible'}"""

'''
vehicle_data = {
    'Matricula': 'ABC666',
    'MarcaModelo': 'Honda Civic',
    'AnnoFabricacion': '2006',
    'TarifaDia': '250.00',
    'Estado': 'Disponible'
}

cargar_arbol_xml()
crear_vehiculo(vehicle_data)
crear_vehiculo(vehicle_data2)
mostrar_todos()
'''
