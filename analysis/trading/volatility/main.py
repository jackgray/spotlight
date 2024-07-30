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



############################
#
#       CONSTANTS
#
############################

SYMBOL = 'GME'

call_bids,call_asks,put_bids,put_asks, = [],[],[],[]

# DTE = days to expiration
IV_DTE = []

start_year = 2023
now_year = 2024
TRADING_WINDOW = 35

windows = [30, 60, 90, 120]  # num days used to compute volatility
quantiles = [0.25, 0.75]  # percentage of the top and bottom 25% of values

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

def calc_sigmas(N, X, period=20):
    start = 0
    end = N
    results = []
    while end <= len(X):
        sigma = calc_sigma(N, X[start:end])
        results.append(sigma)
        # print('N: {}, sigma: {}'.format(N, sigma))
        start += period
        end += period
    sigmas = np.array(results)
    mean = sigmas.mean()
    # Uncomment the following three lines to use z scores instead of minimum
    # and maximum sigma values
    #
    # z_score=2.0
    # interval = sigmas.std() * z_score
    # return mean - interval, mean, mean + interval
    #
    return sigmas.min(), mean, sigmas.max()

def calc_daily_sigma(lookback, data):
    results = np.zeros(len(data))
    start = 0
    end = lookback
    results[start:end] = np.nan
    while end < len(data):
        results[end] = calc_sigma(lookback, data[start:end])
        start += 1
        end += 1
    return results

def calc_sigma(N, X):
    return sqrt(sum((X)**2) / float(N - 1)) * sqrt(252.0)


def lag(data):
    lagged = np.roll(data, 1)
    lagged[0] = 0.
    return lagged

def thirdThurs(year, month):
    '''
    Finds the 3rd Thursday of every month
    '''
    daysInMonth = calendar.monthrange(year, month)[1] # Returns tuple(month, numdays)
    date = dt.date(year, month, daysInMonth)
    offset = 4 - date.isoweekday()  # most recent Thursday
    if offset < 0: 
        offset -= 7
    date += dt.timedelta(offset)

    now = dt.date.today()
    
    if date.year == now.year and date.month ==now.month and date < now:
        raise Exception('Missed third Thursday')

    return date - dt.timedelta(7)



def historicalVolatility(df):
    df2 = df.copy()
    for date, val in df.iteritems():
        try:
            df2.loc[date] = round(volatility[df.name].loc[date, SYMBOL]*100,2)
        except:
            df2.loc[date] = np.nan

        return df2

def logReturns(closing_price, basis='D'):
    '''
    Daily basis='D'
    Weekly basis='W'
    Month basis='M'

    Log returns are commonly used in finance to analyze the rate of return on an asset
    log_returns = the natural log of the ratio of yesterday's price to today's price
    '''
    
    log_returns = (closing_price/closing_price.shift(1)).apply(np.log).dropna()
    
    if basis == 'D':
        return log_returns
    else:
        return log_returns.resample(basis).sum()
   

def periodicVolatility(log_returns, window):
    return log_returns.rolling(window=window).std()
    

def realizedVolatility(periodic_volatility, trading_periods=252):
    '''
    periodic volatility * sqrt of number of trading periods 

    252 trading days in a year for annualized volatility
    '''
    return periodic_volatility * np.sqrt(trading_periods)

     
def realized_vol(price_data, window=30):

    log_return = (price_data["Close"] / price_data["Close"].shift(1)).apply(np.log)
    
    return log_return.rolling(window=window, center=False).std() * np.sqrt(252)

def fetch_options_data(SYMBOL='GME', strike_price='25.00'):

    # API_KEY=os.getenv('API_KEY')
    API_KEY='AC4AQOG7U1ZVWYVN'
    api_endpoint_options = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={SYMBOL}&apikey={API_KEY}'
    r = requests.get(api_endpoint_options)
    data_json = r.json()

    if 'data' not in data_json:
        raise ValueError("No data found in the API response")
    
    data_df = pd.DataFrame(data_json['data'])

    # call_options = data_df[data_df['type'] == 'call']
    return data_df

