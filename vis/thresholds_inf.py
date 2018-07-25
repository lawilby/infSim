import matplotlib.pyplot as plt
import configparser
import sqlite3

def hist_all_influenced(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    print(config['FILES']['DB'])

    conn = sqlite3.connect(config['FILES']['DB'])

    thresholds_of_influenced_nodes_query = conn.execute('''SELECT threshold FROM node WHERE inf=1''')

    thresholds_of_influenced_nodes = [node[0] for node in thresholds_of_influenced_nodes_query]

    n, bins, patches = plt.hist(thresholds_of_influenced_nodes, 75, range=(1,500), log=True, histtype='stepfilled')

    plt.xlabel('Threshold')
    plt.ylabel('Influenced Nodes')
    plt.title('Threshold Proportion: {}  Time Window: {}  Target Set Size: {}'.format(config['PARAMS']['thresh_prop'], config['PARAMS']['lambda_val'], config['PARAMS']['target_size']))

    plt.savefig(directory_name + '/thresholds_inf_' + config['PARAMS']['lambda_val'] + '.png')

    plt.cla()
    plt.clf()