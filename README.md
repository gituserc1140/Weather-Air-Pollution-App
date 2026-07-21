# ☀️ Weather Solar Irradiance App

[![GitHub stars](https://img.shields.io/github/stars/gituserc1140/Weather-Solar-Irradiance-App?style=social)](https://github.com/gituserc1140/Weather-Solar-Irradiance-App)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)

A Streamlit web app that lets you fetch and visualise real-time solar irradiance data (GHI, DNI, DHI) for any location on Earth using the [OpenWeatherMap Solar Irradiance API](https://openweathermap.org/api/solar-irradiance).

---

## Features

- 🔑 **Front-end API key input** — enter your OpenWeatherMap key directly in the app sidebar; no config files required
- 📍 **Location picker** — enter latitude/longitude for any global location
- 📅 **Date & time-step selection** — choose hourly (1 h), 3-hourly, or daily aggregation
- 📊 **Interactive charts** — line chart for GHI/DNI/DHI irradiance, bar chart for cloud cover and sunshine duration
- 📋 **Data table** — full tabular view of all returned records
- 🌙 **Dark theme** — polished gradient UI

---

## Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.8 or newer |
| OpenWeatherMap API key | Free tier available — sign up at [openweathermap.org](https://home.openweathermap.org/users/sign_up) and subscribe to the [Solar Irradiance API](https://openweathermap.org/api/solar-irradiance) |

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

1. **Enter your API key** — paste your OpenWeatherMap API key into the *OpenWeatherMap API Key* field in the left sidebar. The key is masked for security.
2. **Set location** — enter the *Latitude* and *Longitude* of the place you want data for (e.g. London: 51.5074, -0.1278).
3. **Choose query options**:
   - **Date** — the calendar date to query (defaults to today).
   - **Time Step** — `Hourly (1h)`, `3-Hourly (3h)`, or `Daily`.
   - **Max Records** — how many time steps to return (up to 48 for hourly, 16 for daily).
4. **Click ☀️ Fetch Solar Irradiance** — the app calls the API and displays:
   - A line chart of **GHI / DNI / DHI** irradiance (W/m²) over time.
   - A bar chart of **cloud cover (%)** and **sunshine duration (min)**.
   - A full data table you can sort and scroll.

### Solar irradiance terms

| Abbreviation | Meaning |
|---|---|
| **GHI** | Global Horizontal Irradiance — total solar radiation on a horizontal surface (W/m²) |
| **DNI** | Direct Normal Irradiance — beam radiation perpendicular to the sun (W/m²) |
| **DHI** | Diffuse Horizontal Irradiance — scattered sky radiation on a horizontal surface (W/m²) |

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

If you find this app useful, please consider giving it a ⭐ on GitHub or sponsoring the author:

[![Star on GitHub](https://img.shields.io/badge/Star%20on%20GitHub-%E2%AD%90-yellow?logo=github)](https://github.com/gituserc1140/Weather-Solar-Irradiance-App)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?logo=github-sponsors)](https://github.com/sponsors/gituserc1140)
