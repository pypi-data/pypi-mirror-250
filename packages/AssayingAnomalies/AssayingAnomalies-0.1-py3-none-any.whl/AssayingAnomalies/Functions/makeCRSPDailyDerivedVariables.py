import numpy as np
import pandas as pd
from datetime import datetime
import os
import statsmodels.api as sm
from multiprocessing import Pool
from .getFFDailyFactors import getFFDailyFactors


def parallel_compute_ivol(i, j, col_index, ind1, ind3, dret, dmkt, dff3):
    # Regression for 1-month residual
    X = sm.add_constant(dmkt[ind1])  # Add a constant term
    y = dret.loc[ind1, j]
    model = sm.OLS(y.values, X.values, missing='drop')
    results = model.fit()
    ivol = np.sqrt(np.mean(results.resid ** 2))

    # Regression for FF3 1-month residual
    X_ff3 = dff3.loc[ind1]
    y = dret.loc[ind1, j]
    model_ff3 = sm.OLS(y.values, X_ff3.values, missing='drop')
    results_ff3 = model_ff3.fit()
    iffvol = np.sqrt(np.mean(results_ff3.resid ** 2))

    # Regression for 3-month residual
    X = sm.add_constant(dmkt[ind3])  # Add a constant term
    y = dret.loc[ind3, j]
    model = sm.OLS(y.values, X.values, missing='drop')
    results = model.fit()
    ivol3 = np.sqrt(np.mean(results.resid ** 2))

    # Regression for FF3 3-month residual
    X_ff3 = dff3.loc[ind3]
    y = dret.loc[ind3, j]
    model_ff3 = sm.OLS(y.values, X_ff3.values, missing='drop')
    results_ff3 = model_ff3.fit()
    iffvol3 = np.sqrt(np.mean(results_ff3.resid ** 2))

    return i, col_index, ivol, iffvol, ivol3, iffvol3


