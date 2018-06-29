######################################
## Parse data from ASU datasets.    ##
##                                  ##
## Requirements:                    ##
##  nodes.csv - ids of nodes        ##
##  edges.csv - pairs of node ids   ##
##                                  ##
######################################

import sqlite3
import argparse

conn = sqlite3.connect('infSim.db')
parser = argparse.ArgumentParser()
parser.add_argument("node_file", help="csv file with node ids")
parser.add_argument("edge_file", help="csv file with edge pairs")
args = parser.parse_args()

c = conn.cursor()

###################### nodes

with open(args.node_file, 'r') as node_ids:

    node_records = [(int(node_id.rstrip()), 1, 1, 0) for node_id in node_ids]


c.executemany('INSERT INTO node VALUES (?, ?, ?, ?)', node_records)

###################### edges

with open(args.edge_file, 'r') as edge_pairs:

    # Here only one entry for each edge in an undirected matter. Will this work for the query??
    edge_records = [(int(edge.split(',')[0]), int(edge.split(',')[1])) for edge in edge_pairs]

c.executemany('INSERT INTO edges VALUES (?, ?)', edge_records)

###################### set up round 1 TODO: should this be here?

with open(args.node_file, 'r') as node_ids:

    activeNodes_records = [(int(node_id.rstrip()), 1, 0) for node_id in node_ids]


c.executemany('INSERT INTO activeNodes VALUES (?, ?, ?)', activeNodes_records)

######################
conn.commit()
conn.close()