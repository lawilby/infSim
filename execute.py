import time
import sqlite3
import configparser
import os

# local files
from settings import make_settings_file
from db import create_db
from parse import parse_asu_data
from parse import parse_stanford_data
from initiate import thresholds_proportion
from initiate import thresholds_random
from initiate import lambda_value_degree
from initiate import incentivize
from sim import run_sim
from results import record_results
from thresholds import thresholds_all_nodes
from thresholds import thresholds_target_set
from thresholds import thresholds_influenced_nodes
from thresholds import thresholds_not_influenced_nodes

def execute_simulation(directory_name, results_db):

    start_time = time.time()
    print("START")

    results_config  = configparser.ConfigParser()
    settings_config = configparser.ConfigParser() 
    settings_config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row

    create_db(conn) 

    parse_stanford_data(settings_config, conn)

    if settings_config['PARAMS']['thresh_prop'] == '0':

        thresholds_random(settings_config, conn)

    else:

        thresholds_proportion(settings_config, conn)

    if settings_config['PARAMS']['lambda_val'] == '0':

        lambda_value_degree(settings_config, conn)

    files_in_parent_dir  = os.listdir(settings_config['FILES']['parent_directory'])
    current_threshold_db = 'nodes-thresh-{}.db'.format(settings_config['PARAMS']['thresh_prop'].replace('.', ''))

    if current_threshold_db not in files_in_parent_dir:

        thresholds_all_nodes(settings_config, conn, current_threshold_db)


    results_config['RESULTS'] = dict()
    
    incentivize(settings_config, results_config, conn)

    thresholds_target_set(settings_config, conn, current_threshold_db)

    run_sim(settings_config, conn)

    thresholds_influenced_nodes(settings_config, conn)
    thresholds_not_influenced_nodes(settings_config, conn)

    record_results(settings_config, results_config, conn, results_db) 

    with open(directory_name + '/results.ini', 'w') as configfile:

        results_config.write(configfile)

    print('END {}'.format(str(round(time.time() - start_time, 2))))

    conn.close()
    os.remove(settings_config['FILES']['DB'])
