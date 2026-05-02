import requests
import pandas as pd
import numpy as np



def do_transform_layer(url):
        
    response = requests.get(url)

    data = response.json()

    ##print(data["hourly"]["time"])

    df = pd.DataFrame({
        "datetime": data["hourly"]["time"], 
        "temp": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"]
        })

    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["day"] = df["datetime"].dt.day
    df["hour"] = df["datetime"].dt.hour
    df = df.dropna(how="any")

    df["temp"] = pd.to_numeric(df["temp"], errors='coerce').astype(float)

    conditions = [
        (df["temp"] > 30),
        (df["temp"] >=20) & (df["temp"] <= 30),
        (df["temp"] < 20)
    ]

    choices = ['hot', 'warm', 'cold']
    df["temp_category"] = np.select(conditions, choices, default='Unknown')
    
    return df


