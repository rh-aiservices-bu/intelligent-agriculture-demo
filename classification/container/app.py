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
corn_common_rust = sorted(glob(os.path.join('./assets/pictures/corn_common_rust/','*')))
corn_gray_leaf_spot = sorted(glob(os.path.join('./assets/pictures/corn_gray_leaf_spot/','*')))
corn_healthy = sorted(glob(os.path.join('./assets/pictures/corn_healthy/','*')))
corn_northern_leaf_blight = sorted(glob(os.path.join('./assets/pictures/corn_northern_leaf_blight/','*'))) # pylint: disable=line-too-long
potato_early_blight = sorted(glob(os.path.join('./assets/pictures/potato_early_blight/','*')))
potato_healthy = sorted(glob(os.path.join('./assets/pictures/potato_healthy/','*')))
potato_late_blight = sorted(glob(os.path.join('./assets/pictures/potato_late_blight/','*')))

def add_path_entry(kind,coordinates):
    """ Calls the API to add a field to the array of places to visit """
    data_json = {"kind": kind, "coordinates": coordinates}
    resp = requests.put(url = PATH_ENDPOINT + 'destination', json=data_json, timeout=5)
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
        if entry.disease == "Wheat___Healthy":
            picture_path = wheat_healthy[entry.frame]
        if entry.disease == "Wheat___Brown_Rust":
            picture_path = wheat_brown_rust[entry.frame]
        if entry.disease == "Wheat___Yellow_Rust":
            picture_path = wheat_yellow_rust[entry.frame]

    if entry.kind == "corn":
        if entry.disease == "Corn___Common_Rust":
            picture_path = corn_common_rust[entry.frame]
        if entry.disease == "Corn___Gray_Leaf_Spot":
            picture_path = corn_gray_leaf_spot[entry.frame]
        if entry.disease == "Corn___Healthy":
            picture_path = corn_healthy[entry.frame]
        if entry.disease == "Corn___Northern_Leaf_Blight":
            picture_path = corn_northern_leaf_blight[entry.frame]

    if entry.kind == "potato":
        if entry.disease == "Potato___Early_Blight":
            picture_path = potato_early_blight[entry.frame]
        if entry.disease == "Potato___Healthy":
            picture_path = potato_healthy[entry.frame]
        if entry.disease == "Potato___Late_Blight":
            picture_path = potato_late_blight[entry.frame]

    file =  {'file': open(picture_path, 'rb')}
    resp = requests.post(url = PREDICTION_ENDPOINT, files = file, timeout=5)

    result = resp.json()

    if entry.disease in ["Wheat___Healthy","Corn___Healthy","Potato___Healthy"]:
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
