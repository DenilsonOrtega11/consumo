import streamlit as st
import googlemaps
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
gmaps = googlemaps.Client(key=API_KEY)

st.title("Consumo de combustible entre ciudades")

origen = st.text_input("Ciudad de Origen", placeholder="Ejemplo: Ciudad de México")
destino = st.text_input("Ciudad de Destino", placeholder="Ejemplo: Monterrey")
peso = st.text_input("Peso", placeholder="Ejemplo: 7200kg")

if st.button("Calcular Consumo"):
    if origen and destino and peso:
        directions_result = gmaps.directions(origen, destino, mode="driving", departure_time=datetime.now(), avoid=["tolls", "highways"])

        if directions_result:
            distance = directions_result[0]['legs'][0]['distance']['text']
            duration = directions_result[0]['legs'][0]['duration']['text']

            st.success(f"Distancia: {distance}")

            distance_float = distance.replace(",", "")
            distance_float = float((distance_float.split()[0]))

            df = pd.read_excel("dataset_MOE.xlsx")

            x1 = "distancia"
            x2 = "peso"
            y = "litros"

            variables_x = [x1, x2]
            variable_y = y

            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(df[variables_x])

            modelo = LinearRegression()
            modelo.fit(X_poly, df[variable_y])

            dt = (distance_float + distance_float)
            pt = float(peso)

            prediccion_nueva = pd.DataFrame({x1: [dt], x2: [pt]})
            prediccion_nueva_poly = poly.transform(prediccion_nueva)
            ct = modelo.predict(prediccion_nueva_poly)

            st.success(f"Consumo de combustible aproximado: {round(ct[0], 3)}")
            st.success(f"Distancia total: {dt}")
        else:
            st.error("No se pudo calcular la ruta. Verifique las ciudades ingresadas.")
    else:
        st.warning("Por favor, ingrese todos los campos.")
