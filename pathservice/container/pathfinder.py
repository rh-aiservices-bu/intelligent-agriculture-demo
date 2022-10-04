""" PathFinder functions """
import map_definition

# Path calculation functions
def translate_coordinates(coordinates):
    """ Convert to/from GDevelop to PathFinder coordinates """
    x,y = coordinates
    return (x,map_definition.MAP_HEIGHT-y)

def initialize_environment(pathfinder_environment):
    """ Initialize pathfinder environment """
    translated_boundary_coordinates = []
    for coordinates in map_definition.boundary_coordinates:
        translated_boundary_coordinates.append(translate_coordinates(coordinates))

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
    path, length = \
        pathfinder_environment.find_shortest_path(translate_coordinates(start_coordinates), \
        translate_coordinates(goal_coordinates))

    translated_path = []
    for coordinates in path:
        translated_path.append(translate_coordinates(coordinates))

    return translated_path, length
