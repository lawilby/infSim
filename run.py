import os
import sqlite3
import configparser

# Local Imports #
from settings import make_settings_file
from execute import execute_simulation
from db import create_results_db

parent_directory = '/Users/laurawilby/dev/experiments_data/November/YouTube/Decay0/vary_budget_incentives'

results_conn = sqlite3.connect('{}/results.db'.format(parent_directory))
results_conn.row_factory = sqlite3.Row

create_results_db(results_conn)

params = dict()

threshold_levels      = [0.5]
lambda_levels         = [2]
incentive_levels      = [0,1,2,3]
decay                 = [1]
budget_levels         = [0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
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

stan_astroph            = {
                         'name'     : 'stan_astroph',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/astro.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/astro.txt'
                        }

stan_condmat            = {
                         'name'     : 'stan_condmat',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/condmat.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/condmat.txt'
                        }

stan_epinions            = {
                         'name'     : 'stan_epinions',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/epinions.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/epinions.txt'
                        }

stan_amazon            = {
                         'name'     : 'stan_amazon',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/amazon.txt',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/amazon.txt'
                        }

flights                = {
                         'name'     : 'flights',
                         'edges'    : '/Users/laurawilby/dev/experiments_data/flights.csv',
                         'nodes'    : '/Users/laurawilby/dev/experiments_data/flights.csv'
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