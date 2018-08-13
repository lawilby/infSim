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
from decimal import Decimal


def run_sim(config, conn):

    start_time = time.time()
    print('Starting Simulation')

    with open(config['FILES']['directory'] + "/simulation-details.csv", "a") as f: # record details of sim to file for reference

        ''' NOTE: Updating active and influenced nodes for NEXT round based on previous round. 
        i.e. Nodes in round 0 have already been added as active and influenced for round 0. On first run, nodes still active for round 1 are added, 
        and influenced nodes for round 1 are updated as influenced based on nodes active in round 0 and are also added to the active nodes for round 1. 
        '''
        for sim_round in range(1,int(config['PARAMS']['rounds'])+1):

            round_string = 'Starting ROUND: {}  {}'.format(str(sim_round), str(round(time.time()-start_time, 2)))
            print(round_string)


            ## Add nodes which are still active to current round.
            # NOTE: assumption that node becomes active and is active for lambda consecutive rounds before becoming inactive and never being active again.
            nodes_still_active_query = conn.execute('''SELECT count(distinct(activeNodes.round)) as num_rounds_active, 
                                                              count(distinct(edges.nodeID2)) as neighbours, 
                                                              nodes.nodeID, 
                                                              nodes.lambda FROM nodes
                                                        JOIN activeNodes ON nodes.nodeID = activeNodes.nodeID
                                                        JOIN edges ON nodes.nodeID = edges.nodeID1
                                                        GROUP BY nodes.nodeID
                                                        HAVING count(distinct(activeNodes.round)) < nodes.lambda''')

            nodes_still_active_query.arraysize = 500
            activeNodes_records = list()

            while True:

                nodes_still_active = nodes_still_active_query.fetchmany()

                if(len(nodes_still_active) != 0):

                    for node in nodes_still_active:

                        if int(config['PARAMS']['decay']):

                            power = float(Decimal(node['neighbours']) - (Decimal(node['neighbours'])/Decimal(node['lambda']))*Decimal(node['num_rounds_active']))

                        else:

                            power = 1

                        activeNodes_records.append((node['nodeID'], sim_round, power))
                       
                else:

                    break
            
            print('Finished finding previously active nodes which are still active ' + str(round(time.time()-start_time, 2)))

            ''' Look at nodes which have not been influenced. 
                If they have >= threshold neighbours which are active this round, then they become influenced and active. 
            '''
            nodes_not_influenced_query = conn.execute('''SELECT nodes.nodeID, nodes.threshold FROM nodes
                                                            JOIN edges ON nodes.nodeID = edges.nodeID1
                                                            JOIN activeNodes ON edges.nodeID2 = activeNodes.nodeID
                                                            WHERE nodes.inf=0 AND activeNodes.round=?
                                                            GROUP BY nodes.nodeID 
                                                            HAVING sum(activeNodes.power) >= nodes.threshold''', (sim_round-1,))

            nodes_not_influenced_query.arraysize = 500
            infNodes_records = list()

            while True:

                nodes_not_influenced = nodes_not_influenced_query.fetchmany()

                if(len(nodes_not_influenced) != 0):

                    # ## For each node - check if should be influenced
                    for node in nodes_not_influenced:

                        if int(config['PARAMS']['decay']):

                            neighbours = conn.execute('''SELECT count(edges.nodeID2) FROM edges WHERE edges.nodeID1=?''', (node['nodeID'],)).fetchone()[0]
                            power = neighbours

                        else:

                            power = 1
                        
                        activeNodes_records.append((node['nodeID'], sim_round, power))
                        infNodes_records.append((node['nodeID'],))

                else:

                    break

            print('Finished finding nodes which will be influenced this round ' + str(round(time.time()-start_time, 2)))

            conn.executemany('''INSERT INTO activeNodes VALUES (?, ?, ?)''', activeNodes_records)
            conn.executemany('''UPDATE nodes SET inf=1 WHERE nodeID=?''', infNodes_records)
            conn.commit()

            print('Updated DB for this round {}\nActive nodes: {}\nNewly influenced nodes: {}'.format(round(time.time() - start_time, 2), 
                                                                            len(activeNodes_records), 
                                                                            len(infNodes_records), ))
            
            f.write('{},{},{}\n'.format(sim_round, len(activeNodes_records), len(infNodes_records)))

            if len(infNodes_records) == 0:
                ''' No changes means that all node that can be influenced have already been influenced.
                    Set of active nodes for next run will be the same as the set for the round just checked, so no further 
                    rounds need to be executed.
                '''
                break
