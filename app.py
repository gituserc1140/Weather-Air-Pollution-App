import streamlit as st
import requests
from datetime import datetime

# OpenWeatherMap API configuration
API_KEY = 'your_openweathermap_api_key'
BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall'

def get_solar_irradiance(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'current,minutely,hourly,alerts',
        'appid': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if response.status_code == 200:
        return data['daily'][0]['uvi']  # UVI is used as a proxy for solar irradiance
    else:
        st.error(f'Error fetching data: {data.get("message", "Unknown error")}')
        return None

def main():
    st.title('Solar Irradiance App')
    st.write('Enter the latitude and longitude to get the solar irradiance data.')

    lat = st.number_input('Latitude', value=37.7749, step=0.0001)
    lon = st.number_input('Longitude', value=-122.4194, step=0.0001)

    if st.button('Get Solar Irradiance'):
        irradiance = get_solar_irradiance(lat, lon)
        if irradiance is not None:
            st.success(f'Solar Irradiance (UVI): {irradiance}')

if __name__ == '__main__':
    main()