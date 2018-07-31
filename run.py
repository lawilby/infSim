import os
import sqlite3
import configparser

# Local Imports #
from settings import make_settings_file
from execute import execute_simulation
from db import create_results_db

parent_directory = '/local-scratch/lw-data/first-run'

results_conn = sqlite3.connect('{}/results.db'.format(parent_directory))
results_conn.row_factory = sqlite3.Row

create_results_db(results_conn)

params = {
    'dataset': 'asu_youtube'
}

threshold_levels      = [0.4,0.8]
lambda_levels         = [1,5]
selection_size_levels = [.0001,.01]
composition_levels    = ['random','top']
incentive_levels      = [0.2,1]
decay                 = [0,1]

experiment = 1
for thresh in threshold_levels:

    params['thresh_prop'] = thresh

    for lambda_val in lambda_levels:

        params['lambda_val'] = lambda_val

        for sel in selection_size_levels:

            params['target_set_prop'] = sel

            for comp in composition_levels:

                params['target_set_sel'] = comp

                for inc in incentive_levels:

                    params['incentive_prop'] = inc

                    for val in decay:

                        params['decay'] = val
                        directory_name  = '{}/{}'.format(parent_directory, experiment)
                        try:
                            os.mkdir(directory_name)
                        except:
                            pass
                        make_settings_file(directory_name, parent_directory, params)
                        execute_simulation(directory_name, results_conn)
                        experiment += 1

results_conn.close()