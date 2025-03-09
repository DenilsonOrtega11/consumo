import streamlit as st
import googlemaps
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Initialize Google Maps client
API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]  # Store your API key in Streamlit secrets
gmaps = googlemaps.Client(key=API_KEY)

# Title of the application
st.title("Consumo de combustible entre ciudades")

# User input for origin and destination
origen = st.text_input("Ciudad de Origen", placeholder="Ejemplo: Ciudad de México")
destino = st.text_input("Ciudad de Destino", placeholder="Ejemplo: Monterrey")
peso = st.text_input("Peso", placeholder="Ejemplo: 7200kg")

if st.button("Calcular Consumo"):
    if origen and destino and peso:
        # Request directions from Google Maps API
        directions_result = gmaps.directions(origen, destino, mode="driving", departure_time=datetime.now(),avoid=["tolls", "highways"])

        if directions_result:
            # Extract distance and duration from the response
            distance = directions_result[0]['legs'][0]['distance']['text']
            duration = directions_result[0]['legs'][0]['duration']['text']

            # Display results
            st.success(f"Distancia: {distance}")
            # st.success(f"Duración: {duration}")

            distance_float = distance.replace(",", "")
            distance_float = float((distance_float.split()[0]))

            # Optionally, display a map with the route
            # route = directions_result[0]['overview_polyline']['points']
            # st.map(gmaps.static_map(size="400x400", markers=[origen, destino], path=f"enc:{route}"))

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

            dt = (distance_float+distance_float)
            pt = peso

            prediccion_nueva = pd.DataFrame({x1: [dt], x2: [pt]})
            ct = modelo.predict(prediccion_nueva)
            st.success(f"Consumo de combustible aproximado: {round(ct[0], 3)}")
            st.success(f"Distancia total: {dt}")
        else:
            st.error("No se pudo calcular la ruta. Verifique las ciudades ingresadas.")
    else:
        st.warning("Por favor, ingrese todos los campos.")
