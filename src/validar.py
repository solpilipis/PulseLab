# funciones para validar

#funciones valor (señal ECG) numérico y dentro de rango (min, max)

def validar_valores_ECG (valores, maxi, mini):
    """
    
    recibe una lista de valores y revisa si son valores nuemricos y si estan dentro de l rango 

    Parameters
    ----------
    valores : list
        lista de valores del ECG .
    maxi : float
        valor maixmo del rango .
    mini : float
        valor minimo del ranog.

    Raises
    ------
    ValueError
        .si cargan una lista de valores que etsa vacia
    
        si el valor esta fuera de rango .
        
    TypeError
        si el valor no es un numero o si no se puede convertir, por ejemplo si ingresan "a".

    Returns
    -------
    valores_validos : list
        son los valores que son numeros y estan dentro del rango .

    """

    if type(valores) != list:
        valores = [valores]
    
    if len(valores) == 0:
        raise ValueError ("la lista de valores no puede estar vacia")
   
    valores_numericos = [
        ]
    
    for valor in valores: 
        #valido que sea numerico 
        # si esta en formato correcto continua la validacion 
        if isinstance(valor, (int, float)):
            valores_numericos.append(valor)
            continue
        #si no es valor numerico entra en el elif 
        #si es str valido que sea un numero, sino hago un raise 
        elif isinstance(valor, str):
            try:
                valor_numerico = float(valor) #lo convierto para despues ver si esta dentro del rango 
                valores_numericos.append(valor_numerico)
            except ValueError:
                raise TypeError("el dato", valor, "no se un numero")

            
            
    #me fijo que este adentro del rango maxi - mini
    valores_validos =[]
    
    for valoor in valores_numericos: 
        if valoor < mini or valoor > maxi:
            raise ValueError ("valor fuera de rango", valoor)
        else:
            valores_validos.append (valoor)
            
    
    return valores_validos[0]

def validar_fase(fase):  
    
    ''' 
    Valida que el valor de la fase sea correcto, sea "baseline" o "tarea".

    Parámetros
    ----------
    
    fase: str 
        La fase indicada en el archivo

    Retorna
    --------
    
    str: La fase en minúsculas y sin espacios

    Raises:
   
    TypeError: si el valor no es un string
    ValueError: si la fase no es "baseline" o "tarea"
    '''

    if not isinstance(fase, str): 
        
        raise TypeError("La fase debe ser un string.") 
        
    fase = fase.strip().lower()

    if fase not in ["baseline", "tarea"]: 
        
        raise ValueError("La fase es inválida.")

    return fase

def validar_condicion(condicion):
    """
    Chequea que las condiciones sean las correctas.

    Parameters
    ----------
    condicion : str
        la condicion indicada en el archivo

    Raises
    ------
    ValueError: si la condicion no esta en el archivo.

    Returns
    -------
    condicion : si no hay error, devuelve la condicion original

    """
    opciones_validas = ["competencia", "cooperacion", "cooperación"]
    
    condicion = condicion.strip().lower()

    encontrado = False
    for opcion in opciones_validas:
        if condicion == opcion:
            encontrado = True
    
    if encontrado == False:
        raise ValueError("La condición no es válida.")
        
    return condicion


def validar_tiempo_creciente(tiempos):
    """
    chequea que los tiempos sean crecientes
    
    Parameters
    ----------
   tiempos : pandas.series
       serie de tiempo s

    Raises
    ------
    ValueError: Si los timepos no son crecientes

    """
    for i in range (len(tiempos) - 1 ):
        if tiempos.iloc[i] >= tiempos.iloc[i+1]:
            raise ValueError("los tiempos no son crecientes")

