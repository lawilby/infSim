import os
import sqlite3
import configparser

# Local Imports #
from settings import make_settings_file
from execute import execute_simulation
from db import create_results_db

parent_directory = '/Users/laurawilby/dev/experiments_data/new'

results_conn = sqlite3.connect('{}/results.db'.format(parent_directory))
results_conn.row_factory = sqlite3.Row

create_results_db(results_conn)

params = dict()

threshold_levels      = [0.5,0]
lambda_levels         = [2,0]
incentive_levels      = [.5,1]
decay                 = [0,1]
budget_levels         = [50,200]
stan_youtube          = {
                         'name'     : 'stan_youtube',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/youtube.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/youtube.txt'
                        }

stan_enron            = {
                         'name'     : 'stan_enron',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/enron.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/enron.txt'
                        }
datasets              = [stan_enron,stan_youtube]

experiment = 1

for dataset in datasets:

    params['dataset'] = dataset['name']
    params['nodes']   = dataset['edges']
    params['edges']   = dataset['nodes']

    for thresh in threshold_levels:

        params['thresh_prop'] = thresh

        for incentive in incentive_levels:

            params['incentive_prop'] = incentive

            for lambda_val in lambda_levels:

                params['lambda_val'] = lambda_val

                for budget in budget_levels:

                    params['budget'] = budget

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