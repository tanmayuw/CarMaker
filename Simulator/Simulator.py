from Client import Client
from Manufacturer import *
from Components import Component, Component_Type, Component_factory
import CompatibilityDatabase
from Builder import Builder


def sim_client(clientID: str, builder: Builder, inventory: set):
    """
    Simulates a client. Alter below lines for
    :param clientID: client ID
    :param builder: builder object given to client
    :param inventory: inventory passed to a client
    :return: None
    """

    '''
    Client acquires client object
    '''
    client1 = Client(clientID, builder, inventory)

    '''
    create factory objects
    '''
    maruti_factory = Component_factory("Maruti")
    tesla_factory = Component_factory("Tesla")

    '''
    create and add components to design
    '''
    # body = maruti_factory.create_body_component('Maruti_alto', Structure.Mini)
    body = tesla_factory.create_body_component('Tesla_X', Structure.Sedan)

    # engine = maruti_factory.create_engine_component('Maruti_engine_small', Engine_Mechanism.Gas)
    engine = tesla_factory.create_engine_component('Tesla_engine_med', Engine_Mechanism.Electric)

    # battery = maruti_factory.create_battery_component('Maruti_battery_small')
    battery = tesla_factory.create_battery_component('Tesla_battery_big')

    # wheels = maruti_factory.create_wheels_component('Maruti_wheels_small', Diameter.Sixteen)
    wheels = tesla_factory.create_wheels_component('Tesla_wheels_small', Diameter.Eighteen)

    radio = Component_factory('Doordarshan').create_extra_component('DD_radio', 'Radio')

    try:
        client1.add_component(body)
        client1.add_component(engine)
        client1.add_component(wheels)
        client1.add_component(battery)
        client1.add_component(radio)
    except Warning as w:
        print(w)

    '''
    Optionally load components from a file
    '''
    # client1.load_components_from_json('./correct_build1.json')

    '''
    Send to build
    '''
    print('Sending to build with following components :')
    print([comp.name for comp in client1.current_components])
    print("\n Building ... \n")

    built = client1.send_build()

    if built:
        print("Build Succeeded! \n")
        client1.save_components_to_json('correct_build1.json')
    else:
        print("Build Failed. Below are the conflicts and potential resolves")
        print("\n Conflicts: ")
        print([(x.name, y.name) for (x, y) in client1.show_conflict()])
        print("\n Suggestions: ")
        print([x.name for x in client1.show_suggestions()])


def sim_manufacturer(man_name: str, database: CompatibilityDatabase):
    """
    Simulates a manufacturer
    :param man_name: Manufacturer name
    :param database: database for Manufacturer to add to
    :return: None
    """

    '''
    Define manufacturer factory and create a component with its compatibility set
    '''

    print("Creating Component....")
    man1 = Manufacturer(man_name, database)
    man_factory = Component_factory(man_name)
    all_compatible_radio = man_factory.create_extra_component('DD_radio', 'Radio')
    compatibility_set = set(database.inventory.values())

    '''
    Send component to database
    '''
    man1.send_to_database(all_compatible_radio, compatibility_set)

    '''
    update compatibility sets of all compatible components
    '''
    for comp in database.inventory.keys():
        man1.update_compatibility(comp, all_compatible_radio)

    print("Component added!")
