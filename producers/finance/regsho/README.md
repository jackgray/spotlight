

# Regulation SHO (Reg SHO) Daily Threshold Data (README)

This component so far aggregates data from Nasdaq, NYSE, Cboe-BZX, and FINRA. It aims to aggregate all Reg SHO threshold reports.

The reporting of these lists can vary based on where and how the trades are executed.

They are are mandated to be publicly available, but finding the right place to look can be tricky, which is why this project aims to pull all the lists into one place with a unified schema


## Data Sources
Reg SHO Threshold lists are reported separately by the respective agencies that manage the exchanges where the transactions failing settlement take place. There should not be overlap between them except potentially in the OTC Markets Group reports, as their exchanges are expected to be overseen and reported on by FINRA, but this script does not yet pull data from this source. This is a list of all of my known sources for Reg SHO Threshold reporting.

- NYSE/NYSE American (non-OTC)
- Nasdaq (non-OTC after Nov 17, 2014)
- FINRA (OTC Equities from Nasdaq and NYSE)
- Cboe Global Markets (including BZX, BYX, EDGX, and EDGA)
- OTC Markets Group (theoretically covered by FINRA reporting)


Nasdaq and NYSE fortunately have the same schema, but require different URL query parameters and use different datestring formats to call the data.

Example from Nasdaq: `http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth20240130.txt`

Example from NYSE: `https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate=03-Feb-2024&market=NYSE`

Cboe-BZX: `https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/2013-03-20/csv` -- The script will map Company Name to correspond to the standard 'Security Name' field name

FINRA reports require wrapping API requests with a session token, then need their field names to be mapped to correspond to Nasdaq and NYSE schema in order to consolidate the records into the same table

A description of the original data can be found here: https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock


### NASDAQ
Stocks like KOSS (Koss Corporation) are traded on Nasdaq, which reports FTDs for its listed securities.

Nasdaq stopped including securities that reached the threshold due to OTC trades in 2014. It is unclear how far back FINRA reporting goes for Nasdaq OTC equities, if it reported on them before 2014 creating an overlap between those and Nasdaq reports, or if FINRA only started reporting when Nasdaq stopped.

Nasdaq reports FTDs on 3 of their primary equities markets are designated in the reports by their letter code:
- Q - NASDAQ Global Select Market (NGS)
- G - NASDAQ Global Market (NGM)
- S - NASDAQ Capital Market

Reference:
https://www.nasdaqtrader.com/Trader.aspx?id=RegShoDefs
https://www.nasdaqtrader.com/trader.aspx?id=regshothreshold

##### Short Sale Circuit Breaker
The SEC adopted amendments to Regulation SHO with a compliance date of November 10, 2010. Among the rule changes, the SEC introduced Rule 201 (Alternative Uptick Rule), a short sale-related circuit breaker that when triggered, will impose a restriction on prices at which securities may be sold short. The SEC also issued guidance for broker-dealers wishing to mark certain qualifying orders 201cshort exempt.

This could be worth looking into. KOSS shows up a lot these days.

https://www.nasdaqtrader.com/trader.aspx?id=ShortSaleCircuitBreaker


### FINRA 
FINRA provides separate reports for FTDs related to OTC trades and "Other OTC" trades. This distinction helps differentiate between the standard OTC market and less regulated OTC markets.

OTC trades conducted directly between parties without the use of a central exchange, while "Other OTC" denotes trades that are not listed on major exchanges and are typically traded through OTC markets. 

#### Requirements
Note that using the FINRA Query API requires a free account API key, and code to generate a session key for 30 minutes of connection at a time. The code is available in api.get_finra_session()

#### Schema Mapping
The column names in FINRA datasets do not match NYSE AND Nasdaq reporting schema, so the function `clean_df()` converts them to NYSE/Nasdaq equivalents (left hand side is the original field name in the FINRA dataset):
```
    'tradeDate': 'Date',
    'issueSymbolIdentifier': 'Symbol',
    'issueName': 'Security Name',
    'marketClassCode': 'Market Category',
    'marketCategoryDescription': 'Market',
    'thresholdListFlag': 'Threshold List Flag',
    'regShoThresholdFlag': 'Reg SHO Threshold Flag',
    'rule4320Flag': 'FINRA Rule 4320 Flag'
```

