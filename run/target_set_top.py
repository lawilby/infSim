import os
import uuid
import datetime

import executeSim

for val in [500, 1000, 5000, 10000, 50000, 150000, 500000]:

    ## Make a new directory
    date = datetime.datetime.now()
    directory_name = '/local-scratch/lw-data/target-set-top/' + date.strftime("%d-%b-%Y:%H-%M-%S")

    try:

        os.mkdir(directory_name)

    except:

        raise
        # permissions, already exists etc.

    executeSim.executeSim_target_high_thresh(directory_name, 3, val, .5)