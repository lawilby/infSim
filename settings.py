import configparser
import uuid

config = configparser.ConfigParser()


config['FILES'] = {
    'nodes': 'YouTube-dataset/data/nodes.csv',
    'edges': 'YouTube-dataset/data/edges.csv',
    'DB'   : uuid.uuid4().hex + '.db'
}

config['PARAMS'] = {
    'target_size': '100',
    'thresh_prop': '.5',
    'rounds'     : '100', #TODO: make this until no changes (i.e until halt)
    'lambda_val' : '1',
    'trials'     : '1'
}

with open('settings.ini', 'w') as configfile:

    config.write(configfile)