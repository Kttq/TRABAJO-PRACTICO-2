import jsonMain


def mostrarAlertas(lista):
    i = 0
    print("\nLas alertas a nivel nacional son...")
    for alerta in lista:
        print(f"\nALERTA #{i+1}\n")
        for atributo in lista[i]:
            print(atributo,":",lista[i][atributo])
        i += 1

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
            print("Nada")
            
        elif Seleccion == "2":
            URL = "https://ws.smn.gob.ar/alerts/type/AL"
            alertas = jsonMain.formatoAlertas(URL)
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
    