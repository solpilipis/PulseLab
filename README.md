# PulseLab
El sistema hace lo siguiente:
1. Lee datos desde un archivo
2. Transforma cada línea en un registro
3. Almacena los datos
4. Extrae la señal y el tiempo
5. Detecta picos
6. Calcula métricas básicas

Errores y Validaciones

cargar_datos(ruta): 

No necesita manejar ningun error ya que se manejan en parsear_linea(linea) o en el main.py.

main.py: 

Puede no existir o no hallarse el archivo por eso se maneja con un except FileNotFoundError.
         
Puede haber un error en la conversion de datos por eso se maneja con un except ValueError.
         
Puede haber un error en los tipos de datos por eso se maneja con un except TypeError.
         
Se puede producir una division por cero cuando se calculan metricas, por eso se maneja con un except ZeroDivisionError.

metricas.py: 

puede cargarse un valor no numerico, como por ejmeplo que se ecriba "uno" y no "1", esto se maneja con la funcion verificar. dentro de la funcion se maneja con un except ValueError, TypeError


Participantes:

Clara Baietti

Micaela Cohen

Sol Pilipis

Guadalupe Silva
