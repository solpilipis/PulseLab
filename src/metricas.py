from src.utils_ecg import detectar_picos_qrs 

def calcular_promedio_señal(señal):
    """
    calcula el promedio de las señales ingresadas
    
    Parameters
    ----------
    señal: pandas.Series. Los valores de las senales. 

    Returns
    -------
    promedio : float
        promedio de la señal

    """
    return señal.mean()
        
        
def calcular_maximo_señal (señal):
    """
    Identifica el maximo de una senal
    
    Parameters
    ----------
    señal: pandas.Series. Valores de la señal.

    Returns
    -------
    float
        valor maximo de la señal

    """
    return señal.max()
            

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


def calcular_fc_desde_datos(datos): 
    
    """  
    Calcula la frecuencia cardíaca a partir de un dataframe.
    
    Parámetros 
    ---------- 
    
    - datos: pandas.DataFrame. dataframe con los valores de la senal.
    
    Retorna 
    ------- 
    
    - float. Frecuencia cardíaca.
    
    """
    tiempos = datos["tiempo"].tolist()
    senal = datos["valor"].tolist()

    picos = detectar_picos_qrs(tiempos, senal)

    return calcular_frecuencia_cardiaca(picos)
