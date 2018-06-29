#################################################################
#                                                               #
#   Goes through the number of rounds requested and checks      #
#    which nodes have active neighbours exceeding the threshold #
#                                                               #
#################################################################

import sqlite3
import argparse

conn = sqlite3.connect('infSim.db')
c = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("rounds", help="number of rounds to run")
parser.add_argument("lambda", help="number of rounds that a node is active after being influenced")
args = parser.parse_args()


## for round in args.rounds
##   for node in node table not influenced
##    select nodes from activeNode table and compare to threshold. 
##    if greater or equal threshold, set influenced and add to active for round

##    remove from active if lambda is over - select round first active with query and then compare with current round