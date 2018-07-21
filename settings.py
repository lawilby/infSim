import configparser
import uuid

def make_settings_file(filepath, lambda_val, target_set_size, thresh_prop, incentive=0):

    config = configparser.ConfigParser()


    config['FILES'] = {
        'nodes': '/local-scratch/lw-data/YouTube-dataset/data/nodes.csv',
        'edges': '/local-scratch/lw-data/YouTube-dataset/data/edges.csv',
        'DB'   : filepath + '/' + uuid.uuid4().hex + '.db'
    }

    config['PARAMS'] = {
        'target_size': target_set_size,
        'thresh_prop': thresh_prop,
        'rounds'     : '50', # NOTE: If the simulation is complete, simulation will halt prior to completing all rounds
        'lambda_val' : lambda_val,
        'trials'     : '1',
        'incentive'  : incentive
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)