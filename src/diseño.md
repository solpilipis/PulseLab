# **Diseño del Sistema: PulseLab**

Este documento contiene la especificación completa de diseño, arquitectura y contratos lógicos para el sistema de análisis de señales electrocardiográficas (ECG) denominado **PulseLab**. Este documento sirve como mapa de referencia técnica para asegurar la integración correcta entre los componentes modulares del backend y la interfaz gráfica web interactiva desarrollada en Streamlit.

## **1\. Estructura del Repositorio y Directorios**

Para cumplir con los requisitos establecidos por la cátedra y garantizar un entorno mantenible, la distribución de los componentes del proyecto se organiza bajo la siguiente jerarquía física:

`PulseLab/`  
`├── datos/`  
`│   └── PulseLab_mock_data.csv       # Dataset de prueba con registros de señales ECG`  
`├── diagramas/`  
`│   └── diagramas_flujo/             # Diagramas lógicos del sistema y sus funciones`  
`├── graficos/`  
`│   └── participante_X.png           # Figuras fijas exportadas por los análisis visuales`  
`├── src/`  
`│   ├── carga_datos.py               # Lógica de lectura y estructuración con Pandas`  
`│   ├── procesamiento_datos.py       # Segmentación y filtrado de datos por participante`  
`│   ├── validar.py                   # Programación defensiva y atajado de excepciones`  
`│   ├── utils_ecg.py                 # Algoritmo matemático de detección de picos QRS`  
`│   ├── metricas.py                  # Computación de indicadores clave (KPIs) de salud`  
`│   └── diseño.md                    # Este archivo de documentación técnica`  
`├── app.py                           # Interfaz web interactiva del Dashboard (Streamlit)`  
`├── main.py                          # Orquestador original para ejecución por consola`  
`├── prompts_dashboard.txt            # Bitácora de Ingeniería de Prompts con la IA`  
`└── README.md                        # Guía de usuario e instrucciones de despliegue`

## **2\. Resumen de Responsabilidades por Módulo**

El sistema se rige bajo el principio de separación total de responsabilidades. Ninguna función interna del backend realiza operaciones de entrada/salida (como print o input), delegando todo el manejo visual y control de excepciones al script orquestador correspondiente (main.py en consola o app.py en entorno web).

| Módulo | Responsabilidad Principal | Estructura de Datos Relacionada   |
| :---- | :---- | :---- |
| **src/carga\_datos.py** | Lectura automatizada de archivos CSV estructurados. | pandas.DataFrame |
| **src/procesamiento\_datos.py** | Filtrado, transformaciones y segmentación de series. | pandas.DataFrame / pandas.Series |
| **src/validar.py** | Validaciones defensivas de rangos, consistencia temporal y tipos. | Lanzamiento de excepciones (ValueError, TypeError) |
| **src/utils\_ecg.py** | Procesamiento numérico y algorítmico de la onda de ECG (Derivada y Energía). | numpy.ndarray / List\[float\] |
| **src/metricas.py** | Cálculo matemático de la frecuencia cardíaca (BPM) y resúmenes. | Float / Métricas numéricas individuales |

## **3\. Especificación Detallada de Funciones y Contratos (Docstrings)**

### **Módulo: src/carga\_datos.py**

* **cargar\_datos(ruta)**  
  * *Descripción:* Carga de forma segura el archivo CSV con los datos crudos del laboratorio y formatea la cabecera con las columnas estandarizadas.  
  * *Parámetros:* ruta (str) \- Dirección física o relativa del archivo de datos.  
  * *Retorna:* pandas.DataFrame \- Tabla indexada con las columnas básicas: id\_participante, tiempo, valor, estado, fase, valido.

### **Módulo: src/procesamiento\_datos.py**

* **filtrar\_por\_participante(datos, id\_participante)**  
  * *Descripción:* Aisla la información conductual y fisiológica correspondiente a un único sujeto del estudio.  
  * *Parámetros:*  
    * datos (pandas.DataFrame) \- El conjunto de datos completo cargado en memoria.  
    * id\_participante (int) \- El identificador único del sujeto a buscar.  
  * *Retorna:* pandas.DataFrame \- Subconjunto filtrado con los registros exclusivos del participante indicado.

### **Módulo: src/validar.py**

* **validar\_tiempo\_creciente(tiempos)**  
  * *Descripción:* Inspecciona que la serie temporal avance de manera estrictamente incremental. Requisito crítico para el análisis de frecuencia cardíaca.  
  * *Parámetros:* tiempos (pandas.Series) \- Secuencia cronológica de la señal de ECG.  
  * *Lanza:* ValueError si se detecta que un registro temporal es menor o igual al inmediato anterior.  
* **validar\_valores\_ECG(valores, maxi, mini)**  
  * *Descripción:* Verifica que los voltajes medidos de la señal se mantengan dentro de los umbrales fisiológicos establecidos.  
  * *Lanza:* ValueError si la lista está vacía o si algún elemento excede los límites, y TypeError si se proveen caracteres no numéricos.

### **Módulo: src/metricas.py**

* **calcular\_promedio\_señal(señal)** y **calcular\_maximo\_señal(señal)**  
  * *Descripción:* Extraen estadísticas descriptivas rápidas de la amplitud de la señal.  
  * *Retorna:* float con el valor promediado o el valor máximo de la onda respectivamente.  
* **calcular\_fc\_desde\_datos(datos)**  
  * *Descripción:* Actúa como puente integrador de alto nivel; toma las columnas de tiempo y amplitud, invoca recursivamente al detector de picos QRS y calcula la frecuencia cardíaca final en pulsaciones por minuto (BPM).  
  * *Parámetros:* datos (pandas.DataFrame) \- Tabla limpia correspondiente a un participante.  
  * *Retorna:* float con la frecuencia cardíaca calculada.

## **4\. Requisitos para la Interfaz de Usuario (app.py)**

La capa de presentación web, construida con la librería Streamlit, debe acoplarse sobre este backend respetando la siguiente secuencia lógica de interacción:

1. **Carga Dinámica:** Implementar st.file\_uploader para capturar el archivo CSV cargado por el usuario.  
2. **Control Defensivo:** Envolver las llamadas de inicialización en bloques try-except ValueError. Si el backend arroja un error de consistencia, la app debe bloquearse inmediatamente y mostrar una alerta llamativa mediante st.error.  
3. **Métricas en Tarjetas:** Presentar los indicadores clave del sujeto (Promedio, Máximo y Frecuencia Cardíaca en BPM) distribuidos de forma elegante utilizando componentes de tipo st.metric.  
4. **Visualización de Curvas:** Renderizar los gráficos de la señal ECG en el panel principal utilizando el contenedor nativo st.pyplot.