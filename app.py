import streamlit as st
import matplotlib.pyplot as plt

from src.carga_datos import cargar_datos
from src.procesamiento_datos import filtrar_por_participante
from src.metricas import calcular_promedio_señal, calcular_maximo_señal, calcular_fc_desde_datos
from src.validar import validar_tiempo_creciente


st.set_page_config(page_title="Dashboard PulseLab", page_icon="❤", layout="wide")

st.title("❤ Dashboard de Análisis ECG - PulseLab")
st.markdown("Esta aplicación utiliza las funciones modulares del sistema PulseLab para analizar datos de ECG.")


@st.cache_data
def cargar_datos_app():
    
    return cargar_datos("datos/PulseLab_mock_data.csv")

try:
    
    datos = cargar_datos_app()
    
    participantes = datos["id_participante"].unique()

    st.sidebar.header("Controles")
    participante_seleccionado = st.sidebar.selectbox("Seleccione un Participante", participantes)
    
    datos_filtrados = filtrar_por_participante(datos, participante_seleccionado)
    
    tiempos = datos_filtrados["tiempo"]
    señal = datos_filtrados["valor"]

   
    try:
        validar_tiempo_creciente(tiempos)
        st.sidebar.success("Estado de tiempo: Válido (Creciente)")
    except Exception as e:
        st.sidebar.error(f"Error de validación: {e}")

    promedio = calcular_promedio_señal(señal)
    maximo = calcular_maximo_señal(señal)
    
    try:
        frecuencia = calcular_fc_desde_datos(datos_filtrados)
    except Exception as e:
        frecuencia = f"Error: {e}"


    st.subheader(f"Métricas del Participante {participante_seleccionado}")
    

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Promedio de Señal", value=f"{promedio:.2f}")
    col2.metric(label="Máximo de Señal", value=f"{maximo:.2f}")
    

    if isinstance(frecuencia, (int, float)):
        col3.metric(label="Frecuencia Cardíaca (BPM)", value=f"{frecuencia:.1f}")
    else:
        col3.error(frecuencia)

    st.subheader("Gráfico de Electrocardiograma (ECG)")
    

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(tiempos, señal, color="#E91E63", linewidth=1.5)
    ax.set_title(f"Señal ECG - Participante {participante_seleccionado}")
    ax.set_xlabel("Tiempo (segundos)")
    ax.set_ylabel("Amplitud de la Señal")
    ax.grid(True, linestyle="--", alpha=0.6)
 
    st.pyplot(fig)

except FileNotFoundError:
    st.error("❌ No se encontró el archivo de datos. Asegúrate de que 'datos/PulseLab_mock_data.csv' exista.")
except Exception as e:
    st.error(f"❌ Ocurrió un error inesperado al procesar los datos: {e}")