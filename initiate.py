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
from random import seed
from random import randint


################################################ Set Node Thresholds
'''
Sets all nodes in the database found in the given directory. 
Threshold is set to the proportion of the neighbours set in setting.ini
Thresholds are set to the nearest integer value using a ceiling function. 
'''
def thresholds(config, conn):

    start_time = time.time()

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


################################################ Prepare Round Zero By Incentivizing Nodes
'''
target_set is a sqlite3 cursor object with rows from the nodes table to incentivize
'''
def incentivize(settings_config, results_config, conn, target_set):

    start_time = time.time()
    print('Starting incentivization')

    ####### Incentivizing Target Set
    nodes_to_incentivize = list()
    incentive_total = 0

    with open("{}/target-set.csv".format(settings_config['FILES']['directory']), 'w') as target_file, open("{}/simulation-details.csv".format(settings_config['FILES']['directory']), "w") as details_file:
            
        for node in target_set:

            target_file.write('{},{}\n'.format(node['nodeID'], node['threshold']))
            new_threshold_value = int(math.floor(float(Decimal(node['threshold'])*Decimal(settings_config['PARAMS']['incentive_prop']))))
            incentive_total += node['threshold'] - new_threshold_value
            nodes_to_incentivize.append((new_threshold_value, node['nodeID']))

        results_config['RESULTS']['incentive_total'] = str(incentive_total)
        
        conn.executemany('''UPDATE nodes SET threshold=? WHERE nodeID=?''', nodes_to_incentivize)

        ####### Activate nodes which now have threshold 0
        influenced_nodes = conn.execute('SELECT nodeID FROM nodes Where threshold=0').fetchall()

        nodes_to_influence = [(node['nodeID'],) for node in influenced_nodes]


        conn.executemany('''UPDATE nodes SET inf=1 WHERE nodeID=?''', nodes_to_influence)

        print('Finished updating NODES table with influenced nodes ' + str(round(time.time() - start_time, 2)))

        active_nodes_records = [(node['nodeID'], 0, 1) for node in influenced_nodes]
        conn.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', active_nodes_records)
        
        details_file.write('0,{},{}\n'.format(len(active_nodes_records), len(nodes_to_influence))) 
        
        conn.commit()

        print('Finished inserting active nodes for first round ' + str(round(time.time() - start_time, 2)))



################################################ Random Set of Nodes
def select_random_target_set(config, conn):

    start_time = time.time()
    print('Selecting Target Set')

    number_of_nodes = conn.execute('SELECT count(*) as num FROM nodes').fetchone()['num']
    target_set_size = int(Decimal(config['PARAMS']['target_set_prop'])*Decimal(number_of_nodes))

    seed(5) # TODO: determine seeds  
    random_nodes = list()

    if target_set_size > number_of_nodes:

        raise Exception()

    while len(random_nodes) != target_set_size:

        random_int = randint(1,number_of_nodes)
        if random_int not in random_nodes:
            random_nodes.append(random_int)

    query_string = 'SELECT * FROM nodes WHERE rowid in ({seq})'.format(seq=','.join(['?']*target_set_size))
    target_set = conn.execute(query_string, random_nodes)

    print('Finished Selecting Random Target Set {}'.format(str(round(time.time() - start_time, 2))))
    
    return target_set


################################################ Set of Nodes With Highest Thresholds
def select_target_set_top(config, conn):

    start_time = time.time()
    print('Selecting Target Set')

    number_of_nodes = conn.execute('SELECT count(*) as num FROM nodes ').fetchone()['num']
    target_set_size = int(Decimal(config['PARAMS']['target_set_prop'])*Decimal(number_of_nodes))

    target_set = conn.execute('SELECT nodeID FROM node ORDER BY threshold DESC LIMIT ?', target_set_size)

    print('Finished Selecting Target Set With Highest Thresholds {}'.format(str(round(time.time() - start_time, 2))))

    return target_set

################################################ Set of Nodes With Lowest Thresholds
def select_target_set_bottom(config, conn):

    start_time = time.time()
    print('Selecting Target Set')

    number_of_nodes = conn.execute('SELECT count(*) as num FROM nodes ').fetchone()['num']
    target_set_size = int(Decimal(config['PARAMS']['target_set_prop'])*Decimal(number_of_nodes))

    target_set = conn.execute('SELECT nodeID FROM node ORDER BY threshold ASC LIMIT ?', target_set_size)

    print('Finished Selecting Target Set With Lowest Thresholds {}'.format(str(round(time.time() - start_time, 2))))

    return target_set

