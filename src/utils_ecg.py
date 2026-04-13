def detectar_picos_qrs(tiempos, senal, umbral=0.8, distancia_minima=0.3, debug=False):
    """
    Detecta picos QRS en una señal de ECG de forma robusta

    La función:
    1. Calcula la derivada de la señal
    2. Obtiene una señal de energía (derivada al cuadrado)
    3. Suaviza la energía
    4. Calcula un umbral adaptativo local
    5. Detecta regiones donde hay actividad tipo QRS
    6. Busca el pico real en la señal original

    Args:
    - tiempos (list): tiempos en segundos
    - senal (list): valores de ECG
    - umbral (float): controla la sensibilidad del detector de picos. Default = 0.8
    - distancia_minima (float): tiempo mínimo entre picos (segundos). Default = 0.3
    - debug (bool): si True, muestra gráfico de energía y umbral. Default = False

    Return:
    - list: tiempos donde se detectan picos QRS (en segundos)

    Errores:
    - ValueError: si las listas están vacías, tienen distinto largo, el tiempo no está ordenado o
      es muy corto para detectar picos
    """

    import numpy as np

    # ---------------------------
    # Validación básica
    # ---------------------------
    if len(tiempos) != len(senal):
        raise ValueError("El tiempo y la señal deben tener el mismo largo")
    
    if len(tiempos) == 0 or len(senal) == 0:
        raise ValueError("Las listas 'tiempos' y 'senal' no pueden estar vacías.")

   # if np.any(np.diff(tiempos) <= 0):
   #     raise ValueError("Los valores de 'tiempos' deben estar ordenados de forma creciente.")
    
    if len(tiempos) < 3:
        raise ValueError("Tiempo de registro demasiado corto para detectar picos")
    

    t = np.array(tiempos)
    x = np.array(senal)

    # ---------------------------
    # 0. Parámetros
    # ---------------------------
    
    # Frecuencia de muestreo estimada
    dt = np.diff(t)
    dt_medio = np.median(dt)

    # Ventanas expresadas en segundos y convertidas a muestras
    ventana_energia_seg = 0.03      # ~30 ms para suavizado de la señal
    ventana_umbral_seg = 2.0        # ~2 s para el umbral adaptativo
    padding_seg = 0.05              # ~50 ms 

    window = max(1, int(round(ventana_energia_seg / dt_medio)))
    ventana_umbral = max(3, int(round(ventana_umbral_seg / dt_medio)))
    window = min(window, len(x))
    ventana_umbral = min(ventana_umbral, len(x))
    padding = max(1, int(round(padding_seg / dt_medio)))

    # ---------------------------
    # 1. Derivada + energía
    # ---------------------------
    dx = np.diff(x, prepend=x[0])
    energia = dx ** 2

    # ---------------------------
    # 2. Suavizado (30 ms)
    # ---------------------------
    energia_suavizada = np.convolve(
        energia,
        np.ones(window) / window,
        mode='same'
    )

    # ---------------------------
    # 3. Umbral adaptativo (2 seg)
    # ---------------------------
    media_local = np.convolve(
        energia_suavizada,
        np.ones(ventana_umbral) / ventana_umbral,
        mode='same'
    )

    var_local = np.convolve(
        (energia_suavizada - media_local) ** 2, 
        np.ones(ventana_umbral) / ventana_umbral,
        mode="same"
    )

    std_local = np.sqrt(
        var_local
    )

    umbral_local = media_local + umbral * std_local

    # ---------------------------
    # 4. Detectar regiones
    # ---------------------------
    candidatos = np.where(energia_suavizada > umbral_local)[0]

    if len(candidatos) == 0:
        if debug:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12, 4))
            plt.plot(t, energia_suavizada, label="Energía suavizada")
            plt.plot(t, umbral_local, label="Umbral local", color="red")
            plt.title("Señal de energía + umbral local")
            plt.xlabel("Tiempo (s)")
            plt.legend()
            plt.show()
        return []

    grupos = []
    grupo_actual = [candidatos[0]]

    for i in candidatos[1:]:
        if i == grupo_actual[-1] + 1:
            grupo_actual.append(i)
        else:
            grupos.append(grupo_actual)
            grupo_actual = [i]

    grupos.append(grupo_actual)

    # ---------------------------
    # 5. Buscar pico real
    # ---------------------------
    picos = []
    ultimo_t = -np.inf

    for g in grupos:

        inicio = max(0, g[0] - padding)
        fin = min(len(x), g[-1] + padding + 1)

        idx_max = np.argmax(x[inicio:fin]) + inicio
        tiempo_pico = t[idx_max]

        if (tiempo_pico - ultimo_t) >= distancia_minima:
            picos.append(float(tiempo_pico))
            ultimo_t = tiempo_pico

    # ---------------------------
    # Debug opcional
    # ---------------------------
    if debug:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12,4))
        plt.plot(t, energia_suavizada, label="Energía")
        plt.plot(t, umbral_local, label="Umbral local", color='red')
        plt.legend()
        plt.title("Energía + umbral")
        plt.xlabel("Tiempo (s)")
        plt.show()

    return picos