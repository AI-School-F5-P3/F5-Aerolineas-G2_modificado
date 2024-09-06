import streamlit as st
import requests
from threading import Thread
import subprocess
from utils import data_access
from database import save_to_db

# URL de la API
API_URL = "http://localhost:8000/predict/"

# Función para iniciar la API
def start_api():
    subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

# Iniciar la API en un hilo separado
api_thread = Thread(target=start_api, daemon=True)
api_thread.start()

# Título de la aplicación
st.title('Predicción de Satisfacción del Cliente de Aerolínea G2')

# Menú de navegación
page = st.sidebar.selectbox("Selecciona una página", ["Formulario", "Datos"])

if page == "Formulario":
    # Formulario para ingresar datos
    st.write("""
        Complete los siguientes campos para predecir si el cliente estará satisfecho o no.
    """)

    # Nombre
    name = st.text_input('Nombre', '')

    # Apellidos
    last_name = st.text_input('Apellidos', '')

    # Edad
    age = st.slider('Edad', 0, 100, 30)

    # Distancia de vuelo
    flight_distance = st.slider('Distancia de vuelo (en km)', 0, 5000, 1000)

    # Retraso de salida
    departure_delay = st.slider('Retraso en la salida (minutos)', 0, 240, 15)

    # Retraso de llegada
    arrival_delay = st.slider('Retraso en la llegada (minutos)', 0, 240, 15)

    # Variables categóricas con botones (0 a 5)
    inflight_wifi_service = st.radio('Inflight wifi service', [0, 1, 2, 3, 4, 5])
    departure_arrival_time_convenient = st.radio('Departure/Arrival time convenient', [0, 1, 2, 3, 4, 5])
    ease_of_online_booking = st.radio('Ease of Online booking', [0, 1, 2, 3, 4, 5])
    gate_location = st.radio('Gate location', [0, 1, 2, 3, 4, 5])
    food_and_drink = st.radio('Food and drink', [0, 1, 2, 3, 4, 5])
    online_boarding = st.radio('Online boarding', [0, 1, 2, 3, 4, 5])
    seat_comfort = st.radio('Seat comfort', [0, 1, 2, 3, 4, 5])
    inflight_entertainment = st.radio('Inflight entertainment', [0, 1, 2, 3, 4, 5])
    on_board_service = st.radio('On-board service', [0, 1, 2, 3, 4, 5])
    leg_room_service = st.radio('Leg room service', [0, 1, 2, 3, 4, 5])
    baggage_handling = st.radio('Baggage handling', [0, 1, 2, 3, 4, 5])
    checkin_service = st.radio('Checkin service', [0, 1, 2, 3, 4, 5])
    inflight_service = st.radio('Inflight service', [0, 1, 2, 3, 4, 5])
    cleanliness = st.radio('Cleanliness', [0, 1, 2, 3, 4, 5])

    # Género
    gender = st.selectbox('Género', ['Male', 'Female'])
    gender = 1 if gender == 'Male' else 0

    # Tipo de Cliente
    customer_type = st.selectbox('Tipo de Cliente', ['Loyal Customer', 'Disloyal Customer'])
    customer_type = 1 if customer_type == 'Loyal Customer' else 0

    # Tipo de Viaje
    travel_type = st.selectbox('Tipo de Viaje', ['Personal Travel', 'Business Travel'])
    travel_type = 1 if travel_type == 'Personal Travel' else 0

    # Clase de Viaje
    travel_class = st.selectbox('Clase de Viaje', ['Eco', 'Eco Plus', 'Business'])
    eco = 1 if travel_class == 'Eco' else 0
    eco_plus = 1 if travel_class == 'Eco Plus' else 0
    business = 1 if eco == 0 and eco_plus == 0 else 0

    # Datos de entrada para la API
    input_data = {
        'age': age,
        'flight_distance': flight_distance,
        'inflight_wifi_service': inflight_wifi_service,
        'departure_arrival_time_convenient': departure_arrival_time_convenient,
        'ease_of_online_booking': ease_of_online_booking,
        'gate_location': gate_location,
        'food_and_drink': food_and_drink,
        'online_boarding': online_boarding,
        'seat_comfort': seat_comfort,
        'inflight_entertainment': inflight_entertainment,
        'on_board_service': on_board_service,
        'leg_room_service': leg_room_service,
        'baggage_handling': baggage_handling,
        'checkin_service': checkin_service,
        'inflight_service': inflight_service,
        'cleanliness': cleanliness,
        'departure_delay': departure_delay,
        'arrival_delay': arrival_delay,
        'gender': gender,
        'customer_type': customer_type,
        'travel_type': travel_type,
        'eco': eco,
        'eco_plus': eco_plus,
        'business': business
    }

    # Enviar los datos a la API para obtener la predicción
    if st.button('Predecir Satisfacción'):
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            satisfaction_satisfied = prediction.get('satisfaction')
            st.write(f"Predicción de satisfacción: {satisfaction_satisfied}")
        else:
            st.error("Error al conectar con la API")

    # Enviar los datos a la base de datos
    if st.button('Guardar en la base de datos'):
        data = {
            'name': name,
            'last_name': last_name,
            'age': age,
            'flight_distance': flight_distance,
            'inflight_wifi_service': inflight_wifi_service,
            'departure_arrival_time_convenient': departure_arrival_time_convenient,
            'ease_of_online_booking': ease_of_online_booking,
            'gate_location': gate_location,
            'food_and_drink': food_and_drink,
            'online_boarding': online_boarding,
            'seat_comfort': seat_comfort,
            'inflight_entertainment': inflight_entertainment,
            'on_board_service': on_board_service,
            'leg_room_service': leg_room_service,
            'baggage_handling': baggage_handling,
            'checkin_service': checkin_service,
            'inflight_service': inflight_service,
            'cleanliness': cleanliness,
            'departure_delay': departure_delay,
            'arrival_delay': arrival_delay,
            'gender': gender,
            'customer_type': customer_type,
            'travel_type': travel_type,
            'eco': eco,
            'eco_plus': eco_plus,
            'business': business,
            'satisfaction': satisfaction_satisfied if 'satisfaction_satisfied' in locals() else None  # Asegúrate de usar el valor predicho aquí
        }
        save_to_db(data)
        st.success('Datos guardados con éxito')

elif page == "Datos":
    data_access()