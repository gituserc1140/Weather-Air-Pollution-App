# Solar Irradiance App

This Streamlit app fetches and displays solar irradiance data using the OpenWeatherMap Solar Irradiance API.

## Prerequisites
1. Python 3.7+
2. OpenWeatherMap API Key (sign up at [OpenWeatherMap](https://home.openweathermap.org/)).

## Installation
1. Clone the repository or download the files.
2. Install the required packages:
   ```bash
pip install -r requirements.txt
```
3. Replace `'your_openweathermap_api_key'` in `app.py` with your actual API key.

## Running the App
Run the Streamlit app using the following command:
```bash
streamlit run app.py
```

## Usage
1. Enter the latitude and longitude of the location.
2. Click 'Get Solar Irradiance' to fetch and display the solar irradiance data (represented by UVI).