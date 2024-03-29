import matplotlib.pyplot as plt
import configparser
import sqlite3

def thresholds_all_nodes(config, conn, thresh_db):

    try:

        thresholds_of_nodes_query = conn.execute('''SELECT threshold, nodeID FROM nodes''')

        thresh_db_conn = sqlite3.connect('{}/{}'.format(config['FILES']['parent_directory'],thresh_db))

        thresh_db_conn.execute('''CREATE TABLE IF NOT EXISTS nodes
                    (nodeID INTEGER PRIMARY KEY,
                    threshold INTEGER)''')

        thresh_db_conn.execute('PRAGMA synchronous = OFF')

        thresholds_all_nodes = list()
        threshold_records    = list()

        for node in thresholds_of_nodes_query:

            thresholds_all_nodes.append(node['threshold'])
            threshold_records.append((node['nodeID'], node['threshold']))

        thresh_db_conn.executemany('INSERT INTO nodes VALUES (?,?)', threshold_records)

        thresh_db_conn.commit()

        thresh_db_conn.close()

        n, bins, patches = plt.hist(thresholds_all_nodes, 75, range=(1,800), log=True, histtype='stepfilled')

        plt.xlabel('Threshold')
        plt.ylabel('Nodes')
        plt.title('Threshold Proportion: ' + config['PARAMS']['thresh_prop'])

        plt.savefig('{}/thresh-{}-{}'.format(config['FILES']['parent_directory'],config['PARAMS']['thresh_prop'], config['FILES']['dataset']).replace('.', ''))

        plt.cla()
        plt.clf()

    except:

        pass

def thresholds_target_set(config, conn, thresh_db):

    try:

        with open('{}/target-set.csv'.format(config['FILES']['directory']), 'r') as target_set:

            node_ids = [int(node_id.rstrip()) for node_id in target_set]

        query_string = 'SELECT threshold FROM nodes WHERE nodeID in ({seq})'.format(seq=','.join(['?']*len(node_ids)))

        thresholds_of_target_set_query = conn.execute(query_string, node_ids)
        thresholds_incentivized = [node['threshold'] for node in thresholds_of_target_set_query]

        thresh_db_conn = sqlite3.connect('{}/{}'.format(config['FILES']['parent_directory'],thresh_db))
        original_thresholds_of_target_set_query = thresh_db_conn.execute(query_string,node_ids)
        thresholds_original = [node[0] for node in original_thresholds_of_target_set_query]

        plt.hist(thresholds_original, 75, range=(0,500), log=True, histtype='stepfilled', color='#ff7f0e')
        plt.hist(thresholds_incentivized, 75, range=(0,500), log=True, histtype='stepfilled', color='#1f77b4')


        plt.xlabel('Threshold')
        plt.ylabel('Target Set Nodes')
        plt.title('Data: {}   Thre: {}   Lam: {}   Inc: {}   $: {}   Dec: {}'
                        .format(config['FILES']['dataset'],
                                config['PARAMS']['thresh_prop'], 
                                config['PARAMS']['lambda_val'], 
                                config['PARAMS']['incentive_prop'],
                                config['PARAMS']['budget'],
                                config['PARAMS']['decay']))

        plt.savefig('{}/thresholds_target_set'.format(config['FILES']['directory']))

        plt.cla()
        plt.clf()

    except:

        pass

def thresholds_influenced_nodes(config, conn):

    thresholds_of_influenced_nodes_query = conn.execute('''SELECT threshold FROM nodes WHERE inf=1''')

    thresholds_of_influenced_nodes = [node['threshold'] for node in thresholds_of_influenced_nodes_query]

    n, bins, patches = plt.hist(thresholds_of_influenced_nodes, 75, range=(1,500), log=True, histtype='stepfilled')

    plt.xlabel('Threshold')
    plt.ylabel('Influenced Nodes')
    plt.title('Data: {}   Thre: {}   Lam: {}   Inc: {}   $: {}   Dec: {}'
                    .format(config['FILES']['dataset'],
                            config['PARAMS']['thresh_prop'], 
                            config['PARAMS']['lambda_val'], 
                            config['PARAMS']['incentive_prop'],
                            config['PARAMS']['budget'],
                            config['PARAMS']['decay']))

    plt.savefig('{}/thresholds_inf'.format(config['FILES']['directory']))

    plt.cla()
    plt.clf()

def thresholds_not_influenced_nodes(config, conn):

    thresholds_of_influenced_nodes_query = conn.execute('''SELECT threshold FROM nodes WHERE inf=0''')

    thresholds_of_influenced_nodes = [node['threshold'] for node in thresholds_of_influenced_nodes_query]

    n, bins, patches = plt.hist(thresholds_of_influenced_nodes, 75, range=(1,500), log=True, histtype='stepfilled', color='#ff7f0e')

    plt.xlabel('Threshold')
    plt.ylabel('Not Influenced Nodes')
    plt.title('Data: {}   Thre: {}   Lam: {}   Inc: {}   $: {}   Dec: {}'
                    .format(config['FILES']['dataset'],
                            config['PARAMS']['thresh_prop'], 
                            config['PARAMS']['lambda_val'], 
                            config['PARAMS']['incentive_prop'],
                            config['PARAMS']['budget'],
                            config['PARAMS']['decay']))

    plt.savefig('{}/thresholds__not_inf'.format(config['FILES']['directory']))

    plt.cla()
    plt.clf()