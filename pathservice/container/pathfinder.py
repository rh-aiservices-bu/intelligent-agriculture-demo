""" PathFinder functions """
import map_definition

# Path calculation functions
def translate_coordinates(coordinates):
    """ Convert to/from GDevelop to PathFinder coordinates.
        We have to do this because PathFinder has (0,0)  at the bottom left.
        We use this function every time there is data in/out from a different referential """
    x,y = coordinates
    return (x,map_definition.MAP_HEIGHT-y)

def translate_destinations(destinations):
    """ Translates an array of coordinates """
    translated_destinations = []
    for coordinates in destinations:
        translated_destinations.append(translate_coordinates(coordinates))
    return translated_destinations

def initialize_environment(pathfinder_environment):
    """ Initialize pathfinder environment """
    # Boundary coordinates are using a different referential
    translated_boundary_coordinates = []
    for coordinates in map_definition.boundary_coordinates:
        translated_boundary_coordinates.append(translate_coordinates(coordinates))

    # Obstacles coordinates are using a different referential
    translated_list_of_obstacles = []
    for item in map_definition.list_of_obstacles:
        item_coordinates = []
        for coordinates in item:
            item_coordinates.append(translate_coordinates(coordinates))
        translated_list_of_obstacles.append(item_coordinates)

    pathfinder_environment.store(translated_boundary_coordinates, \
        translated_list_of_obstacles, validate=False)
    pathfinder_environment.prepare()
    print("PathFinder Environment ready")

def calculate_path(pathfinder_environment,start_coordinates, goal_coordinates):
    """ Finds shortest path, returns array and length """
    # Start and goal have to be in the same referential as PathFinder
    # Please translate if needed before submitting to the function
    path, length = \
        pathfinder_environment.find_shortest_path(start_coordinates, goal_coordinates)

    return path, length
