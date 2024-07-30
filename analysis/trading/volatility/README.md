# Volatility Cone Analysis with Python

Adapted from this article:
https://quantpy.com.au/black-scholes-model/historical-volatility-cones/

Which is based on ideas presented in this article https://www.m-x.ca/f_publications_en/cone_vol_en.pdf


## Some important concepts

Volatility cones are constructed as a benchmark to identify whether current implied volatilities are too high or too low

Time horizon matching is required while we apply the volatility cone method in practice (implied volatility corresponds with historical volatilities of the same DTE)

Historical volatilities: trading-day underlying price volatilities observed over a specific period. Participants generally use 20-day and 30-day historical volatilities. 

Implied volatility: represents current derivatives prices on the market, reflecting how variable option traders expect the underlying asset price to be over the life of the option. 



 Time horizons and stuff

 annualized 