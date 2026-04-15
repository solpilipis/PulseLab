def filtrar_por_participante(datos, id_participante):
    """
    Qué hace la función:
    Busca y devueleve el diccionario que contiene los datos de un participante en específico.

    Parámetros:
    datos (list): La lista que contiene los diccionarios de todos los participantes.
    id_participante (int): El número de id del participante a filtrar.

    Retorna:
    dict: El diccionario con los datos de participante requerido.
    """
    try:  
        for participante in datos:
            if participante["id_participante"] == id_participante:
                return participante
        return None
    except (KeyError, TypeError):
        print("Error")
        return None