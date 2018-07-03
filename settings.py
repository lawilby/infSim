import configparser

config = configparser.ConfigParser()

config['FILES'] = {
    'nodes': 'YouTube-dataset/data/nodes.csv',
    'edges': 'YouTube-dataset/data/edges.csv',
    'DB'   : 'infSim2.db'
}

with open('settings.ini', 'w') as configfile:

    config.write(configfile)