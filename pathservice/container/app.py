""" Path and Route services API """
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import run
from extremitypathfinder import PolygonEnvironment

import pathfinder
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
    """ Path query data """
    start_coordinates: tuple[float,float] = None
    goal_coordinates: tuple[float,float] = None

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "start_coordinates": (715,822),
                "goal_coordinates": (220,200)
            }
        }

class PathFinderResult(BaseModel):
    """ Path query result """
    path: list[tuple[float,float]] = None
    length: float = None

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "path": [(10.0, 22.1), (20.5, 400.0)],
                "length": 378.0458437808832
            }
        }

class RouteFinderEntry(BaseModel): # Tractor asks for full Route
    """ Route query data """
    kind: str = ""
    start_coordinates: tuple[float,float] = None

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "kind": "wheat",
                "start_coordinates": (715,822)
            }
        }

class RouteFinderResult(BaseModel):
    """ Route query result """
    path: list[tuple[float,float]] = None # List of coordinates to follow

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "path": [(10.0, 22.1), (20.5, 400.0)],
            }
        }

class DestinationsQuery(BaseModel):
    """ Destinations table query """
    kind: str = ""

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "kind": "wheat",
            }
        }

# TBD: Find why this model does not work
class DestinationsResult(BaseModel):
    """ Destinations query result """
    destinations: list[tuple[float,float]] = [] # List of coordinates

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "destinations": [(10.0, 22.1), (20.5, 400.0)],
            }
        }

class DestinationEntry(BaseModel):
    """ Additional destination entry """
    kind: str = ""
    coordinates: tuple[float,float] = None

    class Config:
        """ Example """
        schema_extra = {
            "example": {
                "kind": "wheat",
                "coordinates": (10.0,22.1)
            }
        }

# Destination arrays
destinations = dict()
destinations['wheat'] = []
destinations['corn'] = []
destinations['potatoes'] = []

# Base API
@app.get("/")
async def root():
    """ Basic status """
    return {"message": "Status:OK"}

# Pathfinder API
@app.post("/pathfinder", response_model = PathFinderResult)
async def pathfinder_api(entry: PathFinderEntry):
    """ Finds path between two points """
    result = PathFinderResult()
    result.path, result.length = \
        pathfinder.calculate_path(environment,entry.start_coordinates, entry.goal_coordinates)
    return result

# Route API
@app.post("/routefinder", response_model = RouteFinderResult)
async def routefinder(entry: RouteFinderEntry):
    """ Finds route going through all destinations """
    result = RouteFinderResult()
    result.path = route_solver.routefinder(environment,entry.kind,destinations[entry.kind])
    return result

# Path API
@app.post("/alldestinations", response_model = DestinationsResult)
async def get_destinations(entry: DestinationsQuery):
    """ Returns destinations array for a kind of crop """
    response = DestinationsResult()
    response.destinations = destinations[entry.kind]
    return response

@app.delete("/alldestinations")
async def delete_destinations(entry: DestinationsQuery):
    """ Reset destinations array for a kind of crop """
    destinations[entry.kind] = []
    return destinations

@app.put("/destination")
async def add_destination_entry(entry: DestinationEntry):
    """ Adds a destination in the array """
    if entry.kind == "wheat":
        destinations['wheat'].append(entry.coordinates)
        print(destinations['wheat'])
    return True

@app.delete("/destination")
async def delete_destination_entry(entry: DestinationEntry):
    """ Removes a destination from an array
    """
    if entry.kind == "wheat":
        try:
            destinations['wheat'] = \
                list(filter(lambda a: a != entry.coordinates, destinations['wheat']))
        except ValueError():
            print("Destination is not in list")
    print(destinations['wheat'])
    return True

# Initialize PathFinder
environment = PolygonEnvironment()
pathfinder.initialize_environment(environment)

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    run(app, host="0.0.0.0", port=port)
