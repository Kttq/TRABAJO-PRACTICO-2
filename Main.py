import jsonMain
from geopy import distance #Sirve para calcular distancia entre coordenadas.
from unidecode import unidecode #Sirve para eliminar errores en URLs por caracteres especiales.
import cv2
import numpy as np
import os.path
from urllib.request import urlopen
from datetime import datetime, timezone, timedelta

#URL DEL SNM
URL_ALERTAS = "https://ws.smn.gob.ar/alerts/type/AL"
URL_PRONOSTICO = ["https://ws.smn.gob.ar/map_items/forecast/1",
                "https://ws.smn.gob.ar/map_items/forecast/2",
                "https://ws.smn.gob.ar/map_items/forecast/3"]
#KEY DE API GOOGLE
GOOGLE_KEY = "AIzaSyBjcydmjry7-tklJTPPseYrcpUCznTRWH8"

def intCheck(string):
    """ Funcion que permite chequear que un string sea transformable en entero
        Pre: recibe un string
        Pos: tras chequear que dicho string sea transformable en entero,
        devuelve el string transformado"""
    bandera = True
    while bandera:
        try:
            string = int(string)
            return string
        except:
            print("\nNumero ingresado invalido...")
            string = input("Ingrese un valor: ")  

def floatCheck(x,y):
    """ Funcion que permite chequear que un par de strings sean transformables a Float
        Pre: necesita recibir un par de strings
        Pos: si son transformables devuelve un par de Floats"""
    bandera = True
    while bandera:
        try:
            x,y = float(x),float(y)
            return x , y
        except:
            print("Numeros ingresados son invalidos...")
            x = input("Ingrese el primer valor: ")
            y = input("Ingrese el segundo valor: ")

def latlongInput():
    """ Funcion que se asegura que un par de strings ingresados sean validas coordenadas
        Pre: no requiere un dato pasado
        Pos: si son validos los datos, devuelve las coordenadas (latitud,longitud)"""
    bandera = True
    while bandera:
        lat = input("Ingrese una latitud (entre -90 a 90 grados): ")
        lon = input("Ingrese una longitud (entre -180 a 180 grados): ")
        print("\nEspere un momento...\n")
        lat,lon = floatCheck(lat,lon)
        if (lat >= -90 and lat <= 90) and (lon >= -180 and lon <= 180) == True:
            return lat,lon
        else:
            print("\nCoordenadas fuera de rango...")

def mostrarAlertas(listaAlertas):
    """ Procedimiento que recibe una lista de diccionarios y muestra de manera ordenada sus datos
        Pre: Necesita que le pasen una lista
        Pos: Muestra en orden los componentes de cada alerta"""
    if len(listaAlertas) != 0:
        i = 0
        print("\nLas alertas encontradas son...")
        for alerta in listaAlertas:
            print(f"\nALERTA #{i+1}\n")
            for atributo in alerta:
                print(atributo,":",alerta[atributo])
            i += 1
    else:
        print("\nNo hay alertas para mostrar...")    

def listaCoords(listaAlertas):  #Preguntar maneras de como reducir tiempo de espera.
    """ Funcion que transforma una lista de zonas en coordenadas
        Pre: necesita una lista de alertas las cuales, cada una, tiene zonas afectadas.
        Pos: devuelve un lista de coordenadas separada por alertas."""
    nuevasCoords = []
    for alerta in listaAlertas:
        coords = [] #Creo esta vacia para separar por alerta las coordenadas. (se usa al momento de determinar cual alerta mostrar)
        for zona in alerta["Zonas"]:
            zona = unidecode(zona)
            zona = zona.replace(" ","%20")
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zona}&key={GOOGLE_KEY}"
            resultado = jsonMain.obtenerCoords(url)
            coords.append(resultado)
        nuevasCoords.append(coords)
    return nuevasCoords

def calculoDistancia(coordAlertas,coordUsuario,alertas):
    """ Procedimiento que calcula distancia entre unas coordenadas dadas por el usuario y areas afectadas por alertas
        Pre: necesita que le pasen listado de coordenadas afectadas por alertas, coordenadas dadas por el usuario
        y las alertas en cuestion:
        Pos: si detecta una alerta dentro de la distancia calculada, la muestra."""
    radioMin = input("Ingrese el radio de escaneo (en KM y se recomienda 50Km como minimo): ")
    radioMin = intCheck(radioMin)
    print("\nCalculando distancia...\n")
    lista = []
    for alerta in coordAlertas: #Recuerdo que separe la lista de coordenadas por alertas
        for coordenada in alerta:
            alertaCoord = (coordenada["Latitud"],coordenada["Longitud"])
            distancia = round((distance.distance(coordUsuario,alertaCoord).km),5)
            if distancia <= radioMin:
                print(f"Alerta encontrada a {distancia}Km !!!")
                indice = coordAlertas.index(alerta) #Consigo en cual alerta esta dicha coordenada.
                lista.append(alertas[indice]) #Muestro la alerta encontrada
    mostrarAlertas(lista)
    
