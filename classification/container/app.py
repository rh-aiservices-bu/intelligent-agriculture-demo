""" Classification API. Receives field data and sends back prediction. """
import io
import os
import uuid
from glob import glob
from typing import Tuple

import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from numpy import argmax, array
from numpy import max as max_
from PIL import Image
from pydantic import BaseModel
from tensorflow import expand_dims
from tensorflow.keras.utils import img_to_array, load_img
from uvicorn import run

# Load local env vars if present
load_dotenv()
INFERENCE_ENDPOINT = os.getenv('INFERENCE_ENDPOINT', '')
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

# Inference classes
class_predictions = array([
    'Corn___Common_Rust',
    'Corn___Gray_Leaf_Spot',
    'Corn___Healthy',
    'Corn___Northern_Leaf_Blight',
    'Potato___Early_Blight',
    'Potato___Healthy',
    'Potato___Late_Blight',
    'Rice___Brown_Spot',
    'Rice___Healthy',
    'Rice___Leaf_Blast',
    'Rice___Neck_Blast',
    'Wheat___Brown_Rust',
    'Wheat___Healthy',
    'Wheat___Yellow_Rust'
])

## FastAPI classes
# Input
class TileEntry(BaseModel):
    """ Data about a field received from the drone """
    coordinates: Tuple[float,float] = None
    kind: str = ""
    status: str = ""
    disease: str = ""
    frame: int = None
    uuid: str = ""

# Output
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

def add_path_entry(kind,coordinates,uuid):
    """ Calls the API to add a field to the array of places to visit """
    data_json = {"kind": kind, "coordinates": coordinates, "uuid": uuid}
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

    #file =  {'file': open(picture_path, 'rb')}

    img = load_img(picture_path, target_size=(200, 200))
    img_array = img_to_array(img) # Transform image to array
    img_array = expand_dims(img_array, 0) # Expand dimension as expected by inference point

    # json payload
    img_numpy = img_array.numpy() # Convert to numpy array
    im_json = img_numpy.tolist() # Converts to a nested list for json payload
    
    # ModelMesh expected input format
    # (get model input "name" and "shape" from your model)
    data = {
        "inputs": [
            { 
                "name": "input_1",
                "shape": [1,200,200,3],
                "datatype": "FP32",
                "data": im_json
            }
        ]
    }

    # Call the inference point
    response = requests.post(INFERENCE_ENDPOINT, json=data)
    raw_output = response.json() # Extract to Json
    arr = np.array(raw_output['outputs'][0]['data']) # Get the response data as a NumPy Array
    # Retrieve result
    class_prediction = class_predictions[argmax(arr)]
    score = max_(arr)
    model_score = round(score * 100, 2)
    result = {}
    if entry.disease in ["Wheat___Healthy","Corn___Healthy","Potato___Healthy"]:
        result['status'] = 'healthy'
    else:
        result['status'] = 'ill'
        add_path_entry(entry.kind, entry.coordinates,entry.uuid)

    response = TileStatus()
    response.status = result['status']
    response.model_prediction = class_prediction
    response.model_prediction_confidence_score = model_score

    return response

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
