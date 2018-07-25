import matplotlib.pyplot as plt
import configparser
import sqlite3
import os


directory_name = '/Users/laurawilby/dev/experiments_data/vary-lambda-partial/youTube/prop-5/target-150k/inc-2'

results_folders = os.listdir(directory_name)

print(results_folders)

percentages = list()
lambda_vals = list()

for folder in results_folders:

    try:

        results_config = configparser.ConfigParser()
        results_config.read(directory_name + '/' + folder + '/results.ini')
        settings_config = configparser.ConfigParser()
        settings_config.read(directory_name + '/' + folder + '/settings.ini')
        print(results_config['RESULTS']['percentage_influenced'])
        percentages.append(float(results_config['RESULTS']['percentage_influenced']))
        lambda_vals.append(float(settings_config['PARAMS']['lambda_val']))

    except:

        continue

print(percentages)
plt.plot(percentages, lambda_vals, 'ro')
plt.xlabel('Percentage Influenced')
plt.ylabel('Time Window')
plt.title('Target Size: 150k  Partial Incentive: .2  Threshold Proportion: .5')
plt.axis([0, 100, 0, 11])
plt.savefig('{}/percentages_influenced.png'.format(directory_name))
plt.cla()
plt.clf()