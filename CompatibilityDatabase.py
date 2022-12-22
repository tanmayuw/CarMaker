import pickle
import time
import warnings
from Components import *
from uuid import uuid1
from threading import Thread


class CompatibilityDatabase:
    """
    The database class. In this example, it is collection of key-value stores.
    Ideally should be an SQL database as it is easier for users
    and manufacturers to filter components they need.
    """

    def __init__(self, inventory_file: str, dependency_file: str):
        """
        init function
        :param inventory_file: file to save and load inventory from
        :param dependency_file: file to save and load dependency dependencies from
        """
        # Initializing file
        self.inventory_file = inventory_file
        self.dependency_file = dependency_file

        # dictionary mapping object to its id
        self.inventory = dict()

        # reverse inventory mapping id to object
        self.id_chart = dict()

        # Current dependencies is a dictionary which keeps track of dependencies
        # key: tuple(component, type)
        # value: set of all compatible objects as tuple(component, type)
        self.dependencies = dict()

        self.initialized = False
        self.write_thread = Thread(target=self.periodic_write, daemon=True)

    def fill_id_chart(self):
        """
        fills id_chart
        """
        for (key, value) in self.inventory.items():
            self.id_chart[value] = key

    def cid(self, component: Component) -> str:
        """
        returns component ID in the inventory
        :param component: Component to fetch ID for
        :return: ID of the given component
        """
        return self.inventory[component]

    def component_from_id(self, comp_id: str):
        """
        returns component with given ID
        :param comp_id:
        :return: Component with given ID
        """
        return self.id_chart[comp_id]

    def default_init(self):
        """
        An example initialization of the dependencies state
        """

        if not self.initialized:
            self.initialized = True
            self.write_thread.start()

        # Generate components
        maruti_body = Body('Maruti_alto', Structure.Mini, 'Maruti')
        maruti_engine = Engine('Maruti_engine_small', Engine_Mechanism.Gas, 'Maruti')
        maruti_battery = Battery('Maruti_battery_small', 'Maruti')
        maruti_wheels = Wheels('Maruti_wheels_small', Diameter.Sixteen, 'Maruti')
        maruti_radio = Extra('Maruti_radio', 'Radio', 'Maruti')

        tesla_body = Body('Tesla_X', Structure.Sedan, 'Tesla')
        tesla_engine = Engine('Tesla_engine_med', Engine_Mechanism.Electric, 'Tesla')
        tesla_battery = Battery('Tesla_battery_big', 'Tesla')
        tesla_wheels = Wheels('Tesla_wheels_small', Diameter.Eighteen, 'Tesla')
        tesla_radio = Extra('Tesla_radio', 'Radio', 'Tesla')

        # Add to inventory
        maruti_ids = list()
        for comp in [maruti_body, maruti_engine, maruti_battery, maruti_wheels, maruti_radio]:
            self.inventory[comp] = str(uuid1())
            maruti_ids.append(self.inventory[comp])

        tesla_ids = list()
        for comp_t in [tesla_body, tesla_engine, tesla_battery, tesla_wheels, tesla_radio]:
            self.inventory[comp_t] = str(uuid1())
            tesla_ids.append(self.inventory[comp_t])

        # Add dependencies dependency for Maruti
        self.dependencies[self.cid(maruti_body)] = set(maruti_ids + [self.cid(tesla_engine), self.cid(tesla_wheels)])
        self.dependencies[self.cid(maruti_engine)] = set([self.cid(tesla_radio), self.cid(tesla_body)] + maruti_ids)
        self.dependencies[self.cid(maruti_battery)] = set(maruti_ids + [self.cid(tesla_wheels)])
        m_wheel_list = maruti_ids + tesla_ids
        m_wheel_list.remove(self.cid(tesla_wheels))
        self.dependencies[self.cid(maruti_wheels)] = set(m_wheel_list)
        m_radio_list = maruti_ids + tesla_ids
        m_radio_list.remove(self.cid(tesla_radio))
        self.dependencies[self.cid(maruti_radio)] = set(m_radio_list)

        # Add dependencies dependency for Tesla
        self.dependencies[self.cid(tesla_body)] = set(tesla_ids + [self.cid(maruti_engine), self.cid(maruti_wheels)])
        self.dependencies[self.cid(tesla_engine)] = set(tesla_ids + [self.cid(maruti_wheels), self.cid(maruti_radio)])
        self.dependencies[self.cid(tesla_battery)] = set(tesla_ids + [self.cid(maruti_engine), self.cid(maruti_wheels)])
        t_wheel_set = set(maruti_ids + tesla_ids)
        t_wheel_set.remove(self.cid(maruti_wheels))
        self.dependencies[self.cid(tesla_wheels)] = t_wheel_set
        t_radio_set = set(maruti_ids + tesla_ids)
        t_radio_set.remove(self.cid(maruti_radio))
        self.dependencies[self.cid(tesla_radio)] = t_radio_set

        self.fill_id_chart()

    def periodic_write(self):
        """
        Periodically saves to disk every 10 seconds
        """
        while self.initialized is True:
            # print('saving.....')
            self.write_state_to_disk()
            time.sleep(10.0)

    def write_state_to_disk(self):
        """
        Writes the current database state to disk
        """
        f_i = open(self.inventory_file, "wb")
        pickle.dump(self.inventory, f_i)
        f_i.close()

        f_dep = open(self.dependency_file, "wb")
        pickle.dump(self.dependencies, f_dep)
        f_dep.close()

    def init_from_file(self):
        """
        initialize the database from existing file
        """

        if not self.initialized:
            self.initialized = True
            self.write_thread.start()

        f_i = open(self.inventory_file, "rb")
        self.inventory = pickle.load(f_i)
        f_i.close()

        f_dep = open(self.dependency_file, "rb")
        self.dependencies = pickle.load(f_dep)
        f_dep.close()

        self.fill_id_chart()

    def add_component(self, component: Component, compatibility_set: set):
        """
        Adds new component to the database
        :param component: Component to add
        :param compatibility_set: Compatibility set for the Component
        :return: None
        """
        if component not in self.inventory:
            self.inventory[component] = str(uuid1())
            self.dependencies[self.cid(component)] = compatibility_set
            self.id_chart[self.inventory[component]] = component
        else:
            warnings.warn('Component already exists. Use update_compatibility to add more compatible items')

    def update_compatibility(self, component, new_item):
        """
        updates compatibility list of a particular component
        :param component: component to update
        :param new_item: item to add in compatibility set
        :return: None
        """
        if component not in self.inventory:
            raise KeyError('Component not in inventory')

        elif new_item not in self.inventory:
            raise KeyError('new compatible item not in inventory')
        else:
            (self.dependencies[self.cid(component)]).add(self.cid(new_item))

    def compatibility(self, comp1, comp2):
        """
        compares the compatibility of two objects in database
        :param comp1: first object
        :param comp2: second object
        :return: True if compatible, False otherwise
        """
        if comp1 not in self.inventory:
            raise KeyError("First component not in inventory")

        elif comp2 not in self.inventory:
            raise KeyError("Second component not in inventory")

        else:
            return self.cid(comp2) in self.dependencies[self.cid(comp1)]

    def close(self):
        """
        Closes the database
        """
        self.initialized = False
        self.write_thread.join()
        del self.inventory
        del self.dependencies
