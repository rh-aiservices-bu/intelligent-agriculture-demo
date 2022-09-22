# This is were the main map is defined.
# Location coordinates are with (0,0) at bottom left

# Boundaries, with counter clockwise vertex numbering!
boundary_coordinates = [(0.0, 0.0), (1919.0, 0.0), (1919.0, 1079.0), (0.0, 1079.0)]

# Array of obstacles/holes, with clockwise numbering!
list_of_obstacles = [
    [
        (50.0, 200.0),
        (500.0, 200.0),
        (500.0, 100.0),
        (50.0, 100.0),
    ],
]

barns = [
    {
        'name': 'wheat-0',
        'location': (10.0,15.0),
        'kind': 'wheat'
    }
]

tractors = [
    {
        'name': 'wheat-0',
        'kind': 'wheat',
        'capacity': 5,
        'barn': 0,
        'virtual': False
    },
    {
        'name': 'wheat-virtual',
        'kind': 'wheat',
        'capacity': 1000,
        'barn': 0,
        'virtual': True
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
