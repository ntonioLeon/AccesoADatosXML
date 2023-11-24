import CRUD_Vehiculo

def tres_opciones():
    """
    Metodo que apoya a los menus en la entrada de teclado
    :return: resultado de la seleccion del menu
    """
    fallos=0
    while True:
        print("╔════════════════════════════════╗")
        print("║Seleccione para continuar       ║")
        respuesta = input("║ Opcion:")
        if respuesta == "0":
            return "0"
        elif respuesta  == '1':
            return "1"
        elif respuesta == '2':
            return "2"
        else:
            fallos += 1
            if fallos >=5:
                print("║ LLevas "+str(fallos)+" fallos, consecutivos"+" "*(2-len(str(fallos)))+" ║")
                print("║ Introduzca una opcion valida   ║")
                print("║            POR FAVOR           ║")
                print("╚════════════════════════════════╝")
            else:
                print("║ LLevas "+str(fallos)+" fallos, consecutivos"+" "*(2-len(str(fallos)))+" ║")
                print("║ Introduzca una opcion valida:  ║")
                print("╚════════════════════════════════╝")


def cinco_opciones(cadena):
    """
    Metodo que apoya a los menus en la entrada de teclado
    :return: resultado de la seleccion del menu
    """
    fallos=0
    while True:
        respuesta = input(cadena)
        if respuesta == "0":
            return "0"
        elif respuesta  == '1':
            return "1"
        elif respuesta == '2':
            return "2"
        elif respuesta == '3':
            return "3"
        elif respuesta == '4':
            return "4"
        else:
            if fallos==3:
                return 0
            else:
                print("║  Introduzca una opcion valida:")
                print("╚════════════════════════════════╝")


def seis_opciones(cadena):
    """
    Metodo que apoya a los menus en la entrada de teclado
    :return: resultado de la seleccion del menu
    """
    fallos=0
    while True:
        if cadena is not None:
            respuesta = input(cadena)
        else:
            respuesta = input()
        if respuesta == "0":
            return "0"
        elif respuesta  == '1':
            return "1"
        elif respuesta == '2':
            return "2"
        elif respuesta == '3':
            return "3"
        elif respuesta == '4':
            return "4"
        elif respuesta == '5':
            return "5"
        else:
            if fallos==3:
                return 0
            else:
                print("║  Introduzca una opcion valida:")
                print("╚════════════════════════════════╝")


def fails(fallos, modificacion):
    fallos += 1
    print("║ "+str(fallos)+"/3 fallos hasta salir del " + modificacion)
    return fallos


def si_no(cadena):
    """
    funcion que sirve como comprobante para las preguntas al usuario.
    @:param cadena que se printeara junto a la pregunta.
    """
    print(cadena)
    while True:
        print("╠════════════════════════════════╣")
        print("║ 1. SI                          ║")
        print("║ 2. NO                          ║")
        print("╠════════════════════════════════╣")
        respuesta = input("║  Introduzca una opcion valida:")
        print("╠════════════════════════════════╣")
        if respuesta == "1":
            return True
        elif respuesta == '2':
            return False
        print(cadena)


def mostrar_nuevo_vehicle(vehicle):

    print("║         Nuevo Vehiculo         ║")
    print("╠════════════════════════════════╣")
    print("║ Matricula: "+vehicle['Matricula']+"              ║")
    print("║ Modelo: "+vehicle['MarcaModelo']+" "*(23-len(vehicle['MarcaModelo']))+"║")
    print("║ Fecha fabricacion: "+str(vehicle['AnnoFabricacion'])+"        ║")
    print("║ Tarifa: "+str(vehicle['TarifaDia'])+" "*(23-len(str(vehicle['TarifaDia'])))+"║")
    print("║              ----              ║")




def mostar_menu_alquileres():
    print("╔════════════════════════════════╗")
    print("║   Menu Gestion de Alquileres   ║")
    print("╠════════════════════════════════╣")
    print("║ 1. Nuevo Alquiler              ║")
    print("║ 2. Busqueda de Alquiler        ║")
    print("║ 3. Modificar Alquiler          ║")
    print("║ 4. Finalizacion de Alquiler    ║")
    print("║ 5. Mostrar Todos los Alquileres║")
    print("║              ----              ║")
    print("║ 0. Volver al Menu Princpal     ║")
    print("╚════════════════════════════════╝")


