#################################################################
#                                                               #
#   Start the simulation by selecting some nodes to be active   #
#                                                               #
#################################################################

### For now nodes are selected randomly

import sqlite3
import argparse

conn = sqlite3.connect('infSim.db')
c = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("target_size", help="number of nodes to activate initially") # TODO: Move this to a config file if adding incentives?
args = parser.parse_args()

################################################ target set

## random selection of the number of nodes set in input
t = (int(args.target_size),)
target_set = c.execute('SELECT nodeID FROM node ORDER BY RANDOM() LIMIT ?', t)
nodeIDs_to_influence = [(node[0],) for node in target_set]
print(nodeIDs_to_influence)

## set influenced to true
c.executemany('UPDATE node SET inf=1 WHERE nodeID=?', nodeIDs_to_influence)

## update as active for round 1
c.executemany('UPDATE activeNodes SET active=1 WHERE nodeID=? AND round=1', nodeIDs_to_influence)

################################################ threshold

#TODO: set threshold to a proportion of neighbours