import configparser
import uuid

def make_settings_file(filepath, parent_filepath, params):

    config = configparser.ConfigParser()


    config['FILES'] = {
        'nodes'            : '/Users/laurawilby/dev/experiments_data/YouTube-dataset/data/nodes.csv',
        'edges'            : '/Users/laurawilby/dev/experiments_data/YouTube-dataset/data/edges.csv',
        'DB'               : filepath + '/' + uuid.uuid4().hex + '.db',
        'directory'        : filepath,
        'parent_directory' : parent_filepath,
        'dataset'          : params.get('dataset', ''),
    }

    config['PARAMS'] = {
        'target_set_prop' : params.get('target_set_prop', .01),
        'target_set_sel'  : params.get('target_set_sel', 'random'),
        'thresh_prop'     : params.get('thresh_prop', .5),
        'rounds'          : '50', # NOTE: If the simulation is complete, simulation will halt prior to completing all rounds
        'lambda_val'      : params.get('lambda_val', 1),
        'incentive_prop'  : params.get('incentive_prop', .2),
        'decay'           : params.get('decay', 0)
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)