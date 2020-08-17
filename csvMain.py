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

def filtroCategoria(diccionario):
    """Funcion que retorna una lista de datos tras filtrar por año los datos recibidos de un diccionario"""
    maxtemp = [[],[],[],[],[]]  
    mintemp = [[],[],[],[],[]]  #Separo listas en "ranuras", para identificar cada año desde los 4 años anteriores a año presente.
    humedad = [[],[],[],[],[]]
    lluvia = [[],[],[],[],[]]

    for año in diccionario:

        slot = int(año[0:1])

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
    años = {"0 años": [], "1 años": [], "2 años": [], "3 años": [], "4 años": []}
    
    for i in lista:
        
        fechaLista = i["Fecha"].split('/')
        año = fechaLista[2]
        
        if año.isnumeric():
            
            añoIndice = año_corriente - int(año)        
                
            diccionario = (str(añoIndice) + " años")
                
            if diccionario in años:
            
                años[diccionario].append(i)
        
        else:
            print("Recuerde introducir fechas numéricas. ")
    
    return años

def introducirArchivo():
    '''Función que le permite al usuario ingresar un archivo CSV'''
    
    print("El archivo debe ser de extension CSV y respetar la forma:")
    print('[Fecha, Longitud, Latitud, Elevacion, Max. Temp, Min. Temp, Precipitaciones, Viento, Humedad, Solar]\n')
    print("¿Dónde se encuentra el archivo?\n 1)Carpeta del programa\n 2)Otra carpeta\n")
    
    ubicacionArchivo = input("Seleccione la opción que desea : ")
    
    bandera = True
    
    while bandera:
        
        if ubicacionArchivo == '1':
            nombreArchivo = input("Ingrese el nombre del archivo (sin extension): ")
            nombreArchivo = nombreArchivo + ".csv"
            bandera = False
        
        elif ubicacionArchivo == '2':
        
            ruta = input("Ingrese la ruta (completa) de la carpeta donde se encuentra de el archivo: ")
            nombreArchivo = input("Ingrese el nombre del archivo (sin extension): ")
            nombreArchivo = nombreArchivo + ".csv"
            
            nombreArchivo = os.path.join(ruta, nombreArchivo)
            bandera = False
        else:
            ubicacionArchivo = input("Seleccione una opción correcta (1-2): ")
    
    return nombreArchivo

def csvaLista():
    """Funcion que con un archivo CSV dado, lo transforma en una lista en la cual se puede manipular su informacion
    Debe respetar la forma: ["Date", "Longitude", "Latitude", "Elevation", "Max Temperature", "Min Temperature", "Precipitation", "Wind", "Relative Humidity", "Solar"]   
    """
    data_lista = []
    
    archivo_csv = introducirArchivo()
    
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
            exito = True
        
        except:
            print("\nE R R O R: No se pudo abrir el archivo .CSV (Quizas no esta en la carpeta)\n")
            bandera = False
            exito = False
        
        return data_lista, exito

def menu():
    """Menu"""
    AÑO_CORRIENTE = calcularAño()
    
    lista, exito = csvaLista()
    
    bandera = True

    if exito:
        data = filtroAño(lista, AÑO_CORRIENTE)
        dataPorAño = filtroCategoria(data)
        promedios = calcularPromedios(dataPorAño)

        
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
                y = (promedios[0]) # Doy vuelta para mostrar linea cronologica (recuerdo que promedios[0][0] pertenece al año corriente)
                y.reverse() # TEMP MAX
                
                x = [str(AÑO_CORRIENTE-4), str(AÑO_CORRIENTE-3), str(AÑO_CORRIENTE-2), str(AÑO_CORRIENTE-1), str(AÑO_CORRIENTE)] # Es necesario transformarlos en string
                
                y2 = (promedios[1])                                                                                               # para que no salgan coordenadas decimales
                y2.reverse() # TEMP MIN
                
                plt.plot(x, y, "r")                                          # Dibujo de los valores
                plt.plot(x, y2, "b")
                
                plt.xlabel("Año")                                            # Titulo eje X
                plt.ylabel("ºC")                                             # Titulo eje Y
                
                plt.title("Promedio de temperatura maxima y minima por año") # Titulo grafico
                
                plt.show()                                                   # Impresion del grafico

            elif menu =="2":
                y = promedios[2]
                y.reverse()
                
                x = [str(AÑO_CORRIENTE-4), str(AÑO_CORRIENTE-3), str(AÑO_CORRIENTE-2), str(AÑO_CORRIENTE-1), str(AÑO_CORRIENTE)]
                
                plt.plot(x, y, "r")
                
                plt.xlabel("Año")
                plt.ylabel("Humedad relativa (fraccion)")
                
                plt.title("Promedio de humedad por año")
                
                plt.show()
        
            elif menu == "3":
                for año in range(5):
                    
                    maxLluvia = (max(dataPorAño[3][año]))
                    
                    añoLlave = str(año)+" años"
                    añoDato = AÑO_CORRIENTE - año
                    
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
                    
                    añoLlave = str(año)+" años"
                    añoDato = AÑO_CORRIENTE - año
                    
                    if len(data[añoLlave]) == 0:
                        print(f'No hay datos del año {str(añoDato)}\n')
                    
                    else:
                        for dia in data[añoLlave]:
                            if float(dia['Max t']) == maxTemp:
                                print("El dia " + dia["Fecha"] + " en las coordenadas: " + dia["Longitud"] + ", " + dia["Latitud"])
                                print("Se registraron " + dia["Max t"] + " grados centigrados.\n")

            elif menu == "5":
                bandera = False
    else:
        print("\nE R R O R: No se pudo leer el archivo correctamente. Verifique datos.")