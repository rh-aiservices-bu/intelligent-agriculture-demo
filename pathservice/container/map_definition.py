"""
    This is were the main map is defined.
    Location coordinates are with (0,0) at top left (GDevelop/Inkscape reference)
    So everything will have to be translated for use with PathFinder and RouteFinder
"""

MAP_WIDTH = 1650
MAP_HEIGHT = 930

# Boundaries, with counter clockwise vertex numbering!
boundary_coordinates = [
    (0,0),
    (0, 930),   #South-West corner
    (1650, 930),
    (1650, 0)   #North-East corner
    ]

# Array of obstacles/holes, with clockwise numbering!
list_of_obstacles = [
    [   # Barn Potato
        (404,135),
        (503,130),
        (533,160),
        (547,214),
        (545,269),
        (451,299),
        (422,295),
        (361,270),
        (345,253),
        (346,202),
        (353,158),

    ],
    [   # Barn Corn
        (1322,92),
        (1421,88),
        (1451,117),
        (1465,171),
        (1463,226),
        (1369,257),
        (1340,253),
        (1279,227),
        (1263,210),
        (1264,159),
        (1271,115),
    ],
    [   # Barn Wheat
        (775,672),
        (875,667),
        (905,697),
        (918,751),
        (917,806),
        (823,836),
        (793,832),
        (733,807),
        (717,790),
        (717,739),
        (724,695),
    ],
    [   # River - Left
        (0,581),
        (43,553),
        (123,530),
        (206,576),
        (255,659),
        (189,663),
        (108,690),
        (0,750),
    ],
    [   # River - Middle
        (320,653),
        (262,569),
        (188,523),
        (240,520),
        (291,533),
        (377,509),
        (493,440),
        (602,391),
        (699,373),
        (784,381),
        (853,377),
        (945,353),
        (1031,394),
        (1078,490),
        (1005,494),
        (902,530),
        (779,549),
        (635,553),
        (536,590),
        (452,630),
    ],
    [   # River - Right
        (1142,484),
        (1080,391),
        (1010,342),
        (1105,351),
        (1240,371),
        (1393,383),
        (1487,370),
        (1579,327),
        (1659,287),
        (1659,471),
        (1537,514),
        (1404,527),
        (1295,507),
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
