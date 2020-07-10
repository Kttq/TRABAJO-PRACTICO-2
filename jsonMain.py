import json
from urllib.request import urlopen

def urlaLista(url):
    url_ingresada = url
    abrir_url = urlopen(url_ingresada)
    leer_json = abrir_url.read()
    lista = json.loads(leer_json)    
    return lista


    
    
        
        
