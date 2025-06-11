import streamlit as st
import pandas as pd
import plotly.express as px
import data
from streamlit_option_menu import option_menu

# Leer el CSV
datos = data.importar_datos()

# Función para seleccionar las fechas límite de los gráficos
def fechas(etiqueta=""):
    fecha_min = st.date_input(
        'Seleccione una fecha de inicio',
        value=pd.to_datetime('2020-01-01'),
        min_value=datos['Fecha del registro'].min(),
        max_value=datos['Fecha del registro'].max(),
        key=f"{etiqueta}_fecha_inicio")

    fecha_max = st.date_input(
        'Seleccione una fecha de fin',
        value=pd.to_datetime('2025-05-31'),
        min_value=fecha_min,
        max_value=datos['Fecha del registro'].max(),
        key=f"{etiqueta}_fecha_fin")

    if fecha_min > fecha_max:
        return [pd.to_datetime(fecha_max), pd.to_datetime(fecha_min)]

    return [pd.to_datetime(fecha_min), pd.to_datetime(fecha_max)]

def variables_clima():
    seleccion = st.selectbox('',['Seleccione la variable a visualizar', 'Temperatura promedio del aire a 2 metros (°C)', 
                                    'Humedad relativa promedio a 2 metros (%)', 
                                    'Velocidad del viento a 2 metros (m/s)',
                                    'Precipitación total corregida (mm/día)', 
                                    'Radiación solar total en la superficie (kWh/m²/día)'])
    return seleccion


menu_opcion = option_menu(None, ["Inicio", 'Tendencias climáticas', 'Comparación de rangos temporales', 'Anomalías climáticas'], 
    icons=['brightness-alt-high', 'thermometer-sun', 'calendar-range', 'exclamation-triangle'], 
    menu_icon="house-door-fill", default_index=0, orientation="horizontal")

if menu_opcion == 'Inicio':
    # Título de la página web
    st.title('Datos Meteorológicos en Cuenca - Ecuador')

    # Descripción de la página
    st.markdown('<div style="text-align: justify;">En esta página web se presentan los datos meteorológicos de la ciudad de Cuenca, obtenidos a partir de la base de datos del proyecto POWER (Prediction Of Worldwide Energy Resources) de la NASA. Este conjunto de datos incluye información meteorológica histórica y actualizada, recopilada mediante sensores satelitales.</div>', unsafe_allow_html=True)
    st.write('Los datos están disponibles desde el 1 de enero del 2020 hasta el 31 de mayo del 2025.')

    st.image('cathedral-of-cuenca-4021077_1920.jpg', width=None, caption='Catedral de Cuenca, Ecuador', use_container_width=True)

elif menu_opcion == 'Tendencias climáticas':
    # Visualización de los datos
    st.header('Visualización de tendencias climáticas a lo largo del tiempo.')
    variable = variables_clima()

    if variable == 'Temperatura promedio del aire a 2 metros (°C)':
        arreglo = fechas("temperatura")
        grafico = datos[(datos['Fecha del registro'] >= arreglo[0]) & (datos['Fecha del registro'] <= arreglo[1])]

        fig = px.line(
            grafico,
            x='Fecha del registro',
            y='Temperatura (°C)',
            title='Temperatura Diaria Promedio',
            labels={'Fecha del registro': 'Fecha', 'Temperatura (°C)': 'Temperatura (°C)'}
        )
        fig.update_layout(xaxis_title='Fecha', yaxis_title='Temperatura (°C)')
        st.plotly_chart(fig)

    elif variable == 'Humedad relativa promedio a 2 metros (%)':
        arreglo = fechas("humedad")
        grafico = datos[(datos['Fecha del registro'] >= arreglo[0]) & (datos['Fecha del registro'] <= arreglo[1])]

        fig = px.line(
            grafico,
            x='Fecha del registro',
            y='Humedad relativa (%)',
            title='Humedad Diaria Promedio',
            labels={'Fecha del registro': 'Fecha', 'Humedad relativa (%)': 'Humedad relativa (%)'}
        )
        fig.update_layout(xaxis_title='Fecha', yaxis_title='Humedad relativa (%)')
        st.plotly_chart(fig)

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
            title='Radiación Solar Diaria Promedio',
            labels={'Fecha del registro': 'Fecha', 'Radiación solar (kWh/m²/día)': 'Radiación solar (kWh/m²/día)'}
        )
        fig.update_layout(xaxis_title='Fecha', yaxis_title='Radiación solar (kWh/m²/día)')
        st.plotly_chart(fig)

