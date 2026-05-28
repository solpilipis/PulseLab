import os
import matplotlib.pyplot as plt

from src.carga_datos import cargar_datos
#from src.validar import "las funciones"
from src.procesamiento_datos import filtrar_por_participante
from src.metricas import calcular_promedio_señal, calcular_maximo_señal, calcular_fc_desde_datos
from src.validar import validar_tiempo_creciente

os.makedirs("graficos", exist_ok=True)

try:
    datos = cargar_datos("datos/PulseLab_mock_data.csv")
    
    print("Columnas en el CSV:", datos.columns)
    
    participantes = datos["id_participante"].unique()
    
    for participante in participantes:
        
        datos_filtrados = filtrar_por_participante(datos, participante)
        
        tiempos = datos_filtrados["tiempo"]
        señal = datos_filtrados["valor"]

        validar_tiempo_creciente(tiempos)

        promedio = calcular_promedio_señal(señal)
        maximo = calcular_maximo_señal(señal)

        frecuencia = calcular_fc_desde_datos(datos_filtrados)

        print(f"Participante: {participante}")
        print(f"Promedio señal: {promedio}")
        print(f"Maximo señal: {maximo}")
        print(f"Frecuencia cardiaca: {frecuencia}")
        
        plt.figure(figsize=(10, 4))
        plt.plot(tiempos, señal)
        plt.title(f"ECG Participante {participante}")
        plt.xlabel("Tiempo")
        plt.ylabel("Señal")
        ruta = f"graficos/participante_{participante}.png"
        plt.savefig(ruta)
        plt.close()
        
except FileNotFoundError:
    print("No se encontro el archivo")
    
except KeyError:
    print("Faltan columnas o datos")
    
except ValueError as e:
    print(f"Error: {e}")
    
except Exception as e:
    print(f"Ocurrio un error inesperado: {e}")
