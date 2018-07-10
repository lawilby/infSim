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
        'thresh_prop': '.5',
        'rounds'     : '20', #TODO: make this until no changes (i.e until halt)
        'lambda_val' : '1',
        'trials'     : '1'
    }

    with open(filepath + '/settings.ini', 'w') as configfile:

        config.write(configfile)