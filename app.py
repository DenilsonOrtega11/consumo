import streamlit as st
import googlemaps
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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
        directions_result = gmaps.directions(origen, destino, mode="driving", departure_time=datetime.now(), avoid=["tolls", "highways"])

        if directions_result:
            # Extract distance and duration from the response
            distance = directions_result[0]['legs'][0]['distance']['text']
            duration = directions_result[0]['legs'][0]['duration']['text']

            # Display results
            st.success(f"Distancia: {distance}")
            # st.success(f"Duración: {duration}")

            distance_float = distance.replace(",", "")
            distance_float = float((distance_float.split()[0]))

            # Load dataset
            df = pd.read_excel("dataset_MOE.xlsx")

            # Calculate and display the correlation matrix
            correlation_matrix = df[['distancia', 'peso', 'litros']].corr()
            st.write("Matriz de Correlación:")
            st.write(correlation_matrix)

            x1 = "distancia"
            x2 = "peso"
            y = "litros"

            variables_x = [x1, x2]
            variable_y = y
            modelo = LinearRegression()  # generamos la regresión lineal
            modelo.fit(df[variables_x], df[variable_y])  # entrenamos el modelo

            dt = (distance_float + distance_float)
            pt = peso

            prediccion_nueva = pd.DataFrame({x1: [dt], x2: [pt]})
            ct = modelo.predict(prediccion_nueva)
            st.success(f"Consumo de combustible aproximado: {round(ct[0], 3)}")
            st.success(f"Distancia total: {dt}")

            # Evaluate model performance using metrics
            y_true = df[variable_y]  # True values
            y_pred = modelo.predict(df[variables_x])  # Predicted values

            # Calculate the mean squared error
            mse = mean_squared_error(y_true, y_pred)
            st.write(f"Error Cuadrático Medio (MSE): {mse:.3f}")

            # Calculate R squared (R²)
            r2 = r2_score(y_true, y_pred)
            st.write(f"R Cuadrado (R²): {r2:.3f}")

            # Calculate Adjusted R squared (R² ajustado)
            n = len(df)  # number of data points
            p = len(variables_x)  # number of predictors
            r2_adjusted = 1 - (1 - r2) * (n - 1) / (n - p - 1)
            st.write(f"R Cuadrado Ajustado (R² ajustado): {r2_adjusted:.3f}")

        else:
            st.error("No se pudo calcular la ruta. Verifique las ciudades ingresadas.")
    else:
        st.warning("Por favor, ingrese todos los campos.")
