import json
import os
import uuid
from json import dumps
from typing import List,Tuple

from dotenv import load_dotenv
from extremitypathfinder import PolygonEnvironment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uvicorn import run

import map_definition
import route_solver

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
class PathFinderEntry(BaseModel):
    start_coordinates: Tuple[float,float] = None
    goal_coordinates: Tuple[float,float] = None

    class Config:
        schema_extra = {
            "example": {
                "start_coordinates": (10.0,22.1),
                "goal_coordinates": (20.5,400.0)
            }
        }

class PathFinderResult(BaseModel):
    path: List[Tuple[float,float]] = None
    length: float = None

    class Config:
        schema_extra = {
            "example": {
                "path": [(10.0, 22.1), (20.5, 400.0)],
                "length": 378.0458437808832
            }
        }

class RouteFinderEntry(BaseModel): # Tractor asks for full Route
    kind: str = ""
    start_coordinates: Tuple[float,float] = None

    class Config:
        schema_extra = {
            "example": {
                "kind": "wheat",
                "start_coordinates": (10.0,22.1)
            }
        }

class RouteFinderResult(BaseModel):
    path: List[Tuple[float,float]] = None # List of coordinates to follow

    class Config:
        schema_extra = {
            "example": {
                "path": [(10.0, 22.1), (20.5, 400.0)],
            }
        }

class DestinationEntry(BaseModel):
    kind: str = ""
    coordinates: Tuple[float,float] = None

    class Config:
        schema_extra = {
            "example": {
                "kind": "wheat",
                "coordinates": (10.0,22.1)
            }
        }

# Destination arrays
wheat_destinations = []

# Path calculation functions
def initializeEnvironment(environment):
    environment.store(map_definition.boundary_coordinates, map_definition.list_of_obstacles, validate=False)
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
    return result

# Route API
@app.post("/routefinder", response_model = RouteFinderResult)
async def routefinder(entry: RouteFinderEntry):
    result = RouteFinderResult()
    for first_destination in wheat_destinations:
        for second_destination in wheat_destinations:
            print('toto')

    route_solver.routefinder()

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
