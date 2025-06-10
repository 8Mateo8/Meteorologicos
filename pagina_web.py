import streamlit as st
import pandas as pd
import plotly.express as px
import data
from streamlit_option_menu import option_menu

# Leer el CSV
datos = data.importar_datos()

# Función para seleccionar las fechas límite de los gráficos
def fechas(etiqueta=""):
    fecha_min = st.date_input('Seleccione una fecha de inicio', 
                              value=pd.to_datetime('2020-01-01'), 
                              min_value=datos['Fecha del registro'].min(), 
                              max_value=datos['Fecha del registro'].max(),
                              key=f"{etiqueta}_fecha_inicio")

    fecha_max = st.date_input('Seleccione una fecha de fin',
                              value=pd.to_datetime('2025-05-31'),
                              min_value=datos['Fecha del registro'].min(),
                              max_value=datos['Fecha del registro'].max(),
                              key=f"{etiqueta}_fecha_fin")

    return [pd.to_datetime(fecha_min), pd.to_datetime(fecha_max)]

menu_opcion = option_menu(None, ["Inicio", 'Tendencias climáticas', 'Comparación de rangos temporales', 'Anomalías climáticas'], 
    icons=['brightness-alt-high', 'thermometer-sun', 'calendar-range', 'exclamation-triangle'], 
    menu_icon="house-door-fill", default_index=0, orientation="horizontal")

if menu_opcion == 'Inicio':
    # Título de la página web
    st.title('Datos Metereológicos en Cuenca - Ecuador')

    # Descripción de la página
    st.markdown('<div style="text-align: justify;">En esta página web se presentan los datos meteorológicos de la ciudad de Cuenca, obtenidos a partir de la base de datos del proyecto POWER (Prediction Of Worldwide Energy Resources) de la NASA. Este conjunto de datos incluye información meteorológica histórica y actualizada, recopilada mediante sensores satelitales.</div>', unsafe_allow_html=True)
    st.write('Los datos están disponibles desde el 1 de enero del 2020 hasta el 31 de mayo del 2025.')

    # Visualización de los datos
    st.header('Visualización de tendencias climáticas a lo largo del tiempo.')
    variable = st.selectbox('',['Seleccione la variable a visualizar', 'Temperatura promedio diaria del aire a 2 metros (°C)', 
                                    'Humedad relativa promedio diaria a 2 metros (%)', 
                                    'Velocidad del viento a 2 metros (m/s)',
                                    'Precipitación total corregida (mm/día)', 
                                    'Radiación solar total en la superficie (kWh/m²/día)'])

if variable == 'Temperatura promedio diaria del aire a 2 metros (°C)':
    pass
elif variable == 'Humedad relativa promedio diaria a 2 metros (%)':
    pass
elif variable == 'Velocidad del viento a 2 metros (m/s)':
    arreglo = fechas("viento")
    grafico = datos[(datos['Fecha del registro'] >= arreglo[0]) & (datos['Fecha del registro'] <= arreglo[1])]

    fig = px.line(
        grafico,
        x='Fecha del registro',
        y='Viento (m/s)',
        title='Viento Diario Promedio',
        labels={'Fecha del registro': 'Fecha', 'Viento (m/s)': 'Viento (m/s)'}
    )
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Viento (m/s)')
    st.plotly_chart(fig)

elif variable == 'Precipitación total corregida (mm/día)':
    arreglo = fechas("precipitacion")
    grafico = datos[(datos['Fecha del registro'] >= arreglo[0]) & (datos['Fecha del registro'] <= arreglo[1])]

    fig = px.line(
        grafico,
        x='Fecha del registro',
        y='Precipitación (mm)',
        title='Precipitación Diaria Promedio',
        labels={'Fecha del registro': 'Fecha', 'Precipitación (mm)': 'Precipitación (mm)'}
    )
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Precipitación (mm)')
    st.plotly_chart(fig)

elif variable == 'Radiación solar total en la superficie (kWh/m²/día)':
    arreglo = fechas("radiacion")
    grafico = datos[(datos['Fecha del registro'] >= arreglo[0]) & (datos['Fecha del registro'] <= arreglo[1])]

    fig = px.line(
        grafico,
        x='Fecha del registro',
        y='Radiación solar (kWh/m²/día)',
        title='Radiación Solar Diaria promedio',
        labels={'Fecha del registro': 'Fecha', 'Radiación solar (kWh/m²/día)': 'Radiación solar (kWh/m²/día)'}
    )
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Radiación solar (kWh/m²/día)')
    st.plotly_chart(fig)

st.header('Comparación de promedios mensuales o anuales entre diferentes rangos temporales.')
rangos = st.pills('Seleccione el rango de tiempo para comparar promedios:', 
                  ['Mensual', 'Anual'])

if rangos == 'Mensual':
    st.write('Seleccione el rango de fechas para calcular los promedios mensuales.')
    rango_fechas = fechas("promedios_mensuales")
    datos_mensuales = datos[(datos['Fecha del registro'] >= rango_fechas[0]) & (datos['Fecha del registro'] <= rango_fechas[1])]
    datos_mensuales['Mes'] = datos_mensuales['Fecha del registro'].dt.to_period('M').astype(str)
    promedios_mensuales = datos_mensuales.groupby('Mes').mean().reset_index()

    # st.write(promedios_mensuales)
    fig = px.bar(promedios_mensuales, x='Mes', y='Temperatura (°C)', title='Promedio Mensual de Temperatura')
    st.plotly_chart(fig)
elif rangos == 'Anual':
    st.write('Seleccione el rango de fechas para calcular los promedios anuales.')
    rango_fechas = fechas("promedios_anuales")
    datos_anuales = datos[(datos['Fecha del registro'] >= rango_fechas[0]) & (datos['Fecha del registro'] <= rango_fechas[1])]
    datos_anuales['Año'] = datos_anuales['Fecha del registro'].dt.year
    promedios_anuales = datos_anuales.groupby('Año').mean().reset_index()

    # st.write(promedios_anuales)
    fig = px.bar(promedios_anuales, x='Año', y='Temperatura (°C)', title='Promedio Anual de Temperatura')
    st.plotly_chart(fig)
