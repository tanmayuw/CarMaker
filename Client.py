import json
from Builder import *
from CompatibilityDatabase import *


class Client:

    def __init__(self, clientID: str, builder: Builder, inventory: set):
        self.clientID = clientID
        self.inventory = inventory
        self._builder = builder
        self.current_components = set()
        self.suggestions = dict()

    def add_component(self, component):
        """
        Adds component to current configuration
        :param component: component to add
        :return: True if added, False otherwise
        """
        if component not in self.inventory:
            raise Warning("\n Requested Component \" " + str(component.name) + " \" not in "
                                                                               "inventory, can't add to build \n")

        else:
            self.current_components.add(component)

    def remove_component(self, component):
        """
        Removes a component from current configuration
        :param component: component to remove
        """
        self.current_components.remove(component)

    def send_build(self):
        """
        Sends current configuration to the builder to build
        :return: True if success, False otherwise
        """
        return self._builder.build(self.current_components)

    def show_conflict(self):
        """
        show conflicts in current build set
        :return: list of conflicts
        """
        return self._builder.conflicts

    def show_suggestions(self):
        """
        show suggestions to resolve conflicts
        :return: dict of suggestions per component
        """
        return self._builder.suggestions

    def save_components_to_json(self, filename: str):
        """
        saves component set to json
        :param filename: file to save to
        :return: None
        """
        component_list = list(self.current_components)
        j_write = json.dumps([vars(comp) for comp in component_list])
        f_j = open(filename, "w")
        f_j.write(j_write)
        f_j.close()

    def load_components_from_json(self, filename: str):
        """
        Loads data from given file into current component set
        :param filename: file to read from
        :return: None
        """
        f_r = open(filename, "r")
        reading = json.load(f_r)
        result = set()
        for data in reading:
            result.add(self.recreate_from_json(data))
        self.current_components = result
        f_r.close()

    def recreate_from_json(self, data: dict):
        """
        recreates a component from json dict
        :param data: component data
        :return: component object
        """
        man = data['manufacturer']
        comp_type = data['comp_type']
        factory = Component_factory(man_name=man)
        if comp_type == Component_Type.Body:
            return factory.create_body_component(data['name'], data['structure'])
        elif comp_type == Component_Type.Engine:
            return factory.create_engine_component(data['name'], data['mechanism'])
        elif comp_type == Component_Type.Battery:
            return factory.create_battery_component(data['name'])
        elif comp_type == Component_Type.Wheels:
            return factory.create_wheels_component(data['name'], data['diameter'])
        elif comp_type == Component_Type.Extra:
            return factory.create_extra_component(data['name'], data['use'])
        else:
            raise LookupError("Can't find the component type in default values")


