import configparser
import uuid

def make_settings_file(filepath, lambda_val=1, target_set_prop=.01, thresh_prop=0.5, incentive_prop=1):

    config = configparser.ConfigParser()


    config['FILES'] = {
        'nodes'     : '/Users/laurawilby/dev/experiments_data/YouTube-dataset/data/nodes.csv',
        'edges'     : '/Users/laurawilby/dev/experiments_data/YouTube-dataset/data/edges.csv',
        'DB'        : filepath + '/' + uuid.uuid4().hex + '.db',
        'directory' : filepath
    }

    config['PARAMS'] = {
        'target_set_prop' : target_set_prop,
        'thresh_prop'     : thresh_prop,
        'rounds'          : '50', # NOTE: If the simulation is complete, simulation will halt prior to completing all rounds
        'lambda_val'      : lambda_val,
        'incentive_prop'  : incentive_prop
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)