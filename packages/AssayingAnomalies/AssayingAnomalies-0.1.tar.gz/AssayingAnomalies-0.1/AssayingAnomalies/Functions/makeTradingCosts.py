import numpy as np
import pandas as pd
import os
from glob import glob
from datetime import datetime
from .makeGibbs import makeGibbs
from .makeCorwinSchultz import makeCorwinSchultz
from .makeAbdiRanaldi import makeAbdiRanaldi
from .makeKyleObizhaeva import makeKyleObizhaeva


def makeTradingCosts(params):
    # Timekeeping
    print(f"\nNow working on creating the transaction costs. Run started at {datetime.now()}\n")

    # Store the general and daily CRSP data path
    crsp_path = params.crspFolder + os.sep
    daily_path = params.daily_crsp_folder + os.sep

    # Store the tcost types
    # tcostsType = params.tcostsType
    tcostsType = 'full'

    # Check if correct tcosts input selected
    if tcostsType not in ['full', 'lf_combo', 'gibbs']:
        print(f"params.tcostsType is {tcostsType} but should be one of the folowing: \"full\", \"lf_combo\", \"gibbs\"")

    # Initialize dictionary to hold trading costs. CorwinSchultz = hl, AbdiRanaldi = chl, KyleObizhaeva = vov
    effSpreadStruct = {'gibbs': None,
                       'hl': None,
                       'chl': None,
                       'vov': None,
                       'hf_spreads': None
                       }

    "Check for Gibbs file"
    # Construct the file search pattern
    search_pattern = os.path.join(params.data_folder, '**', 'crspgibbs.csv')

    # Find all files matching the pattern
    gibbs_file_list = glob(search_pattern, recursive=True)  # recursive=True searches the subdirectories as well

    # Check if any files were found
    if not gibbs_file_list:
        raise FileNotFoundError('Gibbs input file does not exist. Gibbs trading cost estimate cannot be constructed.')
    else:
        file_path = gibbs_file_list[0]

    "Create Gibbs spreads"
    # path to file with Hasbrouck effective spread estimates
    effSpreadStruct['gibbs'] = makeGibbs(params, file_path)

    if tcostsType in ['lf_combo', 'full']:
        effSpreadStruct['hl'] = makeCorwinSchultz(params)
        effSpreadStruct['chl'] = makeAbdiRanaldi(params)
        effSpreadStruct['vov'] = makeKyleObizhaeva(params)

    if tcostsType == 'full':
        search_pattern = os.path.join(params.data_folder, '**', 'hf_monthly.csv')
        hf_file_list = glob(search_pattern, recursive=True)
        if not hf_file_list:
            raise FileNotFoundError('High-frequency trading cost input file does not exist. High-frequency trading '
                                    'cost estimate cannot be constructed.')
        else:
            file_path = hf_file_list[0]
        hf_spreaads = makeHighFreqEffSpreads(file_path)



