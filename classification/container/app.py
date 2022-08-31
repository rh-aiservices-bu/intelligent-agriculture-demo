import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from pydantic import BaseModel
from typing import Tuple

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
    ill: bool = False

# Output data class
class TileStatus(BaseModel):
    status: str = ""

def calculatePath(start_coordinates, goal_coordinates):
    path, length = environment.find_shortest_path(start_coordinates, goal_coordinates)
    print(path)
    print(length)
    return path, length

# Base API
@app.get("/")
async def root():
    return {"message": "Status:OK"}

# Pathfinder API
@app.post("/classify", response_model = TileStatus)
async def classify(entry: TileEntry):
    response = TileStatus()
    if entry.ill:
        response.status = "ill"
    else:
        response.status = "healthy"
    return response
    
# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)