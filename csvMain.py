import csv
import matplotlib.pyplot as plt
import numpy as np
#"Date","Longitude","Latitude","Elevation","Max Temperature","Min Temperature","Precipitation","Wind","Relative Humidity","Solar"    
def calcularPromedios(data):
    promediosTempMax = []
    promediosTempMin = []
    promedioHumedad = []
    
    tempMax = data[0]
    tempMin = data[1]
    humedad = data[2]

    for i in tempMax:
        promedio = sum(i) / len(i)
        promediosTempMax.append(promedio)

    for j in tempMin:
        promedio = sum(j) / len(j)
        promediosTempMin.append(promedio)
    
    for k in humedad:
        promedio = sum(k) / len(k)
        promedioHumedad.append(promedio)

    listaPromedios = [promediosTempMax, promediosTempMin, promedioHumedad]

    return listaPromedios

def filtroAnio(lista):
    
    tempmax= [[],[],[],[],[]]
    tempmin= [[],[],[],[],[]]
    humedad = [[],[],[],[],[]]
    
    
    for i in lista:
        
        if i["Fecha"][5:9] == "2015":
            tempmax[0].append(float(i["Max t"]))
            tempmin[0].append(float(i["Min t"]))
            humedad[0].append(float(i["Humedad"]))
        
        elif i["Fecha"][5:9] == "2016":
            tempmax[1].append(float(i["Max t"]))
            tempmin[1].append(float(i["Min t"]))
            humedad[1].append(float(i["Humedad"]))
        
        elif i["Fecha"][5:9] == "2017":
            tempmax[2].append(float(i["Max t"]))
            tempmin[2].append(float(i["Min t"]))
            humedad[2].append(float(i["Humedad"]))
        
        elif i["Fecha"][5:9] == "2018":
            tempmax[3].append(float(i["Max t"]))
            tempmin[3].append(float(i["Min t"]))
            humedad[3].append(float(i["Humedad"]))
        
        elif i["Fecha"][5:9] == "2019":
            tempmax[4].append(float(i["Max t"]))
            tempmin[4].append(float(i["Min t"]))
            humedad[4].append(float(i["Humedad"]))
       
        else:
            print("Error")

    data = [tempmax,tempmin,humedad]
    
    return data

def csvaLista():
    
    data_lista = []
    archivo_csv = 'weatherdata.csv'
    
    with open(archivo_csv, 'r') as archivo:
        
        data_leida = csv.reader(archivo)
        
        for fila in data_leida:
            
            indice = {"Fecha": fila[0],
                    "Longitud": fila[1],
                    "Latitud": fila[2],
                    "Elevacion": fila[3],
                    "Max t": fila[4],
                    "Min t": fila[5],
                    "Precipitaciones": fila[6],
                    "Viento": fila[7],
                    "Humedad": fila[8],
                    "Solar": fila[9]}
            
            data_lista.append(indice)

    return data_lista

def main():
    lista = csvaLista()
    data = filtroAnio(lista)
    promedios = calcularPromedios(data)
    menu = input("1 2 3")

    if menu == "1":
        y = promedios[0]
        x = [2015, 2016, 2017, 2018, 2019]
        y2 = promedios[1]

        plt.plot(x, y, "r")
        plt.plot(x, y2, "b")
        
        
        plt.xlabel("Año")
        plt.ylabel("ºC")
        plt.title("Promedio de temperatura maxima y minima por año")
        plt.show()

    elif menu =="2":
        y = promedios[2]
        x = [2015, 2016, 2017, 2018, 2019]

        plt.plot(x, y, "r")

        plt.xlabel("Año")
        plt.ylabel("Humedad relativa (fraccion)")
        plt.title("Promedio de humedad por año")
        plt.show()

    elif menu == "3":
        pass


main()
