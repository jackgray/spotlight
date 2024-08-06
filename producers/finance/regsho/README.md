

# Regulation SHO (Reg SHO) Daily Threshold Data

This component so far aggregates data from Nasdaq, NYSE, and FINRA. It aims to aggregate all Reg SHO threshold reports.

## About Reg SHO
https://www.investopedia.com/terms/t/thresholdlist.asp#toc-understanding-threshold-lists

A threshold list, also known as a Regulation SHO Threshold Security List, is a list of securities whose transactions failed to clear for five consecutive settlement days at a registered clearing agency.

Threshold lists are published in accordance with regulations set by the Securities and Exchange Commission (SEC). Regulators review this information as part of their efforts to detect market manipulation.

In January 2005, the SEC implemented Regulation SHO to reduce the abuse of naked short selling, where the seller does not borrow or arrange to borrow the securities in time to make delivery to the buyer within the standard two-day settlement period. As a result, the seller fails to deliver securities to the buyer when delivery is due, known as a "failure to deliver" or "fail."

When naked short selling is used and the affected securities aren't delivered, the associated transactions will fail to clear. These failed transactions are reported regularly on a threshold list, and the SEC and other regulators can identify clues that improper naked short selling may have occurred.

In order to appear on a threshold list, the security must be registered with the SEC and fail to settle for five or more consecutive days. The failed settlements must also involve a transaction size totaling 10,000 shares or more, or at least 0.5% of the security's shares outstanding. Securities that meet these criteria and are included on the list are known as threshold securities. - Investopedia

The reporting of these lists can vary based on where and how the trades are executed.

They are are mandated to be publicly available to ensure transparency and market integrity, but finding the right place to look can be tricky, which is why this project aims to pull all the lists into one place with a unified schema



## Data Sources
Reg SHO Threshold lists are reported by the following agencies. There should not be overlap between them except potentially in the OTC Markets Group reports, as their exchanges are expected to be overseen and reported on by FINRA

- NYSE/NYSE American
- Nasdaq
- FINRA
- Cboe Global Markets (including BZX, BYX, EDGX, and EDGA)
- OTC Markets Group


Nasdaq and NYSE fortunately have the same schema, but require different URL query parameters and use different datestring formats to call the data

Example from Nasdaq: `http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth20240130.txt`

Example from NYSE: `https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate=03-Feb-2024&market=NYSE`





### NASDAQ
Stocks like KOSS (Koss Corporation) are traded on Nasdaq, which reports FTDs for its listed securities.

Nasdaq stopped including securities that reached the threshold due to OTC trades in 2014. It is unclear how far back FINRA reporting goes for Nasdaq OTC equities, if it reported on them before 2014 creating an overlap between those and Nasdaq reports, or if FINRA only started reporting when Nasdaq stopped.


Source:

https://www.nasdaqtrader.com/trader.aspx?id=regshothreshold

##### Short Sale Circuit Breaker
The SEC adopted amendments to Regulation SHO with a compliance date of November 10, 2010. Among the rule changes, the SEC introduced Rule 201 (Alternative Uptick Rule), a short sale-related circuit breaker that when triggered, will impose a restriction on prices at which securities may be sold short. The SEC also issued guidance for broker-dealers wishing to mark certain qualifying orders 201cshort exempt.

This could be worth looking into. KOSS shows up a lot these days.

https://www.nasdaqtrader.com/trader.aspx?id=ShortSaleCircuitBreaker


### FINRA 
FINRA provides separate reports for FTDs related to OTC trades and "Other OTC" trades. This distinction helps differentiate between the standard OTC market and less regulated OTC markets.

#### OTC (Over-The-Counter) Trades
These are trades conducted directly between parties without the use of a central exchange. FINRA (Financial Industry Regulatory Authority) reports FTDs for OTC trades.

#### Other OTC
This category includes trades that are not listed on major exchanges and are typically traded through OTC markets. FINRA also reports FTDs for these trades.

#### Trade Reporting Facilities (TRFs)
Platforms established by FINRA to facilitate the reporting of over-the-counter (OTC) trades in equities and related securities. These facilities play a crucial role in ensuring transparency and regulatory compliance in the trading of securities that are not listed on national exchanges or are traded off-exchange. 

TRF Exchange Participants: https://www.finra.org/filing-reporting/trf/trf-exchange-participants

FINRA currently has 3 active TRFs
NYSE TRF, and 2 Nasdaq TRFs: 

##### NYSE Trade Reporting Facility (NYTRF)
Provides a platform for reporting trades executed away from the NYSE and ensures that all trades, including those in listed and non-listed securities, are reported to a centralized system.

It facilitates trade reporting for equities and equity-related products, ensures compliance with regulatory reporting requirements, and integrates with the NYSE’s trading and clearing systems.

https://www.finra.org/sites/default/files/nyse-trf-fix-specification.pdf

##### Nasdaq Trade Reporting Facility (NCTRF/?TRF)
Nasdaq TRF Carteret/ Nasdaq TRF Chicago

Serves as a platform for reporting trades in Nasdaq-listed securities and other equities. It supports trade reporting for both listed and off-exchange trades. 

###### Nasdaq Chicago TRF
A short sale executed on an alternative trading system (ATS) or through a broker-dealer not connected to Nasdaq’s infrastructure would be reported here. For instance, if a trade is executed off-exchange through an ATS in Chicago, this TRF captures and reports that data.

###### Nasdaq Carteret TRF
A short sale on a Nasdaq-listed security that takes place directly within Nasdaq’s trading environment or through its systems might be reported here. For example, if a trader shorts a Nasdaq-listed stock via Nasdaq’s own platform, the Carteret TRF reports this transaction.

https://nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/fixactspec.pdf