def alertasLocales():
    """Funcion 'Maestra' de las alertasLocales, recopila y ejecuta todas las funciones relacionadas
    con esta actividad."""
    coordUsuario = latlongInput()
    alertas = jsonMain.formatoAlertas(URL_ALERTAS)
    coordenadas = listaCoords(alertas)
    calculoDistancia(coordenadas,coordUsuario,alertas)

def buscarPronosticos(ciudad,links):
    """ Funcion que retorna una lista de pronosticos a 3 dias con una ciudad dada
        Pre: necesita que le pasen una ciudad y links
        Pos: dependiendo de cuantos resultados se obtengan, retorna una lista con los pronosticos"""
    lista = jsonMain.recolectoCiudadProv(links[0],ciudad)
    if len(lista) == 0:
        print("\nCiudad no encontrada...")
        return []

    elif len(lista) > 1:
        print("\nMultiples resultados encontrados..")
        print(f"\nProvincias")
        for item in lista:
            print(f"{lista.index(item)+1}) "+item[1].upper())
            listaProv = [i[1].lower() for i in lista]
        provincia = input("\nIngresa a cual provincia te referis: ").lower()
        while provincia not in listaProv:
            provincia = input("Ingresa a una Provincia de las mostradas: ").lower()
        lista = [ciudad,provincia]
        return list(map(jsonMain.pronosticoCiudad,URL_PRONOSTICO,[lista]*3))

    else:
        print("\nResultado encontrado...")
        return list(map(jsonMain.pronosticoCiudad,URL_PRONOSTICO,lista*3))

def mostrarPronosticos(listaPronosticos):
    """ Procedimiento que tras pasarle una lista, muestra de manera ordenada pronosticos extendidos
        Pre: Necesita que le pasen una lista de pronosticos
        Pos: Muestra dichos pronosticos"""
    if len(listaPronosticos) != 0:
        i = 0
        print("\nLos pronosticos encontrados son...\n")
        for pronostico in listaPronosticos:
            print(f"DIA #{i+1}")
            for atributo in pronostico:
                if type(atributo) == dict:
                    for subAtributo in atributo:
                        print(subAtributo,":",atributo[subAtributo])
                    print()
                else:
                    print(atributo,":",pronostico[atributo])
            i += 1
    else:
        print("No hay pronostico para mostrar...\n")

def pronosticoExtendido():
    """Funcion 'Maestra' de pronosticos extendidos, recopila y ejecuta todas las funciones relacionadas con pronosticos."""
    ciudad = input("\nIngrese la ciudad a buscar (recuerda usar acentos): ").lower()  
    listaPronosticos = buscarPronosticos(ciudad,URL_PRONOSTICO)
    mostrarPronosticos(listaPronosticos)
    if listaPronosticos != []:
        seleccion = input(f"Desea escanear por alertas en {ciudad.capitalize()}? (Y/N): ").lower()
        while seleccion not in "yn":
            seleccion = input("Ingrese una opcion valida (Y/N): ").lower()
        if seleccion == "y":
            print("\nEspere un momento...")
            alertas = jsonMain.formatoAlertas(URL_ALERTAS)
            coordenadas = listaCoords(alertas)
            coordenadasCiudad = listaPronosticos[0][0]["Coord"]
            calculoDistancia(coordenadas,coordenadasCiudad,alertas)

def instertaImagen():
    '''Función que recibe la imagen ingresada por el usuario
        Pos: En caso de exito, imagen ingresada, como un objeto de la clase ndarray, de 3 dimensiones, y True
             En caso de no exito, None y False'''
    print("Ponga la imagen a analizar en la carpeta del programa, sin editar y en formato .png")
    nombreImagen = input("ingrese el nombre de la imagen: ")
    nombreImagen = nombreImagen + ".png"
    while not os.path.exists(nombreImagen):
        print("No se pudo cargar la imagen, verifique que haya escrito el nombre correctamente")
        nombreImagen = input("ingrese el nombre de la imagen: ")
        nombreImagen = nombreImagen + ".png"
    try:
        imagen = cv2.imread(nombreImagen)
        imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        exito = True
    except:
        imagenHSV = None
        exito = False
    return imagenHSV, exito

