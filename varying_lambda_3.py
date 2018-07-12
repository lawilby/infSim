import os
import uuid
import datetime

import executeSim

for val in range(10):

    ## Make a new directory
    date = datetime.datetime.now()
    directory_name = 'vary-lambda-3/' + date.strftime("%d-%b-%Y:%H-%M-%S")

    try:

        os.mkdir(directory_name)

    except:

        raise
        # permissions, already exists etc.

    executeSim.executeSim(directory_name, val + 1, 100, .2)