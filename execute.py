import time
import sqlite3
import configparser
import os

# local files
from infSim.settings import make_settings_file
from infSim.db import create_db
from infSim.parse import parse_asu_data
from infSim.initiate import thresholds
from infSim.initiate import select_random_target_set
from infSim.initiate import incentivize
from infSim.sim import run_sim
from infSim.results import record_results
from infSim.thresholds import thresholds_all_nodes
from infSim.thresholds import thresholds_target_set
from infSim.thresholds import thresholds_influenced_nodes
from infSim.thresholds import thresholds_not_influenced_nodes

def execute_simulation(directory_name, params, results_db):

    start_time = time.time()
    print("START")

    make_settings_file(directory_name, params) # TODO: do this in outer run file

    results_config  = configparser.ConfigParser()
    settings_config = configparser.ConfigParser() 
    settings_config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    parse_asu_data(settings_config, conn)

    thresholds(settings_config, conn)

    if params['target_set_sel'] == 'random':

        target_set = select_random_target_set(settings_config, conn)

    if params['target_set_sel'] == 'top':

        target_set = select_target_set_top(settings_config, conn)

    files_in_parent_dir  = os.listdir(settings_config['FILES']['parent_directory'])
    current_threshold_db = 'nodes-thresh-{}.db'.format(settings_config['PARAMS']['thresh_prop'].replace('.', ''))

    if current_threshold_db not in files_in_parent_dir:

        thresholds_all_nodes(settings_config, conn, current_threshold_db)


    results_config['RESULTS'] = dict()
    
    incentivize(settings_config, results_config, conn, target_set)

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
