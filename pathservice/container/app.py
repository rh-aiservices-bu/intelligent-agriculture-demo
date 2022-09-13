import json
import os
import uuid
from json import dumps
from typing import List,Tuple

from dotenv import load_dotenv
from extremitypathfinder import PolygonEnvironment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import run

# Load local env vars if present
load_dotenv()

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

# Input/Output data classes
class PathFinderEntry(BaseModel): # Used only for testing
    start_coordinates: Tuple[float,float] = None
    goal_coordinates: Tuple[float,float] = None

class PathFinderResult(BaseModel): # Used only for testing
    path: List[Tuple[float,float]] = None
    length: float = None

class RouteFinderEntry(BaseModel): # Tractor asks for full Route
    kind: str = ""
    start_coordinates: Tuple[float,float] = None

class RouteFinderResult(BaseModel):
    path: List[Tuple[float,float]] = None # List of coordinates to follow

class DestinationEntry(BaseModel):
    kind: str = ""
    coordinates: Tuple[float,float] = None

# Destination arrays
wheat_destinations = []

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
    return path, length

# Base API
@app.get("/")
async def root():
    return {"message": "Status:OK"}

# Pathfinder API
@app.post("/pathfinder", response_model = PathFinderResult)
async def pathfinder(entry: PathFinderEntry):
    result = PathFinderResult()
    result.path, result.length = calculatePath(entry.start_coordinates, entry.goal_coordinates)
    print(result)
    return result

# Route API
@app.post("/routefinder", response_model = RouteFinderResult)
async def routefinder(entry: RouteFinderEntry):
    result = RouteFinderResult()

    for first_destination in wheat_destinations:
        for second_destination in wheat_destinations:
            print('toto')


    print(result)
    return result

# Path API
@app.put("/destination")
async def addDestinationEntry(entry: DestinationEntry):
    if entry.kind == "wheat":
        wheat_destinations.append(entry.coordinates)
        print(wheat_destinations)
    return True

@app.post("/delete-destination")
async def deleteDestinationEntry(entry: DestinationEntry):
    if entry.kind == "wheat":
        wheat_destinations.remove(entry.coordinates)
        print(wheat_destinations)
    return True
    
# Initialize PathFinder
environment = PolygonEnvironment()
initializeEnvironment(environment)

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    run(app, host="0.0.0.0", port=port)
