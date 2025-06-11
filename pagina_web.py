import streamlit as st
import pandas as pd
import plotly.express as px
import data
from streamlit_option_menu import option_menu
import numpy as np
from scipy import stats

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

# Función para seleccionar la variable climática a visualizar
def variables_clima():
    seleccion = st.selectbox('Seleccione la variable a visualizar:', ['Seleccione una opción',  
                                                                      'Temperatura promedio del aire a 2 metros (°C)',
                                                                      'Humedad relativa promedio a 2 metros (%)',
                                                                      'Velocidad del viento a 2 metros (m/s)',
                                                                      'Precipitación total corregida (mm/día)',
                                                                      'Radiación solar total en la superficie (kWh/m²/día)'])
    if seleccion == 'Seleccione una opción':
        return None
    else:
        return seleccion

# Diccionario de apoyo para las variables climáticas
apoyo = {'Temperatura promedio del aire a 2 metros (°C)': 'Temperatura (°C)',
         'Humedad relativa promedio a 2 metros (%)': 'Humedad relativa (%)',
         'Velocidad del viento a 2 metros (m/s)': 'Viento (m/s)',
         'Precipitación total corregida (mm/día)': 'Precipitación (mm)',
         'Radiación solar total en la superficie (kWh/m²/día)': 'Radiación solar (kWh/m²/día)'}

# Función para calcular la prueba de Kendall Tau
def kend_tau(data, columna):
    x = data['Fecha del registro'].map(pd.Timestamp.toordinal)
    booleano = st.toggle('Prueba estadística', key='estadistica_temperatura')

    if booleano:
        tau, p = stats.kendalltau(x, data[columna])
        st.write('Prueba de Kendall')
        st.write(f"τ: {tau}, p: {p}")
        if p < 0.05 and tau > 0:
            st.success("Hay una tendencia creciente en los datos.")
        elif p < 0.05 and tau < 0:
            st.success("Hay una tendencia decreciente en los datos.")
        elif p >= 0.05:
            st.warning("La correlación no es estadísticamente significativa")

# Función para realizar la prueba de normalidad
def Shapiro(data, mes, año):
    stat, p = stats.shapiro(data)
    if p > 0.05:
        # st.write(f"{mes} de {año}, Estadístico: {stat}, p: {p}, Distribución normal")
        return True # La variable sigue una distribución normal.
    else:
        # st.write(f"{mes} de {año}, Estadístico: {stat}, p: {p}, Distribución no normal")
        return False # La variable no sigue una distribución normal.

# Configuración del menú de la página
menu_opcion = option_menu(None, ["Inicio", 'Tendencias climáticas', 'Comparación de rangos temporales', 
                                 'Anomalías climáticas', 'Preguntas de investigación'], 
    icons=['brightness-alt-high', 'thermometer-sun', 'calendar-range', 'tropical-storm', 'stars'], 
    menu_icon="house-door-fill", default_index=0, orientation="horizontal")

if menu_opcion == 'Inicio':
    # Título de la página web
    st.title('Datos Meteorológicos en Cuenca - Ecuador')

    st.subheader('Mateo Calderón - Lisseth Guazhambo')

    # Descripción de la página
    st.markdown('<div style="text-align: justify;">En esta página web se presentan los datos meteorológicos ' \
    'de la ciudad de Cuenca, obtenidos a partir de la base de datos del proyecto POWER (Prediction Of ' \
    'Worldwide Energy Resources) de la NASA. Este conjunto de datos incluye información meteorológica ' \
    'histórica y actualizada, recopilada mediante sensores satelitales.</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Además se realizó un análisis de los datos en' \
    ' base a gráficas y pruebas estadísticas para responder a las preguntas de investigación</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify;">Se usaron los datos disponibles desde el 1 de enero del 2020 ' \
    'hasta el 31 de mayo del 2025.</div>', unsafe_allow_html=True)

    st.image('cathedral-of-cuenca-4021077_1920.jpg', width=None, caption='Catedral de Cuenca, Ecuador', use_container_width=True)

