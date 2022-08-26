import json
import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from json import dumps
from uvicorn import run
from pydantic import BaseModel
from typing import Tuple
from extremitypathfinder import PolygonEnvironment

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
class PathFinderEntry(BaseModel):
    start_coordinates: Tuple[float,float] = None
    goal_coordinates: Tuple[float,float] = None

# Path calculation functions
def initializeEnvironment(environment):
    # counter clockwise vertex numbering!
    boundary_coordinates = [(0.0, 0.0), (10.0, 0.0), (9.0, 5.0), (10.0, 10.0), (0.0, 10.0)]

    # clockwise numbering!
    list_of_holes = [
        [
            (3.0, 7.0),
            (5.0, 9.0),
            (4.5, 7.0),
            (5.0, 4.0),
        ],
    ]
    environment.store(boundary_coordinates, list_of_holes, validate=False)

    environment.prepare()

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
@app.post("/pathfinder")
async def pathfinder(entry: PathFinderEntry):
    return calculatePath(entry.start_coordinates, entry.goal_coordinates)
    
# Initialize PathFinder
environment = PolygonEnvironment()
initializeEnvironment(environment)

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)