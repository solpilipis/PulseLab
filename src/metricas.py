# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:46:54 2026

@author: 54115
"""

def verificar (num):
    try:
        float(num)
        return True
    except (ValueError, TypeError):
        return False


def calcular_promedio_señal (lista):
    """
    calcula el promedio de las señlaes ingresadas en la lista 
    
    Parameters
    ----------
    lista : list
        señaes recolectadas en la lista

    Returns
    -------
    promedio : float
        promedio de todos los valores de la lista 

    """
    
    
    suma = 0 
    cantidad = 0 
    for elemento in lista:
        veri = verificar (elemento)
        if veri == True: 
            suma += elemento 
            cantidad += 1   
    promedio = suma / cantidad
    return promedio 
        
        
def calcular_maximo_señal (lista):
    """
    identifica el valor maximo de la lista 
    
    Parameters
    ----------
    lista : list
        lista de señales recolectadas.

    Returns
    -------
    maxi : float
        valor maximo de la lista.

    """
    maxi = 0 
    for elemento in lista: 
        veri = verificar(elemento)
        if veri == True: 
            if elemento > maxi: 
                maxi = elemento 
    return maxi
            
            

def calcular_frecuencia_cardiaca(picos: list) -> float: 
    
    """
    Calcula la frecuencia cardíaca a partir de los tiempos de los picos.

    Parámetros
        
    ----------
    
    - picos: list de floats. Lista de los tiempos en los que ocurre cada pico

    Retorna
        
    -------- 
    
    - frecuencia: float. Frecuencia cardíaca de la persona
    
    Errores 
    -------

    - ValueError: si la lista contiene menos de 2 picos o si todos los picos corresponden al mismo tiempo 
    
    """

    if len(picos) < 2: 
        
        raise ValueError("Se necesita un minimo de 2 picos para calcular la frecuencia cardíaca")

    tiempo_total = picos[-1] - picos[0]

    if tiempo_total == 0: 
        
        raise ValueError("Los picos ingresados corresponden a un único tiempo, no se puede calcular la frecuencia")

    cantidad_picos = len(picos)

    frecuencia = (cantidad_picos / tiempo_total) * 60

    return frecuencia 

from src.utils_ecg import detectar_picos_qrs

def calcular_fc_desde_datos(datos): 
    
    """  
    Calcula la frecuencia cardíaca a partir de una lista de datos de senal. 
    
    Parámetros 
    ---------- 
    
    - datos: list. Lista de diccionarios 
    
    Retorna 
    ------- 
    
    - float. Frecuencia cardíaca a través de picos calculados. 
    
    """
    tiempos = []
    senal = []
    for d in datos:
        tiempos.append(d["tiempo"])
        senal.append(d["valor"])
    picos = detectar_picos_qrs(tiempos, senal)
    return calcular_frecuencia_cardiaca(picos)
