import configparser
import uuid

def make_settings_file(filepath, parent_filepath, params):

    config = configparser.ConfigParser()


    config['FILES'] = {
        'nodes'            : params.get('nodes', ''),
        'edges'            : params.get('edges', ''),
        'DB'               : filepath + '/' + uuid.uuid4().hex + '.db',
        'directory'        : filepath,
        'parent_directory' : parent_filepath,
        'dataset'          : params.get('dataset', ''),
    }

    config['PARAMS'] = {
        'thresh_prop'     : params.get('thresh_prop', .5),
        'rounds'          : '1000', # NOTE: If the simulation is complete, simulation will halt prior to completing all rounds
        'lambda_val'      : params.get('lambda_val', 1),
        'incentive_prop'  : params.get('incentive_prop', 1),
        'decay'           : params.get('decay', 0),
        'budget'          : params.get('budget', 100)
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)