def fetch_trading_data():
    trading_data = yf.download([SYMBOL], start, end)
    return trading_data


def closing_price(df, date):
    '''
    Get closing price for a given day from yahoo trading data df
    '''
    closing_prices = df.Close
    data = json.loads(closing_prices.to_json())   # Load df to JSON then to dictionary
    date_as_timestamp = pd.Timestamp(date).timestamp() * 1000  # Convert date to milliseconds since epoch
    closing_price = data.get(str(int(date_as_timestamp)), None)
    return closing_price

def query_IV():
    pass

# options_data = fetch_options_data()

# def filter_options(type, strike_price):
#     return options_data.query("type == 'call' and strike == @strike_price")

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

trading_data = fetch_trading_data()
options_data = fetch_options_data()
print(options_data.to_json(orient='index', indent=4))   
# print(trading_data)

# periodic_volatility(log_returns_daily, 35)
# print(realized_vol(trading_data, 5))
for window in windows:

    estimator = realized_vol(trading_data, window)

    min_.append(estimator.min())
    max_.append(estimator.max())
    median.append(estimator.median())
    top_q.append(estimator.quantile(quantiles[1]))
    bottom_q.append(estimator.quantile(quantiles[0]))
    realized.append(estimator[-1])

print(realized)




# create the plots on the chart
plt.plot(windows, min_, "-o", linewidth=1, label="Min")
plt.plot(windows, max_, "-o", linewidth=1, label="Max")
plt.plot(windows, median, "-o", linewidth=1, label="Median")
plt.plot(windows, top_q, "-o", linewidth=1, label=f"{quantiles[1] * 100:.0f} Prctl")
plt.plot(windows, bottom_q, "-o", linewidth=1, label=f"{quantiles[0] * 100:.0f} Prctl")
plt.plot(windows, realized, "ro-.", linewidth=1, label="Realized")

# set the x-axis labels
plt.xticks(windows)

# format the legend
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
plt.show()
# Gather dates to analyze (apply function)
dates = [thirdThurs(year, month) for year in range(start_year, now_year) for month in range(1,13) if thirdThurs(year, month) < dt.datetime.now().date()]

column_names = ['1-mth', '3-mth', '6-mth', '9-mth', '12-mth']
trading_days = [int(20*n) for n in [1,3,6,9,12]]
DTE = [int(30*n) for n in [1,3,6,9,12]]     # Days to expiration. Assumes 30 days in all months
data = np.array([np.arange(len(dates))]*len(column_names)).T


# Download trading data for stock between start and end dates







# periodic volatility = std deviation of returns over given period 
#  create a rolling window of the number
# weekly_volatility = log_returns_weekly.rolling(window=5).std()

# annualized_weekly_volatility_daily_basis = weekly_volatility * np.sqrt(252)
# annualized_weekly_volatility_weekly_basis = weekly_volatility * np.sqrt(52)



# print("Volatility: ", volatility)
# volatility.plot()
# plt.show()

def plotit(df):

    df2 = pd.DataFrame(data='', columns=['max', 'mean', 'min'], index=DTE)
    df2.index.name = 'DTE'

    df2['max'] = pd.Series(df[column_names].max().values, index=DTE)
    df2['mean'] = pd.Series(df[column_names].mean().values, index=DTE)
    df2['min'] = pd.Series(df[column_names].min().values, index=DTE)

    fig1 = plt.figure(figsize=(12,8))
    ax1 = fig1.add_subplot(111)

    plt.plot(df2.index, df2['max'], 'k+-')
    plt.plot(df2.index, df2['mean'], 'ms-')

    plt.plot(df2.index, df.iloc[-1,:], 'gs-')

    plt.plot(df2.index, df2['min'], 'k+-')

    df = pd.DataFrame(data, columns=column_names, index=dates)
    df.index.name = 'period'



    df = df.apply(lambda x: historical_vol(x), axis=0)