#### Nasdaq Chicago TRF
##### Cboe Trade Reporting Facility (Cboe TRF)
Operated by Cboe Global Markets. Originally known as the BATS TRF before Cboe acquired BATS Global Markets. It reports trades executed off-exchange, including those in equities listed on various exchanges and non-listed securities.

#### Query API
FINRA's Query API has reports on OTC RegSHO lists, GME does not pop up in this database. 

#### Requirements
Note that using the FINRA Query API requires a free account API key, and code to generate a session key for 30 minutes of connection at a time

#### Schema Mapping
The column names do not match NYSE AND Nasdaq reporting schema, so the function `clean_df()` converts them to NYSE/Nasdaq equivalents


#### Data Source Info
https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock

#### Rule 3210 -- Accounts At Other Broker-Dealers and Financial Institutions
https://www.investopedia.com/financial-advisor/what-advisors-need-know-about-rule-3210/#:~:text=FINRA%20Rule%203210%20was%20adopted,at%20any%20other%20financial%20institution.
https://www.finra.org/rules-guidance/rulebooks/finra-rules/3210

#### Rule 4320 -- Short Sale Delivery Requirements
https://www.finra.org/rules-guidance/rulebooks/finra-rules/4320

#### market code (TRFs)
https://www.finra.org/filing-reporting/trade-reporting-facility-trf

There are 3 Trade Reporting Facilities in FINRA: NYTRF (NYSE), NCTRF (Nasdaq Carteret), and 

 ##### NYTRF 
 provides a platform for reporting trades executed away from the NYSE and ensures that all trades, including those in listed and non-listed securities, are reported to a centralized system.

### NYSE (New York Stock Exchange)
Stocks like GME (GameStop) are traded on major exchanges like the NYSE. The exchange reports FTDs for these listed securities.

https://www.nyse.com/regulation/threshold-securities

If we go to this data source at NYSE, and search dates we know GME existed on the threshold list like 02/02/2021, we can finally see GME.

### CBOE (Chicago Board Options Exchange) Global Markets
Cboe operates various exchanges for trading options, equities, futures, and other financial instruments.

Includes a broad range of financial instruments, particularly options and ETFs.

This includes the Cboe BZX Exchange, Cboe BYX Exchange, Cboe EDGX Exchange, and Cboe EDGA Exchange. These exchanges also provide threshold lists for securities traded on their platforms.


### OTC Markets Group
OTC Markets Group operates the following market tiers, all of which are subject to FINRA oversight in terms of broker-dealer activity and trade reporting:

#### OTCQX
The highest tier, for well-established, investor-focused companies.
#### OTCQB
The venture market, for early-stage and developing companies.
Pink Market: Includes a wide variety of companies, from speculative penny stocks to distressed companies.

The threshold qualifications are different for SEC reporting issuers and non-SEC reporting issuers (see definitions). Reporting companies are governed by Reg SHO and non-reporting companies are governed by Rule 4320. -OTC Markets

OTC Markets is subject to lighter regulatory scrutiny compared to major exchanges. However, they still must comply with SEC regulations, including Reg SHO.

Stocks reported on the Reg SHO lists by OTC Markets Group and FINRA *should* *appear on FINRA's list, as FINRA has oversight over the exchanges listed by OTC Markets Group


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

Source: 

https://www.otcmarkets.com/market-activity/reg-sho-data

### Summary
While FINRA oversees most OTC trading in the U.S., certain specialized trading platforms like ATSs, ECNs, and international OTC markets may operate under different regulatory frameworks or additional layers of oversight. However, these still fall under broader SEC regulations, ensuring that even if FINRA isn't the primary overseer, there are stringent regulatory mechanisms in place.




## ICE (Intercontinental Exchange)

ICE owns and operates multiple exchanges, including the NYSE.

In theory, any securities traded on ICE-owned exchanges that meet the Reg SHO threshold criteria would be reported as part of the public threshold lists through the NYSE or other relevant exchanges.

ICE itself does not typically produce separate, undisclosed Reg SHO threshold lists; instead, it complies with the SEC's requirements for public disclosure through its exchanges.

Explore data reported through ICE here 
https://www.ice.com/report-center


## Usage

### Example Usage

This directory uses api.py scripts to make calls to Reg SHO Lists via a variety of HTTP requests from various sources.

Included is a file that shows example usage of these functions.

```
from api import regsho_by_range

df = regsho_by_range(start_date='20140101', end_date='20190101' data_source='nasdaq', db_path='./regsho.duckdb')
        if df:
            print("Some rows were not added to duckdb")
            print(df)
        else:
            print("All downloaded data was inserted successfully")
```

This will create a new table in DuckDB called {data_source}_regsho_daily

The next version will allow CSV file export of the data.

To run all in one go, create an array and loop through all the data sources
```
sources = ['finra', 'nasdaq', 'nyse']
for source in sources:
    df = regsho_by_range(start_date='20140101', end_date='20190101' data_source=source, db_path='./regsho.duckdb')
```


Everything should be achieved by the command `regsho_by_range()`, which uses the other functions to make calls to the various sources by date range. Setting the start_date equal to end_date should get you one date, and changing the source should allow you to filter that source. DuckDB integrates well with dataframes and exports to CSV easily so you can play with the data how you normally would without having to clean it.

If you don't pip install duckdb then the table load should fail and you will receive a dataframe back. Depending on the request size, this may be memory intensive.

### Requirements
DuckDB - crazy light and fast to install, no configuration needed

python3 (3.11 recommended)

pip packages: datetime, pandas, duckdb, dotenv


Note that for FINRA to be used as a source, you must have a .env file in the same directory with an API key and secret. The secret is a password you set through a confirmation email link after creating an API token in FINRA's API Console. You can access this by creating a free individual investor account. 

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

To combine tables from nyse nasdaq and finra:
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