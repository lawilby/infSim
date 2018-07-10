import configparser
import uuid

def make_settings_file(filepath):

    config = configparser.ConfigParser()


    config['FILES'] = {
        'nodes': 'YouTube-dataset/data/nodes.csv',
        'edges': 'YouTube-dataset/data/edges.csv',
        'DB'   : filepath + '/' + uuid.uuid4().hex + '.db'
    }

    config['PARAMS'] = {
        'target_size': '100',
        'thresh_prop': '.2',
        'rounds'     : '20', # NOTE: If the simulation is complete, simulation will halt prior to completing all rounds
        'lambda_val' : '1',
        'trials'     : '1'
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)