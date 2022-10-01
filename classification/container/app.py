""" Classification API. Receives field data and sends back prediction. """
import os
from glob import glob
from typing import Tuple

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import run

# Load local env vars if present
load_dotenv()
PREDICTION_ENDPOINT = os.getenv('PREDICTION_ENDPOINT')
PATH_ENDPOINT = os.getenv('PATH_ENDPOINT')

# App creation
app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)

# Input data classes
class TileEntry(BaseModel):
    """ Data about a field received from the drone """
    coordinates: Tuple[float,float] = None
    kind: str = ""
    status: str = ""
    disease: str = ""
    frame: int = None

# Output data classes
class TileStatus(BaseModel):
    """ Data sent back to the drone after model prediction """
    status: str = ""
    model_prediction: str = ""
    model_prediction_confidence_score: float = None

# Initialize picture banks arrays with full relative path
wheat_healthy = sorted(glob(os.path.join('./assets/pictures/wheat_healthy/','*')))
wheat_brown_rust = sorted(glob(os.path.join('./assets/pictures/wheat_brown_rust/','*')))
wheat_yellow_rust = sorted(glob(os.path.join('./assets/pictures/wheat_yellow_rust/','*')))

def add_path_entry(kind,coordinates):
    """ Calls the API to add a field to the array of places to visit """
    data_json = {"kind": kind, "coordinates": coordinates}
    resp = requests.put(url = PATH_ENDPOINT + 'destination', json=data_json)
    print(resp.json())

# Base API
@app.get("/")
async def root():
    """ Simple status check """
    return {"message": "Status:OK"}

# Classification API
@app.post("/classify", response_model = TileStatus)
async def classify(entry: TileEntry):
    """ Classification API """

    if entry.kind == "wheat":
        if entry.disease == "wheat_healthy":
            picture_path = wheat_healthy[entry.frame]
        if entry.disease == "wheat_brown_rust":
            picture_path = wheat_brown_rust[entry.frame]
        if entry.disease == "wheat_yellow_rust":
            picture_path = wheat_yellow_rust[entry.frame]

    file =  {'file': open(picture_path, 'rb')}
    resp = requests.post(url = PREDICTION_ENDPOINT, files = file)

    result = resp.json()

    if entry.disease in {"wheat_healthy"}:
        result['status'] = 'healthy'
    else:
        result['status'] = 'ill'
        add_path_entry(entry.kind, entry.coordinates)

    response = TileStatus()
    response.status = result['status']
    response.model_prediction = result['model_prediction']
    response.model_prediction_confidence_score = result['model_prediction_confidence_score']

    return response

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
