import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

from src.carga_datos import cargar_datos
from src.procesamiento_datos import filtrar_por_participante
from src.validar import validar_tiempo_creciente, validar_valores_ECG
from src.metricas import calcular_promedio_señal, calcular_maximo_señal, calcular_fc_desde_datos

st.set_page_config(page_title="PulseLab Dashboard", page_icon="🫀", layout="wide")

st.title("PulseLab: Dashboard de Señales ECG 🫀")
st.markdown("Sistema integral de carga, procesamiento, validación y visualización de datos electrocardiográficos.")
st.divider()

st.subheader("Carga de Datos")
archivo_subido = st.file_uploader("Sube el archivo de registros del laboratorio (CSV)", type=["csv"])

if archivo_subido is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(archivo_subido.getvalue())
        ruta_temporal = tmp.name

    try:
        # 1. CARGA INICIAL
        df_crudo = cargar_datos(ruta_temporal)
        
        if df_crudo.empty:
            raise ValueError("El archivo cargado no contiene datos.")

        # ====================================================================
        # 2. FILTRO DE CALIDAD DE DATOS (Orquestación Defensiva)
        # ====================================================================
        
        # A. Verificar columnas obligatorias
        columnas_requeridas = ['id_participante', 'tiempo', 'valor', 'estado', 'fase', 'valido']
        for col in columnas_requeridas:
            if col not in df_crudo.columns:
                raise KeyError(f"Estructura inválida: Falta la columna requerida '{col}'.")
                
        # B. Verificar valores nulos
        if df_crudo.isnull().values.any():
            raise ValueError("El dataset contiene valores nulos o celdas vacías irrecuperables.")

        # C. Verificar tipos de datos correctos
        if not pd.api.types.is_numeric_dtype(df_crudo['id_participante']):
            raise TypeError("La columna 'id_participante' contiene texto o caracteres corruptos.")
            
        # Tolerancia a booleanos parseados como string
        if not pd.api.types.is_bool_dtype(df_crudo['valido']):
            valido_str = df_crudo['valido'].astype(str).str.strip().str.lower()
            if not valido_str.isin(['true', 'false']).all():
                raise TypeError("La columna 'valido' contiene errores tipográficos. Deben ser estrictamente booleanos (True/False).")
            df_crudo['valido'] = (valido_str == 'true')

        # D. Verificar reglas de negocio (Matemáticas básicas)
        if (df_crudo['id_participante'] <= 0).any():
            raise ValueError("Existen identificadores de participante negativos o iguales a cero.")
        if (df_crudo['tiempo'] < 0).any():
            raise ValueError("Se detectaron registros con tiempo negativo, lo cual es físicamente imposible.")
            
        # E. LIMPIEZA HIGIÉNICA DE TEXTOS Y AUTOCORRECCIÓN (El Fix)
        # Eliminamos espacios fantasmas y estandarizamos a minúsculas
        df_crudo['fase'] = df_crudo['fase'].astype(str).str.strip().str.lower()
        df_crudo['estado'] = df_crudo['estado'].astype(str).str.strip().str.lower()

        fases_permitidas = ['baseline', 'tarea']
        estados_permitidos = ['cooperacion', 'competencia']

        # Si el CSV tenía el orden invertido respecto al Doc de Diseño, lo arreglamos silenciosamente
        if df_crudo['fase'].isin(estados_permitidos).all() and df_crudo['estado'].isin(fases_permitidas).all():
            df_crudo = df_crudo.rename(columns={'fase': 'estado', 'estado': 'fase'})

        # Ahora sí, validamos estrictamente los dominios
        if not df_crudo['fase'].isin(fases_permitidas).all():
            valores_invalidos = df_crudo['fase'][~df_crudo['fase'].isin(fases_permitidas)].unique()
            raise ValueError(f"Existen valores no reconocidos en 'fase': {list(valores_invalidos)}. Solo se permite: {fases_permitidas}")

        if not df_crudo['estado'].isin(estados_permitidos).all():
            valores_invalidos = df_crudo['estado'][~df_crudo['estado'].isin(estados_permitidos)].unique()
            raise ValueError(f"Existen valores no reconocidos en 'estado': {list(valores_invalidos)}. Solo se permite: {estados_permitidos}")

        # ====================================================================
        # 3. VALIDACIÓN MATEMÁTICA GLOBAL (Backend)
        # ====================================================================
        participantes_disponibles = df_crudo['id_participante'].unique()
        
        for pid in participantes_disponibles:
            df_test = filtrar_por_participante(df_crudo, pid).reset_index(drop=True)
            if not df_test.empty:
                validar_tiempo_creciente(df_test['tiempo'])
                validar_valores_ECG(df_test['valor'].tolist(), maxi=15.0, mini=-15.0)
                calcular_fc_desde_datos(df_test)

        # ====================================================================
        # 4. RENDERIZADO DE INTERFAZ
        # ====================================================================
        st.sidebar.header("Filtros de Análisis")
        id_seleccionado = st.sidebar.selectbox("Selecciona el ID del Participante:", participantes_disponibles)
        
        df_participante = filtrar_por_participante(df_crudo, id_seleccionado).reset_index(drop=True)

        tiempos_serie = df_participante['tiempo']
        valores_serie = df_participante['valor']

        promedio = calcular_promedio_señal(valores_serie)
        maximo = calcular_maximo_señal(valores_serie)
        bpm = calcular_fc_desde_datos(df_participante)

        st.subheader(f"Indicadores Clave de Salud - Sujeto {id_seleccionado}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Frecuencia Cardíaca", value=f"{bpm:.0f} BPM")
        with col2:
            st.metric(label="Voltaje Promedio", value=f"{promedio:.2f} mV")
        with col3:
            st.metric(label="Voltaje Máximo", value=f"{maximo:.2f} mV")

        st.divider()

        st.subheader("Señal Electrocardiográfica (Dominio del Tiempo)")
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_participante['tiempo'], df_participante['valor'], color='#e63946', linewidth=1.5)
        ax.set_xlabel("Tiempo (segundos)")
        ax.set_ylabel("Amplitud de señal (mV)")
        ax.set_title(f"Registro Continuo de ECG - Participante {id_seleccionado}")
        ax.grid(True, linestyle='--', alpha=0.5)
        
        st.pyplot(fig)

    # ---------------------------------------------------------
    # MANEJO CENTRALIZADO DE EXCEPCIONES
    # ---------------------------------------------------------
    except pd.errors.ParserError:
        st.error("🚨 **Archivo Corrupto (ParserError):** Se detectó texto irrecuperable o celdas desplazadas en medio del documento.")
        st.stop()
        
    except ValueError as e:
        st.error(f"🚨 **Archivo Rechazado (Error de Integridad/Consistencia):** {str(e)}")
        st.stop()
        
    except TypeError as e:
        st.error(f"🚨 **Archivo Rechazado (Tipos de Datos Inválidos):** {str(e)}")
        st.stop()
        
    except KeyError as e:
        st.error(f"🚨 **Estructura Incorrecta:** {str(e)}")
        st.stop()
        
    except Exception as e:
        st.error(f"🚨 **Error Interno en el Procesamiento:** {str(e)}")
        st.stop()
        
    finally:
        if os.path.exists(ruta_temporal):
            try:
                os.remove(ruta_temporal)
            except Exception:
                pass

else:
    st.info("💡 Esperando datos. Por favor, utiliza el componente superior para subir tu dataset CSV.")