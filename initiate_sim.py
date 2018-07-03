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

## random selection of the number of nodes set in input
t = (int(args.target_size),)
target_set = c.execute('SELECT nodeID FROM node ORDER BY RANDOM() LIMIT ?', t)
nodeIDs_to_influence = [(node[0],) for node in target_set]

## set influenced to true
c.executemany('UPDATE node SET inf=1 WHERE nodeID=?', nodeIDs_to_influence)

## update as active for round 1
c.executemany('UPDATE activeNodes SET active=1 WHERE nodeID=? AND round=1', nodeIDs_to_influence)

conn.commit()
################################################ threshold

start_time = time.time()

c.execute('''SELECT nodeID FROM node 
                        JOIN edges ON node.nodeID = edges.nodeID1 LIMIT 500000''')

number_of_neighbours = c.fetchall()

nodeID = number_of_neighbours[0][0]
neighbour_count = 0
thresholds = list()
count = 0

# TODO: make this better!! Count() is so slow in sqlite it seems so that is why I am doing it this way. 
for row in number_of_neighbours:

    if row[0] == nodeID:

        neighbour_count +=1

    else:

        thresholds.append((int(neighbour_count*float(args.threshold_proportion)), nodeID))
        neighbour_count = 1
        nodeID = row[0]

    if count == len(number_of_neighbours)-1:

        thresholds.append((int(neighbour_count*float(args.threshold_proportion)), nodeID))

    count += 1

print(thresholds)
print(len(thresholds))

print(time.time() - start_time)

c.executemany('UPDATE node SET threshold=? WHERE nodeID =?', thresholds)

print(time.time() -start_time)

conn.commit()
conn.close()