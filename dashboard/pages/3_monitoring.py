import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Monitoring", layout="wide")

st.title("Monitoring")
st.markdown("Real-time trends, correlations, and city-level monitoring")

@st.cache_data
def load_data():
    df = pd.read_csv("../datasets/dashboard_df.csv")
    df['date_day'] = pd.to_datetime(df['date_day'])
    return df

df = load_data()

# Create tabs for different monitoring views
tab1, tab2, tab3, tab4 = st.tabs([" City Explorer", "📈 Trends", "🏙️ City Comparison", " Correlations"])

with tab1:
    # City Details Explorer
    st.header(" City Details Explorer")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_city = st.selectbox("Select a City", sorted(df['city'].unique()))
        
        if selected_city:
            city_df = df[df['city'] == selected_city]
            
            # City metrics
            st.metric("Total Days", len(city_df))
            st.metric("Average AQI", f"{city_df['us_aqi'].mean():.1f}")
            st.metric("Average Temperature", f"{city_df['temperature_2m'].mean():.1f}°C")
            st.metric("Average PM2.5", f"{city_df['pm2_5'].mean():.1f} µg/m³")
    
    with col2:
        if selected_city:
            city_df = df[df['city'] == selected_city]
            
            # Time series for selected city
            fig = px.line(
                city_df,
                x='date_day',
                y='us_aqi',
                title=f'AQI Trend for {selected_city}',
                markers=True
            )
            
            # Add threshold lines
            fig.add_hline(y=50, line_dash="dash", line_color="green", 
                         annotation_text="Good", annotation_position="top left")
            fig.add_hline(y=100, line_dash="dash", line_color="orange", 
                         annotation_text="Moderate", annotation_position="top left")
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Trends
    st.header("📈 Trends Analysis")
    
    # Multi-city time series
    selected_cities_trend = st.multiselect(
        "Select Cities for Trend Comparison",
        sorted(df['city'].unique()),
        default=sorted(df['city'].unique())[:3]
    )
    
    if selected_cities_trend:
        trend_df = df[df['city'].isin(selected_cities_trend)]
        
        fig = px.line(
            trend_df,
            x='date_day',
            y='us_aqi',
            color='city',
            title='AQI Trends Comparison',
            markers=True
        )
        
        # Add range selector
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    # City Comparison
    st.header("🏙️ Multi-City Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        compare_cities = st.multiselect(
            "Select Cities",
            sorted(df['city'].unique()),
            default=sorted(df['city'].unique())[:4]
        )
        
        compare_metric = st.selectbox(
            "Compare Metric",
            ["us_aqi", "pm2_5", "temperature_2m", "humidity"]
        )
    
    if compare_cities:
        compare_df = df[df['city'].isin(compare_cities)]
        
        # Box plot comparison
        fig = px.box(
            compare_df,
            x='city',
            y=compare_metric,
            color='city',
            title=f'{compare_metric.replace("_", " ").title()} Distribution by City',
            points='all'
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    # Correlations
    st.header("🌡️ Correlations Analysis")
    
    # Select variables for correlation
    numeric_cols = [col for col in df.select_dtypes(include=['float64', 'int64']).columns 
                   if col not in ['lat', 'lon']]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_var = st.selectbox("X Variable", numeric_cols, index=numeric_cols.index('temperature_2m'))
    with col2:
        y_var = st.selectbox("Y Variable", numeric_cols, index=numeric_cols.index('us_aqi'))
    with col3:
        color_var = st.selectbox("Color by", ['city', 'us_aqi', 'pm2_5'])
    
    # Scatter plot with regression
    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color=color_var,
        trendline="ols",
        title=f'{x_var.replace("_", " ").title()} vs {y_var.replace("_", " ").title()}',
        hover_data=['city', 'date_day']
    )
    
    # Calculate correlation coefficient
    correlation = df[x_var].corr(df[y_var])
    fig.add_annotation(
        x=0.05, y=0.95,
        xref="paper", yref="paper",
        text=f"Correlation: {correlation:.3f}",
        showarrow=False,
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    if st.checkbox("Show Correlation Heatmap"):
        corr_matrix = df[numeric_cols].corr()
        
        fig2 = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title='Correlation Matrix'
        )
        st.plotly_chart(fig2, use_container_width=True)

# Prediction Navigation
st.markdown("---")
st.subheader("🔮 Prediction Models")
st.write("Explore atmospheric regime clustering and AQI risk forecasting")

if st.button("Go to Predictions Page", use_container_width=True):
    st.switch_page("pages/4_🔮_Predictions.py")
