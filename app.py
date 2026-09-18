import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Weather Dashboard", layout="wide")

DATABASE_URL = "postgresql://airflow:airflow@postgres:5432/weather_db"

# @st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM weather_infos", engine)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

st.title("Weather & Risk Dashboard")

# Filters
st.sidebar.header("Filters")

cities = st.sidebar.multiselect(
    "City",
    df["city"].unique(),
    default=df["city"].unique()
)

risks = st.sidebar.multiselect(
    "Risk level",
    df["risk_level"].unique(),
    default=df["risk_level"].unique()
)

dates = st.sidebar.date_input(
    "Date",
    [df["date"].min().date(), df["date"].max().date()]
)

# Apply filters
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["risk_level"].isin(risks))
]





# KPIs
st.subheader("Key Indicators")

nb_villes = filtered_df["city"].nunique() 
temp_max = filtered_df["temperature_2m_max"].max() 
print(temp_max)
precip_max = filtered_df["precipitation_sum"].max()
risk_count = filtered_df["risk_level"].isin(["High", "Élevé"]).sum()

if not filtered_df.empty:
    highest_risk_city = filtered_df.loc[
        filtered_df["risk_score"].idxmax(), "city"
    ]
else:
    highest_risk_city = "N/A"

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Cities", nb_villes)
col2.metric("Max Temperature", f"{temp_max:.2f} °C")
col3.metric("Max Precipitation", f"{precip_max:.2f} mm")
col4.metric("High Risk Periods", risk_count)
col5.metric("Highest Risk City", highest_risk_city)

st.divider()

# Alerts
st.subheader("Risk Alerts")

high_risk = filtered_df[
    filtered_df["risk_level"].isin(["High", "Élevé"])
]

if not high_risk.empty:
    st.warning("High risks detected!")
    st.dataframe(high_risk, use_container_width=True)
else:
    st.success("No high risks detected.")

# All data
with st.expander("View filtered data"):
    st.dataframe(filtered_df, use_container_width=True)