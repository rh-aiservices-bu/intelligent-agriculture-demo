import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic import BaseModel
from typing import Tuple
from glob import glob
from dotenv import load_dotenv
import requests
import json

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

# Load env vars
load_dotenv()
PREDICTION_ENDPOINT = os.getenv('PREDICTION_ENDPOINT')

# Input data class
class TileEntry(BaseModel):
    coordinates: Tuple[float,float] = None
    kind: str = ""
    status: str = ""
    disease: str = ""
    frame: int = None

# Output data class
class TileStatus(BaseModel):
    status: str = ""
    model_prediction: str = ""
    model_prediction_confidence_score: str = ""

# Initialize picture banks arrays with full relative path
wheat_healthy = sorted(glob(os.path.join('./assets/pictures/wheat_healthy/','*')))
wheat_brown_rust = sorted(glob(os.path.join('./assets/pictures/wheat_brown_rust/','*')))
wheat_yellow_rust = sorted(glob(os.path.join('./assets/pictures/wheat_yellow_rust/','*')))

def calculatePath(start_coordinates, goal_coordinates):
    path, length = environment.find_shortest_path(start_coordinates, goal_coordinates)
    print(path)
    print(length)
    return path, length

# Base API
@app.get("/")
async def root():
    return {"message": "Status:OK"}

# Classification API
@app.post("/classify", response_model = TileStatus)
async def classify(entry: TileEntry):
    response = TileStatus()
    
    if (entry.kind == "wheat"):
        if (entry.disease == "wheat_healthy"):
            picture_path = wheat_healthy[entry.frame]
        if (entry.disease == "wheat_brown_rust"):
            picture_path = wheat_brown_rust[entry.frame]
        if (entry.disease == "wheat_yellow_rust"):
            picture_path = wheat_yellow_rust[entry.frame]

    file =  {'file': open(picture_path, 'rb')}
    resp = requests.post(url = PREDICTION_ENDPOINT, files = file)
    
    result = resp.json()
    
    if entry.disease in {"wheat_healthy"}:
        result['status'] = 'healthy'
    else:
        result['status'] = 'ill'
    
    print(result)

    return result
    
# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)