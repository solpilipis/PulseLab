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
            
            
lista = [1,1,2,6,5,4,8,2,37,9]

maximo = calcular_maximo_señal (lista)
print (maximo )