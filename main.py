import joblib
import uvicorn
import pandas as pd
import numpy as np
import io


from fastapi import FastAPI

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

import inference
import cnn_ae

app = FastAPI()

app.mount('/static', StaticFiles(directory='public'))

filename = './model/model.pkl'
loaded_model = joblib.load(filename)

stscfilename = './model/stsc.pkl'
stsc = joblib.load(stscfilename)


class Model(BaseModel):
    X: list[str]


@app.get('/')
def read_root():
    return RedirectResponse('./static/index.html')


@app.post('/predict')
def predict_model(model: Model, ucl: float):
    #data = """datetime;Accelerometer1RMS;Accelerometer2RMS;Current;Pressure;Temperature;Thermocouple;Voltage;Volume Flow RateRMS
    #""" + "\n".join(model.X)
    data = """datetime,Accelerometer1RMS,Accelerometer2RMS,Current,Pressure,Temperature,Thermocouple,Voltage,Volume Flow RateRMS
        """ + "\n".join(model.X)


    df = pd.read_csv(io.StringIO(data), sep=",", index_col='datetime', parse_dates=True)

    print(df.columns)

    df["Power"] = df["Current"] * df["Voltage"]
    # отношение расхода к мощности

    df["Power_flow_rate"] = df["Volume Flow RateRMS"] / df["Power"]
    # разница температур (если признаки скоррелированы и с одним из них что-то происходит, то покажет наличие аномалии)
    df["Temperature_diff"] = df['Temperature'] - df['Thermocouple']
    # разница акселлерометров (если признаки скоррелированы и с одним из них что-то происходит, то покажет наличие аномалии)
    df["Accel_diff"] = df['Accelerometer1RMS'] - df['Accelerometer2RMS']
    df["Volume Flow RateRMS_10mean"] = df["Volume Flow RateRMS"].rolling(window=10, min_periods=0).mean()
    df['Volume Flow RateRMS nean 20'] = df['Volume Flow RateRMS'].rolling(window=20, min_periods=0).mean()
    df['Volume Flow RateRMS nean 30'] = df['Volume Flow RateRMS'].rolling(window=30, min_periods=0).mean()
    print('stsc', stsc)
    result = inference.model_inference(df, loaded_model, stsc, ucl)
    return {"result": ''.join(map(str, result))}


def main():
    uvicorn.run('__main__:app', host='0.0.0.0', port=8001)


if __name__ == '__main__':
    main()