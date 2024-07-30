import requests
import os
# from dotenv import load_dotenv
import json
import pandas as pd
import numpy as np
import calendar
import yfinance as yf

# from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime as dt

from volatility import volest



############################
#
#       CONSTANTS
#
############################

symbol = 'GME'
SYMBOL = 'GME'
bench = 'XRT'
estimator = 'GarmanKlass'

start_year = 2023
now_year = 2024
TRADING_WINDOW = 35

windows = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90]  # num days used to compute volatility
quantiles = [0.25, 0.75]  # percentage of the top and bottom 25% of values
bins = 100
normed = True

start = dt.datetime(2023,7,6)
# end = dt.datetime(2024,5,1)
end = dt.datetime.now()

min_ = []
max_ = []
median = []
top_q = []
bottom_q = []
realized = []

############################
#
#       FUNCTIONS
#
############################

def fetch_options_data(SYMBOL='GME', source='alphavantage', API_KEY='AC4AQOG7U1ZVWYVN'):

    # API_KEY=os.getenv('API_KEY')
    if source == 'alphavantage':
        api_endpoint_options = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={SYMBOL}&apikey={API_KEY}'
    
    r = requests.get(api_endpoint_options)
    data_json = r.json()

    if 'data' not in data_json:
        raise ValueError("No data found in the API response")
    
    df = pd.DataFrame(data_json['data'])

    # call_options = data_df[data_df['type'] == 'call']
    return df

def fetch_trading_data(source='yahoo', symbol='GME'):
    if source == 'yahoo':
        trading_data = yf.download([symbol], start, end)
    return trading_data


def filter_options(options_df, type, strike_price):
    return options_df.query("type == 'call' and strike == @strike_price")


# options_data = fetch_options_data()

# call_25 = filter_options('call', '25.00')

# # print(call_25)

# for contract_id, implied_volatility in zip(call_25['contractID'], call_25['implied_volatility']):
#     print(f"\n{contract_id}: Implied Volatility: {implied_volatility}")

# call_data_json = call_25.to_json(orient='records', indent=4)

# print(call_data_json)

# print(json.dumps(fetch_call_data(), indent=4))


##########################
#
#      HISTORICAL CONES
#
#########################

gme_trading_data = fetch_trading_data()
gme_trading_data.symbol = symbol
xrt_trading_data = fetch_trading_data(symbol='XRT')
xrt_trading_data.symbol = 'XRT'

vol = volest.VolatilityEstimator(
    price_data=gme_trading_data,
    estimator=estimator,
    bench_data=xrt_trading_data
)

_, plopt = vol.cones(windows=windows, quantiles=quantiles)
plopt.show()






