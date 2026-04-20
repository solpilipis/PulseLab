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
    if len(valores) == 0:
        raise ValueError ("la lista de valores no puede etsar vacia")
   
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
        elif isinstance(valor, str) and valor.isdigit():
            valor_numerico = float(valor) #lo convierto para despues ver si esta dentro del rango 
            valores_numericos.append(valor_numerico)
        #como no es niun valor numerico ni puede convertirse lanzo un raise
        else:
            raise TypeError ("el dato", valor, " no es un numero")
            
            
    #me fijo que este adentro del rango maxi - mini
    valores_validos =[]
    
    for valoor in valores_numericos: 
        if valoor < mini or valoor > maxi:
            raise ValueError ("valor fuera de rango", valoor)
        else:
            valores_numericos.append (valoor)
            
    
    return valores_validos 

