
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
        padding: 1rem;
        border-radius: 10px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white !important;
        margin: 0.5rem 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #e8f4fd !important;
        margin: 0.3rem 0;
        font-size: 1.1rem;
    }
    .main-header em {
        color: #b8d4ea !important;
        font-size: 0.95rem;
    }
    /* Ensure header content is properly styled */
    .main-header * {
        color: inherit !important;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3c72;
    }
    .insight-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: #333333;
    }
    .insight-box h4 {
        color: #2E7D32;
        margin-top: 0;
        font-weight: 600;
    }
    .insight-box ul li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    .insight-box strong {
        color: #1B5E20;
    }
    .warning-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #ff9800;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: #333333;
    }
    .warning-box h4 {
        color: #F57C00;
        margin-top: 0;
        font-weight: 600;
    }
    .warning-box p {
        margin-bottom: 0;
        line-height: 1.5;
    }
    /* Improve general text readability (excluding main header) */
    .stMarkdown:not(.main-header) {
        color: #333333;
    }
    .stMarkdown:not(.main-header) h1, .stMarkdown:not(.main-header) h2, .stMarkdown:not(.main-header) h3, .stMarkdown:not(.main-header) h4 {
        color: #1e3c72;
    }
    /* Improve metric readability */
    .metric-container {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
    }
    /* Better contrast for selectbox and other inputs */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #cccccc;
        color: #333333;
    }
    
    /* Fix dropdown menu options visibility */
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Ensure dropdown options are visible */
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    /* Style dropdown menu items */
    .stSelectbox [role="option"] {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Hover state for dropdown options */
    .stSelectbox [role="option"]:hover {
        background-color: #f0f0f0 !important;
        color: #1e3c72 !important;
    }
    
    /* Selected option styling */
    .stSelectbox [aria-selected="true"] {
        background-color: #e3f2fd !important;
        color: #1e3c72 !important;
    }
    /* Improve slider readability */
    .stSlider > div > div > div {
        color: #333333;
    }
    
    /* Additional dropdown fixes for different Streamlit versions */
    div[data-testid="stSelectbox"] > div {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stSelectbox"] [role="listbox"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    
    div[data-testid="stSelectbox"] [role="option"] {
        background-color: #ffffff !important;
        color: #333333 !important;
        padding: 8px 12px !important;
    }
    
    div[data-testid="stSelectbox"] [role="option"]:hover {
        background-color: #f5f5f5 !important;
        color: #1e3c72 !important;
    }
    
    /* Ensure text in selected value is visible */
    .stSelectbox input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_data():
    """Load realistic holiday travel emissions data with proper trends"""
    # NOTE: This uses generated data for demonstration purposes
    # The Jupyter notebook uses real CSV data from aviation authorities
    # This realistic model ensures valid growth patterns and seasonal trends
    # Create realistic data with actual growth patterns based on aviation industry trends
    
    np.random.seed(42)  # For reproducible results
    
    # Expanded country set for better regional analysis and comparisons
    countries = ['DEU', 'FRA', 'ESP', 'ITA', 'GBR', 'USA', 'BRA', 'ARG', 'MEX', 'CAN', 
                 'PAN', 'PER', 'COL', 'CHN', 'JPN']  # Added Latin America + Asia
    years = list(range(2010, 2020))  # 10 years of data
    months = list(range(1, 13))
    
    data = []
    
    for country in countries:
        # Base emission level varies by country (realistic ranges)
        country_base = {
            # Europe - higher efficiency
            'DEU': 3500, 'FRA': 3200, 'ESP': 2800, 'ITA': 2600, 'GBR': 3800,
            # North America - higher emissions  
            'USA': 8500, 'CAN': 3000,
            # Latin America - moderate levels
            'BRA': 2400, 'ARG': 1800, 'MEX': 2200,
            'PAN': 1500, 'PER': 1900, 'COL': 2100,
            # Asia - varying levels
            'CHN': 7200, 'JPN': 4200
        }[country]
        
        for year_idx, year in enumerate(years):
            # Realistic annual growth: 2-4% per year with some volatility
            annual_growth_factor = 1.02 + (year_idx * 0.015) + np.random.normal(0, 0.02)
            annual_base = country_base * annual_growth_factor
            
            for month in months:
                # Seasonal patterns: holiday months higher
                seasonal_multiplier = 1.0
                if month in [1, 7, 8, 12]:  # Holiday months
                    seasonal_multiplier = 1.15 + np.random.normal(0, 0.05)
                elif month in [6, 11]:  # Shoulder seasons
                    seasonal_multiplier = 1.05 + np.random.normal(0, 0.03)
                else:  # Regular months
                    seasonal_multiplier = 0.95 + np.random.normal(0, 0.03)
                
                # Calculate emissions with realistic variation
                emissions = annual_base * seasonal_multiplier * (1 + np.random.normal(0, 0.1))
                passengers = int(emissions * 20 * (1 + np.random.normal(0, 0.15)))  # Realistic passenger ratio
                
                # Regional classification
                region = {
                    # Europe
                    'DEU': 'Europe', 'FRA': 'Europe', 'ESP': 'Europe', 'ITA': 'Europe', 'GBR': 'Europe',
                    # North America
                    'USA': 'North America', 'CAN': 'North America',
                    # Latin America (expanded)
                    'BRA': 'Latin America', 'ARG': 'Latin America', 'MEX': 'Latin America',
                    'PAN': 'Latin America', 'PER': 'Latin America', 'COL': 'Latin America',
                    # Asia (expanded)
                    'CHN': 'Asia', 'JPN': 'Asia'
                }[country]
                
                data.append({
                    'ISO3': country,
                    'Year': year,
                    'Month': month,
                    'Passengers': max(1000, passengers),  # Ensure positive values
                    'CO2_Emissions_Tonnes': max(100, emissions),  # Ensure positive values
                    'Holiday_Count': np.random.poisson(2 if month in [1, 7, 8, 12] else 1),
                    'Region': region,
                    'Holiday_Season': 'Holiday' if month in [1, 7, 8, 12] else 'Regular'
                })
    
    df = pd.DataFrame(data)
    
    # Add hemisphere information
    southern_countries = ['BRA', 'ARG', 'PER']  # Southern hemisphere countries (Peru added)
    df['Hemisphere'] = df['ISO3'].apply(lambda x: 'Southern' if x in southern_countries else 'Northern')

    return df

# Load constants from our analysis
EMISSION_FACTORS = {
    'domestic_flight': 246,
    'international_flight': 195,
    'rail': 35,
    'bus': 105,
    'car': 192
}

AVERAGE_DISTANCES = {
    'domestic': 500,
    'international': 2500
}

RADIATIVE_FORCING_INDEX = 1.9

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✈️ Sustainable Skies Insights Dashboard</h1>
        <p>Interactive analysis of holiday travel emissions and sustainable intervention opportunities</p>
        <p><em>Enhanced demo with expanded regional coverage (15 countries) • Methodology validated with real aviation data</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("### Analysis Modules")
    page = st.sidebar.radio(
        "Choose your exploration:",
        ["🌍 Global Overview", "🗺️ Cultural Patterns", "📅 Holiday Calendar", 
         "🚨 Anomaly Detection", "🎯 Policy Simulator", "🧮 Carbon Calculator"],
        index=0
    )

    # Route to different pages
    if page == "🌍 Global Overview":
        global_overview_page(df)
    elif page == "🗺️ Cultural Patterns":
        cultural_patterns_page(df)
    elif page == "📅 Holiday Calendar":
        holiday_calendar_page(df)
    elif page == "🚨 Anomaly Detection":
        anomaly_detection_page(df)
    elif page == "🎯 Policy Simulator":
        policy_simulator_page(df)
    elif page == "🧮 Carbon Calculator":
        carbon_calculator_page()

def global_overview_page(df):
    st.header("🌍 Global CO₂ Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    total_emissions = df['CO2_Emissions_Tonnes'].sum() / 1000000  # Convert to Mt
    total_passengers = df['Passengers'].sum() / 1000000  # Convert to millions
    countries_count = df['ISO3'].nunique()
    avg_per_passenger = (df['CO2_Emissions_Tonnes'].sum() / df['Passengers'].sum()) * 1000  # kg per passenger

    with col1:
        st.metric("Total Emissions", f"{total_emissions:.1f} Mt CO₂-eq", "📈 Annual Impact")
    with col2:
        st.metric("Total Passengers", f"{total_passengers:.1f}M", "✈️ Global Reach")
    with col3:
        st.metric("Countries Analyzed", f"{countries_count}", "🌍 Coverage")
    with col4:
        st.metric("Avg per Passenger", f"{avg_per_passenger:.0f} kg CO₂", "👤 Individual Impact")

    col1, col2 = st.columns(2)

    with col1:
        # Regional emissions breakdown
        regional_data = df.groupby('Region')['CO2_Emissions_Tonnes'].sum().reset_index()
        regional_data['Percentage'] = (regional_data['CO2_Emissions_Tonnes'] / 
                                     regional_data['CO2_Emissions_Tonnes'].sum() * 100)

        fig_pie = px.pie(regional_data, values='CO2_Emissions_Tonnes', names='Region',
                        title="🌍 Global Emissions by Region",
                        color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Monthly emissions pattern
        monthly_data = df.groupby('Month')['CO2_Emissions_Tonnes'].sum().reset_index()
        monthly_data['Month_Name'] = monthly_data['Month'].apply(lambda x: calendar.month_abbr[x])
        monthly_data['Is_Holiday'] = monthly_data['Month'].apply(lambda x: x in [1, 7, 8, 12])

        colors = ['#D32F2F' if holiday else '#1976D2' for holiday in monthly_data['Is_Holiday']]

        fig_bar = go.Figure(data=[
            go.Bar(x=monthly_data['Month_Name'], y=monthly_data['CO2_Emissions_Tonnes']/1000,
                  marker_color=colors, name='Monthly Emissions')
        ])
        fig_bar.update_layout(
            title="📅 Monthly Emissions Pattern<br><sub>Holiday months (Jan, Jul, Aug, Dec) in red, regular months in blue</sub>",
            xaxis_title="Month",
            yaxis_title="Emissions (kt CO₂-eq)",
            showlegend=False,
            title_font_size=14
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Holiday impact analysis
    st.subheader("🎄 Holiday Travel Impact Analysis")

    holiday_data = df[df['Holiday_Season'] == 'Holiday']
    regular_data = df[df['Holiday_Season'] == 'Regular']

    holiday_avg = holiday_data['CO2_Emissions_Tonnes'].mean()
    regular_avg = regular_data['CO2_Emissions_Tonnes'].mean()
    holiday_uplift = ((holiday_avg - regular_avg) / regular_avg) * 100

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Holiday Emissions Uplift", f"+{holiday_uplift:.1f}%", "🎉 Seasonal Impact")
    with col2:
        holiday_share = (holiday_data['CO2_Emissions_Tonnes'].sum() / 
                        df['CO2_Emissions_Tonnes'].sum()) * 100
        st.metric("Holiday Share of Annual", f"{holiday_share:.1f}%", "📊 Concentration")
    with col3:
        peak_months = df.groupby('Month')['CO2_Emissions_Tonnes'].sum().nlargest(4)
        peak_concentration = (peak_months.sum() / df['CO2_Emissions_Tonnes'].sum()) * 100
        st.metric("Peak 4 Months Share", f"{peak_concentration:.1f}%", "🔥 Peak Impact")

    # Insights box
    st.markdown(f"""
    <div class="insight-box">
        <h4>🔍 Key Insights</h4>
        <ul>
            <li><strong>Holiday Concentration:</strong> {holiday_share:.1f}% of annual emissions occur during holiday periods</li>
            <li><strong>Peak Impact:</strong> Top 4 months account for {peak_concentration:.1f}% of total emissions</li>
            <li><strong>Intervention Opportunity:</strong> Targeting holiday periods could achieve maximum impact</li>
            <li><strong>Regional Variation:</strong> {regional_data.iloc[0]['Region']} leads with {regional_data.iloc[0]['Percentage']:.1f}% of global emissions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def cultural_patterns_page(df):
    st.header("🗺️ Cultural Pattern Explorer")

    # Country/Region selector
    st.subheader("🎯 Select Region or Country for Analysis")

    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.selectbox("Choose Region", ['All Regions'] + list(df['Region'].unique()))
    with col2:
        if selected_region != 'All Regions':
            available_countries = df[df['Region'] == selected_region]['ISO3'].unique()
        else:
            available_countries = df['ISO3'].unique()
        selected_country = st.selectbox("Choose Country", ['All Countries'] + list(available_countries))

    # Filter data based on selection
    filtered_df = df.copy()
    if selected_region != 'All Regions':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_country != 'All Countries':
        filtered_df = filtered_df[filtered_df['ISO3'] == selected_country]

    col1, col2 = st.columns(2)

    with col1:
        # Monthly pattern for selected region/country
        monthly_pattern = filtered_df.groupby('Month').agg({
            'CO2_Emissions_Tonnes': 'mean',
            'Passengers': 'mean',
            'Holiday_Count': 'mean'
        }).reset_index()

        monthly_pattern['Month_Name'] = monthly_pattern['Month'].apply(lambda x: calendar.month_name[x])

        fig_pattern = make_subplots(specs=[[{"secondary_y": True}]])

        fig_pattern.add_trace(
            go.Scatter(x=monthly_pattern['Month_Name'], y=monthly_pattern['CO2_Emissions_Tonnes'],
                      mode='lines+markers', name='CO₂ Emissions', line=dict(color='#D32F2F', width=3)),
            secondary_y=False,
        )

        fig_pattern.add_trace(
            go.Scatter(x=monthly_pattern['Month_Name'], y=monthly_pattern['Passengers'],
                      mode='lines+markers', name='Passengers', line=dict(color='#1976D2', width=2)),
            secondary_y=True,
        )

        fig_pattern.update_xaxes(title_text="Month")
        fig_pattern.update_yaxes(title_text="CO₂ Emissions (tonnes)", secondary_y=False)
        fig_pattern.update_yaxes(title_text="Passengers", secondary_y=True)

        title_text = f"Monthly Patterns: {selected_country if selected_country != 'All Countries' else selected_region}"
        fig_pattern.update_layout(title_text=title_text, height=400)

        st.plotly_chart(fig_pattern, use_container_width=True)

    with col2:
        # Seasonal comparison - adjust for hemisphere
        if selected_region != 'All Regions' and selected_region in ['Europe', 'North America', 'Asia']:
            # Northern hemisphere seasons
            summer_months = [6, 7, 8]
            winter_months = [12, 1, 2]
        else:  # Southern hemisphere adjustment (Latin America includes southern countries)
            summer_months = [12, 1, 2]
            winter_months = [6, 7, 8]

        summer_data = filtered_df[filtered_df['Month'].isin(summer_months)]['CO2_Emissions_Tonnes'].mean()
        winter_data = filtered_df[filtered_df['Month'].isin(winter_months)]['CO2_Emissions_Tonnes'].mean()
        spring_data = filtered_df[filtered_df['Month'].isin([3, 4, 5])]['CO2_Emissions_Tonnes'].mean()
        autumn_data = filtered_df[filtered_df['Month'].isin([9, 10, 11])]['CO2_Emissions_Tonnes'].mean()

        seasonal_data = pd.DataFrame({
            'Season': ['Spring', 'Summer', 'Autumn', 'Winter'],
            'Emissions': [spring_data, summer_data, autumn_data, winter_data]
        })

        fig_seasonal = px.bar(seasonal_data, x='Season', y='Emissions',
                             title="Seasonal Emissions Comparison",
                             color='Emissions',
                             color_continuous_scale='plasma')
        st.plotly_chart(fig_seasonal, use_container_width=True)

    # Cultural insights based on patterns
    peak_month = monthly_pattern.loc[monthly_pattern['CO2_Emissions_Tonnes'].idxmax(), 'Month_Name']
    peak_value = monthly_pattern['CO2_Emissions_Tonnes'].max()
    min_value = monthly_pattern['CO2_Emissions_Tonnes'].min()
    variation = ((peak_value - min_value) / min_value) * 100

    st.markdown(f"""
    <div class="insight-box">
        <h4>🎭 Cultural Travel Patterns Analysis</h4>
        <ul>
            <li><strong>Peak Travel Month:</strong> {peak_month} ({peak_value:.0f} tonnes CO₂)</li>
            <li><strong>Seasonal Variation:</strong> {variation:.1f}% difference between peak and low months</li>
            <li><strong>Travel Culture:</strong> {"Summer-focused travel pattern" if peak_month in ["July", "August"] else "Winter/Holiday-focused pattern" if peak_month in ["December", "January"] else "Distributed travel pattern"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Side-by-side comparison
    st.subheader("🔄 Compare Two Regions/Countries")

    col1, col2 = st.columns(2)
    with col1:
        compare_region1 = st.selectbox("First Region", df['Region'].unique(), key="comp1")
    with col2:
        compare_region2 = st.selectbox("Second Region", df['Region'].unique(), key="comp2")

    if compare_region1 != compare_region2:
        # Create comparison chart
        region1_data = df[df['Region'] == compare_region1].groupby('Month')['CO2_Emissions_Tonnes'].mean()
        region2_data = df[df['Region'] == compare_region2].groupby('Month')['CO2_Emissions_Tonnes'].mean()

        fig_compare = go.Figure()

        month_names = [calendar.month_abbr[i] for i in range(1, 13)]

        fig_compare.add_trace(go.Scatter(
            x=month_names, y=region1_data.values,
            mode='lines+markers', name=compare_region1,
            line=dict(color='blue', width=3)
        ))

        fig_compare.add_trace(go.Scatter(
            x=month_names, y=region2_data.values,
            mode='lines+markers', name=compare_region2,
            line=dict(color='red', width=3)
        ))

        fig_compare.update_layout(
            title=f"Regional Comparison: {compare_region1} vs {compare_region2}",
            xaxis_title="Month",
            yaxis_title="Average CO₂ Emissions (tonnes)",
            height=400
        )

        st.plotly_chart(fig_compare, use_container_width=True)

def holiday_calendar_page(df):
    st.header("📅 Emissions Calendar & Seasonal Trends")

    # Year selector
    available_years = sorted(df['Year'].unique())
    selected_year = st.selectbox("Select Year for Analysis", available_years)

    # Filter data for selected year
    year_data = df[df['Year'] == selected_year]

    # Create calendar heatmap data
    calendar_data = year_data.groupby(['Month'])['CO2_Emissions_Tonnes'].sum().reset_index()

    # Create a pivot table for heatmap
    months_grid = np.arange(1, 13).reshape(3, 4)  # 3 rows, 4 columns
    month_names = [calendar.month_abbr[i] for i in range(1, 13)]

    # Create heatmap
    emissions_values = []
    for month in range(1, 13):
        if month in calendar_data['Month'].values:
            emissions_values.append(calendar_data[calendar_data['Month'] == month]['CO2_Emissions_Tonnes'].iloc[0])
        else:
            emissions_values.append(0)

    emissions_grid = np.array(emissions_values).reshape(3, 4)

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=emissions_grid,
        x=['Q1 Start', 'Q1 End', 'Q2 End', 'Q3 Start'],
        y=['Jan-Apr', 'May-Aug', 'Sep-Dec'],
        text=[[f"{month_names[i*4+j]}<br>{emissions_grid[i,j]:.0f}t" for j in range(4)] for i in range(3)],
        texttemplate="%{text}",
        textfont={"size": 12},
        colorscale='plasma',
        colorbar=dict(title="CO₂ Emissions (tonnes)")
    ))

    fig_heatmap.update_layout(
        title=f"📅 Emissions Calendar Heatmap - {selected_year}",
        height=400
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Timeline view with holiday markers
    st.subheader("📈 Timeline View with Holiday Markers")

    # Create monthly timeline
    monthly_timeline = year_data.groupby('Month').agg({
        'CO2_Emissions_Tonnes': 'sum',
        'Holiday_Count': 'sum'
    }).reset_index()

    monthly_timeline['Month_Name'] = monthly_timeline['Month'].apply(lambda x: calendar.month_name[x])
    monthly_timeline['Is_Holiday_Month'] = monthly_timeline['Holiday_Count'] > 2

    fig_timeline = go.Figure()

    # Base emissions line
    fig_timeline.add_trace(go.Scatter(
        x=monthly_timeline['Month_Name'],
        y=monthly_timeline['CO2_Emissions_Tonnes'],
        mode='lines+markers',
        name='Monthly Emissions',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))

    # Holiday markers
    holiday_months = monthly_timeline[monthly_timeline['Is_Holiday_Month']]
    if not holiday_months.empty:
        fig_timeline.add_trace(go.Scatter(
            x=holiday_months['Month_Name'],
            y=holiday_months['CO2_Emissions_Tonnes'],
            mode='markers',
            name='Holiday Periods',
            marker=dict(
                size=15,
                color='red',
                symbol='star',
                line=dict(width=2, color='darkred')
            )
        ))

    fig_timeline.update_layout(
        title=f"Emissions Timeline with Holiday Markers - {selected_year}",
        xaxis_title="Month",
        yaxis_title="CO₂ Emissions (tonnes)",
        height=400
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    # Seasonal trend analysis
    col1, col2 = st.columns(2)

    with col1:
        # Year-over-year comparison
        st.subheader("📊 Year-over-Year Trends")
        yearly_data = df.groupby(['Year', 'Month'])['CO2_Emissions_Tonnes'].sum().reset_index()

        fig_yearly = px.line(yearly_data, x='Month', y='CO2_Emissions_Tonnes', 
                            color='Year', title="Multi-Year Monthly Patterns")
        fig_yearly.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=[calendar.month_abbr[i] for i in range(1, 13)]
        )
        st.plotly_chart(fig_yearly, use_container_width=True)

    with col2:
        # Growth analysis
        st.subheader("📈 Growth Analysis")
        
        # Add explanation of data source
        st.markdown("""
        <div class="insight-box">
            <h4>📊 Data Source & Methodology</h4>
            <p><strong>Growth Rate Calculation:</strong> Year-over-year percentage change in total annual emissions</p>
            <p><strong>Data Basis:</strong> Modeled data with realistic aviation industry trends (2-4% annual growth)</p>
            <p><strong>Formula:</strong> Growth Rate = ((Current Year - Previous Year) / Previous Year) × 100</p>
            <p><strong>Industry Context:</strong> Global aviation typically grows 3-5% annually in normal periods</p>
        </div>
        """, unsafe_allow_html=True)
        
        annual_totals = df.groupby('Year')['CO2_Emissions_Tonnes'].sum().reset_index()
        annual_totals['Growth_Rate'] = annual_totals['CO2_Emissions_Tonnes'].pct_change() * 100

        # Display key statistics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            avg_growth = annual_totals['Growth_Rate'].mean()
            st.metric("Average Growth", f"{avg_growth:.1f}%", "📈 Annual Average")
        with col_b:
            max_growth = annual_totals['Growth_Rate'].max()
            st.metric("Peak Growth", f"{max_growth:.1f}%", "🚀 Highest Year")
        with col_c:
            min_growth = annual_totals['Growth_Rate'].min() if not annual_totals['Growth_Rate'].isna().all() else 0
            st.metric("Lowest Growth", f"{min_growth:.1f}%", "📉 Minimum Year")

        fig_growth = go.Figure()
        fig_growth.add_trace(go.Bar(
            x=annual_totals['Year'],
            y=annual_totals['Growth_Rate'],
            name='Annual Growth Rate',
            marker_color=['#2E7D32' if x >= 0 else '#D32F2F' for x in annual_totals['Growth_Rate']],
            text=[f"{x:.1f}%" for x in annual_totals['Growth_Rate']],
            textposition='outside'
        ))

        fig_growth.update_layout(
            title="Annual Emissions Growth Rate (Industry-Realistic Model)",
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            height=450,
            showlegend=False
        )
        st.plotly_chart(fig_growth, use_container_width=True)

def anomaly_detection_page(df):
    st.header("🚨 Anomaly Detector (Event Explorer)")

    st.markdown("""
    This module identifies unusual patterns in travel emissions that deviate from normal seasonal trends,
    helping to understand the impact of external events on aviation patterns.
    """)

    # Calculate monthly averages and identify anomalies
    monthly_avg = df.groupby(['Year', 'Month'])['CO2_Emissions_Tonnes'].sum().reset_index()
    monthly_avg['Date'] = pd.to_datetime(monthly_avg[['Year', 'Month']].assign(day=1))

    # Calculate rolling average for anomaly detection
    monthly_avg = monthly_avg.sort_values('Date')
    monthly_avg['Rolling_Mean'] = monthly_avg['CO2_Emissions_Tonnes'].rolling(window=12, center=True).mean()
    monthly_avg['Rolling_Std'] = monthly_avg['CO2_Emissions_Tonnes'].rolling(window=12, center=True).std()

    # Define anomalies (beyond 2 standard deviations)
    monthly_avg['Upper_Bound'] = monthly_avg['Rolling_Mean'] + 2 * monthly_avg['Rolling_Std']
    monthly_avg['Lower_Bound'] = monthly_avg['Rolling_Mean'] - 2 * monthly_avg['Rolling_Std']

    monthly_avg['Is_Anomaly'] = (
        (monthly_avg['CO2_Emissions_Tonnes'] > monthly_avg['Upper_Bound']) | 
        (monthly_avg['CO2_Emissions_Tonnes'] < monthly_avg['Lower_Bound'])
    )

    # Anomaly timeline chart
    fig_anomaly = go.Figure()

    # Normal data points
    normal_data = monthly_avg[~monthly_avg['Is_Anomaly']]
    fig_anomaly.add_trace(go.Scatter(
        x=normal_data['Date'],
        y=normal_data['CO2_Emissions_Tonnes'],
        mode='lines+markers',
        name='Normal Emissions',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    # Anomaly points
    anomaly_data = monthly_avg[monthly_avg['Is_Anomaly']]
    if not anomaly_data.empty:
        fig_anomaly.add_trace(go.Scatter(
            x=anomaly_data['Date'],
            y=anomaly_data['CO2_Emissions_Tonnes'],
            mode='markers',
            name='Anomalies',
            marker=dict(
                size=12,
                color='red',
                symbol='circle-open',
                line=dict(width=3, color='red')
            )
        ))

    # Add bounds
    fig_anomaly.add_trace(go.Scatter(
        x=monthly_avg['Date'],
        y=monthly_avg['Upper_Bound'],
        mode='lines',
        name='Upper Bound',
        line=dict(color='gray', dash='dash'),
        opacity=0.5
    ))

    fig_anomaly.add_trace(go.Scatter(
        x=monthly_avg['Date'],
        y=monthly_avg['Lower_Bound'],
        mode='lines',
        name='Lower Bound',
        line=dict(color='gray', dash='dash'),
        opacity=0.5,
        fill='tonexty',
        fillcolor='rgba(128,128,128,0.1)'
    ))

    fig_anomaly.update_layout(
        title="🔍 Emissions Anomaly Detection Timeline",
        xaxis_title="Date",
        yaxis_title="CO₂ Emissions (tonnes)",
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig_anomaly, use_container_width=True)

    # Anomaly details table
    if not anomaly_data.empty:
        st.subheader("📋 Detected Anomalies")

        # Create a more detailed anomaly table
        anomaly_details = anomaly_data[['Year', 'Month', 'CO2_Emissions_Tonnes']].copy()
        anomaly_details['Month_Name'] = anomaly_details['Month'].apply(lambda x: calendar.month_name[x])
        anomaly_details['Deviation'] = (
            (anomaly_details['CO2_Emissions_Tonnes'] - monthly_avg.loc[anomaly_details.index, 'Rolling_Mean']) /
            monthly_avg.loc[anomaly_details.index, 'Rolling_Std']
        ).round(2)
        anomaly_details['Type'] = anomaly_details['Deviation'].apply(lambda x: 'High Spike' if x > 0 else 'Unusual Drop')

        # Add potential explanations
        explanations = {
            (2020, 3): "COVID-19 pandemic onset - travel restrictions",
            (2020, 4): "Global lockdowns - minimal travel",
            (2010, 4): "Icelandic volcanic ash - flight disruptions", 
            (2008, 12): "Financial crisis impact on holiday travel",
            (2016, 7): "Summer Olympics boost",
        }

        anomaly_details['Potential_Cause'] = anomaly_details.apply(
            lambda row: explanations.get((int(row['Year']), int(row['Month'])), "Unknown external factor"),
            axis=1
        )

        st.dataframe(
            anomaly_details[['Year', 'Month_Name', 'CO2_Emissions_Tonnes', 'Type', 'Deviation', 'Potential_Cause']],
            column_config={
                'Year': 'Year',
                'Month_Name': 'Month',
                'CO2_Emissions_Tonnes': st.column_config.NumberColumn('Emissions (tonnes)', format="%.0f"),
                'Type': 'Anomaly Type',
                'Deviation': st.column_config.NumberColumn('Std Deviation', format="%.1f"),
                'Potential_Cause': 'Potential Cause'
            }
        )
    else:
        st.info("No significant anomalies detected in the current dataset.")

    # Anomaly statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        anomaly_count = len(anomaly_data)
        total_points = len(monthly_avg)
        anomaly_rate = (anomaly_count / total_points) * 100
        st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%", f"{anomaly_count} out of {total_points} months")

    with col2:
        if anomaly_count > 0:
            avg_deviation = anomaly_details['Deviation'].abs().mean()
            st.metric("Avg Deviation", f"{avg_deviation:.1f}σ", "Standard deviations")
        else:
            st.metric("Avg Deviation", "0.0σ", "No anomalies")

    with col3:
        if anomaly_count > 0:
            high_spikes = len(anomaly_details[anomaly_details['Type'] == 'High Spike'])
            unusual_drops = anomaly_count - high_spikes
            st.metric("Spike/Drop Ratio", f"{high_spikes}:{unusual_drops}", "High vs Low anomalies")
        else:
            st.metric("Spike/Drop Ratio", "0:0", "No anomalies")

def policy_simulator_page(df):
    st.header("🎯 Holiday Impact Simulator")

    st.markdown("""
    Simulate the impact of various policy interventions on holiday travel emissions.
    Adjust the sliders to see how different measures could reduce CO₂ emissions.
    """)

    # Current baseline
    baseline_emissions = df['CO2_Emissions_Tonnes'].sum()

    st.subheader("🔧 Policy Intervention Controls")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🚄 Modal Shift Policies")
        rail_shift = st.slider("High-speed rail adoption (%)", 0, 50, 15, 5,
                              help="Percentage of short-haul flights shifted to rail")

        bus_shift = st.slider("Enhanced bus/coach networks (%)", 0, 30, 10, 5,
                             help="Percentage of medium-distance flights shifted to bus")

        st.markdown("#### ⛽ Technology Interventions")
        saf_adoption = st.slider("Sustainable Aviation Fuel adoption (%)", 0, 100, 25, 5,
                                help="Percentage of flights using SAF")

        fleet_efficiency = st.slider("Fleet efficiency improvement (%)", 0, 30, 10, 2,
                                    help="Efficiency gains from newer aircraft")

    with col2:
        st.markdown("#### 💰 Economic Measures")
        carbon_tax = st.slider("Carbon tax level (€/tonne CO₂)", 0, 200, 50, 10,
                              help="Carbon pricing to reduce demand")

        peak_surcharge = st.slider("Holiday period surcharge (%)", 0, 50, 15, 5,
                                  help="Additional charges during peak periods")

        st.markdown("#### 📱 Behavioral Interventions")
        telecommuting = st.slider("Remote work adoption (%)", 0, 50, 20, 5,
                                 help="Reduction in business travel")

        local_tourism = st.slider("Local tourism promotion (%)", 0, 40, 15, 5,
                                 help="Shift to domestic/local destinations")

    # Calculate impacts based on research-backed coefficients
    def calculate_emission_reduction():
        # Modal shift impacts (based on efficiency differences)
        rail_reduction = rail_shift * 0.85  # Rail is 85% more efficient
        bus_reduction = bus_shift * 0.45   # Bus is 45% more efficient

        # Technology impacts
        saf_reduction = saf_adoption * 0.80  # SAF reduces emissions by 80%
        efficiency_reduction = fleet_efficiency * 0.95  # Almost 1:1 efficiency gain

        # Economic impacts (price elasticity of demand)
        carbon_tax_reduction = carbon_tax * 0.12  # -0.12% demand per €1 carbon tax
        surcharge_reduction = peak_surcharge * 0.08  # Targeted at peak periods

        # Behavioral impacts
        telecommute_reduction = telecommuting * 0.15  # 15% of travel is business
        local_reduction = local_tourism * 0.25  # Promotes shorter trips

        # Calculate total reduction (with diminishing returns)
        total_reduction = min(80, 
            rail_reduction + bus_reduction + 
            saf_reduction * 0.7 + efficiency_reduction * 0.5 +  # Partial overlap
            carbon_tax_reduction * 0.6 + surcharge_reduction * 0.8 +  # Complementary
            telecommute_reduction + local_reduction * 0.6
        )

        return total_reduction, {
            'modal_shift': rail_reduction + bus_reduction,
            'technology': saf_reduction * 0.7 + efficiency_reduction * 0.5,
            'economic': carbon_tax_reduction * 0.6 + surcharge_reduction * 0.8,
            'behavioral': telecommute_reduction + local_reduction * 0.6
        }

    total_reduction, category_impacts = calculate_emission_reduction()
    new_emissions = baseline_emissions * (1 - total_reduction/100)
    emissions_saved = baseline_emissions - new_emissions

    # Results visualization
    st.subheader("📊 Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Reduction", f"{total_reduction:.1f}%", 
                 f"{emissions_saved/1000000:.1f}M tonnes saved")
    with col2:
        st.metric("New Annual Emissions", f"{new_emissions/1000000:.1f}M tonnes",
                 f"vs {baseline_emissions/1000000:.1f}M baseline")
    with col3:
        economic_value = emissions_saved * 150 / 1000000  # €150 per tonne
        st.metric("Economic Value", f"€{economic_value:.0f}M", "Carbon credit value")
    with col4:
        passengers_affected = df['Passengers'].sum() * total_reduction / 100
        st.metric("Passengers Affected", f"{passengers_affected/1000000:.1f}M", "Travel pattern changes")

    # Impact breakdown chart
    col1, col2 = st.columns(2)

    with col1:
        categories = ['Modal Shift', 'Technology', 'Economic', 'Behavioral']
        impacts = [category_impacts['modal_shift'], category_impacts['technology'],
                  category_impacts['economic'], category_impacts['behavioral']]

        fig_breakdown = px.bar(
            x=categories, y=impacts,
            title="Policy Impact Breakdown",
            labels={'x': 'Policy Category', 'y': 'Emission Reduction (%)'},
            color=impacts,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)

    with col2:
        # Scenario comparison
        scenarios = {
            'Business as Usual': 0,
            'Conservative': total_reduction * 0.3,
            'Current Settings': total_reduction,
            'Aggressive': min(total_reduction * 1.5, 75)
        }

        scenario_emissions = [baseline_emissions * (1 - r/100) / 1000000 for r in scenarios.values()]

        fig_scenarios = px.bar(
            x=list(scenarios.keys()), y=scenario_emissions,
            title="Scenario Comparison",
            labels={'x': 'Scenario', 'y': 'Annual Emissions (Mt CO₂)'},
            color=scenario_emissions,
            color_continuous_scale='plasma_r'
        )
        st.plotly_chart(fig_scenarios, use_container_width=True)

    # Implementation roadmap
    st.subheader("🗺️ Implementation Roadmap")

    if total_reduction > 0:
        phases = {
            'Phase 1 (0-2 years)': ['Carbon pricing', 'SAF pilot programs', 'Rail investment'],
            'Phase 2 (2-5 years)': ['Fleet modernization', 'Modal shift infrastructure', 'Behavioral campaigns'],
            'Phase 3 (5-10 years)': ['Full SAF deployment', 'Complete rail networks', 'Cultural shift achieved']
        }

        phase_reductions = [total_reduction * 0.2, total_reduction * 0.6, total_reduction * 1.0]

        for i, (phase, actions) in enumerate(phases.items()):
            with st.expander(f"{phase} - Target: {phase_reductions[i]:.1f}% reduction"):
                for action in actions:
                    st.write(f"• {action}")

                st.progress(min(phase_reductions[i]/50, 1.0))

    # Warning for extreme scenarios
    if total_reduction > 60:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Implementation Warning</h4>
            <p>This scenario requires very aggressive policy implementation and may face significant 
            political and economic resistance. Consider a phased approach with stakeholder engagement.</p>
        </div>
        """, unsafe_allow_html=True)

def carbon_calculator_page():
    st.header("🧮 Personal Carbon Calculator")

    st.markdown("""
    Calculate the carbon footprint of your holiday travels and explore alternatives.
    This tool uses the same emission factors from our research analysis.
    """)

    # Trip input form
    with st.form("carbon_calculator"):
        st.subheader("✈️ Trip Details")

        col1, col2 = st.columns(2)

        with col1:
            departure = st.text_input("Departure City", value="New York")
            arrival = st.text_input("Arrival City", value="London")

            trip_type = st.selectbox("Trip Type", ["Round Trip", "One Way"])
            passengers = st.number_input("Number of Passengers", min_value=1, max_value=10, value=1)

        with col2:
            distance = st.number_input("Flight Distance (km)", min_value=100, max_value=20000, value=5585,
                                     help="Approximate distance between cities")

            flight_class = st.selectbox("Travel Class", ["Economy", "Business", "First"])

            travel_month = st.selectbox("Travel Month", 
                                      [calendar.month_name[i] for i in range(1, 13)],
                                      index=6)  # Default to July

        calculate_button = st.form_submit_button("Calculate Carbon Footprint", type="primary")

    if calculate_button:
        # Emission calculation
        if distance <= 1500:
            base_emission_factor = EMISSION_FACTORS['domestic_flight']
        else:
            base_emission_factor = EMISSION_FACTORS['international_flight']

        # Class multipliers
        class_multipliers = {"Economy": 1.0, "Business": 2.5, "First": 4.0}
        class_multiplier = class_multipliers[flight_class]

        # Calculate emissions
        trip_multiplier = 2 if trip_type == "Round Trip" else 1

        # Base calculation: distance × emission factor × passengers × class × trip type
        base_emissions_kg = (distance * base_emission_factor * passengers * 
                            class_multiplier * trip_multiplier) / 1000  # Convert to kg

        # Apply radiative forcing index
        total_emissions_kg = base_emissions_kg * RADIATIVE_FORCING_INDEX
        total_emissions_tonnes = total_emissions_kg / 1000

        # Results display
        st.subheader("📊 Your Carbon Footprint Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("CO₂ Emissions", f"{total_emissions_kg:.0f} kg", 
                     f"{total_emissions_tonnes:.2f} tonnes")

        with col2:
            # Compare to annual average
            annual_per_person = 4.8  # tonnes CO₂ per person per year (global average)
            percentage_of_annual = (total_emissions_tonnes / annual_per_person) * 100
            st.metric("% of Annual Footprint", f"{percentage_of_annual:.1f}%",
                     f"vs {annual_per_person}t/year average")

        with col3:
            # Economic value
            carbon_price = 50  # €50 per tonne (average)
            cost_to_offset = total_emissions_tonnes * carbon_price
            st.metric("Offset Cost", f"€{cost_to_offset:.0f}", "At €50/tonne CO₂")

        # Alternative transport comparison
        st.subheader("🚄 Alternative Transport Comparison")

        # Calculate alternatives
        rail_emissions = (distance * EMISSION_FACTORS['rail'] * passengers * trip_multiplier) / 1000
        bus_emissions = (distance * EMISSION_FACTORS['bus'] * passengers * trip_multiplier) / 1000
        car_emissions = (distance * EMISSION_FACTORS['car'] * passengers * trip_multiplier) / 1000

        alternatives_data = pd.DataFrame({
            'Transport': ['Flight (Current)', 'High-Speed Rail', 'Bus/Coach', 'Car (shared)'],
            'Emissions_kg': [total_emissions_kg, rail_emissions, bus_emissions, car_emissions],
            'Feasible': ['✅', '🤔' if distance < 2000 else '❌', 
                        '🤔' if distance < 1000 else '❌',
                        '🤔' if distance < 1500 else '❌']
        })

        alternatives_data['Reduction_vs_Flight'] = (
            (alternatives_data.loc[0, 'Emissions_kg'] - alternatives_data['Emissions_kg']) /
            alternatives_data.loc[0, 'Emissions_kg'] * 100
        ).round(1)

        fig_alternatives = px.bar(
            alternatives_data, x='Transport', y='Emissions_kg',
            title="Carbon Footprint by Transport Mode",
            color='Emissions_kg',
            color_continuous_scale='inferno_r',
            text='Feasible'
        )
        fig_alternatives.update_traces(textposition='outside')
        fig_alternatives.update_layout(
            yaxis_title="CO₂ Emissions (kg)",
            height=400
        )
        st.plotly_chart(fig_alternatives, use_container_width=True)

        # Offsetting options
        st.subheader("🌱 Carbon Offsetting Options")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Tree Planting")
            trees_needed = total_emissions_tonnes / 0.025  # 25kg CO₂ per tree per year
            st.write(f"🌳 **{trees_needed:.0f} trees** needed to offset this trip")
            st.write("*(Based on average tree absorption of 25kg CO₂/year)*")

            st.markdown("#### Renewable Energy")
            solar_panels = total_emissions_tonnes / 0.5  # 0.5 tonnes CO₂ avoided per panel per year
            st.write(f"☀️ **{solar_panels:.1f} solar panels** for one year")
            st.write("*(Based on average solar panel impact)*")

        with col2:
            st.markdown("#### Travel Alternatives")
            if distance < 1500:
                st.write("✅ Consider train travel for this route")
                st.write(f"🚄 Rail would save **{(total_emissions_kg - rail_emissions):.0f} kg CO₂**")

            if distance < 3000:
                st.write("💡 Consider extending your stay to make the trip more worthwhile")
                days_recommended = max(7, distance / 500)
                st.write(f"📅 Recommended minimum stay: **{days_recommended:.0f} days**")

        # Holiday travel context
        travel_month_num = list(calendar.month_name).index(travel_month)
        if travel_month_num in [1, 7, 8, 12]:
            st.markdown("""
            <div class="warning-box">
                <h4>🎄 Holiday Travel Period</h4>
                <p>You're traveling during a peak holiday month! Consider:</p>
                <ul>
                    <li>Traveling during off-peak months for lower emissions (fewer flights needed)</li>
                    <li>Booking early to ensure efficient flight routing</li>
                    <li>Choosing direct flights when possible</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Personal recommendations
        st.subheader("💡 Personalized Recommendations")

        recommendations = []

        if flight_class != "Economy":
            economy_savings = total_emissions_kg * (1 - 1/class_multiplier)
            recommendations.append(f"Switch to Economy class to save {economy_savings:.0f} kg CO₂")

        if distance > 3000 and trip_type == "Round Trip":
            recommendations.append("For long-distance trips, consider staying longer to maximize the value")

        if total_emissions_tonnes > 2:
            recommendations.append("This is a high-impact trip - consider offsetting through verified programs")

        if percentage_of_annual > 20:
            recommendations.append("This trip represents a large portion of your annual carbon budget")

        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

        if not recommendations:
            st.write("✅ This appears to be a relatively efficient travel choice!")

if __name__ == "__main__":
    main()
