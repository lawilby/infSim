import os
import uuid
import datetime

import executeSim

for val in range(10):

    ## Make a new directory
    date = datetime.datetime.now()
    directory_name = 'vary-thresh-prop/' + date.strftime("%d-%b-%Y:%H-%M-%S")

    try:

        os.mkdir(directory_name)

    except:

        raise
        # permissions, already exists etc.

    executeSim.executeSim(directory_name, 3, 100, float(val+1)/10)