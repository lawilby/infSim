import sqlite3
import configparser

def display_results(directory_name):

    config = configparser.ConfigParser()
    config.read(directory_name + '/settings.ini')

    conn = sqlite3.connect(config['FILES']['DB'])

    # number of rounds

    with open(directory_name + '/results.txt', 'w') as f:

        max_round = conn.execute('''SELECT max(round) FROM activeNodes''').fetchone()[0]
        print("Number of rounds to finish: " + str(max_round + 1))
        f.write("Number of rounds to finish: " + str(max_round + 1) + '\n')

    # percentage influenced

        number_influenced = conn.execute('''SELECT count(*) FROM node WHERE inf=1''').fetchone()[0]
        print("Number of nodes influenced: " + str(number_influenced))
        f.write("Number of nodes influenced: " + str(number_influenced) + '\n')

        total_nodes = conn.execute('''SELECT count(*) FROM node''').fetchone()[0]
        print("Total number of nodes: " + str(total_nodes))
        f.write("Total number of nodes: " + str(total_nodes) + '\n')

        percentage = float(number_influenced)*100/float(total_nodes)
        print("Percentage of nodes influenced: " + str(percentage))
        f.write("Percentage of nodes influenced: " + str(percentage) + '\n')
