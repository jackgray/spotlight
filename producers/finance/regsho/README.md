
# NYSE Data

## Regulation SHO Daily Threshold Data



### Multiple Data Sources
Reg SHO (Regulation SHO) threshold lists are published by various entities to provide transparency into stocks with significant levels of fails-to-deliver (FTDs). The reporting of these lists can vary based on where and how the trades are executed.

NYSE
NASDAQ
FINRA
Cboe Global Markets (including BZX, BYX, EDGX, and EDGA)
NYSE American
OTC Markets Group

This component so far aggregates data from Nasdaq, NYSE, and FINRA. 

Nasdaq and NYSE fortunately have the same schema, but require different URL query parameters and use different datestring formats to call the data

Example from Nasdaq: `http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth20240130.txt`

Example from NYSE: `https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate=03-Feb-2024&market=NYSE`





# NASDAQ
Stocks like KOSS (Koss Corporation) are traded on NASDAQ, which reports FTDs for its listed securities.

Nasdaq stopped including securities that reached the threshold due to OTC trades in 2014. This should be reported by FINRA.



Source:

https://www.nasdaqtrader.com/trader.aspx?id=regshothreshold

## Short Sale Circuit Breaker
The SEC adopted amendments to Regulation SHO with a compliance date of November 10, 2010. Among the rule changes, the SEC introduced Rule 201 (Alternative Uptick Rule), a short sale-related circuit breaker that when triggered, will impose a restriction on prices at which securities may be sold short. The SEC also issued guidance for broker-dealers wishing to mark certain qualifying orders 201cshort exempt.

This could be worth looking into. KOSS shows up a lot these days.

https://www.nasdaqtrader.com/trader.aspx?id=ShortSaleCircuitBreaker


# FINRA 
FINRA provides separate reports for FTDs related to OTC trades and "Other OTC" trades. This distinction helps differentiate between the standard OTC market and less regulated OTC markets.

## OTC (Over-The-Counter) Trades
These are trades conducted directly between parties without the use of a central exchange. FINRA (Financial Industry Regulatory Authority) reports FTDs for OTC trades.

## Other OTC
This category includes trades that are not listed on major exchanges and are typically traded through OTC markets. FINRA also reports FTDs for these trades.

## Query API
FINRA's Query API has reports on OTC RegSHO lists, GME does not pop up in this database. 

## Requirements
Note that using the FINRA Query API requires a free account API key, and code to generate a session key for 30 minutes of connection at a time

## Schema Mapping
The column names do not match, NYSE AND Nasdaq reporting schema, so the function `clean_df()` converts them to NYSE/Nasdaq equivalents




## Data Source Info
https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock

## Rule 3210 -- Accounts At Other Broker-Dealers and Financial Institutions
https://www.investopedia.com/financial-advisor/what-advisors-need-know-about-rule-3210/#:~:text=FINRA%20Rule%203210%20was%20adopted,at%20any%20other%20financial%20institution.
https://www.finra.org/rules-guidance/rulebooks/finra-rules/3210

## Rule 4320 -- Short Sale Delivery Requirements
https://www.finra.org/rules-guidance/rulebooks/finra-rules/4320

## market code (TRFs)
https://www.finra.org/filing-reporting/trade-reporting-facility-trf

There are 3 Trade Reporting Facilities in FINRA: NYTRF (NYSE), NCTRF (Nasdaq Carteret), and 


# NYSE (New York Stock Exchange)
Stocks like GME (GameStop) are traded on major exchanges like the NYSE. The exchange reports FTDs for these listed securities.

https://www.nyse.com/regulation/threshold-securities

If we go to this data source at NYSE, and search dates we know GME existed on the threshold list like 02/02/2021, we can finally see GME.

# Other sources?

Where else is data being reported that we simply cannot access? Are there other data sources we don't know about?

# ICE

This is a newer intermediary with their own swap data repository, where it is legal for institutions to file a swap with ICE, instead of the SEC or DTCC, and remain anonymous to everyone except the participants in the contract.

Most of the data reported here is not available to the public


### Requirements

DuckDB - crazy light and fast to install, no configuration needed
python3
pip packages
### Usage



### Queries

Enter the database with `duckdb gme.duckdb` or whatever you named the db

To query the top 5 most occurring stocks on Reg SHO Daily Threshold list and display their rate of occurence

```
SELECT
    Symbol,
    COUNT(*) AS count
FROM
    regsho_daily_nyse_nasdaq
WHERE
    "Reg SHO Threshold Flag" = 'Y'
    AND "Date" > '2019-01-02'
GROUP BY
    Symbol
ORDER BY
    count DESC
LIMIT 15;
```

Combine tables from nyse nasdaq and finra
```

```
To query stocks related to GME:

```
SELECT * FROM regsho_daily
WHERE Symbol IN ('GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF');
```

Create a CSV file

```
COPY regsho_daily TO 'regsho_complete.csv' (HEADER, DELIMITER ',');
```