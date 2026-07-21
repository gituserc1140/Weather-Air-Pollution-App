# Weather Air Pollution App

[![GitHub stars](https://img.shields.io/github/stars/gituserc1140/Weather-Solar-Irradiance-App?style=social)](https://github.com/gituserc1140/Weather-Air-Pollution-App)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://weather-air-pollution-app-f5zdx4sgeuzwlt2pq3pflh.streamlit.app/)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)

A Streamlit web app that lets you fetch and visualise real-time, forecast, and historical air quality data (AQI and pollutant concentrations) for any location on Earth using the free [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution).

---

## Features

- **Front-end API key input** — enter your free OpenWeatherMap key directly in the app sidebar; no config files required
- **Location picker** — enter latitude/longitude for any global location
- **Three data modes** — Current snapshot, Forecast (up to 5 days ahead, hourly), or Historical (custom date range)
- **Interactive charts** — line charts for PM2.5, PM10, O₃, NO₂, CO, and SO₂ concentrations over time
- **Data table** — full tabular view of all returned records including AQI and all 8 pollutant components
- **Dark theme** — polished gradient UI

---

## Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.9 or newer |
| OpenWeatherMap API key | **Free** — sign up at [openweathermap.org](https://home.openweathermap.org/users/sign_up); the Air Pollution API is included in the free plan |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/gituserc1140/Weather-Solar-Irradiance-App.git
cd Weather-Solar-Irradiance-App

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

---

## How to Use

1. **Enter your API key** — paste your free OpenWeatherMap API key into the *OpenWeatherMap API Key* field in the left sidebar. The key is masked for security.
2. **Set location** — enter the *Latitude* and *Longitude* of the place you want data for (e.g. London: 51.5074, -0.1278).
3. **Choose a data mode**:
   - **Current** — fetches the latest air quality snapshot for the location.
   - **Forecast (5 days)** — returns hourly predictions for the next 5 days.
   - **Historical** — pick a start and end date to retrieve past air quality data.
4. **Click Fetch Air Pollution Data** — the app calls the API and displays:
   - Summary metrics for the latest AQI, PM2.5, and PM10 readings.
   - A line chart of **PM2.5 / PM10 / O₃ / NO₂** concentrations (μg/m³) over time.
   - A line chart of **CO** and **SO₂** concentrations over time.
   - A full data table you can sort and scroll.

### Air Quality Index (AQI)

| AQI Value | Level |
|---|---|
| 1 | Good  |
| 2 | Fair  |
| 3 | Moderate  |
| 4 | Poor  |
| 5 | Very Poor  |

### Pollutant components (all in μg/m³)

| Field | Pollutant |
|---|---|
| `co` | Carbon monoxide |
| `no` | Nitrogen monoxide |
| `no2` | Nitrogen dioxide |
| `o3` | Ozone |
| `so2` | Sulphur dioxide |
| `pm2_5` | Fine particulate matter (< 2.5 μm) |
| `pm10` | Coarse particulate matter (< 10 μm) |
| `nh3` | Ammonia |

---

## Optional: pre-configure the API key

If you deploy the app on Streamlit Community Cloud (or another server) and prefer not to enter the key manually each session, you can supply it via:

**Streamlit secrets** (`~/.streamlit/secrets.toml`):
```toml
OPENWEATHERMAP_API_KEY = "your_key_here"
```

**Environment variable**:
```bash
export OPENWEATHERMAP_API_KEY="your_key_here"
streamlit run app.py
```

The sidebar input always takes priority over pre-configured values.

---

## Support the Project

If you find this app useful, please consider giving it a star on GitHub or sponsoring the author:

[![Star on GitHub](https://img.shields.io/badge/Star%20on%20GitHub-%E2%AD%90-yellow?logo=github)](https://github.com/gituserc1140/Weather-Solar-Irradiance-App)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)
