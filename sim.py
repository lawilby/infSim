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

def run_sim(config, conn):

    start_time = time.time()
    print('Starting Simulation')

    with open(config['FILES']['directory'] + "/simulation-details.txt", "w") as f: # record details of sim to file for reference

        for sim_round in range(int(config['PARAMS']['rounds'])):

            # NOTE: round is actually the previous round. I.e. the first round is 0 which is executed as part of initialization.
            round_string = 'Starting ROUND: {}  {}'.format(str(sim_round+1), str(round(time.time()-start_time, 2)))
            print(round_string)
            f.write(round_string)

            ## Add nodes which are still active to round.
            # NOTE: assumption that node becomes active and is active for lambda consecutive rounds before becoming inactive and never being active again.
            nodes_still_active_query = conn.execute('''SELECT count(*) as num_rounds_active, nodes.nodeID FROM nodes
                                                        JOIN activeNodes ON nodes.nodeID = activeNodes.nodeID
                                                        GROUP BY nodes.nodeID
                                                        ORDER BY count(*) ASC''')

            nodes_still_active_query.arraysize = 500

            activeNodes_records = list()

            while True:

                nodes_still_active = nodes_still_active_query.fetchmany()

                if(len(nodes_still_active) != 0):

                    for node in nodes_still_active:

                        if node['num_rounds_active'] < int(config['PARAMS']['lambda_val']):

                            activeNodes_records.append((node['nodeID'], sim_round + 1))

                        else:

                            # Ordered by count so this condition will not be met on the rest of the nodes
                            # TODO: can I refactor this to make it not do the rest of the fetches as well?
                            break

                else:

                    break

            print('Finished finding previously active nodes which are still active ' + str(round(time.time()-start_time, 2)))

            ## Newly influenced and active
            nodes_not_influenced_query = conn.execute('''SELECT nodes.nodeID, nodes.threshold FROM nodes
                                                            JOIN edges ON nodes.nodeID = edges.nodeID1
                                                            JOIN activeNodes ON edges.nodeID2 = activeNodes.nodeID
                                                            WHERE nodes.inf=0 AND activeNodes.round=?
                                                            GROUP BY nodes.nodeID HAVING count(*) >= nodes.threshold''', (sim_round,))

            nodes_not_influenced_query.arraysize = 500


            infNodes_records = list()

            while True:

                nodes_not_influenced = nodes_not_influenced_query.fetchmany()

                if(len(nodes_not_influenced) != 0):

                    # ## For each node - check if should be influenced
                    for node in nodes_not_influenced:

                        activeNodes_records.append((node['nodeID'], sim_round + 1))
                        infNodes_records.append((node['nodeID'],))

                else:

                    break

            print('Finished finding nodes which will be influenced this round ' + str(round(time.time()-start_time, 2)))

            conn.executemany('''INSERT INTO activeNodes VALUES (?, ?)''', activeNodes_records)
            conn.executemany('''UPDATE nodes SET inf=1 WHERE nodeID=?''', infNodes_records)
            conn.commit()

            print('Updated DB for this round ' + str(round(time.time() - start_time, 2)))
            print('Active nodes: ' + str(len(activeNodes_records)))
            print('Newly influenced nodes: ' + str(len(infNodes_records)))
            f.write('Active nodes: ' + str(len(activeNodes_records)) + '\n')
            f.write('Newly influenced nodes: ' + str(len(infNodes_records)) + '\n')

            if len(infNodes_records) == 0:
                #No changes means that all node that can be influenced have already been influenced
                break
