import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm
import datetime

# Fetch historical data for GameStop
ticker = 'GME'
start_date = '2020-01-01'
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate daily returns
data['Returns'] = data['Adj Close'].pct_change()

# Define function to calculate historical volatility
def historical_volatility(returns, window):
    return returns.rolling(window=window).std() * np.sqrt(252)

# Define function to calculate volatility cone
def volatility_cone(returns, time_horizons, confidence_level=0.95):
    volatilities = {horizon: historical_volatility(returns, horizon) for horizon in time_horizons}
    stats = {
        horizon: {
            'mean': volatilities[horizon].mean(),
            'std': volatilities[horizon].std(),
            'percentile': {
                'lower': volatilities[horizon].quantile((1 - confidence_level) / 2),
                'upper': volatilities[horizon].quantile(1 - (1 - confidence_level) / 2)
            }
        }
        for horizon in time_horizons
    }
    return stats

# Define time horizons
time_horizons = [5, 10, 20, 60, 120]  # in days

# Calculate volatility cone
volatility_stats = volatility_cone(data['Returns'].dropna(), time_horizons)

# Plot volatility cone
plt.figure(figsize=(12, 8))
for horizon in time_horizons:
    mean_vol = volatility_stats[horizon]['mean']
    lower_vol = volatility_stats[horizon]['percentile']['lower']
    upper_vol = volatility_stats[horizon]['percentile']['upper']
    plt.plot([horizon, horizon], [lower_vol, upper_vol], color='blue')
    plt.scatter(horizon, mean_vol, color='red')
plt.title(f'Volatility Cone for {ticker}')
plt.xlabel('Time Horizon (days)')
plt.ylabel('Volatility')
plt.grid(True)
plt.show()

# Print out the calculated statistics
for horizon in time_horizons:
    stats = volatility_stats[horizon]
    print(f"Time Horizon: {horizon} days")
    print(f"Mean Volatility: {stats['mean']}")
    print(f"Lower {confidence_level*100}% Volatility: {stats['percentile']['lower']}")
    print(f"Upper {confidence_level*100}% Volatility: {stats['percentile']['upper']}")
    print('-' * 40)
