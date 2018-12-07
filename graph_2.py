import matplotlib.pyplot as plt
import configparser

directory_name = '/Users/laurawilby/dev/experiments_data/November/Astroph/Decay1/vary_budget_incentives'

for i in [11,22,33,44]:

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
        
        label = '{}'.format(settings_config['PARAMS']['incentive_prop'])
        plt.plot(x, y, '.', label=label)
    

plt.legend()
plt.xlabel('Round')
plt.ylabel('Percentage Influenced')
plt.title('Budget 0.50, Effect of Incentives')
plt.axis([-1, 15, -1, 80])
plt.savefig('{}/percentages_influenced_budget_50.png'.format(directory_name))
plt.cla()
plt.clf()