def makeCRSPDailyDerivedVariables(params):
    # Timekeeping
    print(f"\nNow working on making CRSP daily derived variables. Run started at {datetime.now()}.\n")

    # set the path to crsp daily folder
    crsp_folder = params.crspFolder + os.sep

    # set the path to crsp daily folder
    daily_crsp_folder = params.daily_crsp_folder + os.sep

    # set the path to ff data folder
    ff_data_folder = params.ff_data_folder + os.sep

    "Make market capitalization"
    dprc = pd.read_csv(daily_crsp_folder + 'dprc.csv', index_col=0)
    dshrout = pd.read_csv(daily_crsp_folder + 'dshrout.csv', index_col=0)
    dme = np.abs(dprc) * dshrout / 1000

    # replace zeros with nan
    dme.replace(0, np.nan, inplace=True)
    dme.to_csv(daily_crsp_folder + 'dme.csv')

    "Load the necessary data from storage"
    dret_x_dl = pd.read_csv(daily_crsp_folder + 'dret_x_adj.csv', index_col=0)
    permno = pd.read_csv(crsp_folder + 'permno.csv', index_col=0)
    ddates = pd.read_csv(daily_crsp_folder + 'ddates.csv', index_col=0)
    crsp_dsedelist = pd.read_csv(daily_crsp_folder + 'crsp_dsedelist.csv', index_col=0)

    "get permnos to drop"
    #get the indices of the permnos in crsp_msedelist.permno  that are NOT in permno
    mask = np.isin(crsp_dsedelist.permno, permno, invert=True)
    # get the permnos to remove
    toDrop = crsp_dsedelist.permno[mask]

    "drop these permnos from crsp_dsedelist dataframe"
    crsp_dsedelist = crsp_dsedelist.set_index('permno')
    crsp_dsedelist = crsp_dsedelist.drop(toDrop)
    #changing permnos back to a column instead of index
    crsp_dsedelist.reset_index(inplace=True)

    " Turn the date into YYYYMMDD format"
    crsp_dsedelist['dlstdt'] = pd.to_datetime(crsp_dsedelist['dlstdt'])
    crsp_dsedelist['dlstdt'] = crsp_dsedelist['dlstdt'].dt.strftime('%Y%m%d')
    # change from string to integer
    crsp_dsedelist['dlstdt'] = crsp_dsedelist['dlstdt'].astype(int)

    "fill in the delisting returns"
    dret = dret_x_dl.copy()
    for i in range(len(crsp_dsedelist)):
    # for i in range(500):
        "find the index in permno of ith permno in the delist dataframe"
        c = np.where(permno == crsp_dsedelist.permno[i])[0][0]
        # print(c)
        "find the index in dates that corresponds to the delisting date of the ith permno"
        r_dt_ar = np.where(ddates == crsp_dsedelist.dlstdt[i])[0]
        if r_dt_ar.size == 0:
            continue
        else:
            r_dt = r_dt_ar[0]
        # print(r_dt)
        "returns a series of row numbers in ret dataframe where the delisted permno has finite returns"
        r_last_array = np.where(np.isfinite(dret.iloc[:, c]) == True)[0]
        "check to see of the array is empty, and if it is, skip to the next iteration of the loop"
        if r_last_array.size == 0:
            continue
        else:
            "selects the last index, i.e., the row number of the final finite return for delisted permno"
            r_last = r_last_array[-1] + 1
            # print(r_last)
        if np.isfinite(dret.iloc[r_dt, c]):
            if r_last < len(ddates):
                "assigns the delisting return to the position following the last finite return"
                dret.iloc[(r_last), c] = crsp_dsedelist.dlret[i]
        else:
            dret.iloc[r_dt, c] = crsp_dsedelist.dlret[i]
    #
    # c = np.where(permno == 11754)[0][0]
    # r = np.where(ddates == 201201)[0][0]
    # kodak_delist_ret = ret.iloc[r, c]
    # print(f'Adjusting for delisting complete. Kodak\'s delisting return was {kodak_delist_ret:.4f}')

    "Save the returns dataframe"
    dret.to_csv(daily_crsp_folder + 'dret.csv')

    "Adjust NASDAQ volume following Gao and Ritter (2010). See their Appendix B for more details"
    # load additional objects
    dvol_x_adj = pd.read_csv(daily_crsp_folder + 'dvol_x_adj.csv', index_col=0)
    exchcd = pd.read_csv(crsp_folder + 'exchcd.csv', index_col=0)
    dvol = dvol_x_adj.copy()

    # :TODO:Note: the matlab code does not load in the EOM flag (probably because it is still in memory from the prev
    #  function call but I have to re-load it in python and declare the datatype to be a boolean array.
    eomflag = pd.read_csv(daily_crsp_folder + 'eomflag.csv', index_col=0).iloc[:, 0].astype(bool)

    "To adjust the volume, we first need to create the daily exchange code matrix"
    # Initialize daily exchange code:
    n_days, n_stocks = dvol_x_adj.shape
    dexchcd = np.full((n_days, n_stocks), np.nan)
    dexchcd[eomflag, :] = exchcd

    # Iterate over the eomflag to fill in the daily exchange code matrix
    eom_indices = np.where(eomflag)[0]

    # Fill in the initial part of the dexchcd before the first end-of-month flag
    if len(eom_indices) > 0:
        first_eom_index = eom_indices[0]
        dexchcd[:first_eom_index, :] = np.tile(exchcd.iloc[0, :], (first_eom_index, 1))

    # Fill in the rest of the daily exchange code matrix
    for i in range(len(eom_indices) - 1):
        start_index = eom_indices[i]
        end_index = eom_indices[i + 1]
        dexchcd[start_index:end_index, :] = np.tile(exchcd.iloc[i, :], (end_index - start_index, 1))

    # Now turn into a pandas dataframe and store it for future use
    dexchcd = pd.DataFrame(dexchcd)
    dexchcd.index = ddates.values.flatten()
    dexchcd.columns = permno.values.flatten()
    dexchcd.to_csv(daily_crsp_folder + 'dexchcd.csv')

    "Requires too much memory to do entire dataframe at once. Will try and go row by row"
    # Divide by 2 prior to Feb 2001
    for i in range(len(dexchcd.columns)):
    # for i in range(10):
    #     print(vol.index[i])
        # Since iterating over columns, I only need the row numbers where both conditions are satisfied for a particular column
        rows = np.where((dexchcd.iloc[:, i]==3) & (dexchcd.index < 20010201))[0]
        dvol.iloc[rows, i] = dvol.iloc[rows, i]/2

    # Divide by 1.8 for most of 2001
    for i in range(len(dexchcd.columns)):
    # for i in range(10):
    #     print(vol.index[i])
        # Since iterating over columns, I only need the row numbers where both conditions are satisfied for a particular column
        rows = np.where((dexchcd.iloc[:, i]==3) & (dexchcd.index >= 20010201) & (dexchcd.index < 20020101))[0]
        dvol.iloc[rows, i] = dvol.iloc[rows, i]/1.8

    # Divide by 1.6 for 2002 and 2003
    for i in range(len(dexchcd.columns)):
    # for i in range(10):
    #     print(vol.index[i])
        # Since iterating over columns, I only need the row numbers where both conditions are satisfied for a particular column
        rows = np.where((dexchcd.iloc[:, i]==3) & (dexchcd.index >= 20020101) & (dexchcd.index < 20040101))[0]
        dvol.iloc[rows, i] = dvol.iloc[rows, i]/1.6

    dvol.to_csv(daily_crsp_folder + 'dvol.csv')

    "Download, clean up, and save the Fama-French factors from Ken French's website"
    getFFDailyFactors(params=params)

    "Make Amihud values"
    # first 12 month rolling amihud values

    # load the monthly returns, monthly price, and monthly dates, matrices
    ret = pd.read_csv(crsp_folder + 'ret.csv', index_col=0).astype(float)
    prc = pd.read_csv(crsp_folder + 'prc.csv', index_col=0).astype(float)
    dates = pd.read_csv(crsp_folder + 'dates.csv', index_col=0).astype(int)

    # make sure ddates datatype is int
    ddates = ddates.astype(int)

    # initialize amihud matrix
    amihud = np.full_like(ret, np.nan)

    # replace zero-volume observations with nan and calculate dollar volume
    dollar_volume = np.abs(dprc) * np.abs(dvol)
    zeroVolInd = (dvol == 0)
    dollar_volume[zeroVolInd] = np.nan

    # calculate the daily price impact
    priceImpact = np.abs(dret) / dollar_volume

    # Take the absolute value of the monthly price and store the number of months
    prc = np.abs(prc)
    nmonths = len(ret.index)

    # Calculate amihud
    for i in range(11, nmonths):
        # Find the days in the last year
        start_date = dates.iloc[i - 11]
        end_date = dates.iloc[i]
        index_year = ((ddates // 100 >= start_date) & (ddates // 100 <= end_date))

        # Ensure index_year is a 1D boolean array
        index_year = index_year.values.flatten()

        # Store monthly price impact for last year
        last_yr_pi = priceImpact[index_year].copy()

        # Apply the filters (200 obs & price > $5)
        idx_to_drop = np.isfinite(last_yr_pi).sum(axis=0) < 200
        idx_to_drop |= prc.iloc[i, :].values.flatten() <= 5
        last_yr_pi.iloc[:, idx_to_drop] = np.nan

        # Calculate the mean price impact for the last year, ignoring NaN values
        amihud[i, :] = np.nanmean(last_yr_pi, axis=0)

    amihud = pd.DataFrame(amihud)
    amihud.index = dates.values.flatten()
    amihud.columns = permno.values.flatten()
    amihud.to_csv(crsp_folder + 'amihud.csv')

    "Make other measures from the daily data"
    # Realized volatilities

    # Initialize the matrices
    n_months, n_stocks = ret.shape
    RVOL_matrices = {period: np.full((n_months, n_stocks), np.nan) for period in [1, 3, 6, 12, 36, 60]}
    dshvol = np.full_like(ret, np.nan)
    dshvolM = np.full_like(ret, np.nan)
    dretmax = np.full_like(ret, np.nan)
    dretmin = np.full_like(ret, np.nan)

    # First turn the dates and ddates dataframes into arrays
    ddates_array = ddates.values.flatten()
    dates_array = dates.values.flatten()

    # Find the first month index
    first_month_date = ddates_array[0] // 100
    if first_month_date in dates_array:
        first_month = np.where(dates_array == first_month_date)[0][0]
    else:
        raise ValueError("First month date not found in dates array")

    # Monthly loop range
    last_month = len(dates)

    # Calculate measures
    for i in range(first_month, last_month):
        for period, RVOL in RVOL_matrices.items():
            start_index = max(i - period + 1, 0)
            ind = (ddates_array // 100 >= dates_array[start_index]) & (ddates_array // 100 <= dates_array[i])

            # Ensure ind is a 1D boolean array and matches the number of rows in dret
            ind = ind.flatten()

            # Apply the indexing to the DataFrame
            selected_dret = dret.loc[ind, :]

            RVOL[i, :] = np.nanstd(selected_dret, axis=0)

        ind1 = (ddates_array // 100 == dates_array[i])

        # Ensure ind1 is a 1D boolean array and matches the number of rows in dvol
        ind1 = ind1.flatten()

        # Apply the indexing to the DataFrame
        selected_dvol = dvol.loc[ind1, :]

        dshvol[i, :] = np.nansum(selected_dvol, axis=0)
        dshvolM[i, :] = np.nanmax(selected_dvol, axis=0)
        dretmax[i, :] = np.nanmax(selected_dvol, axis=0)
        dretmin[i, :] = np.nanmin(selected_dvol, axis=0)

    # Save the matrices
    for period, RVOL_matrix in RVOL_matrices.items():
        filename = f'RVOL{period}.csv'
        RVOL_matrix = pd.DataFrame(RVOL_matrix)
        RVOL_matrix.to_csv(crsp_folder + filename)

    dshvol = pd.DataFrame(dshvol)
    dshvol.to_csv(crsp_folder + 'dshvol.csv')
    dshvolM = pd.DataFrame(dshvolM)
    dshvolM.to_csv(crsp_folder + 'dshvolM.csv')
    dretmax = pd.DataFrame(dretmax)
    dshvol.to_csv(crsp_folder + 'dretmax.csv')
    dretmin = pd.DataFrame(dretmin)
    dretmin.to_csv(crsp_folder + 'dretmin.csv')

    "Make IVOLs"
    # Load the FF factors
    dff = pd.read_csv(ff_data_folder + 'dff.csv', index_col=0).astype(float)
    dff3 = pd.read_csv(ff_data_folder + 'dff3.csv', index_col=0).astype(float)
    dff3.index = dff3['dates']
    dff3.drop(columns=['dates'], inplace=True)
    dmkt = dff['mkt'].copy()

    # Create the daily excess returns above Rf
    drf = dff['rf'].to_numpy()
    rf_mat = np.tile(drf, (len(ret.columns), 1)).T
    dxret = dret - rf_mat

    # Initialize the IVOL variables
    ivol = np.full_like(ret, np.nan)
    ivol3 = np.full_like(ret, np.nan)
    iffvol = np.full_like(ret, np.nan)
    iffvol3 = np.full_like(ret, np.nan)

    if params.remote_or_not:
        # Prepare a list of arguments for parallel processing
        arguments = []
        for i in range(first_month, last_month):
            ind1 = ((ddates.values.flatten() // 100) == dates.iloc[i, 0])
            ind3 = ((ddates.values.flatten() // 100) >= dates.iloc[max(i - 2, 0), 0]) & (
                        (ddates.values.flatten() // 100) <= dates.iloc[i, 0])
            hor_ind = dxret.iloc[ind1, :].apply(lambda x: np.isfinite(x).sum(), axis=0) > 0
            for j in hor_ind[hor_ind].index:
                col_index = dret.columns.get_loc(j)
                arguments.append((i, j, col_index, ind1, ind3, dret, dmkt, dff3))

        # Run the computation in parallel
        with Pool(processes=params.num_cpus) as pool:  # Adjust number of processes based on your machine
            results = pool.starmap(parallel_compute_ivol, arguments)

        # Unpack results and populate the matrices
        for res in results:
            i, col_index, ivol_val, iffvol_val, ivol3_val, iffvol3_val = res
            ivol[i, col_index] = ivol_val
            iffvol[i, col_index] = iffvol_val
            ivol3[i, col_index] = ivol3_val
            iffvol3[i, col_index] = iffvol3_val

    else:
        # Monthly loop range
        first_month_date = ddates.iloc[0, 0] // 100
        first_month = np.where(dates.values.flatten() == first_month_date)[0][0]
        last_month = len(dates)

        # Calculate IVOLs
        for i in range(first_month, last_month):
            # Find the 1- and 3-month daily indices
            ind1 = ((ddates.values.flatten() // 100) == dates.iloc[i, 0])
            ind3 = ((ddates.values.flatten() // 100) >= dates.iloc[max(i - 2, 0), 0]) & (
                        (ddates.values.flatten() // 100) <= dates.iloc[i, 0])

            # Stocks which we need to loop through
            hor_ind = dxret.iloc[ind1, :].apply(lambda x: np.isfinite(x).sum(), axis=0) > 0

            for j in hor_ind[hor_ind].index:
                # Get the integer index for the column
                col_index = dret.columns.get_loc(j)

                # Regression for 1-month residual
                X = sm.add_constant(dmkt[ind1])  # Add a constant term
                y = dret.loc[ind1, j]
                model = sm.OLS(y.values, X.values, missing='drop')
                results = model.fit()
                ivol[i, col_index] = np.sqrt(np.mean(results.resid ** 2))

                # Regression for FF3 1-month residual
                X_ff3 = dff3.loc[ind1]
                y = dret.loc[ind1, j]
                model_ff3 = sm.OLS(y.values, X_ff3.values, missing='drop')
                results_ff3 = model_ff3.fit()
                iffvol[i, col_index] = np.sqrt(np.mean(results_ff3.resid ** 2))

                # Regression for 3-month residual
                X = sm.add_constant(dmkt[ind3])  # Add a constant term
                y = dret.loc[ind3, j]
                model = sm.OLS(y.values, X.values, missing='drop')
                results = model.fit()
                ivol3[i, col_index] = np.sqrt(np.mean(results.resid ** 2))

                # Regression for FF3 3-month residual
                X_ff3 = dff3.loc[ind3]
                y = dret.loc[ind3, j]
                model_ff3 = sm.OLS(y.values, X_ff3.values, missing='drop')
                results_ff3 = model_ff3.fit()
                iffvol3[i, col_index] = np.sqrt(np.mean(results_ff3.resid ** 2))

    # Save the IVOLs as CSV files
    ivol = pd.DataFrame(ivol)
    ivol.to_csv(crsp_folder + 'IVOL.csv')
    iffvol = pd.DataFrame(iffvol)
    iffvol.to_csv(crsp_folder + 'IffVOL.csv')
    ivol3 = pd.DataFrame(ivol3)
    ivol3.to_csv(crsp_folder + 'IVOL3.csv')
    iffvol3 = pd.DataFrame(iffvol3)
    iffvol3.to_csv(crsp_folder + 'IffVOL3.csv')

    "Make CAR3s: Inilialize the CAR3 matrix, calculate abnormal returns, iterate through each month to compute the" \
    "CAR3 value for each stock at each announcement date"
    # load additional variables
    rdq = pd.read_csv(params.compFolder + os.sep + 'RDQ.csv', index_col=0)
    fqtr = pd.read_csv(params.compFolder + os.sep + 'FQTR.csv', index_col=0)
    nyse = pd.read_csv(params.crspFolder + os.sep + 'NYSE.csv', index_col=0)
    me = pd.read_csv(params.crspFolder + os.sep + 'me.csv', index_col=0)

    # For some reason RDQ and FQTR has an additional row at the beginning of the matrix. It doesn't correspond to any
    # date so I will check if this is the case and remove it.
    if pd.isna(rdq.index[0]):
        rdq = rdq.iloc[1:, :]

    if pd.isna(fqtr.index[0]):
        fqtr = fqtr.iloc[1:, :]

    # Only leave the announcement dates
    rdq = rdq.where(~fqtr.isna(), np.nan)

    # Initialize the CAR3 matrix
    n_stocks = dret.shape[1]
    CAR3 = np.full_like(rdq, np.nan)

    # Calculate the abnormal return (in excess of the market); (ret_{i,t} - ret_{mkt,t})
    rptdMkt_values = (1 + dmkt + drf).values
    rptdMkt = np.tile(rptdMkt_values, (len(me.columns), 1)).T
    dxret = 1 + dret - rptdMkt

    # Monthly loop range
    first_month = np.where(rdq.notna().sum(axis=1) > 0)[0][0]
    last_month = len(dates)

    # Loop over the months
    for i in range(first_month, last_month):
        # Find all the announcements in the current month
        idx_announcements = np.where(rdq.iloc[i, :].notna())[0]

        # Loop over the announcements
        for c in idx_announcements:
            permno = rdq.columns[c]  # Get the permno (column label) from rdq

            # Check if the permno is in the columns of dxret
            if permno in dxret.columns:
                dxret_col_index = dxret.columns.get_loc(permno)  # Find the corresponding column in dxret

                # Get the announcement date and find the corresponding row in ddates
                announcement_date = rdq.iloc[i, c]
                r = np.where(ddates == announcement_date)[0]

                # Calculate the CAR3 if we found a match
                if r.size > 0 and r[0] < len(ddates) - 1:
                    CAR3[i, c] = np.prod(dxret.iloc[r[0] - 1:r[0] + 2, dxret_col_index]) - 1


    # Fill the observations between quarters; Matlab uses a helper function, but this isn't necessary in Python
    CAR3 = pd.DataFrame(CAR3).ffill(axis=0)

    # Change the columns names to be integers
    ret.columns = [int(float(col)) for col in ret.columns]
    CAR3.columns = [int(float(col)) for col in rdq.columns]

    # Identify common columns between 'ret' and 'CAR3'
    common_columns = ret.columns.intersection(CAR3.columns)

    # Initialize a mask with False for all entries in CAR3
    idx_to_drop = pd.DataFrame(False, index=ret.index, columns=CAR3.columns)

    # Update the mask for common columns based on NaN values in 'ret'
    idx_to_drop.loc[:, common_columns] = ret[common_columns].isna()

    # Remove all observations where ret is nan
    CAR3[idx_to_drop] = np.nan

    # Save
    CAR3.to_csv(crsp_folder + 'CAR3.csv')

    "Timekeeping"
    print(f"\nCRSP daily derived variables run ended at {datetime.now()}.\n")

    return

# makeCRSPDailyDerivedVariables(params=params)


