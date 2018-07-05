######################################
## Parse data from ASU datasets.    ##
##                                  ##
## Requirements:                    ##
##  nodes.csv - ids of nodes        ##
##  edges.csv - pairs of node ids   ##
##                                  ##
######################################

import sqlite3
import configparser
import time

config = configparser.ConfigParser()
config.read('settings.ini')

conn = sqlite3.connect(config['FILES']['DB'])


c = conn.cursor()

###################### nodes

start_time = time.time()
print(time.time() - start_time)
with open(config['FILES']['nodes'], 'r') as node_ids:

    node_records = [(int(node_id.rstrip()), 1, 1, 0) for node_id in node_ids]


c.executemany('INSERT INTO node VALUES (?, ?, ?, ?)', node_records)
print(time.time() - start_time)


###################### edges

with open(config['FILES']['edges'], 'r') as edge_pairs:

    edge_records = list()

    for edge in edge_pairs:

        edge_records.append((int(edge.split(',')[0]), int(edge.split(',')[1])))
        edge_records.append((int(edge.split(',')[1]), int(edge.split(',')[0])))

c.executemany('INSERT INTO edges VALUES (?, ?)', edge_records)
print(time.time() - start_time)

c.execute('''CREATE INDEX IF NOT EXISTS nodeID1 ON edges (nodeID1)''')
print(time.time() - start_time)

###################### set up round 1 TODO: should this be here?

with open(config['FILES']['nodes'], 'r') as node_ids:

    activeNodes_records = [(int(node_id.rstrip()), 1, 0) for node_id in node_ids]

c.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', activeNodes_records)
print(time.time() - start_time)


######################

conn.commit()
conn.close()