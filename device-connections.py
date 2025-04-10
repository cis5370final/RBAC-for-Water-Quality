import time
import pandas as pd
import requests
#kkm2m2zwqqzp4r3cn8wc
#Salinity (ppt),Dissolved Oxygen (mg/L),pH (standard units),Secchi Depth (m),Water Depth (m),Water Temp (?C),Air Temp-Celsius,Air Temp (?F)

#TODO:
#Delete NaNs from CSV
ACCESS_TOKEN_PH = "kkm2m2zwqqzp4r3cn8wc"
URL_PH = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_PH}/telemetry"

ACCESS_TOKEN_DISS = "ACSssYaX5cyjdq0uUzBh"
URL_DISS = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_DISS}/telemetry"

ACCESS_TOKEN_DEPTH = "1xjTUFT4fdQXu6Cdy9xb"
URL_DEPTH = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_DEPTH}/telemetry"


df=pd.read_csv("BKB_WaterQualityData_2020084.csv")
for i, row in df.iterrows():
    payload1={
        "pH": row["pH (standard units)"]
    }

    payload2={
        "Dissolved Oxygen": row["Dissolved Oxygen (mg/L)"]
    }

    payload3={
        "Water Depth": row["Water Depth (m)"]
    }

    response = requests.post(URL_PH, json=payload1)
    response2 = requests.post(URL_DISS, json=payload2)
    response3 = requests.post(URL_DEPTH, json=payload3)
    print(f"Sent row {i+1}: {payload1}, {payload2}, {payload3} | StatusL {response.status_code}, {response2.status_code}, {response3.status_code}")
    time.sleep(5)