import matplotlib.pyplot as plt
import configparser
import sqlite3

directory_name = '/local-scratch/lw-data/vary-lambda/youTube/prop-6/19-Jul-2018:19-43-30'

config = configparser.ConfigParser()
config.read(directory_name + '/settings.ini')

print(config['FILES']['DB'])

conn = sqlite3.connect(config['FILES']['DB'])

thresholds_of_nodes_query = conn.execute('''SELECT threshold FROM node''')

thresholds_of_nodes = [node[0] for node in thresholds_of_nodes_query]

n, bins, patches = plt.hist(thresholds_of_nodes, 75, range=(1,800), log=True, histtype='stepfilled')

plt.xlabel('Threshold')
plt.ylabel('Nodes')
plt.title('Threshold Proportion: ' + config['PARAMS']['thresh_prop'])

plt.savefig('/local-scratch/lw-data/vary-lambda/youTube/prop-6/thresholds.png')

plt.cla()
plt.clf()