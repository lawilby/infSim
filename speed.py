import configparser
import sqlite3

directory_name = '/local-scratch/lw-data/aug29/enron/inc_0_1_budget_1_15'
benchmark = .8

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

# conn.execute('ALTER TABLE results ADD COLUMN benchmark INTEGER')

for i in range(1,33):

    with open('{}/{}/simulation-details.csv'.format(directory_name,i), 'r') as f:

        settings_config = configparser.ConfigParser() 
        settings_config.read('{}/{}/settings.ini'.format(directory_name, i))
        results_config = configparser.ConfigParser()
        results_config.read('{}/{}/results.ini'.format(directory_name, i))
        final_percentage = float(results_config['RESULTS']['percentage_influenced'])
        total_nodes = results_config['RESULTS']['total_nodes']

        cumulative_value = 0
        for line in f:

            data = line.split(',')
            cumulative_value = cumulative_value + 100*float(data[2].strip())/float(total_nodes)
            ratio_influenced = cumulative_value/final_percentage

            if ratio_influenced >= benchmark:

                query = 'UPDATE RESULTS SET benchmark={} WHERE rowid={}'.format(int(data[0]), i)
                conn.execute(query)
                conn.commit()
                break




