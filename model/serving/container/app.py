""" Model serving API. Receives picture and sends back prediction. """
import os
import uuid

from PIL import Image
import io
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from numpy import argmax, array, max as max_
from tensorflow import expand_dims
from tensorflow.keras.utils import img_to_array, load_img
from uvicorn import run
import numpy as np

# Load local env vars if present
load_dotenv()
INFERENCE_ENDPOINT = os.getenv('INFERENCE_ENDPOINT', '')

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

# FastAPI classes
class Detections(BaseModel):
    model_prediction: str
    model_prediction_confidence_score: float

    class Config:
        schema_extra = {
            "example": {
                "model_prediction": "Wheat___Healthy",
                "model_prediction_confidence_score": 98.01
            }
        }


# Base API
@app.get("/")
async def root():
    """ Simple status check """
    return {"message": "Status:OK"}

# Model API
@app.post("/prediction", response_model=Detections)
async def get_net_image_prediction(file: UploadFile = File(...)):
    """ Prediction API"""
    contents = await file.read()

    img = Image.open(io.BytesIO(contents))
    img = img.convert('RGB')
    img = img.resize((200, 200), Image.NEAREST)
    img_array = img_to_array(img)

    #img_array = img_to_array(img) # Transform image to array
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
    print(f'Class prediction: {class_prediction}')
    model_score = round(max_(score) * 100, 2)
    print(f'Model score: {model_score}')

    # Return JSON-formatted results
    result = Detections(model_prediction=class_prediction, model_prediction_confidence_score=model_score)

    return result

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
