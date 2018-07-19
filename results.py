import sqlite3
import configparser

def display_results(directory_name):

    settings_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/settings.ini')

    conn = sqlite3.connect(settings_config['FILES']['DB'])

    # number of rounds

    max_round = conn.execute('''SELECT max(round) FROM activeNodes''').fetchone()[0]
    print("Number of rounds to finish: " + str(max_round + 1))

    # percentage influenced

    number_influenced = conn.execute('''SELECT count(*) FROM node WHERE inf=1''').fetchone()[0]
    print("Number of nodes influenced: " + str(number_influenced))

    total_nodes = conn.execute('''SELECT count(*) FROM node''').fetchone()[0]
    print("Total number of nodes: " + str(total_nodes))

    percentage = float(number_influenced)*100/float(total_nodes)
    print("Percentage of nodes influenced: " + str(percentage))

    results_config = configparser.ConfigParser()
    results_config['RESULTS'] = {
        'rounds'                : str(max_round + 1),
        'nodes_influenced'      : str(number_influenced),
        'total_nodes'           : str(total_nodes),
        'percentage_influenced' : str(percentage)
    }

    with open(directory_name + '/results.ini', 'w') as configfile:

        results_config.write(configfile)