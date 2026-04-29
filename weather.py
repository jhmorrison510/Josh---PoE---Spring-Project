#imports
import streamlit as st
import requests

lat = 37.806396
lon = -122.21545

url = "https://api.open-meteo.com/v1/forecast"

params = {
	"latitude": lat,
	"longitude": lon,
	"minutely_15": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m"],
	"forecast_days": 1,
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
}

#weather function
@st.cache_data(ttl=60)
def get_weather():
    try:
        response = requests.get(url, params=params, timeout=25)
        response.raise_for_status()

        data = response.json()
        minute_data = data.get("minutely_15", {})

        temps = minute_data.get("temperature_2m", [])
        winds = minute_data.get("wind_speed_10m", [])
        humidities = minute_data.get("relative_humidity_2m", [])

        if not temps or not winds or not humidities:
            return None, None, None

        temperature = round(temps[-1], 1)
        wind_speed = round(winds[-1], 1)
        humidity = round(humidities[-1], 1)

        return temperature, wind_speed, humidity

    except Exception:
        return None, None, None


#delta calculation
def get_deltas(temp, wind, humidity):

    if "prev_temp" not in st.session_state:
        st.session_state.prev_temp = temp
    if "prev_wind" not in st.session_state:
        st.session_state.prev_wind = wind
    if "prev_humidity" not in st.session_state:
        st.session_state.prev_humidity = humidity

    temp_delta = round(temp - st.session_state.prev_temp, 1)
    wind_delta = round(wind - st.session_state.prev_wind, 1)
    humidity_delta = round(humidity - st.session_state.prev_humidity, 1)

    st.session_state.prev_temp = temp
    st.session_state.prev_wind = wind
    st.session_state.prev_humidity = humidity

    return temp_delta, wind_delta, humidity_delta