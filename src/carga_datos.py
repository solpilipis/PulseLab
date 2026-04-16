def parsear_linea(linea: str):
    """
    Qué hace la función:
    toma una línea de str de un archivo y la convierte en una lista procesada

    Parámetros:
    linea (str): una cadena de texto con valores separados por comas

    Retorna:
    list: una lista con los datos convertidos:
          [ID (int), Tiempo (float), ECG (float), Fase (str), Condicion (str)]
    """
    try:
        partes = linea.split(",")

        id_entero = int(partes[0])
        tiempo = float(partes[1])
        ecg = float(partes[2])
        fase = partes[3]
        condicion = partes[4].strip()
        if partes[5].strip().lower() == "true":
            hit = True
        else:
            hit = False
    
        return [id_entero, tiempo, ecg, fase, condicion, hit]

    except ValueError:
        raise ValueError
    except IndexError:
        raise IndexError

    
def cargar_datos(ruta):
    """
    Qué hace la función:
    Abre el archivo, procesa la información línea por línea
    y agrupa los datos en diccionarios por participante.

    Parámetros:
    ruta: La dirección del archivo.

    Retorna:
    lista_final: list: Lista de diccionarios por participante.
    """
    lista_final = []
    with open(ruta) as archivo:
        for linea in archivo:
            datos = parsear_linea(linea)
            id_actual = datos[0]
            
            diccionario_existente = None
            for diccionario in lista_final:
                if diccionario["id_participante"] == id_actual:
                    diccionario_existente = diccionario
                    break
            if diccionario_existente is None:
                nuevo_diccionario = {
                "id_participante": id_actual,
                "tiempo": [datos[1]],
                "valor": [datos[2]],
                "fase": [datos[3]],
                "condicion_experimental": [datos[4]],
                "hit": [datos[5]]}
                lista_final.append(nuevo_diccionario)
            else:
                diccionario_existente["tiempo"].append(datos[1])
                diccionario_existente["valor"].append(datos[2])
                diccionario_existente["fase"].append(datos[3])
                diccionario_existente["condicion_experimental"].append(datos[4])
                diccionario_existente["hit"].append(datos[5])

    return lista_final