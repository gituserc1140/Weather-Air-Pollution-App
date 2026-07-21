import os
from datetime import date, datetime, timedelta, timezone

import pandas as pd
import requests
import streamlit as st

AIR_POLLUTION_BASE_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
GITHUB_URL = "https://github.com/gituserc1140/Weather-Air-Pollution-App"
GITHUB_SPONSOR_URL = "https://github.com/sponsors/gituserc1140"

AQI_LABELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

_CSS = """
<style>
/* ── Page background ─────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d1117, #161b22, #0d1f2d);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Hero banner ─────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #34d399, #3b82f6, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0;
}

/* ── GitHub buttons row ──────────────────────────────────────── */
.gh-buttons {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0.5rem 0 1.5rem;
}
.gh-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.45rem 1.1rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none !important;
    transition: opacity 0.2s;
}
.gh-btn:hover { opacity: 0.82; }
.gh-btn-github {
    background: #24292f;
    color: #f0f6fc !important;
    border: 1px solid #444c56;
}
.gh-btn-sponsor {
    background: linear-gradient(135deg, #db61a2, #ea4899);
    color: #fff !important;
    border: none;
}

/* ── Fetch button ────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #34d399, #3b82f6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* ── Sidebar ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(13,17,23,0.92);
    border-right: 1px solid rgba(52,211,153,0.15);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #94a3b8 !important; }
[data-testid="stSidebar"] h2 { color: #34d399 !important; font-size: 1.1rem; }

/* ── Alerts / spinners ───────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }
[data-testid="stSpinner"] p { color: #34d399 !important; }
</style>
"""

_SIDEBAR_BUTTONS = """
<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:0.4rem 0 1rem;">
  <a href="https://github.com/gituserc1140/Weather-Air-Pollution-App" target="_blank"
     style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.35rem 0.85rem;
            border-radius:7px;background:#24292f;color:#f0f6fc !important;
            border:1px solid #444c56;font-weight:600;font-size:0.82rem;text-decoration:none;">
    GitHub
  </a>
  <a href="https://github.com/sponsors/gituserc1140" target="_blank"
     style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.35rem 0.85rem;
            border-radius:7px;background:linear-gradient(135deg,#db61a2,#ea4899);
            color:#fff !important;font-weight:600;font-size:0.82rem;text-decoration:none;">
    Sponsor
  </a>
</div>
"""


def get_configured_api_key():
    if "OPENWEATHERMAP_API_KEY" in st.secrets:
        return st.secrets["OPENWEATHERMAP_API_KEY"]
    return os.getenv("OPENWEATHERMAP_API_KEY", "")


def fetch_air_pollution_data(api_key, lat, lon, mode, start_ts=None, end_ts=None):
    """Fetch air pollution data from OpenWeatherMap.

    mode: "current" | "forecast" | "historical"
    start_ts / end_ts: Unix timestamps required for historical mode.
    """
    if mode == "current":
        url = AIR_POLLUTION_BASE_URL
        params = {"lat": lat, "lon": lon, "appid": api_key}
    elif mode == "forecast":
        url = f"{AIR_POLLUTION_BASE_URL}/forecast"
        params = {"lat": lat, "lon": lon, "appid": api_key}
    else:  # historical
        url = f"{AIR_POLLUTION_BASE_URL}/history"
        params = {"lat": lat, "lon": lon, "start": start_ts, "end": end_ts, "appid": api_key}
    return requests.get(url, params=params, timeout=15)


