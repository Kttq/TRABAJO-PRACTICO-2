import jsonMain
from geopy import distance
from unidecode import unidecode

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

def mostrarAlertas(listaAlertas):
    """ Procedimiento que recibe una lista de diccionarios y muestra de manera ordenada sus datos
        Pre: Necesita que le pasen una lista
        Pos: Muestra en orden los componentes de cada alerta"""
    if len(listaAlertas) != 0:
        i = 0
        print("Las alertas encontradas son...")
        for alerta in listaAlertas:
            print(f"\nALERTA #{i+1}\n")
            for atributo in alerta:
                print(atributo,":",alerta[atributo])
            i += 1
    else:
        print("No hay alertas para mostrar...")

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
                print(f"Alerta encontrada a {distancia}Km !!!\n")
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
        print("Multiples resultados encontrados..")
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
    ciudad = input("\nIngrese la ciudad a buscar: ").lower()
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

def menuGraficos():
    print()

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
            menuGraficos()

        elif Seleccion == "4":
            pronosticoExtendido()
            
        elif Seleccion == "5":
            print("Nada")  
        
        elif Seleccion == "6":
            bandera = False
            print("\n¡Hasta luego!")

main()
    