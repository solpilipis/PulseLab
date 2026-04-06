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
    partes = linea.split(",")

    id_entero = int(partes[0])
    tiempo = float(partes[1])
    ecg = float(partes[2])
    fase = partes[3]
    condicion = partes[4].strip()
    hit = int(partes[5])
    
    return [id_entero, tiempo, ecg, fase, condicion, hit]

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
    diccionario = {}
    with open(ruta) as archivo:
        archivo.readline()
        #salteamos los titulos
        for linea in archivo:
            datos = parsear_linea(linea)
            id_participante = datos[0]
            if id_participante not in diccionario:
                diccionario[id_participante] = {
                    "id_participante": id_participante,
                    "tiempo": [],
                    "valor": [],
                    "fase": [],
                    "condicion_experimental": [],
                    "hit": []}
            diccionario[id_participante]["tiempo"].append(datos[1])
            diccionario[id_participante]["valor"].append(datos[2])
            diccionario[id_participante]["fase"].append(datos[3])
            diccionario[id_participante]["condicion_experimental"].append(datos[4])
            diccionario[id_participante]["hit"].append(datos[5])
    lista_final = []
    for participante in diccionario.values():
        lista_final.append(participante)
    return lista_final