
#from xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

def construir():
    #arbol = ET.parse("agenda.xml")
    a = ET.Element('a')
    b = ET.SubElement(a, 'b')
    c = ET.SubElement(a, 'c')
    d = ET.SubElement(c, 'd')
    ET.dump(a)
    ElementTree(a).write("salida.xml")

print("Inicio proyecto")

print("Fin proyecto")
