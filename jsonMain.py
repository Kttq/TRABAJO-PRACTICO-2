import json
from urllib.request import urlopen

def urlaLista(url):
    try:
        url_ingresada = url
        abrir_url = urlopen(url_ingresada)
        leer_json = abrir_url.read()
        lista = json.loads(leer_json)    
        return lista
    except:
        print("\nE R R O R: Falla en conexion a servidores (Lista Vacia)")
        return []

def formatoAlertas(url):
    listaAlertas = urlaLista(url)
    nuevaAlertas = []
    for item in listaAlertas:
        alerta = {"Titulo": item["title"],
                  "Tipo": item["status"],
                  "Fecha": item["date"],
                  "Hora": item["hour"],
                  "Descripcion": item["description"],
                  "Zonas": list(item["zones"].values())}
        nuevaAlertas.append(alerta)
    return nuevaAlertas

def pronosticoCiudad(url,ubicacion): 
    pronosticoDiario = urlaLista(url) 
    pronosticoEncontrado = [] 
    for item in pronosticoDiario: 
        resultadoLista = [item["name"].lower(),item["province"].lower()]
        if resultadoLista == ubicacion:
            pronostico = item["name"]
            pronostico = {"Mañana": {"Temperatura": str(item["weather"]["morning_temp"])+"°",
                                            "Descripción": item["weather"]["morning_desc"]},
                                "Tarde": {"Temperatura": str(item["weather"]["afternoon_temp"])+"°",
                                            "Descripción": item["weather"]["afternoon_desc"]},
                                "Coord": (item["lat"],item["lon"])}
            pronosticoEncontrado.append(pronostico)   
    return pronosticoEncontrado

def obtenerCoords(url):
    listaUbicacion = urlaLista(url)
    coords = {"Latitud": listaUbicacion["results"][0]["geometry"]["location"]["lat"], "Longitud":listaUbicacion["results"][0]["geometry"]["location"]["lng"]}
    return coords 

def recolectoCiudadProv(url,ciudad):
    lista = []
    recolectoCiudad = urlaLista(url)
    for item in recolectoCiudad:
        if item["name"].lower() == ciudad.lower():
            ciudadProv = [ciudad,item["province"].lower()]
            lista.append(ciudadProv)
    return lista