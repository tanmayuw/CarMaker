from enum import Enum


# Enum for primary components of the car, non-primary components are marked as Extra
# Component_Type = Enum('Component_Type', ['Body', 'Engine', 'Battery', 'Wheels', 'Extra'])

class Component_Type(str, Enum):
    Body = 1
    Engine = 2
    Battery = 3
    Wheels = 4
    Extra = 5


# Body structure
# Structure = Enum('Structure', ['Mini', 'Sedan', 'Van', 'Truck'])
class Structure(str, Enum):
    Mini = 1
    Sedan = 2
    Van = 3
    Truck = 4


# Engine mechanism
# Engine_Mechanism = Enum('Engine_Mechanism', ['Electric', 'Gas', 'Diesel', 'Hybrid'])
class Engine_Mechanism(str, Enum):
    Electric = 1
    Gas = 2
    Diesel = 3
    Hybrid = 4


# Wheel diameter
# Diameter = Enum('Diameter', ['Sixteen', 'Eighteen', 'Twentytwo', 'Twentyfour'])
class Diameter(str, Enum):
    Sixteen = 1
    Eighteen = 2
    Twentytwo = 3
    Twentyfour = 4


class Component:
    """
    Component superclass
    """

    def __init__(self, comp_type: Enum, name: str, manufacturer: str):
        self.comp_type = comp_type
        self.name = name
        self.manufacturer = manufacturer


class Body(Component):
    """
    Body class, includes seats and lights
    """

    def __init__(self, name: str, structure: Structure.Mini, manufacturer: str):
        super().__init__(Component_Type.Body, name, manufacturer)
        self.structure = structure

    def __eq__(self, other):
        if not isinstance(other, Body):
            return False

        return self.name == other.name and self.structure == other.structure \
               and self.manufacturer == other.manufacturer

    def __hash__(self):
        return hash((self.name, self.structure, self.manufacturer))


class Engine(Component):
    """
    Engine class, includes tank
    """

    def __init__(self, name: str, mechanism: Engine_Mechanism.Electric, manufacturer: str):
        super().__init__(Component_Type.Engine, name, manufacturer)
        self.mechanism = mechanism

    def __eq__(self, other):
        if not isinstance(other, Engine):
            return False

        return self.name == other.name and self.mechanism == other.mechanism \
               and self.manufacturer == other.manufacturer

    def __hash__(self):
        return hash((self.name, self.mechanism, self.manufacturer))


class Battery(Component):
    """
    Battery class
    """

    def __init__(self, name: str, manufacturer: str):
        super().__init__(Component_Type.Battery, name, manufacturer)

    def __eq__(self, other):
        if not isinstance(other, Battery):
            return False

        return self.name == other.name and self.manufacturer == other.manufacturer

    def __hash__(self):
        return hash((self.name, self.manufacturer))


class Wheels(Component):
    """
    Wheel class
    """

    def __init__(self, name: str, diameter: Diameter.Sixteen, manufacturer: str):
        super().__init__(Component_Type.Wheels, name, manufacturer)
        self.diameter = diameter

    def __eq__(self, other):
        if not isinstance(other, Wheels):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name and self.diameter == other.diameter \
               and self.manufacturer == other.manufacturer

    def __hash__(self):
        return hash((self.name, self.diameter, self.manufacturer))


class Extra(Component):
    """
    Extra Component class
    """

    def __init__(self, name: str, use: str, manufacturer: str):
        super().__init__(Component_Type.Extra, name, manufacturer)
        self.use = use

    def __eq__(self, other):
        if not isinstance(other, Extra):
            # don't attempt to compare against unrelated types
            return False

        return self.name == other.name and self.use == other.use \
               and self.manufacturer == other.manufacturer

    def __hash__(self):
        return hash((self.name, self.use, self.manufacturer))


class Component_factory:
    """
    Component factory
    Creates and returns components
    """

    def __init__(self, man_name):
        self.man_name = man_name

    '''
    Methods below create components for the car.
    '''

    def create_body_component(self, name, structure):
        return Body(name, structure, self.man_name)

    def create_engine_component(self, name, mechanism):
        return Engine(name, mechanism, self.man_name)

    def create_battery_component(self, name):
        return Battery(name, self.man_name)

    def create_wheels_component(self, name, diameter):
        return Wheels(name, diameter, self.man_name)

    def create_extra_component(self, name, use):
        return Extra(name, use, self.man_name)
