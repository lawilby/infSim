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

config = configparser.ConfigParser()
config.read('settings.ini')

conn = sqlite3.connect(config['FILES']['DB'])
c = conn.cursor()


################################################ target set
start_time = time.time()
print('Starting initialization')

## random selection of the number of nodes set in input
t = (str(config['PARAMS']['target_size']),)
target_set = conn.execute('SELECT nodeID FROM node ORDER BY RANDOM() LIMIT ?', t).fetchall()
nodeIDs_to_influence = [(node[0],) for node in target_set]

print('Finished selecting random set of nodes to influence ' + str(time.time() - start_time))

## set influenced to true
c.executemany('UPDATE node SET inf=1 WHERE nodeID=?', nodeIDs_to_influence)
conn.commit()

print('Finished updating NODE table with influenced nodes ' + str(time.time() - start_time))


## update as active for round 1

active_nodes_records = [(node[0], 0) for node in target_set]
c.executemany('INSERT INTO activeNodes VALUES (?, ?)', active_nodes_records)
conn.commit()

print('Finished inserting active nodes for first round ' + str(time.time() - start_time))


################################################ threshold



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


print('Finished setting thresholds ' + str(time.time() - start_time))


conn.close()