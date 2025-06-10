import pandas as pd

def importar_datos():

    try:
        # Leer el CSV, saltando las 13 filas iniciales
        datos_i = pd.read_csv("POWER_Point_Daily_20200101_20250531_002d92S_079d00W_LST.csv", skiprows=13)
        
        # Renombrar columnas para facilitar su uso
        datos_i = datos_i.rename(columns={
            'DATE': 'Fecha del registro', 
            'T2M': 'Temperatura (°C)', 
            'RH2M': 'Humedad relativa (%)', 
            'PRECTOTCORR': 'Precipitación (mm)', 
            'WS2M': 'Viento (m/s)',
            'ALLSKY_SFC_SW_DWN': 'Radiación solar (kWh/m²/día)'
        })
        
        # Convertir la columna de fecha a tipo datetime
        datos_i['Fecha del registro'] = pd.to_datetime(datos_i['Fecha del registro'])

        # Reemplazar valores -999 (faltantes) con NaN
        datos_i = datos_i.replace(-999, pd.NA)
        
        # Convertir columnas a tipo numérico donde sea posible
        for col in datos_i.columns:
            if col != 'Fecha del registro':
                datos_i[col] = pd.to_numeric(datos_i[col], errors='coerce')

        # Imputar valores faltantes con el promedio semanal
        datos_i.set_index('Fecha del registro', inplace=True)
        datos_i = datos_i.groupby(datos_i.index.to_period('W')).transform(lambda x: x.fillna(x.mean()))
        datos_i = datos_i.reset_index()
        
        return datos_i
    except Exception as e:
        print(f"Error al importar datos: {e}")
        return None