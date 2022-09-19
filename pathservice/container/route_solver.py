import json
import math

from pprint import pprint

import optapy.config
import map_definition
from optapy import (constraint_provider, planning_entity,
                    planning_entity_collection_property,
                    planning_list_variable, planning_score, planning_solution,
                    problem_fact, problem_fact_collection_property,
                    solver_manager_create, value_range_provider)
from optapy.score import HardSoftScore
from optapy.types import Duration

## Problem facts
# Problem facts are facts about the problem. As such, they do not change during
# solving (and thus cannot have any planning variables). For Tractor Routing,
# the problem facts are the locations a tractor can visit, the barns,
# and the fields to visit.

class Location:
# Location coordinates, as well as the distances from every other locations    
    def __init__(self, X, Y, distance_map=None):
        self.X = X
        self.Y = Y
        self.distance_map = distance_map

    def set_distance_map(self, distance_map):
        self.distance_map = distance_map

    def get_distance_to(self, location):
        return self.distance_map[location]

    def to_X_Y_tuple(self):
        return (
            self.X,
            self.Y
        )

    def __str__(self):
        return f'[{self.X}, {self.Y}]'


class DistanceCalculator:
# Compute and initialize distance maps   
    def __init__(self):
        pass

    def calculate_distance(self, start, end):
        if start == end:
            return 0
        X_diff = end.X - start.X
        Y_diff = end.Y - start.Y
        return math.ceil(math.sqrt(X_diff**2 + Y_diff**2))

    def init_distance_maps(self, location_list):
        for location in location_list:
            distance_map = dict()
            for other_location in location_list:
                distance_map[other_location] = self.calculate_distance(location, other_location)
            location.set_distance_map(distance_map)

class Barn:
# Start/stop locations of the tractors
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __str__(self):
        return f'BarnLocation {self.name}'


@problem_fact
class Field:
# A tractor visits fields to treat crops, which takes up some capacity
    def __init__(self, name, location, demand):
        self.name = name
        self.location = location
        # Not really used at the moment, but each field
        # could have a different "weight"
        self.demand = demand

    def __str__(self):
        return f'Field {self.name}'

## Planning entities
# In Tractor Routing, tractors are the planning entities.
# Each tractor has a fixed barn to depart from and return to, and a list
# of fields to visit which we want to plan. In particular:
# - A field is visited by exactly one tractor
# - The order of the fields in the list is significant
# As such, the field list can be modelled as a planning list variable:

@planning_entity
class Tractor:
    def __init__(self, name, capacity, barn, field_list=None):
        self.name = name
        self.capacity = capacity
        self.barn = barn
        if field_list is None:
            self.field_list = []
        else:
            self.field_list = field_list

    @planning_list_variable(Field, ['field_range'])
    def get_field_list(self):
        return self.field_list

    def set_field_list(self, field_list):
        self.field_list = field_list

    def get_route(self):
        if len(self.field_list) == 0:
            return []
        route = [self.barn.location]
        for field in self.field_list:
            route.append(field.location)
        route.append(self.barn.location)
        return route
    
    def __str__(self):
        return f'Tractor {self.name}'

## The Constraints
# In tractor routing, we have one hard constraint: no tractor can go over its capacity

def get_total_demand(tractor):
    total_demand = 0
    for field in tractor.field_list:
        total_demand += field.demand
    return total_demand

def tractor_capacity(constraint_factory):
# The lambda in penalize controls how much to penalize for a violation. We want a tractor 5 over capacity to be penalized more than a tractor only 1 over capacity. Hence we penalize by
# `get_total_demand(tractor) - tractor.capacity`
# which is how much over capacity the tractor is.
    return constraint_factory \
        .for_each(Tractor) \
        .filter(lambda tractor: get_total_demand(tractor) > tractor.capacity) \
        .penalize("Over tractor capacity", HardSoftScore.ONE_HARD,
                  lambda tractor: int(get_total_demand(tractor) - tractor.capacity))


# We also have one soft constraint: minimize the total distance
def get_total_distance(tractor):

    total_distance = 1
    last_location = tractor.barn.location
    for field in tractor.field_list:
        total_distance += field.location.get_distance_to(last_location)
        last_location = field.location
    if last_location is not tractor.barn.location:
        total_distance += tractor.barn.location.get_distance_to(last_location)
    return total_distance

