#################################################################
#                                                               #
#   Start the simulation by selecting some nodes to be active   #
#                                                               #
#################################################################

### For now nodes are selected randomly

import sqlite3
import argparse
import time
import configparser
import math
from decimal import Decimal



################################################ Set Node Thresholds Proportionally
'''
Threshold is set to the proportion of the neighbours set in setting.ini
Thresholds are set to the nearest integer value using a ceiling function. 
'''
def thresholds_proportion(config, conn):

    start_time = time.time()
    print('Setting the thresholds proportionally ' + str(round(time.time() - start_time, 2)))

    number_of_neighbours_query = conn.execute('''SELECT count(*) as neighbours, nodeID FROM nodes
                                                JOIN edges ON nodes.nodeID = edges.nodeID1 GROUP BY nodes.nodeID''')

    number_of_neighbours_query.arraysize = 500

    while True:

        number_of_neighbours = number_of_neighbours_query.fetchmany()

        if len(number_of_neighbours) != 0:

            thresholds = [(int(math.ceil(float(Decimal(node['neighbours'])*Decimal(config['PARAMS']['thresh_prop'])))), node['nodeID']) for node in number_of_neighbours]
            conn.executemany('UPDATE nodes SET threshold=? WHERE nodeID=?', thresholds)
            number_of_neighbours = number_of_neighbours_query.fetchmany()

        else:

            break

    conn.commit()

    print('Finished setting thresholds ' + str(round(time.time() - start_time, 2)))


################################################ Set Node Thresholds Randomly
'''
Threshold is set to a uniform random integer in [1, d(v)]
'''
def thresholds_random(config, conn):

    from random import seed
    from random import randrange

    seed(123)

    start_time = time.time()

    number_of_neighbours_query = conn.execute('''SELECT count(*) as neighbours, nodeID FROM nodes
                                                JOIN edges ON nodes.nodeID = edges.nodeID1 GROUP BY nodes.nodeID''')

    number_of_neighbours_query.arraysize = 500

    while True:

        number_of_neighbours = number_of_neighbours_query.fetchmany()

        if len(number_of_neighbours) != 0:

            thresholds = [(randrange(1, node['neighbours']+1), node['nodeID']) for node in number_of_neighbours]
            conn.executemany('UPDATE nodes SET threshold=? WHERE nodeID=?', thresholds)
            number_of_neighbours = number_of_neighbours_query.fetchmany()

        else:

            break

    conn.commit()

    print('Finished setting thresholds ' + str(round(time.time() - start_time, 2)))


################################################ Set Lambda Value
'''
Lambda is set to the number of neighbours
'''
def lambda_value_degree(config, conn):
    
    start_time = time.time()

    number_of_neighbours_query = conn.execute('''SELECT count(*) as neighbours, nodeID FROM nodes
                                                JOIN edges ON nodes.nodeID = edges.nodeID1 GROUP BY nodes.nodeID''')

    number_of_neighbours_query.arraysize = 500

    while True:

        number_of_neighbours = number_of_neighbours_query.fetchmany()

        if len(number_of_neighbours) != 0:

            lambda_values = [(node['neighbours'], node['nodeID']) for node in number_of_neighbours]
            conn.executemany('UPDATE nodes SET lambda=? WHERE nodeID=?', lambda_values)
            number_of_neighbours = number_of_neighbours_query.fetchmany()

        else:

            break

    conn.commit()

    print('Finished setting lambda values ' + str(round(time.time() - start_time, 2)))


def incentivize(settings_config, results_config, conn):

    from random import seed
    from random import choice

    start_time = time.time()
    print('Selecting Target Set')

    seed(5)

    rows = conn.execute('SELECT nodeID, threshold FROM nodes').fetchall()

    budget = int(settings_config['PARAMS']['budget'])

    nodes_to_incentivize = list()
    active_nodes_records = list()

    with open("{}/target-set.csv".format(settings_config['FILES']['directory']), 'w') as target_file, open("{}/simulation-details.csv".format(settings_config['FILES']['directory']), "w") as details_file:
        
        while budget > 0:

            node = choice(rows)
            # node = conn.execute('''SELECT nodes.nodeID, nodes.threshold FROM nodes 
            #                         WHERE nodes.rowid=?''',(row_to_incentivize,)).fetchone()

            target_file.write('{}\n'.format(node['nodeID']))

            new_threshold_value = int(math.floor(float(Decimal(node['threshold'])*(Decimal('1') - Decimal(settings_config['PARAMS']['incentive_prop'])))))
            incentive_total = node['threshold'] - new_threshold_value
            
            if incentive_total > budget:

                break
                        
            budget = budget - incentive_total

            nodes_to_incentivize.append((new_threshold_value,node['nodeID']))
            rows.remove(node)

        conn.executemany('UPDATE nodes SET threshold=? WHERE nodeID=?', nodes_to_incentivize)

        conn.commit()

        ####### Activate nodes which now have threshold 0
        influenced_nodes = conn.execute('''SELECT nodes.nodeID, count(edges.nodeID2) as neighbours FROM nodes
                                            JOIN edges on edges.nodeID1 = nodes.nodeID
                                            WHERE nodes.threshold=0
                                            GROUP BY nodes.nodeID''').fetchall()

        nodes_to_influence = [(node['nodeID'],) for node in influenced_nodes]

        conn.executemany('''UPDATE nodes SET inf=1 WHERE nodeID=?''', nodes_to_influence)

        print('Finished updating NODES table with influenced nodes ' + str(round(time.time() - start_time, 2)))

        if settings_config['PARAMS']['decay']:

            active_nodes_records = [(node['nodeID'],0,node['neighbours']) for node in influenced_nodes]
        
        else:
            
            active_nodes_records = [(node['nodeID'], 0, 1) for node in influenced_nodes]
        
        conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', active_nodes_records)
        
        details_file.write('0,{},{}\n'.format(len(active_nodes_records), len(nodes_to_influence))) 
        
        conn.commit()
        
        print('Finished inserting active nodes for first round ' + str(round(time.time() - start_time, 2)))



