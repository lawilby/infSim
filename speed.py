import configparser
import sqlite3
import os
import db

directory_name = '/Users/laurawilby/dev/experiments_data/November/YouTube/Decay1/vary_budget_incentives'

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

db.add_benchmark_columns(conn)

benchmarks = [.10,.20,.30,.40,.50,.60,.70,.80,.90]

for benchmark in benchmarks:

    results_rows = conn.execute('''SELECT rowid FROM results;''')

    for row in results_rows:

        with open('{}/{}/simulation-details.csv'.format(directory_name,row['rowid']), 'r') as f:

            settings_config  = configparser.ConfigParser() 
            settings_config.read('{}/{}/settings.ini'.format(directory_name, row['rowid']))

            results_config   = configparser.ConfigParser()
            results_config.read('{}/{}/results.ini'.format(directory_name, row['rowid']))
            
            final_percentage = float(results_config['RESULTS']['percentage_influenced'])
            total_nodes      = results_config['RESULTS']['total_nodes']
            total_rounds     = float(results_config['RESULTS']['rounds'])
            print(total_rounds)

            cumulative_value = 0
            for line in f:

                data = line.split(',')
                cumulative_value = cumulative_value + 100*float(data[2].strip())/float(total_nodes)
                ratio_influenced = cumulative_value/final_percentage
                prop_done        = (float(data[0])+1)/total_rounds

                if ratio_influenced >= benchmark:

                    print(data[0])
                    print(prop_done)
                    values = (row['rowid'], benchmark, prop_done)
                    conn.execute('INSERT INTO benchmark VALUES (?,?,?);', values)
                    break

conn.commit()


