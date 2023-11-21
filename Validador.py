import datetime
import xml.etree.ElementTree as ET

def validar_dni():
    cont = 0
    while cont < 3:
        dni = input(
            "Introduzca un dni valido, este debe de tener 9 caracteres, los 8 primeros numeros y el ultimo una letra. ")
        if not dni.isspace():
            dni = dni.strip()  # El trim de python
            if len(dni) == 9:
                if dni[0:8].isnumeric():  # Es cerrado por la izquierda abierto por la derecha
                    if dni[8].isalpha():  # Solo coge el noveno caracter
                        print("DNI Valido.")
                        return dni
                    else:
                        cont += 1
                        print("El ultimo caracter debe tratarse de una letra. Fallos = ", cont)
                else:
                    cont += 1
                    print("Los primeros 8 caracteres deben tratarse de numeros. Fallos = ", cont)
            else:
                cont += 1
                print("El DNI debe de tener 9 caracteres. Fallos = ", cont)
        else:
            cont += 1
            print("La cadena no puede tratarse de una cadena vacia o solo de espacios, Fallos = ", cont)
    return None


def validar_fecha(fecha_ini=None):
    cont = 0
    anno = ""
    mes = ""
    dia = ""
    check = False
    fin = False
    while not fin:
        if fecha_ini is None:
            print("La fecha constará de anno, mes y dia.")
        else:
            print("La fecha constará de anno, mes y dia, recuerde que esta debe ser posterior a " + str(fecha_ini))
        while not check:
            anno = input("Introduzca el anno, este debe estar comprendido entre el anno 2000 y 2050: ")
            if not anno.isspace():
                anno = anno.strip()
                if anno.isnumeric():
                    if int(anno) >= 2000 and int(anno) <= 2050:
                        check = True
                    else:
                        cont += 1
                        print("La fecha debe estar contenida entre el anno 2000 y el anno 2050. Fallo = ", cont)
                else:
                    cont += 1
                    print("El anno debe ser numerico. Fallos = ", cont)
            else:
                cont += 1
                print("El anno no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
            if cont == 3:
                check = True
        if cont < 3:
            check = False
            while not check:
                mes = input("Introduzca el mes: ")
                if not (mes.isspace()):
                    mes = mes.strip()
                    if mes.isnumeric():
                        if int(mes) >= 1 and int(mes) <= 12:
                            check = True
                        else:
                            cont += 1
                            print("El mes debe estar contenido entre el mes 1 y 12. Fallo = ", cont)
                    else:
                        cont += 1
                        print("El mes debe ser numerico. Fallos = ", cont)
                else:
                    cont += 1
                    print("El mes no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
                if cont == 3:
                    check = True
        if cont < 3:
            check = False
            while not check:
                if int(mes) == 1 or int(mes) == 3 or int(mes) == 5 or int(mes) == 7 or int(mes) == 8 or int(
                        mes) == 10 or int(mes) == 12:
                    dia = input("Introduzca dia del 1 al 31: ")
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 31:
                                check = True
                            else:
                                cont += 1
                                print("El dia debe estar comprendido entre 1 y 31. Fallos = ", cont)
                        else:
                            cont += 1
                            print("El dia debe ser numerico. Fallos = ", cont)
                    else:
                        cont += 1
                        print("El dia no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
                elif int(mes) == 4 or int(mes) == 6 or int(mes) == 9 or int(mes) == 11:
                    dia = input("Introduzca dia del 1 al 30: ")
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 30:
                                check = True
                            else:
                                cont += 1
                                print("El dia debe estar comprendido entre 1 y 30. Fallos = ", cont)
                        else:
                            cont += 1
                            print("El dia debe ser numerico. Fallos = ", cont)
                    else:
                        cont += 1
                        print("El dia no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
                elif int(mes) == 2:
                    dia = input("Introduzca dia del 1 al 28: ")
                    if not (dia.isspace()):
                        dia = dia.strip()
                        if dia.isnumeric():
                            if int(dia) >= 1 and int(dia) <= 28:
                                check = True
                            else:
                                cont += 1
                                print("El dia debe estar comprendido entre 1 y 28. Fallos = ", cont)
                        else:
                            cont += 1
                            print("El dia debe ser numerico. Fallos = ", cont)
                    else:
                        cont += 1
                        print("El dia no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
                if cont == 3:
                    check = True
            if cont < 3:
                if fecha_ini is None:
                    print("Fecha Valida.")
                    return datetime.date(int(anno), int(mes), int(dia))
                else:
                    date = datetime.date(int(anno), int(mes), int(dia))
                    if fecha_ini < date:
                        fin = True
                        print("Fecha Valida.")
                        return date
                    else:
                        cont += 1
                        print("La fecha no puede ser anterior a", str(fecha_ini), ". Fallos = ", cont)
            else:
                print("La obtencion de la fecha se suspendio debido a que se fallaron demasiadas veces seguidas.")
                return None


def validar_kilometraje(km_ini=None):
    cont = 0
    while cont < 3:
        if km_ini is None:
            km = input("Introduzca un kilometraje valido, este debe ser un numero ")
        else:
            km = input("Introduzca un kilometraje valido, este debe ser un numero mayor a " + km_ini + " ")
        if len(km.strip()) > 0:
            km = km.strip()
            if km.isnumeric():
                if km_ini is None:
                    print("Kilometraje valido")
                    return km
                else:
                    if int(km) > int(km_ini):
                        print("Kilometraje valido")
                        return km
                    else:
                        cont += 1
                        print("El kilometrake debe ser mayor que ", km_ini, ". Fallos = ", cont)
            else:
                cont += 1
                print("El kilometrake debe ser un numero. Fallos = ", cont)
        else:
            cont += 1
            print("El kilometrake no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
    print("La obtencion del kilometrake se suspendio debido a que se fallaron demasiadas veces seguidas.")
    return None

def id_existe(root, identificacion):
    vehiculos = root.find("Vehiculos")
    if vehiculos is not None:
        vehiculo = vehiculos.find("Vehiculo")
        if vehiculo is not None:
            for attr in vehiculo.attrib:
                attr_name = attr
                attr_value = vehiculo.attrib[attr_name]
                if attr_value == identificacion:
                    return True
    return False

def validar_id(root):
    cont = 0
    while cont < 3:
        identification = input("Introduzca un id valido, este debe ser un numero ")
        if len(identification.strip()) > 0:
            identification = identification.strip()
            if identification.isnumeric():
                if id_existe(root, identification):
                    return identification
                else:
                    cont += 1
                    print("El id no se corresponde con el de ningun vehiculo existente. Fallos = ", cont)
            else:
                cont += 1
                print("El id debe ser un numero. Fallos = ", cont)
        else:
            cont += 1
            print("El id no puede tratarse de una cadena vacia o solo de espacios. Fallos = ", cont)
    print("La obtencion del id se suspendio debido a que se fallaron demasiadas veces seguidas.")
    return None
