from extremitypathfinder import PolygonEnvironment

def initializeEnvironment():
    environment = PolygonEnvironment()

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
    #start_coordinates = (4.5, 1.0)
    #goal_coordinates = (4.0, 8.5)
    path, length = environment.find_shortest_path(start_coordinates, goal_coordinates)

    print(path)
    print(length)

    return path, length