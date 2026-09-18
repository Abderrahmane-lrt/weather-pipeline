import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES_CSV = PROJECT_ROOT / "data" / "ma.csv"
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze" / "raw_json"


def get_meteo_data(url, params, timeout=30):
    try:
        res = requests.get(url=url, params=params, timeout=timeout)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code

        print(f"HTTP Error {status_code} : {e}")
        return None

    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code 
        print(f"Error Fetching data from Open-Meteo API : {e} {status_code}")
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
        
        if res_json is None:
            continue

        if res_json:
            res_json["city_metadata"] = {
                "city": city_name,
                "lat": lat,
                "lng": lng,
            }
            raw_data.append(res_json)

    # Save aggregated raw responses to Bronze layer
    if not raw_data:
        raise RuntimeError("Extraction failed: no weather data was retrieved")

    output_filepath = BRONZE_DIR / "latest_raw_weather.json"

    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    print(
        f"\nExtraction complete! {len(raw_data)} cities saved to {output_filepath}"
    )


if __name__ == "__main__":
    run_extraction()




