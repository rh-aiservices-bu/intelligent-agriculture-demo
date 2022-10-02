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
    [   # Barn Potato
        (94,42),
        (116,35),
        (143,37),
        (153,53),
        (151,76),
        (131,82),
        (108,85),
        (94,76),
        (85,62),
    ],
    [   # Barn Corn
        (344,25),
        (377,23),
        (392,36),
        (393,56),
        (385,67),
        (364,72),
        (347,69),
        (336,60),
        (334,40),
    ],
    [   # Barn Wheat
        (199,179),
        (231,176),
        (245,183),
        (251,199),
        (249,213),
        (232,223),
        (211,226),
        (193,218),
        (184,208),
        (184,190),
    ],
    [   # River - Left
        (0,151),
        (20,145),
        (44,144),
        (57,154),
        (69,175),
        (45,177),
        (23,184),
        (0,199),
    ],
    [   # River - Middle
        (57,143),
        (92,136),
        (126,116),
        (155,101),
        (186,98),
        (214,101),
        (252,92),
        (272,105),
        (287,129),
        (264,133),
        (229,143),
        (182,144),
        (165,147),
        (132,161),
        (108,169),
        (82,173),
        (71,153),
    ],
    [   # River - Right
        (265,91),
        (284,89),
        (332,98),
        (367,100),
        (386,99),
        (410,89),
        (439,74),
        (439,123),
        (410,134),
        (385,138),
        (353,135),
        (319,128),
        (301,126),
        (286,104),
    ]
]

barns = [
    {
        'name': 'wheat',
        'location': (715.0,822.0),
        'kind': 'wheat'
    },
    {
        'name': 'corn',
        'location': (1272.0,245.0),
        'kind': 'corn'
    },
    {
        'name': 'potato',
        'location': (344.0,288.0),
        'kind': 'potato'
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
    },
    {
        'name': 'corn-0',
        'kind': 'corn',
        'capacity': 5,
        'barn': 0,
        'virtual': False
    },
    {
        'name': 'corn-virtual',
        'kind': 'corn',
        'capacity': 1000,
        'barn': 0,
        'virtual': True
    },
    {
        'name': 'potato-0',
        'kind': 'potato',
        'capacity': 5,
        'barn': 0,
        'virtual': False
    },
    {
        'name': 'potato-virtual',
        'kind': 'potato',
        'capacity': 1000,
        'barn': 0,
        'virtual': True
    }
]
