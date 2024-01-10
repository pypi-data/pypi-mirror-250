import numpy as np
import pandas as pd
import os


def makeAbdiRanaldi(params):
    crsp_path = params.crspFolder + os.sep
    daily_crsp_path = params.daily_crsp_folder + os.sep

    # Load the necessary variables
    dbidlo = pd.read_csv(daily_crsp_path + 'dbidlo.csv', index_col=0).astype(float)
    daskhi = pd.read_csv(daily_crsp_path + 'daskhi.csv', index_col=0).astype(float)
    ddates = pd.read_csv(daily_crsp_path + 'ddates.csv', index_col=0).astype(int)
    dprc = pd.read_csv(daily_crsp_path + 'dprc.csv', index_col=0).astype(float)
    dcfacpr = pd.read_csv(daily_crsp_path + 'dcfacpr.csv', index_col=0).astype(float)
    ret = pd.read_csv(crsp_path + 'ret.csv', index_col=0).astype(float)
    dates = pd.read_csv(crsp_path + 'dates.csv', index_col=0).astype(int)

    # Store the number of days and number of months
    nDays = len(ddates)
    nMonths = len(dates)

    # Create a copy of raw daily price matrix
    dprc_raw = dprc.copy()
    dhigh = dbidlo.copy()
    dlow = daskhi.copy()

    # Set the daily high and low for days when a stock does not trade to np.nan
    dhigh.iloc[dprc < 0 | np.isnan(dprc)] = np.nan
    dlow.iloc[dprc < 0 | np.isnan(dprc)] = np.nan

    # Mask where the stock didn't trade (dprc < 0 or NaN)
    mask = (dprc_raw < 0) | dprc_raw.isna()

    # Carry over the previous days daily high, low, and close on days when a stock doesn't trade. To achieve this, I
    # forward fill the masked data for dprc, dhigh, and dlow
    dprc.mask(mask).fillna(method='ffill', inplace=True)
    dhigh.mask(mask).fillna(method='ffill', inplace=True)
    dlow.mask(mask).fillna(method='ffill', inplace=True)

    # Take the absolute value of the daily price
    dprc = dprc.abs()

    # Store the midpoints of the low and high for t and tp1 (= t plus one)
    midpoint = (np.log(dlow) + np.log(dhigh)) / 2
    midpoint_tp1 = midpoint.shift(-1)

    # Set the days where the stock does not trade to nan
    dbidlo[dprc_raw < 0 | np.isnan(dprc_raw)] = np.nan
    daskhi[dprc_raw < 0 | np.isnan(dprc_raw)] = np.nan

    # Initiate the close-high-low effective spread measure
    chl = pd.DataFrame(np.nan, index=ddates.values.flatten(), columns=ret.columns)
    chl.index = pd.to_datetime(chl.index, format='%Y%m%d')

    # Calculate the spread
    c_t = np.log(dprc)
    s_hat_t = np.sqrt(np.maximum(4 * (c_t - midpoint) * (c_t - midpoint_tp1), 0))
    s_hat_t[s_hat_t < 0] = 0  # Set negative spreads to 0

    # Set s_hat_t index to datetime
    s_hat_t.index = ddates.values.flatten()
    s_hat_t.index = pd.to_datetime(s_hat_t.index, format='%Y%m%d')

    # Resample and calculate the mean spread for each month
    chl = s_hat_t.resample('M').mean()

    # Define a function to apply to each monthly group
    def check_applicable_days(group):
        criteria = (group['dprc_raw'] > 0) & \
                   group['dprc_raw'].notna() & \
                   group['dbidlo'].notna() & \
                   group['daskhi'].notna() & \
                   (group['daskhi'] - group['dbidlo'] != 0)

        # Count the number of days that meet the criteria for each stock
        valid_days_count = criteria.sum()

        # Check if each stock has at least 12 applicable days
        valid_stocks = valid_days_count >= 12
        return valid_stocks

    # Combine data into a single DataFrame for easy processing
    combined_data = pd.concat([dprc_raw, dbidlo, daskhi], keys=['dprc_raw', 'dbidlo', 'daskhi'], axis=1)
    combined_data.index = s_hat_t.index

    # Group by month and apply the function
    monthly_valid_stocks = combined_data.groupby(pd.Grouper(freq='M')).apply(check_applicable_days)

    chl = chl[monthly_valid_stocks]

    return chl