def total_distance(constraint_factory):
    return constraint_factory \
        .for_each(Tractor) \
        .penalize("Minimize total distance", HardSoftScore.ONE_SOFT,
                  lambda tractor: int(get_total_distance(tractor)))


@constraint_provider
# Return a list containing the constraints in a `@constraint_provider` decorated function
def tractor_routing_constraints(constraint_factory):
    return [
        # Hard constraints
        tractor_capacity(constraint_factory),
        
        # Soft constraints
        total_distance(constraint_factory)
    ]


## Planing solution

# Finally, there is the planning solution. The planning solution stores
# references to all the problem facts and planning entities that define
# the problem. Additionally, it also contain the score of the solution.
# The planning solution class represent both the problem and the solution;
# as such, a problem can be viewed as an uninitialized planning solution.

# In Tractor Routing, it needs to contain the field list, tractor list,
# and the score. The bounds are included for easier visualization of the route.

@planning_solution
class TractorRoutingSolution:
    def __init__(self,  name, location_list, barn_list, tractor_list, field_list,
                 south_west_corner, north_east_corner, score=None):
        self.name = name
        self.location_list = location_list
        self.barn_list = barn_list
        self.tractor_list = tractor_list
        self.field_list = field_list
        self.south_west_corner = south_west_corner
        self.north_east_corner = north_east_corner
        self.score = score

    @planning_entity_collection_property(Tractor)
    def get_tractor_list(self):
        return self.tractor_list

    @problem_fact_collection_property(Field)
    @value_range_provider('field_range', value_range_type=list)
    def get_field_list(self):
        return self.field_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_bounds(self):
        return [self.south_west_corner.to_X_Y_tuple(), self.north_east_corner.to_X_Y_tuple()]

    def get_distance_meters(self):
        return -self.score.getSoftScore() if self.score is not None else 0

## Solving

def routefinder():
    # Now that we defined our model and constraints, create an instance of the problem
    #problem = DataBuilder.builder(Location, Barn, Field, Tractor, TractorRoutingSolution, 
    #                                DistanceCalculator()) \
    #                                .set_tractor_capacity(2) \
    #                                .set_field_count(50).set_tractor_count(15).set_barn_count(1) \
    #                                .set_south_west_corner(Location(0, 1079)) \
    #                                .set_north_east_corner(Location(1919, 0)).build()

    
    name = 'data'
    southWestCorner = Location(*map_definition.boundary_coordinates[3])
    northEastCorner = Location(*map_definition.boundary_coordinates[1])

    barn_list = []
    for barn in map_definition.barns:
        barn_list.append(Barn(barn['name'],Location(*barn['location'])))

    tractor_list = []
    for tractor in map_definition.tractors:
        tractor_list.append(Tractor(tractor['name'],tractor['capacity'],barn_list[tractor['barn']]))

    field_list = []
    for field in map_definition.fields:
        field_list.append(Field(field['name'],Location(*field['location']),field['demand']))

    location_list = []
    for field in field_list:
        location_list.append(field.location)
    for barn in barn_list:
        location_list.append(barn.location)

    DistanceCalculator().init_distance_maps(location_list)

    problem = TractorRoutingSolution(name, location_list, barn_list, tractor_list, field_list, southWestCorner, northEastCorner)


    # Solve the problem
    
    SINGLETON_ID = 1
    solver_config = optapy.config.solver.SolverConfig()
    solver_config \
        .withSolutionClass(TractorRoutingSolution) \
        .withEntityClasses(Tractor) \
        .withConstraintProviderClass(tractor_routing_constraints) \
        .withTerminationSpentLimit(Duration.ofSeconds(5))

    solver_manager = solver_manager_create(solver_config)
    last_score = HardSoftScore.ZERO

    tractor_routing_solution = problem
    
    best_solution = solver_manager.solve(SINGLETON_ID, lambda _: problem)
    
    print('ok')
    final_solution = best_solution.getFinalBestSolution()

    for tractor in final_solution.tractor_list:
        verts = [(tractor.barn.location.X,tractor.barn.location.Y)]
        verts.extend(map(lambda field: (field.location.X,field.location.Y), tractor.field_list))
        print(tractor.name)
        print(verts)
    

routefinder()