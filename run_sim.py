#################################################################
#                                                               #
#   Goes through the number of rounds requested and checks      #
#    which nodes have active neighbours exceeding the threshold #
#                                                               #
#################################################################

import sqlite3
import argparse
import configparser
import time

def run_sim(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    conn = sqlite3.connect(config['FILES']['DB'])

    c = conn.cursor()

    start_time = time.time()
    print('Starting simulation')

    for sim_round in range(int(config['PARAMS']['rounds'])):

        # NOTE: round is actually the previous round. I.e. the first round is 0 which is executed as part of initialization.
        print('Starting ROUND: ' + str(sim_round+1) + ' ' + str(round(time.time()-start_time, 2)))

        ## Add nodes which are still active to round.
        # NOTE: assumption that node becomes active and is active for lambda consecutive rounds before becoming inactive and never being active again.
        nodes_still_active_query = conn.execute('''SELECT count(*), node.nodeID FROM node
                                                    JOIN activeNodes ON node.nodeID = activeNodes.nodeID
                                                    GROUP BY node.nodeID''')

        nodes_still_active_query.arraysize = 500

        activeNodes_records = list()

        while True:

            nodes_still_active = nodes_still_active_query.fetchmany()

            if(len(nodes_still_active) != 0):

                for node in nodes_still_active:

                    if node[0] < int(config['PARAMS']['lambda_val']):

                        activeNodes_records.append((node[1], sim_round + 1))

            else:

                break

        print('Finished finding previously active nodes which are still active ' + str(round(time.time()-start_time, 2)))

        ## Newly influenced and active
        nodes_not_influenced_query = conn.execute('''SELECT count(*), node.nodeID, node.threshold FROM node
                                                        JOIN edges ON node.nodeID = edges.nodeID1
                                                        JOIN activeNodes ON edges.nodeID2 = activeNodes.nodeID
                                                        WHERE node.inf=0 AND activeNodes.round=?
                                                        GROUP BY node.nodeID''', (sim_round,))

        nodes_not_influenced_query.arraysize = 500


        infNodes_records = list()

        while True:

            nodes_not_influenced = nodes_not_influenced_query.fetchmany()

            if(len(nodes_not_influenced) != 0):

                ## For each node - check if should be influenced
                for node in nodes_not_influenced:

                    if node[0] >= node[2]:

                        activeNodes_records.append((node[1], sim_round + 1))
                        infNodes_records.append((node[1],))

            else:

                break

        print('Finished finding nodes which will be influenced this round ' + str(round(time.time()-start_time, 2)))

        c.executemany('''INSERT INTO activeNodes VALUES (?, ?)''', activeNodes_records)
        c.executemany('''UPDATE node SET inf=1 WHERE nodeID=?''', infNodes_records)
        conn.commit()

        print('Updated DB for this round ' + str(round(time.time() - start_time, 2)))
        print('Active nodes: ' + str(len(activeNodes_records)))
        print('Newly influenced nodes: ' + str(len(infNodes_records)))

        if len(infNodes_records) == 0:
            #No changes means that all node that can be influenced have already been influenced
            break

    conn.close()