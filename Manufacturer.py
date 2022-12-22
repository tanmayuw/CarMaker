import json
from Components import *
from CompatibilityDatabase import *

'''
Class representing Manufacturer
'''


class Manufacturer:

    def __init__(self, man_name, database: CompatibilityDatabase):
        self.man_name = man_name
        self.database = database

    '''
    Send created component to the dependencies
    '''

    def send_to_database(self, component, compatibility_set):
        self.database.add_component(component, compatibility_set)

    '''
    Update Compatibility list of a particular component
    '''
    def update_compatibility(self, component, new_compatibility_item):
        self.database.update_compatibility(component, new_compatibility_item)
