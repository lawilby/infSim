import matplotlib.pyplot as plt
import configparser
import sqlite3

directory_name = '/local-scratch/lw-data/vary-lambda/youTube/prop-8/18-Jul-2018:15-22-55'

config = configparser.ConfigParser()
config.read(directory_name + '/settings.ini')

print(config['FILES']['DB'])

conn = sqlite3.connect(config['FILES']['DB'])

with open(directory_name + '/target_set.csv', 'r') as f:



thresholds_of_influenced_nodes_query = conn.execute('''SELECT threshold FROM node WHERE inf=1''')

thresholds_of_influenced_nodes = [node[0] for node in thresholds_of_influenced_nodes_query]

n, bins, patches = plt.hist(thresholds_of_influenced_nodes, 500, range=(1,500), log=True)

plt.savefig(directory_name + '/thresholds_all.png')