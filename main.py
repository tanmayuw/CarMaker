from CompatibilityDatabase import CompatibilityDatabase
from Simulator import Simulator
from importlib import reload
from Builder import Builder

'''
Main class, connects to client or manufacturer simulation
'''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('booting up dependencies...')
    database = CompatibilityDatabase('inventory.pkl', 'dependency.pkl')

    # Choose how to initialize the dependencies
    database.default_init()
    # dependencies.init_from_file()

    response = ''
    while response == '' or response[0].lower() != 'e':

        response = input('Welcome to Custom Car Builder! \n '
                         'enter \'c\' for Client and \'m\' for manufacturer simulation.'
                         'Enter \'e\' to exit: \n')

        '''
        Reloads Simulator.py in every loop. Changes will be
        reflected after every cycle
        '''
        if response != '':
            if response[0].lower() == 'm':
                reload(Simulator)
                man_name = "Doordarshan"
                Simulator.sim_manufacturer(man_name, database)

            elif response[0].lower() == 'c':
                reload(Simulator)
                builder = Builder('client1', database)
                inventory = set(database.inventory.keys())
                Simulator.sim_client('client1', builder, inventory)
        print("-"*100)

    print('shutting down....')
    database.close()
    del database
