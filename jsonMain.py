import json
from urllib.request import urlopen

def urlaLista(url):
    """Funcion que recibe un URL del cual saca un JSON y lo trasnforma a Lista
    Pre: Recibe un Url (string)
    Pos: Retorna una lista con un Json """
    try:
        url_ingresada = url
        abrir_url = urlopen(url_ingresada)
        leer_json = abrir_url.read()
        lista = json.loads(leer_json)    
        return lista
    except:
        print("\nE R R O R: Falla en conexion a servidores (Lista Vacia/No es Json/Sin internet)")
        return []

def formatoAlertas(url):
    """Funcion que recibe un url y retorna una lista con informacion relevante a Alertas
    Pre: Recibe un Url (string)
    Pos: Retorna, tras extraer informacion importante, una lista de diccionarios (Alertas) """
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
    """Funcion que recibe un url y retorna una lista con informacion relevante a Pronosticos
    Pre: Recibe un Url (string)
    Pos: Retorna, tras extraer informacion importante, una lista de diccionarios (Pronosticos)""" 
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
    """Funcion que recibe un url y retorna una lista con coordenadas
    Pre: Recibe un Url (string)
    Pos: Retorna, tras extraer informacion importante, una lista de diccionarios (coordenadas)"""
    listaUbicacion = urlaLista(url)
    try:
        coords = {"Latitud": listaUbicacion["results"][0]["geometry"]["location"]["lat"], "Longitud":listaUbicacion["results"][0]["geometry"]["location"]["lng"]}
        return coords 
    except:
        print(f"Google no pudo encontrar alguna de las ciudades...\n")
        errorCoords = {"Latitud": 0, "Longitud": 0}
        return errorCoords

def recolectoCiudadProv(url,ciudad):
    """Funcion que recibe un Url y una ciudad (string) y devuelve una lista de [ciudad,provincia]
    Pre: Recibe un Url (string) y una ciudad (string)
    Pos: Tras chequear que exista esa ciudad en el Json, te duelve una lista con [ciudad,provincia]"""
    lista = []
    recolectoCiudad = urlaLista(url)
    for item in recolectoCiudad:
        if item["name"].lower() == ciudad.lower():
            ciudadProv = [ciudad,item["province"].lower()]
            lista.append(ciudadProv)
    return lista