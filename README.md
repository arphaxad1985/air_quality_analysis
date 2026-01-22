# Air Quality Analysis

### Project Overview
Analysis of air pollution patterns and meteorological relationships across multiple cities.

### Project Overview

This project analyses air quality and weather data across multiple US cities to achieve three objectives:  

1. **Monitoring and Drawing Insights:** Understand patterns, trends, and variability in weather and air quality data.  
2. **Clustering Weather Regimes and Air Quality Risk Indicators:** Identify distinct regimes of environmental conditions and associated pollution levels using unsupervised learning.  
3. **Prediction of Engineered AQI Risk Levels:** Build a multiclass classifier to predict Air Quality Index (AQI) risk categories (Good → Hazardous).  

The analysis combines statistical methods, exploratory data analysis (EDA), and machine learning techniques to provide actionable insights for environmental monitoring and predictive modeling.

---

### Project Setup

- **Environment Isolation:**  
  A dedicated virtual environment (`airquality_env`) was created to ensure package compatibility and reproducibility. All dependencies such as `pandas`, `numpy`, `plotly`, `scikit-learn` were installed in this environment.  


### Project Structure
- `notebooks/`: Jupyter notebooks for analysis
- `datasets/`: Processed air quality and weather data
- `dashboard/`: Interactive dashboard files
- `figures/`: Generated visualizations and plots
- `models/`: Machine learning models and results
- `presentations/`: Presentation materials
- `README/`: Project overview and documentation

### Data Sources and variables
- Air Quality: Open-Meteo API
- Weather forecast: Open-Meteo API

### Variables

## Air Quality Measurements
| Variable | Unit | Description | Health Relevance |
|----------|------|-------------|------------------|
| `pm2_5` | µg/m³ | Fine particulate matter (≤2.5µm) | Penetrates lungs, cardiovascular effects |
| `pm10` | µg/m³ | Coarse particulate matter (≤10µm) | Respiratory irritation, asthma |
| `carbon_monoxide` | µg/m³ | Incomplete combustion gas | Reduces blood oxygen capacity |
| `sulphur_dioxide` | µg/m³ | Fossil fuel combustion | Respiratory irritant, acid rain precursor |
| `ozone` | µg/m³ | Secondary photochemical pollutant | Lung function impairment, asthma trigger |
| `nitrogen_dioxide` | µg/m³ | High-temperature combustion | Airway inflammation, asthma exacerbation |
| `carbon_dioxide` | ppm | Greenhouse gas | Climate indicator, indoor air quality |
| `us_aqi` | index (0-500) | Composite air quality index | Overall health risk assessment |

### Weather & Meteorological Variables
| Variable | Unit | Description | Environmental Relevance |
|----------|------|-------------|------------------------|
| `temperature_2m` | °C | Air temperature at 2m height | Pollution formation rates, dispersion |
| `relative_humidity_2m` | % | Relative humidity at 2m height | Aerosol formation, pollutant lifetime |
| `precipitation` | mm | Rainfall/snowfall amount | Wet deposition, pollution scavenging |
| `wind_speed_10m` | m/s | Wind speed at 10m height | Pollutant transport and dispersion |
| `surface_pressure` | hPa | Atmospheric pressure at surface | Vertical mixing, pollution trapping |
| `city` | text | Location name | Geographic context, urban vs rural |
| `country` | text | Country code | Regional air quality patterns |
| `lat` | degrees | Latitude coordinate | Spatial analysis, climate zone |
| `lon` | degrees | Longitude coordinate | Spatial analysis, transport patterns |

### Location Metadata
- `city`, `country`: Measurement location
- `lat`, `lon`: Geographic coordinates

*Data sourced from Open-Meteo Air Quality API*

### Cities Analyzed
1. Los Angeles, California
2. Sacramento, California
3. Detroit, Michigan
4. Houston, Texas
5. Cleveland, Ohio
6. Chicago, Illinois

### Analysis Period
November 7, 2025 - January 5, 2026

### Technical Stack
- **Python 3.10+**
- **Libraries:** pandas, numpy, matplotlib, seaborn, scikit-learn
- **APIs:** Open-Meteo
- **Environment:** Conda (airquality_env)

### Getting Started
### Clone repository
- git clone https://github.com/arphaxad1985/Air_quality_Analysis.git
- cd Air_quality_Analysis

### Create conda environment (optional)
- conda create -n airquality_env python=3.10
- conda activate airquality_env

### Install dependencies
- pip install pandas numpy matplotlib seaborn scikit-learn jupyter

### Run notebooks
- jupyter notebook notebooks/01.data_ingestion.ipynb

### Methodological Justification by Research Objective
This study applies statistical analysis and machine learning techniques in a structured manner, aligned with three research objectives: exploratory monitoring, unsupervised clustering, and supervised prediction. Each method was selected based on the nature of the data and the analytical goal.

---

### Research Questions
1. How do weather conditions (temperature, wind, humidity) affect air pollution levels?
2. What are the spatial patterns of pollution across different cities?
3. Which meteorological factors are strongest predictors of poor air quality?
4. How do pollution episodes correlate with specific weather regimes?

### Objective 1: Monitoring and Exploratory Insights

The first objective focuses on understanding patterns, variability, and trends in weather and air quality data. Descriptive statistics, including the mean, median, standard deviation, and quartiles, are used to summarise central tendency and dispersion. These measures provide baseline environmental conditions and highlight variability across time and locations.

Distribution analysis using boxplots and summary statistics indicates that several variables (e.g. PM2.5, precipitation, and wind speed) are skewed and deviate from normality. This behaviour is typical of environmental data, which is influenced by episodic events and physical constraints. A Shapiro–Wilk normality test is used to formally assess this assumption.

Correlation analysis is conducted using Spearman’s rank correlation coefficient. This non-parametric approach is selected because it does not assume normality and is suitable for identifying monotonic relationships between environmental variables. Correlation analysis at this stage is exploratory and is used to support interpretation rather than infer causality.

---

### Objective 2: Clustering Weather Regimes and Air Quality Risk Indicators

The second objective aims to identify distinct weather–air quality regimes using unsupervised learning. Prior to clustering, continuous variables are scaled to ensure that differences in magnitude do not disproportionately influence distance-based algorithms.

K-Means clustering is employed to group observations based on similarity in meteorological conditions and air quality indicators. Because K-Means requires the number of clusters to be specified in advance, cluster validation techniques are applied. The elbow method is used to examine within-cluster variance across different values of k, while the silhouette score is used to assess cluster cohesion and separation.

These validation measures do not constitute hypothesis testing but provide statistical support for selecting an appropriate number of clusters. Once clusters are defined, cluster profiling is performed using descriptive statistics to interpret the environmental and air quality characteristics of each regime.

---

### Objective 3: Multiclass Prediction of Air Quality Risk Levels
