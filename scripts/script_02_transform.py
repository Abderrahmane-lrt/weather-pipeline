import json
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_JSON = (
    PROJECT_ROOT / "data" / "bronze" / "raw_json" / "latest_raw_weather.json"
)
OUTPUT_CSV = PROJECT_ROOT / "data" / "silver" / "cleaned_weather_data.csv"


def calculate_risk(row):
    score = 0

    # Extreme Temperature Risk
    temperature_max = float(row.get("temperature_2m_max", 0))
    if temperature_max >= 40:
        score += 40
    elif temperature_max >= 35:
        score += 20

    # High Wind Risk
    wind_speed_max = float(row.get("wind_speed_10m_max", 0))
    if wind_speed_max >= 50:
        score += 30
    elif wind_speed_max >= 30:
        score += 15

    # Heavy Rain 
    precipitation_sum = float(row.get("precipitation_sum", 0))
    if precipitation_sum >= 20:
        score += 30

    precipitation_probability_max = float(
        row.get("precipitation_probability_max", 0)
    )
    if precipitation_probability_max >= 10:
        score += 15

    return min(score, 100)


def run_transform():
    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"لم يتم العثور على الملف: {INPUT_JSON}")

    df = pd.read_json(INPUT_JSON)
    raw_data = df.to_dict(orient="records")
    rows = []

    for item in raw_data:
        city_name = item["city_metadata"]["city"]
        daily = item["daily"]

        for i in range(len(daily["time"])):
            rows.append({
                "city": city_name,
                "date": daily["time"][i],
                "weather_code": daily["weather_code"][i],
                "temperature_2m_max": daily["temperature_2m_max"][i],
                "temperature_2m_min": daily["temperature_2m_min"][i],
                "wind_speed_10m_max": daily["wind_speed_10m_max"][i],
                "wind_gusts_10m_max": daily["wind_gusts_10m_max"][i],
                "precipitation_sum": daily["precipitation_sum"][i],
                "precipitation_probability_max": daily[
                    "precipitation_probability_max"
                ][i],
            })

    df = pd.DataFrame(rows)
    df.drop_duplicates(inplace=True)

    df["risk_score"] = df.apply(calculate_risk, axis=1)
    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 25, 60, 100],
        labels=["Low", "Medium", "High"],
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    print("Data transformed successfully!")


if __name__ == "__main__":
    run_transform()