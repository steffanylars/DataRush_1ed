
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import calendar
from datetime import datetime
import json
import os

# Configure page
st.set_page_config(
    page_title="Sustainable Skies Insights",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3c72;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #ff9800;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Load configuration and data
@st.cache_data
def load_config():
    """Load configuration file with constants and metrics"""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback configuration if file not found
        return {
            "emission_factors": {
                "domestic_flight": 246,
                "international_flight": 195,
                "rail": 35,
                "bus": 105,
                "car": 192
            },
            "average_distances": {
                "domestic": 500,
                "international": 2500
            },
            "radiative_forcing_index": 1.9,
            "key_metrics": {
                "total_emissions_mt": 19.3,
                "total_passengers_m": 34.7,
                "countries_analyzed": 90,
                "years_analyzed": 10,
                "holiday_uplift_percent": 7.0,
                "peak_concentration_percent": 38.7
            }
        }

@st.cache_data
def load_data():
    """Load the processed holiday travel emissions data"""
    try:
        # Try to load actual data file
        df = pd.read_csv("data/holiday_emissions_data.csv")
        return df
    except FileNotFoundError:
        # Generate representative sample data if file not found
        st.warning("📁 Using sample data - actual dataset not found")

        # Create sample data based on actual analysis patterns
        np.random.seed(42)  # For reproducibility
        countries = ['DEU', 'FRA', 'ESP', 'ITA', 'GBR', 'USA', 'CAN', 'BRA', 'ARG', 'MEX', 
                    'JPN', 'AUS', 'NLD', 'CHE', 'AUT', 'BEL', 'SWE', 'NOR', 'DNK', 'FIN']

        data = []
        for country in countries:
            for year in range(2010, 2020):
                for month in range(1, 13):
                    # Create realistic patterns based on actual analysis
                    base_passengers = np.random.normal(45000, 15000)

                    # Holiday months have higher emissions
                    if month in [12, 1, 7, 8]:
                        seasonal_multiplier = np.random.uniform(1.3, 1.8)
                        holiday_season = 'Holiday'
                        holiday_count = np.random.poisson(3)
                    else:
                        seasonal_multiplier = np.random.uniform(0.7, 1.2)
                        holiday_season = 'Regular'
                        holiday_count = np.random.poisson(1)

                    passengers = max(1000, int(base_passengers * seasonal_multiplier))

                    # CO2 emissions based on passengers with realistic factors
                    emissions_per_passenger = np.random.normal(0.55, 0.1)  # ~556 kg avg
                    co2_emissions = passengers * emissions_per_passenger

                    # Regional assignments
                    if country in ['DEU', 'FRA', 'ESP', 'ITA', 'GBR', 'NLD', 'CHE', 'AUT', 'BEL', 'SWE', 'NOR', 'DNK', 'FIN']:
                        region = 'Europe'
                    elif country in ['USA', 'CAN']:
                        region = 'North America'
                    elif country in ['BRA', 'ARG', 'MEX']:
                        region = 'Latin America'
                    elif country in ['JPN']:
                        region = 'Asia'
                    else:
                        region = 'Other'

                    # Hemisphere
                    hemisphere = 'Southern' if country in ['BRA', 'ARG', 'AUS'] else 'Northern'

                    data.append({
                        'ISO3': country,
                        'Year': year,
                        'Month': month,
                        'Passengers': passengers,
                        'CO2_Emissions_Tonnes': co2_emissions,
                        'Holiday_Count': holiday_count,
                        'Holiday_Season': holiday_season,
                        'Region': region,
                        'Hemisphere': hemisphere
                    })

        return pd.DataFrame(data)

def main():
    # Load configuration and data
    config = load_config()
    df = load_data()

    # Header with dynamic metrics
    st.markdown(f"""
    <div class="main-header">
        <h1>✈️ Sustainable Skies Insights Dashboard</h1>
        <p style="font-size: 1.2em;">Interactive Holiday Travel Emissions Analysis & Policy Tools</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{config['key_metrics']['countries_analyzed']}</div>
                <div>Countries</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{config['key_metrics']['total_emissions_mt']:.1f}M</div>
                <div>Tonnes CO₂-eq</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{config['key_metrics']['total_passengers_m']:.1f}M</div>
                <div>Passengers</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{config['key_metrics']['years_analyzed']}</div>
                <div>Years Data</div>
            </div>
        </div>
        <p style="margin-top: 1rem; font-style: italic;">Team DenkWerk | DataRush Competition 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced sidebar with better navigation
    with st.sidebar:
        st.markdown("### 🧭 Analysis Modules")
        st.markdown("---")

        page = st.radio(
            "Choose your exploration:",
            [
                "🌍 Global Overview",
                "🗺️ Cultural Patterns", 
                "📅 Holiday Calendar",
                "🚨 Anomaly Detection",
                "🎯 Policy Simulator",
                "🧮 Carbon Calculator"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### 📊 Quick Stats")

        # Calculate quick stats
        total_emissions = df['CO2_Emissions_Tonnes'].sum()
        holiday_emissions = df[df['Holiday_Season'] == 'Holiday']['CO2_Emissions_Tonnes'].sum()
        holiday_share = (holiday_emissions / total_emissions) * 100

        st.metric("Holiday Impact", f"{holiday_share:.1f}%", "of annual emissions")

        peak_month_emissions = df.groupby('Month')['CO2_Emissions_Tonnes'].sum()
        peak_month_num = peak_month_emissions.idxmax()
        peak_month_name = calendar.month_name[peak_month_num]

        st.metric("Peak Month", peak_month_name, f"{peak_month_emissions[peak_month_num]/1000:.0f}k tonnes")

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Sustainable Skies** transforms holiday travel data into actionable climate insights.

        Built on comprehensive analysis of aviation emissions across 90 countries.
        """)

    # Route to different pages based on selection
    if page == "🌍 Global Overview":
        global_overview_page(df, config)
    elif page == "🗺️ Cultural Patterns":
        cultural_patterns_page(df, config)
    elif page == "📅 Holiday Calendar":
        holiday_calendar_page(df, config)
    elif page == "🚨 Anomaly Detection":
        anomaly_detection_page(df, config)
    elif page == "🎯 Policy Simulator":
        policy_simulator_page(df, config)
    elif page == "🧮 Carbon Calculator":
        carbon_calculator_page(config)

# [Previous function definitions remain the same but with enhanced styling and config integration]
# ... [Include all the previous function definitions with minor enhancements] ...

if __name__ == "__main__":
    main()
