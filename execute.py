import time

# local files
from infSim.settings import make_settings_file
from infSim.db import create_db
from infSim.parse import parse_asu_data
from infSim.initiate import select_random_target_set
from infSim.initiate import incentivize
from infSim.sim import run_sim
import results
# import plots

def execute_simulation(directory_name, params):

    start_time = time.time()
    print("START")

    make_settings_file(directory_name, params)

    results_config  = configparser.ConfigParser()
    settings_config = configparser.ConfigParser() 
    settings_config.read(directory_name + '/settings.ini')
    conn = sqlite3.connect(settings_config['FILES']['DB'])
    conn.row_factory = sqlite3.Row
    
    create_db(conn) 

    parse_asu_data(settings_config, conn)

    if params['target_set_selection'] == 'random':

        target_set = select_random_target_set(settings_config, conn)

    results_config['RESULTS'] = dict()
    
    incentivize(settings_config, results_config, conn, target_set)

    run_sim(settings_config, conn)

    ## display results

    results.display_results(directory_name)

    # plots.results_plot(directory_name)

    print('END {}'.format(str(round(time.time() - start_time, 2))))

    conn.close()

    # TODO: cleanup files