def mostar_menu_vehiculo():
    print("╔════════════════════════════════╗")
    print("║   Menu Gestion de Vehículos    ║")
    print("╠════════════════════════════════╣")
    print("║ 1. Alta de Vehículo            ║")
    print("║ 2. Buscar Vehículo             ║")
    print("║ 3. Modificar Vehículo          ║")
    print("║ 4. Baja de Vehículo            ║")
    print("║ 5. Mostrar Todos los Vehículos ║")
    print("║              ----              ║")
    print("║ 0. Volver al Menu Princpal     ║")
    print("╚════════════════════════════════╝")


def mostar_menu_principal():
    print("╔════════════════════════════════╗")
    print("║    Menu Gestion de Renting     ║")
    print("╠════════════════════════════════╣")
    print("║ 1. Gestion Vehiculos           ║")
    print("║ 2. Gestion Alquileres          ║")
    print("║              ----              ║")
    print("║ 0. Cerrar el programa          ║")
    print("╚════════════════════════════════╝")


def menu_modificar_vehiculo(root):
    errores=0
    renuncia = False
    while not renuncia:
        fallos = 0
        print("╔════════════════════════════════╗")
        print("║    Menu Modificar Vehículos    ║")
        print("╠════════════════════════════════╣")
        if CRUD_Vehiculo.check_status(root):
            print("║ Introduzca la matricula del    ║")
            print("║ vehiculo que desea modificar   ║")
            pregunta = input("║ Matricula, formato AAA000: ")
            if CRUD_Vehiculo.matricula_en_uso(pregunta, root): #esta
                vehicle=CRUD_Vehiculo.obtener_vehiculo(pregunta)

                if vehicle is not None:
                    modificacion = seis_opciones("║ 1. Modificar Matricula         ║\n"
                                                 "║ 2. Modificar Marca/Modelo      ║\n"
                                                 "║ 3. Modificar Anno Fabricacion  ║\n"
                                                 "║ 4. Modificar Tarifa diaria     ║\n"
                                                 "║              ----              ║\n"
                                                 "║ Seleccione que desea modificar ║\n"
                                                 "║              ----              ║\n"
                                                 "║ 0. Cancelar modificacion       ║\n"
                                                 "╠════════════════════════════════╣")
                    if modificacion == "0":

                        renuncia = True
                    elif modificacion == "1":
                        exito = False
                        fallos = 0
                        print("║ Matricula antigua: " + vehicle['Matricula'] + "      ║")
                        while not exito:
                            matricula = input("║ Matricula, formato AAA000: ")
                            if matricula is not None and not CRUD_Vehiculo.matricula_en_uso(matricula, root) and CRUD_Vehiculo.verificar_matricula(matricula):
                                print("║ Matricula introducida con exito║")
                                vehiculo = {'Matricula': matricula, 'MarcaModelo': vehicle['MarcaModelo'], 'AnnoFabricacion': vehicle['AnnoFabricacion'],
                                           'TarifaDia': vehicle['TarifaDia'], 'Estado': vehicle['Estado']}
                                mostrar_nuevo_vehicle(vehiculo)
                                if si_no("║ Desea modificar vehiculo       ║\n║ con estas caracteristicas?     ║"):
                                    CRUD_Vehiculo.modificar_vehiculo(root, pregunta, vehiculo)
                                    #AQUIIIIIIIIIIIIIIIII
                                    print("║ Coche modificado.              ║")
                                    print("╚════════════════════════════════╝")
                                    exito = True

                                else:
                                    print("║ Modificacion cancelada.        ║")
                                    print("╚════════════════════════════════╝")
                                    exito = True

                            elif matricula is None:
                                print("║ No introduzca cadenas vacias   ║")
                                fallos = fails(fallos, "Alta")
                            elif not CRUD_Vehiculo.verificar_matricula(matricula):
                                print("║ Formato de matricula no valido ║")
                                fallos = fails(fallos, "Alta")
                            elif CRUD_Vehiculo.matricula_en_uso(matricula, root):
                                print("║ No introduzca cadenas vacias   ║")
                                fallos = fails(fallos, "Alta")
                            if fallos == 3:
                                print("║ Ha alcanzado el máximo de      ║")
                                print("║ intentos. Saliendo del proceso.║")
                                print("╚════════════════════════════════╝")
                                exito = True

                    elif modificacion == "2":

                        fallos = 0
                        exito = False
                        print("║ Marca/Modelo antigua: " + vehicle['MarcaModelo'])
                        while not exito:
                            marca = input("║ Introduzca la nueva Marca/Modelo : ")
                            if marca is not None:
                                print("║ Marca introducida con exito    ║")
                                vehiculo = {'Matricula': vehicle['Matricula'], 'MarcaModelo': marca,
                                            'AnnoFabricacion': vehicle['AnnoFabricacion'],
                                            'TarifaDia': vehicle['TarifaDia'], 'Estado': vehicle['Estado']}
                                mostrar_nuevo_vehicle(vehiculo)
                                if si_no("║ Desea modificar vehiculo       ║\n║ con estas caracteristicas?     ║"):
                                    CRUD_Vehiculo.modificar_vehiculo(root, pregunta, vehiculo)
                                    print("║ Coche modificado.              ║")
                                    print("╚════════════════════════════════╝")
                                    exito = True

                                else:
                                    print("║ Modificacion cancelada.        ║")
                                    print("╚════════════════════════════════╝")
                                    exito = True

                            elif marca is None:
                                print("║ No introduzca cadenas vacias   ║")
                                fallos = fails(fallos, "Alta")

                            if fallos == 3:
                                print("║ Ha alcanzado el máximo de      ║")
                                print("║ intentos. Saliendo del proceso.║")
                                print("╚════════════════════════════════╝")
                                exito = True
                                renuncia = True

                    elif modificacion == "3":

                        fallos = 0
                        exito = False
                        print("║ Fecha antigua: " + vehicle['AnnoFabricacion'])
                        while not exito:
                            print("║ Fecha, recuerde entre 1970-2023║")
                            anno = input("║ Fecha de fabricacion: ")
                            if anno is not None:
                                if anno.isnumeric():
                                    anno = int(anno)
                                    if 1970 <= anno <= 2023:
                                        print("║ Fecha introducida con exito    ║")
                                        vehiculo = {'Matricula': vehicle['Matricula'], 'MarcaModelo': vehicle['MarcaModelo'],
                                                    'AnnoFabricacion': anno,
                                                    'TarifaDia': vehicle['TarifaDia'], 'Estado': vehicle['Estado']}
                                        mostrar_nuevo_vehicle(vehiculo)
                                        if si_no("║ Desea modificar vehiculo       ║\n║ con estas caracteristicas?     ║"):
                                            CRUD_Vehiculo.modificar_vehiculo(root, pregunta, vehiculo)
                                            print("║ Coche modificado.              ║")
                                            print("╚════════════════════════════════╝")
                                            exito = True

                                        else:
                                            print("║ Modificacion cancelada.        ║")
                                            print("╚════════════════════════════════╝")
                                            exito = True

                                    else:
                                            print("║ No ha introducido fecha valida.║")
                                            fallos = fails(fallos, "Alta")
                                else:
                                    print("║ Introduzca una fecha valida    ║")
                                    fallos = fails(fallos, "Alta")
                            elif anno is None:
                                print("║ No introduzca cadenas vacias   ║")
                                fallos = fails(fallos, "Alta")

                            if fallos == 3:
                                print("║ Ha alcanzado el máximo de      ║")
                                print("║ intentos. Saliendo del proceso.║")
                                print("╚════════════════════════════════╝")
                                exito = True
                                renuncia = True

                    elif modificacion == "4":

                            fallos = 0
                            exito = False
                            print("║ Tarifa antigua: " + vehicle['TarifaDia'])
                            while not exito:
                                print("║ Introduzca una tarifa. Recuerde║")
                                print("║ nuestros modelos abarcan       ║")
                                tarifa = input("║ entre 50 y 250€ al dia: ")
                                tarifa = CRUD_Vehiculo.isdecima(tarifa)
                                if tarifa is not None:
                                    print("║ Tarifa introducida con exito   ║")
                                    vehiculo = {'Matricula': vehicle['Matricula'], 'MarcaModelo': vehicle['MarcaModelo'],
                                                'AnnoFabricacion': vehicle['AnnoFabricacion'],
                                                'TarifaDia': tarifa, 'Estado': vehicle['Estado']}
                                    mostrar_nuevo_vehicle(vehiculo)
                                    if si_no("║ Desea modificar vehiculo       ║\n║ con estas caracteristicas?     ║"):
                                        CRUD_Vehiculo.modificar_vehiculo(root, pregunta, vehiculo)
                                        print("║ Coche modificado.              ║")
                                        print("╚════════════════════════════════╝")
                                        exito = True

                                    else:
                                        print("║ Modificacion cancelada.        ║")
                                        print("╚════════════════════════════════╝")
                                        exito = True
                                    exito = True
                                else:
                                    fallos = fails(fallos, "Alta")

                                if fallos == 3:
                                    print("║ Ha alcanzado el máximo de      ║")
                                    print("║ intentos. Saliendo del proceso.║")
                                    print("╚════════════════════════════════╝")
                                    exito = True
                                    renuncia = True

                    print("╔════════════════════════════════╗")
                    if si_no("║¿Continuar en Menu Modificacion?║"):
                        print("║ Volviendo al Menu Modificacion ║")
                        print("╚════════════════════════════════╝")
                        renuncia = False
                    else:
                        print("║ Volviendo al Menu Vehiculos    ║")
                        print("╚════════════════════════════════╝")
                        renuncia = True
                else:
                    print("║ Fallo al encontrar Vehiculo    ║")
                    print("║ Slaiendo del menu              ║")
                    renuncia = True
            else:
                if errores == 2:
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║              ----              ║")
                    print("║ Volviendo al menu Vehiculos    ║")
                    print("╚════════════════════════════════╝")
                    renuncia = True
                else:
                    errores += 1
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║ "+str(errores)+"/3 fallos antes de salir      ║")
                    print("╚════════════════════════════════╝")
        else:
            renuncia = True


