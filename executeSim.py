import time

# local files
import settings
import create_db
import parse_asu
import run_sim
import initiate_sim
import results
# import plots

def executeSim(directory_name, lambda_val, target_set_size, thresh_prop):

    start_time = time.time()
    print("START")

    ## Call settings.py to make the settings.ini file in the directory

    settings.make_settings_file(directory_name, lambda_val, target_set_size, thresh_prop)

    ## Create db

    create_db.create_db(directory_name)

    ## Parse -- eventually make this an option in settings.ini

    parse_asu.parse_data(directory_name)

    ## initiate_sim -- eventually could have different options for selecting target set or thresholds in settings.ini

    initiate_sim.select_target_set_random(directory_name)
    initiate_sim.set_thresholds_proportional(directory_name)

    ## run_sim -- need to allow for number of trials with same target set.

    run_sim.run_sim(directory_name)

    ## display results

    results.display_results(directory_name)

    # plots.results_plot(directory_name)

    print('END ' + str(round(time.time() - start_time, 2)))

def executeSim_target_high_thresh(directory_name, lambda_val, target_set_size, thresh_prop):

    start_time = time.time()
    print("START")

    ## Call settings.py to make the settings.ini file in the directory

    settings.make_settings_file(directory_name, lambda_val, target_set_size, thresh_prop)

    ## Create db

    create_db.create_db(directory_name)

    ## Parse -- eventually make this an option in settings.ini

    parse_asu.parse_data(directory_name)

    ## initiate_sim -- eventually could have different options for selecting target set or thresholds in settings.ini

    initiate_sim.set_thresholds_proportional(directory_name)
    initiate_sim.select_target_set_top(directory_name)

    ## run_sim -- need to allow for number of trials with same target set.

    run_sim.run_sim(directory_name)

    ## display results

    results.display_results(directory_name)

    print('END ' + str(round(time.time() - start_time, 2)))

def executeSim_target_low_thresh(directory_name, lambda_val, target_set_size, thresh_prop):

    start_time = time.time()
    print("START")

    ## Call settings.py to make the settings.ini file in the directory

    settings.make_settings_file(directory_name, lambda_val, target_set_size, thresh_prop)

    ## Create db

    create_db.create_db(directory_name)

    ## Parse -- eventually make this an option in settings.ini

    parse_asu.parse_data(directory_name)

    ## initiate_sim -- eventually could have different options for selecting target set or thresholds in settings.ini

    initiate_sim.set_thresholds_proportional(directory_name)
    initiate_sim.select_target_set_bottom(directory_name)

    ## run_sim -- need to allow for number of trials with same target set.

    run_sim.run_sim(directory_name)

    ## display results

    results.display_results(directory_name)

    print('END ' + str(round(time.time() - start_time, 2)))
