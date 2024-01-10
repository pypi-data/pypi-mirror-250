import AssayingAnomalies.Functions as aa
from AssayingAnomalies.Functions import estFactorRegs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
import os
from AssayingAnomalies import Config


params = Config()
params.prompt_user()
params.make_folders()
path = r"C:\Users\josh\OneDrive - University at Buffalo\Desktop\Spring_2023\AssayingAnomalies-main\AssayingAnomalies-main\Data" + os.sep


raw_data = pd.read_csv(r'C:\Users\josh\Downloads\OK_portfolios.csv', index_col=0)
plt.close()
fig, ax = plt.subplots(1, 1)
ax.plot(raw_data.index, raw_data.OMK)
ax.set(ylabel='OMK', xlabel='Date')

# estimate factor regs of OMK portfolios on the FF5 factors
ff = pd.read_csv(r'C:\Users\josh\OneDrive - University at Buffalo\Desktop\Spring_2023\AA_Test_Data\AA_Data\CRSP\ff.csv', index_col=0)

dates = np.array(raw_data.index)
test = aa.estFactorRegs(params=params, pret=np.array(raw_data), dates=dates, factorModel=5, addLongShort=0)
test['w'] = 'v'
test['hperiod'] = 1
aa.prt_sort_results(test)

# Test against RMW without CMA (investment)
factors = ff[['mkt', 'smb', 'hml', 'rmw']]
factors.index = ff.dates
test2 = estFactorRegs(params, np.array(raw_data), dates, factorModel=factors, addLongShort=0)
test2['w'] = 'v'
test2['hperiod'] = 1
aa.prt_sort_results(test2)

def to_latex_table(text):
    lines = text.split('\n')
    headers = [''] + lines[4].split()[1:]
    latex_table = []

    latex_table.append('\\begin{table}[ht]')
    latex_table.append('\\centering')
    latex_table.append('\\begin{tabular}{|l|' + 'r|' * len(headers) + '}')

    # Header row
    latex_table.append('\\hline')
    header_row = ' & '.join(headers) + ' \\\\'
    latex_table.append(header_row)
    latex_table.append('\\hline')

    # Content rows
    for i in range(5, len(lines) - 2, 2):
        row_data = lines[i].split()
        row_values = ' & '.join(row_data) + ' \\\\'
        latex_table.append(row_values)

        if i + 1 < len(lines) - 2:  # Check if there are significance values
            sig_values = lines[i + 1].split()
            sig_row = ' & '.join([''] + sig_values) + ' \\\\'
            latex_table.append(sig_row)

    latex_table.append('\\hline')
    latex_table.append('\\end{tabular}')
    latex_table.append('\\caption{Value-weighted portfolio sort, 1-month holding period: Excess returns, alphas, and loadings on the Fama and French 5-factor model.}')
    latex_table.append('\\label{tab:my_label}')
    latex_table.append('\\end{table}')

    return '\n'.join(latex_table)

testing = to_latex_table(text)

# Test against Roberts profitability
factors = ff[['mkt', 'smb', 'hml', 'roberts']]


# from AssayingAnomalies.Functions.makeBivSortInd import makeBivSortInd
#
xsga = scipy.io.loadmat(path + 'COMPUSTAT' + os.sep + 'XSGA.mat')['XSGA']
assets = scipy.io.loadmat(path + 'COMPUSTAT' + os.sep + 'AT.mat')['AT']
dates = scipy.io.loadmat(path + os.sep + 'CRSP' + os.sep + 'dates.mat')['dates']
dates = dates.flatten()

# initialize O_0 = SGA_0/(0.10 + 0.15)
O_0 =

R = scipy.io.loadmat(path + 'R.mat')['R']
# # R = pd.read_csv(path + 'R.csv', index_col=0)
# me = scipy.io.loadmat(path + 'me.mat')['me']
# NYSE = scipy.io.loadmat(path + 'NYSE.mat')['NYSE']
# ind1 = makeBivSortInd(me, 5, R, 5)
# ret = scipy.io.loadmat(path + 'ret.mat')['ret']
# test_res1, test_cond_res1 = runBivSort(params=params, ret=ret, ind=ind1, nptf1=5, nptf2=5, dates=dates, mcap=me)
#
# ind2 = makeBivSortInd(me, 2, R, [30, 70])
# test_res2, test_cond_res2 = runBivSort(params=params, ret=ret, ind=ind2, nptf1=3, nptf2=2, dates=dates, mcap=me)
#
# ind3 = makeBivSortInd(me, 5, R, 5, sort_type='conditional')
# test_res3, test_cond_res3 = runBivSort(params=params, ret=ret, ind=ind3, nptf1=5, nptf2=5, dates=dates, mcap=me)
