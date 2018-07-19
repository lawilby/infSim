import matplotlib.pyplot as plt
import configparser
import sqlite3
import os


directory_name = '/local-scratch/lw-data/vary-lambda/youTube/prop-5'

results_folders = os.listdir(directory_name)

print(results_folders)

percentages = list()
lambda_vals = list()

for folder in results_folders:

    results_config = configparser.ConfigParser()
    results_config.read(directory_name + '/' + folder + '/results.ini')
    settings_config = configparser.ConfigParser()
    settings_config.read(directory_name + '/' + folder + '/settings.ini')
    print(results_config['RESULTS']['percentage_influenced'])
    percentages.append(float(results_config['RESULTS']['percentage_influenced']))
    lambda_vals.append(float(settings_config['PARAMS']['lambda_val']))

plt.plot(lambda_vals, percentages, 'ro')
plt.savefig(directory_name + '/percentages_influenced.png')