######################################
## Parse data from ASU datasets.    ##
##                                  ##
## Requirements:                    ##
##  nodes.csv - ids of nodes        ##
##  edges.csv - pairs of node ids   ##
##                                  ##
######################################

import sqlite3

conn = sqlite3.connect('infSim.db')

c = conn.cursor()



conn.close()