def menu_alta_vehiculo(root):
    renuncia = False
    while not renuncia:
        fallos = 0
        print("╔════════════════════════════════╗")
        print("║      Menu Alta Vehiculos       ║")
        print("╠════════════════════════════════╣")
        exito = False
        while not exito:
            matricula= input("║ Matricula, formato AAA000: ")
            if matricula is not None and not CRUD_Vehiculo.matricula_en_uso(matricula, root) and CRUD_Vehiculo.verificar_matricula(matricula):
                print("║ Matricula introducida con exito║")
                exito = True
            elif matricula is None:
                print("║ No introduzca cadenas vacias   ║")
                fallos = fails(fallos, "Alta")
            elif not CRUD_Vehiculo.verificar_matricula(matricula):
                print("║ Formato de matricula no valido ║")
                fallos = fails(fallos, "Alta")
            elif CRUD_Vehiculo.matricula_en_uso(matricula, root):
                print("║ No introduzca cadenas vacias   ║")
                fallos = fails(fallos, "Alta")
            if fallos == 3:
                print("║ Ha alcanzado el máximo de      ║")
                print("║ intentos. Saliendo del proceso.║")
                print("╚════════════════════════════════╝")
                exito = True
                renuncia = True

        if fallos < 3:
            fallos = 0
            exito = False
            while not exito:
                marca = input("║ Marca: ")
                if marca is not None:
                    print("║ Marca introducida con exito    ║")
                    exito = True
                elif marca is None:
                    print("║ No introduzca cadenas vacias   ║")
                    fallos = fails(fallos, "Alta")

                if fallos == 3:
                    print("║ Ha alcanzado el máximo de      ║")
                    print("║ intentos. Saliendo del proceso.║")
                    print("╚════════════════════════════════╝")
                    exito = True
                    renuncia = True

            if fallos < 3:
                fallos = 0
                exito = False
                while not exito:
                    modelo = input("║ Modelo: ")
                    if modelo is not None:
                        print("║ Modelo introducida con exito   ║")
                        exito = True
                    elif modelo is None:
                        print("║ No introduzca cadenas vacias   ║")
                        fallos = fails(fallos, "Alta")

                    if fallos == 3:
                        print("║ Ha alcanzado el máximo de      ║")
                        print("║ intentos. Saliendo del proceso.║")
                        print("╚════════════════════════════════╝")
                        exito = True
                        renuncia = True

            if fallos < 3:
                fallos = 0
                exito = False
                while not exito:
                    print("║ Fecha, recuerde entre 1970-2023║")
                    anno = input("║ Fecha de fabricacion: ")
                    if anno is not None:
                        if anno.isnumeric():
                            anno = int(anno)
                            if 1970 <= anno <= 2023:
                                print("║ Fecha introducida con exito    ║")
                                exito = True
                            else:
                                print("║ No ha introducido fecha valida.║")
                                fallos = fails(fallos, "Alta")
                        else:
                            print("║ Introduzca una fecha valida    ║")
                            fallos = fails(fallos, "Alta")
                    elif anno is None:
                        print("║ No introduzca cadenas vacias   ║")
                        fallos = fails(fallos, "Alta")

                    if fallos == 3:
                        print("║ Ha alcanzado el máximo de      ║")
                        print("║ intentos. Saliendo del proceso.║")
                        print("╚════════════════════════════════╝")
                        exito = True
                        renuncia = True

            if fallos < 3:
                fallos = 0
                exito = False
                while not exito:
                    print("║ Introduzca una tarifa. Recuerde║")
                    print("║ nuestros modelos abarcan       ║")
                    tarifa = input("║ entre 50 y 250€ al dia: ")
                    tarifa = CRUD_Vehiculo.isdecima(tarifa)
                    if tarifa is not None:
                        print("║ Tarifa introducida con exito   ║")
                        exito = True
                    else:
                        fallos = fails(fallos, "Alta")

                    if fallos == 3:
                        print("║ Ha alcanzado el máximo de      ║")
                        print("║ intentos. Saliendo del proceso.║")
                        print("╚════════════════════════════════╝")
                        exito = True
                        renuncia = True

            if fallos < 3:
                fallos = 0
                retorno = False

                vehicle = {'Matricula': matricula, 'MarcaModelo': marca+" "+modelo, 'AnnoFabricacion': anno, 'TarifaDia': tarifa,
                           'Estado': 'Disponible'}
                mostrar_nuevo_vehicle(vehicle)
                if si_no("║ Desea agregar un nuevo vehiculo║\n║ con estas caracteristicas?     ║"):
                    CRUD_Vehiculo.crear_vehiculo(vehicle, root)
                    print("║ Nuevo coche agrgado.           ║")
                    print("╚════════════════════════════════╝")
                    retorno = True
                else:
                    print("║ Alta cancelada     .           ║")
                    print("╚════════════════════════════════╝")
                    retorno = True
                if retorno:
                    print("╔════════════════════════════════╗")
                    if si_no("║ ¿Continuar en menu alta?       ║"):
                        print("║ Volviendo al Menu Alta         ║")
                        print("╚════════════════════════════════╝")
                        retono = False
                    else:
                        print("║ Volviendo al Menu Vehiculo     ║")
                        print("╚════════════════════════════════╝")
                        renuncia = True


