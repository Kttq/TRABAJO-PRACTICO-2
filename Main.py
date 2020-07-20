import jsonMain
from geopy import distance
from unidecode import unidecode

URL_ALERTAS = "https://ws.smn.gob.ar/alerts/type/AL"
GOOGLE_KEY = "AIzaSyBjcydmjry7-tklJTPPseYrcpUCznTRWH8"

def intCheck(string):
    bandera = True
    while bandera:
        try:
            string = int(string)
            return string
        except:
            print("\nNumero ingresado invalido...")
            string = input("Ingrese un valor: ")  

def floatCheck(x,y):
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
    if len(listaAlertas) != 0:
        i = 0
        print("\nLas alertas encontradas son...")
        for alerta in listaAlertas:
            print(f"\nALERTA #{i+1}\n")
            for atributo in alerta:
                print(atributo,":",alerta[atributo])
            i += 1
    else:
        print("No hay alertas para mostrar...")

def latlongInput():
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
            
def listaCoords(listaAlertas):
    nuevasCoords = []
    for alerta in listaAlertas:
        coords = [] #Creo esta vacia para separar por alerta las coordenadas. (se usa al momento de determinar cual alerta mostrar)
        for zona in alerta["Zonas"]:
            zona = unidecode(zona)
            zona = zona.replace(" ","%20")
            URL = f"https://maps.googleapis.com/maps/api/geocode/json?address={zona}&key={GOOGLE_KEY}"
            coords.append(jsonMain.obtenerCoords(URL))
        nuevasCoords.append(coords)
    return nuevasCoords      

def calculoDistancia(coordAlertas,coordUsuario,alertas):
    radioMin = input("Ingrese el radio de escaneo (en KM y se recomienda 100k como minimo): ")
    radioMin = intCheck(radioMin)
    print("\nCalculando distancia...\n")
    for alerta in coordAlertas: #Recuerdo que separe la lista de coordenadas por alertas
        for coordenada in alerta:
            alertaCoord = (coordenada["Latitud"],coordenada["Longitud"])
            distancia = round((distance.distance(coordUsuario,alertaCoord).km),5)
            if distancia <= radioMin:
                print(f"Alerta encontrada a {distancia}Km !!!\n")
                indice = coordAlertas.index(alerta) #Consigo en cual alerta esta dicha coordenada.
                mostrarAlertas([alertas[indice]]) #Muestro la alerta encontrada
    print("No se encontraron alertas en tu area...")
    
def alertasLocales():
    coordUsuario = latlongInput()
    alertas = jsonMain.formatoAlertas(URL_ALERTAS)
    coordenadas = listaCoords(alertas)
    calculoDistancia(coordenadas,coordUsuario,alertas)

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
            print("Nada")  
            
        elif Seleccion == "5":
            print("Nada")  
        
        elif Seleccion == "6":
            bandera = False
            print("\n¡Hasta luego!")

main()
    