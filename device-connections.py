import time
import pandas as pd
import requests

#Access token is provided by Thingsboard Cloud to be able to send 
ACCESS_TOKEN_PH = "kkm2m2zwqqzp4r3cn8wc"
URL_PH = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_PH}/telemetry"

ACCESS_TOKEN_DISS = "ACSssYaX5cyjdq0uUzBh"
URL_DISS = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_DISS}/telemetry"

ACCESS_TOKEN_DEPTH = "1xjTUFT4fdQXu6Cdy9xb"
URL_DEPTH = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_DEPTH}/telemetry"

ACCESS_TOKEN_TEMP = "kaxejzegx889d6y0fhhl"
URL_TEMP = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_TEMP}/telemetry"

ACCESS_TOKEN_SAL = "qw8tuu3KbpCv9YHwDW74"
URL_SAL = f"https://thingsboard.cloud/api/v1/{ACCESS_TOKEN_SAL}/telemetry"


df=pd.read_csv("BKB_WaterQualityData_2020084.csv")
#Salinity (ppt), Dissolved Oxygen (mg/L), pH (standard units), Secchi Depth (m),Water Depth (m),Water Temp (?C),Air Temp-Celsius,Air Temp (?F)
df_no_nan = df.dropna()

for i, row in df_no_nan.iterrows():
    payload1={
        "pH": row["pH (standard units)"]
    }

    payload2={
        "Dissolved Oxygen": row["Dissolved Oxygen (mg/L)"]
    }

    payload3={
        "Water Depth": row["Water Depth (m)"]
    }

    payload4={
        "Water Temp": row["Water Temp (?C)"]
    }

    payload5={
        "Salinity": row["Salinity (ppt)"]
    }

    response = requests.post(URL_PH, json=payload1)
    response2 = requests.post(URL_DISS, json=payload2)
    response3 = requests.post(URL_DEPTH, json=payload3)
    response4 = requests.post(URL_TEMP, json=payload4)
    response5 = requests.post(URL_SAL, json=payload5)
    time.sleep(5)