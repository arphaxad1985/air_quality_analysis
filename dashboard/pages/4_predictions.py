import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Predictions", layout="wide")


st.title(" Predictions: Service NOT currently abvailable")
st.markdown("Atmospheric regime analysis and AQI risk forecasting")


# Create tabs
tab1, tab2 = st.tabs([" Atmospheric Regimes", " AQI Risk Analysis"])

with tab1:
    st.header("🌤️ Rule-Based Atmospheric Regime Analysis")
    
    # Simple rule-based classification
    regimes = []
    for idx, row in df.iterrows():
        # Use available features with defaults
        wind = row.get('wind_speed_10m', row.get('wind_speed', 5))
        pm25 = row.get('pm2_5', 25)
        temp = row.get('temperature_2m', row.get('temperature', 20))
        
        if wind < 3:
            if pm25 > 35:
                regime = 'Polluted Stagnation'
            else:
                regime = 'Stagnant'
        elif wind > 8:
            regime = 'Well-Ventilated'
        elif pm25 > 50:
            regime = 'High Pollution'
        elif temp > 28:
            regime = 'Heat Dominated'
        else:
            regime = 'Mixed Conditions'
        
        regimes.append(regime)
    
    df['regime'] = regimes
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        regime_counts = pd.Series(regimes).value_counts()
        fig = px.pie(
            values=regime_counts.values,
            names=regime_counts.index,
            title='Regime Distribution',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'us_aqi' in df.columns:
            summary = df.groupby('regime')['us_aqi'].agg(['mean', 'min', 'max']).round(1)
            st.dataframe(summary, use_container_width=True)
    
    # AQI by regime
    if 'us_aqi' in df.columns:
        fig2 = px.box(df, x='regime', y='us_aqi', color='regime',
                     title='AQI by Atmospheric Regime')
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header(" AQI Risk Categories")
    
    if 'us_aqi' in df.columns:
        # Categorize AQI
        def categorize_aqi(aqi):
            if aqi <= 50:
                return "Good"
            elif aqi <= 100:
                return "Moderate"
            elif aqi <= 150:
                return "Unhealthy for Sensitive"
            elif aqi <= 200:
                return "Unhealthy"
            else:
                return "Very Unhealthy"
        
        df['aqi_category'] = df['us_aqi'].apply(categorize_aqi)
        
        # Display distribution
        category_counts = df['aqi_category'].value_counts()
        
        colors = {
            'Good': 'green',
            'Moderate': 'yellow',
            'Unhealthy for Sensitive': 'orange',
            'Unhealthy': 'red',
            'Very Unhealthy': 'purple'
        }
        
        fig3 = px.bar(
            x=category_counts.index,
            y=category_counts.values,
            color=category_counts.index,
            color_discrete_map=colors,
            title='AQI Risk Category Distribution',
            labels={'x': 'Category', 'y': 'Count'},
            text=category_counts.values
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Health recommendations
        st.subheader("💡 Health Guidelines")
        
        guidelines = {
            'Good': " Normal outdoor activities are safe for everyone.",
            'Moderate': "⚠️ Sensitive individuals should consider reducing prolonged exertion.",
            'Unhealthy for Sensitive': "⚠️ People with respiratory conditions should limit outdoor activities.",
            'Unhealthy': " Everyone should reduce outdoor activities.",
            'Very Unhealthy': " Avoid all outdoor activities. Health alert conditions."
        }
        
        for category, advice in guidelines.items():
            with st.expander(f"{category} AQI"):
                st.write(advice)
    else:
        st.warning("AQI data not available for risk analysis")

# Navigation
st.markdown("---")
if st.button("← Back to Monitoring", use_container_width=True):
    st.switch_page("pages/3_monitoring.py")