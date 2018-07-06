import os
import uuid
import datetime
import configparser

# local files
import settings
import create_db
import parse_asu
import run_sim


# TODO add some details of execution into settings file -- this will probably have to be later
config = configparser.ConfigParser()
config.read('settings.ini')

## Make a new directory
date = datetime.datetime.now()
directory_name = date.strftime("%d-%b-%Y:%H-%M-%S")

print(directory_name)

try:

    os.mkdir(directory_name)

except:

    raise
    # permissions, already exists etc. 

## Call settings.py to make the settings.ini file in the directory

settings.make_settings_file(directory_name) # TODO: probably want some sort of option of different ones to call for different paramaters ... or? edit file each time change?

#### TODO: need to pass in directory for settings file to each one so it is reading correct settings

## Create db

create_db.create_db()

## Parse -- eventually make this an option in settings.ini

parse_asu.parse_data()

## initiate_sim -- eventually could have different options for selecting target set or thresholds in settings.ini

initiate_sim.select_target_set_random()
initiate_sim.set_thresholds_proportional()

## run_sim -- need to allow for number of trials with same target set.

run_sim.run_sim()
