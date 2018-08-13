import sqlite3
import configparser
from decimal import Decimal
from datetime import datetime

def record_results(settings_config, results_config, conn, results_db_conn):

    ########### CALCULATIONS ###########

    try:
        rounds = conn.execute('''SELECT max(round) FROM activeNodes''').fetchone()[0] + 1
        print("Number of rounds to finish: " + str(rounds))
    except:
        rounds = 0

    number_influenced = conn.execute('''SELECT count(*) FROM nodes WHERE inf=1''').fetchone()[0]
    print("Number of nodes influenced: " + str(number_influenced))

    total_nodes = conn.execute('''SELECT count(*) FROM nodes''').fetchone()[0]
    print("Total number of nodes: " + str(total_nodes))

    percentage = float(Decimal(number_influenced)*Decimal('100')/Decimal(total_nodes))
    print("Percentage of nodes influenced: " + str(percentage))

    ########### RESULTS CONFIG #########

    results_config['RESULTS'].update({
        'rounds'                : str(rounds),
        'nodes_influenced'      : str(number_influenced),
        'total_nodes'           : str(total_nodes),
        'percentage_influenced' : str(percentage)
    })

    ######## RESULTS DB ##########

    results_row = ( datetime.now().isoformat(' '),
                    settings_config['FILES']['dataset'],
                    settings_config['PARAMS']['thresh_prop'],
                    settings_config['PARAMS']['lambda_val'],
                    settings_config['PARAMS']['incentive_prop'],
                    settings_config['PARAMS']['decay'],
                    settings_config['PARAMS']['budget'],
                    5,
                    rounds,
                    percentage)

    results_db_conn.execute('INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?)', results_row)
    results_db_conn.commit()