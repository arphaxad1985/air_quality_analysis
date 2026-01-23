import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Insights", layout="wide")

st.title(" Insights")
st.markdown("City comparisons, detailed analysis, and AQI health guidelines")

@st.cache_data
def load_data():
    return pd.read_csv("../datasets/dashboard_df.csv")

df = load_data()

# Sidebar for city selection
with st.sidebar:
    st.header(" Filter Settings")
    
    # City selector
    all_cities = sorted(df['city'].unique())
    selected_cities = st.multiselect(
        "Select Cities for Comparison",
        all_cities,
        default=all_cities[:3] if len(all_cities) > 3 else all_cities
    )
    
    # Metric selector
    metric = st.selectbox(
        "Select Metric for Comparison",
        ["us_aqi", "pm2_5", "temperature_2m", "humidity", "wind_speed"],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    st.markdown("---")
    st.info("Use the filters to customize the comparison view below.")

# Calculate city statistics
if selected_cities:
    filtered_df = df[df['city'].isin(selected_cities)]
else:
    filtered_df = df
    selected_cities = all_cities

city_stats = filtered_df.groupby("city").agg({
    "us_aqi": ["mean", "min", "max", "std"],
    "pm2_5": "mean",
    "temperature_2m": "mean"
}).round(2)

city_stats.columns = ['_'.join(col).strip() for col in city_stats.columns.values]
city_stats = city_stats.reset_index()
city_stats = city_stats.sort_values("us_aqi_mean", ascending=False)

# City Comparison Dashboard
st.header("🏙️ City Comparison Dashboard")

# Create comparison chart
fig = go.Figure()

for idx, row in city_stats.iterrows():
    aqi = row['us_aqi_mean']
    
    # Color coding
    if aqi <= 50:
        color = '#2ECC71'  # Green
        category = "Good"
    elif aqi <= 100:
        color = '#F39C12'  # Orange
        category = "Moderate"
    elif aqi <= 150:
        color = '#E74C3C'  # Red
        category = "Unhealthy"
    else:
        color = '#8B0000'  # Dark Red
        category = "Very Unhealthy"
    
    fig.add_trace(go.Bar(
        x=[row['city']],
        y=[aqi],
        marker_color=color,
        hovertemplate=(
            "<b>%{x}</b><br><br>" +
            "Mean AQI: %{y:.1f}<br>" +
            f"Category: {category}<br>" +
            f"PM2.5: {row['pm2_5_mean']:.1f} µg/m³<br>" +
            f"Temp: {row['temperature_2m_mean']:.1f}°C<br>" +
            "<extra></extra>"
        ),
        text=f"{aqi:.1f}",
        textposition='outside'
    ))

# Add threshold lines
fig.add_hline(y=50, line_dash="dash", line_color="blue",
              annotation_text="Good Air Quality", annotation_position="top left")
fig.add_hline(y=100, line_dash="dot", line_color="orange",
              annotation_text="Moderate", annotation_position="top left")

fig.update_layout(
    title=f"Average {metric.replace('_', ' ').title()} by City",
    xaxis_title="City",
    yaxis_title=f"Average {metric.replace('_', ' ').title()}",
    showlegend=False,
    height=500,
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

# Detailed City Statistics
st.header(" Detailed City Statistics")

# Create formatted table
display_df = city_stats.copy()
display_df.columns = [col.replace('_', ' ').title() for col in display_df.columns]

# Add color coding
def color_aqi(val):
    if val <= 50:
        color = '#d4edda'
    elif val <= 100:
        color = '#fff3cd'
    elif val <= 150:
        color = '#f8d7da'
    else:
        color = '#721c24'
    return f'background-color: {color}; color: {"white" if val > 150 else "black"}'

styled_df = display_df.style.applymap(color_aqi, subset=['Us Aqi Mean']).format({
    'Us Aqi Mean': '{:.1f}',
    'Us Aqi Min': '{:.1f}',
    'Us Aqi Max': '{:.1f}',
    'Us Aqi Std': '{:.2f}',
    'Pm2_5 Mean': '{:.1f}',
    'Temperature 2M Mean': '{:.1f}'
})

st.dataframe(styled_df, use_container_width=True)

# Download button
csv = city_stats.to_csv(index=False)
st.download_button(
    label=" Download Selected Cities Data",
    data=csv,
    file_name="city_aqi_comparison.csv",
    mime="text/csv",
    use_container_width=True
)

# AQI Information Panel
st.header(" AQI Information & Health Guidelines")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 🟢 **Good (0-50)**
    **Air Quality:** Satisfactory  
    **Health Impact:** Minimal risk  
    **Action:** Normal outdoor activities
    """)

with col2:
    st.markdown("""
    ### 🟡 **Moderate (51-100)**
    **Air Quality:** Acceptable  
    **Health Impact:** Sensitive groups affected  
    **Action:** Reduce prolonged exertion
    """)

with col3:
    st.markdown("""
    ### 🟠 **Unhealthy for Sensitive Groups (101-150)**
    **Air Quality:** Unhealthy for some  
    **Health Impact:** Heart/lung disease risks  
    **Action:** Limit outdoor activities
    """)

with col4:
    st.markdown("""
    ### 🔴 **Unhealthy (151-200)**
    **Air Quality:** Unhealthy  
    **Health Impact:** Everyone affected  
    **Action:** Avoid outdoor activities
    """)

st.info("""
**Note:** Based on US EPA AQI standards. AQI above 200 is considered "Very Unhealthy" 
and above 300 is "Hazardous". Sensitive groups include children, elderly, and 
people with respiratory or heart conditions.
""")
