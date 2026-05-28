import pandas as pd


    
def cargar_datos(ruta):
    """
    Qué hace la función:
    Abre y carga el archivo CSV y devuelve un DataFrame.

    Parámetros:
    ruta: (str) La dirección del archivo.

    Retorna:
    pandas.DataFrame: el DataFrame dcon los datos del archivo cargados.
    """
    nombres = ["id_participante", "tiempo", "valor", "estado", "fase", "valido"]
    
    datos = pd.read_csv(ruta, names=nombres)
    return datos