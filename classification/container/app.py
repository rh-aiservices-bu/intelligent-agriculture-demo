import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic import BaseModel
from typing import Tuple
from glob import glob

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
    
    #TODO Remove debug
    picture_path = ""
    print(entry.disease)
    print(entry.frame)

    if (entry.kind == "wheat"):
        if (entry.disease == "wheat_healthy"):
            picture_path = wheat_healthy[entry.frame]
        if (entry.disease == "wheat_brown_rust"):
            picture_path = wheat_brown_rust[entry.frame]
        if (entry.disease == "wheat_yellow_rust"):
            picture_path = wheat_yellow_rust[entry.frame]

    #TODO Remove debug
    print(picture_path)

    #TODO Send picture to prediction service
            
    #if entry.ill:
    #    response.status = "ill"
    #else:
    #    response.status = "healthy"
    
    response.status = "healthy"
    return response
    
# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)