from random import Random

class DemoDataBuilder:
    def __init__(self, Location, Barn, Field, Tractor, TractorRoutingSolution, calculator):
        self.southWestCorner = None
        self.northEastCorner = None
        self.fieldCount = None
        self.tractorCount = None
        self.barnCount = None
        self.minDemand = None
        self.maxDemand = None
        self.tractorCapacity = None
        self.Location = Location
        self.Barn = Barn
        self.Field = Field
        self.Tractor = Tractor
        self.TractorRoutingSolution = TractorRoutingSolution
        self.distance_calculator = calculator

    @staticmethod
    def builder(Location, Barn, Field, Tractor, TractorRoutingSolution, calculator):
        return DemoDataBuilder(Location, Barn, Field, Tractor, TractorRoutingSolution, calculator)

    def set_south_west_corner(self, southWestCorner):
        self.southWestCorner = southWestCorner
        return self

    def set_north_east_corner(self, northEastCorner):
        self.northEastCorner = northEastCorner
        return self

    def set_min_demand(self, minDemand):
        self.minDemand = minDemand
        return self

    def set_max_demand(self, maxDemand):
        self.maxDemand = maxDemand
        return self

    def set_field_count(self, fieldCount):
        self.fieldCount = fieldCount
        return self

    def set_tractor_count(self, tractorCount):
        self.tractorCount = tractorCount
        return self

    def set_barn_count(self, barnCount):
        self.barnCount = barnCount
        return self

    def set_tractor_capacity(self, tractorCapacity):
        self.tractorCapacity = tractorCapacity
        return self

    def build(self):
        if self.minDemand < 1:
            raise ValueError("minDemand (" + self.minDemand + ") must be greater than zero.")
        if self.maxDemand < 1:
            raise ValueError("maxDemand (" + self.maxDemand + ") must be greater than zero.")
        if self.minDemand >= self.maxDemand:
            raise ValueError("maxDemand (" + self.maxDemand + ") must be greater than minDemand ("
                             + self.minDemand + ").")
        if self.tractorCapacity < 1:
            raise ValueError("Number of tractorCapacity (" + self.tractorCapacity + ") must be greater than zero.")
        if self.fieldCount < 1:
            raise ValueError("Number of fieldCount (" + self.fieldCount + ") must be greater than zero.")
        if self.tractorCount < 1:
            raise ValueError("Number of tractorCount (" + self.tractorCount + ") must be greater than zero.")
        if self.barnCount < 1:
            raise ValueError("Number of barnCount (" + self.barnCount + ") must be greater than zero.")

        if self.northEastCorner.X <= self.southWestCorner.X:
            raise ValueError("northEastCorner.getX (" + str(self.northEastCorner.X)
               + ") must be greater than southWestCorner.getX(" +  str(self.southWestCorner.X) + ").")

        if self.southWestCorner.Y <= self.northEastCorner.Y:
            print(self.northEastCorner.Y)
            raise ValueError("southWestCorner.getY (" + str(self.northEastCorner.Y)
               + ") must be greater than northEastCorner.getY(" +  str(self.southWestCorner.Y) + ").")

        name = "demo"

        random = Random(0)
        id_sequence = [0]

        def generate_id():
            out = id_sequence[0]
            id_sequence[0] = out + 1
            return str(out)

        generate_X = lambda: random.uniform(self.southWestCorner.X, self.northEastCorner.X)
        generate_Y = lambda: random.uniform(self.southWestCorner.Y, self.northEastCorner.Y)

        generate_demand = lambda: random.randint(self.minDemand, self.maxDemand)

        barn_list = []
        random_barn = lambda: random.choice(barn_list)

        generate_barn = lambda: self.Barn(
            generate_id(),
            self.Location(generate_X(), generate_Y()))

        for i in range(self.barnCount):
            barn_list.append(generate_barn())

        generate_tractor = lambda: self.Tractor(
            generate_id(),
            self.tractorCapacity,
            random_barn())

        tractor_list = []
        for i in range(self.tractorCount):
            tractor_list.append(generate_tractor())

        generate_field = lambda: self.Field(
            generate_id(),
            self.Location(generate_X(), generate_Y()),
            generate_demand())

        field_list = []
        for i in range(self.fieldCount):
            field_list.append(generate_field())

        location_list = []
        for field in field_list:
            location_list.append(field.location)
        for barn in barn_list:
            location_list.append(barn.location)

        self.distance_calculator.init_distance_maps(location_list)

        return self.TractorRoutingSolution(name, location_list,
                                      barn_list, tractor_list, field_list, self.southWestCorner,
                                      self.northEastCorner)