elif menu_opcion == 'Tendencias climáticas':
    # Visualización de los datos
    st.header('Visualización de tendencias climáticas a lo largo del tiempo.')
    variable = variables_clima()

    # Se filtran los datos según la variable seleccionada
    # Se crea un gráfico de líneas para la variable seleccionada
    # Se calcula la prueba de Kendall Tau para la tendencia de la variable seleccionada
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

        kend_tau(grafico, 'Temperatura (°C)')

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

        kend_tau(grafico, 'Humedad relativa (%)')

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

        kend_tau(grafico, 'Viento (m/s)')

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

        kend_tau(grafico, 'Precipitación (mm)')

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

        kend_tau(grafico, 'Radiación solar (kWh/m²/día)')

elif menu_opcion == 'Comparación de rangos temporales':
    st.header('Comparación de promedios mensuales o anuales entre diferentes rangos temporales.')
    
    # Menú para seleccionar el rango de tiempo
    rangos = st.pills('Seleccione el rango de tiempo para comparar promedios:', ['Mensual', 'Anual'])
    
    # Selección de la variable climática
    opcion = variables_clima()

    # Validación de la selección de la variable
    if rangos == 'Mensual':

        # Selección del año y meses
        Año = st.segmented_control('Seleccione el año:', datos['Fecha del registro'].dt.year.unique(), key='año')
        if Año == 2025:
            arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
        else:
            arr_m = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        meses = st.segmented_control('Seleccione el/los mes/es:', arr_m, selection_mode='multi', key='meses')
        
        # Validación de la selección del año, meses y variable
        if Año != None and meses != [] and opcion != None:
            promedios = []
            meses_seleccionados = [arr_m.index(mes) + 1 for mes in meses]
            normal = True

            # Filtrar los datos por el año, filtrar los meses seleccionados y realizar la prueba de normalidad
            for mes in meses_seleccionados:
                datos_filtrados = datos[(datos['Fecha del registro'].dt.year == Año) & (datos['Fecha del registro'].dt.month == mes)]
                columna = apoyo.get(opcion)
                promedio = datos_filtrados[columna].mean()
                promedios.append(promedio)

                # Realizar la prueba de normalidad
                normal = normal and Shapiro(datos_filtrados[columna], arr_m[mes - 1], Año)
            # st.write(normal)

            # Crear un gráfico de barras con los promedios mensuales
            fig = px.bar(
                x=meses,
                y=promedios,
                title=f'Promedio Mensual de {opcion} en {Año}',
                labels={'x': 'Mes', 'y': f'Promedio de {opcion}'},
                color=meses
            )
            fig.update_traces(showlegend=False)
            st.plotly_chart(fig)

            # Mostrar la prueba de normalidad
            mostrar = st.toggle('Pruebas estadísticas', key='pruebas_estadisticas')
            grupos = [datos[(datos['Fecha del registro'].dt.year == Año) & 
                                    (datos['Fecha del registro'].dt.month == mes)][columna].dropna()
                              for mes in meses_seleccionados]
            # st.write(grupos)
            if mostrar and len(grupos) > 1:
                if normal:
                    st.write('Los datos siguen una distribución normal.')

                    if len(grupos) < 3:
                        # Realizar la prueba t
                        st.write('Resultados de la prueba t de Student:')
                        t_stat, p_value = stats.ttest_ind(*grupos)
                        st.write(f"Estadístico t: {t_stat}, p: {p_value}")
                        
                    else:
                        # Realizar la prueba ANOVA
                        st.write('Resultados de la prueba ANOVA:')
                        f_stat, p_value = stats.f_oneway(*grupos)
                        st.write(f"Estadístico F: {f_stat}, p: {p_value}")
                    if p_value < 0.05:
                        st.write("Hay diferencias significativas entre los promedios mensuales.")
                    else:
                        st.write("No hay diferencias significativas entre los promedios mensuales.")
                else:
                    st.write('Los datos no siguen una distribución normal.')

                    if len(grupos) < 3:
                        # Realizar la prueba U de Mann-Whitney
                        st.write('Resultados de la prueba U de Mann-Whitney:')
                        u_stat, p_value = stats.mannwhitneyu(*grupos)
                        st.write(f"Estadístico U: {u_stat}, p: {p_value}")
        
                    else:
                        # Realizar la prueba Kruskal-Wallis
                        st.write('Resultados de la prueba Kruskal-Wallis:')
                        h_stat, p_value = stats.kruskal(*grupos)
                        st.write(f"Estadístico H: {h_stat}, p: {p_value}")
                    if p_value < 0.05:
                        st.write("Hay diferencias significativas entre los promedios mensuales.")
                    else:
                        st.write("No hay diferencias significativas entre los promedios mensuales.")

        else:
            st.warning('Por favor, seleccione todos los campos necesarios para generar el gráfico.')
        
    elif rangos == 'Anual':
    
        # Selección de los años
        arr_a = ['2020', '2021', '2022', '2023', '2024', '2025']
        Años = st.segmented_control('Seleccione los años:', arr_a, 
                                    selection_mode='multi', key='años')

        # Validación de la selección de los años y variable
        if Años != [] and opcion != None:
            años_seleccionados = [int(año) for año in Años]
            promedios_anuales = []
            grupos = []
            normal = True
            columna = apoyo.get(opcion)

            # Filtrar los datos por los años seleccionados y calcular el promedio anual
            for año in años_seleccionados:
                datos_filtrados = datos[datos['Fecha del registro'].dt.year == año]
                promedio_anual = datos_filtrados[columna].mean()
                promedios_anuales.append(promedio_anual)
                grupos.append(datos_filtrados[columna].dropna())

                # Prueba de normalidad para cada grupo
                normal = normal and Shapiro(datos_filtrados[columna], str(año), año)

            # Crear un gráfico de barras con los promedios anuales
            df_promedios = pd.DataFrame({
                'Año': [str(año) for año in años_seleccionados],
                'Promedio': promedios_anuales
            })

            fig = px.bar(
                df_promedios,
                x='Año',
                y='Promedio',
                title=f'Promedio Anual de {opcion}',
                labels={'Año': 'Año', 'Promedio': 'Promedio anual'},
                color='Año'
            )
            fig.update_layout(xaxis_type='category')
            fig.update_traces(showlegend=False)

            st.plotly_chart(fig)

            # Pruebas estadísticas
            mostrar = st.toggle('Pruebas estadísticas', key='pruebas_estadisticas_anual')
            if mostrar and len(grupos) > 1:
                if normal:
                    st.write('Los datos siguen una distribución normal.')
                    if len(grupos) < 3:
                        # Prueba t
                        st.write('Resultados de la prueba t de Student:')
                        t_stat, p_value = stats.ttest_ind(*grupos)
                        st.write(f"Estadístico t: {t_stat:.4f}, p: {p_value:.4f}")
                    else:
                        # ANOVA
                        st.write('Resultados de la prueba ANOVA:')
                        f_stat, p_value = stats.f_oneway(*grupos)
                        st.write(f"Estadístico F: {f_stat:.4f}, p: {p_value:.4f}")
                    if p_value < 0.05:
                        st.write("Hay diferencias significativas entre los promedios anuales.")
                    else:
                        st.write("No hay diferencias significativas entre los promedios anuales.")
                else:
                    st.write('Los datos no siguen una distribución normal.')
                    if len(grupos) < 3:
                        # Mann-Whitney
                        st.write('Resultados de la prueba U de Mann-Whitney:')
                        u_stat, p_value = stats.mannwhitneyu(*grupos)
                        st.write(f"Estadístico U: {u_stat:.4f}, p: {p_value:.4f}")
                    else:
                        # Kruskal-Wallis
                        st.write('Resultados de la prueba Kruskal-Wallis:')
                        h_stat, p_value = stats.kruskal(*grupos)
                        st.write(f"Estadístico H: {h_stat:.4f}, p: {p_value:.4f}")
                    if p_value < 0.05:
                        st.write("Hay diferencias significativas entre los promedios anuales.")
                    else:
                        st.write("No hay diferencias significativas entre los promedios anuales.")

        else:
            st.warning('Por favor, seleccione todos los campos necesarios para generar el gráfico.')

