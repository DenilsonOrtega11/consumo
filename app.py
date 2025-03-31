import streamlit as st
import googlemaps
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import statsmodels.api as sm
# import seaborn as sns
# import matplotlib.pyplot as plt

# API Key de Google Maps
API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
gmaps = googlemaps.Client(key=API_KEY)

# Título de la aplicación
st.set_page_config(page_title="Consumo", page_icon="🛞", layout="wide")
st.title("Consumo de Combustible entre Ciudades")

# Entrada de usuario para las ciudades de origen y destino
origen = st.text_input("Ciudad de Origen (Ejemplo: Ciudad de México):")
destino = st.text_input("Ciudad de Destino (Ejemplo: Monterrey):")

# Botón para realizar la predicción
if st.button("Iniciar Predicción"):
    if origen and destino:
        st.write("Calculando ruta entre las ciudades...")
        
        directions_result_ida = gmaps.directions(origen, destino, mode="driving", departure_time=datetime.now(), avoid=["tolls", "highways"])
        directions_result_vuelta = gmaps.directions(destino, origen, mode="driving", departure_time=datetime.now(), avoid=["tolls", "highways"])

        if directions_result_ida and directions_result_vuelta:
            # Obtener la duración del viaje
            duration_ida = directions_result_ida[0]['legs'][0]['duration']['value']
            duration_vuelta = directions_result_vuelta[0]['legs'][0]['duration']['value']

            duration_ida_hours = duration_ida / 3600
            duration_vuelta_hours = duration_vuelta / 3600

            total_duration_hours = duration_ida_hours + duration_vuelta_hours
            acondicionado_hours = total_duration_hours * 0.30

            st.write(f"Duración total del viaje de ida y vuelta: {total_duration_hours:.2f} horas")
            st.write(f"Horas de aire acondicionado aproximadas: {acondicionado_hours:.2f} horas")

            # Cargar el dataset
            df = pd.read_excel("dataset_MOE.xlsx")

            if 'acondicionado' not in df.columns:
                st.error("La columna 'acondicionado' no se encuentra en el archivo.")
                st.stop()

            # Variables para el modelo
            x1 = "distancia"
            x2 = "acondicionado"
            y = "litros"

            variables_x = [x1, x2]
            variable_y = y

            # Modelo de Regresión Polinómica
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(df[variables_x])

            modelo = LinearRegression()
            modelo.fit(X_poly, df[variable_y])

            # Predicción de Consumo de Combustible
            dt = (total_duration_hours * 100)  # Estimación de distancia total
            prediccion_nueva = pd.DataFrame({x1: [dt], x2: [acondicionado_hours]})
            prediccion_nueva_poly = poly.transform(prediccion_nueva)
            ct = modelo.predict(prediccion_nueva_poly)

            st.write(f"Consumo de combustible aproximado: {round(ct[0], 3)} litros")
            st.write(f"Distancia total estimada: {dt:.2f} km")

        else:
            st.error("No se pudo calcular la ruta de ida y vuelta. Verifique las ciudades ingresadas.")
    else:
        st.warning("Por favor, ingrese todas las ciudades.")
