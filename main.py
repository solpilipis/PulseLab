from src.carga_datos import cargar_datos
from src.procesamiento_datos import filtrar_por_participante
from src.metricas import calcular_promedio_señal, calcular_maximo_señal, calcular_fc_desde_datos
try:
    datos_participantes = cargar_datos("datos/PulseLab_mock_data.csv")
    
except FileNotFoundError:  

    print("No se pudo encontrar el archivo") 
    
else:
    
    for participante in datos_participantes: 
    
        try: 
        
            id_participante = participante["id_participante"]
        
            datos_filtrados = filtrar_por_participante(datos_participantes, id_participante)
        
            tiempos = datos_filtrados["tiempo"]
            señal = datos_filtrados["valor"]
        
            promedio = calcular_promedio_señal(señal)
            maximo = calcular_maximo_señal(señal)
            
            datos_para_metricas = []
            cantidad_datos = len(tiempos)
        
            for i in range(cantidad_datos):
                tiempo_actual = tiempos[i]
                señal_actual = señal[i]
                punto = {"tiempo": tiempo_actual, "valor": señal_actual}
                datos_para_metricas.append(punto)
        
            frecuencia = calcular_fc_desde_datos(datos_para_metricas)
        
            print(f"Promedio de señal: {promedio}")
            print(f"Máximo de señal: {maximo}")
            print(f"Participante: {id_participante}")
            print(f"Frecuencia Cardíaca: {frecuencia}")  
            
        except KeyError:
            print("Error: Hay información incompleta de un participante.")
    
        except ValueError as e:
            print(f"Error: {e}")
    
        except ZeroDivisionError:
            print("Error: Se intentó dividir por 0.")
    
        except TypeError as e:
            print(f"Error: {e}")