def menu_buscar_vehiculo(root):
    errores = 0
    renuncia = False
    while not renuncia:
        fallos = 0
        print("╔════════════════════════════════╗")
        print("║      Menu Buscar Vehículos     ║")
        print("╠════════════════════════════════╣")
        if CRUD_Vehiculo.check_status(root):
            print("║ Introduzca la matricula del    ║")
            print("║ vehiculo que desea buscar      ║")

            pregunta = input("║ Matricula, formato AAA000: ")
            if CRUD_Vehiculo.matricula_en_uso(pregunta, root):  # esta
                vehicle = CRUD_Vehiculo.obtener_vehiculo(pregunta)

                if vehicle is not None:
                    mostrar_nuevo_vehicle(vehicle)
                    if si_no("║ ¿Desea buscar un otro vehiculo?║"):
                        print("║ Volviendo al Menu Busqueda     ║")
                        print("╚════════════════════════════════╝")
                        retono = False
                    else:
                        print("║ Volviendo al Menu Vehiculo     ║")
                        print("╚════════════════════════════════╝")
                else:
                    print("║ Fallo al encontrar Vehiculo    ║")
                    print("║ Slaiendo del menu              ║")
                    renuncia = True
            else:
                if errores == 2:
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║              ----              ║")
                    print("║ Volviendo al menu Vehiculos    ║")
                    print("╚════════════════════════════════╝")
                    renuncia = True
                else:
                    errores += 1
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║ " + str(errores) + "/3 fallos antes de salir      ║")
                    print("╚════════════════════════════════╝")
        else:
            renuncia = True

