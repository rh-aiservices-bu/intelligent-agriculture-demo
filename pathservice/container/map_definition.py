# This is were the main map is defined.location
# Coordinates are with (0,0) at bottom left

# Boundaries, with counter clockwise vertex numbering!
boundary_coordinates = [(0.0, 0.0), (1919.0, 0.0), (1919.0, 1079.0), (0.0, 1079.0)]

# Array of obstacles/holes, with clockwise numbering!
list_of_obstacles = [
    [
        (50.0, 500.0),
        (500.0, 500.0),
        (500.0, 50.0),
        (50.0, 50.0),
    ],
]

barns = [
    {
        'name': '0',
        'location': (10.0,15.0)
    }
]

tractors = [
    {
        'name': '1',
        'capacity': 5,
        'barn': 0,
        'virtual': True
    },
    {
        'name': '2',
        'capacity': 5,
        'barn': 0,
        'virtual': False
    }
]

fields = [
    {
        'name': '5',
        'location': (100.0,260.0),
        'demand': 1
    },
    {
        'name': '6',
        'location': (200.0,300.0),
        'demand': 1
    },
    {
        'name': '7',
        'location': (400.0,260.0),
        'demand': 1
    },
    {
        'name': '8',
        'location': (500.0,300.0),
        'demand': 1
    },
    {
        'name': '9',
        'location': (600.0,260.0),
        'demand': 1
    },
    {
        'name': '10',
        'location': (700.0,300.0),
        'demand': 1
    },
]