#### Data Source Info
https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock

#### Rule 3210 -- Accounts At Other Broker-Dealers and Financial Institutions
https://www.investopedia.com/financial-advisor/what-advisors-need-know-about-rule-3210/#:~:text=FINRA%20Rule%203210%20was%20adopted,at%20any%20other%20financial%20institution.
https://www.finra.org/rules-guidance/rulebooks/finra-rules/3210

#### Rule 4320 -- Short Sale Delivery Requirements
https://www.finra.org/rules-guidance/rulebooks/finra-rules/4320


### NYSE (New York Stock Exchange)
Exchange where most large companies are traded on. It reports on FTDs that occur on it's platforms, while FINRA reports on FTDs that occur for NYSE securities on OTC platforms

https://www.nyse.com/regulation/threshold-securities


NYSE has 3 exchanges: NYSE, NYSE American, and NYSE Arca. This component scans all by default, or can be set to pull select marketpaces.


### CBOE (Chicago Board Options Exchange) Global Markets
Cboe operates various exchanges for trading options, equities, futures, and other financial instruments.

Includes a broad range of financial instruments, particularly options and ETFs.

This includes the Cboe BZX Exchange, Cboe BYX Exchange, Cboe EDGX Exchange, and Cboe EDGA Exchange. These exchanges also provide threshold lists for securities traded on their platforms.

I have added the ability to pull data from Cboe for BZX listed securities: `https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/` but that is the only exchange for which I can find these reports.    

Records go back as far as Sept. 02, 2014

### OTC Markets Group
OTC Markets Group operates the following market tiers, all of which are theoretically subject to FINRA oversight in terms of broker-dealer activity and trade reporting:

#### OTCQX
The highest tier, for well-established, investor-focused companies.
#### OTCQB
The venture market, for early-stage and developing companies.
Pink Market: Includes a wide variety of companies, from speculative penny stocks to distressed companies.

The threshold qualifications are different for SEC reporting issuers and non-SEC reporting issuers (see definitions). Reporting companies are governed by Reg SHO and non-reporting companies are governed by Rule 4320. -OTC Markets

Stocks reported on the Reg SHO lists by OTC Markets Group and FINRA *should* *appear on FINRA's list, as FINRA has oversight over the exchanges listed by OTC Markets Group. Still, I hope to scrape this data to confirm.


### Alternative Trading Systems (ATSs)
These are SEC-regulated but might have specific reporting requirements that differ slightly from traditional OTC markets. ATSs include dark pools, which facilitate private securities transactions. Any FTDs and Reg SHO lists *should* be reported to/by FINRA.

### Direct Market Access (DMA) and Electronic Communication Networks (ECNs)
These platforms allow broker-dealers to trade directly with each other, bypassing traditional exchanges, but are still generally under FINRA and SEC regulation. FTDs *should* be reported. 

### International OTC Markets
#### Foreign OTC Markets
Securities traded on foreign OTC markets might not fall under FINRA's direct oversight, although they might be subject to international regulations and oversight by foreign regulatory bodies.

### Private Placements and Exempt Transactions
#### Regulation D Offerings
These private placements are exempt from standard registration requirements but still have to comply with specific SEC rules. FINRA oversight applies to the broker-dealers involved in these transactions but not necessarily to the trading venues themselves.

Reference: 

https://www.otcmarkets.com/market-activity/reg-sho-data

### Summary
While FINRA oversees most OTC trading in the U.S., certain specialized trading platforms like ATSs, ECNs, and international OTC markets may operate under different regulatory frameworks or additional layers of oversight. They still fall under broader SEC regulations, but it's unclear where they would be published. If FINRA only has 3 active trade reporting facilities, and they are all associated with either Nasdaq or NYSE, it would depend on if those markets are reporting back to Nasdaq or NYSE.


