import os
import sqlite3
import configparser

# Local Imports #
from settings import make_settings_file
from execute import execute_simulation
from db import create_results_db

parent_directory = '/local-scratch/lw-data/aug29/youtube/inc_0_1_budget_15_25_decay_1'

results_conn = sqlite3.connect('{}/results.db'.format(parent_directory))
results_conn.row_factory = sqlite3.Row

create_results_db(results_conn)

params = dict()

threshold_levels      = [0.5,0.6]
lambda_levels         = [2,3]
incentive_levels      = [0,1]
decay                 = [1]
budget_levels         = [.15,.25]
stan_youtube          = {
                         'name'     : 'stan_youtube',
                         'edges'    : '/local-scratch/lw-data/youtube.txt',
                         'nodes'    : '/local-scratch/lw-data/youtube.txt'
                        }

stan_enron            = {
                         'name'     : 'stan_enron',
                         'edges'    : '/local-scratch/lw-data/enron.txt',
                         'nodes'    : '/local-scratch/lw-data/enron.txt'
                        }

stan_astroph            = {
                         'name'     : 'stan_astroph',
                         'edges'    : '/local-scratch/lw-data/astroph.txt',
                         'nodes'    : '/local-scratch/lw-data/astroph.txt'
                        }

stan_epinions            = {
                         'name'     : 'stan_epinions',
                         'edges'    : '/local-scratch/lw-data/epinions.txt',
                         'nodes'    : '/local-scratch/lw-data/epinions.txt'
                        }

stan_amazon            = {
                         'name'     : 'stan_amazon',
                         'edges'    : '/local-scratch/lw-data/amazon.txt',
                         'nodes'    : '/local-scratch/lw-data/amazon.txt'
                        }

datasets              = [stan_youtube]

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
                        print(parent_directory)
                        make_settings_file(directory_name, parent_directory, params)
                        execute_simulation(directory_name, results_conn)
                        experiment += 1

results_conn.close()