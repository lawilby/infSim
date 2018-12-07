import matplotlib.pyplot as plt
import configparser

directory_name = '/Users/laurawilby/dev/experiments_data/aug29/youtube/inc_0_1_budget_1_15_decay_1'

for i in range(1,65):

    with open('{}/{}/simulation-details.csv'.format(directory_name,i), 'r') as f:

        x = list()
        y = list()

        settings_config = configparser.ConfigParser() 
        settings_config.read('{}/{}/settings.ini'.format(directory_name, i))
        results_config = configparser.ConfigParser()
        results_config.read('{}/{}/results.ini'.format(directory_name, i))
        total_nodes = results_config['RESULTS']['total_nodes']

        cumulative_value = 0
        for line in f:

            data = line.split(',')
            x.append(int(data[0]))
            cumulative_value = cumulative_value + 100*float(data[2].strip())/float(total_nodes)
            y.append(cumulative_value)
        

        plt.plot(x, y, '.')
        plt.xlabel('Round')
        plt.ylabel('Percentage Influenced')
        plt.title('{} {}/{}/{}/{}/{}'.format(settings_config['FILES']['dataset'],
                                             settings_config['PARAMS']['thresh_prop'],
                                             settings_config['PARAMS']['lambda_val'],
                                             settings_config['PARAMS']['incentive_prop'],
                                             settings_config['PARAMS']['decay'],
                                             settings_config['PARAMS']['budget']))
        plt.axis([-1, 21, -5, 100])
        plt.savefig('{}/{}/percentages_influenced.png'.format(directory_name, i))
        plt.cla()
        plt.clf()

