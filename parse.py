import sqlite3
import configparser
import time

######################################
## Parse data from ASU datasets.    ##
##                                  ##
## Requirements:                    ##
##  nodes.csv - ids of nodes        ##
##  edges.csv - pairs of node ids   ##
##                                  ##
######################################
def parse_asu_data(config, conn):


    ###################### NODES

    start_time = time.time()
    print('Starting parsing')

    with open(config['FILES']['nodes'], 'r') as node_ids:

        node_records = [(int(node_id.rstrip()), 1, 0) for node_id in node_ids]


    conn.executemany('INSERT INTO nodes VALUES (?, ?, ?)', node_records)

    print('Finished inserting node records {}'.format(str(round(time.time() - start_time, 2))))


    ###################### EDGES

    with open(config['FILES']['edges'], 'r') as edge_pairs:

        edge_records = list()

        for edge in edge_pairs:

            edge_records.append((int(edge.split(',')[0]), int(edge.split(',')[1])))
            edge_records.append((int(edge.split(',')[1]), int(edge.split(',')[0])))

    conn.executemany('INSERT INTO edges VALUES (?, ?)', edge_records)
    print('Finished inserting edges ' + str(round(time.time() - start_time, 2)))

    conn.execute('''CREATE INDEX IF NOT EXISTS nodeID1 ON edges (nodeID1)''')
    print('Finished creating index for edges table {}'.format(str(round(time.time() - start_time, 2))))

    ######################

    conn.commit()