def menu_eliminar_vehiculo(root):
    errores = 0
    renuncia = False
    while not renuncia:
        fallos = 0
        print("╔════════════════════════════════╗")
        print("║       Menu Baja Vehículos      ║")
        print("╠════════════════════════════════╣")
        if CRUD_Vehiculo.check_status(root):
            print("║ Introduzca la matricula del    ║")
            print("║ vehiculo que desea dar de baja ║")
            pregunta = input("║ Matricula, formato AAA000: ")
            if CRUD_Vehiculo.matricula_en_uso(pregunta, root):  # esta
                vehicle = CRUD_Vehiculo.obtener_vehiculo(pregunta)
                if vehicle is not None:
                    mostrar_nuevo_vehicle(vehicle)
                    if si_no("║Desea dar de baja este vehiculo?║"):
                        CRUD_Vehiculo.eliminar_vehiculo(root, vehicle['idVehiculo'])
                    else:
                        print("║ Baja cancelada                 ║")
                        print("║ Volviendo al Menu Busqueda     ║")
                        print("╠════════════════════════════════╣")
                    if si_no("║ ¿Desea buscar un otro vehiculo?║"):
                        print("║ Volviendo al Menu Busqueda     ║")
                        print("╚════════════════════════════════╝")
                        retono = False
                    else:
                        print("║ Volviendo al Menu Vehiculo     ║")
                        print("╚════════════════════════════════╝")
                else:
                    print("║ Fallo al encontrar Vehiculo    ║")
                    print("║ Slaiendo del menu              ║")
                    renuncia = True
            else:
                if errores == 2:
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║              ----              ║")
                    print("║ Volviendo al menu Vehiculos    ║")
                    print("╚════════════════════════════════╝")
                    renuncia = True
                else:
                    errores += 1
                    print("║ La matricula introducida, no   ║")
                    print("║ corresponde con ningun vehiculo║")
                    print("║ " + str(errores) + "/3 fallos antes de salir      ║")
                    print("╚════════════════════════════════╝")
        else:
            renuncia = True

