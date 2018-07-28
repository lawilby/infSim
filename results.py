import sqlite3
import configparser
import Decimal from decimal

def record_results(settings_config, results_config, conn, results_db_conn):

    ########### CALCULATIONS ###########

    rounds = conn.execute('''SELECT max(round) FROM activeNodes''').fetchone()[0] + 1
    print("Number of rounds to finish: " + str(rounds))

    number_influenced = conn.execute('''SELECT count(*) FROM node WHERE inf=1''').fetchone()[0]
    print("Number of nodes influenced: " + str(number_influenced))

    total_nodes = conn.execute('''SELECT count(*) FROM node''').fetchone()[0]
    print("Total number of nodes: " + str(total_nodes))

    percentage = float(Decimal(number_influenced)*Decimal('100')/Decimal(total_nodes))
    print("Percentage of nodes influenced: " + str(percentage))

    ########### RESULTS CONFIG #########

    results_config = configparser.ConfigParser()
    results_config['RESULTS'].update({
        'rounds'                : str(rounds),
        'nodes_influenced'      : str(number_influenced),
        'total_nodes'           : str(total_nodes),
        'percentage_influenced' : str(percentage)
    })

    ######## RESULTS DB ##########

    results_row = ( settings_config['dataset'],
                    settings_config['target_set_prop'],
                    settings_config['target_set_sel'],
                    settings_config['thresh_prop'],
                    settings_config['lambda_val'],
                    settings_config['incentive_prop'],
                    settings_config['decay'],
                    rounds, 
                    percentage, 
                    results_config['RESULTS']['incentive_total'])

    results_db_conn.execute('INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?)', results_row)
    results_db_conn.commit()