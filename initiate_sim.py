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

################################################ target set
def select_target_set_random(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    conn = sqlite3.connect(config['FILES']['DB'])
    c = conn.cursor()

    start_time = time.time()
    print('Starting initialization')

    ## random selection of the number of nodes set in input
    t = (str(config['PARAMS']['target_size']),)
    target_set = conn.execute('SELECT nodeID FROM node ORDER BY RANDOM() LIMIT ?', t).fetchall()
    nodeIDs_to_influence = [(node[0],) for node in target_set]

    print('Finished selecting random set of nodes to influence ' + str(round(time.time() - start_time, 2)))

    ## set influenced to true
    c.executemany('UPDATE node SET inf=1 WHERE nodeID=?', nodeIDs_to_influence)
    conn.commit()

    print('Finished updating NODE table with influenced nodes ' + str(round(time.time() - start_time, 2)))


    ## update as active for round 1

    active_nodes_records = [(node[0], 0) for node in target_set]
    c.executemany('INSERT INTO activeNodes VALUES (?, ?)', active_nodes_records)
    conn.commit()

    print('Finished inserting active nodes for first round ' + str(round(time.time() - start_time, 2)))

    conn.close()

################################################ threshold
def set_thresholds_proportional(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    conn = sqlite3.connect(config['FILES']['DB'])
    c = conn.cursor()

    start_time = time.time()

    number_of_neighbours_query = conn.execute('''SELECT count(*), nodeID FROM node 
                                                JOIN edges ON node.nodeID = edges.nodeID1 GROUP BY node.nodeID''')

    number_of_neighbours_query.arraysize = 500

    while True:

        number_of_neighbours = number_of_neighbours_query.fetchmany()

        if len(number_of_neighbours) != 0:

            thresholds = [(int(math.ceil(node[0]*float(config['PARAMS']['thresh_prop']))), node[1]) for node in number_of_neighbours]
            c.executemany('UPDATE node SET threshold=? WHERE nodeID=?', thresholds)
            number_of_neighbours = number_of_neighbours_query.fetchmany()

        else: 

            break

    conn.commit()


    print('Finished setting thresholds ' + str(round(time.time() - start_time, 2)))

    conn.close()