elif menu_opcion == 'Anomalías climáticas':
    st.header('Identificación de anomalías climáticas ')
    anomalia = variables_clima()

    if anomalia == 'Temperatura promedio del aire a 2 metros (°C)':
        columna = apoyo.get(anomalia)
        st.subheader(f"Análisis de anomalías en {columna}")

        # Calcular IQR
        q1 = datos[columna].quantile(0.25)
        q3 = datos[columna].quantile(0.75)
        iqr = q3 - q1
        lim_inf = q1 - 1.5 * iqr
        lim_sup = q3 + 1.5 * iqr

        # Detectar valores fuera del rango (anomalías)
        datos_filtrados = datos[(datos[columna] >= lim_inf) & (datos[columna] <= lim_sup)]
        datos_anomalías = datos[(datos[columna] < lim_inf) | (datos[columna] > lim_sup)]

        # Mostrar resultados
        st.write(f"Valores normales: {len(datos_filtrados)} | Anómalos: {len(datos_anomalías)}")
        st.write(f"Rango aceptado: [{lim_inf:.2f}, {lim_sup:.2f}]")

        # Prueba de normalidad en los valores filtrados
        stat, p_shapiro = stats.shapiro(datos_filtrados[columna].dropna())
        st.write(f"Prueba de Shapiro-Wilk para valores filtrados: p-valor = {p_shapiro:.4f}")
        if p_shapiro > 0.05:
            st.success("Los valores filtrados siguen una distribución normal.")
        else:
            st.warning("Los valores filtrados NO siguen una distribución normal.")

        # Gráfico de dispersión con anomalías resaltadas
        fig = px.scatter(datos, x="Fecha del registro", y=columna, title=f'{columna} con anomalías (IQR)')
        fig.add_scatter(x=datos_anomalías["Fecha del registro"], y=datos_anomalías[columna],
                        mode='markers', marker=dict(color='red', size=6), name="Anomalías")
        st.plotly_chart(fig)
    elif anomalia == 'Humedad relativa promedio diaria a 2 metros (%)':
        pass
    elif anomalia == 'Velocidad del viento a 2 metros (m/s)':
        pass
    elif anomalia == 'Precipitación total corregida (mm/día)':
        pass
    elif anomalia == 'Radiación solar total en la superficie (kWh/m²/día)':
        pass

elif menu_opcion == 'Preguntas de investigación':
    st.header('Preguntas de investigación')
    st.markdown('''
    1. **¿Cómo ha cambiado la temperatura promedio en Cuenca a lo largo del tiempo?**
       - Esta pregunta busca identificar tendencias en la temperatura promedio diaria a lo largo de los años.
    
    2. **¿Cuál es la variación estacional de la humedad relativa en Cuenca?**
       - Se pretende analizar cómo varía la humedad relativa promedio a lo largo de los meses del año.
    
    3. **¿Cómo afecta la velocidad del viento a las precipitaciones en Cuenca?**
       - Esta pregunta investiga la relación entre la velocidad del viento y las precipitaciones diarias.
    
    4. **¿Qué patrones se pueden observar en la radiación solar a lo largo del año?**
       - Se busca identificar patrones estacionales en la radiación solar total en la superficie.
    
    5. **¿Existen anomalías climáticas significativas en los últimos años?**
       - Esta pregunta se centra en detectar anomalías climáticas, como eventos extremos o cambios inusuales en las variables meteorológicas.
    ''')