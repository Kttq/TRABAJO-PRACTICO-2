import json
from urllib.request import urlopen

def urlaLista(url):
    url_ingresada = url
    abrir_url = urlopen(url_ingresada)
    leer_json = abrir_url.read()
    lista = json.loads(leer_json)    
    return lista

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

def pronosticoCiudad(url, ciudad):
    pronosticoDiario = urlaLista(url)
    dictPronostico = {}
    for item in pronosticoDiario:
         if item["name"].lower() == ciudad.lower():
             dictPronostico[item["province"]] = {"Dia": item["weather"]["day"],
                                                 "Mañana": {"Temperatura": item["weather"]["morning_temp"],
                                                            "Descripción": item["weather"]["morning_desc"]},
                                                 "Tarde": {"Temperatura": item["weather"]["afternoon_temp"],
                                                           "Descripción": item["weather"]["afternoon_desc"]}}           
    return dictPronostico
