# This is were the main map is defined.
# Location coordinates are with (0,0) at bottom left

# Boundaries, with counter clockwise vertex numbering!
boundary_coordinates = [
    (1650,0),
    (1650.0, 930.0),
    (0, 930.0),
    (0.0, 0.0)
    ]

# Array of obstacles/holes, with clockwise numbering!
list_of_obstacles = [
    [
        (0,737),
        (123,665),
        (230,640),
        (142,548),
        (0,592),
    ],
    [
        (338,636),
        (456,620),
        (600,550),
        (830,540),
        (1060,475),
        (935,360),
        (640,390),
        (398,512),
        (236,542),
    ],
    [
        (1158,475),
        (1430,518),
        (1650,470),
        (1650,297),
        (1450,390),
        (1025,352),
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