def analizaImagen(imagen, criterio, alertas):
    '''Función que verifica si se cumple condición para dar alerta
       Pre: Imagen cortada: ndarray de 3 dimensiones, criterio para dar alerta: entero,
            diccionario: donde se almacena un booleano por tipo de lluvia'''
    ROJO1_MIN = np.array([0, 50, 40])
    ROJO1_MAX = np.array([5, 255, 255])
    ROJO2_MIN = np.array([175, 50, 40])
    ROJO2_MAX = np.array([180, 255, 255])
    MAGENTA_MIN = np.array([140, 50, 40])
    MAGENTA_MAX = np.array([170, 255, 255])
    AMARILLO_MIN = np.array([10, 50, 40])
    AMARILLO_MAX = np.array([30, 255, 255])
    AZULVERDE_MIN = np.array([40, 50, 40])
    AZULVERDE_MAX = np.array([135, 255, 255])
    
    rangoRojo = cv2.inRange(imagen, ROJO1_MIN, ROJO1_MAX) + cv2.inRange(imagen, ROJO2_MIN, ROJO2_MAX)
    rangoMagenta = cv2.inRange(imagen, MAGENTA_MIN, MAGENTA_MAX)
    rangoAmarillo = cv2.inRange(imagen, AMARILLO_MIN, AMARILLO_MAX)
    rangoAzulVerde = cv2.inRange(imagen, AZULVERDE_MIN, AZULVERDE_MAX)
    
    contadorRojo = cv2.countNonZero(rangoRojo)
    contadorMagenta = cv2.countNonZero(rangoMagenta)
    contadorAmarillo = cv2.countNonZero(rangoAmarillo)
    contadorAzulVerde = cv2.countNonZero(rangoAzulVerde)
    
    if contadorMagenta >= criterio:        
        alertas["tormentaIntensa"] = True
    if contadorRojo >= criterio:
        alertas["lluviasFuertes"] = True
    if contadorAmarillo >= criterio:
        alertas["lluviasModeradas"] = True
    if contadorAzulVerde >= criterio:
        alertas["nubosidad"] = True

