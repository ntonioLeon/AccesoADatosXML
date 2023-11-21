# from xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree


def construir():
    # arbol = ET.parse("agenda.xml")
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    c = ET.SubElement(a, 'c')
    d = ET.SubElement(c, 'd')
    ET.dump(a)
    ElementTree(a).write("salida.xml")


def prettify(elem):
    from xml.etree import ElementTree
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def construir2():
    top = Element('top')

    comment = Comment('Generated for PyMOTW')
    top.append(comment)

    child = SubElement(top, 'child')
    child.text = 'This child contains text.'

    child_with_tail = SubElement(top, 'child_with_tail')
    child_with_tail.text = 'This child has regular text.'
    child_with_tail.tail = 'And "tail" text.'

    child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
    child_with_entity_ref.text = 'This & that'

    print(prettify(top))


def construir3():
    top = Element('Agenda')
    con1 = ET.SubElement(top, 'contacto')
    nom = ET.SubElement(con1, 'nombre')
    nom.text = "Juan"
    dir = ET.SubElement(con1, 'direccion')
    dir.text = "Madrid"
    tel = ET.SubElement(con1, 'telefono')
    tel.text = "666-555-333"
    con1 = ET.SubElement(top, 'contacto')
    nom = ET.SubElement(con1, 'nombre')
    nom.text = "Jose"
    dir = ET.SubElement(con1, 'direccion')
    dir.text = "Segovia"
    tel = ET.SubElement(con1, 'telefono')
    tel.text = "666-555-333"
    ElementTree(top).write("salida2.xml")


def construir4():
    top = Element('Agenda')
    con1 = ET.Element('contacto')
    nom = ET.SubElement(con1, 'nombre')
    nom.text = "Juan"
    dir = ET.SubElement(con1, 'direccion')
    dir.text = "Madrid"
    tel = ET.SubElement(con1, 'telefono', {'atr1': "aaa", 'atr2': "bbb"})  # los atributos son un diccionario
    tel.text = "666-555-333"
    top.append(con1)  # Los elementos son listas
    con1 = ET.Element('contacto')
    nom = ET.SubElement(con1, 'nombre', id="A")
    nom.text = "Jose"
    dir = ET.SubElement(con1, 'direccion', id="A", id2="5")
    dir.text = "Segovia"
    tel = ET.SubElement(con1, 'telefono')
    tel.text = "666-555-333"
    tel.set("prefijo", "91")
    tel.set("prefijo2", "911")
    ElementTree(top).write("salida2.xml")
    top.append(con1)
    print(prettify(top))
    salida = prettify(top)
    file = open("salida3.xml", "w")
    file.write(salida)
    file.close()


def recorrer(nodo):
    print(nodo.tag, end="")
    # Para recorrer los atributos. Los atributos estan en un diccionario
    for attr in nodo.attrib:
        attrName = attr
        attrValue = nodo.attrib[attr]
        print("\t", attrName, ":", attrValue, " ", end="")
    print("\n\t", nodo.text)
    for n in nodo:
        recorrer(n)


# DOM
# SAX
tree = ET.parse("agenda.xml")
root = tree.getroot()

print(root.tag)
for child in root:
    print(child.tag)

print("---------")
recorrer(root)

construir()
construir2()
construir3()
construir4()

print("Fin")
