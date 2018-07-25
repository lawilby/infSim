import os
import uuid
import datetime

import executeSim

for val in range(10):

    ## Make a new directory
    date = datetime.datetime.now()
    directory_name = '/Users/laurawilby/dev/experiments_data/vary-lambda-partial/youTube/prop-5/target-150k/inc-2/' + date.strftime("%d-%b-%Y:%H-%M-%S")

    try:

        os.mkdir(directory_name)

    except:

        raise
        # permissions, already exists etc.

    executeSim.executeSim_Partial_Incentives(directory_name, val + 1, 150000, .5, .6)