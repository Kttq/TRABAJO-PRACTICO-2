import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

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

def calcularAño():
    # Se consigue el año corriente, es importante que el usuario tenga la fecha correcta en su computadora.
    fecha = str(date.today())
    fecha_lista = fecha.split("-")
    año = int(fecha_lista[0])
    
    return año

def filtroCategoria(diccionario, año_corriente):
    """Funcion que retorna una lista de datos tras filtrar por año los datos recibidos de un diccionario"""
    maxtemp = [[],[],[],[],[]]  
    mintemp = [[],[],[],[],[]]  #Separo listas en "ranuras", para identificar cada año desde los 4 años anteriores a año presente.
    humedad = [[],[],[],[],[]]
    lluvia = [[],[],[],[],[]]

    for año in diccionario:
        if año == "4 años":     # 4 AÑOS ATRAS
            slot = 0
        elif año == "3 años":   # 3 AÑOS ATRAS
            slot = 1
        elif año == "2 años":   # 2 AÑOS ATRAS
            slot = 2
        elif año == "1 año":   # 1 AÑO ATRAS
            slot = 3
        elif año == "Presente":     # AÑO CORRIENTE
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

def filtroAño(lista, año_corriente):
    '''Se filtra toda la informacion de csvaLista segun el año de la fecha.
    '''
    años = {"4 años": [], "3 años": [], "2 años": [], "1 año": [], "Presente": []}
    
    for i in lista:
        
        fechaLista = i["Fecha"].split('/')
        año = fechaLista[2]
        
        if año.isnumeric():
            if int(año) == (año_corriente-4):
                años["4 años"].append(i)

            elif int(año) == (año_corriente-3):
                años["3 años"].append(i)

            elif int(año) == (año_corriente-2):
                años["2 años"].append(i)

            elif int(año) == (año_corriente-1):
                años["1 año"].append(i)

            elif int(año) == (año_corriente):
                años["Presente"].append(i)
        else:
            print("Recuerde introducir fechas numéricas. ")
    
    return años

def csvaLista():
    """Funcion que con un archivo CSV dado, lo transforma en una lista en la cual se puede manipular su informacion
    Debe respetar la forma: ["Date", "Longitude", "Latitude", "Elevation", "Max Temperature", "Min Temperature", "Precipitation", "Wind", "Relative Humidity", "Solar"]   
    """
    data_lista = []
    archivo_csv = 'weatherdata_original2.csv'
    
    bandera = True
    while bandera == True:
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
            
            bandera = False
            return data_lista
        
        except:
            print("\nE R R O R: No se pudo abrir el archivo .CSV (Quizas no esta en la carpeta)\n")
            bandera = False

def main():
    """Menu"""
    AÑO_CORRIENTE = calcularAño()
    
    lista = csvaLista()
    data = filtroAño(lista, AÑO_CORRIENTE)
    dataPorAño = filtroCategoria(data, AÑO_CORRIENTE)
    promedios = calcularPromedios(dataPorAño)
    

    bandera = True
    
    while bandera and not len(lista) == 0:
        #menu
        print("-----------------------------------------------")
        print("[1] Grafico promedio de temperaturas por año.\n[2] Grafico promedio de humedad por año.")
        print("[3] Milímetros máximos de lluvia de los últimos 5 años.\n[4] Temperatura máxima de los últimos 5 años. \n[5] Salir.")
        print("-----------------------------------------------")
        menu = input("\nSelecciona una opcion (1-2-3-4-5): ")
        print()
        while menu not in ["1","2","3","4","5"]:
            menu = input("\nSelecciona una opcion válida (1-2-3-4-5): ")
            print()
        
        if menu == "1":
            y = promedios[0]
            x = [str(AÑO_CORRIENTE-4), str(AÑO_CORRIENTE-3), str(AÑO_CORRIENTE-2), str(AÑO_CORRIENTE-1), str(AÑO_CORRIENTE)] # Es necesario transformarlos en string
            y2 = promedios[1]                                                                                                # para que no salgan coordenadas decimales
            
            plt.plot(x, y, "r")                                          # Dibujo de los valores
            plt.plot(x, y2, "b")
            plt.xlabel("Año")                                            # Titulo eje X
            plt.ylabel("ºC")                                             # Titulo eje Y
            plt.title("Promedio de temperatura maxima y minima por año") # Titulo grafico
            plt.show()                                                   # Impresion del grafico

        elif menu =="2":
            y = promedios[2]
            x = [str(AÑO_CORRIENTE-4), str(AÑO_CORRIENTE-3), str(AÑO_CORRIENTE-2), str(AÑO_CORRIENTE-1), str(AÑO_CORRIENTE)]
            plt.plot(x, y, "r")
            plt.xlabel("Año")
            plt.ylabel("Humedad relativa (fraccion)")
            plt.title("Promedio de humedad por año")
            plt.show()
    
        elif menu == "3":
            for año in range(5):
                
                maxLluvia = (max(dataPorAño[3][año]))
                 
                if año == 0:
                    añoLlave = "4 años"
                    añoDato = AÑO_CORRIENTE-4
                
                elif año == 1:
                    añoLlave = "3 años"
                    añoDato = AÑO_CORRIENTE-3
                
                elif año == 2:
                    añoLlave = "2 años"
                    añoDato = AÑO_CORRIENTE-2
                
                elif año == 3:
                    añoLlave = "1 año"
                    añoDato = AÑO_CORRIENTE-1
                
                elif año == 4:
                    añoLlave = "Presente"
                    añoDato = AÑO_CORRIENTE
                
                if len(data[añoLlave]) == 0:
                    print(f'No hay datos del año {str(añoDato)}\n')
                
                else:
                    for dia in data[añoLlave]:
                            if float(dia['Precipitaciones']) == maxLluvia:
                                print("El dia " + dia["Fecha"] + " en las coordenadas: " + dia["Longitud"] + ", " + dia["Latitud"])
                                print("Se registraron " + dia["Precipitaciones"] + " milimetros de lluvia.\n")
        
        elif menu == "4":         
            for año in range(5):
                
                maxTemp = max(dataPorAño[0][año])                
                
                if año == 0:
                    añoLlave = "4 años"
                    añoDato = AÑO_CORRIENTE-4
                
                elif año == 1:
                    añoLlave = "3 años"
                    añoDato = AÑO_CORRIENTE-3
                
                elif año == 2:
                    añoLlave = "2 años"
                    añoDato = AÑO_CORRIENTE-2
                
                elif año == 3:
                    añoLlave = "1 año"
                    añoDato = AÑO_CORRIENTE-1
                
                elif año == 4:
                    añoLlave = "Presente"
                    añoDato = AÑO_CORRIENTE
                
                if len(data[añoLlave]) == 0:
                    print(f'No hay datos del año {str(añoDato)}\n')
                
                else:
                    for dia in data[añoLlave]:
                        if float(dia['Max t']) == maxTemp:
                            print("El dia " + dia["Fecha"] + " en las coordenadas: " + dia["Longitud"] + ", " + dia["Latitud"])
                            print("Se registraron " + dia["Max t"] + " grados centigrados.\n")

        elif menu == "5":
            bandera = False