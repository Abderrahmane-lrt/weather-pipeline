import os
from pathlib import Path

from sqlalchemy import (
    Date,
    Column,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEATHER_DATA_DIR = PROJECT_ROOT / "data" / "silver"
CSV_WEATHER = WEATHER_DATA_DIR / "cleaned_weather_data.csv"
CSV_CITIES = PROJECT_ROOT / "data" / "ma.csv"
DATABASE_URL = "postgresql://airflow:airflow@postgres:5432/weather_db"
Base = declarative_base()


class WeatherInfo(Base):
    __tablename__ = "weather_infos"

    city = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    weather_code = Column(Integer)
    temperature_2m_max = Column(Float)
    temperature_2m_min = Column(Float)
    wind_speed_10m_max = Column(Float)
    wind_gusts_10m_max = Column(Float)
    precipitation_sum = Column(Float)
    precipitation_probability_max = Column(Float)
    risk_score = Column(Integer)
    risk_level = Column(String)

    def __str__(self):
        return (
            f"Ville : {self.city}, weather_code : {self.weather_code}, "
            f"Temperature Max : {self.temperature_2m_max}, Temperature Min : {self.temperature_2m_min}, "
            f"Wind Speed Max : {self.wind_speed_10m_max}, Wind Gusts Max : {self.wind_gusts_10m_max}, "
            f"Precipitation Sum : {self.precipitation_sum}, Precipitation Probability Max : {self.precipitation_probability_max}, "
            f"Risk Score : {self.risk_score}, Risk Level : {self.risk_level})"
        )


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    country = Column(String)
    iso2 = Column(String, default="MA")
    admin_name = Column(String)
    capital = Column(String)
    population = Column(Integer)
    population_proper = Column(Integer)

    def __str__(self):
        return f"Ville : {self.name}, Province : {self.admin_name}, Country : {self.country})"


def run_load():
    if not CSV_WEATHER.exists() or not CSV_CITIES.exists():
        raise FileNotFoundError(f"Missing file: {CSV_WEATHER} or {CSV_CITIES}")

    engine = create_engine(DATABASE_URL )
    Base.metadata.create_all(engine)

    # Weather data load
    df_weather = pd.read_csv(CSV_WEATHER)
    df_weather["city"] = df_weather["city"].astype(str)
    df_weather["date"] = pd.to_datetime(df_weather["date"], errors="coerce").dt.date

    # Cities data load
    df_cities = pd.read_csv(CSV_CITIES) 
    df_cities["city"] = df_cities["city"].astype(str)
    df_cities["capital"] = df_cities["capital"].fillna("non-capital")

    df_weather.to_sql(
        "weather_infos",
        con=engine,
        if_exists="replace",
        index=False,

    )

    df_cities.to_sql(
        "cities",
        con=engine,
        if_exists="replace",
        index=False,
    )

    print(f"Loaded {len(df_weather)} weather records into PostgreSQL!")
    print(f"Loaded {len(df_cities)} city records into PostgreSQL!")


if __name__ == "__main__":
    run_load()