elif menu_opcion == 'Comparación de rangos temporales':
    st.header('Comparación de promedios mensuales o anuales entre diferentes rangos temporales.')
    rangos = st.pills('Seleccione el rango de tiempo para comparar promedios:', ['Mensual', 'Anual'])
    opcion = variables_clima()

    if rangos == 'Mensual':
        metodo = st.segmented_control(None, ['De un año', 'De varios años'])
        if metodo == 'De varios años':
            Año1 = st.segmented_control('Seleccione el año 1:', datos['Fecha del registro'].dt.year.unique(), key='año1')
            if Año1 == 2025:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
            else:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mes1 = st.segmented_control('Seleccione el mes 1:', arr_m, selection_mode='single', key='mes1')
            Año2 = st.segmented_control('Seleccione el año 2:', datos['Fecha del registro'].dt.year.unique(), key='año2')
            if Año2 == 2025:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
            else:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            mes2 = st.segmented_control('Seleccione el mes 2:', arr_m, selection_mode='single', key='mes2')

            if mes1 != None and mes2 != None and Año1 != None and Año2 != None and opcion != 'Seleccione la variable a visualizar' and not(mes1 != mes2 and Año1 == Año2):
                datos_filtrados1 = datos[(datos['Fecha del registro'].dt.year == Año1) & (datos['Fecha del registro'].dt.month ==arr_m.index(mes1) + 1)]
                datos_filtrados2 = datos[(datos['Fecha del registro'].dt.year == Año2) & (datos['Fecha del registro'].dt.month ==arr_m.index(mes2) + 1)]
                # Map user-friendly variable names to DataFrame column names
                variable_map = {
                    'Temperatura promedio del aire a 2 metros (°C)': 'Temperatura (°C)',
                    'Humedad relativa promedio a 2 metros (%)': 'Humedad relativa (%)',
                    'Velocidad del viento a 2 metros (m/s)': 'Viento (m/s)',
                    'Precipitación total corregida (mm/día)': 'Precipitación (mm)',
                    'Radiación solar total en la superficie (kWh/m²/día)': 'Radiación solar (kWh/m²/día)'
                }
                columna = variable_map.get(opcion)
                promedio1 = datos_filtrados1[columna].mean()
                promedio2 = datos_filtrados2[columna].mean() 
                fig = px.bar(x=[mes1 + ' ' + Año1, mes2 + ' ' + Año2], y=[promedio1, promedio2],
                    title=f'Promedio Mensual de {opcion} para {mes1} de {Año1} y {mes2} de {Año2}')
                st.plotly_chart(fig)
            else:
                st.warning('Por favor, seleccione todos los campos necesarios para generar el gráfico.')



        elif metodo == 'De un año':
            Año = st.segmented_control('Seleccione el año:', datos['Fecha del registro'].dt.year.unique(), key='año')
            if Año == 2025:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
            else:
                arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            meses = st.segmented_control('Seleccione el mes:', ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], 
                                                            selection_mode='multi', key='meses')



    elif rangos == 'Anual':
        st.write('Seleccione el rango de fechas para calcular los promedios anuales.')
        rango_fechas = fechas("promedios_anuales")
        datos_anuales = datos[(datos['Fecha del registro'] >= rango_fechas[0]) & (datos['Fecha del registro'] <= rango_fechas[1])]
        datos_anuales['Año'] = datos_anuales['Fecha del registro'].dt.year
        promedios_anuales = datos_anuales.groupby('Año').mean().reset_index()

        # st.write(promedios_anuales)
        fig = px.bar(promedios_anuales, x='Año', y='Temperatura (°C)', title='Promedio Anual de Temperatura')
        st.plotly_chart(fig)

elif menu_opcion == 'Anomalías climáticas':
    st.header('Identificación de anomalías climáticas ')
    anomalia = variables_clima()

    if anomalia == 'Temperatura promedio diaria del aire a 2 metros (°C)':
        pass
    elif anomalia == 'Humedad relativa promedio diaria a 2 metros (%)':
        pass
    elif anomalia == 'Velocidad del viento a 2 metros (m/s)':
        pass
    elif anomalia == 'Precipitación total corregida (mm/día)':
        pass
    elif anomalia == 'Radiación solar total en la superficie (kWh/m²/día)':
        pass
