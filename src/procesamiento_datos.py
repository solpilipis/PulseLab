def filtrar_por_participante(datos, id_participante):
    """
    Qué hace la función:
    Busca y devuelve el subconjunto de datos de un participante en específico.

    Parámetros:
    datos (DataFrame): El DataFrame que contiene los datos de todos los participantes.
    id_participante (int): El número de id del participante a filtrar.

    Retorna:
    DataFrame: Los datos del participante requerido.
    
    Raises:
    KeyError 
    TypeError
    """ 
    try:
        datos_filtrados = datos[datos["id_participante"] == id_participante]
        return datos_filtrados
    
    except KeyError:
        raise KeyError
        
    except TypeError:
        raise TypeError