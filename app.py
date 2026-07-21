import os
from datetime import date, datetime

import pandas as pd
import requests
import streamlit as st

SOLAR_API_URL = "https://api.openweathermap.org/energy/1.0/solar/data"
GITHUB_URL = "https://github.com/gituserc1140/Weather-Solar-Irradiance-App"
GITHUB_SPONSOR_URL = "https://github.com/sponsors/gituserc1140"

_CSS = """
<style>
/* ── Page background ─────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d1117, #161b22, #1a1f2e);
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
    background: linear-gradient(90deg, #fbbf24, #f59e0b, #ef4444);
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
    background: linear-gradient(135deg, #f59e0b, #ef4444) !important;
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
    border-right: 1px solid rgba(251,191,36,0.15);
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div { color: #94a3b8 !important; }
[data-testid="stSidebar"] h2 { color: #fbbf24 !important; font-size: 1.1rem; }

/* ── Alerts / spinners ───────────────────────────────────────── */
[data-testid="stAlert"] p { color: #ffffff !important; }
[data-testid="stSpinner"] p { color: #fbbf24 !important; }
</style>
"""

_SIDEBAR_BUTTONS = """
<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:0.4rem 0 1rem;">
  <a href="https://github.com/gituserc1140/Weather-Solar-Irradiance-App" target="_blank"
     style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.35rem 0.85rem;
            border-radius:7px;background:#24292f;color:#f0f6fc !important;
            border:1px solid #444c56;font-weight:600;font-size:0.82rem;text-decoration:none;">
    ⭐ GitHub
  </a>
  <a href="https://github.com/sponsors/gituserc1140" target="_blank"
     style="display:inline-flex;align-items:center;gap:0.35rem;padding:0.35rem 0.85rem;
            border-radius:7px;background:linear-gradient(135deg,#db61a2,#ea4899);
            color:#fff !important;font-weight:600;font-size:0.82rem;text-decoration:none;">
    ❤️ Sponsor
  </a>
</div>
"""


def get_configured_api_key():
    if "OPENWEATHERMAP_API_KEY" in st.secrets:
        return st.secrets["OPENWEATHERMAP_API_KEY"]
    return os.getenv("OPENWEATHERMAP_API_KEY", "")


def fetch_solar_data(api_key, lat, lon, date_str, step, limit):
    params = {
        "lat": lat,
        "lon": lon,
        "date": date_str,
        "step": step,
        "limit": limit,
        "appid": api_key,
    }
    return requests.get(SOLAR_API_URL, params=params, timeout=15)


def render_results(payload):
    records = payload.get("data", [])
    if not records:
        st.info("No solar data returned for the selected parameters.")
        return

    rows = []
    for rec in records:
        ts = datetime.fromtimestamp(rec["timestamp"]).strftime("%Y-%m-%d %H:%M")
        rows.append({
            "Time": ts,
            "GHI (W/m²)": rec.get("gh_irradiance", rec.get("ghi", 0)),
            "DNI (W/m²)": rec.get("dn_irradiance", rec.get("dni", 0)),
            "DHI (W/m²)": rec.get("dh_irradiance", rec.get("dhi", 0)),
            "Cloud Cover (%)": rec.get("cloudy", 0),
            "Sunshine (min)": rec.get("sunshine_duration", 0),
        })

    df = pd.DataFrame(rows).set_index("Time")

    st.success(
        f"✅ Retrieved {len(records)} record(s) — "
        f"lat {payload.get('lat')}, lon {payload.get('lon')}"
    )

    st.subheader("📊 Irradiance Over Time")
    st.line_chart(df[["GHI (W/m²)", "DNI (W/m²)", "DHI (W/m²)"]])

    st.subheader("☁️ Cloud Cover & Sunshine Duration")
    st.bar_chart(df[["Cloud Cover (%)", "Sunshine (min)"]])

    st.subheader("📋 Full Data Table")
    st.dataframe(df, use_container_width=True)


def main():
    st.set_page_config(
        page_title="Weather Solar Irradiance App",
        page_icon="☀️",
        layout="centered",
    )
    st.markdown(_CSS, unsafe_allow_html=True)

    # Hero header
    st.markdown(
        """
        <div class="hero">
            <h1>☀️ Weather Solar Irradiance App</h1>
            <p>Fetch and visualise GHI, DNI, and DHI solar irradiance for any global location.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # GitHub / Sponsor buttons (main area)
    st.markdown(
        """
        <div class="gh-buttons">
          <a class="gh-btn gh-btn-github"
             href="https://github.com/gituserc1140/Weather-Solar-Irradiance-App" target="_blank">
            ⭐ Star on GitHub
          </a>
          <a class="gh-btn gh-btn-sponsor"
             href="https://github.com/sponsors/gituserc1140" target="_blank">
            ❤️ Sponsor
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar — API key + buttons
    st.sidebar.header("⚙️ Settings")
    st.sidebar.markdown(_SIDEBAR_BUTTONS, unsafe_allow_html=True)
    api_key_input = st.sidebar.text_input(
        "OpenWeatherMap API Key",
        type="password",
        help=(
            "Enter your OpenWeatherMap API key. "
            "Get a free key at https://openweathermap.org/api/solar-irradiance"
        ),
    )
    stripped = api_key_input.strip()
    api_key = stripped if stripped else get_configured_api_key()

    if not api_key:
        st.warning(
            "🔑 Please enter your **OpenWeatherMap API key** in the sidebar to continue. "
            "Get a free key at [openweathermap.org](https://openweathermap.org/api/solar-irradiance)."
        )
        st.stop()

    # Location
    st.subheader("📍 Location")
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

    # Query options
    st.subheader("🔧 Query Options")
    col3, col4, col5 = st.columns(3)
    with col3:
        selected_date = st.date_input("Date", value=date.today())
    with col4:
        step_label = st.selectbox(
            "Time Step",
            options=["Hourly (1h)", "3-Hourly (3h)", "Daily"],
            index=0,
        )
    with col5:
        max_records = 16 if step_label == "Daily" else 48
        limit = st.number_input(
            "Max Records", value=min(24, max_records),
            min_value=1, max_value=max_records, step=1,
        )

    step_map = {"Hourly (1h)": 1, "3-Hourly (3h)": 3, "Daily": "day"}
    step = step_map[step_label]

    if st.button("☀️ Fetch Solar Irradiance"):
        with st.spinner("Fetching solar irradiance data…"):
            try:
                response = fetch_solar_data(api_key, lat, lon, str(selected_date), step, int(limit))
            except requests.exceptions.RequestException as exc:
                st.error(f"⚠️ Request failed: {exc}")
                return

        if response.status_code == 200:
            render_results(response.json())
        elif response.status_code == 401:
            st.error("❌ Invalid API key. Please check your OpenWeatherMap API key and try again.")
        elif response.status_code == 429:
            st.error("⚠️ API rate limit exceeded. Please wait before making more requests.")
        else:
            err_data = {}
            try:
                err_data = response.json()
            except Exception:
                pass
            st.error(
                f"❌ API Error {response.status_code}: "
                f"{err_data.get('message', response.text or 'Unknown error')}"
            )


if __name__ == "__main__":
    main()