## ICE (Intercontinental Exchange)

ICE owns and operates multiple exchanges, including the NYSE.

In theory, any securities traded on ICE-owned exchanges that meet the Reg SHO threshold criteria would be reported as part of the public threshold lists through the NYSE or other relevant exchanges.

ICE itself does not typically produce separate, undisclosed Reg SHO threshold lists; instead, it complies with the SEC's requirements for public disclosure through its exchanges.

Explore data reported through ICE here 
https://www.ice.com/report-center



Everything should be achieved by the command `regsho_by_range()`, which uses the other functions to make calls to the various sources by date range. Setting the start_date equal to end_date should get you one date, and changing the source should allow you to filter that source. DuckDB integrates well with dataframes and exports to CSV easily so you can play with the data how you normally would without having to clean it.

If you don't pip install duckdb then the table load should fail and you will receive a dataframe back. Depending on the request size, this may be memory intensive.



##### FINRA API KEY 
For FINRA to be used as a source, you must have a .env file in the same directory with an API key and secret. The secret is a password you set through a confirmation email link after creating an API token in FINRA's API Console. You can access this by creating a free individual investor account. 

hint--GME or related tickers didn't show up in my FINRA table

### Queries

To query the top n most occurring stocks on Reg SHO Daily Threshold list and display their rate of occurence

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

To combine tables from nyse nasdaq and finra (already performed by pipeline assuming all sources were retrieved):
```
CREATE TABLE regsho_daily AS
SELECT * FROM nasdaq_regsho_daily
UNION ALL
SELECT * FROM nyse_regsho_daily
UNION ALL
SELECT * FROM finra_regsho_daily
ORDER BY Date;
```

To query a list of stocks (examples are companies and ETFs possibly related to GME):
```
SELECT * FROM regsho_daily
WHERE Symbol IN ('GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF');
```

Create a CSV file:
```
COPY regsho_daily TO 'regsho_complete.csv' (HEADER, DELIMITER ',');
```

Create a csv file from query results
```
COPY (
    SELECT * FROM regsho_daily
    WHERE Symbol IN ('GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF')
) TO regsho_stonks.csv
```

To get the 5 most occuring stocks under each marketplace and each month:
```
CREATE TABLE monthly_heatmap AS 
WITH MonthlyCounts AS (
    SELECT
        SUBSTRING(CAST(Date AS VARCHAR), 1, 7) AS Month, -- Extract YYYY-MM
        Market,
        Symbol,
        COUNT(*) AS SymbolCount
    FROM
        regsho_daily
    GROUP BY
        SUBSTRING(CAST(Date AS VARCHAR), 1, 7), Market, Symbol
),
RankedSymbols AS (
    SELECT
        Month,
        Market,
        Symbol,
        SymbolCount,
        RANK() OVER (PARTITION BY Month, Market ORDER BY SymbolCount DESC) AS SymbolRank
    FROM
        MonthlyCounts
)
SELECT
    Month,
    Market,
    Symbol,
    SymbolCount
FROM
    RankedSymbols
WHERE
    SymbolRank <= 5
ORDER BY
    Month,
    Market,
    SymbolRank;
```

By Week
```
CREATE TABLE weekly_totals AS
WITH WeeklyCounts AS (
    SELECT
        strftime('%Y-%W', Date) AS Week, -- Extract YYYY-WW
        Market,
        Symbol,
        COUNT(*) AS SymbolCount
    FROM
        regsho_daily
    GROUP BY
        strftime('%Y-%W', Date), Market, Symbol
),
RankedSymbols AS (
    SELECT
        Week,
        Market,
        Symbol,
        SymbolCount,
        RANK() OVER (PARTITION BY Week, Market ORDER BY SymbolCount DESC) AS SymbolRank
    FROM
        WeeklyCounts
)
SELECT
    Week,
    Market,
    Symbol,
    SymbolCount
FROM
    RankedSymbols
WHERE
    SymbolRank <= 10
ORDER BY
    Week,
    Market,
    SymbolRank;
```