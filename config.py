import pandas as pd
import os

'''-----------------------global-constant--------------------------'''

market = 'HK'
mkt_idx_name = 'HSCI'
strategy_name = 'Sector Rotate'

test_method = 'single period'  # "rolling" or "single period"
test_beg_yr = 2008
train_set_period = 0
test_set_period = 11
optim_param = 'sharpe'
sim_sec_cnt_min = 3
sim_sec_cnt_max = 8
roll_increm_yr = 0
roll_freq = 1

num_of_sec_chosen = 4  # for single period or signal update only

initial_NAV = 1000000
qtr_to_semi_ratio = 2

signal_beg_date = pd.to_datetime('1998Q4').to_period("Q")
trade_days = 252
line_grph_title = "Sector Rotation NAV Growth"
bar_grph_title = 'Semiannual Return'
scat_grph_title = 'Performance of various No. of sector(s) picked'

pre_csv = {"earn_g": "earnings_growth_bloomberg.csv",
           mkt_idx_name: mkt_idx_name + '_bloomberg.csv',
           'mkt_cap': 'market cap_bloomberg.csv',
           'px': 'prices_bloomberg.csv'}

post_csv = {"earn_g": "earnings growth.csv",
            mkt_idx_name: mkt_idx_name + '.csv',
            'mkt_cap': 'market cap.csv',
            'px': 'prices.csv'}

directory = {"pre": "Pre-amend/" + market + "/",
             "post": "Post-amend/" + market + "/",
             "ssr": "Sector Selection Result/"}

sec_league_tbl = {"CD": "Consumer Discretionary",
                  "CS": "Consumer Staples",
                  "Energy": "Energy",
                  "Financials": "Financials",
                  "Healthcare": "Health Care",
                  "Industrials": "Industrials",
                  "IT": "Information Technology",
                  "Materials": "Materials",
                  "RealEstate": "Real Estate",
                  "Telecom": "Telecommunication Services",
                  "Utilities": "Utilities"}

'''------------------------global-variable--------------------------'''

param_cls_dict = {}
mktidx_cls_dict = {}
updated_csv_data = {}
sec_eval_cls_dict = {}
stats_summary = []
fig_dict = {}

'''------------------------global-method----------------------------'''


def getDateComponent(date):
    if date != "#N/A N/A" and date != "":
        day = date.split("/")[0]
        month = date.split("/")[1]
        year = date.split("/")[2]
        return day, month, year
    else:
        return ""


def refmtDateList(date_list):
    date_list = list(map(getDateComponent, date_list))
    date_list = ['.'.join(x) for x in date_list]
    date_list = pd.to_datetime(date_list, dayfirst=True)
    return date_list


def rfmtToSemiannual(datelist):
    semi_date = []
    quarter_dates = pd.to_datetime(datelist).to_period("Q")
    for idx, _ in enumerate(quarter_dates):
        if quarter_dates[idx].quarter <= qtr_to_semi_ratio:
            semi_date.append(str(quarter_dates[idx].year)+'Q2')
        else:
            semi_date.append(str(quarter_dates[idx].year)+'Q4')
    semi_date = pd.to_datetime(semi_date).to_period('Q')
    return semi_date


def getTestBegEndYr(test_roll_freq):
    if test_beg_yr <= 2000 or test_beg_yr >= 2018:
        print("Use Default Year: 2000")
        return pd.to_datetime(str(2000 + test_roll_freq*roll_increm_yr)),\
            pd.to_datetime(str(2000 + train_set_period + test_roll_freq*roll_increm_yr)),\
            pd.to_datetime(str(2000 + train_set_period + test_roll_freq*roll_increm_yr + test_set_period))
    else:
        return pd.to_datetime(str(test_beg_yr + test_roll_freq*roll_increm_yr)),\
            pd.to_datetime(str(test_beg_yr + train_set_period + test_roll_freq*roll_increm_yr)),\
            pd.to_datetime(str(test_beg_yr + train_set_period + test_roll_freq*roll_increm_yr + test_set_period))


def setupFolder(folder_abbr):
    if not os.path.exists(directory[folder_abbr]):
        os.makedirs(directory[folder_abbr])
