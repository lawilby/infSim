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

config = configparser.ConfigParser()
config.read('settings.ini')

conn = sqlite3.connect(config['FILES']['DB'])
c = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("target_size", help="number of nodes to activate initially") # TODO: Move this to a config file if adding incentives?
parser.add_argument("threshold_proportion", help="proportion of neighbours which determine the node threshold")
args = parser.parse_args()

################################################ target set
start_time = time.time()
## random selection of the number of nodes set in input
t = (int(args.target_size),)
target_set = c.execute('SELECT nodeID FROM node ORDER BY RANDOM() LIMIT ?', t)
nodeIDs_to_influence = [(node[0],) for node in target_set]

print(time.time() - start_time)
## set influenced to true
c.executemany('UPDATE node SET inf=1 WHERE nodeID=?', nodeIDs_to_influence)
print(time.time() - start_time)
## update as active for round 1
c.executemany('UPDATE activeNodes SET active=1 WHERE nodeID=? AND round=1', nodeIDs_to_influence)
print(time.time() - start_time)
conn.commit()
################################################ threshold



number_of_neighbours_query = conn.execute('''SELECT count(*), nodeID FROM node 
                                            JOIN edges ON node.nodeID = edges.nodeID1 GROUP BY node.nodeID''')

number_of_neighbours_query.arraysize = 500

while True:

    number_of_neighbours = number_of_neighbours_query.fetchmany()

    if len(number_of_neighbours) != 0:

        thresholds = [(int(node[0]*float(args.threshold_proportion)), node[1]) for node in number_of_neighbours]
        c.executemany('UPDATE node SET threshold=? WHERE nodeID=?', thresholds)
        number_of_neighbours = number_of_neighbours_query.fetchmany()

    else: 

        break

print(time.time() - start_time)

conn.commit
conn.close()