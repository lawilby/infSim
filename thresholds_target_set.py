import matplotlib.pyplot as plt
import configparser
import sqlite3

def hist_target_set(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    print(config['FILES']['DB'])

    conn = sqlite3.connect(config['FILES']['DB'])

    with open(directory_name + '/target-set.csv', 'r') as target_set:

        node_ids = [int(node_id.rstrip().replace(',', '')) for node_id in target_set]

    query_string = 'SELECT threshold FROM node WHERE nodeID in ({seq})'.format(seq=','.join(['?']*len(node_ids)))

    thresholds_of_target_set_query = conn.execute(query_string, node_ids)

    thresholds = [node[0] for node in thresholds_of_target_set_query]

    n, bins, patches = plt.hist(thresholds, 250, range=(1,500), log=True, histtype='stepfilled')

    plt.xlabel('Threshold')
    plt.ylabel('Target Set Nodes')
    plt.title('Threshold Proportion: {}  Time Window: {}  Target Set Size: {}'.format(config['PARAMS']['thresh_prop'], config['PARAMS']['lambda_val'], config['PARAMS']['target_size']))

    plt.savefig('{}/thresholds_target_{}.png'.format(directory_name, config['PARAMS']['lambda_val']))

    plt.cla()
    plt.clf()