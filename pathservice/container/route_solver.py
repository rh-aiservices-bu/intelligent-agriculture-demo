""" Route solving module, using OptaPlanner """
import optapy.config
import map_definition
from optapy import (constraint_provider, planning_entity,
                    planning_entity_collection_property,
                    planning_list_variable, planning_score, planning_solution,
                    problem_fact, problem_fact_collection_property,
                    solver_manager_create, value_range_provider)
from optapy.score import HardMediumSoftScore
from optapy.types import Duration

import pathfinder

## Problem facts
# Problem facts are facts about the problem. As such, they do not change during
# solving (and thus cannot have any planning variables). For Tractor Routing,
# the problem facts are the locations a tractor can visit, the barns,
# and the fields to visit.

class Location:
    """ Location coordinates, as well as the distances from every other locations """
    def __init__(self, x, y, distance_map=None):
        self.x = x
        self.y = y
        self.distance_map = distance_map

    def set_distance_map(self, distance_map):
        """ Self explanatory """
        self.distance_map = distance_map

    def get_distance_to(self, location):
        """ Self explanatory """
        return self.distance_map[location]

    def to_x_y_tuple(self):
        """ Self explanatory """
        return (
            self.x,
            self.y
        )

    def __str__(self):
        return f'[{self.x}, {self.y}]'


class DistanceCalculator:
    """ Compute and initialize distance maps """
    def __init__(self):
        pass

    def calculate_distance(self, environment,start, end):
        """ Compute path length using Pathfinder """
        if start == end:
            return 0
        result = pathfinder.calculate_path(environment,(start.x,start.y),(end.x,end.y))
        return result[1]

    def init_distance_maps(self, environment,location_list):
        """ Initializes distances between each points pairs """
        for location in location_list:
            distance_map = dict()
            for other_location in location_list:
                distance_map[other_location] = \
                    self.calculate_distance(environment,location, other_location)
            location.set_distance_map(distance_map)

class Barn:
    """ Start/stop locations of the tractors """
    def __init__(self, name, location, kind):
        self.name = name
        self.location = location
        self.kind = kind

    def __str__(self):
        return f'BarnLocation {self.name}'


@problem_fact
class Field:
    """ A tractor visits fields to treat crops, which takes up some capacity """
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
    """ That's a tractor! """
    def __init__(self, name, kind, capacity, barn, virtual, field_list=None):
        self.name = name
        self.kind = kind
        self.capacity = capacity
        self.barn = barn
        self.is_virtual = virtual
        if field_list is None:
            self.field_list = []
        else:
            self.field_list = field_list

    @planning_list_variable(Field, ['field_range'])
    def get_field_list(self):
        """ Getter """
        return self.field_list

    def set_field_list(self, field_list):
        """ Setter """
        self.field_list = field_list

    def get_route(self):
        """ Returns route attached to tractor """
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
    """ Get all demands for a specific tractor """
    total_demand = 0
    for field in tractor.field_list:
        total_demand += field.demand
    return total_demand

def tractor_capacity(constraint_factory):
    """ The lambda in penalize controls how much to penalize for a violation. \
        We want a tractor 5 over capacity to be penalized more than a tractor \
        only 1 over capacity. Hence we penalize by \
        `get_total_demand(tractor) - tractor.capacity`
        which is how much over capacity the tractor is.
    """
    return constraint_factory \
        .for_each(Tractor) \
        .filter(lambda tractor: get_total_demand(tractor) > tractor.capacity) \
        .penalize("Over tractor capacity", HardMediumSoftScore.ONE_HARD,
                  lambda tractor: int(get_total_demand(tractor) - tractor.capacity))


def minimize_virtual_stops(constraint_factory):
    """ We need to minimize the usage of the virtual tractor. """
    return constraint_factory \
        .for_each(Tractor) \
        .filter(lambda tractor: (tractor.is_virtual and len(tractor.field_list)>0)) \
        .penalize("Minimal virtual stops", HardMediumSoftScore.ONE_MEDIUM,
                  lambda tractor: len(tractor.field_list))


def get_total_distance(tractor):
    """ We also have one soft constraint: minimize the total distance """
    distance = 1
    last_location = tractor.barn.location
    for field in tractor.field_list:
        distance += field.location.get_distance_to(last_location)
        last_location = field.location
    if last_location is not tractor.barn.location:
        distance += tractor.barn.location.get_distance_to(last_location)
    return distance

