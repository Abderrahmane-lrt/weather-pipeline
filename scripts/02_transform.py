import json

import numpy as np

import pandas as pd




# 1. Read raw JSON from Bronze folder
df = pd.read_json("data/bronze/raw_json/raw_weather_20260914_140839.json")
raw_data = df.to_dict(orient="records")


rows = []

for item in raw_data:
   city_name = item["city_metadata"]["city"]
   daily = item['daily']

   for i in range(len(daily['time'])):
       rows.append({

           "city": city_name,
           "date": daily['time'][i],
           "weather_code": daily['weather_code'][i],
           "temperature_2m_max": daily['temperature_2m_max'][i],
           "temperature_2m_min": daily['temperature_2m_min'][i],
           "wind_speed_10m_max": daily['wind_speed_10m_max'][i],
           "wind_gusts_10m_max": daily['wind_gusts_10m_max'][i],
           "precipitation_sum": daily['precipitation_sum'][i],
           "precipitation_probability_max": daily['precipitation_probability_max'][i]

       }
       )


df = pd.DataFrame(rows)
df.to_csv("data/silver/cleaned_weather_data.csv", index=False)
print("Data transformed successfully!")