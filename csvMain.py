import csv

#"Date","Longitude","Latitude","Elevation","Max Temperature","Min Temperature","Precipitation","Wind","Relative Humidity","Solar"
def csvaLista():
    data_lista = []
    with open('weatherdata.csv', 'r') as archivo:
        data_leida = csv.reader(archivo)
        for fila in data_leida:
            indice = {"Fecha": fila[0],
                    "Longitud": fila[1],
                    "Latitud": fila[2],
                    "Elevacion": fila[3],
                    "Max temperatura": fila[4],
                    "Min temperatura": fila[5],
                    "Precipitaciones": fila[6],
                    "Viento": fila[7],
                    "Humedad": fila[8],
                    "Solar": fila[9]}
            
            data_lista.append(indice)
    return data_lista