def generaAlertas(imagen, provincias):
    '''Función que genera las alertas, ordenadas por provincia
       Pre: Imagen a analizar: ndarray de 3 dimensiones, diccionario: con provincias
            a analizar como clave, y nombre de imagen como valor
       Pos: Diccionario: con provincias como clave, y alertas como valor, y un booleano'''
    largo, ancho = imagen.shape[:2]
    particion = 20
    criterio = 30    
    provinciasAlertas = {}
    for nombreProvincia in provincias:
        alertas = {"tormentaIntensa": False, "lluviasFuertes": False, "lluviasModeradas": False, "nubosidad": False}
        try:
            ruta = os.path.join(os.path.dirname(__file__), "provincias", provincias[nombreProvincia])
            imagenProvincia = cv2.imread(ruta)
            mascara = cv2.inRange(imagenProvincia, (0,0,0), (5,5,5))
            imagenAnalizar = cv2.bitwise_and(imagen, imagen, mask=mascara)
            exito = True
        except:
            imagenAnalizar = None
            exito = False
        if exito:
            for i in range(particion):
                for j in range(particion):
                    imagenCortada = imagenAnalizar[(largo//particion) * i:(largo//particion) * (i+1), (ancho//particion) * j:(ancho//particion) * (j+1)]
                    analizaImagen(imagenCortada, criterio, alertas)
            provinciasAlertas[nombreProvincia] = alertas
    return provinciasAlertas, exito

def imprimeAlertas(provinciasAlertas):
    '''Función que imprime alertas por provincia
       Pre: Diccionario, con provincias como clave, y alertas como valor'''
    for provincia, alertas in provinciasAlertas.items():
        sinAlerta = True
        print(f"\n{provincia}:")
        if alertas['nubosidad']:
            print("- Nubosidad")
        if alertas['lluviasModeradas']:
            print("- Lluvias Moderadas")
            sinAlerta = False
        if alertas['lluviasFuertes']:
            print("- Lluvias Fuertes")
            sinAlerta = False
        if alertas['tormentaIntensa']:
            print("- Tormentas Intensas")
            sinAlerta = False
        if sinAlerta:
            print("- No hay alertas de lluvia")

def fechaAEntero(fecha):
    '''Función que recibe una fecha, y devuelve valores como entero, en diccionario
       Pre: Fecha (objeto de clase datetime)
       Pos: Diccionario'''
    dia = fecha.day
    mes = fecha.month
    anio = fecha.year
    hora = fecha.hour
    minuto = fecha.minute
    return {'anio': anio, 'mes': mes, 'dia': dia, 'hora': hora, 'minuto': minuto}

def enteroAString(entero, minuto = False):
    '''Función que genera un string de dos digitos, con un entero
       Pre: Entero, booleano (opciona)
       Pos: String'''
    if entero < 10:
        string = '0'+str(entero)
    else:
        string = str(entero)
    if minuto:
        string = string[0] + '0'
    return string

def fechaAString(fechaEntero):
    '''Función que transforma enteros de un diccionario en strings
       Pre: Diccionario, con enteros como valores
       Pos: Diccionario, con strings como valores'''
    anioString = str(fechaEntero['anio'])
    mesString = enteroAString(fechaEntero['mes'])
    diaString = enteroAString(fechaEntero['dia'])
    horaString = enteroAString(fechaEntero['hora'])
    minutoString = enteroAString(fechaEntero['minuto'], True)
    return {'anio': anioString, 'mes': mesString, 'dia': diaString, 'hora': horaString, 'minuto': minutoString}

def obtenerImagenWeb():
    '''Función que obtiene imagen de la web
       Pos: En caso de exito, imagen ingresada, como un objeto de la clase ndarray, de 3 dimensiones, y True
            En caso de no exito, None y False'''
    fechaUTC = datetime.now(tz = timezone.utc)
    exito = False
    contador = 0
    while not exito and contador < 10:
        try:
            fechaEntero = fechaAEntero(fechaUTC)
            fechaString = fechaAString(fechaEntero)
            #ejemplo url: https://estaticos.smn.gob.ar/vmsr/radar/COMP_CEN_ZH_CMAX_20200718_183000Z.png
            URL = 'https://estaticos.smn.gob.ar/vmsr/radar/COMP_CEN_ZH_CMAX_' + fechaString['anio'] + fechaString['mes'] + fechaString['dia'] + '_' + fechaString['hora'] + fechaString['minuto'] + '00Z.png'
            with urlopen(URL) as url:
                nombreImagen = 'radar' + fechaString['anio'] + fechaString['mes'] + fechaString['dia'] + '_' + fechaString['hora'] + fechaString['minuto'] + '00UTC.png'
                with open(nombreImagen, 'wb') as file:
                    file.write(url.read())
            imagenActual = cv2.imread(nombreImagen)
            imagenActualHSV = cv2.cvtColor(imagenActual, cv2.COLOR_BGR2HSV)
            exito = True
        except:
            diezMinutos = timedelta(minutes =+ 10)
            fechaUTC -= diezMinutos
            contador += 1
            imagenActualHSV = None
    return imagenActualHSV, exito

def menuRadar():
    '''Menu del analisis de una imagen de radar'''
    bandera = True
    provincias = {"Buenos Aires": "BuenosAires.png", "Cordoba": "Cordoba.png", "Corrientes": "Corrientes.png", "Entre Rios": "EntreRios.png",
                  "La Pampa": "LaPampa.png", "La Rioja": "LaRioja.png", "Neuquen": "Neuquen.png", "Rio Negro": "RioNegro.png",
                  "San Luis": "SanLuis.png", "Santa Fe": "SantaFe.png"}
    while bandera:
        print("\n---------------- ANALISIS RADAR ----------------\n")
        print("[1] Igresar imagen\n[2] Estado actual\n[3] Volver\n")
        print("------------------------------------------------")
        
        opcion = input("\nSeleccione una opcion: ")
        while opcion not in ["1","2","3"]:
            opcion = input("\nSelecciona una opcion VALIDA (1-2-3): ")
        if opcion == "1":
            imagenIngresada, exito = instertaImagen()
            if exito:
                alertas, exito = generaAlertas(imagenIngresada, provincias)
                if exito:
                    imprimeAlertas(alertas)
                else:
                    print("\nNo se pudo analizar la imagen, verifique que la imagen sea correcta.")
            else:
                print('\nNo se pudo cargar la imagen.')
        if opcion == "2":
            imagenActual, exito = obtenerImagenWeb()
            if exito:
                alertas, exito = generaAlertas(imagenActual, provincias)
                if exito:
                    imprimeAlertas(alertas)
                else:
                    print("\nNo se pudo analizar la imagen")
            else:
                print('\nNo se pudo cargar la imagen.')
        elif opcion == "3":
            bandera = False

def main():
    bandera = True
    Seleccion = ""
    while bandera:
        print("\n--------------- T O R M E N T A ---------------\n")
        print("[1] Alertas Locales\n[2] Listado de Alertas\n[3] Informacion Zona Productora de Argentina")
        print("[4] Pronosticos por Ciudad\n[5] Analisis de Radar\n[6] Salir\n")
        print("-----------------------------------------------")

        Seleccion = input("\nSelecciona una opcion (1-2-3-4-5-6): ")
        while Seleccion not in ["1","2","3","4","5","6"]:
            Seleccion = input("\nSelecciona una opcion VALIDA (1-2-3-4-5-6): ")

        if Seleccion == "1":
            alertasLocales()
               
        elif Seleccion == "2":
            alertas = jsonMain.formatoAlertas(URL_ALERTAS)
            mostrarAlertas(alertas)

        elif Seleccion == "3":
            print("Nada")

        elif Seleccion == "4":
            pronosticoExtendido()
            
        elif Seleccion == "5":
            menuRadar()
        
        elif Seleccion == "6":
            bandera = False
            print("\n¡Hasta luego!")

main()
    