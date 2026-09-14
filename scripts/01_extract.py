import json
import os
from datetime import datetime
import pandas as pd
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES_CSV = "data/ma.csv"
BRONZE_DIR = "data/bronze/raw_json"


def get_meteo_data(url, params, timeout=10):
    try:
        res = requests.get(url=url, params=params, timeout=timeout)
        res.raise_for_status()
        if res.status_code == 200:
            return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error Fetching data from Open-Meteo API : {e}")
        return None


def run_extraction():
    if not os.path.exists(CITIES_CSV):
        raise FileNotFoundError(f"Missing {CITIES_CSV} in data/ Directory :")

    os.makedirs(BRONZE_DIR, exist_ok=True)
    cities_df = pd.read_csv(CITIES_CSV)

    raw_data = []

    # Convert DataFrame rows into a list of dictionaries
    cities_list = cities_df.to_dict(orient="records")

    for city in cities_list:
        city_name = city.get("city")
        lat = city.get("lat")
        lng = city.get("lng")

        print(f"Fetching weather data for: {city_name}...")

        params = {
            "latitude": lat,
            "longitude": lng,
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "precipitation_sum",
                "precipitation_probability_max",
            ],
            "timezone": "auto",
        }

        res_json = get_meteo_data(API_URL, params)

        if res_json:
            # Inject city name and coords into JSON object to keep track of location
            res_json["city_metadata"] = {
                "city": city_name,
                "lat": lat,
                "lng": lng,
            }
            raw_data.append(res_json)

    # Save aggregated raw responses to Bronze layer
    if raw_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filepath = os.path.join(
            BRONZE_DIR, f"raw_weather_{timestamp}.json"
        )

        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)

        print(
            f"\nExtraction complete! {len(raw_data)} cities saved to {output_filepath}"
        )


run_extraction()