def render_results(payload, lat, lon):
    records = payload.get("list", [])
    if not records:
        st.info("No air pollution data returned for the selected parameters.")
        return

    rows = []
    for rec in records:
        ts = datetime.fromtimestamp(rec["dt"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        comp = rec.get("components", {})
        rows.append({
            "Time": ts,
            "AQI": rec.get("main", {}).get("aqi", None),
            "CO (μg/m³)": comp.get("co", 0),
            "NO (μg/m³)": comp.get("no", 0),
            "NO₂ (μg/m³)": comp.get("no2", 0),
            "O₃ (μg/m³)": comp.get("o3", 0),
            "SO₂ (μg/m³)": comp.get("so2", 0),
            "PM2.5 (μg/m³)": comp.get("pm2_5", 0),
            "PM10 (μg/m³)": comp.get("pm10", 0),
            "NH₃ (μg/m³)": comp.get("nh3", 0),
        })

    df = pd.DataFrame(rows).set_index("Time")

    # Summary metric for current / latest record
    latest_aqi = int(df["AQI"].iloc[0]) if pd.notna(df["AQI"].iloc[0]) else None
    aqi_label = AQI_LABELS.get(latest_aqi, "Unknown")

    st.success(
        f"Retrieved {len(records)} record(s) — lat {lat}, lon {lon}"
    )

    col_aqi, col_pm25, col_pm10 = st.columns(3)
    col_aqi.metric("Air Quality Index (latest)", aqi_label)
    col_pm25.metric("PM2.5 — latest (μg/m³)", f"{df['PM2.5 (μg/m³)'].iloc[0]:.2f}")
    col_pm10.metric("PM10 — latest (μg/m³)", f"{df['PM10 (μg/m³)'].iloc[0]:.2f}")

    st.subheader("Key Pollutants Over Time")
    st.line_chart(df[["PM2.5 (μg/m³)", "PM10 (μg/m³)", "O₃ (μg/m³)", "NO₂ (μg/m³)"]])

    st.subheader("CO & SO₂ Over Time")
    st.line_chart(df[["CO (μg/m³)", "SO₂ (μg/m³)"]])

    st.subheader("Full Data Table")
    st.dataframe(df, use_container_width=True)


def main():
    st.set_page_config(
        page_title="Weather Air Pollution App",
        page_icon=None,
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # Hero header
    st.markdown(
        """
        <div class="hero">
            <h1>Weather Air Pollution App</h1>
            <p>Fetch and visualise real-time, forecast, and historical air quality data for any global location.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # GitHub / Sponsor buttons (main area)
    st.markdown(
        """
        <div class="gh-buttons">
          <a class="gh-btn gh-btn-github"
             href="https://github.com/gituserc1140/Weather-Air-Pollution-App" target="_blank">
            Star on GitHub
          </a>
          <a class="gh-btn gh-btn-sponsor"
             href="https://github.com/sponsors/gituserc1140" target="_blank">
            Sponsor
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar — API key + buttons
    st.sidebar.header("Settings")
    st.sidebar.markdown(_SIDEBAR_BUTTONS, unsafe_allow_html=True)
    api_key_input = st.sidebar.text_input(
        "OpenWeatherMap API Key",
        type="password",
        help=(
            "Enter your free OpenWeatherMap API key. "
            "Get one at https://openweathermap.org/api/air-pollution"
        ),
    )
    stripped = api_key_input.strip()
    api_key = stripped if stripped else get_configured_api_key()

    if not api_key:
        st.warning(
            "Please enter your **OpenWeatherMap API key** in the sidebar to continue. "
            "Get a free key at [openweathermap.org](https://openweathermap.org/api/air-pollution)."
        )
        st.stop()

    # Location
    st.subheader("Location")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input(
            "Latitude", value=51.5074, min_value=-90.0, max_value=90.0,
            step=0.0001, format="%.4f",
        )
    with col2:
        lon = st.number_input(
            "Longitude", value=-0.1278, min_value=-180.0, max_value=180.0,
            step=0.0001, format="%.4f",
        )

    # Query mode
    st.subheader("Query Options")
    mode = st.radio(
        "Data Mode",
        options=["Current", "Forecast (5 days)", "Historical"],
        horizontal=True,
        help=(
            "**Current** — latest AQI snapshot. "
            "**Forecast** — hourly predictions up to 5 days ahead. "
            "**Historical** — past data by date range (up to 1 year back)."
        ),
    )

    start_ts = end_ts = None
    if mode == "Historical":
        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input(
                "Start Date",
                value=date.today() - timedelta(days=7),
                max_value=date.today(),
            )
        with col4:
            end_date = st.date_input(
                "End Date",
                value=date.today(),
                max_value=date.today(),
            )
        if start_date > end_date:
            st.error("Start date must be before or equal to end date.")
            st.stop()
        start_ts = int(datetime(start_date.year, start_date.month, start_date.day,
                                tzinfo=timezone.utc).timestamp())
        end_ts = int(datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59,
                              tzinfo=timezone.utc).timestamp())

    mode_key = {"Current": "current", "Forecast (5 days)": "forecast", "Historical": "historical"}[mode]

    if st.button("Fetch Air Pollution Data"):
        with st.spinner("Fetching air pollution data…"):
            try:
                response = fetch_air_pollution_data(api_key, lat, lon, mode_key, start_ts, end_ts)
            except requests.exceptions.RequestException as exc:
                st.error(f"Request failed: {exc}")
                return

        if response.status_code == 200:
            render_results(response.json(), lat, lon)
        elif response.status_code == 401:
            st.error("Invalid API key. Please check your OpenWeatherMap API key and try again.")
        elif response.status_code == 429:
            st.error("API rate limit exceeded. Please wait before making more requests.")
        else:
            err_data = {}
            try:
                err_data = response.json()
            except Exception:
                pass
            st.error(
                f"API Error {response.status_code}: "
                f"{err_data.get('message', response.text or 'Unknown error')}"
            )


if __name__ == "__main__":
    main()