import pandas as pd
import os
import glob
import numpy as np
from datetime import datetime

def makeCRSPDailyData(params):

    # Timekeeping
    print(f"\nNow working on making CRSP daily data. Run started at {datetime.now()}.\n")

    # Store the daily CRSP data path
    daily_crsp_path = params.daily_crsp_folder + os.sep

    # Get the file names and number of files in the daily CRSP directory
    files = os.listdir(daily_crsp_path)

    # Store the daily CRSP directory contents and number of files
    daily_crsp_files = glob.glob(os.path.join(daily_crsp_path, 'crsp_dsf*.csv'))

    # Initiate the crsp_dsf DataFrame
    crsp_dsf = pd.DataFrame()

    # Loop through the files
    for file in daily_crsp_files:
        temp_dsf = pd.read_csv(file, index_col=0)
        crsp_dsf = pd.concat([crsp_dsf, temp_dsf], ignore_index=True)

    #change permno datatype to int
    crsp_dsf['permno'] = crsp_dsf['permno'].astype(int)

    # Keep only the relevant permnos
    permno = pd.read_csv(params.crspFolder + os.sep + 'permno.csv', index_col=0).astype(int)  # Assuming permno is in a CSV file
    idx_to_keep = crsp_dsf['permno'].isin(permno.values)
    crsp_dsf = crsp_dsf[idx_to_keep]

    # Create ddates in YYYYMMDD format
    crsp_dsf['dates'] = pd.to_datetime(crsp_dsf['date'])
    crsp_dsf['dates'] = crsp_dsf['dates'].dt.strftime('%Y%m%d').astype(int)
    ddates = crsp_dsf['dates'].unique()

    crsp_dsf = crsp_dsf.add_prefix('d')

    # change the name of a couple of columns
    crsp_dsf.rename(columns={'dret': 'dret_x_adj', 'dvol': 'dvol_x_adj'}, inplace=True)

    # create list of variables to make
    varNames_crsp_dsf = [col for col in crsp_dsf.columns if col not in ['ddates', 'ddate', 'dpermno']]


    "Create dataframes of single varNames"
    for i in varNames_crsp_dsf:
        print(i)
        temptable = pd.pivot_table(crsp_dsf, index='ddates', columns='dpermno', values=i)
        # temptable = pd.pivot(crsp_msf, index='dates', columns='permno', values=i)
        temptable.to_csv(daily_crsp_path + i + '.csv')

    # Create the end of month flag and store ddates
    yyyy_mm = np.floor(ddates / 100).astype(int)
    eomflag = yyyy_mm != np.roll(yyyy_mm, -1)
    eomflag[-1] = True

    ddates_csv = pd.DataFrame(ddates)
    ddates_csv.to_csv(daily_crsp_path + 'ddates.csv')

    eomflag_csv = pd.DataFrame(eomflag)
    eomflag_csv.to_csv(daily_crsp_path + 'eomflag.csv')


    print(f"Data assignment completed at {datetime.now()}.\n")


# makeCRSPDailyData(params)