def menu_mostrar_vehiculo(root):
    print("╔════════════════════════════════╗")
    print("║      Menu Mostrar Vehículos    ║")
    print("╠════════════════════════════════╣")
    CRUD_Vehiculo.mostrar_todos(root)


def menu_vehiculo(root):
    """
    Se trata de un meno que gestiona los metodos de CRUD de vehiculos
    :return: None
    """
    retroceso= False
    while not retroceso:
        mostar_menu_vehiculo()
        respuesta = seis_opciones(None)

        if respuesta== "0":
            retroceso= True

        elif respuesta=="1":
            menu_alta_vehiculo(root)


        elif respuesta == "2":
            menu_buscar_vehiculo(root)


        elif respuesta == "3":
            menu_modificar_vehiculo(root)


        elif respuesta == "4":
            menu_eliminar_vehiculo(root)


        elif respuesta == "5":
            menu_mostrar_vehiculo(root)


def menu_alquiler(root):
    """
    Se trata de un meno que gestiona los metodos de CRUD de vehiculos
    :return: None
    """
    retroceso= False
    while not retroceso:
        mostar_menu_alquileres()
        respuesta = seis_opciones(None)

        if respuesta== "0":
            retroceso= True

        elif respuesta=="1":
            menu_alta_vehiculo(root)


        elif respuesta == "2":
            menu_buscar_vehiculo(root)


        elif respuesta == "3":
            menu_modificar_vehiculo(root)


        elif respuesta == "4":
            menu_eliminar_vehiculo(root)


        elif respuesta == "5":
            menu_mostrar_vehiculo(root)


def menu_principal(root):
    """
    Se trata de un meno que gestiona los metodos de CRUD de vehiculos
    :return: None
    """
    retroceso= False
    while not retroceso:
        mostar_menu_principal()
        respuesta = tres_opciones()

        if respuesta== "0":
            print("╠════════════════════════════════╣")
            print("║         Menu Principal         ║")
            print("╠════════════════════════════════╣")
            print("║              ----              ║")
            print("║ Cerrando el programa...        ║")
            print("╚════════════════════════════════╝")
            retroceso= True

        elif respuesta=="1":
            menu_vehiculo(root)

        elif respuesta == "2":
            menu_alquiler(root)

        elif respuesta == "3":
            retroceso = True


def menu_basico():
    """
    sMenu basico llamado desde el CRUD_Vehiculo que te manda a los diferentes submenus de vehiculos y alquileres.
    """
    tree = CRUD_Vehiculo.cargar_arbol_xml()
    root = tree.getroot()
    choice = ""
    while choice != "0":
        print("\nMenu:")
        print("1. Menu de vehiculos")
        print("2. Menu de alquileres")
        print("0. Salir del programa")
        choice = input("Selecciona una opcion (1/2/0): ")
        if choice == "1":
            print("Aun no habilitado")
        if choice == "2":
            print("Aun no habilitado")
        elif choice == "0":
            print("Saliendo del programa. Hasta luego!")
        else:
            print("Opción no valida.")



root = CRUD_Vehiculo.cargar_arbol_xml()
#menu_alta_vehiculo(root)
#menu_modificar_vehiculo(root)
#menu_buscar_vehiculo(root)
#menu_eliminar_vehiculo(root)
#menu_mostrar_vehiculo(root)
menu_principal(root)