def total_distance(constraint_factory):
    """ Returns distance constraints """
    return constraint_factory \
        .for_each(Tractor) \
        .penalize("Minimize total distance", HardMediumSoftScore.ONE_SOFT,
                  lambda tractor: int(get_total_distance(tractor)))


@constraint_provider
def tractor_routing_constraints(constraint_factory):
    """ Return a list containing the constraints in a `@constraint_provider` decorated function """
    return [
        # Hard constraints
        tractor_capacity(constraint_factory),

        # Soft constraints
        total_distance(constraint_factory),

        # Soft constraints
        minimize_virtual_stops(constraint_factory)
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
    """ init """
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
        """ Self explanatory """
        return self.tractor_list

    @problem_fact_collection_property(Field)
    @value_range_provider('field_range', value_range_type=list)
    def get_field_list(self):
        """ Self explanatory """
        return self.field_list

    @planning_score(HardMediumSoftScore)
    def get_score(self):
        """ Self explanatory """
        return self.score

    def set_score(self, score):
        """ Self explanatory """
        self.score = score

    def get_bounds(self):
        """ Self explanatory """
        return [self.south_west_corner.to_X_Y_tuple(), self.north_east_corner.to_X_Y_tuple()]

    def get_distance_meters(self):
        """ Self explanatory """
        return -self.score.getSoftScore() if self.score is not None else 0

## Solving

def routefinder(environment,kind,destinations):
    """ Main function """
    name = 'data'

    # We have to translate all inputs
    south_west_corner = \
        Location(*pathfinder.translate_coordinates(map_definition.boundary_coordinates[1]))
    north_east_corner = \
        Location(*pathfinder.translate_coordinates(map_definition.boundary_coordinates[3]))

    barn_list = []
    for barn in (barn for barn in map_definition.barns if barn['kind'] == kind):
        barn_list.append(Barn(barn['name'], \
            Location(*pathfinder.translate_coordinates(barn['location'])),kind))

    tractor_list = []
    for tractor in (tractor for tractor in map_definition.tractors if tractor['kind'] == kind):
        tractor_list.append(Tractor(tractor['name'],tractor['kind'],tractor['capacity'], \
            barn_list[tractor['barn']],tractor['virtual']))

    field_list = []
    for i, destination in enumerate(destinations):
        field_list.append(Field('field-'+str(i), \
            Location(*pathfinder.translate_coordinates(destination)),1))

    location_list = []
    for barn in barn_list:
        location_list.append(barn.location)
    for field in field_list:
        location_list.append(field.location)

    DistanceCalculator().init_distance_maps(environment,location_list)

    problem = TractorRoutingSolution(name, location_list, barn_list, tractor_list, \
         field_list, south_west_corner, north_east_corner)

    # Solve the problem

    singleton_id = 1
    termination_config = optapy.config.solver.termination.TerminationConfig()
    # Stop after 4 seconds with no score improvement
    termination_config.setUnimprovedSpentLimit(Duration.ofSeconds(4))
    # Stop after 6 seconds max anyway
    termination_config.setSpentLimit(Duration.ofSeconds(6))

    solver_config = optapy.config.solver.SolverConfig()
    solver_config \
        .withSolutionClass(TractorRoutingSolution) \
        .withEntityClasses(Tractor) \
        .withConstraintProviderClass(tractor_routing_constraints) \
        .withTerminationConfig(termination_config)

    solver_manager = solver_manager_create(solver_config)

    best_solution = solver_manager.solve(singleton_id, lambda _: problem)

    final_solution = best_solution.getFinalBestSolution()

    verts=dict()

    for tractor in final_solution.tractor_list:
        verts[tractor.name] = []
        #verts[tractor.name] = \
        #    [pathfinder.translate_coordinates((tractor.barn.location.x,tractor.barn.location.y))]
        verts[tractor.name].extend(map(lambda field: \
            pathfinder.translate_coordinates((field.location.x,field.location.y)), \
            tractor.field_list))
        # Add return to the barn
        verts[tractor.name].append(pathfinder.translate_coordinates((tractor.barn.location.x,tractor.barn.location.y)))

    return verts[kind+'-0']
