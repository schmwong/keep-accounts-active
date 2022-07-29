# pip install pandas
"""
# This script is meant to be run after cloning the relevant folder
# from the private repo that holds the log files

# Run following bash commands before calling this module:
git clone \
--depth 1 \
--filter=blob:none \
--sparse \
https://$WORKFLOW_TOKEN@github.com/schmwong/login-log \
;
cd login-log
git sparse-checkout init --cone
git sparse-checkout set <folder name>
cd ..

"""

import sys

sys.dont_write_bytecode = True

import os
import shutil
import pandas as pd


def update_logs(instance):
    instance.logger.removeHandler(instance.DuoHandler)
    filename = instance.filename
    filepath = f"./login-log/{filename.split()[1].split('_')[0]}/{filename}"  # ./<folder name>/<filename>

    if os.path.exists(filename):
        if os.path.exists(filepath):
            df_old = pd.read_csv(filepath, index_col=False)
            df_update = pd.read_csv(filename, index_col=False)
            df_new = pd.concat([df_old, df_update])
            df_new.drop_duplicates(inplace=True)
            df_new.to_csv(filepath, index=False)
            os.remove(filename)  # Delete the update file after successful concat
        else:
            shutil.move(filename, filepath)
    else:
        print("New logs do not exist.")
