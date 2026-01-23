import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Air Quality & Weather Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .nav-button {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .page-container {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌫️ Air Quality & Weather Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analysing the influence of weather conditions on air pollution levels</p>', unsafe_allow_html=True)

# Navigation
st.markdown("---")
st.markdown("## 📋 Navigation")

# Create 4 columns for navigation buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(" **Overview**", use_container_width=True):
        st.switch_page("pages/1_Overview.py")

with col2:
    if st.button(" **Insights**", use_container_width=True):
        st.switch_page("pages/2_Insights.py")

with col3:
    if st.button(" **Monitoring**", use_container_width=True):
        st.switch_page("pages/3_Monitoring.py")

with col4:
    if st.button(" **Predictions**", use_container_width=True):
        st.switch_page("pages/4_Predictions.py")

# Description
st.markdown("---")
st.info("""
**Dashboard Overview:**
- ** Overview**: Dataset preview, basic statistics, and visualizations
- ** Insights**: City comparisons, detailed analysis, and AQI guidelines  
- ** Monitoring**: Real-time trends, correlations, and city explorer
- ** Predictions**: Atmospheric regime clustering and AQI risk forecasting
""")

# Quick stats preview
@st.cache_data
def load_preview():
    import pandas as pd
    df = pd.read_csv("../datasets/dashboard_df.csv")
    return df

df = load_preview()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cities", df["city"].nunique())
with col2:
    st.metric("Records", f"{len(df):,}")
with col3:
    st.metric("Avg AQI", f"{df['us_aqi'].mean():.1f}")
with col4:
    st.metric("Time Period", f"{df['date_day'].min()[:10]} to {df['date_day'].max()[:10]}")

st.markdown("---")
st.caption("Navigate using the buttons above or select a page from the sidebar")