
# NYSE Data

## Regulation SHO Daily Threshold Data



### Multiple Data Sources

Just like swap contracts, there are a number of disparate entities that these events may be reported to.

This component will aggregate data from Nasdaq, NYSE, and FINRA

Nasdaq and NYSE fortunately have the same schema, but require different URL query parameters and use different datestring formats to call the data

Example from Nasdaq: `http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth20240130.txt`

Example from NYSE: `https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate=03-Feb-2024&market=NYSE`

FINRA will be pulled using the FINRA Query REST API, which requires a free account API key, and code to generate a session key for 30 minutes of connection at a time

The column names do not match, so they will have to be mapped to the corresponding names for Nasdaq/NYSE



# NASDAQ

Nasdaq reports on companies that reached the Reg SHO daily threshold, but stopped including securities that reached the threshold due to OTC trades in 2014. You can find KOSS on this list, but not GME, CHWY, or any of the ETFs they're contained in

# FINRA 

FINRA's Query API has reports on OTC RegSHO lists, but you won't find GME there, either

I have made python functions to grab this data (you must make an account and generate an API key first), but you can check the text archives of specific dates here

https://otce.finra.org/otce/RegSHOThreshold/archives

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

# NYSE

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


To query stocks related to GME:

```
SELECT * FROM regsho_daily
WHERE Symbol IN ('GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF');
```

Create a CSV file

```
COPY regsho_daily TO 'regsho_complete.csv' (HEADER, DELIMITER ',');
```