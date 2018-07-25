import os

import thresholds_inf
import thresholds_target_set

directory_name = '/local-scratch/lw-data/vary-lambda/youTube'

level_one_folders = os.listdir(directory_name)

print(level_one_folders)

for folder_level_one in level_one_folders:

    level_two_folders = os.listdir('{}/{}'.format(directory_name, folder_level_one))
    print(level_two_folders)

    for folder_level_two in level_two_folders:

        try:

            thresholds_inf.hist_all_influenced('{}/{}/{}'.format(directory_name, folder_level_one, folder_level_two))
            thresholds_target_set.hist_target_set('{}/{}/{}'.format(directory_name, folder_level_one, folder_level_two))

        except:

            continue