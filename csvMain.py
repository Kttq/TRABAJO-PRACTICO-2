import csv
import matplotlib.pyplot as plt
import numpy as np
#"Date","Longitude","Latitude","Elevation","Max Temperature","Min Temperature","Precipitation","Wind","Relative Humidity","Solar"    

def calcularPromedios(data):
    """Funcion que recibe data, y calcula promedios para luego devolver una lista
    Pre: Recibe una lista de datos
    Pos: Retorna una lista de promedios de temperatura y humedad"""
    promediosTempMax = []
    promediosTempMin = []
    promedioHumedad = []
    tempMax = data[0]
    tempMin = data[1]
    humedad = data[2]

    for i in range(len(tempMax)):
        promedio = sum(tempMax[i]) / len(tempMax[i])
        promediosTempMax.append(promedio)

    for j in range(len(tempMin)):
        promedio = sum(tempMin[j]) / len(tempMin[j])
        promediosTempMin.append(promedio)
    
    for k in range(len(humedad)):
        promedio = sum(humedad[k]) / len(humedad[k])
        promedioHumedad.append(promedio)

    listaPromedios = [promediosTempMax, promediosTempMin, promedioHumedad]

    return listaPromedios

def consultarIndiceVacio(lista, i):
    """Funcion que chequea si la lista esta vacia, si es verdad le asigna al primer
    elemento de una lista el valor 0 """
    if len(lista[i]) == 0:
        lista[i] = [0]

def filtroCategoria(diccionario):
    """Funcion que retorna una lista de datos tras filtrar por año los datos recibidos de un diccionario"""
    maxtemp = [[],[],[],[],[]]  
    mintemp = [[],[],[],[],[]]  #Separo listas en "ranuras", para identificar cada año del 2015 a 2019
    humedad = [[],[],[],[],[]]
    lluvia = [[],[],[],[],[]]
    
    for año in diccionario:
        if año == "2015":
            slot = 0
        elif año == "2016":
            slot = 1
        elif año == "2017":
            slot = 2
        elif año == "2018":
            slot = 3
        elif año == "2019":
            slot = 4

        for indice in range(len(diccionario[año])):
            maxtemp[slot].append(float(diccionario[año][indice]["Max t"]))
            mintemp[slot].append(float(diccionario[año][indice]["Min t"]))
            lluvia[slot].append(float(diccionario[año][indice]["Precipitaciones"]))
            humedad[slot].append(float(diccionario[año][indice]["Humedad"]))
    
    listaDatos = [maxtemp, mintemp, humedad, lluvia]
    for i in range(5):
        consultarIndiceVacio(maxtemp, i)
        consultarIndiceVacio(mintemp, i)
        consultarIndiceVacio(humedad, i)
        consultarIndiceVacio(lluvia, i)
    
    return listaDatos

def filtroAnio(lista):
    '''Se filtra toda la informacion de csvaLista segun el año de la fecha. Para datos del año 2020 y anteriores a 2015
       se guardan en la llave Otros
    '''
    anios = {"2015": [], "2016": [], "2017": [], "2018": [], "2019": []}
    for i in lista:
        
        fechaLista = i["Fecha"].split('/')
        anio = fechaLista[2]
        
        if anio == "2015":
            anios["2015"].append(i)

        elif anio == "2016":
            anios["2016"].append(i)

        elif anio == "2017":
            anios["2017"].append(i)

        elif anio == "2018":
            anios["2018"].append(i)

        elif anio == "2019":
            anios["2019"].append(i)
    
    return anios

def csvaLista():
    """Funcion que con un archivo CSV dado, lo transforma en una lista en la cual se puede manipular su informacion"""
    data_lista = []
    archivo_csv = 'weatherdata_original2.csv'
    try:
        with open(archivo_csv, 'r') as archivo:
            data_leida = csv.reader(archivo)
            next(data_leida, None)
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
    except:
        print("\nE R R O R: No se pudo abrir el archivo .CSV (Quizas no esta en la carpeta)\n")
        return []

def main():
    """Menu"""
    lista = csvaLista()
    print("lista")
    print(lista)
    data = filtroAnio(lista)
    print("data")
    print(data)
    dataPorAnio = filtroCategoria(data)
    print("dataporanio")
    print(dataPorAnio)
    promedios = calcularPromedios(dataPorAnio)
    print("promedios")
    print(promedios)
    bandera = True
    while bandera and not len(lista) == 0:
        #menu
        print("-----------------------------------------------")
        print("[1] Grafico promedio de temperaturas por año.\n[2] Grafico promedio de humedad por año.")
        print("[3] Milímetros máximos de lluvia de los últimos 5 años.\n[4] Temperatura máxima de los últimos 5 años. \n[5] Salir.")
        print("-----------------------------------------------")
        menu = input("\nSelecciona una opcion (1-2-3-4-5): ")
        while menu not in ["1","2","3","4","5"]:
            menu = input("\nSelecciona una opcion válida (1-2-3-4-5): ")
        
        if menu == "1":
            y = promedios[0]
            x = np.linspace(2015, 2019, 5)
            y2 = promedios[1]
            
            plt.plot(x, y, "r")
            plt.plot(x, y2, "b")
            plt.xlabel("Año")
            plt.ylabel("ºC")
            plt.title("Promedio de temperatura maxima y minima por año")
            plt.show()

        elif menu =="2":
            y = promedios[2]
            x = np.linspace(2015, 2019, 5)
            plt.plot(x, y, "r")
            plt.xlabel("Año")
            plt.ylabel("Humedad relativa (fraccion)")
            plt.title("Promedio de humedad por año")
            plt.show()
    
        elif menu == "3":
            maxLluviaAnual = []
            for anio in range(5):
                maxLluviaAnual.append(max(dataPorAnio[3][anio]))
            for record in maxLluviaAnual:
                for indice in lista:
                    if str(record) == indice["Precipitaciones"]:
                        print("El dia " + indice["Fecha"] + " en las coordenadas: " + indice["Longitud"] + ", " + indice["Latitud"])
                        print("Se registraron " + indice["Precipitaciones"] + " milimetros de lluvia.\n")
        
        elif menu == "4":
            maxTempAnual = []           
            for anio in range(5):
                maxTempAnual.append(max(dataPorAnio[0][anio]))     
            for record in maxTempAnual:          
                for indice in lista:
                    if str(record) == indice["Max t"]:
                        print("El dia " + indice["Fecha"] + " en las coordenadas: " + indice["Longitud"] + ", " + indice["Latitud"])
                        print("Se registraron " + indice["Max t"] + " grados centigrados.\n")

        elif menu == "5":
            bandera = False
            
main()
    